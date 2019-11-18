# Author: Yesus Becerril
# ID: A00513040
# Date: November 9, 2019
# python 3


from maeStarYacc import square_obj, get_parser
from quadruple import get_avail
from maeStarLex import variable_tables, procedure_directory
import sys
import pickle

filename = sys.argv[1]


filenames = {
    'ifelse': 'testfiles/ifelseprogram.txt',
    'while': 'testfiles/while.txt',
    'do-while': 'testfiles/dowhile.txt',
    'simplemath': 'testfiles/simplemathprogram.txt',
    'main': 'testfiles/maincode.txt',
    'matrix': 'testfiles/matrix.txt',
    'for': 'testfiles/for.txt',
    'method': 'testfiles/methods.txt',
    'dm': 'testfiles/dimensional_variables.txt'
}

file = open(filenames[filename], 'r')
code = file.read()
print(code)

parser = get_parser()
parser.parse(code)

print("\n\n"+"*"*20 + "\n" + "Cuadros: " + "\n"+"*"*20)
for square in square_obj.quadruple_dict:
    print("{0}.- {1}".format(square, square_obj.quadruple_dict[square]))

get_avail()

# Assigning values
# print(operand_stack)
# while(operand_stack):
#     value = operand_stack.pop()
#     destiny = operand_stack.pop()
#    variable_tables[destiny][1] = value


print("\n\n"+"*"*20 + "\n" + "Variable Tables: " + "\n"+"*"*20)
print(variable_tables, end="\n\n")

print(procedure_directory, end="\n\n")

print("#"*50)
with open('quadruples', 'wb') as file_handler:
    pickle.dump(square_obj.quadruple_dict, file_handler)
    print("Quadruples imported correctly")


with open('variableTables', 'wb') as file_handler:
    pickle.dump(variable_tables, file_handler)
    print("Variable Tables imported correctly")

with open('procedureDirectory', 'wb') as file_handler:
    pickle.dump(procedure_directory, file_handler)
    print("Procedure Directory imported correctly")
print("#"*50)