"""
Created on Mon Dec  5 15:21:34 2022

@author: Amir Hamza

"""

import cv2
import numpy as np

def LoadImage(path,gray=False):
    try:
        global img
        if gray==True:
            img=cv2.imread(path,0)

        else:
            img=cv2.imread(path)
        if img is not None:
            return img
        else:
            print('Error! The image could not be loaded. Incorrect path or blank image!')
    except:
        print('PackageError: Neccessary package(s) are not installed. Install OpenCv.')
def PseudoImage(img):
    black = np.zeros(img.shape,np.uint8)
    return black

def Denoise(img,kernel=(3,3),channels=0):
    try:
        blur = cv2.GaussianBlur(img,kernel,channels)
        return blur
    except:
        print('Error! Incorrect kernel: \n1. Use odd values for kernel. \n2. Try a different kernel size.')

def ClassifySurface(img_gray,threshold,invert_color=True):
    global thresh
    if invert_color == True:
        ret,thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY_INV)
    else:
        ret,thresh = cv2.threshold(img,threshold,255,cv2.THRESH_BINARY)
    return thresh

def FindContours(classified_img):
    contours, hierarchy= cv2.findContours(classified_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    return contours,hierarchy

def SignificantContours(classified_img):
    contours, hierarchy= cv2.findContours(classified_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    significant_contours=[]
    area_total= classified_img.shape[0] * classified_img.shape[1]

    for i in contours:
        area = cv2.contourArea(i)
        if area ==0 or area >= area_total:
            pass
        else:
            significant_contours.append(i)
    return significant_contours,hierarchy

def DrawContours(img,contours,index=-1,color = (0,255,0),thickness=1):
    cv2.drawContours(img,contours,index,color,thickness)
    return img
def ContourArea(classified_img,sum=False,scale_factor=None ):
    pore_area=[]
    area_total= classified_img.shape[0] * classified_img.shape[1]
    contours, hierarchy= cv2.findContours(classified_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for i in contours:
        area = cv2.contourArea(i)
        if area ==0 or area >= area_total:
            pass
        else:
            if scale_factor is None:
                pore_area.append(area)
            else:
                pore_area.append(area/scale_factor)
    if sum == False:
         return pore_area
    else:
         return sum(pore_area)

def EquivalentDiameter(contours,scale_factor=1):
    equivalent_dia = []
    for i in contours:
        (x,y),radius = cv2.minEnclosingCircle(i)
        dia = radius*2/scale_factor
        equivalent_dia.append(dia)
        return equivalent_dia

def DrawCircles(img,contours,color=(0,255,0),thickness=1):
    for i in contours:
        (x,y),radius = cv2.minEnclosingCircle(i)
        center = (int(x),int(y))
        radius_int = int(radius)
        cv2.circle(img,center,radius_int,color,thickness)
    return img

def SurfacePorosity(img,contour_area):
    area_total = img.shape[0] * img.shape[1]
    porosity = contour_area/area_total*100
    return porosity


def DefineScale(height,width):
    dim = img.shape
    scale_factor = ((dim[0]/height) + (dim[1]/width)  )/2
    return scale_factor

