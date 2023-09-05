from cadastre import parcel_database
from cadastre import parcel_subdivision_register
from cadastre import register_and_database as rnd

from conversion import register_conversion
from conversion import shapefile_conversion

def main(vdc, ward):
	# Conversion of database geodataframe to object
	geodataframe = shapefile_conversion.generate_geodataframe(vdc, ward)
	database = parcel_database.ParcelDatabase(geodataframe)

	# Conversion of register dataframe to object
	dataframe = register_conversion.generate_parcel_subdivision_dataframe(vdc,ward)
	register = parcel_subdivision_register.ParcelSubdivisionRegister(dataframe)


	
	rnd.generate_report(register, database)
	#rnd.generate_dead_parcel_report(register, database)



if __name__ == "__main__":
	
	ward_list = [3]
	vdc = "Tapting"

	for ward in ward_list:
		main(vdc, ward)
	
	print()
	