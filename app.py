import tkinter            as     tk                    # python gui library
from   tkinter.font       import Font                  # font
import tkinter.filedialog as     filedialog            # for saving and opening files
import tkinter.messagebox as     messagebox            # for message boxes or alerts
import os                                              # for control of naming of files
import spell_check                                     # spell checking thread


# App START #


class App(tk.Tk):

    # __init()__ START

    def __init__(self, root: tk.Tk):

        root.title("Untitled - PyTextEditor 1.0")
        root.geometry("950x600")

        # filename
        self.file_name: str = None  # no file name at the beginning

        # creating a class variable for master(root) to use it outside this class to instantiate other Widgets
        self.root: tk.Tk = root

        # font (local variable)
        text_font: Font = Font(family="Times New Roman", size=14)

        # menu check buttons
        self.show_status_bar: tk.BooleanVar = tk.BooleanVar()

        self.text_area: tk.Text = tk.Text(master=root, font=text_font)
        self.scroll_bar: tk.Scrollbar = tk.Scrollbar(master=root, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scroll_bar.set)

        # placing text area and scroll bar on interface(text editor)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        # creating an instance of menu bar
        # calling __init__() at this point of time because it configures other Widgets
        self.menu_bar = MenuBar(self)
        self.status_bar = StatusBar(self, self.show_status_bar)

        # binding keyboard buttons
        self.__bind()

        # starting spell checking thread
        self.spell_check_thread = spell_check.SpellCheckThread(self)
        self.thread_already_started = False  # to check if the thread is already started to restrain from starting again

        # __init__() END

    def window_title(self, name: str = None):
        if name:
            lhs, rhs = name.split(".", 1)
            del lhs
            rhs = App.__parser(rhs)
            if rhs:
                self.root.title(name + " - PyTextEditor 1.0 (" + rhs + ")")
            else:
                self.root.title(name + " - PyTextEditor 1.0")
        else:
            self.root.title("Untitled - PyTextEditor 1.0")

    ###################################################################################################################
    # file menu methods START

    def new_file(self, *args):
        self.text_area.delete(1.0, tk.END)
        self.file_name = None
        self.window_title()

    def open_file(self, *args):
        self.file_name = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[
                ("All Files", ".*"),
                ("Text Files", ".txt"),
                ("Python Scripts", ".py"),
                ("CPP Source Files", ".cpp .cc"),
                ("C Source Files", ".c"),
                ("HTML Documents", ".html .htm"),
                ("JavaScript Files", ".js"),
                ("CSS Documents", ".css"),
                ("JSON Files", ".json")
            ]
        )

        if self.file_name:
            self.text_area.delete(1.0, tk.END)
            with open(self.file_name, "r") as f:
                self.text_area.insert(1.0, f.read())
            # set window title
            self.window_title(self.file_name)
            # start spell check thread
            if not self.thread_already_started:
                self.thread_already_started = True
                self.spell_check_thread.start_spell_check()

    def save(self, *args):
        if self.file_name:
            try:
                text_area_content = self.text_area.get(1.0, tk.END)
                with open(self.file_name, "w") as f:
                    f.write(text_area_content)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self, *args):

        initial_file_num = 0
        while os.path.exists("Untitled%s.txt" % initial_file_num):
            initial_file_num += 1
        initial_file_name = "Untitled" + str(initial_file_num)

        try:
            new_file = filedialog.asksaveasfilename(
                initialfile=initial_file_name,
                defaultextension=".txt",
                filetypes=[
                    ("All Files", ".*"),
                    ("Text Files", ".txt"),
                    ("Python Scripts", ".py"),
                    ("CPP Source Files", ".cpp .cc"),
                    ("C Source Files", ".c"),
                    ("HTML Documents", ".html .htm"),
                    ("JavaScript Files", ".js"),
                    ("CSS Documents", ".css"),
                    ("JSON Files", ".json")
                ]
            )

            text_area_content = self.text_area.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(text_area_content)

            self.file_name = new_file
            self.window_title(self.file_name)

            # starting spell check when new file is saved
            if not self.thread_already_started:
                self.spell_check_thread.start_spell_check()

        except Exception as e:
            print(e)

    def destroy(self):
        self.spell_check_thread.join()  # joining spell check thread before destruction
        self.root.destroy()

    # file menu methods END
    ###################################################################################################################

    ###################################################################################################################
    # view menu methods START

    def show_status_bar_method(self):
        self.status_bar.show_status_bar(self.show_status_bar)

    # view menu methods END
    ###################################################################################################################

    ###################################################################################################################
    # about menu methods START

    @staticmethod
    def release_notes():
        release_info = "Nothing yet"
        title = "Release Notes"
        messagebox.showinfo(title, release_info)

    @staticmethod
    def version_info():
        version = "PyTextEditor v1.0"
        title = "Version Info"
        messagebox.showinfo(title, version)

    # about menu methods END
    ###################################################################################################################

    # to display type of file at the END
    @staticmethod
    def __parser(rhs: str = None):
        switchers = {
            "txt": "Text File",
            "py": "Python Scripts",
            "cpp": "CPP Source Files",
            "c": "C Source Files",
            "html": "HTML Document",
            "css": "CSS Document",
            "json": "JSON File",
            "js": "JavaScript File"
        }

        return switchers.get(rhs, None)

    def __bind(self):

        self.root.bind('<Control-n>', self.new_file)
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-s>', self.save)
        self.root.bind('<Control-S>', self.save_as)


