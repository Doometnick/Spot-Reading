from typing import Generator, Iterable
import tkinter as tk


class SpotReader:
    
    """ GUI displaying words in the canvas center with a delay. 

    Args:
        words: Iterable or generator of words that will be shown including 
            punctuation. Example: ['Hello,', 'my', 'name', 'is', 'Waldo.'].
        wpm: Words per minute according to which two subsequent words will
            be displayed.
        wpm_step: Magnitude of change in words per minute.
    """

    # Settings for tkinter GUI.
    WIDTH = 1200
    HEIGHT = 700
    BG_COLOR_TOP = '#002633'
    BG_COLOR = 'black'

    FONT = 'Consolas'
    FONT_SIZE = 20
    FONT_COLOR = 'white'

    def __init__(self, 
                 words, 
                 wpm=200,  
                 wpm_step=10):

        if isinstance(words, Generator):
            self.text = words
        elif isinstance(words, Iterable):
            self.text = iter(words)
        else:
            raise ValueError('words should be iterable or generator.')

        self.wpm = wpm
        self.wpm_step = wpm_step

        self.root = tk.Tk()
        self.root.wm_title('Spot Reading')
        self.root.configure(background=self.BG_COLOR)
        self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')

        self.topbar = tk.Frame(self.root, width=self.WIDTH, height=50, bg=self.BG_COLOR_TOP)
        self.topbuttonbar = tk.Frame(self.root, width=self.WIDTH, height=50, bg=self.BG_COLOR_TOP)
        self.bottom = tk.Frame(self.root, width=self.WIDTH, height=50, bg=self.BG_COLOR)
        
        # Setup individual frames for wpm text, 
        # speed buttons, and displayed text.
        self._setup_wpm_label()
        self._setup_wpm_change_buttons()
        self._setup_center_text()

        self.topbar.pack(fill='both')
        self.topbuttonbar.pack(fill='both')
        self.bottom.pack()
        
        self.root.after(self._text_delay, self._show_next_word)
        self.root.mainloop()

    @property
    def wpm(self):
        return self._wpm
    
    @wpm.setter
    def wpm(self, value):
        # Automatically update delay between two subsequent words.
        self._wpm = int(value)
        self._text_delay = 60 * 1000 // value
        

    def _display_text(self, text):
        self.txt_var.set(text)

    def _show_next_word(self):
        try:
            new_text = next(self.text)
        except StopIteration:
            self.txt_var.set('<Text has finished>')
        else:
            self._display_text(new_text)
            self.root.after(self._text_delay, self._show_next_word)

    def _setup_center_text(self):
        self.txt_var = tk.StringVar()
        self.msg = tk.Label(self.root, 
                            textvariable=self.txt_var, 
                            anchor=tk.CENTER, 
                            font=(self.FONT, self.FONT_SIZE),
                            bg=self.BG_COLOR,
                            fg=self.FONT_COLOR)
        self.msg.place(relx=.5, rely=.5, anchor=tk.CENTER)

    def _setup_wpm_label(self):
        self.wpm_var = tk.StringVar()
        self.msg = tk.Label(self.topbar,
                            textvariable=self.wpm_var,
                            anchor=tk.CENTER,
                            font=(self.FONT, self.FONT_SIZE),
                            bg=self.BG_COLOR_TOP,
                            fg=self.FONT_COLOR)
        self._update_wpm_display()
        self.msg.pack()
    
    def _setup_wpm_change_buttons(self):
        wpm_down_btn = tk.Button(
            self.topbuttonbar, text='--', command=self._decrease_wpm)
        wpm_down_btn.config(height=1, width=10)
        wpm_down_btn.place(relx=.46, rely=.5, anchor=tk.CENTER)
        
        wpm_up_btn = tk.Button(
            self.topbuttonbar, text='++', command=self._increase_wpm)
        wpm_up_btn.config(height=1, width=10)
        wpm_up_btn.place(relx=.54, rely=.5, anchor=tk.CENTER)

    def _increase_wpm(self):
        self.wpm += self.wpm_step
        self._update_wpm_display()

    def _decrease_wpm(self):
        self.wpm -= self.wpm_step
        self._update_wpm_display()

    def _update_wpm_display(self):
        """ Update the text variable used to show the wpm parameter. """
        self.wpm_var.set(f'wpm: {self.wpm}')
