import os
folder = r"G:\VIKASH\QGIS_work\All_year_dataset\Unsorted_year_wise\2012_Mask_tiles" 
prefix = "Mask_"                                   # base name (note underscore for clarity)
start = 159                                        # starting number (e.g., 1 → Image_001)


files = sorted(os.listdir(folder))  # get all files sorted

for i, filename in enumerate(files, start=start):
    old_path = os.path.join(folder, filename)
    
    # Skip if it's a folder
    if not os.path.isfile(old_path):
        continue
    
    # Get original file extension (like .tif, .jpg, etc.)
    ext = os.path.splitext(filename)[1]
    
    # New name with zero-padding (3 digits)
    new_name = f"{prefix}{i:03}{ext}"   # e.g., Image_001.tif
    new_path = os.path.join(folder, new_name)
    
    os.rename(old_path, new_path)
    print(f"Renamed: {filename} -> {new_name}")

