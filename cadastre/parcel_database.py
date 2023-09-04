

class ParcelDatabase:
	"""
	A class representing database of parcels.

	Attributes:
	db : Parcel database in geopanda format.

	Methods :
	__init__ : Constructor method to initialize parcel database class
	get_parcels : Returns list of parcels 

	"""

	def __init__(self, db):				
		self.db = db

	def get_parcels(self): 
		"""
		Returns list of parcels in the database.
		"""
		db_parcels = self.db.parcelno.values.tolist()
		db_parcels = [int(i) for i in db_parcels] # string to int
		return db_parcels
	
	def get_sheetnumber(self, parcel):
		sheetnumber = self.db.loc[self.db['parcelno'] == str(parcel), 'mapsheetno'].iloc[0]
		#['parcelno' == str(parcel), 'sheetid']
		return sheetnumber

		














