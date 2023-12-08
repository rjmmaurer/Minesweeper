import tkinter as tk
from tkinter import simpledialog, messagebox
import random
from typing import List, Tuple

class MinesweeperGame:
    def __init__(self, master: tk.Tk) -> None:
        """
        Initialize the Minesweeper game.

        Parameters:
            master (tk.Tk): The master Tkinter window.
        """
        self.master = master
        self.rows = 0
        self.cols = 0
        self.num_mines = 0

        self.buttons: List[List[tk.Button]] = []
        self.board: List[List[int]] = []
        self.mines: set[Tuple[int, int]] = set()
        
        self.board_clickable = True        
        self.game_over_flag = False

        self.create_widgets()
        self.new_game()

    def create_widgets(self) -> None:
        """
        Create the GUI widgets.
        """
        self.master.title("Minesweeper")

        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.new_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.destroy)

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack()

    def new_game(self) -> None:
        """
        Start a new game.
        """
        if self.rows > 0 and self.cols > 0 and self.num_mines > 0:
            self.destroy_widgets()

        self.rows, self.cols, self.num_mines = self.get_game_settings()
        self.board = [[0] * self.cols for _ in range(self.rows)]

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack()

        self.buttons = [[tk.Button(self.buttons_frame, width=2, height=1, command=lambda r=row, c=col: self.click(r, c))
                         for col in range(self.cols)] for row in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col].grid(row=row, column=col)

        self.generate_mines()
        self.update_counts()

    def destroy_widgets(self) -> None:
        """
        Destroy the existing GUI widgets.
        """
        for row in self.buttons:
            for button in row:
                button.destroy()
        self.buttons_frame.destroy()

    def get_game_settings(self) -> Tuple[int, int, int]:
        """
        Get the game settings from the user.

        Returns:
            Tuple[int, int, int]: The number of rows, columns, and mines.
        """
        rows = simpledialog.askinteger("Minesweeper", "Enter the number of rows:", initialvalue=8)
        cols = simpledialog.askinteger("Minesweeper", "Enter the number of columns:", initialvalue=8)
        num_mines = simpledialog.askinteger("Minesweeper", "Enter the number of mines:", initialvalue=5)

        return rows, cols, num_mines

    def generate_mines(self) -> None:
        """
        Generate mine positions for the game.
        """
        self.mines = set()
        while len(self.mines) < self.num_mines:
            mine = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
            self.mines.add(mine)

    def update_counts(self) -> None:
        """
        Update the count of mines in neighboring cells.
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.mines:
                    count = sum(1 for i in range(-1, 2) for j in range(-1, 2)
                                if (row + i, col + j) in self.mines)
                    self.board[row][col] = count

    def click(self, row: int, col: int) -> None:
        """
        Handle button click event.

        Parameters:
            row (int): The row index of the clicked button.
            col (int): The column index of the clicked button.
        """
        if (row, col) in self.mines:
            self.game_over()
        else:
            self.reveal(row, col)
            self.check_win()

    def reveal(self, row: int, col: int) -> None:
        """
        Reveal the content of the clicked button and its neighbors.

        Parameters:
            row (int): The row index of the clicked button.
            col (int): The column index of the clicked button.
        """
        button = self.buttons[row][col]
        if button["state"] == tk.NORMAL:
            count = self.board[row][col]
            if count > 0:
                button.config(text=str(count), state=tk.DISABLED, bg="lightgreen")
            else:
                button.config(state=tk.DISABLED, bg="lightgreen")
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= row + i < self.rows and 0 <= col + j < self.cols:
                            self.reveal(row + i, col + j)

    def game_over(self) -> None:
        """
        Handle the game over condition.
        """
        for row, col in self.mines:
            self.buttons[row][col].config(text="*", state=tk.DISABLED, bg="lightcoral")
        messagebox.showinfo("Game Over", "You hit a mine!")
        self.board_clickable = False
        self.game_over_flag = True


    def check_win(self) -> None:
        """
        Check if the player has won the game.
        """
        unrevealed_buttons = sum(1 for row in self.buttons for button in row if button["state"] == tk.NORMAL)
        if unrevealed_buttons == self.num_mines:
            messagebox.showinfo("You Win!", "Congratulations, you've cleared the board!")
            self.board_clickable = False
            self.game_over_flag = True