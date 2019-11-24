import pickle

# We need to first load the previous objects
with open('quadruples', 'rb') as file_object:
    quadruple_dict = pickle.load(file_object)

with open('variableTables', 'rb') as file_object:
    variable_tables = pickle.load(file_object)

with open('procedureDirectory', 'rb') as file_object:
    procedure_directory = pickle.load(file_object)

with open('availDict', 'rb') as file_object:
    avail_dict = pickle.load(file_object)

virtual_machine = dict()
PC_stack = list()                                   # Stack for program counter
PC = next(iter(quadruple_dict.keys()))              # Program Counter as first element on the list
EOF = len(quadruple_dict.keys())                    #End Of File


#Convert variable_tables to virtual_machine
for _,values in variable_tables.items():
    # values ex. [['int', 0], ['symbol', 'x']]
    var_id = values[1][1]
    var_type = values[0][0]
    var_val = values[0][1]
    virtual_machine[var_id] = [var_type,var_val]


def operation(program_counter):
    print(quadruple_dict[program_counter])
    op_code, oper1, oper2, oper_result = quadruple_dict[program_counter]

    avail_flag = True if oper_result in avail_dict else False

    if oper1 in virtual_machine:
        var1_type = virtual_machine[oper1][0]
        val1 = int(virtual_machine[oper1][1]) if var1_type == 'int' else float(virtual_machine[oper1][1])
    elif oper1 in avail_dict:
        val1 = avail_dict[oper1]
    elif oper1.isalpha():
        raise RuntimeError("Local variable unreferenced before: {0} \n".format(oper1))


    if oper2 in virtual_machine:
        var2_type = virtual_machine[oper2][0]
        val2 = int(virtual_machine[oper2][1]) if var2_type == 'int' else float(virtual_machine[oper2][1])
    elif oper2 in avail_dict:
        val2 = avail_dict[oper2]
    elif oper2.isalpha():
        raise RuntimeError("Local variable unreferenced before: {0} \n".format(oper2))

    if op_code == 'plus':
        aux_result = val1 + val2
        if avail_flag:
            virtual_machine[oper_result][1] = aux_result
        else:
            avail_dict[oper_result] = aux_result
        program_counter += 1

    elif op_code == '*':
        aux_result = val1 * val2
        if avail_flag:
            virtual_machine[oper_result][1] = aux_result
        else:
            avail_dict[oper_result] = aux_result
        program_counter += 1

    elif op_code == '/':
        aux_result = val1 / val2
        if avail_flag:
            virtual_machine[oper_result][1] = aux_result
        else:
            avail_dict[oper_result] = aux_result
        program_counter += 1

    elif op_code == '=':
        virtual_machine[oper_result][1] = oper1
        program_counter += 1

    elif op_code == '<':
        aux_result = val1 < val2
        if avail_flag:
            virtual_machine[oper_result][1] = aux_result
        else:
            avail_dict[oper_result] = aux_result
        program_counter += 1

    elif op_code == '>':
        aux_result = val1 > val2
        if avail_flag:
            virtual_machine[oper_result][1] = aux_result
        else:
            avail_dict[oper_result] = aux_result
        program_counter += 1

    elif op_code == '==':
        aux_result = val1 == val2
        if avail_flag:
            virtual_machine[oper_result][1] = aux_result
        else:
            avail_dict[oper_result] = aux_result
        program_counter += 1

    elif op_code in ('goto','gotoFor'):
        program_counter = int(oper_result)

    elif op_code == 'gotoF':   # goto False
        if avail_dict[oper1]:
            program_counter += 1
        else:
            program_counter = int(oper_result)

    elif op_code == 'gotoT':   # goto True
        if avail_dict[oper1]:
            program_counter = int(oper_result)
        else:
            program_counter += 1

    elif op_code == 'call':
        PC_stack.append(program_counter + 1)
        program_counter = int(oper_result)

    elif op_code == 'return': # Methods
        program_counter = int(PC_stack.pop())

    elif op_code == 'read':
        aux_result = input('>> ')
        var1_type = virtual_machine[oper_result][0]
        virtual_machine[oper_result][1] = int(aux_result) if var1_type == 'int' else float(aux_result)
        program_counter += 1

    elif op_code == 'write':
        print(">> ",virtual_machine[oper_result][1])
        program_counter += 1

    return program_counter

while PC != EOF:
    PC = operation(PC)


print(quadruple_dict,variable_tables,procedure_directory, sep='\n\n\n')