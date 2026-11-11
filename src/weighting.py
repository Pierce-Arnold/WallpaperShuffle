import json
import random
import glob
from pathlib import Path
import copy

def pick_weighted_random(images_directory, weighting_file):
    """
    Picks a random image from the images directory based on the weights specified in the weighting file.
    :param images_directory: Path to the images directory
    :param weighting_file: Path to the weighting file
    :return: Path to the selected image
    """
    images_directory = Path(images_directory)
    try:
        with open(weighting_file, 'r') as f:
            weight_data = json.load(f)
    except FileNotFoundError:
        print("Weighting file not found. Please create a weighting file and restart the program.")
        exit()
    except json.JSONDecodeError:
        print("Weighting file is not a valid JSON. Please fix the file and restart the program.")
        exit()

    image_weight_data = copy.deepcopy(weight_data)
    for item in list(image_weight_data):
        if "tag" in image_weight_data[item]["tags"]:
            del image_weight_data[item]
    tag_weight_data = copy.deepcopy(weight_data)
    for item in list(tag_weight_data):
        if "tag" not in tag_weight_data[item]["tags"]:
            del tag_weight_data[item]

    if not images_directory:
        print("Images directory not found. Creating a new images directory...")
        images_directory.mkdir(parents=True, exist_ok=True)
        print("Images directory created. Please add images to the directory and restart the program.")
        exit()

    full_image_file_paths = glob.glob(str(images_directory / "*.png"))
    full_image_file_paths += glob.glob(str(images_directory / "*.jpg"))
    full_image_file_paths += glob.glob(str(images_directory / "*.jpeg"))
    if not full_image_file_paths:
        print("No images found in the images directory. Please add images to the directory and restart the program.")
        exit()
    image_files = [Path(image).name for image in full_image_file_paths]

    #a 2d list of all images with their total weights
    all_images = []
    for image in image_files:
        if image in image_weight_data:
            weight = image_weight_data[image]["weight"]
            for tag in image_weight_data[image]["tags"]:
                try:
                    weight *= tag_weight_data[tag]["weight"]
                except KeyError:
                    pass
        else:
            weight = 1
        all_images.append([image, weight])

    if not all_images:
        print("No images found in the images directory. Please add images to the directory and restart the program.")
        exit()

    total_weight = sum([image[1] for image in all_images])
    rand_num = random.uniform(0, (total_weight - 0.0001))
    random_image = find_image(0, rand_num, all_images)
    full_random_image_path = images_directory / random_image
    return full_random_image_path


def find_image(start_weight, rand_num, all_images):
    """
    Recursively finds the image that corresponds to the random number generated based on the weights.
    :param start_weight: The starting weight for comparison
    :param rand_num: The random number generated
    :param all_images: List of all images with their weights
    :return: Path to the selected image
    """
    end_weight = start_weight + all_images[0][1]
    if start_weight <= rand_num < end_weight:
        return all_images[0][0]
    else:
        return find_image(end_weight, rand_num, all_images[1:])

def update_weighting_file(weighting_file_path, image_directory):
    """
    Updates the image_weighting.json file to include every image in the images folder
    with a default weight of 1 if it does not already exist in the file. Also adds
    entries for any tags not already defined. Also removes entries for images
    that no longer exist in the images folder.
    :param weighting_file_path: Path to the weighting file
    :param image_directory: Path to the images directory
    :return: None
    """
    image_directory = Path(image_directory)
    weighting_file_path = Path(weighting_file_path)

    # Load existing weighting data or create a new dictionary if the file doesn't exist
    if weighting_file_path.exists():
        with open(weighting_file_path, 'r') as f:
            try:
                weight_data = json.load(f)
            except json.JSONDecodeError:
                print("Weighting file is not a valid JSON. Please fix the file and restart the program.")
                exit()
    else:
        weight_data = {}

    # Get a list of all images in the images directory
    full_image_file_paths = glob.glob(str(image_directory / "*.png"))
    full_image_file_paths += glob.glob(str(image_directory / "*.jpg"))
    full_image_file_paths += glob.glob(str(image_directory / "*.jpeg"))
    image_files = [Path(image).name for image in full_image_file_paths]

    # Add new images to the weighting data with a default weight of 1
    for image in image_files:
        if image not in weight_data:
            weight_data[image] = {"weight": 1, "tags": []}

    # Remove entries for images that no longer exist in the images directory
    for image in list(weight_data.keys()):
        if image not in image_files:
            del weight_data[image]

    #Add new tag entries for any tags not already defined
    undefined_tags = []
    for image in weight_data:
        undefined_tags.extend(tag for tag in weight_data[image]["tags"] if tag not in weight_data)
    for tag in undefined_tags:
        weight_data[tag] = {"weight": 1, "tags": ["tag"]}

    # Write the updated weighting data back to the file
    with open(weighting_file_path, 'w') as f:
        json.dump(weight_data, f, indent=4)
