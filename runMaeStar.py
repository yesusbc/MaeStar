import pickle

# We need to first load the previous objects
with open('quadruples', 'rb') as file_object:
    quadruple_dict = pickle.load(file_object)

with open('variableTables', 'rb') as file_object:
    variable_tables = pickle.load(file_object)

with open('procedureDirectory', 'rb') as file_object:
    procedure_directory = pickle.load(file_object)



print(quadruple_dict,variable_tables,procedure_directory, sep='\n\n\n')