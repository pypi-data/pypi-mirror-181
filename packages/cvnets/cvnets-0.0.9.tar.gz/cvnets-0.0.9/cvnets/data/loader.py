import PIL
import random
import torchvision.transforms as T
from torchvision import datasets
from torch.utils.data import DataLoader, SubsetRandomSampler


crop = 28
mean_std = (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)
train_tr = T.Compose(
        [
            T.Grayscale(3),
            T.RandomResizedCrop(
                crop, scale=(0.2, 1.0), interpolation=PIL.Image.BICUBIC
            ),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize(*mean_std),
        ]
    )

def data_loader(dataname, batch_size, train=False, sampling=None):
    if dataname == "FashionMNIST":
        # Download training data from open datasets.
        data = datasets.FashionMNIST(
            root="data",
            train=train,
            download=True,
            # transform=T.ToTensor(),
            transform=train_tr,
        )
    if sampling is not None:
        print("sampling")
        sampler = SubsetRandomSampler(random.sample(list(range(len(data))), int(len(data)*sampling)))
    else:
        sampler = None
    return DataLoader(data, batch_size=batch_size, sampler=sampler)

def get_data(dataname, batch_size=1, train=False, sampling=None):
    if dataname == "FashionMNIST":
        # Download training data from open datasets.
        data = datasets.FashionMNIST(
            root="data",
            train=train,
            download=True,
            # transform=T.ToTensor(),
            transform=train_tr,
        )
    if sampling is not None:
        print("sampling")
        sampler = SubsetRandomSampler(random.sample(list(range(len(data))), int(len(data)*sampling)))
    else:
        sampler = None
    return DataLoader(data, batch_size=batch_size, sampler=sampler)