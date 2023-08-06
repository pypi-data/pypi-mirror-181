import sys
import cv2
import os
lib_path = (os.path.split(os.path.realpath(__file__))[0])
sys.path.append(lib_path)
from My_CV import *
# -*- coding utf-8 -*-
"""
Created on Sept 2th 09:41 2020

@auther: Peiqi Miao

"""
def find_C_only(cnts,level):
    c = find_c_only(cnts,level)
    return c

def find_Mask_points(img, c):
    mask_pic, pts = find_mask_points(img, c)
    return mask_pic,pts

##########基于灰度图像的梯度共生矩阵###################
'''根据灰度梯度共生矩阵计算纹理特征量，包括小梯度优势，大梯度优势，灰度分布不均匀性，梯度分布不均匀性，能量，灰度平均，梯度平均，
    灰度方差，梯度方差，相关，灰度熵，梯度熵，混合熵，惯性，逆差矩'''
def get_Glgcm(img_gray, ngrad=16, ngray=16):
    glgcm_features = glgcm(img_gray, ngrad, ngray)
    return glgcm_features
#########color moments(CMs)###################
def get_Color_moments_array(array):
    color_feature = get_color_moments_array(array)
    return color_feature
# Compute low order moments(1,2,3)
def get_Color_moments(img):
    ####img为BGR格式,用opencv打开即可，或readPic（）方法
    color_feature = color_moments(img)
    return color_feature
#########color moments(CMs)###################

def cutPic(pic,gre_thre,kernel,thre1,thre2):
    #gre_thre[0,255],kernel卷积核大小，thre1缩小程度，扩大程度
    new_pic = cut_pic(pic,gre_thre,kernel,thre1,thre2)
    return new_pic

def readPic(name):
    img = read_pic(name)
    return img

def readGraypic(name):
    img = readPic(name)
    gray_pic = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray_pic

def showName(name,dely):
    img = cv2.imread(name)
    cv2.namedWindow('show',0)
    cv2.imshow('show', img)
    cv2.waitKey(dely)

def show_img(img,dely):
    cv2.namedWindow('show',0)
    cv2.imshow('show', img)
    cv2.waitKey(dely)

def mkDir(path):
    mkdir(path)

def rot90(img):
    img90 = rot_90(img)
    return img90

def warpMinirect(rect,img):
    warped = warp_minirect(rect,img)
    return warped

def xintaiArg(c):
    a1_w, a1_h, area, baohedu1, match_k = xintai_arg(c)
    return a1_w, a1_h, area, baohedu1, match_k

def give_day_name():
    name = datetime.datetime.now().strftime('%Y%m%d')
    print(name)
    return name

def give_name():
    name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    return name

def preProcessing(frame,gray_thre = 100,kernel = 10,iter1=1,iter2 = 1):
    dst = pre_processing(frame,gray_thre,kernel,iter1,iter2)
    return dst

def find_cMax(cnts):
    c = find_c_max(cnts)
    return c

def findCnts(bin_img):
    cnts = find_cnts(bin_img)
    return cnts

def drawCnts(src,cnts):
    src = draw_cnts(src,cnts)
    return src

def minRect(c):
    rect = min_rect(c)
    return rect

def drawRect(frame,rect):
    frame = draw_rect(frame,rect)
    return frame
def drawCircle(img,center,r,color,thickness,txt_key=1,index=1):
    img = draw_circle(img,center,r,color,thickness,txt_key,index)
    return  img
def matchC(c1,c2):
    retval = match_c(c1,c2)
    return retval
def concatPic1(img):
    img_01 = concat_pic1(img)
    return img_01

def concatPic2(img, axis):
    img_02 = concat_pic2(img, axis)
    return img_02

def concatPic3(img):
    img_03 = concat_pic3(img)
    return img_03

def tiaoZheng(img_list):
    out = tiaozheng(img_list)
    return out

def tiaoZheng234(img_list):
    out = tiaozheng234(img_list)
    return out

def getGray(img1,channal):
    get_Gray(img1, channal)

if __name__ == '__main__':
    showName('./test2.jpg',0)
    img = readGraypic('./test2.jpg')
    img = drawCircle(img,(100,100),30,255,-1,txt_key=0)
    show_img(img,0)
    # CMs = get_Color_oments(img)
    # print(CMs)
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # new_pic = cut_pic(img,100,10,1,1)
    # show_img(new_pic,0)
    # glgcm = get_Glgcm(img)
    # print(glgcm)

