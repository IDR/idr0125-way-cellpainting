
import os
from ome_zarr.io import parse_url
from ome_zarr.reader import Reader
import numpy as np
from datetime import datetime
from PIL import Image
import requests
from pathlib import Path
import yaml

base_url = "https://cellpainting-gallery.s3.amazonaws.com/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/"
# plate_names = ["SQ00014812__2016-05-23T20_44_31-Measurement1.ome.zarr"]

plate_yml_url = "https://raw.githubusercontent.com/IDR/idr0125-way-cellpainting/main/docs/_data/plates.yml"

yml_text = requests.get(plate_yml_url).text
plate_names = yaml.safe_load(yml_text)


OUT_DIR = "thumbnails" 

def process_image(url, save_path):

    if os.path.exists(save_path):
        print("Image exists at ", save_path, " Skipping...")
        return
    print(save_path)

    # read the image data
    store = parse_url(url, mode="r").store

    reader = Reader(parse_url(url))
    # nodes may include images, labels etc
    nodes = list(reader())
    # first node will be the image pixel data
    image_node = nodes[0]

    pyramid = image_node.data
    # Use smallest resolution of the pyramid
    dask_data = pyramid[-1]


    # rgb = np.dstack((red, green, blue))
    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    YELLOW = (1, 1, 0)
    WHITE = (1, 1, 1)

    active_colors = [BLUE, GREEN, RED]
    active_windows = [[200, 32000], [400, 30000], [507, 8173]]

    rgb = setActiveChannels(dask_data, [0, 1, 4], active_colors, active_windows)
    img = Image.fromarray(rgb)
    img.resize((96, 96))
    img.save(save_path, "JPEG")


def display(image, display_min, display_max): # copied from Bi Rico
    # https://stackoverflow.com/questions/14464449/using-numpy-to-efficiently-convert-16-bit-image-data-to-8-bit-for-display-with
    image.clip(display_min, display_max, out=image)
    image -= display_min
    np.floor_divide(image, (display_max - display_min + 1) / 256,
                    out=image, casting='unsafe')
    return image.astype(np.uint8)

def render_plane(dask_data, z, c, t, window=None):
    # slice 5D -> 2D
    channel0 = dask_data[t, c, z, :, :]
    channel0 = channel0.compute()

    if window is None:
        min_val = channel0.min()
        max_val = channel0.max()
        window = [min_val, max_val]

    return display(channel0, window[0], window[1])


def setActiveChannels(dask_data, active_indecies, colors, windows=None):
    # colors are (r, g, b)
    rgb_plane = None

    the_z = 0
    the_t = 0
    for idx, ch_index in enumerate(active_indecies):
        color = colors[idx]
        window = windows[idx] if windows is not None else None
        print("----", ch_index, color, window)
        plane = render_plane(dask_data, the_t, ch_index, the_z, window)
        if rgb_plane is None:
            rgb_plane = np.zeros((*plane.shape, 3), np.uint16)
        for index, fraction in enumerate(color):
            if fraction > 0:
                rgb_plane[:, :, index] += (fraction * plane)

    rgb_plane.clip(0, 255, out=rgb_plane)
    return rgb_plane.astype(np.uint8)


for plate_name in plate_names:

    plate_url = base_url + plate_name
    plate_json = requests.get(plate_url + "/.zattrs").json()["plate"]
    for well in plate_json["wells"]:
        well_url = plate_url + "/" + well["path"]
        well_json = requests.get(well_url + "/.zattrs").json()["well"]
        # creating directory for Well
        Path(os.path.join(OUT_DIR, plate_name, well["path"])).mkdir(parents=True, exist_ok=True)
        for image in well_json["images"]:
            img_url = well_url + "/" + image["path"] + "/"
            save_path = os.path.join(OUT_DIR, plate_name, well["path"], image["path"])
            process_image(img_url, save_path)

