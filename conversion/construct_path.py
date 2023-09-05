import os
import pandas



# Generate Path: Given vdc and ward name,
# this function generates path of the plotregister excel file
def construct_register_path(vdc,ward):
	# Defining various levels of path to access the plotregister excel file
	level_1 = r'\\CHECK_JACHA\\Solukhumbu_LIS\\Solukhumbu_fb_pr_prd_gov'
	level_2 = vdc
	level_3 = vdc + '_w' + str(ward)
	level_4 = vdc + '_w' + str(ward) + '_prd.xlsx'

	register_path = os.path.join(level_1, level_2, level_3, level_4)
	return register_path

# Constructs path to shapfile given vdc and ward
def construct_shapefile_path(vdc, ward):
	# Defining various levels of path to access the plotregister excel file
	level_1 = r'D:\solu_db'
	level_2 = vdc
	level_3 = vdc + '_w' + str(ward) + '.shp'
	shapefile_path = os.path.join(level_1, level_2, level_3)
	return shapefile_path


if __name__ == "__main__":

	# Variables
	vdc = 'Tingla'
	ward = 1

	register = construct_register_path(vdc, ward)
	print(register)
	shapefile = construct_shapefile_path(vdc, ward)
	print(shapefile)
	
	











 