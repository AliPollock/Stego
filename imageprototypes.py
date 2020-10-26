# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:14:28 2020

@author: Andrew
"""

from PIL import Image

def importBMP(filename, formats = "bmp"):
    #TODO: add try block after debugging
   
    BMPImage = Image.open(filename)
    return BMPImage

"""    
def convertToJPG(imageFile):
    if infile != outfile:"""
    
if __name__ in "__main__":
    #loads a 2x2 red test image
    testIMG = importBMP("redsquare.bmp")
    print("imported: " + testIMG.filename)
    print("format is: " + str(testIMG.format))
    print("image size is: " + str(testIMG.size))
    print("image mode is: " + str(testIMG.mode))
    print("image info is: " + str(testIMG.info))
    
    #convert Image to PixelAccess object
    imageData = testIMG.load()
    
    #output a visible grid of pixels
    print("\npixel by pixel data:\n----------------------")
    for y in range(testIMG.height):
        pixelLine = ""
        for x in range(testIMG.width):
            pixelLine += ("[" + str(y) + "x" +
                          str(x) + str(imageData[x, y]) + "]   ")
        print(pixelLine + "\n")
    
    #modify the pixel data
    print("\nchange pixel colour:\n----------------------")
    
    #define an amount to decriment the pixels by
    decAmount = 150
    print("reducing red pixel\nbrightness by: " + str(decAmount) + "\n")
    
    for y in range(testIMG.height):
        for x in range(testIMG.width):
            #for each pixel, grap the tuple as a list
            colourList = list(imageData[x, y])
            #reduce the red value by the decriment amount 
            colourList[0] -= decAmount
            
            #convert back to tuple and apply the new pixel to the image
            colourTuple = tuple(colourList)
            testIMG.putpixel((x, y), colourTuple)
    
    #output the updated grid of pixels
    print("\nupdated pixel data:\n----------------------")
    for y in range(testIMG.height):
        pixelLine = ""
        for x in range(testIMG.width):
            pixelLine += ("[" + str(y) + "x" +
                          str(x) + str(imageData[x, y]) + "]   ")
        print(pixelLine + "\n")
    
    #write the image out using the save() function
    testIMG.save("updatedtestsquare.bmp")
