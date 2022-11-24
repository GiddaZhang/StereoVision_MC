from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD  # 当使用树莓派版本的mycobot时，可以引用这两个变量进行MyCobot初始化
import time

# MyCobot 类初始化需要两个参数：
#   第一个是串口字符串， 如：
#       linux： "/dev/ttyUSB0"
#       windows: "COM3"
#   第二个是波特率：
#       M5版本为： 115200
#
#   Example:
#       mycobot-M5:
#           linux:
#              mc = MyCobot("/dev/ttyUSB0", 115200)
#           windows:
#              mc = MyCobot("COM3", 115200)
#       mycobot-raspi:
#           mc = MyCobot(PI_PORT, PI_BAUD)
#
# 初始化一个MyCobot对象
# 下面为M5版本创建对象代码
mc = MyCobot('COM3',115200)
# 机械臂运动的位置
angles = [
            [92.9, -10.1, -60, 5.8, -2.02, -37.7],
            [92.9, -53.7, -83.05, 50.09, -0.43, -38.75],
            [92.9, -10.1, -87.27, 5.8, -2.02, -37.7]
        ]


pos_list = [
    
    [50, 200, 200, -180, 0, 0],      # up-1
    [50, 200, 120, -180, 0, 0],      # down-1

    [200, 0, 200, -180, 0, 0],      # up-2
    [200, 0, 100, -180, 0, 0],      # down-2

]


# 开启吸泵
def pump_on():
    # 让2号位工作
    mc.set_basic_output(2, 0)
    # 让5号位工作
    mc.set_basic_output(5, 0)

# 停止吸泵
def pump_off():
    # 让2号位停止工作
    mc.set_basic_output(2, 1)
    # 让5号位停止工作
    mc.set_basic_output(5, 1)

mode = 0

# 机械臂复原
mc.send_angles([0, 0, 0, 0, 0, 0], 30)
time.sleep(3)

#开启吸泵
pump_on()
mc.send_coords(pos_list[0], 30, mode)
time.sleep(2)

#吸取小物块
mc.send_coords(pos_list[1], 30, mode)
time.sleep(2)
mc.send_coords(pos_list[0], 30, mode)
time.sleep(2)
mc.send_coords(pos_list[2], 30, mode)
time.sleep(2)
mc.send_coords(pos_list[3], 30, mode)
time.sleep(2)

#关闭吸泵
pump_off()
time.sleep(4)
mc.send_coords(pos_list[2], 40, mode)
time.sleep(1.5)


