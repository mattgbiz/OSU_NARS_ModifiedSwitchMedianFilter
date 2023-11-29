#This is the noise filter and removal and processing algorithm
#One of the big things I want to do is improve how to filter stacks of data to remove big and small noise values
#A big difference between our filter and a typical filter we KNOW that any gray value above XX is noise and not part of the object
#Especially within an object, we KNOW it physically cannot be larger than an open beam section because they operate on attenuation
#Maybe an item for the future is to "know" where the object is and make the filter even stricter there based off of open beam section
from matplotlib import pyplot as plt
import numpy as np
import cv2, os, statistics, gc


#HEY DUMMY X is second coordinate and Y is first so in a numpy array it is [y,x] 

#make some of my functions that the code will use
def MedianFilterImage(OriginalImage,FilterSize):
    MedianImage = np.zeros((imgHeight,imgWidth),dtype=np.uint16)
    if FilterSize == 5:
        #DifferenceImage = np.zeros((imgHeight,imgWidth),dtype=np.uint16)
        for x in range(0,imgWidth):
            for y in range(0,imgHeight):
                #im just going to try adding based on quadrants so if we are in corners we may miss out on some data but whatever
                ListForMedian = []        
                try:
                    ListForMedian.append(OriginalImage[y-2,x+2])    #This is the the 6 in top right quadrant
                    ListForMedian.append(OriginalImage[y-1,x+2])
                    ListForMedian.append(OriginalImage[y,x+2])
                    ListForMedian.append(OriginalImage[y-2,x+1])
                    ListForMedian.append(OriginalImage[y-1,x+1])
                    ListForMedian.append(OriginalImage[y,x+1])
                except:
                    pass
                try:
                    ListForMedian.append(OriginalImage[y+1,x+2])    #This ishte 6 in the bottom right quadrant
                    ListForMedian.append(OriginalImage[y+2,x+2])
                    ListForMedian.append(OriginalImage[y+1,x+1])
                    ListForMedian.append(OriginalImage[y+2,x+1])
                    ListForMedian.append(OriginalImage[y+1,x])
                    ListForMedian.append(OriginalImage[y+2,x])
                except:
                    pass
                try:
                    ListForMedian.append(OriginalImage[y,x-2])    #this is the 6 in the bottom left quadrant
                    ListForMedian.append(OriginalImage[y,x-1])
                    ListForMedian.append(OriginalImage[y+1,x-2])
                    ListForMedian.append(OriginalImage[y+1,x-1])
                    ListForMedian.append(OriginalImage[y+2,x-2])
                    ListForMedian.append(OriginalImage[y+2,x-1])
                except:
                    pass
                try:
                    ListForMedian.append(OriginalImage[y-2,x-2])      #this is hte 6 in the top left quadrant
                    ListForMedian.append(OriginalImage[y-2,x-1])
                    ListForMedian.append(OriginalImage[y-2,x])
                    ListForMedian.append(OriginalImage[y-1,x-2])
                    ListForMedian.append(OriginalImage[y-1,x-1])
                    ListForMedian.append(OriginalImage[y-1,x])
                except:
                    pass
                #now I have the median values of the pixel neighbor
                MedianImage[y,x] = statistics.median(ListForMedian)
                #DifferenceImage[y,x] = OriginalImage[y,x]-MedianImage[y,x]
                del ListForMedian
    elif FilterSize == 7:
        for x in range(0,imgWidth):
            for y in range(0,imgHeight):
                #im just going to try adding based on quadrants so if we are in corners we may miss out on some data but whatever
                ListForMedian = []            
                try:
                    ListForMedian.append(OriginalImage[y-3,x+3])    #This is the the 12 in top right quadrant
                    ListForMedian.append(OriginalImage[y-2,x+3])
                    ListForMedian.append(OriginalImage[y-1,x+3])
                    ListForMedian.append(OriginalImage[y,x+3])
                    ListForMedian.append(OriginalImage[y-3,x+2])
                    ListForMedian.append(OriginalImage[y-2,x+2])    
                    ListForMedian.append(OriginalImage[y-1,x+2])
                    ListForMedian.append(OriginalImage[y,x+2])
                    ListForMedian.append(OriginalImage[y-3,x+1])
                    ListForMedian.append(OriginalImage[y-2,x+1])
                    ListForMedian.append(OriginalImage[y-1,x+1])
                    ListForMedian.append(OriginalImage[y,x+1])
                except:
                    pass
                try:
                    ListForMedian.append(OriginalImage[y+1,x+3])    #This is the 12 in the bottom right quadrant
                    ListForMedian.append(OriginalImage[y+2,x+3])
                    ListForMedian.append(OriginalImage[y+3,x+3])
                    ListForMedian.append(OriginalImage[y+1,x+2])
                    ListForMedian.append(OriginalImage[y+2,x+2])
                    ListForMedian.append(OriginalImage[y+3,x+2])
                    ListForMedian.append(OriginalImage[y+1,x+1])
                    ListForMedian.append(OriginalImage[y+2,x+1])
                    ListForMedian.append(OriginalImage[y+3,x+1])
                    ListForMedian.append(OriginalImage[y+1,x])
                    ListForMedian.append(OriginalImage[y+2,x])
                    ListForMedian.append(OriginalImage[y+3,x])
                except:
                    pass
                try:
                    ListForMedian.append(OriginalImage[y,x-3])  #this is the 12 in the bottom left quadrant
                    ListForMedian.append(OriginalImage[y,x-2])    
                    ListForMedian.append(OriginalImage[y,x-1])
                    ListForMedian.append(OriginalImage[y+1,x-3]) 
                    ListForMedian.append(OriginalImage[y+1,x-2])    
                    ListForMedian.append(OriginalImage[y+1,x-1])
                    ListForMedian.append(OriginalImage[y+2,x-3])
                    ListForMedian.append(OriginalImage[y+2,x-2])    
                    ListForMedian.append(OriginalImage[y+2,x-1])
                    ListForMedian.append(OriginalImage[y+3,x-3])
                    ListForMedian.append(OriginalImage[y+3,x-2])    
                    ListForMedian.append(OriginalImage[y+3,x-1])
                except:
                    pass
                try:
                    ListForMedian.append(OriginalImage[y-3,x-3])     #this is the 12 in the top left quadrant
                    ListForMedian.append(OriginalImage[y-3,x-2])
                    ListForMedian.append(OriginalImage[y-3,x-1])
                    ListForMedian.append(OriginalImage[y-3,x])
                    ListForMedian.append(OriginalImage[y-2,x-3])
                    ListForMedian.append(OriginalImage[y-2,x-2])      
                    ListForMedian.append(OriginalImage[y-2,x-1])
                    ListForMedian.append(OriginalImage[y-2,x])
                    ListForMedian.append(OriginalImage[y-1,x-3])
                    ListForMedian.append(OriginalImage[y-1,x-2])
                    ListForMedian.append(OriginalImage[y-1,x-1])
                    ListForMedian.append(OriginalImage[y-1,x])
                except:
                    pass
                MedianImage[y,x] = statistics.median(ListForMedian)
                #DifferenceImage[y,x] = OriginalImage[y,x]-MedianImage[y,x]
                del ListForMedian
    else:
        print('Code Only Accepts filter kernel size of 5 and 7')
        raise Exception
    #once I am done with creating the median image, create the difference map
    #DifferenceImage = OriginalImage-MedianImage
    return MedianImage
    
