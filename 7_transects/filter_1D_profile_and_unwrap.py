# defining a function to read in a 1D profile of data, filter it, unwrap it, then add the phase jumps back to the raw data
#
# inputs are:
#     data is an array of complex values with first row as X values, second row as Y values 
#     std is the standard deviation we use to filter the data 
#     cutoff is the phase change to use as a cutoff for unwrapping
#
# output is array of complex values that are now unwrapped
# with first row as X values, second row as Y values
# (each has one less data point than the input)

# for more detailed + commented code, see filter_1D_profile_and_unwrap.ipynb
# to use this function in a notebook, use the following line of code to import it:
#     %load filter_1D_profile_and_unwrap.py

def unwrap_1D(data, std, cutoff):
    import numpy as np
    from scipy.ndimage import uniform_filter
    x = data[0].real
    y = data[1]
    numPts = len(y)
    re = np.real(y)
    im = np.imag(y)
    phs = np.angle(y)
    refilt = uniform_filter(re,std)
    imfilt = uniform_filter(im,std)
    filtDat = 1j*imfilt + refilt
    cor = np.real(filtDat)
    filtPhs = np.angle(filtDat)
    unwrapped = np.ndarray(len(phs)-1,'float')
    count = 0;
    for i in np.arange(len(phs)-1):
        unwrapped[i] = filtPhs[i]+count
        jump = filtPhs[i+1]-filtPhs[i]
        if (np.abs(jump) > cutoff): 
            if (jump > 0):
                count -= 2*np.pi
            else:
                count += 2*np.pi
    dif = unwrapped - filtPhs[0:-1]
    difAdded = phs[0:-1] + dif 
    rem = np.mod(unwrapped-difAdded+np.pi,2*np.pi)-np.pi
    rem2 = unwrapped - rem
    
    # to vstack, make them (1,n) dimensional 
    newX = x[0:-1]
    outputX = newX.reshape((1,numPts-1))
    outputY = rem2.reshape((1,numPts-1))
    output = np.vstack((outputX,outputY))
    return output
