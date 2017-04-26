	# ---------------------------------------------------------------------------
# Process_800m_PRISM_Images_from_OSU.py
#
# 1) Extract the folders containing .bil files from PRISM variables
# 2) Convert the .bil files to .tif (no need to reproject since these data are already projected as NAD83)
# 3) Create yearly datasets for precipitation, tmin, tmax, and tmean
#
# Author: Gerardo Armendariz
# Created on: Tuesday, January 6th 2015
# Updated on: Wednesday, April 25th 2017
# ---------------------------------------------------------------------------

# Import system modules
import sys, string, os, arcpy, time, datetime, gzip,zipfile, ftplib
from datetime import datetime 
from arcpy import env
from arcpy.sa import *
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

#projections informatiomn
#in_datum = r"C:\Users\garmendariz.TUCSON\AppData\Roaming\ESRI\Desktop10.1\ArcMap\Coordinate Systems\NAD 1983 HARN.prj"
#wgs84_cs = r"C:\Users\garmendariz.TUCSON\AppData\Roaming\ESRI\Desktop10.1\ArcMap\Coordinate Systems\WGS 1984.prj"
#wgs84z12_cs = r"C:\Users\garmendariz.TUCSON\AppData\Roaming\ESRI\Desktop10.1\ArcMap\Coordinate Systems\WGS 1984 UTM Zone 12N.prj"
#azBoundary = r"C:\my\GIS\States\AZ\AZ_Boundary\arizona_utm.shp"

# snap rasters are being used in order to run Resample_management tool
#snapRaster4km = r"H:\PRISM\4km\ppt\Yearly\us_ppt_1895.14.tif"
#snapRaster500m = r"H:\MODIS\modis_yearly_1242013\modis_1-1-2000.tif"
#snapRaster30m = r"Q:\gis\landsat\AZ_Landsat_Seasonal\AZ_2011_fall_tvfc.tif"

PRISM_DIRECTORY ="/Volumes/Drobo/Root/data/PRISM/PRISM_dat_OSU/"

def main():
	# record script run time
	startTime = datetime.now()
	
	#### UNZIP PRISM Datasets
	#unzipPRISMData("ppt")
	#unzipPRISMData("tmin")
	#unzipPRISMData("tmax")
	#unzipPRISMData("tmean")

	### CONVERT TO GEOTIFF
	convertMonthlyPRISMImageryToTIFF("ppt")
	#convertMonthlyPRISMImageryToTIFF("tmin")
	#convertMonthlyPRISMImageryToTIFF("tmax")
	#convertMonthlyPRISMImageryToTIFF("tmean")

	### CREATE YEARLY AVERAGE DATASETS
	#averagePRISMImagery_MonthlyToYearly("ppt")
	#averagePRISMImagery_MonthlyToYearly("tmin")
	#averagePRISMImagery_MonthlyToYearly("tmax")
	#averagePRISMImagery_MonthlyToYearly("tmean")


###############################
#  Unzip all the source files and save the bil files to the same directory
###############################
def unzipPRISMData(prism_variable):
	try:
		# iterate through each of the year range folders and unzip the files
		monthlyRangeFolder = "E:/data/PRISM/PRISM_data_OSU/" + prism_variable
		for root, dirs, files in os.walk(monthlyRangeFolder):
			for file in files:
				print("Processing: " + file)
				currFile = os.path.abspath(os.path.join(root, file))
				currFileDir = os.path.dirname(currFile)

				targetFileDir = os.path.abspath(os.path.join(currFileDir, '..', 'bil', prism_variable))

				print(currFile +  "     " + currFileDir)

				with zipfile.ZipFile(currFile) as zf:
					zf.extractall(targetFileDir)

	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])