def trackNoise(x_coord,y_coord,imgX,imgY,DiffMap,FlagMap):
    #the purpose of this function is to find how large of a cluster the identified noise is
    #The function will flag future pixels so we don't have to repeat the process for those pixels
    #it takes in the starting x and y coordinates of the noise and the image size. This is so I don't look too far right or down
    #flag map is the imgX by imgY array which siginifies if noise has been flagged there yet or no NEEDS to be an array
    TrackListX = []
    TrackListY = []
    TrackListX.append(x_coord)
    TrackListY.append(y_coord)
    FlagMap[y_coord,x_coord] = 500  #500 is the temporary flag designator until we know how large the noise is

    noiseInc = 0
    while noiseInc < len(TrackListX):
        #ok here we are going to be searching for clusters to identify how large the noise is
        #The length of TrackListX will grow until there is no noise left to identify
        #lets start by looking to the right, using the try function because if we are on the edge we can't look to the right
        try:
            if DiffMap[TrackListY[noiseInc],TrackListX[noiseInc]+1] >= NoiseThresh and FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]+1] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc]+1)   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc])
                FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]+1] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go right as we must be near the edge | x = {}'.format(TrackListX[noiseInc]+1))
        #down right
        try:
            if DiffMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]+1] >= NoiseThresh and FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]+1] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc]+1)   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc]+1)
                FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]+1] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go down-right as we must be near the edge | x = {},y = {}'.format(TrackListX[noiseInc]+1,TrackListY[noiseInc]+1))
        #down
        try:
            if DiffMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]] >= NoiseThresh and FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc])   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc]+1)
                FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go down as we must be near the edge | y = {}'.format(TrackListY[noiseInc]+1))
        #down left
        try:
            if DiffMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]-1] >= NoiseThresh and FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]-1] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc]-1)   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc]+1)
                FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]-1] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go down left as we must be near the edge | x= {}, y = {}'.format(TrackListX[noiseInc]-1,TrackListY[noiseInc]+1))
        #left
        try:
            if DiffMap[TrackListY[noiseInc],TrackListX[noiseInc]-1] >= NoiseThresh and FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]-1] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc]-1)   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc])
                FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]-1] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go left as we must be near the edge | x= {}'.format(TrackListX[noiseInc]-1))
        #up left
        try:
            if DiffMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]-1] >= NoiseThresh and FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]-1] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc]-1)   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc]-1)
                FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]-1] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go up left as we must be near the edge | x= {}, y = {}'.format(TrackListX[noiseInc]-1,TrackListY[noiseInc]-1))
        #up
        try:
            if DiffMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]] >= NoiseThresh and FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc])   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc]-1)
                FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go up as we must be near the edge | y = {}'.format(TrackListY[noiseInc]-1))
        #up right
        try:
            if DiffMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]+1] >= NoiseThresh and FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]+1] == 0:
                #if we have noise that has not already been flagged
                TrackListX.append(TrackListX[noiseInc]+1)   #add this pixel to the x and y coords
                TrackListY.append(TrackListY[noiseInc]-1)
                FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]+1] = 500  #flag this one so we don't do it again later
        except:
            pass
            #print('Looks like we cant go up right as we must be near the edge | x= {}, y = {}'.format(TrackListX[noiseInc]+1,TrackListY[noiseInc]-1))

        #now that we have looked in all 8 directions from the noise and added adjacent noise particles to the lists, we can increment the noiseInc
        noiseInc +=1    #now the process will start over for the next noise

    #after we leave the loop, I need to see how large the noise cluster is to then assign appropriate flags
    finalNoiseLength = len(TrackListX)
    if finalNoiseLength == 1:
        #if it is just a single noise no cluster then it is assigned a flag of 1
        FlagMap[TrackListY[0],TrackListX[0]] = 10000
    if finalNoiseLength > 1 and finalNoiseLength < 7:
        #if its 2-6 pixels, I'll use a 5x5 median filter so W_2
        inc = 0
        while inc < len(TrackListX):
            FlagMap[TrackListY[inc],TrackListX[inc]] = 20000
            inc +=1
    if finalNoiseLength >= 7:
        #print('Uhhhoh we likely have a bloomed pixel near x = {} y = {}'.format(TrackListX[0],TrackListY[0]))
        #I want to handle the bloomed pixels differently because I need to change the threshold and search again for noise that is the smear from oversaturation
        noiseInc = 0
        while noiseInc < len(TrackListX):
            #ok here we are going to be searching for clusters to identify how large the noise is
            #The length of TrackListX will grow until there is no noise left to identify
            #lets start by looking to the right, using the try function because if we are on the edge we can't look to the right
            try:
                if DiffMap[TrackListY[noiseInc],TrackListX[noiseInc]+1] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]+1] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc]+1)   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc])
                    FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]+1] = 40000  #flag for noise will blooming
            except:
                pass
                #print('Looks like we cant go right as we must be near the edge | x = {}'.format(TrackListX[noiseInc]+1))
            #down right
            try:
                if DiffMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]+1] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]+1] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc]+1)   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc]+1)
                    FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]+1] = 40000  #flag this one so we don't do it again later
            except:
                pass
                #print('Looks like we cant go down-right as we must be near the edge | x = {},y = {}'.format(TrackListX[noiseInc]+1,TrackListY[noiseInc]+1))
            #down
            try:
                if DiffMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc])   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc]+1)
                    FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]] = 40000  #flag this one so we don't do it again later
            except:
                pass
                #print('Looks like we cant go down as we must be near the edge | y = {}'.format(TrackListY[noiseInc]+1))
            #down left
            try:
                if DiffMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]-1] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]-1] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc]-1)   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc]+1)
                    FlagMap[TrackListY[noiseInc]+1,TrackListX[noiseInc]-1] = 40000  #flag this one so we don't do it again later
            except:
                pass
                #print('Looks like we cant go down left as we must be near the edge | x= {}, y = {}'.format(TrackListX[noiseInc]-1,TrackListY[noiseInc]+1))
            #left
            try:
                if DiffMap[TrackListY[noiseInc],TrackListX[noiseInc]-1] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]-1] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc]-1)   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc])
                    FlagMap[TrackListY[noiseInc],TrackListX[noiseInc]-1] = 40000  #flag this one so we don't do it again later
            except:
                pass
                #print('Looks like we cant go left as we must be near the edge | x= {}'.format(TrackListX[noiseInc]-1))
            #up left
            try:
                if DiffMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]-1] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]-1] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc]-1)   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc]-1)
                    FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]-1] = 40000  #flag this one so we don't do it again later
            except:
                pass
                #print('Looks like we cant go up left as we must be near the edge | x= {}, y = {}'.format(TrackListX[noiseInc]-1,TrackListY[noiseInc]-1))
            #up
            try:
                if DiffMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc])   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc]-1)
                    FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]] = 40000  #flag this one so we don't do it again later
            except:
                pass
                #print('Looks like we cant go up as we must be near the edge | y = {}'.format(TrackListY[noiseInc]-1))
            #up right
            try:
                if DiffMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]+1] >= NoiseThreshBloom and FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]+1] == 0:
                    #if we have noise that has not already been flagged
                    TrackListX.append(TrackListX[noiseInc]+1)   #add this pixel to the x and y coords
                    TrackListY.append(TrackListY[noiseInc]-1)
                    FlagMap[TrackListY[noiseInc]-1,TrackListX[noiseInc]+1] = 40000  #flag this one so we don't do it again later
            except:
                pass
                #print('Looks like we cant go up right as we must be near the edge | x= {}, y = {}'.format(TrackListX[noiseInc]+1,TrackListY[noiseInc]-1))

            #now that we have looked in all 8 directions from the noise and added adjacent noise particles to the lists, we can increment the noiseInc
            noiseInc +=1    #now the process will start over for the next noise

            #lastly after going through and adding all of these to the list and identifying them as bloomed 3...
            # I need to change the ones that were already identified from 500 to 3
            inc = 0
            while inc < finalNoiseLength:
                FlagMap[TrackListY[inc],TrackListX[inc]] = 40000
                inc += 1

