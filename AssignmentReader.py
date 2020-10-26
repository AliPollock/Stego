from PIL import Image


"""functions to read change binary message into text and print to command line"""

def findBinaryMessageLength(binaryMessage):
    messageLength = 0
    for i in binaryMessage:
        messageLength +=1
    return messageLength

def binaryToOutput(binaryMessage):
    message = ''
    numberOfBytes = int(findBinaryMessageLength(binaryMessage)/8)
    for i in range(numberOfBytes):
        byte = binaryMessage[8*i:8*i+8]
        message += chr(int(byte, 2))
    print(f"the message hidden in the image is: '{message}'")
    return message



""" function to take in image and convert to binary array"""

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


""" functions to extract message length and to extract message"""

def extractMessageLengthFromImage(image):
    imageData= image.load()
    y = 0
    j = 0
    messageLengthBinary = ''
    for x in range(70,79):
        pixel = list(imageData[x, y])
        # print(f"{x} pixel is: {pixel}")
        for colour in pixel:
            binaryColour = "{0:b}".format((colour)).zfill(8)
            messageLengthCharacter = binaryColour[7:]
            messageLengthBinary+=messageLengthCharacter
    print(f"message length in binary is {messageLengthBinary}")
    messageLengthInt = int(messageLengthBinary, 2)
    print(f"message length int is {messageLengthInt}")
    return messageLengthInt


def extractMessageFromImage(image, messageLength):
    imageData= image.load()
    i = 100
    j = 0
    messageBinary = ''
    for y in range(image.height):
        for x in range(i, image.width):
            pixel = list(imageData[x, y])
            # print(f"x:{x}, y: {y} message pixel is: {imageData[x,y]}")
            for colour in pixel:
                binaryColour = "{0:b}".format((colour)).zfill(8)
                messageCharacter = binaryColour[7:]
                messageBinary+=messageCharacter
                j+=1
                # print(messageLength)
                # print(j)
                if j == messageLength:
                    print(f"message in binary is {messageBinary}")
                    return messageBinary
        i = 0 # this is to set the indent back to zero after the first row (y=0)








if __name__ == "__main__":


    image = importBMP("Images/stegoimage.bmp")
    messageLength = extractMessageLengthFromImage(image)
    binaryMessage = extractMessageFromImage(image, messageLength)
    binaryToOutput(binaryMessage)