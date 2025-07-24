import numpy as np

def ver2patchconnect(faultstruct, targetLp, Wp, faultnp):
    # faultstruct is a list of fault attributes like strike, dip, location, etc. for each fault 
    # targetLp is the total subdivisions along the length (L) of the (each?) fault 
    # Wp is the number of subdivisions along width (W) of (each?) fault
    # faultnp is how many faults per break. Put this in brackets always (even if just one segment)  

    # how many faults are there? 
    numfaults = len(faultstruct)

    # breakno list tells us which fault belongs to which break 
    if len(faultnp) > 1:
        breakno = []
        idx = 0
        for count in faultnp:
            breakno.extend([idx + 1] * count)
            idx += 1
    else:
        breakno = faultnp

    # total length of (all?) faults
    totL = sum(fault['L'] for fault in faultstruct)

    # total number of patches along length of fault 
    totLp = 0
    # list of patch counts per fault 
    Lps = []
    # Allocate patches along each fault based on length proportion 
    for fault in faultstruct:
        Lp = int(fault['L'] / totL * targetLp)
        if Lp == 0:
            Lp = 1
        Lps.append(Lp)
        totLp += Lp

    # initialize patch structure list 
    patchstruct = [None] * (totLp * Wp)
    
    # loop over faults 
    for k, fault in enumerate(faultstruct):
        xt = np.mean(fault['vertices'][0]) # fault midpoint x value 
        yt = np.mean(fault['vertices'][1]) # fault midpoint y value 
        # extract fault parameters like strike, length L, width W, dip, depth to top of fault.
        strike = fault['strike']
        L = fault['L']
        W = fault['W']
        dip = fault['dip']
        zt = fault['zt']
        # length of this patch? idk. 
        Lp = Lps[k]

        # compute geometry depending on dip direction 
        if dip > 0:
            x0 = xt + W * np.cos(np.radians(dip)) * np.cos(np.radians(strike))
            y0 = yt - W * np.cos(np.radians(dip)) * np.sin(np.radians(strike))
        else:
            x0 = xt - W * np.cos(np.radians(dip)) * np.cos(np.radians(strike))
            y0 = yt + W * np.cos(np.radians(dip)) * np.sin(np.radians(strike))
            dip = -dip

        # bottom edge depth 
        z0 = zt + W * np.sin(np.radians(dip))

        # these are the centroid coordinates of the fault 
        xs = np.mean([xt, x0])
        ys = np.mean([yt, y0])
        zs = np.mean([zt, z0])

        # computer centers for width and strike 
        dL = L / Lp
        dW = W / Wp
        dx = (xt - x0) / Wp
        dy = (yt - y0) / Wp

        # loop over patches across the depth (width) of the fault 
        for i in range(1, Wp + 1):
            xtc = xt - dx * (i - 1)      # top center x 
            x0c = xt - dx * i            # bottom center x 
            xsc = np.mean([x0c, xtc])
            ytc = yt - dy * (i - 1)
            y0c = yt - dy * i
            ysc = np.mean([y0c, ytc])
            z0p = z0 - dW * (Wp - i) * np.sin(np.radians(dip))
            ztp = z0 - dW * (Wp - i + 1) * np.sin(np.radians(dip))
            zsp = np.mean([z0p, ztp])

            # loop over patches along length of fault 
            for j in range(1, Lp + 1):
                id = (i - 1) * totLp + sum(Lps[:k]) + (Lp - j)

                # strike offsets for corners and centers
                lsina = (L / 2 - dL * (j - 1)) * np.sin(np.radians(strike))
                lsinb = (L / 2 - dL * j) * np.sin(np.radians(strike))
                lcosa = (L / 2 - dL * (j - 1)) * np.cos(np.radians(strike))
                lcosb = (L / 2 - dL * j) * np.cos(np.radians(strike))
                lsin = (L / 2 - dL * (j - 0.5)) * np.sin(np.radians(strike))
                lcos = (L / 2 - dL * (j - 0.5)) * np.cos(np.radians(strike))

                # 3D fault patch corners 
                xfault = np.array([xtc + lsina, xtc + lsinb, x0c + lsinb, x0c + lsina, xtc + lsina])
                yfault = np.array([ytc + lcosa, ytc + lcosb, y0c + lcosb, y0c + lcosa, ytc + lcosa])
                zfault = np.array([ztp, ztp, z0p, z0p, ztp])

                # midpoints 
                x0p = x0c + lsin
                y0p = y0c + lcos
                xsp = xsc + lsin
                ysp = ysc + lcos

                # putting together the fault patch structure into a list of coordinates and strike, dip, length, width, etc. 
                patchstruct[id] = {
                    'x0': x0p,
                    'y0': y0p,
                    'z0': z0p,
                    'xs': xsp,
                    'ys': ysp,
                    'zs': zsp,
                    'strike': strike,
                    'dip': dip,
                    'L': dL,
                    'W': dW,
                    'xfault': xfault,
                    'yfault': yfault,
                    'zfault': zfault,
                    'edgetype': 0,
                }

    # Patch connection info 
    if Wp > 1:
        for j in range(Wp):
            for i in range(totLp):
                id = j * totLp + i
                connect = [np.nan] * 6
                if j > 0:
                    connect[0] = id - totLp
                if j < Wp - 1:
                    connect[4] = id + totLp
                if i > 0:
                    connect[5] = id - 1
                if i < totLp - 1:
                    connect[2] = id + 1
                patchstruct[id]['connect'] = connect
    else:
        for i in range(totLp):
            id = i
            connect = [np.nan] * 4
            if i > 0:
                connect[1] = id - 1
            if i < totLp - 1:
                connect[3] = id + 1
            patchstruct[id]['connect'] = connect

    return patchstruct, totLp, Wp, Lps