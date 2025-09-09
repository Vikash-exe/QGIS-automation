
import os
import processing
from qgis import processing

# Input and output paths
input_raster = "G:\VIKASH\QGIS_work\Bnag_sentinal\Clip_FCC_Senti.tif"
output_raster = "G:\VIKASH\QGIS_work\Bnag_sentinal\Clip_FCC_Senti_resampled.tif"

# Run gdal:warpreproject
processing.run("gdal:warpreproject", {
    'INPUT': input_raster,
    'SOURCE_CRS': None,   # keeps original CRS
    'TARGET_CRS': None,   # same as input
    'RESAMPLING': 3,      # 0=Nearest, 1=Bilinear, 2=Cubic, 3=Cubic Spline, etc.
    'NODATA': None,
    'TARGET_RESOLUTION': 5.8,   # set both X and Y resolution
    'OUTPUT': output_raster
})

print("✅ Resampled raster saved at:", output_raster)
