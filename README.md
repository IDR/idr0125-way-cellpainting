# idr0125-way-cellpainting
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IDR/idr0125-way-cellpainting/main?urlpath=notebooks%2Fnotebooks%2Fanalyse.ipynb)
[![Actions Status](https://github.com/IDR/idr0125-way-cellpainting/workflows/repo2docker/badge.svg)](https://github.com/IDR/idr0125-way-cellpainting/actions)

Data hosted on cellpainting-gallery `s3` can be browsed at https://idr.github.io/idr0125-way-cellpainting/.


# Import workflow

 - Use `scripts/s3_sync.py` to generate `aws s3 sync` commands to download all OME-NGFF plates as metadata ONLY (no zarr chunks)

 - Import of metadata-only NGFF plates requires ZarrReader with `--depth=100`:

    $ omero import --depth=100 --bulk screenA/idr0125-screenA-bulk.yml --file /tmp/idr0125.log  --errs /tmp/idr0125.err

 - Need to view an image from each plate OR `omero render set Image:ID rdef.yml` for each plate, to avoid subsequent ResourceError after symlinking. See `scripts/render_set_cmd.py`

 - Run `scripts/get_import_paths.py` to create `imported_paths.txt` with the managed repo path for each imported plate.

 - Run `scripts/symlink_cmd.py` which consumes `imported_paths.txt` to output the commands to replace each plate in the managed repo with a symlink to the corresponding plate on a mounted s3 bucket. These can be saved in `scripts/symlinks.bash`. Need to run `sudo chmod +x symlinks.bash` then `sudo -u omero-server -s` and `bash symlinks.bash`.

 - Run `omero render set Plate:ID` for every plate. NB: takes ~12hrs per plate? TBD: split this job between several parallel processes.
