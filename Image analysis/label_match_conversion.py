import geopandas as gpd
import rasterio
import numpy as np
from rasterio.features import rasterize
import matplotlib.pyplot as plt

# Carica il file GeoJSON contenente le etichette (poligoni) che rappresentano gli edifici
labels_path = 'match_global_monthly_2018_02_mosaic_L15-0924E-1108N_3699_3757_13_Buildings.geojson'
labels = gpd.read_file(labels_path)

# Carica l'immagine satellitare in formato TIFF
tif_image_path = 'global_monthly_2018_02_mosaic_L15-0924E-1108N_3699_3757_13.tif'
with rasterio.open(tif_image_path) as src:
    # Legge i primi tre canali dell'immagine (ignorando il quarto canale se presente)
    img = src.read([1, 2, 3])
    # Ottiene la trasformazione affine dell'immagine, che mappa le coordinate pixel alle coordinate spaziali
    transform = src.transform
    # Salva le dimensioni dell'immagine (altezza e larghezza)
    img_shape = (src.height, src.width)
    # Salva il sistema di riferimento delle coordinate (CRS) dell'immagine
    img_crs = src.crs

# Stampa i bounds (limiti spaziali) delle geometrie e dell'immagine per verificare che le coordinate siano allineate
print(f'Bounds delle geometrie: {labels.total_bounds}')
print(f'Bounds dell\'immagine: {src.bounds}')
print(f'CRS dell\'immagine: {img_crs}')

# Converte le geometrie dal loro CRS originale al CRS dell'immagine satellitare
labels = labels.to_crs(img_crs)

# Definisce una funzione per creare una maschera binaria
def create_mask(geojson, img_shape, transform):
    # Prepara le geometrie e i valori di riempimento per la rasterizzazione
    shapes = [(geom, 1) for geom in geojson.geometry]
    # Rasterizza le geometrie vettoriali in una griglia raster, riempiendo con 1 dove le geometrie sono presenti e 0 altrove
    mask = rasterize(shapes=shapes, out_shape=img_shape, transform=transform, fill=0, dtype=np.uint8)
    return mask

# Crea la maschera binaria chiamando la funzione create_mask
mask = create_mask(labels, img_shape, transform)

# Normalizza i valori della maschera per visualizzarli correttamente
mask_normalized = (mask * 255).astype(np.uint8)

# Salva la maschera binaria creata in un nuovo file TIFF
output_mask_path = 'output_mask.tif'
with rasterio.open(
    output_mask_path,
    'w',
    driver='GTiff',
    height=mask_normalized.shape[0],
    width=mask_normalized.shape[1],
    count=1,
    dtype=mask_normalized.dtype,
    crs=img_crs,
    transform=transform,
) as dst:
    # Scrive la maschera binaria nel file
    dst.write(mask_normalized, 1)

# Verifica il contenuto del file salvato
with rasterio.open(output_mask_path) as src:
    saved_mask = src.read(1)
    plt.figure(figsize=(10, 10))
    plt.imshow(saved_mask, cmap='gray')
    plt.title('Binary Mask')
    plt.show()

