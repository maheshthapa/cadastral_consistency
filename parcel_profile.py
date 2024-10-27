from cadastre import plot_register
from conversion import register_conversion
from conversion import construct_path


def main(vdc, ward, parcels):
	register_path = construct_path.construct_register_path(vdc, ward)
	register_dataframe = register_conversion.transform_excel_to_dataframe(register_path)
	register = plot_register.ParcelSubdivisionRegister(register_dataframe)
	for parcel in parcels: 
		generate_parcel_profile(register, parcel)
			


# Generates parcel profile
def generate_parcel_profile(register, parcelno):
	# get vdc and ward info
	vdc = register.get_vdc()
	ward = register.get_ward()
	
	# Validate input parcel is among children
	if parcelno in register.get_children():
		original_parcel = register.find_original_parcel(parcelno)
		child_parcel = register.find_child_parcel(parcelno)	
		ancestor = register.find_ancestor(parcelno)	
		print (f"[{register}],  Parcel: {parcelno},  Original: {original_parcel},  Child: {child_parcel} ")
		print (f'Ancestor: {ancestor}')
	else:
		print(f"{register}::  Parcel:  {parcelno},  Warning: Input parcel does not exist!!!")
		print()



if __name__ == "__main__":
	# Pass values for generating parcel profile	
	#main('Basa', 1,  [121, 165, 179, 188, 202])
	main('Basa', 1,  [1795])
	
	

	
	