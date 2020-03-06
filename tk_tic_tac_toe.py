"""
Tic-Tac-Toe game with tkinter frontend and numpy backend
"""

from typing import Tuple
from itertools import cycle
from tkinter import Tk, Frame, Button, Label
from numpy import full, flipud


def is_win(field, flag):
    """
    Checks the field for winning player moves
    :param field: game field (numpy matrix) with moves
    :param flag: X or 0
    :return: bool
    """
    diagonal = (
        field.diagonal() == flag).all() or (
            flipud(field).diagonal(0)[::-1] == flag).all()
    horizontal = [row for row in field if all(row == flag)]
    vertical = [col for col in field.T if all(col == flag)]
    return diagonal or horizontal or vertical


class TicTacToe:
    """ The main widget for the game """

    def __init__(self, master, field_size: Tuple[int, int], buttons_size: Tuple[int, int]):
        self.field = full((field_size[0], field_size[1]), '')
        self.steps = cycle(('X', '0'))

        # Create frame for Tic-Tac-Toe with step buttons
        self.frame = Frame(master)
        for i in range(0, self.field.shape[0]):
            for j in range(0, self.field.shape[1]):
                button = Button(self.frame, width=buttons_size[0], height=buttons_size[1],
                                font=('helvetica', 15))
                button.bind('<Button-1>', self.step)
                button.grid(row=i, column=j)

        self.game_state = Label()
        self.new_game_btn = Button(master, text="New game", width=20)
        self.new_game_btn['command'] = self.new_game
        self.frame.pack(padx=20, pady=20)
        self.new_game_btn.pack()
        self.game_state.pack()

    def step(self, event):
        """
        Marks a step on the playing field and checks the field for winning steps
        """
        btn = event.widget

        # If button is not clocked - commit step
        if btn['text'] == '':
            info = event.widget.grid_info()
            row = info['row']
            column = info['column']
            current_step = next(self.steps)
            btn['text'] = current_step
            self.field[row][column] = current_step

            # If win - stop game
            if is_win(self.field, current_step):
                self.game_state['text'] = f'{current_step} won!'
                self.stop_game()

    def new_game(self):
        """
        Resets the game to its original state when the "New game" button is pressed
        """
        # Reload steps iterator
        self.steps = cycle(('X', '0'))

        # Erase game field
        self.field.fill(None)

        # Activate buttons
        for btn in self.frame.grid_slaves():
            btn.config(state="normal", text="")
            btn.bind('<Button-1>', self.step)
        # Erase information about winner
        self.game_state['text'] = ''

    def stop_game(self):
        """
        Stops the game and makes the buttons inactive
        """
        # Deactivate all buttons
        for btn in self.frame.grid_slaves():
            btn.bind('<Button-1>', self.new_game)
            btn.config(state="disabled")


ROOT = Tk()
BLOCK = TicTacToe(ROOT, (3, 3), (1, 1))
ROOT.mainloop()
