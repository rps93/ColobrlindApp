import copy, Image, ImageSequence
import numpy as np
from images2gif import writeGif

red = 0;
green = 1;
blue = 2;

# less than 1
colorScale = .25
# rollover multiplications (weird transforms)
# 0 for no rollover; 1 for rollover
rollover = 0

#inputImage to Process
inputImage = "C:/users/rps93_000/downloads/color_blind_04.png"

gifDuration = 1

frames = 30;

saveImg = Image.open(inputImage);
saveImg = saveImg.convert("RGB")

scalors = []
for angleIndex in range(frames):
    scalors.append([]);
    angle = float(angleIndex)/frames
    if (angle < 1.0 / 3):
        scalors[angleIndex].append(1 + colorScale * (1 - angle * 3))
        scalors[angleIndex].append(1 + colorScale * (angle * 3))
        scalors[angleIndex].append(1 + -1 * colorScale * (0.5 - abs(0.5 - angle * 3)))
    elif (angle < 2.0 / 3):
        scalors[angleIndex].append(1 + -1 * colorScale * (0.5 - abs(1.5 - angle * 3)))
        scalors[angleIndex].append(1 + colorScale * (2 - angle * 3))
        scalors[angleIndex].append(1 + colorScale * (angle * 3 - 1))
    else:
        scalors[angleIndex].append(1 + colorScale * (angle * 3 - 2))
        scalors[angleIndex].append(1 + -1 * colorScale * (0.5 - abs(2.5 - angle * 3)))
        scalors[angleIndex].append(1 + colorScale * (3 - angle * 3))

# Get the size of the image
width, height = saveImg.size
images = []

for angleIndex in range(frames):
    img = saveImg.copy()
    pix = np.array(saveImg)
    pix = pix.astype('uint16')
    
    sources = img.split()

    pixr = np.array(sources[red])
    pixr = pixr.astype('uint16')
    pix[..., red] = pixr * scalors[angleIndex][red];
    
    pixg = np.array(sources[green])
    pixg = pixg.astype('uint16')
    pix[..., green] = pixg * scalors[angleIndex][green];
    
    pixb = np.array(sources[blue])
    pixb = pixb.astype('uint16')
    pix[..., blue] = pixb * scalors[angleIndex][blue];
    
    if rollover == 0:
        pix[pix>255] = 255;
    pix2 = pix.view('uint8')[:,:,::2]
    
    images.append(pix2)


filename = "C:/Users/rps93_000/Downloads/testfolder/Gif.GIF"
writeGif(filename, images, duration=gifDuration/frames)
