from tkinter import *
from SealsData import SealsData


class SealsGui:
    def __init__(self):
        self.root = Tk()
        self.sealsData = SealsData()

    def init_root_size(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        zoom_ratio = 0.95
        root_width = int(screen_width*zoom_ratio)
        root_height = int(screen_height*zoom_ratio)
        root_x = (screen_width - root_width)//2
        root_y = (screen_height - root_height)//2
        self.root.geometry(f"{root_width}x{root_height}+{root_x}+{root_y}")

    def init_root_logo_title(self):
        self.root.bg = "white"
        self.root.title("Seals")
        # self.root.iconbitmap("../img/seals.ico")

    def run(self):
        self.init_root_size()
        self.init_root_logo_title()
        self.init_layout()
        self.init_target_grid()
        self.root.mainloop()

    def init_target_grid(self):
        self.target_gird_list = []
        for i in range(4):
            for j in range(12):
                button = Button(self.target_gird_frame,
                                text=f"({i},{j})", relief="groove")
                button.place(relx=i*1/4, rely=j*1/12,
                             relwidth=1/4, relheight=1/12)
                button.bind("<Button-1>", self.on_target_grid_button_click)
                self.target_gird_list.append(button)
        self.draw_raw_label()
        self.draw_target_grid()

    def draw_raw_label(self):
        self.raw = self.sealsData.pop_raw()
        self.raw_label["text"] = f"raw: {self.raw}"

    def draw_target_grid(self):
        target_grid = self.sealsData.query_distance(self.raw)
        for button in self.target_gird_list:
            target, distance = target_grid.pop(0)
            button["text"] = f"{target},{distance}"

    def on_no_match_button_click(self, event):
        self.target = "null"
        self.target_label["text"] = f"target: {self.target}"

    def on_my_answer_button_click(self, event):
        my_answer = self.my_answer_entry.get()
        self.target = my_answer
        self.target_label["text"] = f"target: {self.target}"

    def on_target_grid_button_click(self, event):
        self.target = event.widget["text"].split(",")[0]
        self.target_label["text"] = f"target: {self.target}"

    def on_next_button_click(self, event):
        key = self.raw
        value = self.target
        self.sealsData.pair_list_dict[key] = value
        # print(self.sealsData.pair_list_dict)
        self.draw_raw_label()
        self.draw_target_grid()

    def on_skip_button_click(self, event):
        self.draw_raw_label()
        self.draw_target_grid()

    def on_save_button_click(self, event):
        self.sealsData.save_pair_list()

    def init_layout(self):
        head_frame = Frame(self.root)
        head_frame.place(relx=0.05, rely=0.05,
                         relwidth=0.9, relheight=0.1)
        raw = "init_raw_value"
        raw_label = Label(head_frame, text=f"raw: {raw}")
        raw_label.place(relx=0, rely=0, relwidth=1/2, relheight=1/2)

        target = "init_target_value"
        target_label = Label(head_frame, text=f"target: {target}")
        target_label.place(relx=0, rely=1/2,
                           relwidth=1/2, relheight=1/2)

        button_group_frame = Frame(head_frame)
        button_group_frame.place(relx=1/2, rely=0,
                                 relwidth=1/2, relheight=1)

        next_button = Button(button_group_frame,
                             text="next", relief="groove")
        next_button.place(relx=0, rely=0, relwidth=1/3, relheight=1/2)
        next_button.bind("<Button-1>", self.on_next_button_click)

        skip_button = Button(button_group_frame,
                             text="skip", relief="groove")
        skip_button.place(relx=1/3,
                          rely=0, relwidth=1/3, relheight=1/2)
        skip_button.bind("<Button-1>", self.on_skip_button_click)

        save_button = Button(button_group_frame, text="save", relief="groove")
        save_button.place(relx=2/3, rely=0, relwidth=1/3, relheight=1/2)
        save_button.bind("<Button-1>", self.on_save_button_click)

        no_match_button = Button(
            button_group_frame, text="no match", relief="groove")
        no_match_button.place(relx=0, rely=1/2, relwidth=1/3, relheight=1/2)
        no_match_button.bind("<Button-1>", self.on_no_match_button_click)

        my_answer_entry = Entry(button_group_frame)
        my_answer_entry.place(relx=1/3, rely=1/2, relwidth=1/3, relheight=1/2)

        my_answer_button = Button(
            button_group_frame, text="my answer", relief="groove")
        my_answer_button.place(relx=2/3, rely=1/2, relwidth=1/3, relheight=1/2)
        my_answer_button.bind("<Button-1>", self.on_my_answer_button_click)

        target_gird_frame = Frame(self.root)
        target_gird_frame.place(relx=0.05, rely=0.2,
                                relwidth=0.9, relheight=0.7)

        self.raw = raw
        self.raw_label = raw_label
        self.target = target
        self.target_label = target_label
        self.my_answer_button = my_answer_button
        self.my_answer_entry = my_answer_entry
        self.no_match_button = no_match_button
        self.target_gird_frame = target_gird_frame


if __name__ == "__main__":
    pass
