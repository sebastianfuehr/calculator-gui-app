from customtkinter import CTkButton
from settings import *


class CalculatorButton(CTkButton):
    """A custom calculator button.
    """
    def __init__(self, parent, text, command, col, row, font, span=1, color='dark-gray'):
        super().__init__(
            master=parent,
            text=text,
            command=command,
            corner_radius=STYLING['corner-radius'],
            font=font,
            fg_color=COLORS[color]['fg'],
            hover_color=COLORS[color]['hover'],
            text_color=COLORS[color]['text'])
        self.grid(column=col, row=row, sticky='nsew', columnspan=span, padx=STYLING['gap'], pady=STYLING['gap'])


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


class NumberButton(CalculatorButton):
    def __init__(self, parent, text, command, col, row, font, span=1, color='light-gray'):
        super().__init__(
            parent=parent,
            text=text,
            command=lambda: command(text),
            col=col,
            row=row,
            font=font,
            span=span,
            color=color
        )


class MathButton(CalculatorButton):
    def __init__(self, parent, text, operator, command, col, row, font, color='orange'):
        super().__init__(
            parent=parent,
            text=text,
            command=lambda: command(operator),
            col=col,
            row=row,
            font=font,
            color=color
        )


class MathImageButton(ImageButton):
    def __init__(self, parent, operator, command, col, row, image, color='orange'):
        super().__init__(
            parent=parent,
            command=lambda: command(operator),
            col=col,
            row=row,
            image=image,
            color=color
        )
