import cv2, numpy as np
from detect_contours import detectContours

def extractShapes(origFileNameWithoutExt):
    print(origFileNameWithoutExt)
    contours, grayscaleImage, binaryImage = detectContours(origFileNameWithoutExt)
    
    shapes = []
    
    for i, contour in enumerate(contours):
        arclen = cv2.arcLength(contour, True)
        approxPoly = cv2.approxPolyDP(contour, 0.015 * arclen, True)
            # Approximate a contour as a polygon by reducing the number of points in
            # the contour.
            # approxPoly: a list of points in an approximated polygon
#         print(approxPoly)
        
        if len(approxPoly) >= 8:
            # Assume approxPoly is a circle.
            (x,y), radius = cv2.minEnclosingCircle(approxPoly)
            center = (int(x), int(y))
            radius = int(radius)
            shapes.append([center, radius])
            if radius >= 8:
                print("\tbig circle\t", center, radius)
            else:
                print("\tsmall circle\t", center, radius)
        else:
            # Assume approxPoly is a rectangle.
            x, y, width, height = cv2.boundingRect(approxPoly)
            center = (int(x+(width/2)), int(y+(height/2)))
            halfSideLength = int((width + height)/4)
            shapes.append([center, halfSideLength])
            print("\trectangle\t", center, halfSideLength)

    return shapes, grayscaleImage, binaryImage

if __name__ == "__main__":
#     origFileNameWithoutExt = "images/aquila"
#     origFileNameWithoutExt = "images/big-dipper"
#     origFileNameWithoutExt = "images/canis-major"
#     origFileNameWithoutExt = "images/cassiopeia"
#     origFileNameWithoutExt = "images/cygnus"
#     origFileNameWithoutExt = "images/lyra"
#     origFileNameWithoutExt = "images/orion"
#     print(origFileNameWithoutExt)
#     extractShapes(origFileNameWithoutExt)
    
    origFileNamesWithoutExt = ["images/aquila",
                               "images/big-dipper",
                               "images/canis-major",
                               "images/cassiopeia",
                               "images/cygnus",
                               "images/lyra",
                               "images/orion",
                               "images/canis-minor"]
    for fileName in origFileNamesWithoutExt:
        extractShapes(fileName)
