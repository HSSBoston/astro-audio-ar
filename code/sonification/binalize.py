import cv2, numpy as np

def binalizeImage(origFileNameWithoutExt):
    origFileName = origFileNameWithoutExt + ".jpg"
    image = cv2.imread(origFileName)

    grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Convert each pixel's color to grayscale.
    cv2.imwrite(origFileNameWithoutExt + "-gray.jpg", grayscaleImage)
        # Save the grayscaled image as *-gray.jpg.

    _, binaryImage = cv2.threshold(grayscaleImage, 127, 255, cv2.THRESH_BINARY)
        # Binarization threshold: 127
        # If a pixel's value > threshold (127), the value is replaced with the max val (255).
        # Otherwise, it becomes 0. 
    cv2.imwrite(origFileNameWithoutExt + "-binary.jpg", binaryImage)
        # Save the binalized image as *-binary.jpg.
    return (grayscaleImage, binaryImage)

if __name__ == "__main__":
#     origFileNameWithoutExt = "images/aquila"
#     origFileNameWithoutExt = "images/big-dipper"
#     origFileNameWithoutExt = "images/canis-major"
#     origFileNameWithoutExt = "images/cassiopeia"
#     origFileNameWithoutExt = "images/cygnus"
#     origFileNameWithoutExt = "images/lyra"
#     origFileNameWithoutExt = "images/orion"
# 
#     binalizeImage(origFileNameWithoutExt)

    origFileNamesWithoutExt = ["images/aquila",
                               "images/big-dipper",
                               "images/canis-major",
                               "images/cassiopeia",
                               "images/cygnus",
                               "images/lyra",
                               "images/orion",
                               "images/canis-minor"]
    for fileName in origFileNamesWithoutExt:
        binalizeImage(fileName)
