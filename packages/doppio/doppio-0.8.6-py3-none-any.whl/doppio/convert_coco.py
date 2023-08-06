import json
import os
import shutil
from glob import glob
from tqdm import tqdm
import cv2
from pycocotools import mask as maskUtils
import numpy as np
import itertools

'''
* coco 양식이지만 나중에는 하나로 묶는 코드로 진행할것. (중요)
1. coco json 파일을 올려 놓는거, rle 에 대해서 어떻게 처리할지는 나중에 회의
-  https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/coco.py , rle 에 대한 내용 -> pycocotools 설치 하게 해야함.
2. keypoint는 아직 만들지 않음. 위에 링크를 참조해서 나중에 이거에 대해서 만들어보면 될것 같다. 
3. bbox, seg, classifiation 3개 위주로 만들면 된다.  
4. 만약, format 양식이 coco  처럼 하나의 json의 전부 있는게 아니라 일대일 매칭인데 좌표만 COCO스타일인것을 처리 해줘야 할듯.

'''

def coco2doppio(json_files, dopio_save_path, task_tag = None, rle_ = False):


    # task_tag 의 key는 task 정보를 담고 있다. 
    save_label_path = os.path.join(dopio_save_path, "doppio_labels/{}_labels/".format(list(task_tag.keys())[0]))

    # task example # keypoint_detection or # object_detection
    task = list(task_tag.keys())[0]

    # make file path
    if not os.path.exists(dopio_save_path + "/doppio_labels"):
        os.mkdir(dopio_save_path + "/doppio_labels")

    # label 폴더가 있으면 겹칠 수 있기 때문에 삭제 
    if os.path.exists(save_label_path) and os.path.isdir(save_label_path):
        shutil.rmtree(save_label_path)
    
    os.mkdir(save_label_path)

    # info_json_form 을 불러오는 코드
    with open("/home/ai/projects/data_api/info.json", 'r') as f:
        format_info_json = json.load(f)


    for json_file in json_files:

        # coco 의 label format
        with open(json_file, 'r') as f:
            format_coco_label = json.load(f)
      
        # catgory dictory 만들기
        categories = format_coco_label['categories']
        dopio_categories_dict = {}
        classes_list = []
        for category in categories:

            id = category["id"]
            name = category['name']
            dopio_categories_dict[id] = name

            if task == "keypoint_detection":
                format_info_json['keypoint_classes'] = {key: idx for idx, key in enumerate(category['keypoints'])}
                format_info_json['skeleton'] = category['skeleton']
                classes_list.append([name, id - 1])
            else:
                classes_list.append([name, id - 1])

        format_info_json['classes'] = {name: id for name, id in classes_list}
        format_info_json['classes'] = {key : idx for idx, key in enumerate(format_info_json['classes'].keys())}

        print(format_info_json['classes'])

        temp_tag = list(task_tag.values())[0]
        tag_list = []

        for L in range(1, len(temp_tag) + 1):
            for subset in itertools.combinations(temp_tag, L):
                tag_list.append(list(subset))
        
        format_info_json['tag'] = tag_list

        # image id 뽑기
        dopio_image_info_dict = {}
        images_info = format_coco_label['images']

        for image_info in images_info:
            key = image_info['id']
            image_name = image_info['file_name']
            width, height = image_info['width'], image_info['height']

            dopio_image_info_dict[key] = {"image_name" : image_name, "width" : width, "height" : height}

        # annotation 만들기
        annotations = format_coco_label['annotations']

        for ann in tqdm(annotations):
            
            with open("./doppio_label_format.json", 'r') as f:
                format_dopio_label = json.load(f)
            

            image_id = ann['image_id']
            category_id = ann['category_id']
            info_ = dopio_image_info_dict[image_id] # info type dict
            class_ = dopio_categories_dict[category_id] # class type str


            # format_dopio_label
            bbox_ = ann['bbox']
            seg_ = ann['segmentation']
            # rle 일때 해당하는 작업
            if type(seg_) != list and not rle_:
                if type(ann['segmentation']['counts']) == list:
                    rle = maskUtils.frPyObjects([ann['segmentation']], height, width)
                else:
                    rle = [ann['segmentation']]
                m = maskUtils.decode(rle)
                cnt, _ = cv2.findContours(m,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                seg_pos= []
                for seg_tmp in cnt:
                    seg_tmp = np.array(seg_tmp, dtype=np.int32).reshape(-1,2).tolist()
                    seg_pos.append(seg_tmp)
            else:
                seg_pos= []
                if len(seg_) > 1:
                    for seg_tmp in seg_:
                        seg_tmp = np.array(seg_tmp, dtype=np.int32).reshape(-1,2).tolist()
                        seg_pos.append(seg_tmp)
                else:
                    seg_pos = np.array(seg_,dtype=np.int32).reshape(-1,2).tolist()

            # key points
            keypoint_ = []
            keypoint_visible_ = []

            if "keypoints" in ann.keys():
                temp_keypoint = ann['keypoints']
                keypoint_, keypoint_visible_ = np.array(temp_keypoint, dtype=np.int32).reshape(-1,3)[:,0:2].tolist(), np.array(temp_keypoint, dtype=np.int32).reshape(-1,3)[:,2].tolist()
                
            seg_ = seg_pos

            area = ann['area']

            # make dopio label format
            format_dopio_label['image_name'] = info_['image_name']
            file_name =  info_['image_name'].split('.')[0]

        
            # 파일이 존재하면 불러와서 작업을 한다. 
            if os.path.exists(os.path.join(save_label_path,"{}.json".format(file_name))):
                with open(os.path.join(save_label_path,"{}.json".format(file_name)), 'r') as f:
                    format_dopio_label = json.load(f)
                    x1, y1, x2, y2 = int(bbox_[0]), int(bbox_[1]), int(bbox_[2] + bbox_[0]), int(bbox_[3] + bbox_[1])
                    if x1 == x2 or y1 == y2:
                        continue
                    dopio_ann = {"class": class_, 'bbox': [x1, y1, x2, y2], 'segmentation': seg_, 'area' : area, 'keypoint': keypoint_, "keypoint_visible" : keypoint_visible_}
                    format_dopio_label['annotation'].append(dopio_ann)   
            else:
                format_dopio_label['image_size']['width'] =info_['width']
                format_dopio_label['image_size']['height'] = info_['height']
                format_dopio_label['image_size']['channel'] = 3

                x1, y1, x2, y2 = int(bbox_[0]), int(bbox_[1]), int(bbox_[2] + bbox_[0]), int(bbox_[3] + bbox_[1])
                if x1 == x2 or y1 == y2:
                    print("save_label_path",file_name )
                    continue

                format_dopio_label["annotation"] = [{"class": class_, 'bbox': [x1, y1, x2, y2], 'segmentation': seg_, 'area' : area, 'keypoint': keypoint_,  "keypoint_visible" : keypoint_visible_}]


            # 파일 우선 저장
            with open(os.path.join(save_label_path,"{}.json".format(file_name)), 'w') as f:
                json.dump(format_dopio_label, f)

    with open(os.path.join(save_label_path,"info.json"), 'w') as f:
        json.dump(format_info_json, f)

    
    make_jsons = glob(os.path.join(save_label_path,"*.json"))

    for j in make_jsons:

        if "info.json" in j:
                continue
    
        with open(j, 'r') as f:
            temp_json = json.load(f)
        temp_dict = {}
        for ann in temp_json['annotation']:
            if str(ann['bbox']) in temp_dict.keys() and len(ann['keypoint']) > 0:
                temp_dict[str(ann['bbox'])] = ann
            elif str(ann['bbox']) not in temp_dict.keys():
                temp_dict[str(ann['bbox'])] = ann
    
        temp_json['annotation'] = [temp_dict[d] for d in temp_dict.keys()]

        with open(j, 'w') as f:
            json.dump(temp_json, f)


# coco label json path
json_path = "/home/ai/disk/data/doppio/ms_coco/val/labels/instances_val2017.json"
json_files = glob(json_path)

# dopio 저장할 위치 
dopio_save_path = "/home/ai/disk/data/doppio/ms_coco/val/"

#task_tag = {"keypoint_detection": ["bbox", "segmentation", "class", "keypoint"]}
#task_tag = {"object_detection": ["bbox", "class"]}
task_tag = {"instance_segmentation": ["bbox", "class", "segmentation"]}
coco2doppio(json_files=json_files, dopio_save_path = dopio_save_path, task_tag=task_tag)





    
    

