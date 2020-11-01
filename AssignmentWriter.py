"""
AssignmentWriter.py
@authors: Group H

contains functions for reading images and creating new stegoimages
"""

from PIL import Image

"""
A function to convert a given text string to binary
"""
def userInputToBinary(message):
    binaryMessage = ''
    for i in message:
        binaryMessage += "{0:b}".format(ord(i)).zfill(8)

    return binaryMessage


"""
A function that finds the length of a given binary message
"""
def findBinaryMessageLength(binaryMessage):
    messageLength = 0
    for i in binaryMessage:
        messageLength +=1
        
    return messageLength


"""
A function to confirm if a given image file has sufficient pixels for
a binary message to be inserted using LSB
"""
def checkImageFitsMessage(binaryMessageLength, image):
    #remove 100 bits to account for the message length
    numBitsAvailable = image.height*image.width - 100
    if binaryMessageLength <= numBitsAvailable:
        return True
    
    return False


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
A function that inserts the given binary message into the RGB values of
the pixels within the given Image file using LSB
Returns the resulting stegoimage
"""
def insertMessageIntoImage(binaryMessage, image):
    #load PixelAccess object for given image
    imageData = image.load()
    messageLength = findBinaryMessageLength(binaryMessage)
    
    #begin iteration after message length binary
    i=100
    #bit counter
    j = 0
    #parse each row of pixels in turn
    for y in range(image.height):
        for x in range (i, image.width):
            #pull pixel as an RGB list using PixelAccess
            pixel = list(imageData[x, y])
            pixelList = []
            
            for colour in pixel:
                messageCharacter = binaryMessage[j]
                binaryColour = "{0:b}".format((colour)).zfill(8)
                binaryColour = binaryColour[:-1]
                
                #add current message bit
                binaryColour += messageCharacter
                intColour = int(binaryColour, 2)
                #add modified colour to temporary pixel list
                pixelList.append(intColour)
                j += 1
                
                #check if current bit is the last in the message
                if j == messageLength:
                    #return stegoimage if last bit is a full pixel
                    if j%3 == 0:
                        pixelTuple = tuple(pixelList)
                        image.putpixel((x, y), pixelTuple)
                        return
                    
                    #pad 2 bits if not a complete pixel and return stegoimage
                    elif j%3 == 1:
                        pixelList.extend((pixel[1], pixel[2]))
                        pixelTuple = tuple(pixelList)
                        image.putpixel((x, y), pixelTuple)
                        return
                    
                    #pad 1 bit if not a complete pixel and return stegoimage
                    else:
                        pixelList.append(pixel[2])
                        pixelTuple = tuple(pixelList)
                        image.putpixel((x, y), pixelTuple)
                        return
                    
            #after 3 inserted bits, cast temporary pixel list as a tuple
            pixelTuple = tuple(pixelList)
            #insert edited pixel back into image
            image.putpixel((x, y), pixelTuple)
            del pixelList[:]
            
        #reset i to 0 after first pixel row
        i=0 
        
    #return error string if there was an error
    return f"an error has occured when entering text into image"


"""
A function that inserts the length of a secret message into - and returns -
the given image in perparation for the actual insertion of the message
"""
def insertMessageLengthIntoImage(messageLength, image):
    #load PixelAccess object for given image
    imageData = image.load()
    
    #use 27 bits to encode message length into image
    binaryMessageLength = "{0:b}".format((messageLength)).zfill(27)
    
    y = 0
    j = 0
    
    #parse given range of first row of pixels in the image
    for x in range(70,79):
        #pull pixel as an RGB list using PixelAccess
        pixel = list(imageData[x, y])
        pixelList = []
        
        for colour in pixel:
            messageLengthCharacter = binaryMessageLength[j]
            binaryColour = "{0:b}".format((colour)).zfill(8)
            binaryColour = binaryColour[:-1]
            binaryColour += messageLengthCharacter
            intColour = int(binaryColour, 2)
            pixelList.append(intColour)
            j += 1
            
        #after 3 inserted bits, cast temporary pixel list as a tuple
        pixelTuple = tuple(pixelList)
        #insert edited pixel back into image
        image.putpixel((x, y), pixelTuple)
        del pixelList[:]
        
    return image


"""
Main function for testing purposes
"""
if __name__ == "__main__":

    message = input("Enter a secret message: ")
    binaryMessage = userInputToBinary(message)
    image = importBMP("Images/unsplash.bmp")
    binaryMessageLength = findBinaryMessageLength(binaryMessage)
    
    checkImageFitsMessage(binaryMessageLength, image)
    
    insertMessageIntoImage(binaryMessage, image)
    insertMessageLengthIntoImage(binaryMessageLength, image)
    image.save("Images/stegoimage.bmp")
    image.close()
    print("message has been inserted into image and written to a new stegoImage")