def filterNoiseSingleRadiograph(FlagMap,FilteredImage):
    #so now that I know how large the noise is for a noisy pixel, I need to Filter Accordingly
    yToFilter, xToFilter = np.nonzero(FlagMap)
    #now I have the x and y coordinates that need to be filtered
    
    for y, x in zip(yToFilter,xToFilter):
        #now with the coordinate pairs, I can filter based off of flagged noise size
        ListForMedian = []
        if FlagMap[y,x] == 10000:
            #Just filter based on 8 adjacent pixels - right, right down, down, left down, left, left up, up, upright
            try:
                ListForMedian.append(FilteredImage[y,x+1])  #right
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y+1,x+1])    #right Down
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y+1,x])      #down
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y+1,x-1])    #left down
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y,x-1])      #left
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y-1,x-1])    #left up
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y-1,x])      #up
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y-1,x+1])      #up right
            except:
                pass
        elif FlagMap[y,x] == 20000:
            #this has 2-6 sized noise so I'm using a 5x5 median filter
            #im just going to try adding based on quadrants so if we are in corners we may miss out on some data but whatever
            try:
                ListForMedian.append(FilteredImage[y-2,x+2])    #This is the the 6 in top right quadrant
                ListForMedian.append(FilteredImage[y-1,x+2])
                ListForMedian.append(FilteredImage[y,x+2])
                ListForMedian.append(FilteredImage[y-2,x+1])
                ListForMedian.append(FilteredImage[y-1,x+1])
                ListForMedian.append(FilteredImage[y,x+1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y+1,x+2])    #This ishte 6 in the bottom right quadrant
                ListForMedian.append(FilteredImage[y+2,x+2])
                ListForMedian.append(FilteredImage[y+1,x+1])
                ListForMedian.append(FilteredImage[y+2,x+1])
                ListForMedian.append(FilteredImage[y+1,x])
                ListForMedian.append(FilteredImage[y+2,x])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y,x-2])    #this is the 6 in the bottom left quadrant
                ListForMedian.append(FilteredImage[y,x-1])
                ListForMedian.append(FilteredImage[y+1,x-2])
                ListForMedian.append(FilteredImage[y+1,x-1])
                ListForMedian.append(FilteredImage[y+2,x-2])
                ListForMedian.append(FilteredImage[y+2,x-1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y-2,x-2])      #this is hte 6 in the top left quadrant
                ListForMedian.append(FilteredImage[y-2,x-1])
                ListForMedian.append(FilteredImage[y-2,x])
                ListForMedian.append(FilteredImage[y-1,x-2])
                ListForMedian.append(FilteredImage[y-1,x-1])
                ListForMedian.append(FilteredImage[y-1,x])
            except:
                pass
            #now I know that if the pixel has a flag of 2 then 2-6 neighboring pixels are noisy. Im going to sort the list lowest to highest and remove the top 3
            ListForMedian.sort()
            #and remove the top 3
            del ListForMedian[-3:]
        elif FlagMap[y,x] == 40000:
            #now this is the >=7 pixels in noisy range so I am using median filter of 7x7
            #im just going to try adding based on quadrants so if we are in corners we may miss out on some data but whatever
            try:
                ListForMedian.append(FilteredImage[y-3,x+3])    #This is the the 12 in top right quadrant
                ListForMedian.append(FilteredImage[y-2,x+3])
                ListForMedian.append(FilteredImage[y-1,x+3])
                ListForMedian.append(FilteredImage[y,x+3])
                ListForMedian.append(FilteredImage[y-3,x+2])
                ListForMedian.append(FilteredImage[y-2,x+2])    
                ListForMedian.append(FilteredImage[y-1,x+2])
                ListForMedian.append(FilteredImage[y,x+2])
                ListForMedian.append(FilteredImage[y-3,x+1])
                ListForMedian.append(FilteredImage[y-2,x+1])
                ListForMedian.append(FilteredImage[y-1,x+1])
                ListForMedian.append(FilteredImage[y,x+1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y+1,x+3])    #This is the 12 in the bottom right quadrant
                ListForMedian.append(FilteredImage[y+2,x+3])
                ListForMedian.append(FilteredImage[y+3,x+3])
                ListForMedian.append(FilteredImage[y+1,x+2])
                ListForMedian.append(FilteredImage[y+2,x+2])
                ListForMedian.append(FilteredImage[y+3,x+2])
                ListForMedian.append(FilteredImage[y+1,x+1])
                ListForMedian.append(FilteredImage[y+2,x+1])
                ListForMedian.append(FilteredImage[y+3,x+1])
                ListForMedian.append(FilteredImage[y+1,x])
                ListForMedian.append(FilteredImage[y+2,x])
                ListForMedian.append(FilteredImage[y+3,x])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y,x-3])  #this is the 12 in the bottom left quadrant
                ListForMedian.append(FilteredImage[y,x-2])    
                ListForMedian.append(FilteredImage[y,x-1])
                ListForMedian.append(FilteredImage[y+1,x-3]) 
                ListForMedian.append(FilteredImage[y+1,x-2])    
                ListForMedian.append(FilteredImage[y+1,x-1])
                ListForMedian.append(FilteredImage[y+2,x-3])
                ListForMedian.append(FilteredImage[y+2,x-2])    
                ListForMedian.append(FilteredImage[y+2,x-1])
                ListForMedian.append(FilteredImage[y+3,x-3])
                ListForMedian.append(FilteredImage[y+3,x-2])    
                ListForMedian.append(FilteredImage[y+3,x-1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage[y-3,x-3])     #this is hte 12 in the top left quadrant
                ListForMedian.append(FilteredImage[y-3,x-2])
                ListForMedian.append(FilteredImage[y-3,x-1])
                ListForMedian.append(FilteredImage[y-3,x])
                ListForMedian.append(FilteredImage[y-2,x-3])
                ListForMedian.append(FilteredImage[y-2,x-2])      
                ListForMedian.append(FilteredImage[y-2,x-1])
                ListForMedian.append(FilteredImage[y-2,x])
                ListForMedian.append(FilteredImage[y-1,x-3])
                ListForMedian.append(FilteredImage[y-1,x-2])
                ListForMedian.append(FilteredImage[y-1,x-1])
                ListForMedian.append(FilteredImage[y-1,x])
            except:
                pass
            #now I know that if the pixel has a flag of 3 then at least 7 neighboring pixels are noisy. Im going to sort the list lowest to highest and remove the top 7
            ListForMedian.sort()
            #and remove the top 7
            del ListForMedian[-7:]
        else:
            print('The flag was somehow none of my options it was {}'.format(FlagMap[y,x]))
        #anyways now i have the list for median regardless of what size we used. Now it is time to take the median and replace the value in the filtered image
        #print('Filtered noise for y = {} and x = {}'.format(y,x))
        #print('The list for to be given median is {}'.format(ListForMedian))
        #print('The median of this list is {}'.format(statistics.median(ListForMedian)))
        FilteredImage[y,x] = statistics.median(ListForMedian)
        del ListForMedian

def filterNoiseNeighbors(FlagMap1,FilteredImage1,FlagMap2,Original2,FlagMap3,Original3):
    #so now that I know how large the noise is for a noisy pixel, I need to Filter Accordingly
    yToFilter, xToFilter = np.nonzero(FlagMap1)
    #now I have the x and y coordinates that need to be filtered
    
    for y, x in zip(yToFilter,xToFilter):
        #now with the coordinate pairs, I can filter based off of flagged noise size
        ListForMedian = []
        if FlagMap1[y,x] == 10000:
            #Just filter based on 10 adjacent pixels - right, right down, down, left down, left, left up, up, upright, and center of next and previous images
            try:
                ListForMedian.append(FilteredImage1[y,x+1])  #right
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y+1,x+1])    #right Down
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y+1,x])      #down
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y+1,x-1])    #left down
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y,x-1])      #left
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y-1,x-1])    #left up
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y-1,x])      #up
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y-1,x+1])      #up right
            except:
                pass
            try:
                ListForMedian.append(Original2[y,x])
            except:
                pass
            try:
                ListForMedian.append(Original3[y,x])
            except:
                pass
        elif FlagMap1[y,x] == 20000:
            #this has 2-6 sized noise so I'm using a 5x5 median filter
            #im just going to try adding based on quadrants so if we are in corners we may miss out on some data but whatever
            try:
                ListForMedian.append(FilteredImage1[y-2,x+2])    #This is the the 6 in top right quadrant
                ListForMedian.append(FilteredImage1[y-1,x+2])
                ListForMedian.append(FilteredImage1[y,x+2])
                ListForMedian.append(FilteredImage1[y-2,x+1])
                ListForMedian.append(FilteredImage1[y-1,x+1])
                ListForMedian.append(FilteredImage1[y,x+1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y+1,x+2])    #This ishte 6 in the bottom right quadrant
                ListForMedian.append(FilteredImage1[y+2,x+2])
                ListForMedian.append(FilteredImage1[y+1,x+1])
                ListForMedian.append(FilteredImage1[y+2,x+1])
                ListForMedian.append(FilteredImage1[y+1,x])
                ListForMedian.append(FilteredImage1[y+2,x])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y,x-2])    #this is the 6 in the bottom left quadrant
                ListForMedian.append(FilteredImage1[y,x-1])
                ListForMedian.append(FilteredImage1[y+1,x-2])
                ListForMedian.append(FilteredImage1[y+1,x-1])
                ListForMedian.append(FilteredImage1[y+2,x-2])
                ListForMedian.append(FilteredImage1[y+2,x-1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y-2,x-2])      #this is hte 6 in the top left quadrant
                ListForMedian.append(FilteredImage1[y-2,x-1])
                ListForMedian.append(FilteredImage1[y-2,x])
                ListForMedian.append(FilteredImage1[y-1,x-2])
                ListForMedian.append(FilteredImage1[y-1,x-1])
                ListForMedian.append(FilteredImage1[y-1,x])
            except:
                pass
            try:
                if FlagMap2[y-1,x-1] == 0:
                    ListForMedian.append(Original2[y-1,x-1])
                    #print('Added from FlagMap2')
                if FlagMap2[y,x-1] == 0:
                    ListForMedian.append(Original2[y,x-1])
                if FlagMap2[y-1,x] == 0:
                    ListForMedian.append(Original2[y-1,x])
                if FlagMap2[y,x] == 0:
                    ListForMedian.append(Original2[y,x])
                if FlagMap2[y+1,x+1] == 0:
                    ListForMedian.append(Original2[y+1,x+1])
                if FlagMap2[y+1,x] == 0:
                    ListForMedian.append(Original2[y+1,x])
                if FlagMap2[y,x+1] == 0:
                    ListForMedian.append(Original2[y,x+1])
                if FlagMap2[y+1,x-1] == 0:
                    ListForMedian.append(Original2[y+1,x-1])
                if FlagMap2[y-1,x+1] == 0:
                    ListForMedian.append(Original2[y-1,x+1])
                #print('Did att from Original 2')
            except:
                pass
                #print('Did not add from the Original 2 for some reason')
            try:
                if FlagMap3[y-1,x-1] == 0:
                    ListForMedian.append(Original3[y-1,x-1])
                    #print('Added from FlagMap3')
                if FlagMap3[y,x-1] == 0:
                    ListForMedian.append(Original3[y,x-1])
                if FlagMap3[y-1,x] == 0:
                    ListForMedian.append(Original3[y-1,x])
                if FlagMap3[y,x] == 0:
                    ListForMedian.append(Original3[y,x])
                if FlagMap3[y+1,x+1] == 0:
                    ListForMedian.append(Original3[y+1,x+1])
                if FlagMap3[y+1,x] == 0:
                    ListForMedian.append(Original3[y+1,x])
                if FlagMap3[y,x+1] == 0:
                    ListForMedian.append(Original3[y,x+1])
                if FlagMap3[y+1,x-1] == 0:
                    ListForMedian.append(Original3[y+1,x-1])
                if FlagMap3[y-1,x+1] == 0:
                    ListForMedian.append(Original3[y-1,x+1])
            except:
                pass
                #print('Did not add from the Original 3 for some reason')
            #now I know that if the pixel has a flag of 2 then 2-6 neighboring pixels are noisy. Im going to sort the list lowest to highest and remove the top 3
            ListForMedian.sort()
            #and remove the top 6
            del ListForMedian[-6:]
        elif FlagMap1[y,x] == 40000:
            #now this is the >=7 pixels in noisy range so I am using median filter of 7x7
            #im just going to try adding based on quadrants so if we are in corners we may miss out on some data but whatever
            try:
                ListForMedian.append(FilteredImage1[y-3,x+3])    #This is the the 12 in top right quadrant
                ListForMedian.append(FilteredImage1[y-2,x+3])
                ListForMedian.append(FilteredImage1[y-1,x+3])
                ListForMedian.append(FilteredImage1[y,x+3])
                ListForMedian.append(FilteredImage1[y-3,x+2])
                ListForMedian.append(FilteredImage1[y-2,x+2])    
                ListForMedian.append(FilteredImage1[y-1,x+2])
                ListForMedian.append(FilteredImage1[y,x+2])
                ListForMedian.append(FilteredImage1[y-3,x+1])
                ListForMedian.append(FilteredImage1[y-2,x+1])
                ListForMedian.append(FilteredImage1[y-1,x+1])
                ListForMedian.append(FilteredImage1[y,x+1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y+1,x+3])    #This is the 12 in the bottom right quadrant
                ListForMedian.append(FilteredImage1[y+2,x+3])
                ListForMedian.append(FilteredImage1[y+3,x+3])
                ListForMedian.append(FilteredImage1[y+1,x+2])
                ListForMedian.append(FilteredImage1[y+2,x+2])
                ListForMedian.append(FilteredImage1[y+3,x+2])
                ListForMedian.append(FilteredImage1[y+1,x+1])
                ListForMedian.append(FilteredImage1[y+2,x+1])
                ListForMedian.append(FilteredImage1[y+3,x+1])
                ListForMedian.append(FilteredImage1[y+1,x])
                ListForMedian.append(FilteredImage1[y+2,x])
                ListForMedian.append(FilteredImage1[y+3,x])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y,x-3])  #this is the 12 in the bottom left quadrant
                ListForMedian.append(FilteredImage1[y,x-2])    
                ListForMedian.append(FilteredImage1[y,x-1])
                ListForMedian.append(FilteredImage1[y+1,x-3]) 
                ListForMedian.append(FilteredImage1[y+1,x-2])    
                ListForMedian.append(FilteredImage1[y+1,x-1])
                ListForMedian.append(FilteredImage1[y+2,x-3])
                ListForMedian.append(FilteredImage1[y+2,x-2])    
                ListForMedian.append(FilteredImage1[y+2,x-1])
                ListForMedian.append(FilteredImage1[y+3,x-3])
                ListForMedian.append(FilteredImage1[y+3,x-2])    
                ListForMedian.append(FilteredImage1[y+3,x-1])
            except:
                pass
            try:
                ListForMedian.append(FilteredImage1[y-3,x-3])     #this is the 12 in the top left quadrant
                ListForMedian.append(FilteredImage1[y-3,x-2])
                ListForMedian.append(FilteredImage1[y-3,x-1])
                ListForMedian.append(FilteredImage1[y-3,x])
                ListForMedian.append(FilteredImage1[y-2,x-3])
                ListForMedian.append(FilteredImage1[y-2,x-2])      
                ListForMedian.append(FilteredImage1[y-2,x-1])
                ListForMedian.append(FilteredImage1[y-2,x])
                ListForMedian.append(FilteredImage1[y-1,x-3])
                ListForMedian.append(FilteredImage1[y-1,x-2])
                ListForMedian.append(FilteredImage1[y-1,x-1])
                ListForMedian.append(FilteredImage1[y-1,x])
            except:
                pass
            try:
                if FlagMap2[y-1,x-1] == 0:
                    ListForMedian.append(Original2[y-1,x-1])
                    #print('added from flagmap2 for big noise')
                if FlagMap2[y,x-1] == 0:
                    ListForMedian.append(Original2[y,x-1])
                if FlagMap2[y-1,x] == 0:
                    ListForMedian.append(Original2[y-1,x])
                if FlagMap2[y,x] == 0:
                    ListForMedian.append(Original2[y,x])
                if FlagMap2[y+1,x+1] == 0:
                    ListForMedian.append(Original2[y+1,x+1])
                if FlagMap2[y+1,x] == 0:
                    ListForMedian.append(Original2[y+1,x])
                if FlagMap2[y,x+1] == 0:
                    ListForMedian.append(Original2[y,x+1])
                if FlagMap2[y+1,x-1] == 0:
                    ListForMedian.append(Original2[y+1,x-1])
                if FlagMap2[y-1,x+1] == 0:
                    ListForMedian.append(Original2[y-1,x+1])
            except:
                pass
                #print('Did not add from the Original 2 for some reason')
            try:
                if FlagMap3[y-1,x-1] == 0:
                    ListForMedian.append(Original3[y-1,x-1])
                    #print('added from flagmap3 for big noise')
                if FlagMap3[y,x-1] == 0:
                    ListForMedian.append(Original3[y,x-1])
                if FlagMap3[y-1,x] == 0:
                    ListForMedian.append(Original3[y-1,x])
                if FlagMap3[y,x] == 0:
                    ListForMedian.append(Original3[y,x])
                if FlagMap3[y+1,x+1] == 0:
                    ListForMedian.append(Original3[y+1,x+1])
                if FlagMap3[y+1,x] == 0:
                    ListForMedian.append(Original3[y+1,x])
                if FlagMap3[y,x+1] == 0:
                    ListForMedian.append(Original3[y,x+1])
                if FlagMap3[y+1,x-1] == 0:
                    ListForMedian.append(Original3[y+1,x-1])
                if FlagMap3[y-1,x+1] == 0:
                    ListForMedian.append(Original3[y-1,x+1])
            except:
                pass
                #print('Did not add from the Original 3 for some reason')
            #now I know that if the pixel has a flag of 3 then at least 7 neighboring pixels are noisy. Im going to sort the list lowest to highest and remove the top 7
            ListForMedian.sort()
            #and remove the top 10
            del ListForMedian[-10:]
        else:
            print('The flag was somehow none of my options it was {}'.format(FlagMap1[y,x]))
        #anyways now i have the list for median regardless of what size we used. Now it is time to take the median and replace the value in the filtered image
        #print('Filtered noise for y = {} and x = {}'.format(y,x))
        #print('The list for to be given median is {}'.format(ListForMedian))
        #print('The median of this list is {}'.format(statistics.median(ListForMedian)))
        FilteredImage1[y,x] = statistics.median(ListForMedian)
        del ListForMedian

