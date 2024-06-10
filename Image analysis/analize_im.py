import matplotlib.pyplot as plt
import rasterio

file_path = 'sample.tif'
dataset = rasterio.open(file_path)

fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for i in range(1, dataset.count + 1):
    band = dataset.read(i)
    band_min = band.min()
    band_max = band.max()
    band_mean = band.mean()
    band_std = band.std()
    
    axes[i - 1].imshow(band, cmap='gray')
    axes[i - 1].set_title(f'Banda {i}\nMin: {band_min}\nMax: {band_max}\nMean: {band_mean:.2f}')
    axes[i - 1].axis('off')


plt.show()




# This simple script converts images to grayscale and analyzes the channels
# in this case 4 with rasterio. With matplotlib, we visualize the bands.
