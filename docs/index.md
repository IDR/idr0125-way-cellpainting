# idr0125-way-cellpainting

This IDR submission is is being processed and not yet available for viewing in IDR.

However the data can be accessed at the Cell Painting Gallery on the [Registry of Open Data on AWS](https://registry.opendata.aws/cellpainting-gallery/) under accession number cpg0004

Individual wells can be visualized using vizarr e.g., [https://hms-dbmi.github.io/vizarr/?source=https://cellpainting-gallery.s3.amazonaws.com/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/SQ00014812__2016-05-23T20_44_31-Measurement1.ome.zarr/P/24/](https://hms-dbmi.github.io/vizarr/?source=https://cellpainting-gallery.s3.amazonaws.com/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr/SQ00014812__2016-05-23T20_44_31-Measurement1.ome.zarr/P/24/)

To list Wells for a Plate, you can open a Plate in `ome-ngff-validator` (see links below). Open Wells in a new page by clicking on the Well in the plate grid.
From each Well you can follow the `V` icon to open the Well in vizarr.

# Plates

{% for plate in site.data.plates %}
  <li>
    <a href="https://ome.github.io/ome-ngff-validator/?source=https://cellpainting-gallery.s3.amazonaws.com/cpg0004-lincs/broad/images/2016_04_01_a549_48hr_batch1/images_zarr{% if plate in site.data.plates_20221101 %}_050{% endif %}/{{ plate }}">
      {{ plate }}
    </a>
  </li>
{% endfor %}