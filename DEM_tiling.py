import os
import subprocess
from qgis.core import QgsRasterLayer, QgsVectorLayer, QgsRectangle, QgsGeometry, QgsProcessingFeedback
import processing

# ------------------------------
# USER INPUTS — EDIT THESE
# ------------------------------
input_dem = r"G:\VIKASH\DEMs\DEM_tomaketiles.tif"
boundary_path = r"G:\VIKASH\QGIS_work\Dataset_26Aug\SORTING_TRIAL\City_boundary_pytest.shp"
output_dir = r"G:\VIKASH\Anc-Aux\DEM_tiles_final"
tile_size = 512  # pixels per tile

os.makedirs(output_dir, exist_ok=True)
feedback = QgsProcessingFeedback()

# ------------------------------
# LOAD DEM
# ------------------------------
raster = QgsRasterLayer(input_dem, "DEM")
if not raster.isValid():
    raise Exception("❌ DEM could not be loaded")

provider = raster.dataProvider()
ext = raster.extent()
width = provider.xSize()
height = provider.ySize()
px_w = raster.rasterUnitsPerPixelX()
px_h = raster.rasterUnitsPerPixelY()

print(f"✅ Raster loaded")
print(f"Raster size: {width}x{height}")
print(f"Pixel size: {px_w} x {px_h}")
print(f"Extent: {ext.xMinimum()}, {ext.yMinimum()} : {ext.xMaximum()}, {ext.yMaximum()}")

# ------------------------------
# LOAD & REPROJECT BOUNDARY
# ------------------------------
boundary = QgsVectorLayer(boundary_path, "boundary", "ogr")
if not boundary.isValid():
    raise Exception("❌ Boundary shapefile could not be loaded")

if boundary.crs() != raster.crs():
    print("♻️ Reprojecting boundary to match raster CRS...")
    boundary = processing.run(
        "native:reprojectlayer",
        {"INPUT": boundary, "TARGET_CRS": raster.crs(), "OUTPUT": "memory:"},
        feedback=feedback
    )["OUTPUT"]

# Merge all boundary geometries
geom_union = None
for f in boundary.getFeatures():
    g = f.geometry()
    geom_union = g if geom_union is None else geom_union.combine(g)

print("✅ Boundary ready")

# ------------------------------
# GENERATE TILES & CLIP USING GDAL
# ------------------------------
tile_count = 0
saved_count = 0

for i in range(0, width - tile_size, tile_size):
    for j in range(0, height - tile_size, tile_size):

        # ✅ Correct EPSG:4326 y_min / y_max
        x_min = ext.xMinimum() + i * px_w
        x_max = ext.xMinimum() + (i + tile_size) * px_w
        y_max = ext.yMaximum() - j * px_h
        y_min = ext.yMaximum() - (j + tile_size) * px_h

        rect = QgsRectangle(x_min, y_min, x_max, y_max)
        tile_geom = QgsGeometry.fromRect(rect)

        # Process only tiles that intersect the boundary
        if geom_union and not geom_union.intersects(tile_geom):
            continue

        out_name = f"tile_{i}_{j}.tif"
        out_path = os.path.abspath(os.path.join(output_dir, out_name))

        print(f"🧩 Tile {tile_count} → {out_name}")
        tile_count += 1

        # GDAL command (forces writing to disk)
        cmd = [
            "gdal_translate",
            "-of", "GTiff",
            "-projwin", str(x_min), str(y_max), str(x_max), str(y_min),
            input_dem,
            out_path
        ]

        try:
            subprocess.run(cmd, check=True, shell=True)
            if os.path.exists(out_path):
                print(f"✅ Saved: {out_path}")
                saved_count += 1
            else:
                print(f"⚠️ GDAL ran but file missing: {out_path}")
        except Exception as e:
            print(f"❌ GDAL error on {out_name}: {e}")

print(f"🎯 Finished! {saved_count} / {tile_count} tiles saved in: {output_dir}")
