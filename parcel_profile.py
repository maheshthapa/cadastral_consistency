from cadastre import parcel_subdivision_register
from conversion import register_conversion

def main(vdc, ward, parcel_list):
	df = register_conversion.generate_parcel_subdivision_dataframe(vdc, ward)
	register = parcel_subdivision_register.ParcelSubdivisionRegister(df)
	for parcel in parcel_list:
		gen_parcel_profile(register, parcel)
		

def main1(vdc, ward, parcel_list):
	df = register_conversion.generate_parcel_subdivision_dataframe(vdc, ward)
	register = parcel_subdivision_register.ParcelSubdivisionRegister(df)
	for parcel in parcel_list:
		register.parcel_tree( parcel)

# Function to test Plotregister class
def gen_parcel_profile(register, parcelno):
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

	
	#main1('Sotang', 1, [1186, 1184, 910, 925, 926, 1177, 1175, 1176])
	
	main('Chaurikharka', 8, [1051])

	