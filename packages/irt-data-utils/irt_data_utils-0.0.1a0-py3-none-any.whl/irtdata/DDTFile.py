import numpy as np
from IRTCore import MagSDK
from IRTCore.MagDevice import MagDevice
import matplotlib.pyplot as plt
import seaborn as sns

def convert_ddt_to_csv_png(ddt_path,csv_path,png_path="",bmp_path=""):
    device = MagDevice()
    if device.Initialize():
        print("IRTCore: init success")
    else:
        print("IRTCore: init failed")

    if device.LoadDDT_v2(ddt_path, MagSDK.MAG_FRAMECALLBACK(), None):
        print("IRTCore: load ddt success")

        # print camera information
        camera_info = device.GetCamInfoEx()

        if bmp_path!="":
            device.SaveBMP(dwIndex=0, charFilename=bmp_path)

        # get temperature matrix, if True for input para , function will const a lot of time
        if csv_path!="":
            temp_matrix = device.GetTemperatureData(True)
            temp_array = np.asarray(temp_matrix).reshape((camera_info.BaseInfo.intFPAHeight,
                                                          camera_info.BaseInfo.intFPAWidth)).astype(np.int32)

            f_out = open(csv_path, "w", encoding='utf-8')
            for i in range(len(temp_array) - 1, 0, -1):
                line = []
                for j in range(len(temp_array[0])):
                    line.append(round(temp_array[i][j] / 1000, 1))
                line_str = [str(l) for l in line]
                f_out.write(",".join(line_str) + "\n")
            f_out.close()
        if png_path!="":
            generate_png(csv_path,png_path)

def read_infrared_data(file):
    lines = open(file, "r", encoding='utf-8')
    data = []
    for line in lines:
        vs = line.strip().split(",")
        row = [float(v) for v in vs]
        data.append(row)
    return data

def generate_png(csv_path,image_path):
    data=read_infrared_data(csv_path)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
    sns.set(font='SimHei', font_scale=0.8, style="ticks")  # 解决Seaborn中文显示问题

    ax = sns.heatmap(data,
                     xticklabels=False,  # remove the labels
                     yticklabels=False,
                     cbar=False,
                     cmap='inferno'
                     )
    plt.tight_layout()

    plt.savefig(image_path, dpi=600, bbox_inches='tight', pad_inches=0)

