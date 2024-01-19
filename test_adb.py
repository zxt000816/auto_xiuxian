import adbutils

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
for info in adb.list():
    print(info.serial, info.state)
    # <serial> <device|offline>

# only list state=device
print(adb.device_list())

# # Set socket timeout to 10 (default None)
# adb = adbutils.AdbClient(host="127.0.0.1", port=5037, socket_timeout=10)
# print(adb.device_list())

output = adb.connect("127.0.0.1:5560")
print(output)

d = adb.device(serial="emulator-5554")

d.screenshot()

dir(d)

d.window_size()

d.click(100, 100)