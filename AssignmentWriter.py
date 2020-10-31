from PIL import Image

""" message functions to switch between string and binary, and count the length of the binary message"""

def userInputToBinary(message): # can't handle & or ( ) need some erro handling for input here
    binaryMessage = ''
    for i in message:
        binaryMessage += "{0:b}".format(ord(i)).zfill(8) # converting to binary zfill gives 0 on the left because format only gives a 7 digit binary value and misses the 0 at the begining
    print(f"'{message}' has been converted to {binaryMessage}")
    return binaryMessage

def findBinaryMessageLength(binaryMessage):
    messageLength = 0
    for i in binaryMessage:
        messageLength +=1
    return messageLength

def checkImageFitsMessage(binaryMessageLength, image):
    numBitsAvailable = image.height*image.width - 100
    if binaryMessageLength <= numBitsAvailable:
        return True
    return False


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


"""functions to put message into image array and insert message length into image array"""

def insertMessageIntoImage(binaryMessage, image):
    imageData = image.load() # creating pixel access object
    messageLength = findBinaryMessageLength(binaryMessage)
    i=100 # this is a pixel indent to make the programme only start the iteration at pixel 100
    j = 0 #this will be the counter for what character in our message we are currently on
    for y in range(image.height):
        for x in range (i, image.width):
            pixel = list(imageData[x, y])
            pixelList = [] # this will be the new container for ammended pixel data
            for colour in pixel:
                messageCharacter = binaryMessage[j]
                binaryColour = "{0:b}".format((colour)).zfill(8)
                binaryColour = binaryColour[:-1] # removes LSB from colour byte
                binaryColour += messageCharacter # adds message character in place of LSB
                intColour = int(binaryColour, 2)
                pixelList.append(intColour) # this will hold the new pixel data
                j += 1 # each pass, j must increase by 1 so that binaryMessage[j] can move down the message
                
                if j == messageLength: # statements to break out of the loop once the last character of the message has been entered
                    if j%3 == 0:
                        pixelTuple = tuple(pixelList) # converting back into tuple
                        image.putpixel((x, y), pixelTuple) # adding into image
                        return
                    
                    elif j%3 == 1: # case if there are two empty colours in current pixel when message ends 
                        pixelList.extend((pixel[1], pixel[2]))
                        pixelTuple = tuple(pixelList)
                        image.putpixel((x, y), pixelTuple)
                        return
                    
                    else: # case if there is one empty colour in current pixel when message ends
                        pixelList.append(pixel[2])
                        pixelTuple = tuple(pixelList)
                        image.putpixel((x, y), pixelTuple)
                        return

            pixelTuple = tuple(pixelList)
            image.putpixel((x, y), pixelTuple)
            # print(f"pixel {x}: {pixel} was written to {pixelList}")
            del pixelList[:]
        i=0 # this sets the pixel indent back to zero after the first  row of pixels is passed
    return f"an error has occured when entering text into image"


def insertMessageLengthIntoImage(messageLength, image):
    imageData = image.load()
    binaryMessageLength = "{0:b}".format((messageLength)).zfill(27) #27 because the maximum value that the photo can hold is 26 digits long and 27 makes 9 full pixels
    y = 0
    j = 0
    print(f" length of {messageLength} is {binaryMessageLength}")
    for x in range(70,79):
        pixel = list(imageData[x, y])  # converting tuple into list
        pixelList = []
        for colour in pixel:
            messageLengthCharacter = binaryMessageLength[j]
            binaryColour = "{0:b}".format((colour)).zfill(8)
            binaryColour = binaryColour[:-1]
            binaryColour += messageLengthCharacter
            intColour = int(binaryColour, 2)
            pixelList.append(intColour)
            j += 1
        pixelTuple = tuple(pixelList)
        image.putpixel((x, y), pixelTuple)
        # print(f" pixel {x}: {pixel} was changed to {pixelList}")
        del pixelList[:]
    return image


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