BitMax = 65536 #this is the uint16 bit max

currentPath = (os.path.dirname(os.path.realpath(__file__)))
InputFilePath = currentPath+'/ImageFilterInputHDPE1_11-29-21.txt'
InputParameters = []
with open(InputFilePath) as file:
    for line in file:
        line = line.split('%',1)[0] #ignores the comments lines which are % (not # because some images have projection#1.0.tif as their name)
        line = line.rstrip()
        if line != '':
            InputParameters.append(line)
ImagePath = InputParameters[0]          #path to original input images
BaseOriginalName = InputParameters[1]   #base file name without the number
BaseNumType = InputParameters[2]        #Type of number for images, Int, Float, TripleInt
MedDifPath = ImagePath+InputParameters[3]         #path relative to median dif files
BaseMedName = InputParameters[4]        #base name of median difference image
MedNumType = InputParameters[5]         #numbering system for median difference images
FilteredPath = ImagePath+InputParameters[6]       #output file path
OutputBaseName = InputParameters[7]     #output base name
FlagBaseName = InputParameters[8]      #flag map base name
maxdeg = float(InputParameters[9])             #maximum degree that stack goes to (typically 359 or 360)
startingNum = float(InputParameters[10])        #starting number (typically 0 or 1)
degInc = float(InputParameters[11])            #Increment between each number
MultImg = InputParameters[12]           #if there are multiple images at each angle
TakeNeighbors = InputParameters[13]     #if we want to use neighboring radiographs or not
NeedFlagMap = InputParameters[14]       #if we need to use create a new flag map or use a created one
OpenNum = int(InputParameters[15])           #number of open beam images to consider
OpenBaseName = InputParameters[16]      #base name for open images, needs to then be number.tif aka 1.tif or 2.tif NO 1.0.tif or 001.tif
NoisePercent = float(InputParameters[17])/100
BloomNoisePercent = float(InputParameters[18])/100

