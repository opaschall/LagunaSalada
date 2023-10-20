#!/usr/bin/env bash

# used this command to cut the existing grids:
# the +c after the -F polygon argument isn't working
# gmt grdcut geo_20171025_20171106_justphs_small.4alks_20rlks.tif -R-116.5/-114.5/31.5/33 -Fbox3.txt -Ggeo_20171025_20171106_cut_small.tif
# gmt grdcut geo_20171025_20171106_justphs_large.4alks_20rlks.tif -R-116.5/-114.5/31.5/33 -Fbox2.txt -Ggeo_20171025_20171106_cut_large.tif

# Make files for masking out the external area
# gmt grdmask box3.txt -Gmask_small.grd -I0.001/0.001 -R-116/-114.9/32/33 # Tried both with .tif output
# gmt grdmask box2.txt -Gmask_large.grd -I0.001/0.001 -R-116/-114.9/32/33

# Now do gridmath 
# Rowena's note: 
# gmt grdmath (-R, etc. stuff if needed) newmask.tif 0 NAN fullint.tif MUL = masked.tif
# Mine:
# gmt grdmath -R-116/-114.9/32/33 mask_small.tif 0 NAN geo_20171025_20171106_cut_large.tif 1 MUL = mask_small_final.tif

gmt begin Finesst_figure_2 png

    # this was for making background match my poster for AGU 2022
    #gmt set PS_PAGE_COLOR 255/238/170

    # could put a shaded relief map in the background here
    # cut the combined grd file to the right size for my map. Only needed to run this once 
    # gmt grdcut 114_116.grd -R-116/-114.9/32/33 -Gcropped_dem.grd
    
    # now see the range of elevation values for shading. Did this in command line:
    # gmt grdinfo cropped_dem.grd 
    # min:-88.55    max: 1817.59

    gmt makecpt -CgrayC -T-100/2000
        # making our own scaled color palette file 
        # -T tells it minimum and maximum (this will be elevation)
        # this applies to both subplots

    # plot basemap 
    gmt basemap -R-116/-114.9/32/33 -JM15c -B

    # plot the dem 
    gmt grdimage cropped_dem.grd -R-116/-114.9/32/33 -Igrdgradient.grd -JM15c -BWsNE

    gmt coast -R-116/-114.9/32/33 -JM15c -Lg-115.7/32.9+w30k+l+f -N1/thick
    # could add -Gwheat -Slightblue if no geotiff
    # -Slightblue wanted to fill in water with blue but couldn't get it to work. 

    gmt makecpt -Crainbow -T-3.14159/3.14159
    # plot a geotiffs (interferograms) 
    gmt grdimage geo_20180926_20181231_cut_large.tif -R-116/-114.9/32/33 -JM15c -Q -nn
    gmt grdimage geo_20180926_20181231_cut_small.tif -R-116/-114.9/32/33 -JM15c -Q -nn


    # plot the regions of focus 
    gmt plot -R-116/-114.9/32/33 -JM15c -B -W3p,black box2.txt
    gmt plot -R-116/-114.9/32/33 -JM15c -B -W3p,black box3.txt
    
    # make a color bar
    gmt colorbar -R-116/-114.9/32/33 -JM15c -B+l"LOS displacement (cm)" -Dg-115/32.05+w6c/0.70c+m  -W0.44138251769

    # how did I calculate the scale factor? 
    # 5.5465763 cm is the wavelength of Sentinel 
    # which equals 4*pi 
    # calculated with 5.5465763/(4*pi) = 0.44138251769

    # below is the location of the evaporation pond for Cerro Prieto but just add arrow to entire area of defo 
    #echo -115.265533 32.399625 | gmt plot -R-116/-114.9/32/33 -JM15c -B -Gblack -St0.3c # Cerro Prieto geothermal 



gmt end