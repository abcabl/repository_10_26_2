
import numpy as np
import cv2
untested_objects=[]
from xml.etree import ElementTree as ET
dd=cv2.imread("./train-5/1312/1312.jpg")
def contrast(file_path_xml, test_objects, pixel=10):
    # 解析xml文件
    tree = ET.parse(file_path_xml)
    root = tree.getroot()
    objects = root.findall('object')
    # 获取xml文件中的矩形信息
    groundtruth = []
    # 列表中字典的个数
    test_count = len(test_objects)

    for obj in objects:
        x_position = int(obj.find('regionX').text)
        y_position = int(obj.find('regionY').text)
        width = int(obj.find('regionWidth').text)
        height = int(obj.find('regionHeight').text)
        # 将xml文件信息存入字典列表中
        groundtruth.append({'regionX': x_position, 'regionY': y_position, 'regionWidth': width, 'regionHeight': height})

    truth_count = len(groundtruth)
    true_count = 0
    # 将测试数据和xml文件数据对比
    for obj in test_objects:
        for item in groundtruth:
            if abs(item['regionX'] - obj['regionX']) <= pixel and abs(
                    item['regionY'] - obj['regionY']) <= pixel and abs(
                item['regionWidth'] + item['regionX'] - obj['regionWidth'] - obj['regionX']) <= pixel and abs(
                item['regionHeight'] + item['regionY'] - obj['regionHeight'] - obj['regionY']) <= pixel:
                true_count += 1
                break
    # 返回查全率和查准率
    return [true_count / truth_count, true_count / test_count]
#----------------------------------
li2=[]
li3=[]
#-----------------------------------------
l1=["./train-5/184/184.jpg","./train-5/1308/1308.jpg","./train-5/1310/1310.jpg","./train-5/1312/1312.jpg","./train-5/1315/1315.jpg"]
l2=["./train-5/184/184.xml","./train-5/1308/1308.xml","./train-5/1310/1310.xml","./train-5/1312/1312.xml","./train-5/1315/1315.xml"]
#------------------------------------------------
def scanner(num,iterations_,len_,pengzhang):
    a=cv2.imread(l1[num])
    b = cv2.imread(l1[num])
    find = gray = cv2.imread(l1[num], 0)
    # cv2.imshow("huiduhua",find)#灰度化
    # kernel = np.ones((18, 18), np.uint8)
    kernel = np.ones((pengzhang, pengzhang), np.uint8)
    # find = cv2.dilate(find, kernel, iterations=1)#调整膨胀参数
    find = cv2.dilate(find, kernel, iterations=iterations_)  # 调整膨胀参数
    ret, find = cv2.threshold(find, 236, 255, cv2.THRESH_BINARY)#246#调参
    # cv2.imshow("pengzhangjiaerhzi",find)#膨胀加二值化
    find = cv2.blur(find, (20, 20))
    # cv2.imshow("mohu",find)#模糊
    find = cv2.add(find, gray)#进行图像变换处理
    # cv2.imshow("xiangsuxiangjia",find)#\\像素相加！！！

    ret1, thresh1 = cv2.threshold(find ,90, 255, cv2.THRESH_BINARY_INV)
    # cv2.imshow("fanzhuan", thresh1)  # \\反转
    contours, hierarchy = cv2.findContours(thresh1 , cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cent in contours:
        epsilon=0.001*cv2.arcLength(cent,True)
        approx=cv2.approxPolyDP(cent,epsilon,True)
        res_=cv2.drawContours(a,[approx],-1,(0,0,255),2)

        # if len(approx)>25:#30
        if len(approx) >len_:  # 30
            li1 = []
            x, y, w, h = cv2.boundingRect(cent)
            li1.append(x)
            li1.append(y)
            li1.append(w)
            li1.append(h)
            li2.append(li1)
            cv2.rectangle(dd, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # cv2.imshow("huakuang",dd)

    for f in li2:
        for d in li2:
            if d!=f:
                zx = abs(f[0] + f[0]+f[2] - d[0] - d[0]-d[2])
                x = abs(f[2]) + abs(d[2])
                zy = abs(f[1] + f[1]+f[3] - d[1] - d[1]-d[3])
                y = abs(f[3]) + abs(d[3])
                if zx <= x and zy <= y:
                    if f not in li3:
                        li3.append(f)

    for n in li3:
        li2.remove(n)#防止方框交叉
    for i in li2:
        g = {}
         # cv2.rectangle(b, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(b, (i[0], i[1]), (i[0] + i[2], i[1] + i[3]), (0, 0, 255), 2)
        g["regionX"]=i[0]
        g["regionY"] = i[1]
        g["regionWidth"] = i[2]
        g["regionHeight"] =i[3]
        untested_objects.append(g)
    # print(untested_objects)
    # cv2.imshow("2",a)#\\\\\\\\\\\\\\\
    # cv2.imshow("3",b)#\\\\\\\\\\\\\\\\\
# scanner(3,1,25)
# m, n = contrast(l2[3], untested_objects)
# print(m)
# print(n)
# print("-------------")
#
# with open("C:\\Users\\周银\\Desktop\\3.txt","w") as w:
#     for iteration in range(5):
#         for lens in range(11):
#             w.writelines(f"参数-->iteration:{1+iteration}, len:{20+lens}"+'\n')
#             # print(f"参数-->iteration:{1+iteration}, len:{20+lens}")
#             for i in range(5):
#                 scanner(i,1+iteration,20+lens)
#                 m, n = contrast(l2[i], untested_objects)
#                 untested_objects.clear()
#                 li2.clear()
#                 li3.clear()
#                 if m<0.25 or n<0.25:
#                     w.write("查全率或查准率过低！该参数不适用xxxxxxxxxxxxxxxxx"+'\n')
#                     break
#                 else:
#                     w.writelines(f"第{i}张图片识别率如下："+'\n')
#                     w.writelines(f"查全率：{m}"+'\n')
#                     w.writelines(f"查准率:{n}"+'\n')
#             w.writelines("-------------"+'\n')

            #     print(f"第{i}张图片识别率如下：")
            #     print(f"查全率：{m}")
            #     print(f"查准率:{n}")
            # print("-------------")

with open("C:\\Users\\周银\\Desktop\\4.txt","w") as w:
    for i in range(19):
        w.writelines(f"参数-->iteration:{1}, len:{25} +膨胀:{i+1}+ '\n'")
        for j in range(5):
                scanner(j,1,25,i+1)
                m, n = contrast(l2[j], untested_objects)
                untested_objects.clear()
                li2.clear()
                li3.clear()
                if m<0.25 or n<0.25:
                    w.write("查全率或查准率过低！该参数不适用xxxxxxxxxxxxxxxxx"+'\n')
                    break
                else:
                    w.writelines(f"第{j}张图片识别率如下："+'\n')
                    w.writelines(f"查全率：{m}"+'\n')
                    w.writelines(f"查准率:{n}"+'\n')
        w.writelines("-------------"+'\n')

#     print(f"第{i}张图片识别率如下：")
#     print(f"查全率：{m}")
#     print(f"查准率:{n}")
# print("-------------")



cv2.waitKey(1000000)
cv2.destroyAllWindows()