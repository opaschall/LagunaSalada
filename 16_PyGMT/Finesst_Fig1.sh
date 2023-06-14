#!/usr/bin/env bash

gmt begin Finesst_figure_1 png

    # this line was for making the background match my 2022 AGU poster
    #gmt set PS_PAGE_COLOR 255/238/170
    
    # plot a geotiff 
    gmt grdimage Test_Landsat_Laguna_Salada.tif -R-118/-113/31/35 -JM15c
    
    
    gmt basemap -R-118/-113/31/35 -JM15c -B

  
    #gmt grdimage @earth_relief_01m -I -Cgray
    # -I is illumination
    # -C changes the color map tables, this one is grayscale 

    gmt coast -R-118/-113/31/35 -JM15c -Lg-117.3/31.2+w100k+l+f -F+gwhite -N1/thickest -N2/thick -Wthin
    # could add -Gwheat -Slightblue if no geotiff
    # this must be here to not be covered by the shaded relief, but not cover the focal mechanisms 

    # region of Junle's figure
    gmt plot -R-118/-113/31/35 -JM15c -B -W3p,blue box5.txt
    # entire SAR image that I cropped from
    gmt plot -R-118/-113/31/35 -JM15c -B -W3p,211/127/250 box4.txt
    # plot the regions of focus 
    gmt plot -R-118/-113/31/35 -JM15c -B -W3p,122/231/106 box2.txt
    gmt plot -R-118/-113/31/35 -JM15c -B -W3p,122/231/106 box3.txt


    #gmt psxy faults.txt -R-118/-113/31/35 -JM15c -B -Wblack

    # study locations in dots
    #echo -116.6 33.6 | gmt plot -R-118/-113/31/35 -JM15c -B -Gdarkgreen -Sc0.5c # Pathfinder Ranch 
    #echo -117.8 36.0 | gmt plot -R-118/-113/31/35 -JM15c -B -Gred -Sc0.5c # Coso geothermal
    #echo -115.3 32.4 | gmt plot -R-118/-113/31/35 -JM15c -B -Gblue -Sc0.5c # Cerro Prieto geothermal 
    # earthquake epicenters in stars
    #echo -117.599 35.770 | gmt plot -R-118/-113/31/35 -JM15c -B -Gred -Sa0.5c # 2019 Ridgecrest EQ epicenter, associated with Coso
    #echo -115.295 32.286 | gmt plot -R-118/-113/31/35 -JM15c -B -Gblue -Sa0.5c # 2010 Sierra El Mayor EQ epicenter, associated with Cerro Prieto



    echo -116.4 34.1 "California" | gmt pstext -R-118/-113/31/35 -JM15c -B -F+f14p+fwhite
    echo -116 31.9 "Mexico" | gmt pstext -R-118/-113/31/35 -JM15c -B -F+f14p+fwhite
    echo -113.8 33.3 "Arizona" | gmt pstext -R-118/-113/31/35 -JM15c -B -F+f14p+fwhite

    # Let's make an inset map 
    gmt inset begin -DjTR+w4c+o0.3c -F # creates an inset map
        gmt coast -R-123/-106/27/43 -JM4c -A500 -N1/thick -N2 -Gwheat -Slightblue -Wthinnest
        gmt plot -R-123/-106/27/43 -JM4c -B -W2p,red box.txt
        gmt pstext states.txt -R-123/-106/27/43 -JM4c -B -F+f9p

    gmt inset end

gmt end