###############################
#  Convert all the Monthly and Yearly images to GeoTiffs
###############################
def convertMonthlyPRISMImageryToTIFF(prism_variable):
	try:
		monthlyOutputFolder = PRISM_DIRECTORY + "geotiff/" + prism_variable + "/Monthly"
		#yearlyOutputFolder = "H:/PRISM/4km/new/" + prism_variable + "/Yearly/"
		
		# iterate through each of the year range folders
		monthlyRangeFolder = PRISM_DIRECTORY + "/bil/" + prism_variable
		for root, dirs, files in os.walk(monthlyRangeFolder):
			for file in files:
				fileExtension = os.path.splitext(file)[1]

				year = file.split(".")[0].split("_")[5][0:4]
				month = str(int(file.split(".")[0].split("_")[5][4:6]))

				#print file
				if fileExtension == ".bil" and year == "2013" and (month == "11"):
					currFile = os.path.abspath(os.path.join(root, file))
					currFileDir = os.path.dirname(currFile)

					print(file  + "    " + year + "    " + month)
					# export to GeoTif
					#env.workspace = currFileDir
					#arcpy.RasterToOtherFormat_conversion(file, monthlyOutputFolder ,"TIFF")

					print("*** Processing " + file + "  ***")
				
		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])



###############################
#  Create Yearly averages from monthly 
###############################
def averagePRISMImagery_MonthlyToYearly(prism_variable):
	try:
		monthlyOutputFolder = "E:/data/PRISM/PRISM_data_OSU/geotiff/" + prism_variable + "/Yearly"
		#yearlyOutputFolder = "H:/PRISM/4km/new/" + prism_variable + "/Yearly/"
		# iterate through each of the year range folders 
		monthlyRangeFolder = "E:/data/PRISM/PRISM_data_OSU/geotiff/" + prism_variable + "/Monthly"

		for year in range(2013,2014): #(1990,2013):
			print("Processing..." + str(year))
			jan_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "01.tif"
			feb_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "02.tif"
			mar_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "03.tif"
			apr_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "04.tif"
			may_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "05.tif"
			jun_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "06.tif"
			jul_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "07.tif"
			aug_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "08.tif"
			sep_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "09.tif"
			oct_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "10.tif"
			nov_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "11.tif"
			dec_month = "cai_" + prism_variable + "_us_us_30s_" + str(year) + "12.tif"

			jan_raster = Raster(monthlyRangeFolder + "/" + jan_month)
			feb_raster = Raster(monthlyRangeFolder + "/" + feb_month)
			mar_raster = Raster(monthlyRangeFolder + "/" + mar_month)
			apr_raster = Raster(monthlyRangeFolder + "/" + apr_month)
			may_raster = Raster(monthlyRangeFolder + "/" + may_month)
			jun_raster = Raster(monthlyRangeFolder + "/" + jun_month)
			jul_raster = Raster(monthlyRangeFolder + "/" + jul_month)
			aug_raster = Raster(monthlyRangeFolder + "/" + aug_month)
			sep_raster = Raster(monthlyRangeFolder + "/" + sep_month)
			oct_raster = Raster(monthlyRangeFolder + "/" + oct_month)
			nov_raster = Raster(monthlyRangeFolder + "/" + nov_month)
			dec_raster = Raster(monthlyRangeFolder + "/" + dec_month)

			if(prism_variable == "ppt"):
				raster_yearly = (jan_raster + feb_raster + mar_raster + apr_raster +  may_raster + jun_raster + jul_raster + aug_raster + sep_raster + oct_raster + nov_raster + dec_raster)
			else:
				raster_yearly = (jan_raster + feb_raster + mar_raster + apr_raster +  may_raster + jun_raster + jul_raster + aug_raster + sep_raster + oct_raster + nov_raster + dec_raster)/12

			raster_yearly.save(monthlyOutputFolder + "/" + "cai_" + prism_variable + "_us_us_30s_" + str(year) + ".tif")
		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])























































































