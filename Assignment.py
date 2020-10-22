from PIL import Image

""" message functions to switch between string and binary, and count the length of the binary message"""

def findBinaryMessageLength(binaryMessage):
    messageLength = 0
    for i in binaryMessage:
        messageLength +=1
    return messageLength

def userInputToBinary(message): # can't handle & or ( )
    binaryMessage = ''
    for i in message:
        binaryMessage += "{0:b}".format(ord(i)).zfill(8) # converting to binary zfill gives 0 on the left because format only gives a 7 digit binary value and misses the 0 at the begining
    print(binaryMessage)
    return binaryMessage

def binaryToOutput(binaryMessage):
    message = ''
    numberOfBytes = int(findBinaryMessageLength(binaryMessage)/8)
    for i in range(numberOfBytes):
        byte = binaryMessage[8*i:8*i+8]
        message += chr(int(byte, 2))
        print(message)
    return message


""" function to take in image and convert to binary array"""

def importImage(image):
    imageBytes = []
    with Image.open(image) as image:
        print(image)
        print(type(image))
        imageBytes = list(image.getdata()) # pixels as a list of tuples
        # imagebytes = bytes(image.tobytes())
    return imageBytes


"""functions to put message into image array and insert message length into image array"""

def insertMessageIntoImage(binaryMessage, imageBytes):
    messageLength = findBinaryMessageLength(binaryMessage)
    for i in range(100, messageLength + 100): # start at index 100 to ensure we don't change the
        j = 3*(i - 100) # this keeps track of the position in the actual message
        pixel = list(imageBytes[i])  # converting tuple into list
        pixelList = []
        for colour in pixel:
            if j == messageLength:
                return imageBytes
            messageCharacter = binaryMessage[j]
            binaryColour = "{0:b}".format((colour)).zfill(8)
            binaryColour = binaryColour[:-1] # removes LSB from colour byte
            binaryColour += messageCharacter # adds message character in place of LSB
            #need line that converts binary back into ints
            pixelList.append(binaryColour) # this will hold the new pixel data
            j += 1 # each pass, j must increase by 1 so that binaryMessage[j] can move down the message
        imageBytes[i] = tuple(pixelList) #swapping old pixel in for new one
        del pixelList[:]
    return imageBytes # this may be obselete


def insertMessageLengthIntoImage(messageLength, imageBytes):
    binaryMessageLength = "{0:b}".format((messageLength)).zfill(26)
    print(binaryMessageLength)
    for i in range(70, 79): # will encode length of message starting at byte no. 70 and extending 26 characters long padded on the left with zeros this corresponds to 8 pixels
        j = 3*(i - 70)
        messageLengthCharacter = binaryMessageLength[j]
        pixel = list(imageBytes[i])  # converting tuple into list
        pixelList = []
        for colour in pixel:
            binaryColour = "{0:b}".format((colour)).zfill(8)
            binaryColour = binaryColour[:-1]
            binaryColour += messageLengthCharacter
            #line need that converts binary back into int
            pixelList.append(binaryColour)
            j += 1
        imageBytes[i] = tuple(pixelList)
        del pixelList[:]
    return imageBytes


"""function to output image"""

def returnToImage(binaryImage):
    # binaryImage.tobitmap()
    # stegoImage = Image.new(img.bmp, img.size)
    # stego = Image.fromarray(binaryImage, "RGB")
    stegoImage = Image.frombuffer("RGB",(3974, 4968),binaryImage,"raw")
    print(stegoImage)


"""functions to extract string from Image"""


if __name__ == "__main__":
    message = input("Enter a secret message: ")
    binaryMessage = userInputToBinary(message)
    binaryMessageLength = findBinaryMessageLength(binaryMessage)
    # messageOut = binaryToOutput(binaryMessage)

    imageBytes = importImage("Images/unsplash.bmp")
    editedImageBytes = insertMessageIntoImage(binaryMessage, imageBytes)
    stegoObject = insertMessageLengthIntoImage(binaryMessageLength, editedImageBytes)
    # stegoImage = returnToImage(stegoObject)