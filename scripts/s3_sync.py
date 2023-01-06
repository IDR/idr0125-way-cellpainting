
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

plates_yml = "docs/_data/plates.yml"

command = """aws s3 sync --no-sign-request --exclude '*' --include "*.z*" --include "*.xml" s3://cellpainting-gallery/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/$a $a"""

# Just update these numbers each time to select a different batch of plates from the list
first_plate_index = 118
batch_size = 30

plates = []
with open(plates_yml) as f:
    plates = [line.replace("- ", "").strip() for line in f.readlines()]
    plates = [line.split("/")[1] for line in plates]

plate_names = " ".join(plates[first_plate_index: first_plate_index + batch_size])

# $ for a in SQ00014812__2016-05-23T20_44_31-Measurement1.ome.zarr SQ00014813__2016-05-23T19_03_28-Measurement1.ome.zarr; do mkdir $a; aws s3 sync --no-sign-request --exclude '*' --include "*.z*" --include "*.xml" s3://cellpainting-gallery/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/$a $a; done
print('for a in %s; do mkdir $a; %s; done' % (plate_names, command))
print("")
print('for a in %s; do echo $a; find ./$a/ -name ".zarray" | wc; done' % plate_names)

