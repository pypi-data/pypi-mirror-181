
from albumentations.pytorch import ToTensorV2
import torch
import albumentations as A
from doppio.doppio_dataset_stream import DoppioDataset, collate
# conver check 용 정식버전 아님. 


def doppio(dataset=None, split_dir=None, task_info=None, augmentation = None, valid_classes = None,  data_root_path=None, num_workers=0, batch_size=2, shuffle=False):


    if data_root_path == None:
        packge_path = torch.__path__
        packge_path = list(packge_path)
        packge_path = packge_path[0].replace('torch', 'doppio')
        data_root_path = packge_path

    if augmentation == None:
        augmentation =  [A.Resize(width=1000, height=1000), ToTensorV2(transpose_mask=True)]


    custom_dataset = DoppioDataset(dataset=dataset, split_dir=split_dir, task_info=task_info, augmentation=augmentation, valid_classes=valid_classes, data_root_path=data_root_path)# [A.Resize(width=512, height=512),ToTensorV2(transpose_mask=True)])
    my_dataset_loader = torch.utils.data.DataLoader(dataset=custom_dataset,
                                                    batch_size=batch_size,
                                                    shuffle=shuffle,  num_workers=num_workers, collate_fn=collate)

    return my_dataset_loader
