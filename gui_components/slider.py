from tkinter import *
from .bar import Bar


class Slider(Bar):
    def __init__(self, master: Misc, range: int, colour: str, haslabel: bool = False, font: tuple = ..., **kwargs) -> None:
        super().__init__(master, range, colour, haslabel=haslabel, font=font, **kwargs)

        self.bind('<Button-1>', self.moved)
        self.bind('<B1-Motion>', self.moved)

    def moved(self, event) -> None:
        value = event.x
        if value < 0:
            value = 0
        elif value > self.width:
            value = self.width

        self.change_value(round(value / self.width * self.range))
