import tkinter as tk
from minesweeper_functions import MinesweeperGame

if __name__ == "__main__":
    root = tk.Tk()
    MinesweeperGame(root)
    root.mainloop()