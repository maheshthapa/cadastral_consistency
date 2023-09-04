from cadastre import parcel_database
from cadastre import parcel_subdivision_register
#from cadastre import register_and_database_functional as rnd


from conversion import register_conversion
from conversion import shapefile_conversion




# Returns list of extra parcels
def find_extra_parcels(register, database):
			db_parcels = database.get_parcels()
			children = register.get_children()

			# Logic : Extra Parcels = Database Parcels - Children 
			extra_parcels = [i for i in db_parcels if i not in children] 
			return sorted(extra_parcels)

# Returns list of duplicate parcels in the database
def find_duplicate_parcels(register, database):
	db_parcels = database.get_parcels()
	children = register.get_children()

	#Logic : if count of parcel in db > count of parcels in children
	duplicate_parcels = []
	for parcel in db_parcels:
		if db_parcels.count(parcel) > 1:
			if db_parcels.count(parcel) > children.count(parcel):
				duplicate_parcels.append(parcel)
	
	return sorted(duplicate_parcels)

	

# Return list of dead parcels
def find_dead_parcels(register, database):
	"""
	Goes through leaves and if does not exist,
	then adds the parent of such leaves to 
	dead parcel_list. 
	"""
	db_parcels = database.get_parcels()
	leaves = register.get_leaves()
	dead_parcels = []
 
	# Iterates for all leaf parcels if parcel not in db_parcels
	for parcel in leaves:
		if parcel not in db_parcels:
			# find parent for such parcel and add it to dead_parcels list
			parent = register.find_parent_parcel(parcel)
			# Avoids adding parcel 0 and parcel already added
			if parent[0] != 0 and parent[0] not in dead_parcels:
				dead_parcels.append(parent[0])
	return sorted(dead_parcels)





# Return missing parcels among source parcels
def find_missing_original_parcels(register, database):
	original_parcels = register.get_original_parcels()
	parent_parcels = register.get_parents()
	db_parcels = database.get_parcels()
	
	missing_leaves = [i for i in original_parcels if i not in db_parcels and i not in parent_parcels]
	return missing_leaves
		
def generate_report(register, database):
		
	# Generation of report parameters	
	vdc = register.get_vdc()
	ward = register.get_ward()
	
	extra_parcels = find_extra_parcels(register, database)
	duplicate_parcels = find_duplicate_parcels(register, database)
	dead_parcels = find_dead_parcels(register, database)
	register_duplicates = register.find_duplicate_children()
	missing_parcels = find_missing_original_parcels(register, database)

	# Report formating
	print(f'VDC: {vdc},  WARD: {ward}\n')
	print (f'EXTRA PARCELS:              {extra_parcels}\n')
	print (f'DATABASE DUPLICATE PARCELS: {duplicate_parcels}\n')
	print (f'REGISTER DUPLICATE PARCELS: {register_duplicates}\n')
	print (f'MISSING PARCELS:            {missing_parcels}\n')
	print (f'DEAD PARCELS:               {dead_parcels}\n')
	
	generate_dead_parcel_report(register, database)
	

def generate_dead_parcel_report(register, database):
	dead_parcels = find_dead_parcels(register, database)
	database_parcels = database.get_parcels()

	for parcel in dead_parcels:		
		children = register.find_child_parcel(parcel)		
		
		if parcel in database_parcels:
			sheet_number = database.get_sheetnumber(parcel)
			print(f'Parent: {parcel:{5}},  Sheet: {sheet_number:{7}},  Child: {children}')	
		else:
			parent = parcel			
			while parent  != 0:
				parent = register.find_parent_parcel(parent)[0]
				
				if parent in database_parcels:
					#print(f'{parent} > {parcel} in database_parcels')
					sheet_number = database.get_sheetnumber(parent)
					print(f'Parent: {parcel:5}, Sheet: {sheet_number:8},  Child: {children}')
					break

				elif parent == 0:
					sheet_number = ""
					print(f'Parent: {parcel:5}, Sheet: {sheet_number:8},  Child: {children}')

