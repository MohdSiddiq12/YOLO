#convert annotations for YOLO format 
import os
import re
from PIL import Image

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

# Create output directories
if not os.path.exists('penn_fudan/yolo_labels'):
    os.makedirs('penn_fudan/yolo_labels')

# Loop through annotation files
for ann_file in os.listdir('D:\YOLO-Project\PennFudanPed\PennFudanPed\Annotation'):
    if ann_file.endswith('.txt'):
        image_id = ann_file.split('.')[0]
        img_path = os.path.join('D:\YOLO-Project\PennFudanPed\PennFudanPed\PNGImages', f'{image_id}.png')
        img = Image.open(img_path)
        w, h = img.size

        with open(os.path.join('penn_fudan/yolo_labels', f'{image_id}.txt'), 'w') as out_file:
            with open(os.path.join('D:\YOLO-Project\PennFudanPed\PennFudanPed\Annotation', ann_file)) as f:
                lines = f.readlines()
                for line in lines:
                    if "Bounding box" in line:
                        box = re.findall(r"\((\d+), (\d+)\) - \((\d+), (\d+)\)", line)[0]
                        box = list(map(int, box))
                        bbox = convert((w, h), (box[0], box[2], box[1], box[3]))
                        out_file.write(f'0 {" ".join(map(str, bbox))}\n')  # Class '0' for person

print('Annotations converted to YOLO format.')
