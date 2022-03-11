from tkinter import *


class Bar(Canvas):
    def __init__(self, master: Misc, range: int, colour: str, haslabel: bool = False, font: tuple = ('Arial', 9), **kwargs) -> None:
        super().__init__(master=master, **kwargs)

        self.width = int(self['width'])
        self.height = int(self['height'])

        self.value = 0
        self.range = range
        self.part = self.width / range

        self.bar = self.create_rectangle(0, 0, 0, self.height, fill=colour)

        self.haslabel = haslabel
        if haslabel:
            self.label = self.create_text(
                self.width//2, self.height//2, anchor=CENTER, text='0', font=font)

    def change_value(self, value: int) -> None:
        if value > self.range:
            value = self.range
        elif value < 0:
            value = 0
            
        self.value = value
        if self.haslabel:
            self.itemconfigure(self.label, text=str(value))
        self.coords(self.bar, 0, 0, value * self.part, self.height)

    def set_range(self, new_range: int) -> None:
        self.range = new_range
        self.part = self.width / new_range
        if self.value > new_range:
            self.value = new_range
        self.change_value(self.value)
