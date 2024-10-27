import pandas as pd

class PlotRegister:
    """ 
    A class representing a Parcel Subdivision Register.
    
    Attributes:
        dataframe (pd.DataFrame): Plot register in pandas DataFrame format.

    Methods:
       __init__(file_path): Initializes the plot register DataFrame.
        __str__(): Returns a string representation of the register.
        get_vdc(): Retrieves the VDC from the DataFrame.
        get_ward(): Retrieves the ward from the DataFrame.
        list_child_parcels(): Returns a list of child parcels.
        list_parent_parcels(): Returns a list of parent parcels.
        extract_leaf_parcels(): Returns a list of leaf parcels.
        get_parent_parcel(parcel): Retrieves parent parcels for a given parcel.
        get_ancestors(parcel): Retrieves all ancestors for a given parcel.
    """

    def __init__(self, file_path):
        """
        Initializes the PlotRegister with data from an Excel file.

        Parameters:
            file_path (str): The path to the Excel file containing the plot register data.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file cannot be read as a DataFrame.
        """
        self.file_path = file_path
        self.dataframe = self.load_data(file_path)

    def load_data(self, path):
        """Loads data from an Excel file into a DataFrame."""
        try:
            return pd.read_excel(path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file at {path} was not found.") from e
        except Exception as e:
            raise ValueError(f"Could not read the file at {path}: {e}") from e


    def __str__(self):
        """Return a string representation of the PlotRegister."""
        try:
            vdc = self.get_vdc()
        except ValueError as e:
            vdc = "N/A"  # Indicate that VDC is not available

        try:
            ward = self.get_ward()
        except ValueError as e:
            ward = "N/A"  # Indicate that Ward is not available

        return f"Register(VDC: {vdc}, Ward: {ward})"


    def get_vdc(self):
        """Retrieve the first VDC from the DataFrame.

        Returns:
            str: The first VDC value.
        
        Raises:
            ValueError: If the DataFrame is empty.
        """
        if self.dataframe.empty:
            raise ValueError("DataFrame is empty; cannot retrieve VDC.")
        return self.dataframe['vdc'].iloc[0]

    def get_ward(self):
        """Retrieve the first ward from the DataFrame.

        Returns:
            str: The first ward value.
        
        Raises:
            ValueError: If the DataFrame is empty.
        """
        if self.dataframe.empty:
            raise ValueError("DataFrame is empty; cannot retrieve ward.")
        return self.dataframe['ward'].iloc[0]

    def list_child_parcels(self):
        """Retrieve a list of child parcels from the DataFrame.

        Returns:
            list: A list of child parcels as strings.
        """
        return self._get_column_as_list('child_parcel')
        

    def list_parent_parcels(self):
        """Retrieve a list of parent parcels from the DataFrame.

        Returns:
            list: A list of parent parcels as strings, or an empty list if an error occurs.
        """
        try:
            parent_parcels = self._get_column_as_list('parent_parcel')
            
            # Flatten and clean the list
            return [item.strip() for sublist in parent_parcels for item in sublist.split(',')]
        
        except Exception as e:
            print(f"An error occurred while retrieving parent parcels: {e}")
            return []  # Return an empty list if any error occurs

            
            # Flatten and clean the list
            return [item.strip() for sublist in parent_parcels for item in sublist.split(',')]

    def extract_leaf_parcels(self):
        """Retrieve a list of leaf parcels (i.e., child parcels that are not parents).

        Returns:
            list: A list of leaf parcels as strings, or an empty list if an error occurs.
        """
        try:
            child_parcels = self.list_child_parcels()
            parent_parcels = self.list_parent_parcels()

            # Calculate leaf parcels by filtering out parent parcels from child parcels
            leaf_parcels = [parcel for parcel in child_parcels if parcel not in parent_parcels]
            
            return leaf_parcels

        except Exception as e:
            print(f"An error occurred while extracting leaf parcels: {e}")
            return []  # Return an empty list if any error occurs


    def find_parent_parcel(self, parcel):
        """Retrieve parent parcels for a given parcel.

        Parameters:
            parcel (str): The parcel number for which to retrieve parent parcels.

        Returns:
            list: A list of parent parcels as strings, or an empty list if none are found.
        """
        # Ensure the input is a string
        parcel_str = str(parcel)

        # Retrieve parent parcels from the DataFrame
        parents = self.dataframe.loc[self.dataframe['child_parcel'].astype(str) == parcel_str, 'parent_parcel']

        # Flattening and cleaning the parent list
        flattened_parents_list = [
            item.strip() 
            for sublist in parents.astype(str).tolist() 
            for item in sublist.split(',')
        ]

        return flattened_parents_list if flattened_parents_list else []

    def find_ancestors(self, parcel):
        """Retrieve all ancestors for a given parcel.

        Parameters:
            parcel (str): The parcel number for which to retrieve ancestors.

        Returns:
            list: A list of ancestor parcels as strings.
        """
        ancestors = []  # List to hold all ancestors
        parents = self.find_parent_parcel(parcel)

        while parents:
            # Add current parents to the ancestors list
            ancestors.extend(parents)
            
            # Retrieve new parents for the current set of parents
            next_parents = []
            for parent in parents:
                next_parents.extend(self.find_parent_parcel(parent))
            
            # Update the list of parents for the next iteration
            parents = next_parents

        return list(set(ancestors))


    

    def _get_column_as_list(self, column_name):
        """Helper method to retrieve a column as a list."""
        try:
            return self.dataframe[column_name].astype(str).tolist()
        except KeyError:
            print(f"KeyError: The '{column_name}' column does not exist in the DataFrame.")
            return []
        except Exception as error:
            print(f"An unexpected error occurred: {error}")
            return []

# Testing
if __name__ == "__main__":
    sample_plotregister = PlotRegister(r'D:\coding_projects\cadastral_consistency\data\Sample_Plotregister.xlsx')
    
    print("Child Parcel List: {}".format(sample_plotregister.list_child_parcels()))
    print("Parent Parcel List: {}".format(sample_plotregister.list_parent_parcels()))
    print("Leaf Parcel List: {}".format(sample_plotregister.extract_leaf_parcels()))
    
    print("Ancestors of '13': {}".format(sample_plotregister.find_ancestors('13')))
