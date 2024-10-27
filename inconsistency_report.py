from cadastre import parcel_database
from cadastre import plot_register
from cadastre import inconsistency_utils 

def main(plot_register, database):
    

    #print(basa_database.list_parcels())
    
    print("Leaf Parcels")
    print(plot_register.extract_leaf_parcels())
    print()
    
    print("Extra Parcels")
    print(inconsistency_utils.extract_extra_parcels(plot_register, database))
    print()
    
    print("Duplicate Parcels")
    print(inconsistency_utils.extract_duplicate_parcels(plot_register, database))
    print()

    print("Missing Parcels")
    print(inconsistency_utils.extract_missing_parcels(plot_register, database))
    print()

    print("Dead Parcels")
    print(inconsistency_utils.extract_dead_parcels(plot_register, database))
    print()




if __name__ == "__main__":
    plot_register_path = r'D:\coding_projects\cadastral_consistency\data\Sample_Plotregister.xlsx' 
    sample_plot_register = plot_register.PlotRegister(plot_register_path)

    database_path = r'D:\coding_projects\cadastral_consistency\data\Sample_Database.shp'
    sample_database = parcel_database.Parcel_Database(database_path)

    
   
    
    main(sample_plot_register, sample_database)
    
    
    