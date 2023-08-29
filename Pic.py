import os
from PIL import Image, ImageDraw, ImageFont

def generate_handwriting_image(text, font_file, output_path):
    # 设置图片大小和背景色
    image_width = 800
    image_height = 200

    # 设置字体和字体大小
    font_size = 72
    font = ImageFont.truetype(font_file, font_size)

    # 创建空白图片和绘图对象，背景设置为透明
    image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # 设置文字颜色为黑色
    text_color = (0, 0, 0)

    # 计算文字在图片中的位置
    text_bbox = font.getbbox(text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2

    # 绘制文字
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # 放大图片
    image = image.resize((int(image_width * 1.2), int(image_height * 1.2)))

    # 保存图片
    image.save(output_path)

def insert_text(directory, text, font_file):
    # 检查目录是否存在，不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 生成手写体图片
    handwriting_image_path = os.path.join(directory, 'handwriting.png')
    generate_handwriting_image(text, font_file, handwriting_image_path)

    # 遍历目录下的所有JPG文件
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(directory, filename)

            # 打开目录中的图片
            with Image.open(file_path) as base_image:
                base_width, base_height = base_image.size

                # 打开手写体图片
                with Image.open(handwriting_image_path) as handwriting_image:
                    # 计算插入位置
                    insert_pos = (base_width - 100 - handwriting_image.width, 100)

                    # 将手写体图片插入到目录中的图片右上角下方100像素、左方100像素位置
                    base_image.paste(handwriting_image, insert_pos, handwriting_image)

                    # 保存处理后的图片到results文件夹
                    result_directory = os.path.join(directory, 'results')
                    if not os.path.exists(result_directory):
                        os.makedirs(result_directory)

                    result_path = os.path.join(result_directory, filename)
                    base_image.save(result_path)

                    print(f'处理完成: {result_path}')

# 用户输入目录和文字
directory = input('请输入目录路径: ')
text = input('请输入班级 姓名 学号: ')

# 用户输入字体文件的名称
font_file = input('请输入字体文件的名称（.ttf格式）: ')

# 调用函数处理图片
insert_text(directory, text, font_file)