###############################
#  Add the raster datasets to the Raster Catalog
###############################
def addPRISMRastersToCatalog(prism_variable, time_resolution):
	try:
		env.workspace = "H:/PRISM/4km/" + prism_variable + "/" + time_resolution
		catalogName = "C:/my/GIS/PRISM/usPRISM.gdb/conus_PRISM_4km_" + time_resolution + "_tminn_RC"

		rasters = arcpy.ListRasters("*","tif")

		rasterNames = ""
		for r in rasters:
			rasterNames = rasterNames + r + ";"

		print("Adding rasters to catalog...")			
		arcpy.RasterToGeodatabase_conversion(rasterNames, catalogName)

		print("Finished adding rasters to catalog: " + catalogName)


	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])


###############################
#  Adds the date to each of the raster datasets in the Raster Catalog 
#  based on the dataset name in the file system
###############################
def addPRISMRasterDatesToCatalog(prism_variable, time_resolution):
	try:
		catalogName = "C:/my/GIS/PRISM/usPRISM.gdb/conus_PRISM_4km_" + time_resolution + "_tminn_RC"

		updateCursor = arcpy.UpdateCursor(catalogName)

		for row in updateCursor:
			rasterName = row.Name
			date = rasterName.split(".")[0].split("_")[4]
			year = date[0:4]
			if time_resolution == "Monthly":
				month = date[4:6].lstrip("0")
				row.img_date = month + "/1/" + year
			else:
				row.img_date = "1/1/" + year
			print("Updating row: " + rasterName)
			updateCursor.updateRow(row)
			#if year == "2013":
		print("Finished updated dates for catalog: " + catalogName)
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])


###############################
#  Reproject from 4km WGS84 to WGS84 Zone12 and rename to AZ "az_"
###############################
def reprojectPRISMImagery(prism_variable, temporal_range):
	try:
		outputFolder = "H:/PRISM/4km/" + prism_variable + "/" + temporal_range + "/az/4km"
		
		# iterate through each of the year range folders
		dateRangeFolder = "H:/PRISM/4km/" + prism_variable + "/" + temporal_range + "/az"
		
		for root, dirs, files in os.walk(dateRangeFolder):	
			for file in files:
				print(file)
				fileNameArray = file.split(".")
				if(fileNameArray[2] == 'tif' and len(fileNameArray) == 3):
					sourceFileName = dateRangeFolder + "/" + fileNameArray[0] + "." + fileNameArray[1] + ".tif"
					azFileName = outputFolder + "/" + str(fileNameArray[0]).replace("us", "az") + "." + fileNameArray[1] + ".tif"
					print(azFileName)
					# define the image spatial reference for the US image
					arcpy.ProjectRaster_management(sourceFileName,azFileName,wgs84z12_cs,"NEAREST",4307.10933863036,"","","")

		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])


###############################
#  Rename raster datasets
###############################
def renamePRISMImagery(prism_variable, temporal_range):
	try:
		outputFolder = "H:/PRISM/4km/" + prism_variable + "/" + temporal_range + "/az/4km"
		
		# iterate through each of the year range folders
		dateRangeFolder = "H:/PRISM/4km/" + prism_variable + "/" + temporal_range + "/az"
		
		env.workspace = dateRangeFolder
		
		for root, dirs, files in os.walk(dateRangeFolder):	
			for file in files:
				print(file)
				fileNameArray = file.split(".")
				if(fileNameArray[2] == 'tif' and len(fileNameArray) == 3):
					sourceFileName = dateRangeFolder + "/" + fileNameArray[0] + "." + fileNameArray[1] + ".tif"
					azFileName = outputFolder + "/" + str(fileNameArray[0]).replace("us", "az") + "." + fileNameArray[1] + ".tif"
					print(azFileName)
					# define the image spatial reference for the US image
					arcpy.ProjectRaster_management(sourceFileName,azFileName,wgs84z12_cs,"NEAREST",4307.10933863036,"","","")

		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])



