# SpaceNet-Multi-Temporal-Urban-Development-Challenge
In this project, I tackle the following challenge: https://spacenet.ai/sn7-challenge/ by analyzing the dataset and developing a binary convolutional neural network for segmentation.
I implemented a UNET convolutional neural network for binary segmentation of buildings.

Dataset download:
<aws s3 cp s3://spacenet-dataset/spacenet/SN7_buildings>

Regarding the dataset, I worked exclusively on the material in the "train" folder, splitting the elements into training, test, and validation sets (70%-15%-15%). I recommend splitting each area into validation/test/train sets separately to avoid mixing, as each subfolder in "train" contains 12 images and their respective labels from the same area in different months. In the training, test, and validation directories, I created three folders: images_maked, labels/labels_match, and mask_from_label.

Mask_from_label is the output folder for processing the geojson labels, which in the project I convert into binary masks in TIFF format necessary for model training. In the other folders (images_maked, labels/labels_match) of train, validation, and test, I included all the corresponding images and labels_match from the train dataset in the indicated proportions.
