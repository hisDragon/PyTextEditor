
import threading
from   enchant.checker import SpellChecker
from   app             import App


class SpellCheckThread(threading.Thread):

    def __init__(self, root_widget: App, name: str = "<\'SpellCheckThread\'>"):
        threading.Thread.__init__(self, name=name)
        self.thread_name = name
        self.language = "en_US"
        self.dictionary = SpellChecker(self.language)  # or import enchant and use Dict() to check individual words
        self.thread_flag = True
        self.setDaemon(True)
        self.root_widget = root_widget

        # tag config for misspelled words
        root_widget.text_area.tag_config("misspelled", foreground="red", underline=True)

    def run(self):

        while self.thread_flag:
            input_text = self.root_widget.text_area.get("1.0", "end-1c")
            self.dictionary.set_text(input_text)

            for error in self.dictionary:
                # print(error.word)  # debugging
                index = "1.0"
                index = self.root_widget.text_area.search(error.word, index, nocase=1, stopindex="end")
                if not index: break
                last_index = "%s+%dc" % (index, len(error.word))
                self.root_widget.text_area.tag_add("misspelled", index, last_index)
                index = last_index
                self.root_widget.text_area.see(index)

    def start_spell_check(self):
        self.start()

    def stop_spell_check(self):
        self.thread_flag = False
