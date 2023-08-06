from pathlib import Path
from dataclasses import dataclass
from .terminal import warn
import platform
import tomllib
import typing

# Define the default paths
DEFAULT_NOTES_PATH: Path = Path(Path.home(), 'Documents', 'notes')
DEFAULT_EXTENSION: str = 'md'

# Structure of the config
@dataclass
class config_data():
    notes_dir_path: Path
    extension: str
    no_whitespaces: bool
    no_uppercase: bool
    no_firstline: bool

def init_config(custom_path: Path | None = None) -> Path:
    """
    Check if the config path and file exist and configure a custom path if it is given.
    """
    config_path: Path = get_default_config_path()

    if custom_path is not None:
        config_path = custom_path

    if not config_path.is_dir():
        config_path.mkdir()

    yaqn_path: Path = Path(config_path, 'yaqn')
    yaqn_file: Path = Path(yaqn_path, 'config.toml')

    if not yaqn_path.is_dir():
        yaqn_path.mkdir()

    if not yaqn_file.is_file():
        yaqn_file.touch()
        regenerate_config(yaqn_file, True)

    return yaqn_file

def get_default_config_path() -> Path:
    if platform.system() == 'Windows':
        return Path(Path.home(), 'AppData', 'Roaming')
    else:
        return Path(Path.home(), '.config')

def check_config(config_path: Path) -> None:
    """
    Check if the config file is valid
    """
    with open(config_path, 'rb') as config:
        # Check if the config is a valid toml file
        loaded_config: dict
        try:
            loaded_config = tomllib.load(config)
        except tomllib.TOMLDecodeError:
            regenerate_config(config_path)
            # Load the config again and check the structure
            return

        # Check if the config is following the expected structure
        match loaded_config:
            case {
                'notes_path': str(),
                'extension': str(),
                'no_whitespaces': bool(),
                'no_uppercase': bool(),
                'no_firstline': bool()
                }:
                pass
            case _:
                regenerate_config(config_path)


def regenerate_config(config_path: Path, silent: bool = False) -> None:
    """
    Rewrite the config file with all the defaults.
    """

    if not config_path.is_file():
        warn('Not config file was found, use \'yaqn --check\' to create a new one')

    if not silent:
        warn('The config was invalid and it has been restored to its defaults')
    
    # Rewrite all the config file
    with open(config_path, 'w') as config:
        config.writelines([
            f'notes_path = \'{DEFAULT_NOTES_PATH}\'',
            f'\nextension = \'{DEFAULT_EXTENSION}\'',
            f'\nno_whitespaces = false',
            f'\nno_uppercase = false',
            f'\nno_firstline = false',
            f'\n'
        ])

def read_config(custom_path: Path | None = None) -> config_data:
    """
    Read the config file, check it and repair it if is necessary.
    """
    config_path: Path = init_config(custom_path)
    check_config(config_path)

    with open(config_path, 'rb') as config:
        data: dict[str, typing.Any] = tomllib.load(config)

        if data['notes_path'] == 'default':
            data['notes_path'] = DEFAULT_NOTES_PATH

        return config_data(
            Path(data['notes_path']),
            data['extension'],
            data['no_whitespaces'],
            data['no_uppercase'],
            data['no_firstline']
        )

def restore_config(custom_path: Path | None = None) -> None:
    """
    Restore the configuration to its defaults values
    """
    config_path: Path = init_config(custom_path)
    regenerate_config(config_path, True)
