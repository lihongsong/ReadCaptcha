# -*- coding:utf-8 -*-

from PIL import Image

import os

import time

import math

import hashlib

# 先把两个图片的像素值计算为一个向量
# 然后通过向量的余弦定理计算夹角从而判断相似度 cosA = (x1 * x2 + y1 * y2) / (sqrt(x1^2 + y1^2) * sqrt(x2^2 + y2^2))
class VectorCompare:
    # 计算矢量大小

    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    # 计算矢量之前的cos值
    def relation(self,concordance1, concordance2):
        relevance = 0
        topvalue = 0

        for word, count in concordance1.items():
            if set(concordance2.keys()).issuperset({word}):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

def buildvector(im):
    d1 = {}

    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1

    return d1

v = VectorCompare()

iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m',
'n','o','p','q','r','s','t','u','v','w','x','y','z']

imageset = []

for letter in iconset:
    for img in os.listdir('./iconset/%s/' % (letter)):
        temp = []
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
            imageset.append({letter:temp})

im = Image.open("captcha.gif")
im2 = Image.new("P",im.size,255)
# 将图片转换为8位像素模式
im.convert("P")
temp = {}

for x in range(im.size[1]):
    for y in range(im.size[0]):
        pixel = im.getpixel((y,x))
        if pixel == 220 or pixel == 227:
            im2.putpixel((y,x),0)


inletter = False
foundletter = False

start = 0
end = 0

letters = []

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    if foundletter == False and inletter == True:
        foundletter = True
        start = y

    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start,end))

    inletter = False

count = 0

# 删除之前没用的文件
def clearHistoryImage():
    lists = os.listdir("./")
    for item in lists:
        if item.find("gif") != -1 and item != "captcha.gif":
            os.remove(item)

# 分割图片
for index,letter in enumerate(letters):
    m = hashlib.md5()
    im3 = im2.crop(( letter[0] ,0 ,letter[1], im2.size[1] ))
    name = "%s%s" % ((time.time()),str(index))
    m.update(name.encode("utf-8"))
    im3.save("./%s.gif" % (m.hexdigest()))

    guess = []

    for image in imageset:
        for x,y in image.items():
            if len(y) != 0:
                guess.append( (v.relation(y[0],buildvector(im3)),x) )
    guess.sort(reverse = True)
    print("",guess[0])

clearHistoryImage()
