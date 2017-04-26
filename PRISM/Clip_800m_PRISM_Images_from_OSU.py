 # ---------------------------------------------------------------------------
# Process_800m_PRISM_Images_from_OSU.py
#
# Clips the PRISM imagery based on the selected variable and time range
#
# Author: Gerardo Armendariz
# Created on: Friday May 6th, 2016
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy, time, datetime, gzip, zipfile, ftplib
from datetime import datetime 
from arcpy import env
from arcpy.sa import *
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

cienegaCreekBoundary = "C:/my/GIS/States/AZ/AZ_LCNCA/CienegaCreek_boundary.shp"
outputDir = "E:/data/PRISM/800m_1895_to_2013/clipped"

def main():
    # record script run time
    startTime = datetime.now()

    clipPRISMGrids("ppt","Monthly")


###############################
#  Convert all the Monthly and Yearly images to GeoTiffs
###############################
def clipPRISMGrids(prism_variable, time):
    try:
        gridsDir = "E:/data/PRISM/800m_1895_to_2013/geotiff/" + prism_variable + "/" + time 

        arcpy.env.workspace = gridsDir

        rasters = arcpy.ListRasters("*", "TIF")
        for raster in rasters:
            print("Processing..."  + raster)
            #outExtractByMask = ExtractByMask(gridsDir + "/" + raster, cienegaCreekBoundary)
            #outExtractByMask.save(outputDir + "/" + "LCNCA_"  + raster)
                
        print "All Done!"
    except:
        print "*** Error ***"
        print sys.exc_info()[0]
        print sys.exc_info()[1]
        print sys.exc_info()[2]
