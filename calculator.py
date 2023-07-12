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
from buttons import CalculatorButton, ImageButton, NumberButton, MathButton, MathImageButton


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
        self.display_nums = []
        self.full_operation = []

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
        
        # Invert button
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

        # Number buttons
        for num, data in NUM_POSITIONS.items():
            NumberButton(
                parent=self,
                text=num,
                command=self.num_press,
                col=data['col'],
                row=data['row'],
                font=main_font,
                span=data['span']
            )
    
        # Math operator buttons
        for operator, data in MATH_POSITIONS.items():
            if data['image path']:
                divide_image = ctk.CTkImage(
                    light_image=Image.open(data['image path']['dark']),
                    dark_image=Image.open(data['image path']['light'])
                )
                MathImageButton(
                    parent=self,
                    operator=operator,
                    command=self.math_press,
                    col=data['col'],
                    row=data['row'],
                    image=divide_image
                )
            else:
                MathButton(
                    parent=self,
                    text=data['character'],
                    operator=operator,
                    command=self.math_press,
                    col=data['col'],
                    row=data['row'],
                    font=main_font,
                )

    def clear(self):
        self.result_str.set(0)
        self.formula_str.set('')

        self.display_nums.clear()
        self.full_operation.clear()

    def percent(self):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percent = current_number/100
            self.display_nums = list(str(percent))
            self.result_str.set(''.join(self.display_nums))

    def invert(self):
        current_number = ''.join(self.display_nums)
        if current_number:
            if float(current_number) > 0:
                self.display_nums.insert(0, '-')
            else:
                del self.display_nums[0]

            self.result_str.set(''.join(self.display_nums))

    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = ''.join(self.display_nums)
        self.result_str.set(full_number)

    def math_press(self, operator):
        curr_number = ''.join(self.display_nums)
        if curr_number:
            self.full_operation.append(curr_number)

            if operator != '=':
                # Update data
                self.full_operation.append(operator)
                self.display_nums.clear()

                # Update output
                self.result_str.set('')
                self.formula_str.set(' '.join(self.full_operation))
            else:
                formula = ''.join(self.full_operation)
                result = eval(formula)

                # Format result
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)

                # Update output
                self.result_str.set(result)
                self.formula_str.set(' '.join(self.full_operation))

                # Update data
                self.full_operation.clear()
                self.display_nums = [str(result)]

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