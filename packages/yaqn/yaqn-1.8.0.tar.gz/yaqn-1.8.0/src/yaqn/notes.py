from pathlib import Path
from datetime import datetime
from .config import config_data

def save_note(note_title: str, note_data: str, config_data: config_data):
        notes_dir_path: Path = config_data.notes_dir_path
        extension: str = config_data.extension
        no_whitespaces: bool = config_data.no_whitespaces
        no_uppercase: bool = config_data.no_uppercase
        no_firstline: bool = config_data.no_firstline

        # Create the notes path
        notes_dir_path.mkdir(parents=True, exist_ok=True)

        # Check if the first line in the textbox is valid as a filename
        note_filename: str
        if note_title != '':
            note_filename = note_title
        else:
            note_filename = datetime.now().strftime('%H%M%S-%d%m%Y')

        if no_whitespaces:
            # Remove all whitespaces and split the words with hyphens
            note_filename = '-'.join(note_filename.split())

        if no_uppercase:
            note_filename = note_filename.lower()

        if no_firstline:
            # Split the text of the note in lines, discard the first line and convert to string
            note_list_modified: list[str] = note_data.split('\n')[1:]
            note_data = '\n'.join(note_list_modified)

        # Get the note path and check if its valid
        note_path: Path = Path(notes_dir_path, f'{note_filename}.{extension}')
        note_path = check_note_path(note_path)

        # Get the textbox data and save it
        note:str = note_data
        
        note_path.touch()
        with open(note_path, 'w') as file:
            file.write(note)

def check_note_path(note_path: Path) -> Path:
    if not note_path.is_file():
        return note_path
    
    datetime_now: str = datetime.now().strftime('%H%M%S-%d%m%Y')
    new_filename: str = f'{note_path.stem}-{datetime_now}{note_path.suffix}'

    return check_note_path(Path(note_path.parent, new_filename))