imgnum = int((maxdeg-startingNum)/degInc)
if startingNum < 1:
    imgnum += 1     #this is because if we are going from 0 to 359 we have 360 images total.


print('Entry for MedDifPath was {}'.format(MedDifPath))

#if the entry to MedDifPath is None, then we need to create the difference images myself as well as the median difference path
if MedDifPath == ImagePath+'None' or MedDifPath == ImagePath+'No':
    NeedMedDif = True       #tells code it needs to make the median difference images
    MedDifPath = ImagePath+'MedianDifference/'
    if not os.path.exists(MedDifPath):
        os.makedirs(MedDifPath)
    else:
        MedOverwrite = input("Why did you not put a Median Difference path if one exists? Overwrite? [Y] or [N]\n")
        if MedOverwrite == 'Y' or MedOverwrite == 'y':
            pass
        elif MedOverwrite == 'N' or MedOverwrite == 'n':
            NewMedPath = input("Enter a new folder name:\n")
            MedDifPath = ImagePath+NewMedPath+'/'
            os.makedirs(MedDifPath)
    BaseMedName = BaseOriginalName+'_MedDiff'
    MedNumType = BaseNumType
else:
    NeedMedDif = False
    
#MultImg = input('Are there multiple images at each angle? (y/n)\n')
if MultImg == 'y' or MultImg == 'Y' or MultImg == 'yes' or MultImg == 'Yes' or MultImg == 'YesDup':
    imgDup = True
    imgInc = 1
    OriginalName = BaseOriginalName+str(startingNum)+'_'+str(imgInc)+'.tif'
    DifferenceName = BaseMedName+str(startingNum)+'_'+str(imgInc)+'.tif'
else:
    imgDup = False
    OriginalName = BaseOriginalName+str(startingNum)+'.tif'
    DifferenceName = BaseMedName+str(startingNum)+'.tif'
print('MultImg response: {} and imgDup response {}'.format(MultImg,imgDup))

if TakeNeighbors == 'y' or TakeNeighbors == 'Y' or TakeNeighbors == 'yes' or TakeNeighbors == 'Yes' or TakeNeighbors == 'YesNeighbors' or TakeNeighbors == 'yesneighbors':
    useAdjacents = True
    print('UseAdjacents is set to be True')
else:
    useAdjacents = False

if NeedFlagMap == 'No' or NeedFlagMap == 'no' or NeedFlagMap == 'N' or NeedFlagMap == 'n' or NeedFlagMap == 'NoFlag' or NeedFlagMap == 'noflag':
    NeedFlag = False
else:
    NeedFlag = True #I want the default to be true as usually we should make a flag map, this is really only if an error occurs in the filtering step

if not os.path.exists(FilteredPath):
    #path didn't exist so we just made it
    os.makedirs(FilteredPath)
    #os.makedirs(NoisePath)
else:
    #path did exist so we should either increment or overwrite
    OverWrite = input("Folder Exists: Overwrite? [Y] or [N]\n")
    if OverWrite == 'Y' or OverWrite == "y":
        pass    #Filtered Path stays the same
    elif OverWrite == 'N' or OverWrite == 'n':
        NewFilteredPath = input("Enter a new folder name:\n")
        FilteredPath = ImagePath+NewFilteredPath+'/'
        #NoisePath = ImagePath+'Noise/'+NewFilteredPath
        os.makedirs(FilteredPath)
        #os.makedirs(NoisePath)
    else:
        print('You didnt put Y or N')
FlaggedPath = FilteredPath+'FlaggedImages/'
if not os.path.exists(FlaggedPath):
    #path didn't exist so we just made it
    os.makedirs(FlaggedPath)

i = 1
OpenMed = []    #precreating arrays and I'll be getting median and standard deviation values for each open beam image
OpenStd = []
OpenMax = []
while i<=OpenNum:
    OpenName = ImagePath+OpenBaseName+str(i)+'.tif'
    OpenImg = cv2.imread(OpenName,-1)
    if i == 1:
        #for the first image, I want to get some things like image size and pull up a ROI selector to get the open beam section
        imgSize = OpenImg.shape
        imgWidth = int(imgSize[1])        
        imgHeight = int(imgSize[0])
        OpenMaxx = np.max(OpenImg)   #want to get the max value so I stretch it for ROI selector
        OpenROI = cv2.selectROI('Select ROI with only open beam',OpenImg*int(BitMax/OpenMaxx))
        #print(OpenROI)
        if not np.any((OpenROI)):
            print('contains only zeros, using defaults')
            OpenROI = np.array([190,130,160,240])   
    #the order here is weird as we need rows then columns meaning y_start to y_start+height then x_start to x_start+width
    OpenCroppedSection = OpenImg[OpenROI[1]:(OpenROI[1]+OpenROI[3]),OpenROI[0]:(OpenROI[0]+OpenROI[2])]
    #now I want to get some statistics on this such as median value, std deviation and such
    OpenMed.append(np.median(OpenCroppedSection))
    OpenStd.append(np.std(OpenCroppedSection))
    OpenMax.append(np.max(OpenCroppedSection))
    print('The median open beam value is {}, with standard deviation of {} and max of {}'.format(OpenMed[i-1],OpenStd[i-1],OpenMax[i-1]))
    #iterate
    i+=1
    del OpenImg  #need to delete this so I can reopen without saving to new spot
    gc.collect()
#now that we've gone through this, we can get averages for these 
AvgOpenMed = np.mean(OpenMed)   #these are means of the median, std dev, and max values for each open beam 
AvgOpenStd = np.mean(OpenStd)
AvgOpenMax = np.mean(OpenMax)

