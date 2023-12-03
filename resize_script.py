import os
import cv2

this_pc_res = (554, 984) # 替换为当前游戏的分辨率(注意是宽高)
other_pc_res = (1080, 1920)

width_ratio = this_pc_res[0] / other_pc_res[0]
height_ratio = this_pc_res[1] / other_pc_res[1]

# 遍历文件夹下的所有.png文件
new_root_dir = './FanRenXiuXianIcon' # 替换为当前游戏的图标文件夹
root_dir = './FanRenXiuXianIcon_1920_1080' # 1920*1080分辨率下的图标文件夹
if not os.path.exists(new_root_dir):
    os.mkdir(new_root_dir)

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.png'):
            file_path = os.path.join(root, file)
            img = cv2.imread(file_path)

            y, x, _ = img.shape

            img = cv2.resize(img, (round(x * width_ratio), round(y * height_ratio)))

            new_root = root.replace(root_dir, new_root_dir)
            if not os.path.exists(new_root):
                os.mkdir(new_root)

            new_file_path = os.path.join(new_root, file)    
            if not os.path.exists(new_file_path):
                cv2.imwrite(new_file_path, img)
                print(f"完成: {new_file_path}")
            else:
                print(f"跳过: {new_file_path}")