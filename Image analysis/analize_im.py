import matplotlib.pyplot as plt
import rasterio

file_path = 'sample2.tif'
with rasterio.open(file_path) as source:
   dataset=source.read()
   
print(dataset.shape)
print(dataset.dtype)

fig, axes = plt.subplots(1, 4, figsize=(20, 5))
for i in range(dataset.shape[0]):
    band = dataset[i]
    band_min = band.min()
    band_max = band.max()
    band_mean = band.mean()
    band_std = band.std()
    
    axes[i].imshow(band, cmap='gray')
    axes[i].set_title(f'Banda {i}\nMin: {band_min}\nMax: {band_max}\nMean: {band_mean:.2f}')
    axes[i].axis('off')


plt.show()




# This simple script converts images to grayscale and analyzes the channels
# in this case 4 with rasterio. With matplotlib, we visualize the bands.
