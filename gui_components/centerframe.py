from tkinter import *


class CenterFrame(Frame):
    def __init__(self, master: Misc, **kwargs) -> None:
        super().__init__(master=master, **kwargs)
        self.master.bind('<Configure>', self.resize)

        self.screenwidth = self.master.winfo_width()
        self.screenheight = self.master.winfo_height()

    def resize(self, event) -> None:

        screenwidth = self.master.winfo_width()
        screenheight = self.master.winfo_height()

        if screenwidth != self.screenwidth or screenheight != self.screenheight:
            self.screenwidth = screenwidth
            self.screenheight = screenheight

            self.place_forget()
            self.place(x=int(self.master.winfo_width())//2,
                       y=int(self.master.winfo_height())//2,
                       anchor=CENTER)
