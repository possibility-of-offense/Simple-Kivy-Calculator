# import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
# kivy.require('2.1.0')

class Calculator(App):
    show_current_operations_label = ''
    output_label = ''
    operations_lbl = ''
    prev_nums = [0]
    cur_nums = [0]
    symbols = ['']

    reset_numbers = False
    clear_data = False

    sound = SoundLoader.load('./sound.wav')
    sound_clear = SoundLoader.load('./Empty-trash-sound-effect.wav')

    operations = list()
    
    # Calc operation
    def calc_operation(self, symb, setting_symbol = {"to_set": False}, setting_prev = False):
        '''
            Reusable function for different types of calculations

            @return calculated value
        '''

        val_to_return = 0

        if symb == '*':
            val_to_return = int(self.prev_nums[0]) * int(self.cur_nums[0])
        elif symb == '/':
            val_to_return = int(self.prev_nums[0]) / int(self.cur_nums[0])
        elif symb == '+':
            val_to_return = int(self.prev_nums[0]) + int(self.cur_nums[0])
        elif symb == '-':
            val_to_return = int(self.prev_nums[0]) - int(self.cur_nums[0])

        operation_arg = f'{int(self.prev_nums[0])} {symb} {int(self.cur_nums[0])}'
        self.fill_operations_list(operation_arg)
        
        self.prev_nums[0] = 0
        self.cur_nums[0] = 0
        
        if setting_symbol['to_set'] is False:
            self.symbols[0] = ''
        else:
            self.symbols[0] = setting_symbol['symb']

            if setting_prev is True:
                self.prev_nums[0] = val_to_return

        return val_to_return

     # Reset numbers and symbols
    def reset_nums_and_symbols(self):
        '''
            Reset Numbers and symbols
        '''
        self.cur_nums[0] = 0
        self.prev_nums[0] = 0
        self.symbols[0] = ''

    # Build functions
    def build(self):
        '''
            Main building function

            Setting widgets + binding event handlers on the buttons press events
        '''

        Window.size = (600, 650)

        # Create parent widget
        layout = BoxLayout(orientation="vertical")

        # Init widgets
        buttons = ['1', '2', '3', '+',
                   '4', '5', '6', '-',
                   '7', '8', '9', 'Clear',
                   '0', '*', '/', '='
                  ]

        button_grid = GridLayout(cols=4, size_hint_y=2)
        for btn in buttons:
            button_grid.add_widget(Button(text=btn))

        for bind_btn in button_grid.children[1:]:
            bind_btn.bind(on_press=self.handle_btn_event)

        # = event handling
        button_grid.children[0].bind(on_press=self.handle_equal_event)

        self.show_current_operations_label = Label(text="")
        self.output_label = Label(text="Result: ", font_size="30px")

        operations_lbl_text = ', '.join(self.operations) if len(self.operations) > 0 else 'No operations yet!'

        self.operations_lbl = Label(text=operations_lbl_text, size_hint_y=.5, font_size="16px")

        # Append to parent widget
        layout.add_widget(self.show_current_operations_label)
        layout.add_widget(self.output_label)
        layout.add_widget(self.operations_lbl)
        layout.add_widget(button_grid)

        return layout

    # Press Handler
    def handle_btn_event(self, inst):
        '''
            Event handler for pressing the button

            @param inst -> current instance of the Button widget
        '''

        if inst.text == 'Clear':
            if self.clear_data:
                self.reset_nums_and_symbols()
                self.show_current_operations_label.text = ''
                self.operations = []
                self.output_label.text = 'Result: '
                self.operations_lbl.text = 'You have cleared the data'

                if self.sound_clear:
                    self.sound_clear.play()

            self.clear_data = False

        else:
            if self.reset_numbers:
                self.reset_nums_and_symbols()
                self.show_current_operations_label.text = ''

            self.show_current_operations_label.text += inst.text

            self.clear_data = True
            if inst.text.isnumeric():
                self.reset_numbers = False
                self.cur_nums[0] = int(str(self.cur_nums[0]) + inst.text)
            else:
                if self.symbols[0] == '':
                    self.symbols[0] = inst.text
                    self.prev_nums[0] = self.cur_nums[0]
                    self.cur_nums[0] = 0
                else:
                    get_symbol = self.symbols[0]
                    self.calc_operation(get_symbol, {"to_set": True, "symb": inst.text}, setting_prev = True)

    # Show something is = is clicked but there is nothing
    def handle_equal_event(self, inst, msg = 'Add numers'):
        '''
            Handler for pressing the '=' Button widget
        '''
        get_symbol = self.symbols[0]
        self.reset_numbers = True
        output = self.calc_operation(get_symbol)
                   
        self.show_current_operations_label.text = ''
        self.output_label.text = f'Result: {str(output)}'

        if self.sound:
            self.sound.play()

    # Fill the operations list
    def fill_operations_list(self, oper):
        self.operations.append(oper)
        if len(self.operations) > 10:
            self.operations.pop(0)
            self.operations_lbl.text = ' || '.join(self.operations)
        else:
            if self.operations_lbl.text == 'No operations yet!':
                self.operations_lbl.text = ''

            self.operations_lbl.text = ' || '.join(self.operations)

if __name__ == "__main__":
    Calculator().run()


