

class ParcelSubdivisionRegister:
	""" 
	A class representing Parcel Subdivision Register.
	
	Atributes:
		df (panda dataframe) : Plotregister in panda dataframe format

	Methods:
		__init__ : Constructor to initialize the plotregister dataframe
		get_children: Return list of all children parcels from register
		get_parents: Return list of all parent parcels from register
		get_leaves: Return list of all leaf parcels from reigister (i.e. all undivided parcels)


	"""
	def __init__(self, df):
		self.df = df		

	def __str__(self):
		return f"Register(Vdc: {self.get_vdc()}, Ward: {self.get_ward()})"

	def get_vdc(self):
		return self.df['Vdc'][0]
	
	def get_ward(self):
		return self.df['Ward'][0]
	
	# Return list of child parcels 
	def get_children(self): 		
		try:
			child_parcels = self.df.child_parcel.values.tolist()
			child_parcels = [int(i) for i in child_parcels]
			return child_parcels
		except:
			child_parcels = self.df.ChildParcel.values.tolist()
			child_parcels = [int(i) for i in child_parcels]
			return child_parcels

			
	# Return list of parent_parcels
	def get_parents(self): 
		"""
		Return list of parent parcels
		"""
		try:
			parent_parcels =  self.df.parent_parcel.values.tolist()
			return  [int(i) for i in parent_parcels]
		except:
			parent_parcels =  self.df.ParentParcel.values.tolist()
			return [int(i) for i in parent_parcels]
		

	def get_original_parcels(self):
		children_parcels = self.get_children()

		original_parcels = []
		for parcel in children_parcels:
			if self.find_parent_parcel(parcel)[0] == 0:
				original_parcels.append(parcel)
		return original_parcels

	# Returns all leaf nodes 
	# STANDING PARCELS
	def get_leaves(self): 
		"""  
		Return list of standing parcels
		Formula : Standing Parcels = Child Parcels - Parent Parcels
		"""
		child_parcels = self.get_children()
		parent_parcels = self.get_parents()
		standing_parcels = [i for i in child_parcels if i not in parent_parcels]
		return standing_parcels
	
	# Assigning alisas name to get_leaves function
	get_standing_parcels = get_leaves
    
	# Returns child(s) of input parcel
	def find_child_parcel(self, parcelno):
		"""
		Returns a list of child(s) of a parent parcel if it exists 
		"""	
		# Input validation for parcel to exist
		if parcelno in self.get_children():
			# Ensuring input parcel is a parent		
			if parcelno in self.get_parents():
				# Get children when matches with parcelno(parent) 		
				try:
					children = self.df.loc[self.df['parent_parcel'] == parcelno, 'child_parcel']
					return children.tolist()
				except:
					children = self.df.loc[self.df['ParentParcel'] == parcelno, 'ChildParcel']
					return children.tolist()
			
		

	# Return parent(s) of input parcelno
	def find_parent_parcel(self, parcelno):
		"""
		Returns parent of given parcel as list
		"""	
		# Validating parcel exists in the register
		if parcelno in self.get_children(): 
			# get parent parcels of input child
			try:
				parent = self.df.loc[self.df['child_parcel'] == parcelno, 'parent_parcel']
				return parent.tolist()
			except:
				parent = self.df.loc[self.df['ChildParcel'] == parcelno, 'ParentParcel']
				return parent.tolist()
		
			
	# Returns list of duplicate parcels in register
	def find_duplicate_children(self):
		"""
		Returns list of duplicate child parcels in plotregister
		"""
		children = self.get_children()

		# Lists of child_parcels which occurs more than once
		duplicate_children = [i for i in children if children.count(i) > 1]
		return duplicate_children


	# Returns source parcel for input parcelno
	def find_original_parcel(self, parcelno):
		
		# Validating parcelno exist in register among children parcels
		if parcelno in self.get_children():
			parent_parcel = self.find_parent_parcel(parcelno)[0] 
			# Traces back to root parcel			
			while parcelno != 0:
				parent_parcels = self.find_parent_parcel(parcelno)
				if parent_parcels[0] == 0:
					return [parcelno]
				elif len(parent_parcels) > 1:
					return [parent_parcels]
				else:
					parcelno = parent_parcels[0]
		

	# Return set of parent parcels
	def find_ancestor(self, parcelno):
		ancestor = []
		# Validating parcelno exists in register
		if parcelno in self.get_children():
			# Appends successive parents to ancestor list
			
			while parcelno != 0:
				parent = self.find_parent_parcel(parcelno)
				if len(parent) > 1:
					ancestor.append(parent)
					#parcelno = parent
					return ancestor
				else: 					
					parent = parent[0]
					ancestor.append(parent)
					parcelno = parent
			return ancestor


			
	

		

				
			
		
		
		






		
		





