import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report # type: ignore

import rasterio
from rasterio.warp import reproject, Resampling

with rasterio.open(r"G:\VIKASH\QGIS_work\Accuracy_test\2018_true.tif",allow_pickle=True) as src_true:
    y_true = src_true.read(1)
    profile_true = src_true.profile

with rasterio.open(r"G:\VIKASH\QGIS_work\Accuracy_test\2025_clip_pred.tif",allow_pickle=True) as src_pred:
    y_pred = src_pred.read(1)
    profile_pred = src_pred.profile

# Reproject predicted raster to match ground truth grid
if profile_true["transform"] != profile_pred["transform"] or profile_true["crs"] != profile_pred["crs"]:
    y_pred_aligned = np.empty_like(y_true)
    reproject(
        source=y_pred,
        destination=y_pred_aligned,
        src_transform=profile_pred["transform"],
        src_crs=profile_pred["crs"],
        dst_transform=profile_true["transform"],
        dst_crs=profile_true["crs"],
        resampling=Resampling.nearest
    )
    y_pred = y_pred_aligned


# Flatten them (remove 2D shape)
y_true_flat = y_true.flatten()
y_pred_flat = y_pred.flatten()

acc = accuracy_score(y_true_flat, y_pred_flat)
print("Overall Accuracy:", round(acc * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_true_flat, y_pred_flat, target_names=["other","Urban", "Vegetation", "Water", "Barren"]))
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay # type: ignore

cm = confusion_matrix(y_true_flat, y_pred_flat)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["other","Urban", "Vegetation", "Water", "Barren"])
disp.plot(cmap="Blues", values_format="d")
plt.title("Confusion Matrix")
plt.show()

