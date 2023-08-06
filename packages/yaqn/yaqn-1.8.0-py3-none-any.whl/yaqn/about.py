from .assets import get_logo_path_low_res, get_logo_path_high_res
from . import __version__
from pathlib import Path
import tkinter

class About(tkinter.Toplevel):
    def __init__(
            self,
            parent_window_position_x: int,
            parent_window_position_y: int, 
            parent_window_size_x: int,
            parent_window_size_y: int
        ) -> None:

        super().__init__()

        # Set the logo of the app and make it MacOS compatible
        logo_path: Path = get_logo_path_high_res()
        logo: tkinter.Image = tkinter.Image('photo', file=f'{logo_path}')
        # Disable type checking because _w is a internal Tkinter var and cant be detected by type checkers
        self.tk.call('wm','iconphoto', self._w, logo)  # type: ignore

        self.set_widgets()
        self.set_window_position(
            parent_window_position_x,
            parent_window_position_y,
            parent_window_size_x,
            parent_window_size_y
        )

    def set_widgets(self) -> None:
        self.title('About YAQN')
        self.resizable(False, False)

        # Set the logo of YAQN as the first half of the window
        self.image_frame: tkinter.Frame = tkinter.Frame(self)
        self.image_frame.pack(side=tkinter.TOP)

        # Define the logo as a tkinter image object
        logo_path: Path = get_logo_path_low_res()
        self.logo_image: tkinter.PhotoImage = tkinter.PhotoImage(file=logo_path)

        # Put the image object to a label
        self.image_label: tkinter.Label = tkinter.Label(
            self,
            image=self.logo_image
        )
        self.image_label.pack(
            padx=50,
            pady=(10, 5)
        )

        # Set the texts
        self.text_frame: tkinter.Frame = tkinter.Frame(self)
        self.text_frame.pack()

        # Set the title of the app and make it bold
        font_title: tkinter.font.Font = tkinter.font.Font(weight='bold')

        self.title: tkinter.Label = tkinter.Label(
            self.text_frame,
            text='YAQN',
            font=font_title
        )
        self.title.pack()

        font_subtitle: tkinter.font.Font = tkinter.font.Font(size=14)

        # Set the subtitle
        self.subtitle: tkinter.Label = tkinter.Label(
            self.text_frame,
            text='Yet Another Quick Note',
            font=font_subtitle
        )
        self.subtitle.pack()

        # Set the version number and make it smaller
        font_little: tkinter.font.Font = tkinter.font.Font(size=12)

        self.version: tkinter.Label = tkinter.Label(
            self.text_frame,
            text=f'Version {__version__}',
            font=font_little
        )
        self.version.pack(
            pady=(0, 5)
        )

        # Set the created by section
        self.created_by_frame: tkinter.Frame = tkinter.Frame(self)
        self.created_by_frame.pack(side=tkinter.BOTTOM)

        self.kutu_label: tkinter.Label = tkinter.Label(
            self.created_by_frame,
            text='Created with ♥ by\nKutu (@kutu-dev)',
            font=font_little
        )
        self.kutu_label.pack()

        self.other_authors_label: tkinter.Label = tkinter.Label(
            self.created_by_frame,
            text='App icon created by\n\'vladlucha\' in MacOS Icons',
            font=font_little
        )
        self.other_authors_label.pack(
            pady=(0, 25)
        )

    def set_window_position(
        self,
        parent_window_position_x: int,
        parent_window_position_y: int, 
        parent_window_size_x: int,
        parent_window_size_y: int
    ) -> None:

        # Make the window transparent and after update it to avoid seeing the window change its position
        self.attributes('-alpha', 0.0)
        self.update()

        window_width: int = self.winfo_width()
        window_height: int = self.winfo_height()

        parent_window_center_x: int = parent_window_position_x + parent_window_size_x/2
        parent_window_center_y: int = parent_window_position_y + parent_window_size_y/2

        # Calculate the coordinates for the top left of the window
        calculated_width: int = int(parent_window_center_x - window_width/2)
        calculated_height: int = int(parent_window_center_y - window_height/2)

        # Apply the correct position of the window
        self.geometry(f'{window_width}x{window_height}+{calculated_width}+{calculated_height}')

        # Detect when the window has finally moved and make it visible
        self.bind("<Configure>", self.make_window_visible)

    def make_window_visible(self, event: tkinter.Event):
        self.attributes('-alpha', 1.0)
        self.bind("<Configure>", None)
