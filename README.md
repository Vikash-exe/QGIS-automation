# QGIS-automation
This repo contains different workflow automation for easy and structured process of dataset development from QGIS
  1. Gridding and splitting the tiles out of large maps can be time consuming. Using these codes can turn hours to secs.
  2. Retile_and_del_outliner takes map, boundary and retiling size in pixels. It deletes the tiles intersecting with boundary for a clean square tile for model training.
  3. Data_sorting keeps the indexing in control.
  4. Accuracy_test is for checking ground truth points to predicted points accuracy in LULC prediction
