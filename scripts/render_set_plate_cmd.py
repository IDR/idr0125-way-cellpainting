
import requests

SERVER = "http://localhost:1080/"

# After creating symlinks to s3, we need to `omero render set Plate:ID` for each Plate
# Takes ~12 hours per plate, so run this in parallel

# Usage (locally):

# deploy webclient at SERVER address above (public)
# $ cd scripts
# $ python render_set_plate_cmd.py

# Copy the final printed command, ssh to pilot or idr server and...

# cd /uod/idr/idr0125-way-cellpainting
# screen -S idr0125_render_set_cmd
# source /opt/omero/server/venv3/bin/activate
# omero login
# paste the command from above

# Then Ctrl-A and Ctrl-D to detatch from Screen.
# Follow progress with:

# $ tail -f /tmp/renderImage.err

import math

screen_id = 3055
plates_url = SERVER + f"webclient/api/plates/?id={screen_id}"

plates_json = requests.get(plates_url).json()

plate_ids = [str(plate['id']) for plate in plates_json["plates"]]

THREADS = 4
batch_size = math.ceil(len(plate_ids) // THREADS)

# omero --debug=2 render set Plate:9940 screenA/idr0125-screenA-renderdef.yml > /tmp/renderPlate9940.log 2>/tmp/renderPlate9940.err
command = """omero --debug=2 render set Plate:$a screenA/idr0125-screenA-renderdef.yml"""

for t in range(4):
    start = t * batch_size
    end = (t + 1) * batch_size
    ids = plate_ids[start: end]

    print('\n')
    print('for a in %s; do %s > /tmp/renderPlateThread%s.log 2>/tmp/renderPlateThread%s.err; done' % (" ".join(ids), command, t, t))
