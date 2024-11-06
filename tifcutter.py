import os
import tkinter as tk
from tkinter import filedialog

import imageio
import matplotlib
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import filedialog
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global click_times  # 在全局作用域中初始化click_times
click_times = 0

global file_path_img
file_path_img=''


import math

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.transforms import Affine2D

def on_plot_hover(event):
    global click_times  # 声明click_times是全局变量
    global x1, y1, x2, y2, x3, y3, x4, y4  # 声明坐标变量为全局变量

    if event.xdata is not None and event.ydata is not None:
        print(f"Clicked coordinates: ({event.xdata}, {event.ydata})")

    if click_times == 0:
        x1 = event.xdata
        y1 = event.ydata

    elif click_times == 1:
        x4 = event.xdata
        y4 = event.ydata

    click_times += 1  # 更新click_times的值
    if click_times <= 3:
        print(f"x1{x1}y1{y1}x4{x4}y4{y4}")
    else:
        print("Maximum number of clicks reached.")

def process_tif(file_path, canvas, fig):
    """
    处理TIF文件的函数。这里仅作为示例，实际功能需要根据需求实现。
    """
    # 打开并显示图片
    filepath = file_path
    multi_channel_image = imageio.volread(filepath, 'tif')

    # multi_channel_image 是一个三维数组，形状通常是 (通道数, 高度, 宽度)
    print(f"图像形状: {multi_channel_image.shape}")

    # 可以选择处理特定的通道
    # 例如，打印第一个通道的数据
    channel_0 = multi_channel_image[200]
    print(f"第一个通道的数据: {channel_0}")
    import matplotlib.pyplot as plt

    # 模拟的数据，使用用户提供的部分数据结构
    # channel_0 = [
    #     [0, 0, 35, 7, 0, 0],
    #     [0, 0, 34, 37, 0, 0],
    #     [0, 0, 34, 0, 0, 0],
    #     [0, 0, 44, 40, 0, 0],
    #     [0, 0, 55, 32, 0, 0],
    #     [0, 0, 46, 16, 0, 0]
    # ]



    # 清除旧的图形
    fig.clear()

    # 使用imshow创建热力图
    ax = fig.add_subplot(111)
    cax = ax.imshow(channel_0, cmap='hot', interpolation='nearest')
    # fig.colorbar(cax)
    # 连接点击事件
    fig.canvas.mpl_connect('button_press_event', on_plot_hover)

    # 重绘图形
    canvas.draw()


def select_file(canvas, fig):
    """
    文件选择函数，用于打开文件选择对话框并处理选中的文件。
    """
    global file_path_img

    file_path = filedialog.askopenfilename(filetypes=[("TIF files", "*.tif")])
    if file_path:
        process_tif(file_path, canvas, fig)
    file_path_img = file_path
    click_times=0


def startcut():
    global x1, y1, x2, y2, x3, y3, x4, y4  # 声明坐标变量为全局变量
    print(f"x1{x1}y1{y1}x2{x2}y2{y2}x3{x3}y3{y3}x4{x4}y4{y4}")
    print(file_path_img)
    file_single_name = os.path.basename(file_path_img)
    file_header_name = file_single_name.replace('.tif','')
    print(file_header_name)
    readpath = f"tif/{file_single_name}"
    outname = 'o' + file_header_name
    rotate_angle = float(text_box.get())
    print(rotate_angle)

    # 读取tif文件
    filename = readpath
    multi_channel_image = imageio.volread(filename, 'tif')


    # multi_channel_image 是一个三维数组，形状通常是 (通道数, 高度, 宽度)
    print(f"图像形状: {multi_channel_image.shape}")
    os.mkdir(f"tif_acc/{outname}")

    # 可以选择处理特定的通道
    # 例如，打印第一个通道的数据
    for index_channel in range(0, 512):
        print(f'processing{index_channel}')

        channel_0 = multi_channel_image[index_channel]
        # print(f"第一个通道的数据: {channel_0}")
        image = Image.fromarray(channel_0)

        # 1.6
        # Rotate the image 10 degrees to the right
        rotated_image = image.rotate(-rotate_angle, expand=True)
        rotated_image_path = 'rotated.tif'
        rotated_image.save(rotated_image_path)

        cut_x1, cut_y1 = x1, y1
        # cut_x2, cut_y2 = x4, y4
        # print(f'x1{x1}y1{y1}x4{x4}y4{y4}')
        # cut_x1, cut_x2 = min(cut_x1, cut_x2), max(cut_x1, cut_x2)
        # cut_y1, cut_y2 = min(cut_y1, cut_y2), max(cut_y1, cut_y2)
        cropped_image = rotated_image.crop((cut_x1, cut_y1+24, cut_x1+480, cut_y1+24+320))
        # Save the rotated image
        cropped_image_path = 'croped.tif'
        cropped_image.save(cropped_image_path)

        # 确保cut文件夹存在，如果不存在则创建
        if not os.path.exists(outname):
            os.makedirs(outname)

        img = cropped_image

        # 计算每份图像的宽度和高度
        width, height = img.size
        horizontal_slice_width = width // 10
        vertical_slice_height = height // 10

        # 切割图像并保存
        for i in range(10):
            for j in range(10):
                # 计算每份图像的坐标
                left = i * horizontal_slice_width
                upper = j * vertical_slice_height
                right = left + horizontal_slice_width
                lower = upper + vertical_slice_height

                # 切割图像
                slice_img = img.crop((left, upper, right, lower))


                # 保存图像
                slice_img.save(f'tif_acc/{outname}/slice{index_channel}__{i}_{j}.tif')


