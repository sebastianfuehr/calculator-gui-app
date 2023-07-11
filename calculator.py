import customtkinter as ctk
import darkdetect
# Windows only (title bar color)
try:
    from ctypes import windll, byref, sizeof, client
except:
    pass
from PIL import Image
# Custom modules
from settings import *
from buttons import CalculatorButton, ImageButton


class Calculator(ctk.CTk):
    """Application entrypoint, encapsulating the application layout
    and the application logic.
    """
    def __init__(self, is_dark):
        super().__init__(fg_color=(WHITE, BLACK))

        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')

        # Windows only
        self.__title_bar_color(is_dark)

        # Data
        self.result_str = ctk.StringVar(value='0')
        self.formula_str = ctk.StringVar(value='')

        # Layout
        self.grid_rowconfigure(list(range(MAIN_ROWS)), weight=1, uniform='a')
        self.grid_columnconfigure(list(range(MAIN_COLUMNS)), weight=1, uniform='a')

        # Widgets
        self.__create_widgets()

        self.mainloop()

    def __create_widgets(self):
        main_font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family=FONT, size=OUTPUT_FONT_SIZE)
        
        OutputLabel(
            self, 0, str_variable=self.formula_str, sticky='se', font=main_font
        )
        OutputLabel(
            self, 1, str_variable=self.result_str, sticky='e', font=result_font
        )

        # Buttons
        CalculatorButton(
            parent=self,
            text=OPERATORS['clear']['text'],
            command=self.clear,
            col=OPERATORS['clear']['col'],
            row=OPERATORS['clear']['row'],
            font=main_font)
        
        CalculatorButton(
            parent=self,
            text=OPERATORS['percent']['text'],
            command=self.percent,
            col=OPERATORS['percent']['col'],
            row=OPERATORS['percent']['row'],
            font=main_font)
        
        img_invert = ctk.CTkImage(
            light_image=Image.open(OPERATORS['invert']['image path']['dark']),
            dark_image=Image.open(OPERATORS['invert']['image path']['light'])
        )
        ImageButton(
            parent=self,
            text=OPERATORS['invert']['text'],
            command=self.invert,
            col=OPERATORS['invert']['col'],
            row=OPERATORS['invert']['row'],
            image=img_invert
        )

    def clear(self):
        print('Clear')

    def percent(self):
        print('Percent')

    def invert(self):
        print('Invert')

    def __title_bar_color(self, is_dark):
        """Hide the title bar somewhat by giving it the same background
        color as the rest of the application.

        WORKS ONLY ON WINDOWS!
        """
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS['dark'] if is_dark else TITLE_BAR_HEX_COLORS['light']
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass


class OutputLabel(ctk.CTkLabel):
    """Shows the output of the calculator.
    """
    def __init__(self, parent, row, str_variable, sticky, font):
        super().__init__(master=parent, font=font, textvariable=str_variable)
        self.grid(row=row, column=0, columnspan=4, sticky=sticky, padx=10)


if __name__ == '__main__':
    Calculator(darkdetect.isDark())