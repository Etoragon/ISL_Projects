from PIL import Image
import cv2
import numpy as np
from scipy.ndimage import grey_opening
import math
from matplotlib import pyplot as plt

def getMaxPixels(im):
    pixelMaxes = []
    for x in range(im.size[0]):
        pixelMaxes.append([])
        for y in range(im.size[1]):
            pixel = im.getpixel((x,y))
            maxPixel = math.sqrt(pixel[0]**2 + pixel[1]**2 + pixel[2]**2)
            pixelMaxes[x].append(maxPixel)
    return pixelMaxes


def getOverallAverage(maxPixels):
    total = []
    for x in range(len(maxPixels)):
        for y in range(len(maxPixels[x])):
            total.append(maxPixels[x][y])

    return sum(total) / (len(maxPixels)*len(maxPixels[0]))

# xcor and ycor are location of central pixel
# fileMaxs are size of file
# search radius is the size of the circle around the center pixel for value calculation
# im is an Image.open(..) object
def getAverageLine(xcor, ycor, fileMaxX, fileMaxY, searchRadius, pixelMaxes, overallAverage, test):
    xLow = 0
    xHigh = fileMaxX
    yLow = 0
    yHigh = fileMaxY
#    if xcor - searchRadius > 0:
#        xLow = xcor - searchRadius
#    if xcor + searchRadius < fileMaxX:
#        xHigh = xcor + searchRadius
#    if ycor - searchRadius > 0:
#        yLow = ycor - searchRadius
#    if ycor + searchRadius < fileMaxY:
#        yHigh = ycor + searchRadius

    averageList = []

    # Obtains and saves list of all maxes per line
    for x in range(xLow, xHigh):
        averageList.append(pixelMaxes[x][ycor])

    comparative = (sum(averageList)/len(averageList))/overallAverage - 1
    
    return sum(averageList)/len(averageList) + comparative*(5*test)


def main(inputFilePath, outputFilePath):
    for abc in range(10):
        # Initialize file paths
        hazyImagePath = inputFilePath
        finishedImagePath1 = outputFilePath

        # Open first first using Image class from PIL
        im = Image.open(hazyImagePath)


        # Initialize original photo to reference throughout code
        sizeX = im.size[0]
        sizeY = im.size[1]

        print("Size of image (x,y): ("+str(sizeX)+","+str(sizeY)+")")

        # Initialize new Image instance to place Veil(DC) pixels in as well as
        # a list for easier access
        imVeil = Image.new("RGB", im.size)
        finishedList = []

        pixelMaxes = getMaxPixels(im)
        overallAverage = getOverallAverage(pixelMaxes)

        # Goes through each pixel, applies an equation found in the paper "Fast_single..."
        for y in range(sizeY):
            atmosphericLightLevel = getAverageLine(0, y, sizeX-1, sizeY-1, 2, pixelMaxes, overallAverage, abc) * .9
            for x in range(sizeX):
                pixelValues = im.getpixel((x, y))
                rPixel, gPixel, bPixel = 0, 0, 0
                pixelFinal = []
            
                # Equation here #
                extinctionCoefficient = -0.4 # Random value based on data
                distanceFromCamToPixel = 6 # Tbh, absolutely random variable
                for key, channel in enumerate(pixelValues):
                    temp = (float(channel) - atmosphericLightLevel * (1 - (math.exp(( extinctionCoefficient )*( distanceFromCamToPixel )))))/(math.exp(extinctionCoefficient*( distanceFromCamToPixel )))
                    pixelFinal.append(temp)
                imVeil.putpixel((x, y),(math.floor(pixelFinal[0]), math.floor(pixelFinal[1]), math.floor(pixelFinal[2])))

        # Saves new Veiled image
        imVeil.save(finishedImagePath1)
        imVeil.show()

inputFilePath = r"C:/Users/Eppat/Documents/College/UNCFSU/ISL Research/usdc7/img1620761217183008909.jpg"
outputFilePath = r"C:\Users\Eppat\Documents\College\UNCFSU\ISL Research\usdc7\testRealImageOutput4.jpg"
main(inputFilePath, outputFilePath)


