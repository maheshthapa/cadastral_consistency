#from cadastre import database
#from cadastre import plot_register
#from cadastre import register_and_database_functional as rnd


#from conversion import register_conversion
#from conversion import shapefile_conversion



# Returns list of extra parcels
def extract_extra_parcels(register, database):
    """
    Extracts parcels from the database that are not present in the register's child parcels.

    Parameters:
        register (PlotRegister): The register containing child parcels.
        database (Database): The database containing all parcels.

    Returns:
        list: A list of extra parcels not found in the child parcels.
    """
    # Retrieve lists of parcels from the database and register
    database_parcels = database.list_parcels()
    child_parcels = register.list_child_parcels()

    # Identify extra parcels that are in the database but not in the register's child parcels
    extra_parcels = [parcel for parcel in database_parcels if parcel not in child_parcels]

    return extra_parcels


def extract_duplicate_parcels(register, database):
    # Extract leaf parcels from the register
    leaf_parcels = register.extract_leaf_parcels()
    
    # List all parcels in the database
    database_parcels = database.list_parcels()
    print(database_parcels)
    
    # Count occurrences of each parcel in the leaf parcels
    leaf_count = {}
    for parcel in leaf_parcels:
        leaf_count[parcel] = leaf_count.get(parcel, 0) + 1

    # Count occurrences of each parcel in the database
    database_count = {}
    for parcel in database_parcels:
        database_count[parcel] = database_count.get(parcel, 0) + 1

    # Identify duplicates by comparing counts
    duplicate_parcels = [
        parcel for parcel in leaf_count 
        if database_count.get(parcel, 0) > leaf_count[parcel]
    ]
    
    return duplicate_parcels

	

def extract_dead_parcels(register, database):
    # Extract leaf parcels and convert to sets for efficient lookups
    leaf_parcels = set(register.extract_leaf_parcels())
    database_parcels = set(database.list_parcels())
    
    dead_parcels = []

    # Iterate through each leaf parcel
    for parcel in leaf_parcels:
        if parcel not in database_parcels:
            ancestors = register.find_ancestors(parcel)

            # Add ancestors that are present in the database parcels
            dead_parcels.extend(ancestor for ancestor in ancestors if ancestor in database_parcels)

    return dead_parcels





def extract_missing_parcels(register, database):
    # Extract leaf parcels and convert to sets for efficient lookups
    leaf_parcels = set(register.extract_leaf_parcels())
    database_parcels = set(database.list_parcels())
    
    missing_parcels = []

    # Iterate through each leaf parcel
    for parcel in leaf_parcels:
        if parcel not in database_parcels:
            ancestors = register.find_ancestors(parcel)

            # Check if none of the ancestors are present in the database parcels
            if not any(ancestor in database_parcels for ancestor in ancestors):
                missing_parcels.append(parcel)  
    return missing_parcels  



	
		
def generate_inconsistency_report(register, database):
		
	# Generation of report parameters	
	vdc = register.get_vdc()
	ward = register.get_ward()
	
	
	extra_parcels = find_extra_parcels(register, database)
	duplicate_parcels = find_duplicate_parcels(register, database)
	dead_parcels = find_dead_parcels(register, database)
	register_duplicates = register.find_duplicate_children()
	missing_parcels = find_missing_original_parcels(register, database)

	# Report formating
	print()
	print(f'VDC: {vdc},  WARD: {ward}')
	print (f'EXTRA PARCELS:              {extra_parcels}')
	print (f'DATABASE DUPLICATE PARCELS: {duplicate_parcels}')
	print (f'REGISTER DUPLICATE PARCELS: {register_duplicates}')
	print (f'MISSING PARCELS:            {missing_parcels}\n')
	print (f'DEAD PARCELS:               {dead_parcels}')
	
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