#if a pixel blooms it will overflow into neighboring pixels, the amount of leftover charge will decrease further from center, so I will have a lower tolerance (2std) for bloomed regtions
#I can test for if something is bloomed based on how many neighboring pixels are affected
NoiseThresh = AvgOpenStd*NoisePercent
NoiseThreshBloom = AvgOpenStd*BloomNoisePercent

#now I want to filter the open beam images as well
if NeedMedDif == True:
    i = 1
    while i <= OpenNum:
        OpenName = ImagePath+OpenBaseName+str(i)+'.tif'
        OpenImg = cv2.imread(OpenName,-1)
        MedOpen = MedianFilterImage(OpenImg,5)
        DiffOpen = cv2.subtract(OpenImg.astype(np.float32),MedOpen.astype(np.float32)) 
        cv2.imwrite(MedDifPath+'OpenBeam_MedDif'+str(i)+'.tif',DiffOpen)
        i +=1
        del OpenImg
        gc.collect()

i = 1
while i <= OpenNum:
    OpenName = ImagePath+OpenBaseName+str(i)+'.tif'
    OpenDiffName = MedDifPath+'OpenBeam_MedDif'+str(i)+'.tif'
    OpenImg = cv2.imread(OpenName,-1)
    DiffArray = cv2.imread(OpenDiffName,-1)
    FlagMap = np.zeros((imgHeight,imgWidth),dtype=np.uint16)
    row = 0
    column = 0
    while row <= (imgHeight-2):  #previously was imgHeight-2 but I now am doing end at imgHeight -5
        while column <= (imgWidth-2):    #same with width
            #print('The row we are looking at is {} image height is {} | the column looking at is {} image width is {}'.format(row,imgHeight,column,imgWidth))
            if np.abs(DiffArray[row,column]) >= NoiseThresh and FlagMap[row,column] == 0:
                #so we are at a pixel with noise that hasnt been previously flagged, it is time to track the noise and determine cluster size
                trackNoise(column,row,imgWidth,imgHeight,DiffArray,FlagMap)
                #now that the noise at this location has been flagged, the FlagMap should have been updated
            column += 1
        row += 1
        column = 0
    #ok now we have gone through all of the pixels and flagged the noise for those pixels
    #first, I want to save the flag map as a csv just to have
    cv2.imwrite(FlaggedPath+'FlaggedOpenBeam_'+str(i)+'.tif',FlagMap)
    #now that we have this, I need to filter the image based off of the flag map
    FilteredImage = OpenImg
    filterNoiseSingleRadiograph(FlagMap,FilteredImage)
    #now that I have filtered the image, I can save it
    cv2.imwrite(FilteredPath+'FilteredOpenBeam_'+str(i)+'.tif',FilteredImage)
    i += 1

#first thing I want to do is fill up the noise array by doing a 5x5 sweep looking at the median pixel value and then if it is above median threshold of X, it gets filled out.
#then i'll go into the actual filter to replace values making sure to not include any other noisy neighbors
inc = 0
i = int(startingNum)
iflt = startingNum
dupInc = 1
if useAdjacents == False: 
    while inc < imgnum:
        #load in the original image and the median difference array
        if imgDup == True:
            #this will alternate for each image since we will have 3 loaded in at a time and usually only have 2 duplicates
            if BaseNumType == 'Float':
                OriginalName = BaseOriginalName+str(iflt)+'_'+str(dupInc)+'.tif'
            elif BaseNumType == 'TripleInteger':
                OriginalName = BaseOriginalName+str("{:03d}".format(i))+'_'+str(dupInc)+'.tif'
            elif BaseNumType == 'Integer':
                OriginalName = BaseOriginalName+str(i)+'_'+str(dupInc)+'.tif'
            else:
                print('Input number type was not Float, TripleInteger, or Integer')
                raise Exception
            if MedNumType == 'Float':
                DifferenceName = BaseMedName+str(iflt)+'_'+str(dupInc)+'.tif'
            elif MedNumType == 'TripleInteger':
                DifferenceName = BaseMedName+str("{:03d}".format(i))+'_'+str(dupInc)+'.tif'
            elif MedNumType == 'Integer':
                DifferenceName = BaseMedName+str(i)+'_'+str(dupInc)+'.tif'
            Original = cv2.imread(ImagePath+OriginalName,-1)
            if NeedMedDif == True:
                MedArray = MedianFilterImage(Original,5)
                DiffArray = cv2.subtract(Original.astype(np.float32),MedArray.astype(np.float32)) 
                cv2.imwrite(MedDifPath+DifferenceName,DiffArray)
            else:
                DiffArray = cv2.imread(MedDifPath+DifferenceName,-1)
            if iflt == startingNum:
                imgSize = Original.shape
                imgWidth = int(imgSize[1])        
                imgHeight = int(imgSize[0])         
                #dupInc += 1
        else:
            if BaseNumType == 'Float':
                OriginalName = BaseOriginalName+str(iflt)+'.tif'
            elif BaseNumType == 'TripleInteger':
                OriginalName = BaseOriginalName+str("{:03d}".format(i))+'.tif'
            elif BaseNumType == 'Integer':
                OriginalName = BaseOriginalName+str(i)+'.tif'
            else:
                print('Input number type was not Float, TripleInteger, or Integer')
                raise Exception
            if MedNumType == 'Float':
                DifferenceName = BaseMedName+str(iflt)+'.tif'
            elif MedNumType == 'TripleInteger':
                DifferenceName = BaseMedName+str("{:03d}".format(i))+'.tif'
            elif MedNumType == 'Integer':
                DifferenceName = BaseMedName+str(i)+'.tif'
            Original = cv2.imread(ImagePath+OriginalName,-1)
            if NeedMedDif == True:
                MedArray = MedianFilterImage(Original,5)
                DiffArray = cv2.subtract(Original.astype(np.float32),MedArray.astype(np.float32))
                cv2.imwrite(MedDifPath+DifferenceName,DiffArray)
            else:
                DiffArray = cv2.imread(MedDifPath+DifferenceName,-1)
        if NeedFlag == True:
            #create the flag map that will be used to track clusters adn which things have already been used
            FlagMap = np.zeros((imgHeight,imgWidth),dtype=np.uint16)
            row = 0
            column = 0
            while row <= (imgHeight-2):  #previously was imgHeight-2 but I now am doing end at imgHeight -5
                while column <= (imgWidth-2):    #same with width
                    #print('The row we are looking at is {} image height is {} | the column looking at is {} image width is {}'.format(row,imgHeight,column,imgWidth))
                    if np.abs(DiffArray[row,column]) >= NoiseThresh and FlagMap[row,column] == 0:
                        #so we are at a pixel with noise that hasnt been previously flagged, it is time to track the noise and determine cluster size
                        trackNoise(column,row,imgWidth,imgHeight,DiffArray,FlagMap)
                        #now that the noise at this location has been flagged, the FlagMap should have been updated
                    column += 1
                row += 1
                column = 0
            #ok now we have gone through all of the pixels and flagged the noise for those pixels
            #first, I want to save the flag map as a csv just to have
            if imgDup == True:
                #np.savetxt(FilteredPath+'FlaggedNoise_'+str(iflt)+'_'+str(dupInc)+'.csv',FlagMap,delimiter=',')
                cv2.imwrite(FlaggedPath+FlagBaseName+str(inc)+'_'+str(dupInc)+'.tif',FlagMap)
            else:
                #np.savetxt(FilteredPath+'FlaggedNoise_'+str(iflt)+'.csv',FlagMap,delimiter=',')
                cv2.imwrite(FlaggedPath+FlagBaseName+str(inc)+'.tif',FlagMap)
            #now that we have this, I need to filter the image based off of the flag map
        elif NeedFlag == False:
            if imgDup == True:
                FlagMap = cv2.imread(FlaggedPath+FlagBaseName+str(inc)+'_'+str(dupInc)+'.tif',-1)
            else:
                FlagMap = cv2.imread(FlaggedPath+FlagBaseName+str(inc)+'.tif',-1)
        FilteredImage = Original
        filterNoiseSingleRadiograph(FlagMap,FilteredImage)
        #now that I have filtered the image, I can save it
        if imgDup == True:
            cv2.imwrite(FilteredPath+OutputBaseName+str(i)+'_'+str(dupInc)+'.tif',FilteredImage)
        else:
            cv2.imwrite(FilteredPath+OutputBaseName+str(i)+'.tif',FilteredImage)
            
        if imgDup == True and dupInc == 1:
            dupInc = 2
        elif imgDup == True and dupInc == 2:
            dupInc = 1
            iflt = iflt + np.round(degInc,1)
            i += 1
            inc += 1
        else:    
            i += 1
            inc += 1
            iflt = iflt + np.round(degInc,1)
