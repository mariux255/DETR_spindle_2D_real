import torch
from scipy.signal import butter, sosfilt, sosfreqz
import scipy.io
import random
from torch.utils.data import Dataset, DataLoader
import os
import numpy as np
import matplotlib.image as mpimg
from torchvision.io import read_image
import json
import cv2


class dreams_dataset(Dataset):
    def __init__(self, input_path = '/home/marius/Documents/THESIS/data/MASS_MODA_processed/real/', label_path = '/home/marius/Documents/THESIS/data/MASS_MODA_processed/labels/'):
        self.input_path = input_path
        self.label_path = label_path
        self.input_dict = {}
        self.label_dict = {}
        for root, dirs, files in os.walk(self.input_path):
            for name in files:
                if name.endswith('npy'):
                    self.input_dict[int(name[:-4])] = os.path.join(root, name)

        for root, dirs, files in os.walk(self.label_path):
            for name in files:
                if name.endswith('json'):
                    self.label_dict[int(name[:-5])] = os.path.join(root, name)
    
                


    def __len__(self):
        return len(self.input_dict)

    def __getitem__(self, idx):
        print(self.input_dict[idx])
        fourier_array = np.load(self.input_dict[idx])
        fourier_array = torch.tensor(fourier_array)
        fourier_array = fourier_array[None, :, :]
        print('dataloader shape')
        print(fourier_array.shape)

        #image = np.array(cv2.imread(self.input_dict[idx]))
        #image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        #image = read_image(self.input_dict[idx])
        f = open(self.label_dict[idx])
        
        labels = (json.load(f))
        f.close()
        
        labels['boxes'] = torch.tensor(labels['boxes'])
        labels['labels'] = torch.tensor(labels['labels'], dtype=torch.int64)


        #image = torch.tensor(image)
        #image = image.view(3,image.shape[1],image.shape[0])
       
        return fourier_array, labels