# END of App #


class MenuBar:
    def __init__(self, parent: App):
        # font for menu
        menu_font = Font(family="Times New Roman", size=12)

        # menu bar configurations
        menu_bar = tk.Menu(master=parent.root, font=menu_font)
        parent.root.config(menu=menu_bar)

        # drop down for 'File' menu
        file_dropdown = tk.Menu(master=menu_bar, font=menu_font, tearoff=0)

        file_dropdown.add_command(label="New File", accelerator='Ctrl+N', command=parent.new_file)
        file_dropdown.add_command(label="Open File", accelerator='Ctrl+O', command=parent.open_file)
        file_dropdown.add_separator()  # separator
        file_dropdown.add_command(label="Save", accelerator='Ctrl+S', command=parent.save)
        file_dropdown.add_command(label="Save As", accelerator='Ctrl+Shift+S', command=parent.save_as)
        file_dropdown.add_separator()  # separator
        file_dropdown.add_command(label="Exit", command=parent.destroy)

        # drop down for 'About' menu
        about_dropdown = tk.Menu(master=menu_bar, font=menu_font, tearoff=0)

        about_dropdown.add_command(label="Release Notes", command=App.release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="Version", command=App.version_info)

        # drop down for 'View' menu
        view_dropdown = tk.Menu(master=menu_bar, font=menu_font, tearoff=0)

        view_dropdown.add_checkbutton(label="Toggle Status Bar", onvalue=1, offvalue=0,
                                      variable=parent.show_status_bar, command=parent.show_status_bar_method)

        # adding 'File' for menu master(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_dropdown)
        menu_bar.add_cascade(label="View", menu=view_dropdown)
        menu_bar.add_cascade(label="About", menu=about_dropdown)


class StatusBar:
    def __init__(self, parent: App, show_status_bar: tk.BooleanVar):
        status_font = Font(family="Times New Roman", size=10)

        self.status = tk.StringVar()
        self.status.set("PyTextEditor v1.0")

        self.label = tk.Label(parent.text_area, textvariable=self.status, fg='black',
                              bg='lightgrey', anchor='sw', font=status_font)
        self.label.pack(side=tk.BOTTOM, fill=tk.BOTH)

        if show_status_bar.get():
            pass
        else:
            self.label.pack_forget()

    def show_status_bar(self, s_s_b: tk.BooleanVar):
        if s_s_b.get():
            self.label.pack(side=tk.BOTTOM, fill=tk.BOTH)
        else:
            self.label.pack_forget()


if __name__ == '__main__':
    master = tk.Tk()
    app = App(master)
    master.mainloop()
