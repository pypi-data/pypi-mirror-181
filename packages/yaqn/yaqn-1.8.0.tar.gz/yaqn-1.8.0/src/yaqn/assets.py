from pathlib import Path

def get_logo_path_high_res():
    logo_path: Path = Path(
        Path(__file__).parent, # Get the path to the root of the package
        'assets/logo_high_res.png'
    ).absolute()

    return logo_path

def get_logo_path_low_res():
    logo_path: Path = Path(
        Path(__file__).parent, # Get the path to the root of the package
        'assets/logo_low_res.png'
    ).absolute()

    return logo_path
