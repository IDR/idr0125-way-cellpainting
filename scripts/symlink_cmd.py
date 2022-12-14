
# Run python symlink_cmd.py to output command for symlinking imported plates
# from managed repo to s3-mount.

# sudo -u omero-server -s

# cd /data/OMERO/ManagedRepository/demo_2/Blitz-0-Ice.ThreadPool.Server-28/2022-10/15/05-53-40.405
# rm -rf SQ00015233__2016-05-12T05_47_03-Measurement1.ome.zarr
# ln -s /cellpainting-gallery/cpg0004-lincs/broad/images_zarr/2016_04_01_a549_48hr_batch1/images/SQ00015233__2016-05-12T05_47_03-Measurement1.ome.zarr SQ00015233__2016-05-12T05_47_03-Measurement1.ome.zarr

file_path = "imported_paths.txt"
s3_plates_dir = "/cellpainting-gallery/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/"

paths = []
with open(file_path) as f:
    paths = [path.strip() for path in f.readlines()]

# paths = paths[30:]

# Run this before running: $ bash ./symlinks.bash
print("sudo -u omero-server -s")

# Put everything after this into symlinks.bash
print("\n#!/bin/bash")

for line in paths:
    import_dir = line.split("/SQ0")[0]
    plate_name = "SQ0" + line.split("/SQ0")[1]

    print(f"echo {plate_name}")
    print(f"cd /data/OMERO/ManagedRepository/{import_dir}")
    print(f"rm -rf {plate_name}")
    print(f"ln -s {s3_plates_dir}{plate_name} {plate_name}")


for line in paths:
    # ls /A/1/well/resolution/t/c/z/y -> should give chunks 0 1 2
    import_dir = line.split("/SQ0")[0]
    plate_name = "SQ0" + line.split("/SQ0")[1]
    print(f"ls /data/OMERO/ManagedRepository/{import_dir}/{plate_name}/A/1/0/0/0/0/0/0/")
