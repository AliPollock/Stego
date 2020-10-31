from PIL import Image
import unittest
import os
import sys
sys.path.insert(0, '../')
from AssignmentReader import findBinaryMessageLength, binaryToOutput, importBMP, extractMessageLengthFromImage, extractMessageFromImage
from AssignmentWriter import userInputToBinary, insertMessageIntoImage, insertMessageLengthIntoImage

class Test(unittest.TestCase):


    def test_findBinaryMessageLength(self):
        message1 = "testing"
        binaryMessage = userInputToBinary(message1)
        binaryLength = findBinaryMessageLength(binaryMessage)

        self.assertEqual(binaryLength, 56)

        message2 = "I am testing a long string with some strange characters(!@^7?) and spaces"
        binaryMessage2 = userInputToBinary(message2)
        binaryLength2 = findBinaryMessageLength(binaryMessage2)
        self.assertEqual(binaryLength2, 584)


    def test_binaryToOutput(self):
        message1 = "testing"
        messageOut1 = binaryToOutput("01110100011001010111001101110100011010010110111001100111")
        self.assertEqual(message1, messageOut1)

        message2 = "!@#$%^&*()_+-=<>?;:'\|}{]["
        messageOut2 = binaryToOutput("0010000101000000001000110010010000100101010111100010011000101010001010000010100101011111001010110010110100111101001111000011111000111111001110110011101000100111010111000111110001111101011110110101110101011011")
        self.assertEqual(message2, messageOut2)



    def test_importBMP(self):
        image = Image.new( 'RGB', (150,150), "blue") # creates test image of 150x150 blue square
        pixels = image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                pixels[i,j] = (0, 0, 255)
        image.save("blueSquare.bmp")

        imageimport = importBMP("blueSquare.bmp")
        imageData = image.load()
        imageimportData = imageimport.load()
        for y in range(image.height):
            for x in range(image.width):
                self.assertEqual(imageData[x,y], imageimportData[x,y])

        os.remove("blueSquare.bmp") # deletes the image after test


    def test_extractMessageLengthFromImage(self):
        message = "0"
        binaryMessage = userInputToBinary(message)
        binaryMessageLength = findBinaryMessageLength(binaryMessage) # this gives a value of 8 which is 000 000 000 000 000 000 000 001 000

        image = Image.new( 'RGB', (150,150), "white") # creates test image of 150x150 white square
        pixels = image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                pixels[i,j] = (255, 255, 255)

        insertMessageLengthIntoImage(binaryMessageLength, image)
        binaryMessageLengthOut = extractMessageLengthFromImage(image)

        self.assertEqual(binaryMessageLength, binaryMessageLengthOut)


    def test_extractMessageFromImage(self):
        message = "0"
        binaryMessage = userInputToBinary(message)
        binaryMessageLength = findBinaryMessageLength(binaryMessage)

        image = Image.new( 'RGB', (150,150), "black") # creates test image of 150x150 black square
        pixels = image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                pixels[i,j] = (0, 0, 0)

        insertMessageIntoImage(binaryMessage, image)
        insertMessageLengthIntoImage(binaryMessageLength, image)
        
        binaryMessageLengthOut = extractMessageLengthFromImage(image)
        binaryMessageOut = extractMessageFromImage(image, binaryMessageLengthOut)

        self.assertEqual(binaryMessage, binaryMessageOut)

if __name__ == "__main__":
    unittest.main()