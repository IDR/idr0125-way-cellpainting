
"""
Modify the annotation.csv file to be compatible with Bio-FileFinder.
We only need to add a "File Path" column that contains the URL to the images.

Usage:

$ cd scripts
$ python csv_to_biofilefinder.py ../screenA/idr0125-screenA-annotation.csv  idr0125-screenA-annotation_bff.csv
"""

# Need to add "File Path" column with url like: https://cellpainting-gallery.s3.amazonaws.com/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/SQ00014812__2016-05-23T20_44_31-Measurement1.ome.zarr/A/1/0/

BASE_URL = "https://cellpainting-gallery.s3.amazonaws.com/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/"

# csv has columns: "Plate", "Well"

import csv
import sys


def main(input_csv, output_file):
    columns = None
    plate_col = 0
    well_col = 1
    with open(input_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        with open(output_file, 'w') as outfile:
            writer = csv.writer(outfile)
            for row in reader:
                if row[0].startswith("#"):
                    continue
                if columns is None:
                    columns = row
                    plate_col = columns.index("Plate")
                    well_col = columns.index("Well")
                    # Add "File Path" column at the beginning
                    columns = ["File Path"] + columns
                    writer.writerow(columns)
                    continue
                plate = row[plate_col]
                well = row[well_col]
                print("Plate:", plate, "Well:", well)
                file_path = f"{BASE_URL}{plate}.ome.zarr/{well[0]}/{well[1:]}/0/"
                row = [file_path] + row
                writer.writerow(row)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python csv_to_biofilefinder.py <input_csv> <output_file>")
        sys.exit(1)
    input_csv = sys.argv[1]
    output_file = sys.argv[2]
    main(input_csv, output_file)
    print(f"Output written to {output_file}")
