import pickle
import pandas as pd
#from functools import reduce
import os

pd.set_option('display.max_columns', 100)

class Searcher:
    def __init__(self):
        # self.danbooru_df = pd.read_csv('danbooru_jpmerged.csv')
        # self.e621_df = pd.read_csv('e621_translated.csv')
        # self.default_userdict = pd.read_csv('default_userdict.csv')
        self.danbooru_df = pd.read_pickle('pickles/danbooru_df.pkl')
        self.e621_df = pd.read_pickle('pickles/e621_df.pkl')
        self.default_userdict = pd.read_pickle('pickles/default_userdict.pkl')
        self.default_userdict = self.default_userdict.fillna("")
        self.default_userdict["danbooru_tag"] = self.default_userdict["danbooru_tag"].str.split(',')
        self.default_userdict["e621_tag"] = self.default_userdict["e621_tag"].str.split(',')
        self.default_userdict["jp_tag"] = self.default_userdict["jp_tag"].str.split(',')
        if os.path.isfile('userdict.csv'):
            self.userdict = pd.read_csv('userdict.csv')
            self.userdict = self.userdict.fillna("")
            self.userdict["danbooru_tag"] = self.userdict["danbooru_tag"].str.split(',')
            self.userdict["e621_tag"] = self.userdict["e621_tag"].str.split(',')
            self.userdict["jp_tag"] = self.userdict["jp_tag"].str.split(',')

        #無効タグ(invalid tags)のみ除外
        self.e621_df = self.e621_df[~self.e621_df["category"].isin([6])]

        # インデックスの集合を定義(一つのセットの中にすべてのインデックスタグがフラットに格納されてる状態)
        # self.danbooru_index_set = set(self.danbooru_df["tag"])
        # self.e621_index_set = set(self.e621_df["tag"])
        self.danbooru_index_set = pickle.load(open('pickles/danbooru_index_set', "rb"))
        self.e621_index_set = pickle.load(open('pickles/e621_index_set', "rb"))

        # aliasesの集合を定義(一つのセットの中にすべてのエイリアスがフラットに格納されてる状態)
        # self.danbooru_aliases = self.danbooru_df.copy()
        # self.danbooru_aliases = self.danbooru_aliases.drop(["post_count", "jp_tag"], axis=1)
        # self.danbooru_aliases = self.danbooru_aliases.dropna(subset=["aliases"])
        # self.danbooru_aliases["aliases_list"] = self.danbooru_df["aliases"].str.split(',')
        #
        # self.e621_aliases = self.e621_df.copy()
        # self.e621_aliases = self.e621_aliases.drop(["post_count", "jp_tag"], axis=1)
        # self.e621_aliases = self.e621_aliases.dropna(subset=["aliases"])
        # self.e621_aliases["aliases_list"] = self.e621_df["aliases"].str.split(',')
        #
        # self.e621_aliases_set = set(reduce(lambda a, b: a + b, self.e621_aliases["aliases_list"]))
        # self.danbooru_aliases_set = set(reduce(lambda a, b: a + b, self.danbooru_aliases["aliases_list"]))
        self.danbooru_aliases_set = pickle.load(open('pickles/danbooru_aliases_set', "rb"))
        self.e621_aliases_set = pickle.load(open('pickles/e621_aliases_set', "rb"))

        # ｄｂとe621の共通部分を定義
        # self.db_index_and_e6_index = self.danbooru_index_set & self.e621_index_set
        # self.db_index_and_e6_aliases = self.danbooru_index_set & self.e621_aliases_set
        # self.db_aliases_and_e6_index = self.danbooru_aliases_set & self.e621_index_set
        # self.db_aliases_and_e6_aliases = self.danbooru_aliases_set & self.e621_aliases_set

        self.db_index_and_e6_index = pickle.load(open('pickles/db_index_and_e6_index', "rb"))
        self.db_index_and_e6_aliases = pickle.load(open('pickles/db_index_and_e6_aliases', 'rb'))
        self.db_aliases_and_e6_index = pickle.load(open('pickles/db_aliases_and_e6_index', 'rb'))
        self.db_aliases_and_e6_aliases = pickle.load(open('pickles/db_aliases_and_e6_aliases', 'rb'))



        # ｄｂとe621のそれぞれのindex,aliasesから他の集合と重複してる部分を除外したものを定義(現状使ってない)
        # self.danbooru_not_match_index_set = self.danbooru_index_set - self.db_index_and_e6_index - self.db_index_and_e6_aliases
        # self.danbooru_not_match_aliases_set = self.danbooru_aliases_set - self.db_aliases_and_e6_index - self.db_aliases_and_e6_aliases
        # self.e621_not_match_index_set = self.e621_index_set - self.db_index_and_e6_index - self.db_aliases_and_e6_index
        # self.e621_not_match_aliases_set = self.e621_aliases_set - self.db_index_and_e6_aliases - self.db_aliases_and_e6_aliases

        # aliases列（文字列）を個々のaliaseが格納されたリストに変換
        # self.danbooru_tag_aliases_df = self.danbooru_df.dropna(subset=['aliases']).copy()
        # self.danbooru_tag_aliases_df['aliases_list'] = self.danbooru_tag_aliases_df["aliases"].str.split(",")
        #
        # self.e621_tag_aliases_df = self.e621_df.dropna(subset=['aliases']).copy()
        # self.e621_tag_aliases_df["aliases_list"] = self.e621_tag_aliases_df["aliases"].str.split(",")
        self.danbooru_tag_aliases_df = pd.read_pickle('pickles/danbooru_tag_aliases_df.pkl')
        self.e621_tag_aliases_df = pd.read_pickle('pickles/e621_tag_aliases_df.pkl')


     # aliase（リスト型）をindexに変換するメソッド
    def return_index_text(self,aliases, selector):
        if selector == "e621":
            index_word = self.e621_tag_aliases_df[self.e621_tag_aliases_df['aliases_list'].apply(lambda x: aliases in x)]["tag"]
            index_word = index_word.to_string(index=False)
            return index_word

        elif selector == "danbooru":
            index_word = self.danbooru_tag_aliases_df[self.danbooru_tag_aliases_df['aliases_list'].apply(lambda x: aliases in x)][
                "tag"]
            index_word = index_word.to_string(index=False)
            return index_word

        # indexからaliases_setを取得して1個のリストとして返す関数

    def return_aliases_set(self,index_word, selector):
        index_aliases_list = [index_word]
        if selector == "danbooru":
            aliases_list = self.danbooru_tag_aliases_df[self.danbooru_tag_aliases_df["tag"] == index_word]["aliases_list"]
            if len(aliases_list) == 0:
                return index_aliases_list
            aliases_set = set(aliases_list.iloc[0])
            index_aliases_list.append(aliases_set)

        elif selector == "e621":
            aliases_list = self.e621_tag_aliases_df[self.e621_tag_aliases_df["tag"] == index_word]["aliases_list"]
            if len(aliases_list) == 0:
                return index_aliases_list
            aliases_set = set(aliases_list.iloc[0])
            index_aliases_list.append(aliases_set)

        # list[0]にindex_word,list[1]にaliasesのsetを格納
        return index_aliases_list


    # index_aliases_listからe621のindexを返す関数
    def return_e621_index_list(self, index_aliases_list):

        if len(index_aliases_list) == 2:
            aliases_set = index_aliases_list[1]
        else:
            aliases_set = set()



        e621_index_list = []

        # e621のindexにｄｂタグのindexが該当するパターン（返すタグが一意に決まる）
        if index_aliases_list[0] in self.db_index_and_e6_index:
            e621_index = index_aliases_list[0]
            e621_index_list.append(e621_index)

        # e621のaliasesにｄｂタグのindexが該当するパターン（返すタグが一意に決まる）
        elif index_aliases_list[0] in self.db_index_and_e6_aliases:
            e621_aliases = index_aliases_list[0]
            e621_index = self.return_index_text(e621_aliases, "e621")
            e621_index_list.append(e621_index)

        # e621のindexにｄｂタグのaliasesが該当するパターン（複数対複数の突合なので返す値が複数になる可能性あり）
        if not (aliases_set & self.db_aliases_and_e6_index == set()):
            match_set = aliases_set & self.db_aliases_and_e6_index
            for alias in match_set:
                e621_index_list.append(self.return_index_text(alias, "e621"))


        # e621のaliasesにｄｂタグのaliasesが該当するパターン（複数対複数の突合なので返す値が複数になる可能性あり）
        elif not (aliases_set & self.db_aliases_and_e6_aliases == set()):
            match_set = aliases_set & self.db_aliases_and_e6_aliases
            for alias in match_set:
                e621_index_list.append(self.return_index_text(alias, "e621"))

        return e621_index_list

    # index_aliases_listからdanbooruのindexを返す関数
    def return_danbooru_index_list(self, index_aliases_list):
        if len(index_aliases_list) == 2:
            aliases_set = index_aliases_list[1]
        else:
            aliases_set = set()

        danbooru_index_list = []

        # danbooruのindexにe621タグのindexが該当するパターン（返すタグが一意に決まる）
        if index_aliases_list[0] in self.db_index_and_e6_index:
            danbooru_index = index_aliases_list[0]
            danbooru_index_list.append(danbooru_index)

        # danbooruのaliasesにe621タグのindexが該当するパターン（返すタグが一意に決まる）
        elif index_aliases_list[0] in self.db_index_and_e6_aliases:
            danbooru_aliases = index_aliases_list[0]
            danbooru_index = self.return_index_text(danbooru_aliases, "danbooru")
            danbooru_index_list.append(danbooru_index)

        # danbooruのindexにe621タグのaliasesが該当するパターン（複数対複数の突合なので返す値が複数になる可能性あり）
        if not (aliases_set & self.db_aliases_and_e6_index == set()):
            match_set = aliases_set & self.db_aliases_and_e6_index
            for alias in match_set:
                danbooru_index_list.append(self.return_index_text(alias, "danbooru"))


        # danbooruのaliasesにe621タグのaliasesが該当するパターン（複数対複数の突合なので返す値が複数になる可能性あり）
        elif not (aliases_set & self.db_aliases_and_e6_aliases == set()):
            match_set = aliases_set & self.db_aliases_and_e6_aliases
            for alias in match_set:
                danbooru_index_list.append(self.return_index_text(alias, "danbooru"))

        return danbooru_index_list

    #post_countを返すメソッド
    def return_post_count(self, search_text, selector):
        if selector == "danbooru":
            post_count = self.danbooru_df[self.danbooru_df["tag"] == search_text]["post_count"]
        elif selector == "e621":
            post_count = self.e621_df[self.e621_df["tag"] == search_text]["post_count"]

        if post_count.empty:
            post_count = 0
        else:
            post_count = post_count.iloc[0]


        return post_count

    # 比較処理


    def return_search_frame_value_danbooru(self,search_text):
        db_index_word = ""
        index_or_aliases = ""
        index_flag = None

        search_text = self.text_cleansing(search_text)


        if not (search_text in (self.danbooru_index_set | self.danbooru_aliases_set)):
            index_or_aliases = "danbooru語ではありません。"
            index_flag = 0

        elif search_text in self.danbooru_index_set:
            index_or_aliases = "danbooru indexです。"
            index_flag = 1



        elif search_text in self.danbooru_aliases_set:
            db_index_word = self.return_index_text(search_text, "danbooru")
            index_or_aliases = "aliasesです。indexは" + db_index_word + "です。"

            index_flag = 2

        else:
            print("未定義！")

        #jptag = self.danbooru_df[self.danbooru_df["tag"] == search_text]["jp_tag"].to_string(index=False)
        jptag, user_flag = self.return_users_jptag(search_text, "danbooru")
        if user_flag == 1:
            index_or_aliases += "ユーザー定義の単語です。"
            jptag = jptag[0]
        elif user_flag == 2:
            index_or_aliases += "デフォルト辞書による単語です"
            jptag = jptag[0]
        post_count = self.return_post_count(search_text,"danbooru")

        return index_or_aliases, jptag, post_count, index_flag, db_index_word

    def return_search_frame_value_e621(self,search_text):
        e6_index_word = ""
        index_or_aliases = ""
        index_flag = None

        search_text = self.text_cleansing(search_text)

        if not (search_text in (self.e621_index_set | self.e621_aliases_set)):
            index_or_aliases = "e621語ではありません。"
            index_flag = 0

        elif search_text in self.e621_index_set:
            index_or_aliases = "e621 indexです。"
            index_flag = 1

        elif search_text in self.e621_aliases_set:
            e6_index_word = self.return_index_text(search_text, "e621")
            index_or_aliases = "aliasesです。indexは" + e6_index_word + "です。"

            index_flag = 2

        else:
            print("未定義！")

        #jptag = self.e621_df[self.e621_df["tag"] == search_text]["jp_tag"].to_string(index=False)
        jptag,user_flag = self.return_users_jptag(search_text, "e621")
        if user_flag == 1:
            index_or_aliases += "ユーザー定義の単語です。"
            jptag = jptag[0]
        elif user_flag == 2:
            index_or_aliases += "デフォルト辞書による単語です"
            jptag = jptag[0]
        post_count = self.return_post_count(search_text, "e621")

        return index_or_aliases, jptag, post_count, index_flag, e6_index_word

    def return_results_frame_value_e621(self,search_text):
        e621_gui_datalist = []
        search_text = self.text_cleansing(search_text)

        # ユーザー辞書に定義がある場合、優先処理してリターン
        e621_return_list = []
        e621_taglist,jp_taglist = self.return_userdict(text=search_text, selector="danbooru")
        if e621_taglist != [''] :

            for e621_tag,jp_tag in zip(e621_taglist, jp_taglist):
                e621_index_list = [
                    e621_tag,
                    jp_tag,
                    self.return_post_count(e621_tag, "e621"),
                    True,
                    False
                ]
                e621_return_list.append(e621_index_list)
            return e621_return_list


        # 入力されたserch_textがdanbooruのaliasesだった場合、indexに変換する
        if search_text in self.danbooru_aliases_set:
            search_text = self.return_index_text(search_text, "danbooru")

        index_aliases_list = self.return_aliases_set(search_text, "danbooru")

        if len(index_aliases_list) == 2:
            e621_gui_datalist = self.return_e621_index_list(index_aliases_list)
            e621_gui_datalist = [x for x in e621_gui_datalist if not (x == 'Series([], )')]
        elif len(index_aliases_list) == 1:
            e621_gui_datalist = self.return_e621_index_list(index_aliases_list)
        e621_gui_tags = list(dict.fromkeys(e621_gui_datalist))



        for i in e621_gui_tags:
            jptag,_ = self.return_users_jptag(i, "e621")
            e621_index_list = [
                i,
                jptag[0],
                self.return_post_count(i,"e621"),
                True,
                False
            ]
            e621_return_list.append(e621_index_list)

        #serch_textがe621のすべての条件に引っかからなかった場合、jptagで比較
        if len(e621_return_list) == 0:
            e621index_jpmatched = self.return_jptag_and_e621index(search_text)
            if e621index_jpmatched != None:

                for i in e621index_jpmatched:
                    e621_index_list = [
                        i,
                        self.e621_df[self.e621_df["tag"] == i]["jp_tag"].to_string(index=False),
                        self.return_post_count(i,"e621"),
                        True,
                        True
                    ]
                    e621_return_list.append(e621_index_list)

        #全てに引っかからなかった場合、該当なしと表示
        if len(e621_return_list) == 0:
            e621_index_list = [
                "該当なし",
                "",
                "",
                False,
                False
            ]
            e621_return_list.append(e621_index_list)


        return e621_return_list


    def return_results_frame_value_danbooru(self,search_text):
        danbooru_gui_datalist = []
        search_text = self.text_cleansing(search_text)

        # ユーザー辞書に定義がある場合、優先処理してリターン
        danbooru_return_list = []
        danbooru_taglist, jp_taglist = self.return_userdict(text=search_text, selector="danbooru")
        if danbooru_taglist != ['']:

            for danbooru_tag, jp_tag in zip(danbooru_taglist, jp_taglist):
                danbooru_index_list = [
                    danbooru_tag,
                    jp_tag,
                    self.return_post_count(danbooru_tag, "danbooru"),
                    True,
                    False
                ]
                danbooru_return_list.append(danbooru_index_list)
            return danbooru_return_list

        # 入力されたserch_textがe621のaliasesだった場合、indexに変換する
        if search_text in self.e621_aliases_set:
            search_text = self.return_index_text(search_text, "e621")

        index_aliases_list = self.return_aliases_set(search_text, "e621")
        if len(index_aliases_list) == 2:
            danbooru_gui_datalist = self.return_danbooru_index_list(index_aliases_list)
            danbooru_gui_datalist = [x for x in danbooru_gui_datalist if not (x == 'Series([], )')]
        elif len(index_aliases_list) == 1:
            danbooru_gui_datalist = self.return_danbooru_index_list(index_aliases_list)
        danbooru_gui_tags = list(dict.fromkeys(danbooru_gui_datalist))


        for i in danbooru_gui_tags:
            jptag,_ = self.return_users_jptag(i,"danbooru")
            danbooru_index_list = [
                i,
                jptag[0],
                self.return_post_count(i,"danbooru"),
                True,
                False
            ]
            danbooru_return_list.append(danbooru_index_list)

        # serch_textがdanbooruのすべての単語に引っかからなかった場合、jptagで比較
        if len(danbooru_return_list) == 0:
            danbooruindex_jpmatched = self.return_jptag_and_danbooruindex(search_text)
            if danbooruindex_jpmatched != None:

                for i in danbooruindex_jpmatched:
                    danbooru_index_list = [
                        i,
                        self.danbooru_df[self.danbooru_df["tag"] == i]["jp_tag"].to_string(index=False),
                        self.return_post_count(i,"danbooru"),
                        True,
                        True
                    ]
                    danbooru_return_list.append(danbooru_index_list)

        # 全てに引っかからなかった場合、該当なしと表示
        if len(danbooru_return_list) == 0:
            danbooru_index_list = [
                "該当なし",
                "",
                "",
                False,
                False
            ]
            danbooru_return_list.append(danbooru_index_list)

        return danbooru_return_list



    #indexをjp_tagに変換する関数
    def return_jptag_text(self,text,selector):
        if selector == "e621":
            return self.e621_df[self.e621_df['tag'] == text]["jp_tag"].to_string(index=False)
    
        elif selector == "danbooru":
            return self.danbooru_df[self.danbooru_df['tag'] == text]["jp_tag"].to_string(index=False)
    
    #textを入力するとdanbooruのjptagに一致するe621のインデックスタグを返すメソッド
    def return_jptag_and_e621index(self,text):
        jptag = self.return_jptag_text(text,"danbooru")
        e621index = self.e621_df[self.e621_df['jp_tag'] == jptag]["tag"]
        if e621index.empty:
            pass
        else:
            return e621index.to_list()

    # textを入力するとe621のjptagに一致するdanbooruのインデックスタグを返すメソッド
    def return_jptag_and_danbooruindex(self,text):
        jptag = self.return_jptag_text(text,"e621")
        danbooruindex = self.danbooru_df[self.danbooru_df['jp_tag'] == jptag]["tag"]
        if danbooruindex.empty:
            pass
        else:
            return danbooruindex.to_list()

    def text_cleansing(self,text):
        text = text.strip()
        text = text.replace(" ","_")
        return text

    #indexをユーザー辞書をもとにｊｐタグに変換するメソッド（登録がない場合、デフォルトの値を返す）
    def return_users_jptag(self,text,selector):
        if selector == "danbooru":
            if True in self.userdict["danbooru_tag"].apply(lambda x: text in x).values:
                jp_tag = self.userdict[self.userdict["danbooru_tag"].apply(lambda x: text in x)]["jp_tag"].values
                user_flag = 1
            elif True in self.default_userdict["danbooru_tag"].apply(lambda x: text in x).values:
                jp_tag = self.default_userdict[self.default_userdict["danbooru_tag"].apply(lambda x: text in x)]["jp_tag"].values
                user_flag = 2
            else:
                jp_tag = self.return_jptag_text(text,"danbooru")
                user_flag = 0

            return jp_tag,user_flag

        if selector == "e621":
            if True in self.userdict["e621_tag"].apply(lambda x: text in x).values:
                jp_tag = self.userdict[self.userdict["e621_tag"].apply(lambda x: text in x)]["jp_tag"].values
                user_flag = 1
            elif True in self.default_userdict["e621_tag"].apply(lambda x: text in x).values:
                jp_tag = self.default_userdict[self.default_userdict["e621_tag"].apply(lambda x: text in x)]["jp_tag"].values
                user_flag = 2
            else:
                jp_tag = self.return_jptag_text(text,"e621")
                user_flag = 0

            return jp_tag,user_flag


    #textがユーザー辞書に存在するかどうか確認するメソッド
    def isin_userdict(self,text,selector):
        if selector == "danbooru":
            return True in self.userdict["danbooru_tag"].apply(lambda x: text in x).values
        elif selector == "e621":
            return True in self.userdict["e621_tag"].apply(lambda x: text in x).values

    #textがユーザー辞書にある場合、対応するタグとｊｐタグを返すメソッド
    def return_userdict(self,text,selector):

        if self.isin_userdict(text,"danbooru"):
            e621_taglist = self.userdict[self.userdict["danbooru_tag"].apply(lambda x: text in x)]["e621_tag"].iloc[0]



            jp_taglist = self.userdict[self.userdict["danbooru_tag"].apply(lambda x: text in x)]["jp_tag"].iloc[0]
            return e621_taglist,jp_taglist

        elif self.isin_userdict(text,"e621"):
            danbooru_taglist = self.userdict[self.userdict["e621_tag"].apply(lambda x: text in x )]["danbooru_tag"].iloc[0]


            jp_taglist = self.userdict[self.userdict["e621_tag"].apply(lambda x: text in x)]["jp_tag"].iloc[0]
            return danbooru_taglist,jp_taglist

        else:
            return [''],['']



    # テスト用設定
    # danbooru_df = danbooru_df[danbooru_df["category"].isin([0,5])]
    # print(danbooru_df)
    # e621_df = e621_df[e621_df["category"].isin([0,7])]
    # テスト設定ここまで

    # テストケース
    # どちらもindex
    # test_text = "nipples"

    # dbがインデックス,e621がaliases
    # test_text = "futanari"

    # ｄｂがインデックス,e621には存在しない
    # test_text = "looking_past_viewer"

    # dbがaliases,e621がインデックス
    # test_text = "nippleless"

    # dbがaliases,e621には存在しない
    # test_text = "galaxies"

    # どっちもaliases
    # test_text = "high_res"

    # ｄｂにあってe621にないけど日本語訳が一致
    # search_text = "pervert"

