import tkinter as tk
from tkinter import ttk
import webbrowser
import Searcher

root = tk.Tk()
root.title('danbooru-e621-converter')
root.option_add("*font", ["游ゴシック", 14])
style = ttk.Style()
style.configure(".", font=("", 14))


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.searcher = Searcher.Searcher()
        self.pack(fill=tk.BOTH, expand=1)
        self.config_master()
        self.create_variables()

        self.danbooru_frame = ttk.LabelFrame(master, text="danbooru")
        self.e621_frame = ttk.LabelFrame(master, text="e621")
        self.button_frame = ttk.Frame(master)
        self.danbooru_frame.pack(fill=tk.BOTH, expand=1)
        self.button_frame.pack(fill=tk.BOTH, expand=1)
        self.e621_frame.pack(fill=tk.BOTH, expand=1)

        self.run_button_danbooruTo_e621 = tk.Button(self.button_frame, text="↓ Search e621",
                                                    command=self.press_db_to_e621button)
        self.run_button_clear = tk.Button(self.button_frame, text="All Clear", command=self.press_clear_button)
        self.run_button_e621To_danbooru = tk.Button(self.button_frame, text="↑ Search danbooru",
                                                    command=self.press_e621_to_danboorubutton)
        self.run_button_danbooruTo_e621.grid(row=0, column=0, padx=5)
        self.run_button_clear.grid(row=0, column=1, padx=5)
        self.run_button_e621To_danbooru.grid(row=0, column=2, padx=5)

        self.create_widgets()

    def config_master(self):
        pass

    def create_variables(self):
        self.search_word = tk.StringVar()
        self.search_word.set("")

        # self.e621_search_word = tk.StringVar()
        # self.e621_search_word.set("")

    def create_widgets(self):
        self.db_search_frame = SearchFrame(master=self.danbooru_frame)
        self.e621_search_frame = SearchFrame(master=self.e621_frame)

    # 左ボタンを押したときの挙動
    def press_db_to_e621button(self):
        # danbooruエリアの書き換え
        self.search_text = self.db_search_frame.get_text()
        if self.search_text == "":
            return 0
        index_or_aliases, jptag, post_count, index_flag, db_index_word = self.searcher.return_search_frame_value_danbooru(
            self.search_text)
        self.db_search_frame.set_results(self.search_text, index_or_aliases, jptag, post_count, index_flag,
                                         db_index_word, dbORe621="db")

        # e621エリアの書き換え
        self.e621_search_frame.destroy()
        for child in self.e621_frame.winfo_children():
            child.destroy()
        self.e621_lists = self.searcher.return_results_frame_value_e621(self.search_text)

        self.resultframes = [ResultsFrame(master=self.e621_frame) for _ in range(len(self.e621_lists))]

        [self.resultframes[i].set_results(self.e621_lists[i], "e621") for i in range(len(self.e621_lists))]

    # 右ボタンを押したときの挙動
    def press_e621_to_danboorubutton(self):
        # e621エリアの書き換え
        self.search_text = self.e621_search_frame.get_text()
        if self.search_text == "":
            return 0
        index_or_aliases, jptag, post_count, index_flag, db_index_word = self.searcher.return_search_frame_value_e621(
            self.search_text)
        self.e621_search_frame.set_results(self.search_text, index_or_aliases, jptag, post_count, index_flag,
                                           db_index_word, dbORe621="e621")

        # danbooruエリアの書き換え
        self.db_search_frame.destroy()
        for child in self.danbooru_frame.winfo_children():
            child.destroy()
        self.e621_lists = self.searcher.return_results_frame_value_danbooru(self.search_text)

        self.resultframes = [ResultsFrame(master=self.danbooru_frame) for _ in range(len(self.e621_lists))]

        [self.resultframes[i].set_results(self.e621_lists[i], "danbooru") for i in range(len(self.e621_lists))]

    # リセットボタン
    def press_clear_button(self):
        [child.destroy() for child in self.danbooru_frame.winfo_children()]
        [child.destroy() for child in self.e621_frame.winfo_children()]

        self.create_widgets()


