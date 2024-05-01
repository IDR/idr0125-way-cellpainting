
import csv
import sys
from omero.cli import cli_login
from omero.gateway import BlitzGateway
from omero.sys import ParametersI
from omero.rtypes import rstring


def get_zarr_name_from_fileset(conn, fileset_id):

    query_service = conn.getQueryService()
    params = ParametersI()
    params.addId(fileset_id)
    params.add("zarr", rstring("%%%s" % "zarr/.zattrs"))
    query = """ select u.clientPath, fs.templatePrefix from Fileset fs
        join fs.usedFiles u
        where fs.id=:id
        and u.clientPath like :zarr"""

    result = query_service.projection(query, params, conn.SERVICE_OPTS)
    if len(result) == 0:
        return None

    client_path = result[0][0].val
    prefix = result[0][1].val

    zarr_name = client_path.split(".zarr")[0] + ".zarr"
    zarr_name = zarr_name.split("/")[-1]

    print(zarr_name, prefix)
    return zarr_name, prefix


def lookup_filesets(conn, name):

    filesets = []
    screen = conn.getObject("Screen", attributes={'name': name})
    for plate in screen.listChildren():
        image = None
        for well in plate.listChildren():
            ws = list(well.listChildren())
            if len(ws) > 0:
                image = list(well.listChildren())[0].getImage()
                if image is not None:
                    break
        # don't .getFileset() as it loads all Files and Images
        zarr_path, prefix = get_zarr_name_from_fileset(conn, image.fileset.id.val)
        filesets.append((image.fileset.id.val, zarr_path, prefix))

    return filesets


def main(argv):

    with cli_login() as cli:
        conn = BlitzGateway(client_obj=cli._client)
    
        filesets = lookup_filesets(conn, "idr0125-way-cellpainting/screenA")
        with open('idr0125_filesets.csv', 'a', newline='') as csvfile:
            fswriter = csv.writer(csvfile)
            for (fsid, zarr_name, prefix) in filesets:
                fswriter.writerow([fsid, zarr_name, prefix])

if __name__ == '__main__':
    main(sys.argv[1:])
