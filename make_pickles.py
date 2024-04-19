import pandas as pd
import pickle
from functools import reduce

danbooru_df = pd.read_csv('csv/danbooru_jpmerged.csv')
e621_df = pd.read_csv('csv/e621_translated.csv')
default_userdict = pd.read_csv('csv/default_userdict.csv')

# danbooru_df.to_pickle("danbooru_df.pkl")
# e621_df.to_pickle("e621_df.pkl")
# default_userdict.to_pickle("default_userdict.pkl")

# 無効タグ(invalid tags)のみ除外
e621_df = e621_df[~e621_df["category"].isin([6])]

# インデックスの集合を定義(一つのセットの中にすべてのインデックスタグがフラットに格納されてる状態)
danbooru_index_set = set(danbooru_df["tag"])
e621_index_set = set(e621_df["tag"])

pickle.dump(danbooru_index_set, open('pickles/danbooru_index_set', "wb"))
pickle.dump(e621_index_set, open('pickles/e621_index_set', "wb"))


# aliasesの集合を定義(一つのセットの中にすべてのエイリアスがフラットに格納されてる状態)
danbooru_aliases = danbooru_df.copy()
danbooru_aliases = danbooru_aliases.drop(["post_count", "jp_tag"], axis=1)
danbooru_aliases = danbooru_aliases.dropna(subset=["aliases"])
danbooru_aliases["aliases_list"] = danbooru_df["aliases"].str.split(',')

e621_aliases = e621_df.copy()
e621_aliases = e621_aliases.drop(["post_count", "jp_tag"], axis=1)
e621_aliases = e621_aliases.dropna(subset=["aliases"])
e621_aliases["aliases_list"] = e621_df["aliases"].str.split(',')

e621_aliases_set = set(reduce(lambda a, b: a + b, e621_aliases["aliases_list"]))
danbooru_aliases_set = set(reduce(lambda a, b: a + b, danbooru_aliases["aliases_list"]))

pickle.dump(danbooru_aliases_set, open('pickles/danbooru_aliases_set', "wb"))
pickle.dump(e621_aliases_set, open('pickles/e621_aliases_set', "wb"))

# ｄｂとe621の共通部分を定義
db_index_and_e6_index = danbooru_index_set & e621_index_set
db_index_and_e6_aliases = danbooru_index_set & e621_aliases_set
db_aliases_and_e6_index = danbooru_aliases_set & e621_index_set
db_aliases_and_e6_aliases = danbooru_aliases_set & e621_aliases_set

pickle.dump(db_index_and_e6_index, open('pickles/db_index_and_e6_index', "wb"))
pickle.dump(db_index_and_e6_aliases, open('pickles/db_index_and_e6_aliases', "wb"))
pickle.dump(db_aliases_and_e6_index, open('pickles/db_aliases_and_e6_index', "wb"))
pickle.dump(db_aliases_and_e6_aliases, open('pickles/db_aliases_and_e6_aliases', "wb"))

# ｄｂとe621のそれぞれのindex,aliasesから他の集合と重複してる部分を除外したものを定義(現状未使用なのでpickle化しない)
# danbooru_not_match_index_set = danbooru_index_set - db_index_and_e6_index - db_index_and_e6_aliases
# danbooru_not_match_aliases_set = danbooru_aliases_set - db_aliases_and_e6_index - db_aliases_and_e6_aliases
# e621_not_match_index_set = e621_index_set - db_index_and_e6_index - db_aliases_and_e6_index
# e621_not_match_aliases_set = e621_aliases_set - db_index_and_e6_aliases - db_aliases_and_e6_aliases

# aliases列（文字列）を個々のaliaseが格納されたリストに変換
danbooru_tag_aliases_df = danbooru_df.dropna(subset=['aliases']).copy()
danbooru_tag_aliases_df['aliases_list'] = danbooru_tag_aliases_df["aliases"].str.split(",")

e621_tag_aliases_df = e621_df.dropna(subset=['aliases']).copy()
e621_tag_aliases_df["aliases_list"] = e621_tag_aliases_df["aliases"].str.split(",")

danbooru_tag_aliases_df.to_pickle("danbooru_tag_aliases_df.pkl")
e621_tag_aliases_df.to_pickle("e621_tag_aliases_df.pkl")