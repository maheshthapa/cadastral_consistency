import os
import pandas


# Generate plotregister dataframe given vdc and ward
def generate_parcel_subdivision_dataframe(vdc, ward):
	pr_path = generate_excel_path(vdc,ward)
	pr_dataframe = transform_excel_to_dataframe(pr_path)
	return pr_dataframe


# Generate Path: Given vdc and ward name,
# this function generates path of the plotregister excel file
def generate_excel_path(vdc,ward):
	# Defining various levels of path to access the plotregister excel file
	level_1 = r'\\CHECK_JACHA\\Solukhumbu_LIS\\Solukhumbu_fb_pr_prd_gov'
	level_2 = vdc
	level_3 = vdc + '_w' + str(ward)
	level_4 = vdc + '_w' + str(ward) + '_prd.xlsx'

	path = os.path.join(level_1, level_2, level_3, level_4)
	return path


# Convert plotregister excel file to panda dataframe
def transform_excel_to_dataframe(file):
	dataframe = pandas.read_excel(file)
	return dataframe



if __name__ == "__main__":

	# Variables
	vdc = 'Tingla'
	ward = 1

	python_subdivision_register = generate_parcel_subdivision_dataframe(vdc,ward)
	print(python_subdivision_register.columns)
	











 