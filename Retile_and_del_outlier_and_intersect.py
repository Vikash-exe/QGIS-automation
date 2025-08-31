import os
from osgeo import gdal, ogr

# --- USER INPUTS ---
input_raster = r"G:\VIKASH\QGIS_work\Pycode\2018_FCC_01.tif"
boundary = r"G:\VIKASH\QGIS_work\Dataset_26Aug\SORTING_TRIAL\City_boundary_pytest.shp"
output_dir = r"G:\VIKASH\QGIS_work\Dataset_26Aug\2018_FCC_tiles"
tile_size = 512  # pixels

os.makedirs(output_dir, exist_ok=True)

# --- Load boundary ---
driver = ogr.GetDriverByName("ESRI Shapefile")
ds = driver.Open(boundary, 0)
layer = ds.GetLayer()
boundary_geom = None
for feat in layer:
    g = feat.GetGeometryRef()
    if boundary_geom is None:
        boundary_geom = g.Clone()
    else:
        boundary_geom = boundary_geom.Union(g)

# --- Load raster ---
r_ds = gdal.Open(input_raster)
gt = r_ds.GetGeoTransform()
x_origin, y_origin = gt[0], gt[3]
px_w, px_h = gt[1], gt[5]

r_xsize, r_ysize = r_ds.RasterXSize, r_ds.RasterYSize

# --- Generate tile grid ---
for i in range(0, r_xsize, tile_size):
    for j in range(0, r_ysize, tile_size):
        x_min = x_origin + i * px_w
        x_max = x_origin + (i + tile_size) * px_w
        y_max = y_origin + j * px_h
        y_min = y_origin + (j + tile_size) * px_h

        # Make tile polygon
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(x_min, y_min)
        ring.AddPoint(x_min, y_max)
        ring.AddPoint(x_max, y_max)
        ring.AddPoint(x_max, y_min)
        ring.AddPoint(x_min, y_min)
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        # --- Only keep FULLY inside boundary ---
        if boundary_geom.Contains(poly):
            out_name = f"tile_{i}_{j}.tif"
            out_path = os.path.join(output_dir, out_name)

            gdal.Translate(
                out_path,
                r_ds,
                srcWin=[i, j, tile_size, tile_size]
            )
            print(f"Saved {out_name}")
