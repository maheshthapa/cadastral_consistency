import geopandas as gpd

class Parcel_Database:
    """
    A class representing a database of parcels.

    Attributes:
        database_path (str): The file path to the parcel database.
        geodataframe (GeoDataFrame): The parcel database in GeoPandas format.

    Methods:
        __init__(database_path): Initializes the Database with the specified path.
        load_geodataframe(path): Loads a GeoDataFrame from the specified file path.
        list_parcels(): Returns a list of parcel numbers as strings.
        get_sheetnumber(parcel): Retrieves the map sheet number for a given parcel number.
    """

    def __init__(self, database_path):
        """
        Initializes the Database with the specified path and loads the GeoDataFrame.

        Parameters:
            database_path (str): The file path to the parcel database.
        
        Raises:
            FileNotFoundError: If the file does not exist at the given path.
            ValueError: If the file cannot be read as a GeoDataFrame.
        """
        self.database_path = database_path
        self.geodataframe = self.load_geodataframe(database_path)

    def load_geodataframe(self, path):
        """
        Loads a GeoDataFrame from the specified file path.

        Parameters:
            path (str): The file path to the geospatial data.

        Returns:
            GeoDataFrame: A GeoDataFrame containing the loaded data.
        
        Raises:
            FileNotFoundError: If the file does not exist at the given path.
            ValueError: If the file cannot be read as a GeoDataFrame.
        """
        try:
            return gpd.read_file(path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {path}") from e
        except Exception as e:
            raise ValueError(f"Could not read the file as a GeoDataFrame: {path}") from e

    def list_parcels(self):
        """
        Returns a list of parcel numbers in the database as strings.

        Returns:
            list: A list of parcel numbers as strings.
        """
        return self.geodataframe['parcelno'].astype(str).tolist()
    
    def get_sheetnumber(self, parcel):
        """
        Retrieves the map sheet number for a given parcel number.

        Parameters:
            parcel (str or int): The parcel number for which to retrieve the map sheet number.

        Returns:
            str: The map sheet number corresponding to the parcel.

        Raises:
            ValueError: If the parcel number is not found in the database.
        """
        # Convert parcel to string for comparison
        parcel_str = str(parcel)
        
        # Attempt to locate the map sheet number
        try:
            sheetnumber = self.geodataframe.loc[self.geodataframe['parcelno'] == parcel_str, 'mapsheetno'].iloc[0]
            return sheetnumber
        except IndexError:
            raise ValueError(f"Parcel number {parcel_str} not found in the database.")

# Testing 
if __name__ == "__main__":
    database = Parcel_Database(r'D:\coding_projects\cadastral_consistency\data\Sample_Database.shp')
    print(database.list_parcels())
