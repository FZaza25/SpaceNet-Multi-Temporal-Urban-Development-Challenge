import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

# Percorsi ai file GeoJSON
labels_paths = [
    'labels_global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13_Buildings.geojson',
    'labels_match_global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13_Buildings.geojson',
    'labels_match_px_global_monthly_2017_07_mosaic_L15-1615E-1205N_6460_3370_13_Buildings.geojson'
]

# Funzione per caricare e visualizzare i file GeoJSON
def load_and_plot_labels(paths):
    fig, axs = plt.subplots(1, len(paths), figsize=(15, 5))
    for i, path in enumerate(paths):
        try:
            labels = gpd.read_file(path)
            if labels.is_empty.any() or not np.isfinite(labels.total_bounds).all():
                print(f'File {path} contiene dati non validi.')
                continue
            # Stampa informazioni per il debug
            print(f'File {path} bounds: {labels.total_bounds}')
            print(f'File {path} CRS: {labels.crs}')
            # Converti al CRS comune EPSG:4326
            if labels.crs != 'EPSG:4326':
                labels = labels.to_crs('EPSG:4326')
            # Verifica che le coordinate siano finite e positive
            bounds = labels.geometry.bounds
            if bounds.isnull().values.any() or (bounds.min().min() < -1e10) or (bounds.max().max() > 1e10):
                print(f'File {path} contiene coordinate non finite.')
                continue
            # Visualizza le etichette
            labels.plot(ax=axs[i], color='blue', edgecolor='black')
            axs[i].set_title(f'Labels {i+1}')
            axs[i].set_aspect('auto')  # Imposta l'aspetto manualmente
        except Exception as e:
            print(f'Errore durante il caricamento del file {path}: {e}')
    plt.tight_layout()
    plt.show()

load_and_plot_labels(labels_paths)

