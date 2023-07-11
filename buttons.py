from customtkinter import CTkButton
from settings import *


class CalculatorButton(CTkButton):
    """A custom calculator button.
    """
    def __init__(self, parent, text, command, col, row, font, color='dark-gray'):
        super().__init__(
            master=parent,
            text=text,
            command=command,
            corner_radius=STYLING['corner-radius'],
            font=font,
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover'],
            text_color=COLORS[color]['text'])
        self.grid(column=col, row=row, sticky='nsew', padx=STYLING['gap'], pady=STYLING['gap'])

class ImageButton(CTkButton):
    def __init__(self, parent, command, col, row, image, text='', color='dark-gray'):
        super().__init__(
            master=parent,
            text=text,
            command=command,
            image=image,
            corner_radius=STYLING['corner-radius'],
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover'],
            text_color=COLORS[color]['text']
        )
        self.grid(column=col, row=row, sticky='nsew', padx=STYLING['gap'], pady=STYLING['gap'])
