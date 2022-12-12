
import requests

SERVER = "http://localhost:1080/"

screen_id = 3054
plates_url = SERVER + f"webclient/api/plates/?id={screen_id}"

plates_json = requests.get(plates_url).json()

for plate in plates_json["plates"]:

    wells_url = SERVER + f"webgateway/plate/{plate['id']}/0/"
    wells_json = requests.get(wells_url).json()
    first_img_id = wells_json["grid"][0][0]['id']

    files_url = SERVER + f"webgateway/original_file_paths/{first_img_id}/"
    # print("files_url", files_url)
    files_json = requests.get(files_url).json()

    first_path = files_json["repo"][0]
    # "demo_2/Blitz-0-Ice.ThreadPool.Server-11/2022-10/06/09-46-37.995/SQ00014812__2016-05-23T20_44_31-Measurement1.ome.zarr/H/13/0/.zattrs"
    path_to_plate = first_path.split("ome.zarr")[0]

    print(path_to_plate + "ome.zarr")
