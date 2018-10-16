
__version__ = "SearchAPP_v1.1"
__author__ = "Elloit Aldersion"
__create_date__ = "2017-10-23"
"""
实现验证码的生成
"""
# coding = UTF-8

# !/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os


class getcode(object):

    def _rndChar(self):
        """
        随机字母
        """
        return chr(random.randint(65, 90))

    def _rndColor(self):
        """
        随机颜色1
        """
        return (
            random.randint(
                64, 255), random.randint(
                64, 255), random.randint(
                64, 255))

    def _rndColor2(self):
        """
        随机颜色2
        """
        return (
            random.randint(
                32, 127), random.randint(
                32, 127), random.randint(
                32, 127))

    def create(self):
        # 240 x 60:
        width = 60 * 4
        height = 60
        image = Image.new('RGB', (width, height), (255, 255, 255))
        # 创建Font对象:
        path = os.path.dirname(os.path.abspath(__file__))
        print(path)
        font = ImageFont.truetype(path+'/data/Arial.ttf', 36)
        # 创建Draw对象:
        draw = ImageDraw.Draw(image)
        # 填充每个像素:
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=self._rndColor())
        # 输出文字:
        codes = []
        for t in range(4):
            code = self._rndChar()
            draw.text((60 * t + 10, 10), code,
                      font=font, fill=self._rndColor2())
            codes.append(code)
        codes = "".join(codes)
        # 模糊:
        image = image.filter(ImageFilter.BLUR)
        # image.save('code.jpg', 'jpeg')
        return image, codes

if __name__ == '__main__':
    a = getcode()
    print(a.create())
