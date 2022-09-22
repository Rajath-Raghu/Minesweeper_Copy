from tkinter import Button, Label
# noinspection PyUnresolvedReferences
import random
import settings
import ctypes
import sys


class Cell:
    all = []
    cell_count = settings.Cell_Count
    cell_count_label_object = None
    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_mine_candidate = False
        self.is_opened = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # Append the object to Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(location, width = 18, height = 5)
        btn.bind("<Button-1>", self.left_click_action) # Left Button
        btn.bind("<Button-3>", self.right_click_action)  # Right Button
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(location, bg = "Black", fg = "White", font = ("Verdana", 20), text = f"Cells Left:{Cell.cell_count}")
        Cell.cell_count_label_object = lbl

    def left_click_action(self, event):
        if self.is_mine:
            self.Show_Mine()
        else:
            if self.Show_Mines_Length == 0:
                for cell_obj in self.Surrounding_Cells:
                    cell_obj.Show_Cell()
            self.Show_Cell()
            # If Mine count is equal to Cell count, player won
            if Cell.cell_count == settings.Mine_Count:
                ctypes.windll.user32.MessageBoxW(0, "You have swept all the Mines!!", "Game Won!!", 0)

        # Cancel Left and Right Click events if the cells are open
        self.cell_btn_object.unbind("<Button-1>")
        self.cell_btn_object.unbind("<Button-3>")

    def Get_Cell_By_Axis(self, x, y):
        # Return a cell obj based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def Surrounding_Cells(self):
        cells = [
            self.Get_Cell_By_Axis(self.x - 1, self.y - 1),
            self.Get_Cell_By_Axis(self.x - 1, self.y),
            self.Get_Cell_By_Axis(self.x - 1, self.y + 1),
            self.Get_Cell_By_Axis(self.x, self.y - 1),
            self.Get_Cell_By_Axis(self.x + 1, self.y - 1),
            self.Get_Cell_By_Axis(self.x + 1, self.y),
            self.Get_Cell_By_Axis(self.x + 1, self.y + 1),
            self.Get_Cell_By_Axis(self.x, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    def Show_Cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text = self.Show_Mines_Length)

            # Updating the cell count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text = f"Cells Left:{Cell.cell_count}")
            # If mine_candidate, for safety, configure the BG colour to SystemButtonFace
            self.cell_btn_object.configure(bg = "SystemButtonFace")
        # Mark the cell as opened(Used as last line of this method)
        self.is_opened = True

    @property
    def Show_Mines_Length(self):
        counter = 0
        for cell in self.Surrounding_Cells:
            if cell.is_mine:
                counter += 1
        return counter

    def Show_Mine(self):
        # Logic to interrupt the game and display a message that player lost
        self.cell_btn_object.configure(bg = "Red")
        ctypes.windll.user32.MessageBoxW(0, "You clicked a Mine!!", "Game Over!!", 0)
        sys.exit()

    def right_click_action(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg = "Orange")
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(bg = "SystemButtonFace")
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        mine_cells = random.sample(Cell.all, settings.Mine_Count)

        for mine_cell in mine_cells:
            mine_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
