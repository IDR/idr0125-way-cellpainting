
# Run python s3_sync.py to output command for downloading to ftp server

# $ ssh -A idr-ftp.openmicroscopy.org
# $ cd /data/idrftp-incoming/idr0125-way-cellpainting/
# USE TODAY's date
# $ mkdir s3-20220927
# $ cd s3-20220927/
# $ conda activate aws

# Then run this script locally...
# $ cd idr0125-way-cell-painting
# $ python scripts/s3_sync.py

# This will output 2 commands. The first does the download.
# the 2nd command counts the .zarray items in each plate. Should be 3456 in each

# plates_yml = "docs/_data/plates.yml"
# 2nd batch of 48 (which failed to import into IDR) regenerated...
plates_yml = "docs/_data/plates_20221101.yml"
# command = """aws s3 sync --no-sign-request --exclude '*' --include "*.z*" --include "*.xml" s3://cellpainting-gallery/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/$a $a"""
command = """aws s3 sync --no-sign-request --exclude '*' --include "*.z*" --include "*.xml" s3://cellpainting-gallery/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr_050/$a $a"""


# Just update these numbers each time to select a different batch of plates from the list
first_plate_index = 0
batch_size = 50

plates = []
with open(plates_yml) as f:
    plates = [line.replace("- ", "").strip() for line in f.readlines()]

plate_names = " ".join(plates[first_plate_index: first_plate_index + batch_size])

# $ for a in SQ00014812__2016-05-23T20_44_31-Measurement1.ome.zarr SQ00014813__2016-05-23T19_03_28-Measurement1.ome.zarr; do mkdir $a; aws s3 sync --no-sign-request --exclude '*' --include "*.z*" --include "*.xml" s3://cellpainting-gallery/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/$a $a; done
print('for a in %s; do mkdir $a; %s; done' % (plate_names, command))
print("")
print('for a in %s; do echo $a; find ./$a/ -name ".zarray" | wc; done' % plate_names)

# plates with less that 3456 .zarray files:
# SQ00015096__2016-06-08T17_05_23-Measurement1.ome.zarr     239
# SQ00015097__2016-06-08T15_26_27-Measurement1.ome.zarr     365
# SQ00015140__2016-06-11T14_43_11-Measurement1.ome.zarr     2620
# SQ00015151__2016-06-09T05_07_35-Measurement1.ome.zarr     489
# SQ00015160__2016-04-15T03_50_42-Measurement1.ome.zarr     456
# SQ00015204__2016-04-24T20_02_01-Measurement2.ome.zarr     864
# SQ00015205__2016-04-24T02_21_50-Measurement1.ome.zarr     817
# SQ00015212__2016-04-23T19_01_00-Measurement1.ome.zarr     2160
# SQ00015229__2016-05-13T08_10_01-Measurement1.ome.zarr     1103
# SQ00015232__2016-05-12T07_24_32-Measurement1.ome.zarr     55
