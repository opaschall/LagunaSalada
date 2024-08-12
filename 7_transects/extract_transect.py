# data must be an array (can be complex values or not)
# start is [x, y] coordinate of starting point of transect 
#     start[0] is the x coord
#     start[1] is the y coord
# end is [x, y] coordinate of ending point of transect
# perpDist is the transect-perpendicular distance you want to average over 
# binSize is the number of pixels over which we average 

# for more detailed + commented code, see extract_transect_creating_function.ipynb
# to use this function in a notebook, use the following line of code to import it:
#     %load extract_transect.py

# output is (2,numBins) dimensions, with datatype the same as the input data

def extract_transect(data, start, end, perpDist, binSize):
    import numpy as np
    
    # normalizes the amplitudes to one so that coherence is btw 0-1
    # coherence will now be the np.abs
    
    probs = np.where(data==0)
    data[probs] = np.nan
    data = data/np.abs(data)
    
    # make sure the start and end inputs are not the same point
    if end[0]==start[0] and end[1]==start[1]:
        print('Start and end points the same. Change one of them.')
        return
    
    # vertical transect 
    if end[0]==start[0]: 
        xVal = start[0] 
        yVals = [start[1], end[1]]
        data1 = data[min(yVals):max(yVals),xVal-perpDist:xVal+perpDist]
        # if the line goes from larger to smaller y vals, flip the array 
        dy = (end[1]-start[1])
        dx = 2*perpDist
        if dy < 0:
            data1 = np.flipud(data1)
            dy = np.abs(dy)
        bins = np.arange(0,dy,binSize)
        numBins = np.shape(bins)[0]
        # ignore the very last bin, doesn't contain same amount of info as the other bins
        binnedVals=np.ndarray([numBins-1,1],'complex')
        for i in np.arange(numBins-1):
            binLow = bins[i]
            binHigh = bins[i+1]
            binnedVals[i] = np.nanmean(data1[binLow:binHigh-1,:]) 
        # make the output bin values the midpoints 
        bins0 = np.diff(bins)/2+bins[0:-1]
        # must reshape them first so that they are (1,n) dimensions
        bins1 = bins0.reshape((1,numBins-1))
        binnedVals1 = binnedVals.reshape((1,numBins-1))
        # put bins and binnedVals together in an array for output 
        output = np.vstack((bins1,binnedVals1))
        return output
    
    # horizontal transect
    if end[1]==start[1]:
        xVals = [start[0], end[0]]
        yVal = start[1]
        data1 = data[yVal-perpDist:yVal+perpDist,min(xVals):max(xVals)]
        # if the line goes from larger to smaller x vals, flip the array 
        dy = 2*perpDist
        dx = (end[0]-start[0])
        if dx < 0:
            data1 = np.fliprl(data1)
            dx = np.abs(dx)
        bins = np.arange(0,dx,binSize)
        numBins = np.shape(bins)[0]
        # ignore the very last bin, doesn't contain same amount of info as the other bins
        binnedVals=np.ndarray([numBins-1,1],'complex')
        for i in np.arange(numBins-1):
            binLow = bins[i]
            binHigh = bins[i+1]
            binnedVals[i]= np.nanmean(data1[:,binLow:binHigh-1]) 
        # make the output bin values the midpoints
        bins0 = np.diff(bins)/2+bins[0:-1]
        # must reshape them first so that they are (1,n) dimensions
        bins1 = bins0.reshape((1,numBins-1))
        binnedVals1 = binnedVals.reshape((1,numBins-1))
        # put bins and binnedVals together in an array for output 
        output = np.vstack((bins1,binnedVals1))
        return output
    
    # diagonal transect 
    dx = (end[0]-start[0])
    dy = (end[1]-start[1])
    theta = np.abs(np.arctan(dy/dx))
    # design the rotation matrix
    rot = np.zeros((2,2),'float')
    rot[0] = [np.cos(theta),np.sin(theta)]
    rot[1] = [-np.sin(theta),np.cos(theta)]
    xVals = [start[0], end[0]]
    yVals = [start[1], end[1]]
    # pull out just the data we need
    data1 = data[min(yVals):max(yVals),min(xVals):max(xVals)]
    # flip the data so that it goes from (smallX,smallY) to (largeX,largeY)
    if dx < 0:
        data1 = np.fliplr(data1)
        dx = np.abs(dx)
    if dy < 0:
        data1 = np.flipud(data1)
        dy = np.abs(dy)
    # make a grid
    x = np.arange(0,dx,1)
    y = np.arange(0,dy,1)
    grdx,grdy = np.meshgrid(x,y,indexing='xy')
    # reshape these to be x in first row, y in second row
    grdx1 = grdx.reshape(1,dx*dy)
    grdy1 = grdy.reshape(1,dx*dy)
    grd = np.vstack((grdx1,grdy1)) 
    # rotate the grid
    newxy = np.matmul(rot,grd)
    x1 = newxy[0,:].reshape((dy,dx)) # this is distance along transect
    y1 = newxy[1,:].reshape((dy,dx)) # this is distance perpendicular to transect
    # find points within perpDist of the now-horizontal (rotated) line
    ind = np.where(np.abs(y1) < perpDist)
    TsctLength = np.sqrt(dx*dx+dy*dy)
    # make bins
    bins = np.arange(0,TsctLength,binSize)
    numBins = np.shape(bins)[0]
    dists = x1[ind]
    vals = data1[ind]
    binnedVals=np.ndarray([numBins,1],'complex')
    # put mean of data within each bin into binnedVals array 
    for i in np.arange(numBins-1):
        inds = (np.where((dists >= bins[i]) & (dists < bins[i+1])))
        binnedVals[i]= np.nanmean(vals[inds]) 
    # make the output bin values the midpoints
    bins0 = np.diff(bins)/2+bins[0:-1]
    bins1 = bins0.reshape((1,numBins-1))
    binnedVals1 = binnedVals[0:-1].reshape((1,numBins-1))
    output = np.vstack((bins1,binnedVals1))
    # output is all complex 
    # what matters is real part of the bins (same as output[0])
        # if using this function across an igram, np.angle of binnedVals (output[1]) is what matters THIS MAY NOT BE TRUE
    return output