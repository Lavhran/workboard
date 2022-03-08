import gui_components as gc
import config as c
import board
from functools import partial
from external import open_file, open_url

class ViewTask(gc.Tk):
    def __init__(self, main_window: gc.Tk, task: dict, **kw) -> None:
        super().__init__(**kw)

        self.task = task
        self.sliders = []

        # ---------------------------
        self.geometry("{0}x{1}".format(main_window.winfo_width(), main_window.winfo_height()))

        slider_length = main_window.winfo_width()//2

        frame = gc.CenterFrame(self)

        gc.Label(frame, text=task["title"], font=c.config["font"]["title"]).grid(column=0, row=0, columnspan=2, sticky=gc.W)

        for count, value in enumerate(task["layout"]):
            gc.Label(frame, text=value[0].lower()+": ", font=c.config["font"]["default"]).grid(column=0, row=count+1, sticky=gc.E)

            if value[0] == "URL":
                url = gc.Label(frame, text=value[1], font=c.config["font"]["default"], fg="blue", cursor="hand2")
                url.grid(column=1, row=count+1, sticky=gc.W)
                url.bind("<Button-1>", partial(open_url, value[1]))

            elif value[0] == "FILE":
                file = gc.Label(frame, text=value[1], font=c.config["font"]["default"], fg="blue", cursor="hand2")
                file.grid(column=1, row=count+1, sticky=gc.W)
                file.bind("<Button-1>", partial(open_file, value[1]))

            elif value[0] == "TEXT":
                gc.Label(frame, text=value[1], font=c.config["font"]["default"]).grid(column=1, row=count+1, sticky=gc.W)

            elif value[0] == "SLIDER":
                slider = gc.Slider(frame, value[1], "green", haslabel=True, font=c.config["font"]["default"], height=50, width=slider_length, bg="lightgrey")
                slider.grid(column=1, row=count+1, sticky=gc.W)

                slider.change_value(value[2])
                self.sliders.append((count, slider))
        
        if len(self.sliders):
            gc.Button(frame, text="Commit changes", command=self.save, font=c.config["font"]["default"]).grid(column=1, sticky=gc.W)

        self.update()

    def save(self) -> None:
        for i in self.sliders:
            board.workboard[self.task["title"]]["layout"][i[0]][2] = int(i[1].value)
        board.save()

