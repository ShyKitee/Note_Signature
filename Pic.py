import os
from PIL import Image, ImageDraw, ImageFont

def generate_handwriting_image(text, font_file, output_path, scale_factor):
    # 设置图片大小和背景色
    image_width = 800
    image_height = 200

    # 创建空白图片和绘图对象，背景设置为透明
    image = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # 设置文字颜色为黑色
    text_color = (0, 0, 0)

    # 动态调整字体大小以适应图片宽度
    font_size = 72
    font = ImageFont.truetype(font_file, font_size)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]

    while text_width > image_width - 20:
        font_size -= 2
        font = ImageFont.truetype(font_file, font_size)
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]

    text_height = text_bbox[3] - text_bbox[1]
    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2

    # 绘制文字
    draw.text((text_x, text_y), text, font=font, fill=text_color)

    # 保存图片
    image.save(output_path)

def insert_text(directory, text, font_file, right_margin, top_margin, scale_factor):
    # 检查目录是否存在，不存在则创建
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 生成手写体图片
    handwriting_image_path = os.path.join(directory, 'handwriting.png')
    generate_handwriting_image(text, font_file, handwriting_image_path, scale_factor)

    # 检查生成的手写体图片
    print(f'手写体图片已生成：{handwriting_image_path}')
    with Image.open(handwriting_image_path) as handwriting_image:
        handwriting_image.show()  # 显示手写体图片以确保其生成正确

    # 遍历目录下的所有图片文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory, filename)
            print(f'正在处理文件: {file_path}')

            # 打开目录中的图片
            with Image.open(file_path) as base_image:
                base_width, base_height = base_image.size
                print(f'原始图片大小: {base_width}x{base_height}')

                # 打开手写体图片
                with Image.open(handwriting_image_path) as handwriting_image:
                    # 计算手写体图片缩放后的大小
                    new_width = int(base_width * scale_factor)
                    new_height = int(handwriting_image.height * (new_width / handwriting_image.width))
                    handwriting_image = handwriting_image.resize((new_width, new_height), Image.LANCZOS)
                    print(f'手写体图片缩放后的大小: {new_width}x{new_height}')

                    # 计算插入位置（居右居上），考虑右侧边距和顶部边距
                    insert_pos = (base_width - new_width - right_margin, top_margin)
                    print(f'插入位置: {insert_pos}')

                    # 创建一个临时图片，保持原始图片并叠加手写体图片
                    temp_image = base_image.convert('RGBA')
                    temp_image.paste(handwriting_image, insert_pos, handwriting_image)

                    # 将处理后的图片转换为RGB模式以保存为JPEG格式
                    final_image = temp_image.convert('RGB')

                    # 保存处理后的图片到results文件夹
                    result_directory = os.path.join(directory, 'results')
                    if not os.path.exists(result_directory):
                        os.makedirs(result_directory)

                    result_path = os.path.join(result_directory, filename)
                    final_image.save(result_path)

                    print(f'处理完成: {result_path}')

# 用户输入目录和文字
print("本工具支持对JPG JPEG PNG格式图片进行操作，使用前请将所有需要操作的图片放置在同一文件夹")
print("仅供测试使用，疑问请联系Vx：canaan04")
directory = input('请输入目录绝对路径: ')
text = input('请输入班级 姓名 学号（或想插入的文本）: ')

# 用户输入字体文件的名称
font_file = input('请输入字体文件的名称（.ttf格式）: ')

# 用户输入右侧边距
right_margin = int(input('请输入手写签名距离最右侧的像素值(不懂就填0): '))

# 用户输入顶部边距
top_margin = int(input('请输入手写签名距离最上侧的像素值(不懂就填0): '))

# 用户输入缩放因子
scale_factor = float(input('请输入手写体图片缩放因子（0到1之间，一般为0.5）: '))

# 调用函数处理图片
insert_text(directory, text, font_file, right_margin, top_margin, scale_factor)