###############################
#  Calculate tmean from tmin and tmax
###############################
def caculatePRISMTMean():
	try:
		tminDir = "H:\\PRISM\\4km\\tmin\\Monthly\\az\\30m\\"
		tmaxDir = "H:\\PRISM\\4km\\tmax\\Monthly\\az\\30m\\"

		tmeanDir = "H:\\PRISM\\4km\\tmean\\Monthly\\az\\30m"

		clip = "H:\\Landsat\\landsat_1984.06.20.tif"
		
		tempWorkspace = "C:\\my\\GIS\\temp\\temp_processing\\"
		env.workspace = tminDir
		
		rasters = arcpy.ListRasters()

		env.workspace = tempWorkspace
		for r in rasters:
			year = int(r.split(".")[0].split("_")[2])
			month = int(r.split(".")[1])
			if(year > 1980 and year < 2012):
				print("Processing: " + r)
				r_min = Raster(tminDir + r)
				r_max = Raster(tmaxDir + r.replace("tmin","tmax"))

				r_mean = (r_max + r_min)/2

				r_mean_by_mask = ExtractByMask(r_mean,clip)

				r_mean_by_mask.save(tmeanDir + "\\cc" + str(year) + "-" + str(month) + ".tif")

				arcpy.RasterToOtherFormat_conversion(tmeanDir + "\\cc" + str(year) + "-" + str(month) + ".tif",tmeanDir + "\\grid","GRID")

		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])



###############################
#  Convert tmin datasets to grids for a specific folder of tif images
###############################
def convertPRISMTmeanToGrid():
	try:
		outputFolder = "C:\\my\\tmean_grid\\"
		
		# iterate through each of the year range folders
		dateRangeFolder = "C:\\my\\tmean\\"
		
		env.workspace = dateRangeFolder
		
		rasters = arcpy.ListRasters("*","tif")

		for r in rasters:
			print(r)
			
			#newName = r.replace(".tif","")
			#newName = newName.replace("studyarea_30m_prism_mo_tmean_","")
			#print newName
			arcpy.RasterToOtherFormat_conversion(r,outputFolder,"GRID")

			

		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])




###############################
#  Renames PRISM datasets
###############################
def renamePRISMrastersSubset():
	try:
		outputFolder = "P:\\arcmap\\Cienega_Creek_Study_Area_Analysis\\Cienega Creek Study Area 30m PRISM\\tmean\\"
		
		env.workspace = outputFolder
		
		rasters = arcpy.ListRasters("*","TIF")

		for r in rasters:
			if (len(r) < 20):
				print(r)
				newName = r.replace(".","_")
				newName = newName.replace("_tif",".tif")
				arcpy.Rename_management(r, newName)
			elif(len(r) > 20):
				print(r)
				newName = r.replace(".","_")
				newName = newName.replace("cc_studyarea_30m_prism_mo_tmean_","cc_")
				newName = newName.replace("_tif",".tif")
				arcpy.Rename_management(r, newName)
			

		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])

###############################
#  Renames PRISM datasets
###############################
def renamePRISMrasters():
	try:
		outputFolder = "P:\\arcmap\\Cienega_Creek_Study_Area_Analysis\\Cienega Creek Study Area 30m PRISM\\tmean\\"
		
		env.workspace = outputFolder
		
		rasters = arcpy.ListRasters("*","TIF")

		for r in rasters:
			print(r)
			arcpy.Rename_management(r, r.replace("cc_","cc_studyarea_30m_prism_mo_tmean_"))
			

		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])


###############################
#  Clips a list of rasters based on the spatial extent of the CC Landsat study area
###############################
def clipToLandsat(folder):
	try:
		outputFolder = "C:\\my\\" + folder + "\\clipped"

		env.workspace = "C:\\my\\" + folder + "\\resampled"

		clip =  r'C:\my\landsat.tif'
		
		if(folder == "ppt"):
			rasters = arcpy.ListRasters("*","TIF")
		else:	
			rasters = arcpy.ListRasters("*", "GRID")

		for r in rasters:
			print(r)
			outExtractByMask = ExtractByMask(r,clip)
			newName = outputFolder + "\\" + r
			outExtractByMask.save(newName)
			

		print("All Done!")
	except:
		print("*** Error ***")
		print(sys.exc_info()[0])
		print(sys.exc_info()[1])
		print(sys.exc_info()[2])

if __name__ == "__main__":
    main()