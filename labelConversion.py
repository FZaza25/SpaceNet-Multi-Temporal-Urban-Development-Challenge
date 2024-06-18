import geopandas as gpd
import rasterio
import numpy as np
from rasterio.features import rasterize

# Caricamento delle etichette GeoJSON
labels = gpd.read_file('labels_match_px_global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13_Buildings.geojson')

# Caricamento dell'immagine satellitare
with rasterio.open('global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13.tif') as src:
    img = src.read([1, 2, 3])  # Ignora il quarto canale
    transform = src.transform
    img_shape = src.shape

# Creazione della maschera binaria
def create_mask(geojson, img_shape, transform):
    shapes = [(geom, 1) for geom in geojson.geometry]
    mask = rasterize(shapes=shapes, out_shape=img_shape, transform=transform, fill=0, dtype=np.uint8)
    return mask

mask = create_mask(labels, img_shape, transform)

# Salvataggio della maschera nella cartella corrente
with rasterio.open('output_mask.tif', 'w', driver='GTiff', height=mask.shape[0], width=mask.shape[1], count=1, dtype=np.uint8) as dst:
    dst.write(mask, 1)