class SearchFrame(tk.Frame):
    def __init__(self, master):

        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        self.searchtext_label = ttk.Label(self, text="検索タグ：")
        self.searchtext_box = ttk.Entry(self)

        self.indexORaliases_label = tk.Label(self, text="index or aliases :")
        self.indexORaliases_returnvalue = tk.Label(self, text="")

        self.jptag_label = tk.Label(self, text="jp tag :")
        self.jptag_returnvalue = tk.Label(self, text="")

        self.post_count_label = tk.Label(self, text="post count : ")
        self.post_count_returnvalue = tk.Label(self, text="")

        self.link_label = tk.Label(self, text="link :")
        self.link_returnvalue = tk.Label(self, text="", fg="blue", font=("游ゴシック", 14, "underline"))
        self.link_returnvalue.bind("<Button-1>",
                                   lambda event: webbrowser.open_new_tab(self.link_returnvalue["text"]))

        self.searchtext_label.grid(row=0, column=0, padx=5, sticky=tk.W)
        self.searchtext_box.grid(row=0, column=1, padx=5, sticky=tk.W)

        self.indexORaliases_label.grid(row=1, column=0, padx=5, sticky=tk.W)
        self.indexORaliases_returnvalue.grid(row=1, column=1, padx=5, sticky=tk.W)

        self.jptag_label.grid(row=2, column=0, padx=5, sticky=tk.W)
        self.jptag_returnvalue.grid(row=2, column=1, padx=5, sticky=tk.W)

        self.post_count_label.grid(row=3, column=0, padx=5, sticky=tk.W)
        self.post_count_returnvalue.grid(row=3, column=1, padx=5, sticky=tk.W)

        self.link_label.grid(row=4, column=0, padx=5, sticky=tk.W)
        self.link_returnvalue.grid(row=4, column=1, padx=5, sticky=tk.W)

    def get_text(self):
        return self.searchtext_box.get()

    def set_text(self, text):
        self.searchtext_box['text'] = text

    def set_results(self, search_text, index_or_aliases, jptag, post_count, index_flag, index_word, dbORe621):
        self.indexORaliases_returnvalue['text'] = index_or_aliases
        self.jptag_returnvalue['text'] = jptag
        self.post_count_returnvalue['text'] = post_count

        if dbORe621 == "db":
            if index_flag == 0:
                self.url = ""
            elif index_flag == 1:
                self.url = "https://danbooru.donmai.us/wiki_pages/" + search_text
            elif index_flag == 2:
                self.url = "https://danbooru.donmai.us/wiki_pages/" + index_word

        elif dbORe621 == "e621":
            if index_flag == 0:
                self.url = ""
            elif index_flag == 1:
                self.url = "https://e621.net/wiki_pages/" + search_text
            elif index_flag == 2:
                self.url = "https://e621.net/wiki_pages/" + index_word

        self.link_returnvalue['text'] = self.url


class ResultsFrame(SearchFrame):
    def __init__(self, master):
        super().__init__(master)

        self.searchtext_label['text'] = '検索結果'
        self.indexORaliases_label.grid_forget()
        self.indexORaliases_returnvalue.grid_forget()

    def set_results(self, return_list, selector):
        self.searchtext_box.insert(0, return_list[0])
        self.jptag_returnvalue['text'] = return_list[1]
        self.post_count_returnvalue['text'] = return_list[2]

        if return_list[3]:
            if selector == 'danbooru':
                self.url = "https://danbooru.donmai.us/wiki_pages/" + return_list[0]
                self.link_returnvalue['text'] = self.url

            elif selector == 'e621':
                self.url = "https://e621.net/wiki_pages/" + return_list[0]
                self.link_returnvalue['text'] = self.url

        if return_list[4]:
            self.searchtext_label["text"] = "jptagによる検索結果"
            self.searchtext_label["foreground"] = "red"


class PrintLabel(tk.Label):
    def __init__(self, master=None):
        tk.Label.__init__(self, master, text="Enter")

    def set_text(self, text):
        self["text"] = text


app = Application(root)
root.mainloop()
