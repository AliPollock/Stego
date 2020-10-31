import unittest
from PIL import Image
import os
import sys
sys.path.insert(0, '../')
from AssignmentWriter import userInputToBinary, findBinaryMessageLength, importBMP, insertMessageIntoImage, insertMessageLengthIntoImage

class TestFunctions(unittest.TestCase):

    def test_userInputToBinary(self):

        message1 = "testing"
        binaryMessage = userInputToBinary(message1)
        self.assertEqual(binaryMessage, "01110100011001010111001101110100011010010110111001100111")

        message2 = "!@#$%^&*()_+-=<>?;:'\|}{]["
        binaryMessage2 = userInputToBinary(message2)
        self.assertEqual(binaryMessage2, "0010000101000000001000110010010000100101010111100010011000101010001010000010100101011111001010110010110100111101001111000011111000111111001110110011101000100111010111000111110001111101011110110101110101011011")


    def test_findBinaryMessageLength(self):
        message1 = "testing"
        binaryMessage = userInputToBinary(message1)
        binaryLength = findBinaryMessageLength(binaryMessage)

        self.assertEqual(binaryLength, 56)

        message2 = "I am testing a long string with some strange characters(!@^7?) and spaces"
        binaryMessage2 = userInputToBinary(message2)
        binaryLength2 = findBinaryMessageLength(binaryMessage2)
        self.assertEqual(binaryLength2, 584)
    
    
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



    def test_insertMessageIntoImage(self):
        message = "0" # this will be a binary value of "00110000"
        binaryMessage = userInputToBinary(message)
        binaryMessageLength = findBinaryMessageLength(binaryMessage)

        image = Image.new( 'RGB', (150,150), "black") # creates test image of 150x150 black square
        pixels = image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                pixels[i,j] = (0, 0, 0)

        insertMessageIntoImage(binaryMessage, image)
        self.assertNotEqual(pixels[100,0], pixels[0, 0])
        self.assertNotEqual(pixels[101,0], pixels[0, 0])
        self.assertEqual(pixels[100,0], (0,0,1))
        self.assertEqual(pixels[101,0], (1,0,0))


    def test_insertMessageLengthIntoImage(self):
        message = "0"
        binaryMessage = userInputToBinary(message)
        binaryMessageLength = findBinaryMessageLength(binaryMessage) # this gives a value of 8 which is 000 000 000 000 000 000 000 001 000

        image = Image.new( 'RGB', (150,150), "white") # creates test image of 150x150 white square
        pixels = image.load()
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                pixels[i,j] = (255, 255, 255)

        insertMessageLengthIntoImage(binaryMessageLength, image)
        self.assertNotEqual(pixels[70,0], pixels[0, 0])
        self.assertNotEqual(pixels[77,0], pixels[0, 0])
        self.assertEqual(pixels[70,0], (254,254,254))
        self.assertEqual(pixels[77,0], (254,254,255))


if __name__ == "__main__":
    unittest.main()