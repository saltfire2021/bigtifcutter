import imageio
import os

# 读取tif文件
filepath = 'croped.tif'
multi_channel_image = imageio.volread(filepath, 'tif')

# multi_channel_image 是一个三维数组，形状通常是 (通道数, 高度, 宽度)
print(f"图像形状: {multi_channel_image.shape}")

# 可以选择处理特定的通道
# 例如，打印第一个通道的数据
channel_0 = multi_channel_image
print(f"第一个通道的数据: {channel_0}")
import matplotlib.pyplot as plt


# 使用imshow创建热力图
plt.imshow(channel_0, cmap='hot', interpolation='nearest')
plt.colorbar()  # 显示颜色条

# 显示图表
plt.show()

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

for i in range(1, 10):
    # 读取上传的tif文件
    tif_file_path = f'tif_acc\o001\slice203__5_{i}.tif'
    print(i)
    img = Image.open(tif_file_path)

    # 将图像转换为numpy数组
    data = np.array(img)
    print(data.shape)

    # 绘制热力图
    plt.imshow(data, cmap='hot')
    plt.colorbar()
    plt.title('Heatmap from TIF file')

    plt.show()