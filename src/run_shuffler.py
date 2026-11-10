
import time
from datetime import datetime
import os
import random
import json


def update_wallpaper():
    """
    Function to update the wallpaper with a random image from the images folder
    :return: None
    """
    print("Updating wallpaper...")


def create_default_settings():
    """
    Creates a default settings file if one does not exist
    :return: None
    """
    print("Creating default settings file...")
    default_settings = {"update_freq": "m", "continue_prog": "True"}
    json_string = json.dumps(default_settings, indent=4)
    try:
        os.makedirs("program_data")
    except FileExistsError:
        pass
    try:
        with open("program_data/settings.json", "w") as new_file:
            new_file.write(json_string)
    except Exception as e:
        print("Unexpected error:\n", str(e))
        print("Exiting...")
        exit()
    print("Default settings file created.")


if __name__ == '__main__':

    prev_time = datetime.now()
    settings_file = os.path.join("program_data", "settings.json")


    while True:
        time.sleep(1)
        current_time = datetime.now()
        try:
            with open(settings_file, 'r') as file:
                settings = json.load(file)
        except FileNotFoundError:
            print("Settings file not found. Generating default settings...")
            create_default_settings()
            with open(settings_file, 'r') as file:
                settings = json.load(file)
        except json.JSONDecodeError:
            print("Error decoding JSON. continuing...")
            continue
        except Exception as e:
            print("Unexpected error:\n", str(e))
            print("Exiting...")
            exit()

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
        prev_time = current_time
        print("looping...")