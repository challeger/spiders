#!/user/bin/env python
# 每天都要有好心情
"""
利用ocr技术识别图形验证码
对于有干扰的图片,可以先进行灰度处理,然后二值化
"""
import pytesseract
from PIL import Image

image = Image.open('code.jpg')
image = image.convert('L')  # 将图片转为灰度图像
threshold = 127
table = []
for _ in range(256):
    if _ < threshold:
        table.append(0)
    else:
        table.append(1)
image = image.point(table, '1')  # 二值化
image.show()
result = pytesseract.image_to_string(image)
print(result)
