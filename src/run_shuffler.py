
import time
from datetime import datetime
import json
from pathlib import Path
import ctypes
from src.weighting import pick_weighted_random, update_weighting_file


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROGRAM_DATA_DIR = PROJECT_ROOT / "program_data"
SETTINGS_FILE = PROGRAM_DATA_DIR / "settings.json"
IMAGE_WEIGHTING_FILE = PROGRAM_DATA_DIR / "image_weighting.json"
IMAGES_DIR = PROJECT_ROOT / "images"


def update_wallpaper():
    """
    Function to update the wallpaper with a random image from the images folder
    :return: None
    """
    try:
        update_weighting_file(IMAGE_WEIGHTING_FILE, IMAGES_DIR)
        random_image_path = pick_weighted_random(IMAGES_DIR, IMAGE_WEIGHTING_FILE)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(random_image_path), 3)
    except Exception as e:
        print("Unexpected error:\n", str(e))
        print("Exiting...")
        exit()
    print("Wallpaper updated...")

def create_default_settings():
    """
    Creates a default settings file if one does not exist
    :return: None
    """
    print("Creating default settings file...")
    default_settings = {"update_freq": "h", "continue_prog": "True"}
    json_string = json.dumps(default_settings, indent=4)
    try:
        PROGRAM_DATA_DIR.mkdir(parents=True, exist_ok=True)
        with SETTINGS_FILE.open("w") as new_file:
            new_file.write(json_string)
        write_current_time_to_settings()
    except Exception as e:
        print("Unexpected error:\n", str(e))
        print("Exiting...")
        exit()
    print("Default settings file created.")

def write_current_time_to_settings():
    """
    Writes the current time to the settings file
    :return: None
    """
    current_time = datetime.now()
    try:
        with SETTINGS_FILE.open('r') as file:
            settings = json.load(file)
        settings["last_update_sec"] = current_time.second
        settings["last_update_min"] = current_time.minute
        settings["last_update_hour"] = current_time.hour
        settings["last_update_day"] = current_time.day
        settings["last_update_month"] = current_time.month
        settings["last_update_year"] = current_time.year
        with SETTINGS_FILE.open('w') as file:
            json.dump(settings, file, indent=4)
    except Exception as e:
        print("Unexpected error:\n", str(e))
        print("Exiting...")
        exit()

def read_last_update_time_from_settings():
    """
    Reads the last update time from the settings file
    :return: datetime object of last update time
    """
    try:
        with SETTINGS_FILE.open('r') as file:
            settings = json.load(file)
        last_update_time = datetime(
            year=settings["last_update_year"],
            month=settings["last_update_month"],
            day=settings["last_update_day"],
            hour=settings["last_update_hour"],
            minute=settings["last_update_min"],
            second=settings["last_update_sec"]
        )
        return last_update_time
    except FileNotFoundError:
        print("Settings file not found. Generating default settings...")
        create_default_settings()
        return read_last_update_time_from_settings()
    except Exception as e:
        print("Unexpected error:\n", str(e))
        print("Exiting...")
        exit()

def read_settings():
    """
    Reads the settings file and returns the settings as a dictionary
    :return: settings dictionary
    """
    try:
        with SETTINGS_FILE.open('r') as file:
            settings = json.load(file)
    except FileNotFoundError:
        print("Settings file not found. Generating default settings...")
        create_default_settings()
        with SETTINGS_FILE.open('r') as file:
            settings = json.load(file)
    except json.JSONDecodeError as e:
        print("Error decoding JSON.\n", str(e))
        print("Exiting...")
        exit()
    except Exception as e:
        print("Unexpected error:\n", str(e))
        print("Exiting...")
        exit()
    return settings


if __name__ == '__main__':

    write_current_time_to_settings()
    while True:
        prev_time = read_last_update_time_from_settings()
        time.sleep(1)
        current_time = datetime.now()
        settings = read_settings()

        if settings["continue_prog"] == "False":
            print("Exiting...")
            exit()

        update_freq = settings["update_freq"]
        if update_freq == "m":
            if current_time.minute != prev_time.minute:
                update_wallpaper()
        if update_freq == "h":
            if current_time.hour != prev_time.hour:
                update_wallpaper()
        if update_freq == "d":
            if current_time.day != prev_time.day:
                update_wallpaper()
        write_current_time_to_settings()
        print("looping...")
