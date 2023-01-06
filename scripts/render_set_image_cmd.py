
import requests

SERVER = "http://localhost:1080/"

# After importing plates, we need to `omero render set Image:ID` for an Image in each Plate

# Usage (locally):

# deploy webclient at SERVER address above (public)
# $ cd scripts
# $ python render_set_image_cmd.py

# Copy the final printed command, ssh to pilot or idr server and...

# cd /uod/idr/idr0125-way-cellpainting
# screen -S idr0125_render_set_cmd
# source /opt/omero/server/venv3/bin/activate
# omero login
# paste the command from above

# Then Ctrl-A and Ctrl-D to detatch from Screen.
# Follow progress with:

# $ tail -f /tmp/renderImage.err

screen_id = 3055
plates_url = SERVER + f"webclient/api/plates/?id={screen_id}"

plates_json = requests.get(plates_url).json()

image_ids = []

for plate in plates_json["plates"]:

    wells_url = SERVER + f"webgateway/plate/{plate['id']}/0/"
    wells_json = requests.get(wells_url).json()
    first_img_id = wells_json["grid"][0][0]['id']
    print("Image:", first_img_id)
    image_ids.append(str(first_img_id))

# omero --debug=2 render set Image:9940 screenA/idr0125-screenA-renderdef.yml > /tmp/renderPlate9940.log 2>/tmp/renderPlate9940.err
command = """omero --debug=2 render set Image:$a screenA/idr0125-screenA-renderdef.yml > /tmp/renderImage.log 2>/tmp/renderImage.err"""

image_ids = " ".join(image_ids)

print('for a in %s; do %s; done' % (image_ids, command))
