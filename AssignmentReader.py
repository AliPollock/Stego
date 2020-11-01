"""
AssignmentReader.py
@authors: Group H

contains functions for reading stegoimages created by AssignmentWriter.py
"""
from PIL import Image


"""
A function that determines the integer length of a given binary message
"""
def findBinaryMessageLength(binaryMessage):
    messageLength = 0
    for i in binaryMessage:
        messageLength +=1
        
    return messageLength

"""
A function that converts a given binary sequence to a readable String
"""
def binaryToOutput(binaryMessage):
    message = ''
    
    #convert message length to bytes for string conversion
    numberOfBytes = int(findBinaryMessageLength(binaryMessage)/8)
    for i in range(numberOfBytes):
        byte = binaryMessage[8*i:8*i+8]
        message += chr(int(byte, 2))
        
    return message


"""
A function to open and return a local bitmap image as a PIL Image
"""
def importBMP(filename, formats = "bmp"):
    try:  
        BMPImage = Image.open(filename)
        print("image loaded")
        #if file gets past "formats=", import it, but display warning
        if BMPImage.format != "BMP":
            print("\n---WARNING---\nimage file may not be compatible\n")
        return BMPImage
            
    except:
        #throw generic i/o error
        print("error importing file data")


"""
A function that extracts the length of a secret message hidden within
the given stegoimage
"""
def extractMessageLengthFromImage(image):
    #load PixelAccess object for given image
    imageData= image.load()
    
    y = 0
    messageLengthBinary = ''
    #parse given range of first row of pixels for length value
    for x in range(70,79):
        #pull pixel as an RGB list using PixelAccess
        pixel = list(imageData[x, y])
        
        for colour in pixel:
            binaryColour = "{0:b}".format((colour)).zfill(8)
            messageLengthCharacter = binaryColour[7:]
            messageLengthBinary+=messageLengthCharacter
    messageLengthInt = int(messageLengthBinary, 2)
    
    return messageLengthInt


"""
A function that extracts a secret message of the given length
from a given stegoimage
"""
def extractMessageFromImage(image, messageLength):
    #load pixelaccess object for given image
    imageData= image.load()
    
    #begin iteration after message length binary
    i = 100
    j = 0
    messageBinary = ''
    #parse each row of pixels in turn
    for y in range(image.height):
        for x in range(i, image.width):
            pixel = list(imageData[x, y])
            # print(f"x:{x}, y: {y} message pixel is: {imageData[x,y]}")
            for colour in pixel:
                binaryColour = "{0:b}".format((colour)).zfill(8)
                messageCharacter = binaryColour[7:]
                messageBinary+=messageCharacter
                j+=1
                
                #return after parsing for messageLength
                if j == messageLength:
                    return messageBinary               
        #reset i to 0 after first pixel row
        i = 0


"""
Main function for testing purposes
"""
if __name__ == "__main__":

    image = importBMP("Images/stegoimage.bmp")
    messageLength = extractMessageLengthFromImage(image)
    binaryMessage = extractMessageFromImage(image, messageLength)
    binaryToOutput(binaryMessage)