# import adbutils

# adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
# for info in adb.list():
#     print(info.serial, info.state)
#     # <serial> <device|offline>

# # only list state=device
# print(adb.device_list())

# # # Set socket timeout to 10 (default None)
# # adb = adbutils.AdbClient(host="127.0.0.1", port=5037, socket_timeout=10)
# # print(adb.device_list())

# output = adb.connect("127.0.0.1:5560")
# print(output)

# d = adb.device(serial="emulator-5554")

# d.screenshot()

# dir(d)

# d.window_size()

# d.click(100, 100)

import adbutils
import pyautogui
import pyscreeze
from matplotlib import image
import numpy as np

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
for info in adb.list():
    print(info.serial, info.state)
    # <serial> <device|offline>

# only list state=device
print(adb.device_list())


d = adb.device(serial="emulator-5560")

needle_image = image.imread("./FanRenXiuXianIcon_1920_1080/xiu_lian/xiu_lian_xin_de.png")
needle_image = needle_image[:, :, ::-1] # convert from RGB to BGR


haystack_image = image.imread("./FanRenXiuXianIcon_1920_1080/xiu_lian/xiu_lian_xin_de.png")
haystack_image = haystack_image[:, :, ::-1] # convert from RGB to BGR
# haystack_image = d.screenshot()
# convert haystack_image to numpy array
# haystack_image = np.array(haystack_image)

# display(
#     d.screenshot(),
#     needle_image,
# )

pyscreeze.locate(needle_image, haystack_image, confidence=0.8)