elif useAdjacents == True:
    if NeedFlag == True:
        while inc < imgnum:
            #load in the original image and the median difference array
            if imgDup == True:
                #print('Within if statement')
                #this will alternate for each image since we will have 3 loaded in at a time and usually only have 2 duplicates
                if BaseNumType == 'Float':
                    OriginalName = BaseOriginalName+str(iflt)+'_'+str(dupInc)+'.tif'
                elif BaseNumType == 'TripleInteger':
                    OriginalName = BaseOriginalName+str("{:03d}".format(i))+'_'+str(dupInc)+'.tif'
                elif BaseNumType == 'Integer':
                    OriginalName = BaseOriginalName+str(i)+'_'+str(dupInc)+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                if MedNumType == 'Float':
                    DifferenceName = BaseMedName+str(iflt)+'_'+str(dupInc)+'.tif'
                elif MedNumType == 'TripleInteger':
                    DifferenceName = BaseMedName+str("{:03d}".format(i))+'_'+str(dupInc)+'.tif'
                elif MedNumType == 'Integer':
                    DifferenceName = BaseMedName+str(i)+'_'+str(dupInc)+'.tif'
                #print(OriginalName)
                #OriginalName = 'EDM1mm_LeftEdge_'+str(iflt)+'_'+str(dupInc)+'.tif'
                #DifferenceName = 'EDM1mm_Left_'+str(iflt)+'MedDiff_'+str(dupInc)+'.tif'
                Original = cv2.imread(ImagePath+OriginalName,-1)
                if NeedMedDif == True:
                    MedArray = MedianFilterImage(Original,5)
                    DiffArray = cv2.subtract(Original.astype(np.float32),MedArray.astype(np.float32)) 
                    cv2.imwrite(MedDifPath+DifferenceName,DiffArray)
                else:
                    DiffArray = cv2.imread(MedDifPath+DifferenceName,-1)
                if iflt == startingNum:
                    imgSize = Original.shape
                    imgWidth = int(imgSize[1])        
                    imgHeight = int(imgSize[0])         
                    #dupInc += 1
            else:
                if BaseNumType == 'Float':
                    OriginalName = BaseOriginalName+str(iflt)+'_1.tif'                                                                      #remove the _1 from this
                elif BaseNumType == 'TripleInteger':
                    OriginalName = BaseOriginalName+str("{:03d}".format(i))+'.tif'
                elif BaseNumType == 'Integer':
                    OriginalName = BaseOriginalName+str(i)+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                if MedNumType == 'Float':
                    DifferenceName = BaseMedName+str(iflt)+'.tif'
                elif MedNumType == 'TripleInteger':
                    DifferenceName = BaseMedName+str("{:03d}".format(i))+'.tif'
                elif MedNumType == 'Integer':
                    DifferenceName = BaseMedName+str(i)+'.tif'
                Original = cv2.imread(ImagePath+OriginalName,-1)
                if NeedMedDif == True:
                    MedArray = MedianFilterImage(Original,5)
                    DiffArray = cv2.subtract(Original.astype(np.float32),MedArray.astype(np.float32))
                    cv2.imwrite(MedDifPath+DifferenceName,DiffArray)
                else:
                    DiffArray = cv2.imread(MedDifPath+DifferenceName,-1)
                #if iflt == startingNum:    #we are at the first image so the [2] spot will be different
                    #imgSize =Original.shape
                    #imgWidth = int(imgSize[0])        
                    #imgHeight = int(imgSize[1])  

            #create the flag map that will be used to track clusters adn which things have already been used
            FlagMap = np.zeros((imgHeight,imgWidth),dtype=np.uint16)
            row = 0
            column = 0
            while row <= (imgHeight-2):  #previously was imgHeight-2 but I now am doing end at imgHeight -5
                while column <= (imgWidth-2):    #same with width
                    #print('The row we are looking at is {} image height is {} | the column looking at is {} image width is {}'.format(row,imgHeight,column,imgWidth))
                    if np.abs(DiffArray[row,column]) >= NoiseThresh and FlagMap[row,column] == 0:
                        #so we are at a pixel with noise that hasnt been previously flagged, it is time to track the noise and determine cluster size
                        trackNoise(column,row,imgWidth,imgHeight,DiffArray,FlagMap)
                        #now that the noise at this location has been flagged, the FlagMap should have been updated
                    column += 1
                row += 1
                column = 0
            #ok now we have gone through all of the pixels and flagged the noise for those pixels
            #first, I want to save the flag map as a csv just to have
            if imgDup == True:
                #np.savetxt(FilteredPath+'FlaggedNoise_'+str(iflt)+'_'+str(dupInc)+'.csv',FlagMap,delimiter=',')
                cv2.imwrite(FlaggedPath+FlagBaseName+str(inc)+'_'+str(dupInc)+'.tif',FlagMap)
            else:
                #np.savetxt(FilteredPath+'FlaggedNoise_'+str(iflt)+'.csv',FlagMap,delimiter=',')
                cv2.imwrite(FlaggedPath+FlagBaseName+str(inc)+'.tif',FlagMap)
            if imgDup == True and dupInc == 1:
                dupInc = 2
            elif imgDup == True and dupInc == 2:
                dupInc = 1
                iflt = iflt + np.round(degInc,1)
                i += 1
                inc += 1
            else:     
                i += 1
                inc += 1
                iflt = iflt + np.round(degInc,1)

    #Now we have gone through the full loop getting the tracked noise for each radiograph slice. I want to go through and filter using each of these
    i = int(startingNum)
    inc = 0
    iflt = startingNum
    dupInc = 1
    while inc < imgnum:
        #load in the original image and the median difference array
        if imgDup == True:
            #print('Within if statement')
            #this will alternate for each image since we will have 3 loaded in at a time and usually only have 2 duplicates
            if iflt == startingNum:
                if BaseNumType == 'Float':
                    OriginalName1 = BaseOriginalName+str(iflt)+'_'+str(dupInc)+'.tif'               #current                                                 
                    OriginalName2 = BaseOriginalName+str(iflt+np.round(degInc,1))+'_'+str(dupInc)+'.tif'             #next degree
                    OriginalName3 = BaseOriginalName+str(maxdeg)+'_'+str(dupInc)+'.tif'      #at the start the "previous" neighbor is the last in stack
                elif BaseNumType == 'TripleInteger':
                    OriginalName1 = BaseOriginalName+str("{:03d}".format(i))+'_'+str(dupInc)+'.tif'
                    OriginalName2 = BaseOriginalName+str("{:03d}".format(i+1))+'_'+str(dupInc)+'.tif'
                    OriginalName3 = BaseOriginalName+str("{:03d}".format(maxdeg))+'_'+str(dupInc)+'.tif'    #same as before
                elif BaseNumType == 'Integer':
                    OriginalName1 = BaseOriginalName+str(i)+'_'+str(dupInc)+'.tif'
                    OriginalName2 = BaseOriginalName+str(i+1)+'_'+str(dupInc)+'.tif'
                    OriginalName3 = BaseOriginalName+str(int(maxdeg))+'_'+str(dupInc)+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                FlagName1 = FlaggedPath+FlagBaseName+str(i)+'_'+str(dupInc)+'.tif'
                FlagName2 = FlaggedPath+FlagBaseName+str(i+1)+'_'+str(dupInc)+'.tif'
                FlagName3 = FlaggedPath+FlagBaseName+str(int(imgnum-1))+'_'+str(dupInc)+'.tif'
            elif inc == (imgnum-1):
                if BaseNumType == 'Float':
                    OriginalName1 = BaseOriginalName+str(iflt)+'_'+str(dupInc)+'.tif'               #current
                    OriginalName2 = BaseOriginalName+str(startingNum)+'_'+str(dupInc)+'.tif'        #next degree is actually starting degree
                    OriginalName3 = BaseOriginalName+str(iflt-np.round(degInc,1))+'_'+str(dupInc)+'.tif'             #previous
                elif BaseNumType == 'TripleInteger':
                    OriginalName1 = BaseOriginalName+str("{:03d}".format(i))+'_'+str(dupInc)+'.tif'
                    OriginalName2 = BaseOriginalName+str("{:03d}".format(int(startingNum)))+'_'+str(dupInc)+'.tif'
                    OriginalName3 = BaseOriginalName+str("{:03d}".format(i-1))+'_'+str(dupInc)+'.tif'
                elif BaseNumType == 'Integer':
                    OriginalName1 = BaseOriginalName+str(i)+'_'+str(dupInc)+'.tif'
                    OriginalName2 = BaseOriginalName+str(int(startingNum))+'_'+str(dupInc)+'.tif'
                    OriginalName3 = BaseOriginalName+str(i-1)+'_'+str(dupInc)+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                FlagName1 = FlaggedPath+FlagBaseName+str(i)+'_'+str(dupInc)+'.tif'
                FlagName2 = FlaggedPath+FlagBaseName+str(0)+'_'+str(dupInc)+'.tif'
                FlagName3 = FlaggedPath+FlagBaseName+str(i-1)+'_'+str(dupInc)+'.tif'
            else:
                if BaseNumType == 'Float':
                    OriginalName1 = BaseOriginalName+str(iflt)+'_'+str(dupInc)+'.tif'               #current
                    OriginalName2 = BaseOriginalName+str(iflt+np.round(degInc,1))+'_'+str(dupInc)+'.tif'             #next   
                    OriginalName3 = BaseOriginalName+str(iflt-np.round(degInc,1))+'_'+str(dupInc)+'.tif'             #previous
                elif BaseNumType == 'TripleInteger':
                    OriginalName1 = BaseOriginalName+str("{:03d}".format(i))+'_'+str(dupInc)+'.tif'
                    OriginalName2 = BaseOriginalName+str("{:03d}".format(i+1))+'_'+str(dupInc)+'.tif'
                    OriginalName3 = BaseOriginalName+str("{:03d}".format(i-1))+'_'+str(dupInc)+'.tif'
                elif BaseNumType == 'Integer':
                    OriginalName1 = BaseOriginalName+str(i)+'_'+str(dupInc)+'.tif'
                    OriginalName2 = BaseOriginalName+str(i+1)+'_'+str(dupInc)+'.tif'
                    OriginalName3 = BaseOriginalName+str(i-1)+'_'+str(dupInc)+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                FlagName1 = FlaggedPath+FlagBaseName+str(inc)+'_'+str(dupInc)+'.tif'
                FlagName2 = FlaggedPath+FlagBaseName+str(inc+1)+'_'+str(dupInc)+'.tif'
                FlagName3 = FlaggedPath+FlagBaseName+str(inc-1)+'_'+str(dupInc)+'.tif'
            Original1 = cv2.imread(ImagePath+OriginalName1,-1)
            Original2 = cv2.imread(ImagePath+OriginalName2,-1)
            Original3 = cv2.imread(ImagePath+OriginalName3,-1)
            FlagMap1 = cv2.imread(FlagName1,-1)
            FlagMap2 = cv2.imread(FlagName2,-1)
            FlagMap3 = cv2.imread(FlagName3,-1)
        else:
            if iflt == startingNum:
                if BaseNumType == 'Float':
                    OriginalName1 = BaseOriginalName+str(iflt)+'_1.tif'                                                     #remove the _1 from this
                    OriginalName2 = BaseOriginalName+str(iflt+np.round(degInc,1))+'_1.tif'                                  #remove the _1 from this               
                    OriginalName3 = BaseOriginalName+str(maxdeg)+'_1.tif'                                                   #remove the _1 from this
                elif BaseNumType == 'TripleInteger':
                    OriginalName1 = BaseOriginalName+str("{:03d}".format(i))+'.tif'
                    OriginalName2 = BaseOriginalName+str("{:03d}".format(i+1))+'.tif'
                    OriginalName3 = BaseOriginalName+str("{:03d}".format(maxdeg))+'.tif'
                elif BaseNumType == 'Integer':
                    OriginalName1 = BaseOriginalName+str(i)+'.tif'
                    OriginalName2 = BaseOriginalName+str(i+1)+'.tif'
                    OriginalName3 = BaseOriginalName+str(int(maxdeg))+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                FlagName1 = FlaggedPath+FlagBaseName+str(inc)+'.tif'
                FlagName2 = FlaggedPath+FlagBaseName+str(inc+1)+'.tif'
                FlagName3 = FlaggedPath+FlagBaseName+str(int(imgnum))+'.tif'
            elif inc == imgnum:
                if BaseNumType == 'Float':
                    OriginalName1 = BaseOriginalName+str(iflt)+'_1.tif'                                                   #remove the _1 from this
                    OriginalName2 = BaseOriginalName+str(startingNum)+'_1.tif'                                            #remove the _1 from this
                    OriginalName3 = BaseOriginalName+str(iflt-np.round(degInc,1))+'_1.tif'                                #remove the _1 from this
                elif BaseNumType == 'TripleInteger':
                    OriginalName1 = BaseOriginalName+str("{:03d}".format(i))+'.tif'
                    OriginalName2 = BaseOriginalName+str("{:03d}".format(int(startingNum)))+'.tif'
                    OriginalName3 = BaseOriginalName+str("{:03d}".format(i-1))+'.tif'
                elif BaseNumType == 'Integer':
                    OriginalName1 = BaseOriginalName+str(i)+'.tif'
                    OriginalName2 = BaseOriginalName+str(int(startingNum))+'.tif'
                    OriginalName3 = BaseOriginalName+str(i-1)+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                FlagName1 = FlaggedPath+FlagBaseName+str(inc)+'.tif'
                FlagName2 = FlaggedPath+FlagBaseName+str(0)+'.tif'
                FlagName3 = FlaggedPath+FlagBaseName+str(inc-np.round(degInc,1))+'.tif'
            else:
                if BaseNumType == 'Float':
                    OriginalName1 = BaseOriginalName+str(iflt)+'_1.tif'                                                    #remove the _1 from this
                    OriginalName2 = BaseOriginalName+str(iflt+1)+'_1.tif'                                                  #remove the _1 from this
                    OriginalName3 = BaseOriginalName+str(iflt-1)+'_1.tif'                                                  #remove the _1 from this
                elif BaseNumType == 'TripleInteger':
                    OriginalName1 = BaseOriginalName+str("{:03d}".format(i))+'.tif'
                    OriginalName2 = BaseOriginalName+str("{:03d}".format(i+1))+'.tif'
                    OriginalName3 = BaseOriginalName+str("{:03d}".format(i-1))+'.tif'
                elif BaseNumType == 'Integer':
                    OriginalName1 = BaseOriginalName+str(i)+'.tif'
                    OriginalName2 = BaseOriginalName+str(i+1)+'.tif'
                    OriginalName3 = BaseOriginalName+str(i-1)+'.tif'
                else:
                    print('Input number type was not Float, TripleInteger, or Integer')
                    raise Exception
                FlagName1 = FlaggedPath+FlagBaseName+str(i)+'.tif'
                FlagName2 = FlaggedPath+FlagBaseName+str(i+1)+'.tif'
                FlagName3 = FlaggedPath+FlagBaseName+str(i-1)+'.tif'
            Original1 = cv2.imread(ImagePath+OriginalName1,-1)
            Original2 = cv2.imread(ImagePath+OriginalName2,-1)
            Original3 = cv2.imread(ImagePath+OriginalName3,-1)
            FlagMap1 = cv2.imread(FlagName1,-1)
            FlagMap2 = cv2.imread(FlagName2,-1)
            FlagMap3 = cv2.imread(FlagName3,-1)

        #now that we have this, I need to filter the image based off of the flag map
        FilteredImage1 = Original1
        filterNoiseNeighbors(FlagMap1,FilteredImage1,FlagMap2,Original2,FlagMap3,Original3)
        #now that I have filtered the image, I can save it
        if imgDup == True:
            cv2.imwrite(FilteredPath+OutputBaseName+str(inc)+'_'+str(dupInc)+'.tif',FilteredImage1)
        else:
            cv2.imwrite(FilteredPath+OutputBaseName+str(inc)+'.tif',FilteredImage1)

        if imgDup == True and dupInc == 1:
            dupInc = 2
        elif imgDup == True and dupInc == 2:
            dupInc = 1
            iflt = iflt + np.round(degInc,1)
            i += 1
            inc += 1
        else:    
            i += 1
            inc += 1
            iflt = iflt + np.round(degInc,1)