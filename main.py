#use pip3 install ...

from PIL import Image
import os
import cv2
import sys

DEFAULT_RES = 128
VIDEO_EXT = ['.mp4', '.avi']
IMAGE_EXT = ['.jpg', '.png']

def main():
    #input should be as absolute path
    path = sys.argv[1]
    _, ext = os.path.splitext(path)
    res = 0
    if (len(sys.argv) > 2):
        res = int(sys.argv[2])

    if (ext in VIDEO_EXT):
        renderVideo(path, res)
    elif (ext in IMAGE_EXT):
        renderFile(path, res)
    else:
        print("Invalid file path/type!")

def renderVideo(path, maxSize):
    if (maxSize == 0):
        maxSize = DEFAULT_RES
    vid = cv2.VideoCapture(path)
    width  = vid.get(3)  # float `width`
    height = vid.get(4)  # float `height`

    newSizes = findNewDimensions(width, height, maxSize)
    
    while (vid.isOpened()):
        # Capture frame-by-frame
        # os.system('clear')
        ret, frame = vid.read()
        if (ret == True):
            cv2_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2_frame = cv2.resize(cv2_frame, (newSizes[0], newSizes[1]), fx = 0, fy = 0,interpolation = cv2.INTER_CUBIC)
            pil_frame = Image.fromarray(cv2_frame)
            renderPostImage(pil_frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    vid.release()
    cv2.destroyAllWindows()

def renderFile(path, maxSize):
    if (maxSize == 0):
        maxSize = DEFAULT_RES
    image = Image.open(path, 'r')
    renderImage(image, maxSize)

def renderPostImage(image):
    characters = """`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""
    scale = [*characters]

    #get image size
    size = image.size
    newSizes = size
    # image.save(dir + '/new_' + imageName + '.jpg')

    toPixel = []
    totalMax = image.getpixel((0, 0))
    totalMin = image.getpixel((0, 0))

    # print(newSizes)

    for y in range(0, newSizes[1], 2):
        row = []
        for x in range(newSizes[0]):
            pixel = image.getpixel((x, y))
            row.append(pixel)
            if (pixel > totalMax): totalMax = pixel
            if (pixel < totalMin): totalMin = pixel
        toPixel.append(row)

    # for i in range(len(toPixel)):
    #     print(toPixel[i])

    eachRange = int((totalMax - totalMin)/len(characters))
    ranges = []
    for i in range(len(characters)):
        ranges.append(totalMin + eachRange * i)

    for a in range(len(toPixel)):
        for b in range(len(toPixel[a])):
            pixelValue = toPixel[a][b]
            toPixel[a][b] = getShading(pixelValue, ranges, scale)

    for i in range(len(toPixel)):
        line = ''.join(toPixel[i])
        print(line)

def renderImage(image, maxSize=0):

    #grayscale range - 69 characters
    ### different gradients to choose from
    # characters = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'."""
    # characters = """@@@@@@@@@@@@%%%%%%%%#########********+++++++++===="""
    # characters = """@&%QWNM0gB$#DR8mHXKAUbGOpV4d9h6PkqwSE2]ayjxY5Zoen[ult13If}C{iF|(7J)vTLs?z/*cr!+<>;=^,_:'-.`"""
    characters = """`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"""
    scale = [*characters]

    #get image size
    size = image.size
    w = size[0]
    l = size[1]

    if (maxSize == 0):
        maxSize = max(w, l)

    newSizes = findNewDimensions(w, l, maxSize)
    image = image.convert('L')
    image = image.resize(newSizes)
    # image.save(dir + '/new_' + imageName + '.jpg')

    toPixel = []
    totalMax = image.getpixel((0, 0))
    totalMin = image.getpixel((0, 0))

    # print(newSizes)

    for y in range(0, newSizes[1], 2):
        row = []
        for x in range(newSizes[0]):
            pixel = image.getpixel((x, y))
            row.append(pixel)
            if (pixel > totalMax): totalMax = pixel
            if (pixel < totalMin): totalMin = pixel
        toPixel.append(row)

    # for i in range(len(toPixel)):
    #     print(toPixel[i])

    eachRange = int((totalMax - totalMin)/len(characters))
    ranges = []
    for i in range(len(characters)):
        ranges.append(totalMin + eachRange * i)

    for a in range(len(toPixel)):
        for b in range(len(toPixel[a])):
            pixelValue = toPixel[a][b]
            toPixel[a][b] = getShading(pixelValue, ranges, scale)

    for i in range(len(toPixel)):
        line = ''.join(toPixel[i])
        print(line)

def findNewDimensions(w, l, ms):
    if (w == l):
        return [ms, ms]
    else:
        maximum = max(w, l)
        mult = (ms / maximum)
        return [int(w * mult), int(l * mult)]

def getShading(v, r, s):
    if (v <= r[0]): return s[0]
    if (v >= r[len(r)-1]): return s[len(s)-1]
    else:
        point = 0
        while (v > r[point]):
            point += 1
        return s[point] 

if __name__ == "__main__":
    main()