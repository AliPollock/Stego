"""
StegoInterface.py
@authors: Group H

contains functions that provide a text interface to AssignmentReader.py
and AssignmentWriter.py, allowing a user to read and write stegoimages
without access to the underlying code
"""

import AssignmentWriter
import AssignmentReader

"""
prints a standard 'string not recognized' message to the screen
exits to reduce code duplication when looping back during input
"""
def unrecognizedString(inputString):
    return("--Error: did not understand input: \'" + str(inputString) +
           "\'\n--returning to last choice\n----------------")
        

"""
initial user input function
asks for 'read' or 'write', and restarts if anything else is entered
"""
def beginInputLoop():
    readOrWrite = input("--Do you wish to read or write a stegoimage?" +
                        "\nread/write\n> ")
    readOrWrite = readOrWrite.lower()
    
    if readOrWrite == "read":
        readImage()
    elif readOrWrite == "write":
        writeImage()
    else:
        print(unrecognizedString(readOrWrite))
        beginInputLoop()
        

"""
function to modify input flow if user selects 'read' in beginInputLoop
"""
def readImage():
    print("--Read Image mode selected")
    imageInFolder = input("--Is the stegoimage file in the root folder?" +
          "\ny/n\n> ")
    imageInFolder = imageInFolder.lower()
    
    if imageInFolder == "y":
        openImage(True)
        pass
    elif imageInFolder == "n":
        exitProgram(0)
    else:
        print(unrecognizedString(imageInFolder))
        readImage()
        

"""
function to modify input flow if user selects 'write' in beginInputLoop()
"""
def writeImage():
    print("--Write Image mode selected")
    imageInFolder = input("--Is the base image file in the root folder?" +
          "\ny/n\n> ")
    imageInFolder = imageInFolder.lower()
    
    if imageInFolder == "y":
        openImage(False)
        pass
    elif imageInFolder == "n":
        exitProgram(0)
    else:
        print(unrecognizedString(imageInFolder))
        writeImage()
        

"""
attempts to load an image from the given filename
will restart if filename is not recognized/image not loaded
will send loaded image to insert or extract message based on bool 'isRead'
"""
def openImage(isRead):
    imageToOpen = input("--Please enter the filename, including extension" +
                "\n--e.g. /'ImageFile.bmp'\n>")
    try:
        importedBMP = AssignmentWriter.importBMP(imageToOpen)
        
        if importedBMP == None:
            unrecognizedString(imageToOpen)
            openImage(isRead)
        elif importedBMP.mode != 'RGB':
            exitProgram(6)
        elif isRead == True:
            extractMessage(importedBMP)
        elif isRead == False:
            insertMessage(importedBMP)
            
    except:
        exitProgram(1)


"""
extracts a hidden message from a specified stegoimage
"""
def extractMessage(image):
    print("\n--Stegoimage loaded")
    msgLength = AssignmentReader.extractMessageLengthFromImage(image)
    binaryMsg = AssignmentReader.extractMessageFromImage(image, msgLength)
    returnString = AssignmentReader.binaryToOutput(binaryMsg)
    
    presentMessage(returnString)
    

"""
presents the message returned from extractMessage() and terminates program
"""
def presentMessage(returnedString):
    print("--Hidden Message extracted successfully:\n")
    print("\t" + str(returnedString))    
    exitProgram(3)
    

"""
requests an hidden message to be added to the given image file
will also ask for a filename for the output stegoimage
terminates the program on success
"""
def insertMessage(importedIMG):
    print("--Payload image loaded")
    message = input("--Enter a secret message:\n\>")
    outputFile = input("--Please enter a filename for the stegoimage" +
                       "\n--e.g. /'StegoFile.bmp'\n>")
    print("--Attempting to insert message via LSB")
    
    try:
        binaryMessage = AssignmentWriter.userInputToBinary(message)
        print("...")
        image = importedIMG
        binaryMessageLength = AssignmentWriter.findBinaryMessageLength(binaryMessage)
        
        if AssignmentWriter.checkImageFitsMessage(binaryMessageLength, image) == False:
            exitProgram(5)

        else:
            AssignmentWriter.insertMessageIntoImage(binaryMessage, image)
            print("...")
            AssignmentWriter.insertMessageLengthIntoImage(binaryMessageLength, image)
            print("... writing to file: " + str(outputFile))
            image.save(outputFile)
            image.close()
            exitProgram(4)
    
    except:
        exitProgram(2)


"""
prints out an exit message to the user when terminating program
specific message is dictated by a condition code
"""
def exitProgram(conditionCode):
    if conditionCode == 0:
        print("\n--Target file must be located in the program folder" +
              "\n--please place the image in the folder and start again")
        
    elif conditionCode == 1:
        print("\n--Error: Image file could not be opened" +
              "\n--please check file details and try again")
    
    elif conditionCode == 2:
        print("\n--Error: Image file could not be created" +
              "n--please check folder rights and try again")
        
    elif conditionCode == 3:
        print("\n--End of Hidden Message")
    
    elif conditionCode == 4:
        print("\n\t--Secret Message successfully inserted into file!")
        
    elif conditionCode == 5:
        print("\n--Error: Image is not large enough for the entered message" +
              "\n--please retry with a larger image or shorter message")
    
    elif conditionCode == 6:
        print("\n--Error: Image is a BMP, but not 24-bit true-colour" +
              "\n--please retry with a true-colour image")
        
    print("\n\t--Program Terminated--")


"""
main function - simply prints a title and kicks off the input loop
"""
if __name__ in "__main__":
    print("--LSB Steganography package for CS808" +
          "\n--Authors: Group H (A.P. and A.J.)")
    beginInputLoop()
