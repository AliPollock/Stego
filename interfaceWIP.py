# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:57:50 2020

@author: Andrew
"""

def readImage():
    print("--Read Image mode selected")
    imageInFolder = input("--Is the image file in the root folder?" +
          "\ny/n\n> ")
    imageInFolder.lower()
    if imageInFolder == "y":
        #I/O nonsense
        pass
    elif imageInFolder == "n":
        exitProgram(0)
    else:
        print("--Error: did not understand input: \'" + str(imageInFolder) +
              "\'\n--returning to last choice\n----------------\n")
        readImage()

def exitProgram(conditionCode):
    if conditionCode == 0:
        print("\n--Target file must be located in the program folder" +
              "\n--please place the image in the folder and start again")
    elif conditionCode == 1:
        print("\n--Message inserted successfully!")

if __name__ in "__main__":
    print("--LSB Steganography package for CS808" +
          "\n--Authors: Group H (A.P. and A.J.)\n")
    readOrWrite = input("--Do you wish to read or write a stegoimage?" +
                        "\nread/write\n> ")
    readOrWrite.lower()
    if readOrWrite == "read":
        readImage()
    elif readOrWrite == "write":
        pass