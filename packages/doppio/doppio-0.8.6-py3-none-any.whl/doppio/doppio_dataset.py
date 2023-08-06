import json
import cv2
import albumentations as A
from torch.utils.data.dataset import Dataset
import torch
from glob import glob
import numpy as np
from collections import OrderedDict
import urllib.request
import os
import zipfile 
import progressbar
from tqdm import tqdm

pbar = None


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None



class DoppioDataset(Dataset):

    def __init__(self, dataset=None, split_dir=None, task_info=None, augmentation=None, valid_classes=None, data_root_path=None, download=True):

        transforms_kwargs_params = {}
        self.transforms_kwargs_input = dict()

        if "segmentation_mask" in list(task_info.values())[0]:
            self.semantic_mask_flag = 1
        else:
            self.semantic_mask_flag = 0

        self.data_count = 0

        # check json file
        # from server call
        # check_json_files = check_json_from_server(dataset=dataset, split_dir=split_dir, task_info=task_info, valid_classes=valid_classes, semantic_mask_flag=semantic_mask_flag)
        data_dict = dict()
        data_dict['dataset'] = dataset
        data_dict['split_dir'] = split_dir
        data_dict['task_info'] = task_info
        data_dict['valid_classes'] = valid_classes
        data_dict['semantic_mask_flag'] = self.semantic_mask_flag

        # local path 지정해줘야 한다. 
        print("지금은 local Test 지만 이 파트를 사용자의 폴더로 지정을 해줘야 한다. !!!!! ~~")
        self.local_json_path =  os.path.join(data_root_path, dataset, split_dir, "doppio_labels", "{}_labels".format(list(task_info.keys())[0]))
        self.local_image_path = os.path.join(data_root_path, dataset, split_dir, "images")
        self.local_mask_path =  os.path.join(data_root_path, dataset, split_dir, "doppio_labels", "{}_labels".format(list(task_info.keys())[0]))
        self.file_path =  os.path.join(data_root_path, dataset, split_dir, "doppio_labels", "{}_labels".format(list(task_info.keys())[0]), "files.json")

         # folder 생성하는 코드
        # Download zip file
        # if os.path.isdir(self.local_json_path ) and os.path.isdir(self.local_image_path):
        #     self.local = True
        # else:
        #     self.local = False

        



        if download:
            zip_label_address =  "http://222.231.59.68/{}.zip".format(dataset)

            zip_path = os.path.join(data_root_path, dataset+'.zip')#urllib.request.urlretrieve(model_url, model_file, show_progress


            if not os.path.isfile(zip_path) :
                urllib.request.urlretrieve(zip_label_address, zip_path, show_progress)
                # zipfile.ZipFile(zip_path).extractall(data_root_path)
                with zipfile.ZipFile(zip_path) as zf:
                    for member in tqdm(zf.infolist(), desc='Extracting'):
                        try:
                            zf.extract(member, data_root_path)
                        except zipfile.error as e:
                            pass

           
        # check json files
        check_json_files =  self.check_json_from_local(file_path=self.file_path, label_path=self.local_json_path, valid_classes =valid_classes,  semantic_mask_flag=self.semantic_mask_flag)        
    

        self.json_files = check_json_files['label_files']
        self.url_image = check_json_files['image_files']
        self.url_mask = check_json_files['mask_files']

        info_path =  os.path.join(data_root_path, dataset, split_dir, "doppio_labels", "{}_labels".format(list(task_info.keys())[0]), "info.json")
        # ms_coco , val, object dtection

        with open(info_path, 'r') as f:
            self.info_json = json.load(f)
        
        # task 는 사용자가 요청하는거 
        self.task = list(task_info.values())[0]

        for item in self.task:
            if item == "bbox":
                transforms_kwargs_params['bbox_params'] = A.BboxParams(format="pascal_voc", label_fields=['class']) # ouput 할때 yolo 나 coco format 처럼 다른 스타일로 내보내게 자유도를 줘야함.
                self.transforms_kwargs_input['bboxes'] = None
            elif item == "segmentation":
                self.transforms_kwargs_input['masks'] = None
            elif item == "keypoint":
                transforms_kwargs_params['keypoint_params'] = A.KeypointParams(format="xy", label_fields=['keypoint_labels'])
                self.transforms_kwargs_input['keypoints'] = None
                self.transforms_kwargs_input['keypoint_visible'] = None
                self.transforms_kwargs_input['keypoint_labels'] = None
                self.keypoint_classes = [ i for i in range(len(self.info_json['keypoint_classes']))]
            elif item == "segmentation_mask":
                self.transforms_kwargs_input['mask'] = None

            elif item == "class":
                self.transforms_kwargs_input['class'] = None
        
        self.classes_total = dict(zip( self.info_json['classes'], range(len( self.info_json['classes']))))

        if "segmentation_mask" in self.task:

            if valid_classes != None: # 빼고 싶은 코드가 있을 경우
                self.info_json['classes'] =  dict(zip(valid_classes, range(len(valid_classes))))
                self.ori2valid_class_num = {}

                for t, t_valid_class in enumerate(valid_classes):
                    self.ori2valid_class_num[self.classes_total[t_valid_class]] = t
            else:
                    self.ori2valid_class_num = {}
                    for t, t_valid_class in enumerate(self.info_json['classes']):
                        self.ori2valid_class_num[self.classes_total[t_valid_class]] = t


        if valid_classes != None:
            self.info_json['classes'] = dict(zip(valid_classes, range(len(valid_classes))))

        
        self.transform = A.Compose(
            augmentation,
            **transforms_kwargs_params
            
        )
        # self.trans = trans
        self.transforms_kwargs_input['image'] = None


    def access_to_local(self, index):

        json_url_file = self.json_files[index]
        url_local_json_path = os.path.join(self.local_json_path, json_url_file)

    
        with open(url_local_json_path, 'r') as f:
            label_json_file = json.load(f)

        # image load
        img_name = label_json_file['image_name']
        im_path = os.path.join(self.local_image_path, img_name)
        img = cv2.imread(im_path)
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # mask mask load
        if "segmentation_mask" in self.task:
            mask_path = os.path.join(self.local_mask_path, label_json_file['annotation'][0]['segmentation_path'])
            mask = cv2.imread(mask_path)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

            return label_json_file, im_rgb, mask
        
        return label_json_file, im_rgb, None


    def __getitem__(self, index):
        
         
        label_json_file, im_rgb, mask = self.access_to_local(index)
        
          
        self.doppio_output = OrderedDict()
        self.doppio_output['area'] = []
        self.doppio_output['image'] = None
        
        for item in self.task:
            if item == "bbox":
                self.doppio_output["bbox"] = []
            elif item == "segmentation":
                self.doppio_output["segmentation"] = []
            elif item == "keypoint":
                self.doppio_output["keypoint"] = []
                self.doppio_output["keypoint_visible"] = []
                self.doppio_output["keypoint_labels"] = []
            elif item == "segmentation_mask":
                self.doppio_output["segmentation_path"] = []
            elif item == "class":
                self.doppio_output['class'] = []     

        
        flag = 0 
        for ann in label_json_file['annotation']:
            classes = ann['class']
            if classes in self.info_json['classes']:
                flag = 1
                break
    
        if flag == 0 and self.semantic_mask_flag == 0:
            return None

        json_file = label_json_file

        annotations = json_file['annotation']

        if "class" in self.doppio_output.keys():
            self.doppio_output.move_to_end('class', False)

        ann_keys = list(self.doppio_output.keys())


        for ann in annotations: # ex) 이미지의 박스 여러개 일때 
            for ann_key in ann_keys:
                if ann_key in ann.keys():
                    temp_ = ann[ann_key] 
                    if ann_key == "class":
                        if temp_ != "" and temp_ in self.info_json['classes']: 
                            self.doppio_output[ann_key].append(int(self.info_json['classes'][temp_]))
                        else:
                            break
                    elif ann_key == "keypoint":
                        self.doppio_output[ann_key].append(temp_)
                    elif ann_key == "segmentation":
                        h, w, _ = im_rgb.shape
                        m = np.zeros([h, w], dtype=np.int32)
                        if len(np.array(temp_).shape) == 2:
                            self.doppio_output[ann_key].append(cv2.fillPoly(m,  [np.array(temp_)], 1 ))
                        else:
                            make_temp_array = [np.array(l) for l in temp_]
                            self.doppio_output[ann_key].append(cv2.fillPoly(m, make_temp_array,1 ))
                    elif ann_key == "segmentation_path":                
                        self.doppio_output[ann_key].append(mask)
                    else:
                        self.doppio_output[ann_key].append(temp_)

        for key in self.transforms_kwargs_input:
            if key == "image":
                self.transforms_kwargs_input[key] = im_rgb
            elif key == 'bboxes':
                self.transforms_kwargs_input[key] =  self.doppio_output['bbox']
            elif key == "class":
                self.transforms_kwargs_input[key] = self.doppio_output['class']
            elif key == "mask": 
                mask = self.doppio_output['segmentation_path'][0]
                copy_mask = np.zeros_like(mask)
                for temp_key, value in self.ori2valid_class_num.items():   
                    copy_mask[mask == temp_key] = value
                self.transforms_kwargs_input[key] = copy_mask
            elif key == "masks":
                self.transforms_kwargs_input[key] = self.doppio_output['segmentation']
            elif key == "keypoints":
                self.transforms_kwargs_input[key] = [el for kp in self.doppio_output['keypoint'] for el in kp]
            elif key == "keypoint_labels":
                self.transforms_kwargs_input[key] = self.keypoint_classes * len(self.doppio_output['keypoint'])
            elif key == "keypoint_visible":
                self.transforms_kwargs_input[key] = [el for kp in self.doppio_output['keypoint_visible'] for el in kp]    
       
        img_tensor = self.transform(**self.transforms_kwargs_input)


        return img_tensor

    # 데이터의 전체 길이를 구하는 함수
    def __len__(self):
        return len(self.json_files)


    def check_json_from_local(self, file_path, label_path , valid_classes=None, semantic_mask_flag=0):

        # file_path = "/home/ai/disk/data/doppio/{}/{}/doppio_labels/{}_labels/files.json".format(dataset, split_dir,list(task_info.keys())[0])

        total_json_files = {"label_files": [], "image_files": [], "mask_files" : []}

        with open(file_path, "r") as json_path:

            json_file = json.load(json_path)

        json_files = json_file['label_files']

        if valid_classes == None or semantic_mask_flag == 1:
            return json_file
        
        for json_file_name in json_files:

            json_path = os.path.join(label_path, json_file_name)  

            with open(json_path, "r") as json_path_:
                json_file = json.load(json_path_)

            img_name = json_file['image_name']
            json_name = json_file_name

            flag = 0 
            for ann in json_file['annotation']:
                classes = ann['class']
                if classes in valid_classes:
                    flag = 1
                    break
            if flag == 1:
            
                total_json_files["label_files"].append(json_name)
                total_json_files['image_files'].append(img_name)

        return total_json_files # json format