class EditTask(gc.Tk):
    def __init__(self, main_window: gc.Tk, listbox_index: int, title: str="", fields: list=[], **kw) -> None:
        super().__init__(**kw)

        self.entries = [] # points to all entries
        self.new_row = 1

        self.main_window = main_window
        self.listbox_index = listbox_index
        self.old_title = title

        # -----------------------------
        self.geometry("{0}x{1}".format(main_window.winfo_width()//2, main_window.winfo_height()))

        frame = gc.CenterFrame(self)

        add_frame = gc.Frame(frame)
        self.part_frame = gc.Frame(frame)

        add_frame.grid(column=0, row=0)
        self.part_frame.grid(column=0, row=1)

        for count, i in enumerate(("URL", "FILE", "TEXT", "SLIDER")):
            gc.Button(add_frame, text="+"+i.lower(), font=c.config["font"]["default"], command=partial(self.add_part, i)).grid(column=count, row=0)
        
        button_text = "Save" if len(fields) else "Create"
        gc.Button(frame, text=button_text, font=c.config["font"]["default"], command=self.save, width=20).grid(column=0, row=2)

        # adding parts
        gc.Label(self.part_frame, text="Title: ", font=c.config["font"]["default"]).grid(column=0, row=0)
        
        title_entry = gc.Entry(self.part_frame, font=c.config["font"]["default"])
        title_entry.insert(gc.END, title)
        title_entry.grid(column=1, row=0)

        self.entries.append(("TITLE", title_entry))

        for field in fields:
            self.add_part(field[0], field[1])

    def add_part(self, type: str, value="") -> None:
        gc.Label(self.part_frame, text=type.lower()+": ", font=c.config["font"]["default"]).grid(column=0, row=self.new_row)
        
        part_entry = gc.Entry(self.part_frame, font=c.config["font"]["default"])
        part_entry.insert(gc.END, value)
        part_entry.grid(column=1, row=self.new_row)

        gc.Button(self.part_frame, font=c.config["font"]["default"], text="-", command=partial(self.remove_part, self.new_row)).grid(column=2, row=self.new_row)

        self.entries.append((type, part_entry))
        self.new_row += 1

    def remove_part(self, index: int) -> None:
        for i in self.entries:
            if i[1] == self.part_frame.grid_slaves(index, 1)[0]:
                self.entries.remove(i)
                break
        for i in self.part_frame.grid_slaves(index):
            i.destroy()

    def save(self) -> None:
        for i in range(len(self.entries)):
            try:
                if self.entries[i][0] == "SLIDER":
                    self.entries[i] = (self.entries[i][0], int(self.entries[i][1].get()), 0)
                else:
                    self.entries[i] = (self.entries[i][0], self.entries[i][1].get())
            except:
                pass

        if self.listbox_index == -1:
            save_info = {
                "title": self.entries[0][1],
                "board": self.listbox_index+2,
                "layout": self.entries[1:]}
            self.main_window.listboxes[self.listbox_index+1].insert(gc.END, self.entries[0][1])
            board.add(save_info)
        else:
            save_info = {
                "title": self.entries[0][1],
                "board": self.listbox_index+1,
                "layout": self.entries[1:]}
            board.update(save_info, self.old_title)

            if self.old_title != self.entries[0][1]:
                index = self.main_window.listboxes[self.listbox_index].get(0, gc.END).index(self.old_title)
                self.main_window.listboxes[self.listbox_index].delete(index)
                self.main_window.listboxes[self.listbox_index].insert(index, self.entries[0][1])

        self.destroy()



class MainWindow(gc.Tk):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

        self.listboxes = []
        self.selected = None

        for count, group in enumerate(c.config["board"]["groups"]):
            label = gc.Label(self, text=group, font=c.config["font"]["title"])
            listbox = gc.Listbox(self, font=c.config["font"]["default"])
            vertical_scrollbar = gc.Scrollbar(self, command=listbox.yview)
            horisontal_scrollbar = gc.Scrollbar(self, command=listbox.xview, orient='horizontal')

            listbox.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horisontal_scrollbar.set)
            listbox.bind("<Button-3>", lambda event, x=count: self.show_menu(x, event))

            label.grid(column=count*2, row=0, columnspan=2)
            listbox.grid(column=count*2, row=1)
            vertical_scrollbar.grid(column=count*2+1, row=1, sticky=gc.NS)
            horisontal_scrollbar.grid(column=count*2, row=2, sticky=gc.EW)

            self.listboxes.append(listbox)

        for k, v in board.workboard.items():
            self.listboxes[v["board"]-1].insert(gc.END, v["title"])

        self.menu = gc.Menu(self, tearoff=0, font=c.config["font"]["default"])
        self.menu.add_command(label="Create New...", command=self.create_task)
        self.menu.add_command(label="View...", command=self.view_task)
        self.menu.add_command(label="Edit...", command=self.edit_task)
        self.menu.add_separator()
        self.menu.add_command(label="--->", command=lambda: self.move_task(True))
        self.menu.add_command(label="<---", command=lambda: self.move_task(False))

    def show_menu(self, listbox, event) -> None:
        try:
            selected_index = self.listboxes[listbox].curselection()
            if not len(selected_index):
                self.menu.delete(1, gc.END)
            else:
                if len(self.menu.children) < 6:
                    self.menu.add_command(label="View...", command=self.view_task)
                    self.menu.add_command(label="Edit...", command=self.edit_task)
                    self.menu.add_separator()
                    self.menu.add_command(label="--->", command=lambda: self.move_task(True))
                    self.menu.add_command(label="<---", command=lambda: self.move_task(False))

                self.menu.delete(6, gc.END)
                self.menu.add_separator()

                self.selected = board.workboard[self.listboxes[listbox].get(selected_index[0])]

                for i in self.selected["layout"]:
                    if i[0] == "URL":
                        self.menu.add_command(label="Open {0}".format(i[0].lower()), command=partial(open_url, i[1]))
                    elif i[0] == "FILE":
                        self.menu.add_command(label="Open {0}".format(i[0].lower()), command=partial(open_file, i[1]))


                self.menu.add_separator()
                self.menu.add_command(label="Delete", command=self.delete_task)

            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def create_task(self) -> None:
        task = EditTask(self, -1)
        task.title("Create Task")

    def view_task(self) -> None:
        task = ViewTask(self, self.selected)
        task.title(self.selected["title"])

    def edit_task(self) -> None:
        task = EditTask(self, self.selected["board"]-1, self.selected["title"], self.selected["layout"])
        task.title("Edit Task")

    def move_task(self, dir: bool) -> None:
        current_board = board.workboard[self.selected["title"]]["board"]
        if dir:
            if not current_board >= 3:
                board.workboard[self.selected["title"]]["board"] += 1
                self.listboxes[current_board].insert(gc.END, self.selected["title"])
            else:
                return
        else:
            if not current_board <= 1:
                board.workboard[self.selected["title"]]["board"] -= 1
                self.listboxes[current_board-2].insert(gc.END, self.selected["title"])
            else:
                return
        self.listboxes[current_board-1].delete(self.listboxes[current_board-1].get(0, gc.END).index(self.selected["title"]))
        board.save()

    def delete_task(self) -> None:
        current_board = board.workboard[self.selected["title"]]["board"]
        self.listboxes[current_board-1].delete(self.listboxes[current_board-1].get(0, gc.END).index(self.selected["title"]))
        board.remove(self.selected["title"])
