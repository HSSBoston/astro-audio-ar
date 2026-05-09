import cv2, numpy as np
from detect_contours import detectContours
from star import Star

def extractStars(origFileNameWithoutExt):
    contours, grayscaleImage, binaryImage = detectContours(origFileNameWithoutExt)
    
    stars = []
    
    for i, contour in enumerate(contours):
        arclen = cv2.arcLength(contour, True)
        approxPoly = cv2.approxPolyDP(contour, 0.015 * arclen, True)
            # Approximate a contour as a polygon by reducing the number of points in
            # the contour.
            # approxPoly: a list of points in an approximated polygon
#         print(approxPoly)
        
        if len(approxPoly) >= 8:
            # Assume approxPoly is a circle.
            (x,y), radius = cv2.minEnclosingCircle(contour)
            center = (int(x), int(y))
            radius = int(radius)
            if radius >= 8:
                shapeName = "big-circle"
            else:
                shapeName = "small-circle"
            star = Star(shapeName, center,
                        center[0]-radius, center[0]+radius,
                        center[1]-radius, center[1]+radius)
        else:
            # Assume approxPoly is a rectangle.
            x, y, width, height = cv2.boundingRect(contour)
            center = (int(x+(width/2)), int(y+(height/2)))
            halfSideLength = int((width + height)/4)
            star = Star("rectangle", center,
                        center[0]-halfSideLength, center[0]+halfSideLength,
                        center[1]-halfSideLength, center[1]+halfSideLength)

        stars.append(star)

    return stars, grayscaleImage, binaryImage

if __name__ == "__main__":
    origFileNamesWithoutExt = ["images/aquila",
                               "images/big-dipper",
                               "images/canis-major",
                               "images/cassiopeia",
                               "images/cygnus",
                               "images/lyra",
                               "images/orion",
                               "images/canis-minor"]
    for fileName in origFileNamesWithoutExt:
        print(fileName)
        stars, _, _ = extractStars(fileName)
        for star in stars:
            print("\t", star.shape, "\t", star.center,
                  star.xLeft, star.xRight, star.yTop, star.yBottom)
        
#     origFileNameWithoutExt = "images/aquila"
#     origFileNameWithoutExt = "images/big-dipper"
#     origFileNameWithoutExt = "images/canis-major"
#     origFileNameWithoutExt = "images/cassiopeia"
#     origFileNameWithoutExt = "images/cygnus"
#     origFileNameWithoutExt = "images/lyra"
#     origFileNameWithoutExt = "images/orion"
#     
#     print(origFileNameWithoutExt)
#     stars, _, _ = extractStars(origFileNameWithoutExt)
#     
#     for star in stars:
#         print( star.shape, star.center,
#                star.xLeft, star.xRight, star.yTop, star.yBottom)
