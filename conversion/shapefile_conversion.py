import os
import geopandas


# Generates a geodataframe from db given vdc and ward
def generate_geodataframe(vdc, ward):
	shp_path = construct_shapefile_path(vdc,ward)
	geo_df = convert_shapefile_to_geodataframe(shp_path)
	return geo_df


# Constructs path to shapfile given vdc and ward
def construct_shapefile_path(vdc, ward):
	# Defining various levels of path to access the plotregister excel file
	level_1 = r'D:\solu_db'
	level_2 = vdc
	level_3 = vdc + '_w' + str(ward) + '.shp'
	shapefile_path = os.path.join(level_1, level_2, level_3)
	return shapefile_path


# Convert shapefile to geopanda dataframe
def convert_shapefile_to_geodataframe(shpfile):
	try:
		geo_df = geopandas.read_file(shpfile)
		return geo_df
	except FileNotFoundError:
		print("Error: File not found")
	except Exception as e:
		print("An error occured:", e)



# 
if __name__ == "__main__":
	vdc = 'Tingla'
	ward = 1

	shp_dataframe = generate_geodataframe(vdc,ward)

	
	print(list(shp_dataframe.columns))

	