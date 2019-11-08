# Author: Yesus Becerril
# ID: A00513040
# Date: November 9, 2019
# python 3


from maeStarYacc import square_obj, get_parser
from quadruple import get_vail


filenames = {
    'ifelse': 'testfiles/ifelseprogram.txt',
    'while': 'testfiles/while.txt',
    'do-while': 'testfiles/dowhile.txt',
    'simplemath': 'testfiles/simplemathprogram.txt',
    'main': 'testfiles/maincode.txt',
    'matrix': 'testfiles/matrix.txt'
}


# file = open('codigoprueba', 'r')
# file = open('maesumamatrices.txt', 'r')
file = open(filenames['ifelse'], 'r')
code = file.read()
print(code)

parser = get_parser()
parser.parse(code)

print("\n\n"+"*"*20 + "\n" + "Cuadros: " + "\n"+"*"*20)
for square in square_obj.quadruple_dict:
    print("{0}.- {1}".format(square, square_obj.quadruple_dict[square]))

get_vail()

# Assigning values
# print(operand_stack)
# while(operand_stack):
#     value = operand_stack.pop()
#     destiny = operand_stack.pop()
#    variable_tables[destiny][1] = value


# print("\n\n"+"*"*20 + "\n" + "Variable Tables: " + "\n"+"*"*20)
# print(variable_tables)