'''
    PyTorch dataset class for COCO-CT-formatted datasets. Note that you could
    use the official PyTorch MS-COCO wrappers:
    https://pytorch.org/vision/master/generated/torchvision.datasets.CocoDetection.html

    We just hack our way through the COCO JSON files here for demonstration
    purposes.

    See also the MS-COCO format on the official Web page:
    https://cocodataset.org/#format-data

    2022 Benjamin Kellenberger
'''

import os
import json
from torch.utils.data import Dataset
from torchvision.transforms import Compose, Resize, ToTensor
from PIL import Image
import csv
from torchvision.transforms import transforms
from torchvision import transforms, datasets



class CTDataset(Dataset):

    def __init__(self, cfg, split, transform):
        '''
            Constructor. Here, we collect and index the dataset inputs and
            labels.
        '''
        if split == 'unlabeled':
            print ('################################# this will not work unless you change the getitem function in models/my_custom_dataset.py to have no labels for val set############') 
        self.data_root = cfg['data_root']
        self.split = split
        self.transform = transform
        # self.transform = Compose([              # Transforms. Here's where we could add data augmentation (see Björn's lecture on August 11).
        #     Resize((cfg['image_size'])),        # For now, we just resize the images to the same dimensions...
        #     ToTensor()                          # ...and convert them to torch.Tensor.
        # ])
        
        # index data into list
        self.data = []

        self.label_mapping = {}
        global_mapping_idx = 0

        if split == 'train':
            f = open(cfg['train_label_file'], 'r')
            
        elif split=='val':
            f = open(cfg['val_label_file'], 'r')
        elif split=='test':
            f = open(cfg['test_label_file'], 'r')
        elif split=='unlabeled':
            f = open(cfg['unlabeled_file'],'r')
        
        csv_reader = csv.reader(f, delimiter=',')
        
        #if split == 'unlabeled':
        if split == 'unlabeled' or split == 'val':
            for row in csv_reader:
                self.data.append(row[0])
        else:
            for row in csv_reader:
                self.data.append([row[0], int(row[1])])

    def __len__(self):
        '''
            Returns the length of the dataset.
        '''
        return len(self.data)

    
    def __getitem__(self, idx):
        '''
            Returns a single data point at given idx.
            Here's where we actually load the image.
        '''
        if self.split == 'unlabeled' or self.split=='val':
                image_name = self.data[idx]              # see line 57 above where we added these two items to the self.data list

                # load image
                image_path = os.path.join(self.data_root, image_name)
                img = Image.open(image_path).convert('RGB')     # the ".convert" makes sure we always get three bands in Red, Green, Blue order

                # transform: see lines 31ff above where we define our transformations
                img_tensor = self.transform(img)

                return img_tensor
        else: 
            image_name,label = self.data[idx][0], self.data[idx][1]              # see line 57 above where we added these two items to the self.data list

            # load image
            image_path = os.path.join(self.data_root, image_name)
            img = Image.open(image_path).convert('RGB')     # the ".convert" makes sure we always get three bands in Red, Green, Blue order

            # transform: see lines 31ff above where we define our transformations
            img_tensor = self.transform(img)

            return img_tensor,label