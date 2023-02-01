from PIL import Image
import os
import re

def main():
    #get current directory
    dir = os.path.dirname(os.path.abspath(__file__))

    #open target file & convert to grayscale
    file = input("Enter image name: ")
    imagePath = dir + '/' + file + '.jpg'
    image = Image.open(imagePath, 'r')
    imageName = (re.split("/|.jpg", imagePath))
    imageName = (imageName[len(imageName)-2])

    #grayscale range - 69 characters
    ### different gradients to choose from
    # characters = """$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'."""
    # characters = """@@@@@@@@@@@@%%%%%%%%#########********+++++++++===="""
    characters = """@&%QWNM0gB$#DR8mHXKAUbGOpV4d9h6PkqwSE2]ayjxY5Zoen[ult13If}C{iF|(7J)vTLs?z/*cr!+<>;=^,_:'-.`"""
    scale = [*characters]


    #get image size and ratio - calculate new dimensions - smallest dimension must be 16
    size = image.size
    w = size[0]
    l = size[1]

    #play w/ different values
    maxSize = int(input('Enter max size (px): '))

    newSizes = findNewDimensions(w, l, maxSize)
    image = image.convert('L')
    image = image.resize(newSizes)
    image.save(dir + '/new_' + imageName + '.jpg')

    toPixel = []
    totalMax = image.getpixel((0, 0))
    totalMin = image.getpixel((0, 0))

    print(newSizes)

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