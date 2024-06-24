import geopandas as gpd
import rasterio
import numpy as np
from rasterio.features import rasterize
import matplotlib.pyplot as plt

# Carica i file GeoJSON contenenti le etichette
labels_path = 'labels_global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13_Buildings.geojson'
labels_match_path = 'labels_match_global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13_Buildings.geojson'
labels_match_px_path = 'labels_match_px_global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13_Buildings.geojson'

labels = gpd.read_file(labels_path)
labels_match = gpd.read_file(labels_match_path)
labels_match_px = gpd.read_file(labels_match_px_path)

# Stampa il CRS di ciascuna label, per match_px non abbiamo un CRS geografico, in quanto sono
# coordinate in unità pixel
print(f'CRS di labels: {labels.crs}')
print(f'CRS di labels_match: {labels_match.crs}')


# Carica l'immagine satellitare in formato TIFF
tif_image_path = 'global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13.tif'

with rasterio.open(tif_image_path) as src:
    img = src.read([1, 2, 3])
    transform = src.transform
    img_shape = (src.height, src.width)
    img_crs = src.crs

# Stampa i bounds (limiti spaziali) delle geometrie e dell'immagine per verificare che le coordinate siano allineate
print(f'Bounds delle geometrie (labels): {labels.total_bounds}')
print(f'Bounds delle geometrie (labels_match): {labels_match.total_bounds}')
print(f'Bounds delle geometrie (labels_match_px): {labels_match_px.total_bounds}')
print(f'Bounds dell\'immagine: {src.bounds}')
print(f'CRS dell\'immagine: {img_crs}')


labels = labels.to_crs(img_crs)
labels_match = labels.to_crs(img_crs)


labels_match_px.crs = None


def filter_invalid_geometries(geojson):
    return geojson[geojson.is_valid & ~geojson.is_empty]


labels = filter_invalid_geometries(labels)
labels_match = filter_invalid_geometries(labels_match)
labels_match_px = filter_invalid_geometries(labels_match_px)


def create_mask(geojson, img_shape, transform):
    shapes = [(geom, 1) for geom in geojson.geometry]
    mask = rasterize(shapes=shapes, out_shape=img_shape, transform=transform, fill=0, dtype=np.uint8)
    return mask

def create_mask_from_pixels(geojson, img_shape):
    shapes = [(geom, 1) for geom in geojson.geometry]
    mask = rasterize(shapes=shapes, out_shape=img_shape, fill=0, dtype=np.uint8)
    return mask


mask_labels = create_mask(labels, img_shape, transform)
mask_labels_match = create_mask(labels_match, img_shape, transform)
mask_labels_match_px = create_mask_from_pixels(labels_match_px, img_shape)


def save_normalized_mask(mask, output_path, crs, transform):
    mask_normalized = (mask * 255).astype(np.uint8)
    with rasterio.open(
        output_path,
        'w',
        driver='GTiff',
        height=mask_normalized.shape[0],
        width=mask_normalized.shape[1],
        count=1,
        dtype=mask_normalized.dtype,
        crs=crs,
        transform=transform,
    ) as dst:
        dst.write(mask_normalized, 1)


save_normalized_mask(mask_labels, 'output_mask_labels.tif', img_crs, transform)
save_normalized_mask(mask_labels_match, 'output_mask_labels_match.tif', img_crs, transform)

save_normalized_mask(mask_labels_match_px, 'output_mask_labels_match_px.tif', None, transform)


fig, axes = plt.subplots(1, 3, figsize=(18, 6))
axes[0].imshow(mask_labels, cmap='cividis')
axes[0].set_title('Mask from Labels')
axes[1].imshow(mask_labels_match, cmap='gray')
axes[1].set_title('Mask from Labels Match')
axes[2].imshow(mask_labels_match_px, cmap='Spectral')
axes[2].set_title('Mask from Labels Match_px')

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.show()