def collate(batch_data):

    keys_ = batch_data[0].keys()
    return_dict ={}

    for k in keys_:
        if k == 'class_labels':
            tmps = [s[k] for s in batch_data]
            return_dict[k] = tmps
        elif k == "keypoints":
            max_value = max(batch_data[0]["keypoint_labels"]) + 1
            tmps = [torch.as_tensor( np.array(s[k]).reshape(-1,max_value,2)) for s in batch_data]
            return_dict[k] = tmps
        elif k == "keypoint_labels":
            max_value = max(batch_data[0]["keypoint_labels"]) + 1
            tmps = [torch.as_tensor( np.array(s[k]).reshape(-1,max_value)) for s in batch_data]
            return_dict[k] = tmps
        elif k == "keypoint_visible":
            max_value = max(batch_data[0]["keypoint_labels"]) + 1
            tmps = [torch.as_tensor( np.array(s[k]).reshape(-1, max_value)) for s in batch_data]
            return_dict[k] = tmps
        elif k == 'image':
            tmp = [s[k] for s in batch_data]
            return_dict[k] = torch.stack(tmp, 0)
        elif k == "masks":
            try:
                h, w = batch_data[0][k][0].shape    
                tmps = [torch.from_numpy(np.vstack(s[k]).astype(np.float).reshape(-1, h, w)) for s in batch_data]
                return_dict[k] = tmps
            except:
                continue
        elif k == "mask":
            tmp = [s[k] for s in batch_data]
            return_dict[k] = torch.stack(tmp, 0)
        elif k == "bboxes":
            tmps = [torch.as_tensor(s[k]) for s in batch_data]
            return_dict[k] = tmps
        else:
            tmps = [torch.as_tensor(s[k]) for s in batch_data]
            return_dict[k] = tmps
        

    return return_dict    
    




    

    
