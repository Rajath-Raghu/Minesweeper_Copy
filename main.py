from tkinter import *
from cell import Cell
import settings
import utils


root = Tk()
# Overriding the settings of the window
root.title("MineSweeper")
root.geometry(f'{settings.Width}x{settings.Height}')
root.resizable(False, False)
root.configure(bg = "black")

# Creating Frames
Top_frame = Frame(root, bg = "black", width = settings.Width, height = utils.Height_prct(25))
Top_frame.place(x = 0, y = 0)

Game_Title = Label(Top_frame, bg = "White", fg = "Gold", text = "MINESWEEPER", font = ("Verdana", 50))
Game_Title.place(x = utils.Width_prct(25), y = 0)

Left_Frame = Frame(root, bg = "black", width = utils.Width_prct(25), height = utils.Height_prct(75))
Left_Frame.place(x = 0, y = utils.Height_prct(25))

Center_Frame = Frame(root, bg = "black", width = utils.Width_prct(75), height = utils.Height_prct(75))
Center_Frame.place(x = utils.Width_prct(25), y = utils.Height_prct(25))

for y in range(settings.Grid_Size):
    for x in range(settings.Grid_Size):
        c = Cell(x, y)
        c.create_btn_object(Center_Frame)
        c.cell_btn_object.grid(column = y, row = x)

# Calling the Label from the Cell Class
Cell.create_cell_count_label(Left_Frame)
Cell.cell_count_label_object.place(x = 0, y = 0)
Cell.randomize_mines()

# Running the window
root.mainloop()
