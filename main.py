#########################################################
# source code: https://github.com/Albert723/pic_to_wall #
#########################################################
from PIL import Image, ImageDraw, ImageFont
import os
from tqdm import tqdm

#generate the pic by text
def gen_text_img(text, font_size=20, font_path=None):
    # args：文字内容，文字字体大小，字体路径(Text content, text font size, font path)
    font = ImageFont.truetype(font_path, font_size) if font_path is not None else None
    (width, length) = font.getsize(text)  # 获取文字大小(Get text size)
    text_img = Image.new('RGBA', (width, length))
    draw = ImageDraw.Draw(text_img)
    # 第一个tuple表示未知(left,up)，之后是文字，然后颜色，最后设置字体
    # (The first tuple means unknown (left,up), followed by text, and then color, and finally font setting)
    draw.text((0, 0), text, fill=(0, 0, 0), font=font)
    text_img.save('./Final_Competition.png')
    return text_img

# adjust the transparency of the pic
def trans_alpha(img, pixel):
    '''
    根据rgba的pixel调节img的透明度
    这里传进来的pixel是一个四元组（r,g,b,alpha）
    According to the Pixel of RGBA to adjust the transparency of the img
    The current pixel is a four-dimensional tuple (r,g,b,alpha)
    '''
    _, _, _, alpha = img.split()
    alpha = alpha.point(lambda i: pixel[-1]*10)
    img.putalpha(alpha)   #Part2有介绍 Refer to Part2
    return img

# cover the pic with the transparency
def picture_wall_mask(text_img, edge_len, pic_dir="./user"):
    # 根据文字图gen_text_img像生成对应的照片墙，输入：文字图像，各个照片边长，照片所在路径
    # Generate the corresponding photo wall based on the text image gen_text_img.
    # Input: text image, length of each photo side, and path of the photo
    new_img = Image.new('RGBA', (text_img.size[0] * edge_len, text_img.size[1] * edge_len))
    file_list = os.listdir(pic_dir)
    img_index = 0
    for x in tqdm(range(0, text_img.size[0])):
        for y in range(0, text_img.size[1]):
            pixel = text_img.getpixel((x, y))         # Refer to Part2
            file_name = file_list[img_index % len(file_list)]
            try:
                img = Image.open(os.path.join(pic_dir, file_name)).convert('RGBA') # Refer to Part2
                img = img.resize((edge_len, edge_len))
                img = trans_alpha(img, pixel)
                new_img.paste(img, (x * edge_len, y * edge_len)) #指定区域替换，Specified area replacement Refer to Part2
                img_index += 1
            except Exception as e:
                print(f"open file {file_name} failed! {e}")
    return new_img

# generate the photo wall
def main(text='', font_size = 20, edge_len = 60,pic_dir = "./user", out_dir = "./out/", font_path = './test.ttf'):
    '''
    Generate the photo wall
    :param text: Text of picture wall, if not defined this will generage a rectangle picture wall
    :param font_size: font size of a clear value
    :param edge_len: sub picture's egde length
    '''
    if len(text) >= 1:
        text_ = ' '.join(text)       #将字符串用空格分隔开，提高展示效果 Use Spaces to separate strings to improve presentation
        #text_ = text
        print(f"generate text wall for '{text_}' with picture path:{pic_dir}")
        text_img = gen_text_img(text_, font_size, font_path)
        # text_img.show()
        img_ascii = picture_wall_mask(text_img, edge_len, pic_dir)
        # img_ascii.show()
        img_ascii.save(out_dir + os.path.sep + '_'.join(text) + '.png')



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(text='python')

# ############Part 2##################
'''
In digital image processing, there are specific processing algorithms for different image formats. 
Therefore, before doing image processing, we need to consider clearly which format of the image we
want to design the algorithm and its implementation. Based on this requirement, this article uses PIL
, an image processing library in Python, to convert different image formats. For color images, 
whether the Image format is PNG, BMP, or JPG, in PIL, after opening the Image module with the open() 
function, the returned Image object mode is "RGB". For grayscale images, whether the image format is 
PNG, BMP, or JPG, the mode is "L" when opened. Conversion between PNG, BMP, and JPG color Image 
formats can be done through the Image module's Open () and Save () functions. To be specific, 
when these images are opened, PIL decodes them into "RGB" images of three channels. Users can process
this "RGB" image based on it. Once processed, you can use the function Save () to save the processed 
results in any format in PNG, BMP, and JPG. This completes the conversion between several formats. 
Similarly, color images in other formats can be converted in this way. Of course, grayscale images of
different formats can also be completed in a similar way, but the images decoded by PIL are those
with the mode "L".
'''