def testcut():
    global x1, y1, x2, y2, x3, y3, x4, y4  # 声明坐标变量为全局变量
    print(f"x1{x1}y1{y1}x2{x2}y2{y2}x3{x3}y3{y3}x4{x4}y4{y4}")
    print(file_path_img)
    file_single_name = os.path.basename(file_path_img)
    file_header_name = file_single_name.replace('.tif', '')
    print(file_header_name)
    readpath = f"tif/{file_single_name}"
    outname = 'o' + file_header_name
    rotate_angle = float(text_box.get())
    print(rotate_angle)

    # 读取tif文件
    filename = readpath
    multi_channel_image = imageio.volread(filename, 'tif')

    # multi_channel_image 是一个三维数组，形状通常是 (通道数, 高度, 宽度)
    print(f"图像形状: {multi_channel_image.shape}")


    # 可以选择处理特定的通道
    # 例如，打印第一个通道的数据
    index_channel = 200
    print(f'processing{index_channel}')

    channel_0 = multi_channel_image[index_channel]
    # print(f"第一个通道的数据: {channel_0}")
    image = Image.fromarray(channel_0)

    # 1.6
    # Rotate the image 10 degrees to the right
    rotated_image = image.rotate(-rotate_angle, expand=True)
    rotated_image_path = 'rotated.tif'
    rotated_image.save(rotated_image_path)

    cut_x1, cut_y1 = x1, y1

    # print(f'x1{x1}y1{y1}x4{x4}y4{y4}')
    # cut_x1, cut_x2 = min(cut_x1, cut_x2), max(cut_x1, cut_x2)
    # cut_y1, cut_y2 = min(cut_y1, cut_y2), max(cut_y1, cut_y2)
    cropped_image = rotated_image.crop((cut_x1, cut_y1+24, cut_x1+480, cut_y1+24+320))
    # Save the rotated image
    cropped_image_path = 'croped.tif'
    cropped_image.save(cropped_image_path)


def rotate_image(angle):
    global click_times
    click_times=0
    ax = fig.axes[0]

    # 获取图像数据
    img_data = ax.images[0]

    # 创建旋转矩阵
    rotation = Affine2D().rotate_deg(angle)

    # 更新图像的变换矩阵
    img_data.set_transform(rotation + ax.transData)

    # 设置图像显示范围，保持原始图像的中心不变
    img_shape = img_data.get_array().shape
    extent = img_data.get_extent()
    center_x = (extent[0] + extent[1]) / 2
    center_y = (extent[2] + extent[3]) / 2
    new_extent = (
        center_x - img_shape[1] / 2,
        center_x + img_shape[1] / 2,
        center_y + img_shape[0] / 2,  # 注意这里和下面的行被交换了
        center_y - img_shape[0] / 2  # 注意这里和上面的行被交换了
    )
    img_data.set_extent(new_extent)

    # 重绘图形
    canvas.draw()


def rotateleft():


    rangle=float(text_box.get())

    rotate_image(rangle)




x1 = y1 = x2 = y2 = x3 = y3 = x4 = y4 = None
# 创建主窗口
root = tk.Tk()
root.title("TIF文件处理器")



# 创建一个框架来放置按钮和文本框
frame_buttons = tk.Frame(root)
frame_buttons.pack(side=tk.TOP, fill=tk.X, expand=False)

# 创建选择文件按钮
button_select = tk.Button(frame_buttons, text="选择文件", command=lambda: select_file(canvas, fig))
button_select.pack(side=tk.LEFT, padx=3, pady=3)

# 创建裁剪按钮
button_cut = tk.Button(frame_buttons, text="开始裁剪", command=lambda: startcut())
button_cut.pack(side=tk.LEFT, padx=3, pady=3)

# 创建左旋按钮
button_left = tk.Button(frame_buttons, text="旋转", command=rotateleft)
button_left.pack(side=tk.LEFT, padx=3, pady=3)

# 创建左旋按钮
button_testcut = tk.Button(frame_buttons, text="裁剪", command=testcut)
button_testcut.pack(side=tk.LEFT, padx=3, pady=3)


# 创建文本框
text_box = tk.Entry(frame_buttons)
text_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3, pady=3)

# 创建matplotlib图形
fig = Figure(figsize=(50, 40), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# 运行主循环
root.mainloop()
