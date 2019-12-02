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
EOF = len(quadruple_dict.keys())                    # End Of File

avail_flag = False
recursive_value = 0

# Convert variable_tables to virtual_machine
for _,values in variable_tables.items():
    # values ex. [['int', 0], ['symbol', 'x']]
    var_id = values[1][1]
    var_type = values[0][0]
    var_val = values[0][1]
    virtual_machine[var_id] = [var_type,var_val]


"""
This method will return the dimensions of an operand
"""
def get_dim1(string):
    start = string.index('[') + 1
    end = string.index(']')
    index_str = string[start:end]

    get_val_from_oper(index_str)
    dim1 = recursive_value

    return dim1


"""
This method will return the dimensions of an operand
"""
def get_dim2(string):
    start = string.index('[') + 1
    end = string.index(']')
    index_str = string[start:end]

    get_val_from_oper(index_str)
    dim1 = recursive_value

    aux_string = string[end+1:]
    end = aux_string.index(']')
    index_str2 = aux_string[1:end]

    get_val_from_oper(index_str2)
    dim2 = recursive_value

    return dim1, dim2


def getval_from_dimension(string):
    dimension = string.count('[')
    if dimension == 1:
        dim1 = get_dim1(string)
        id_result = string.partition("[")[0]
        get_val_from_oper(virtual_machine[id_result][1][dim1])
        val = recursive_value
    elif dimension == 2:
        dim1, dim2 = get_dim2(string)
        id_result = string.partition("[")[0]
        get_val_from_oper(virtual_machine[id_result][1][dim1][dim2])
        val = recursive_value
    return val


"""virtual_machine = {'i': ['int', 0], 'j': ['int', 0] }
avail_dict = {'T1': 0, 'T2': 0}
But we could end with reference to reference, therefore we must obtain the value by recursion"""
def get_val_from_oper(oper):
    global recursive_value
    if isinstance(oper, float):
        recursive_value = float(oper)
        return
    elif isinstance(oper, int) or oper.isdigit():
        recursive_value = int(oper)
        return
    elif oper in avail_dict:
        get_val_from_oper(avail_dict[oper])
    elif oper in virtual_machine:
        get_val_from_oper(virtual_machine[oper][1])
    elif '[' in oper:
        oper_val_from_dim = getval_from_dimension(oper)
        get_val_from_oper(oper_val_from_dim)

    return


def store_value(oper_result, aux_result):
    global avail_flag
    if avail_flag:
        avail_dict[oper_result] = aux_result
    else:
        virtual_machine[oper_result][1] = aux_result


def operation(program_counter):
    global recursive_value
    global avail_flag
    op_code, oper1, oper2, oper_result = quadruple_dict[program_counter]

    avail_flag = True if oper_result in avail_dict else False           # check if it's from an avail

    # print("avail: ", avail_flag)
    # print(program_counter, " ",quadruple_dict[program_counter])
    # print("*"*10)

    # Get value of operand 1
    get_val_from_oper(oper1)
    val1 = recursive_value

    # Get value of operand 2
    get_val_from_oper(oper2)
    val2 = recursive_value

    # print(val1, "  ", val2)


    # Check if it's a dimension variable
    dimension_flag = False
    if isinstance(oper_result, str):
        if '[' in oper_result:
            dimension_flag = True

    # Operations TODO call to function
    if op_code == 'plus' or op_code == '++':
        aux_result = val1 + val2
        store_value(oper_result, aux_result)

        program_counter += 1
    elif op_code == '-' or op_code == '--':
        aux_result = val1 - val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == '*':
        aux_result = val1 * val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == '/':
        aux_result = val1 / val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == '%':
        aux_result = val1 % val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == '<':
        aux_result = val1 < val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == '>':
        aux_result = val1 > val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == '==':
        aux_result = val1 == val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == '!=':
        aux_result = val1 != val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == 'and':
        aux_result = val1 and val2
        store_value(oper_result, aux_result)

        program_counter += 1

    elif op_code == 'or':
        aux_result = val1 or val2
        store_value(oper_result, aux_result)

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

    elif op_code == 'Return': # Methods
        program_counter = int(PC_stack.pop())

    elif op_code == 'read':
        aux_result = input('>> ')
        var1_type = virtual_machine[oper_result][0]
        virtual_machine[oper_result][1] = int(aux_result) if var1_type == 'int' else float(aux_result)

        program_counter += 1

    elif op_code == 'write':
        if oper_result[:2] == '__':
            # Printing message
            print(">> ", str(oper_result))
        else:
            get_val_from_oper(oper_result)
            to_print = recursive_value
            print(">> ", str(to_print))
        program_counter += 1

    elif op_code == '=':
        # EX. ['=', 'num', '_', 'arr[i]']           arr[i] = num;
        if dimension_flag:
            dimension = oper_result.count('[')  # Get how many dimensions

            if dimension == 1:
                dim1 = get_dim1(oper_result)

                id_result = oper_result.partition("[")[0]
                get_val_from_oper(oper1)
                virtual_machine[id_result][1][dim1] = recursive_value

            elif dimension == 2:
                dim1, dim2 = get_dim2(oper_result)

                id_result = oper_result.partition("[")[0]
                get_val_from_oper(oper1)
                virtual_machine[id_result][1][dim1][dim2] = recursive_value
        # ['=', 'x', '_', 'y']          y = x;
        else:
            get_val_from_oper(oper1)
            result_value = recursive_value
            virtual_machine[oper_result][1] = result_value

        program_counter += 1

    return program_counter


while PC != EOF:
    PC = operation(PC)
    # time.sleep(.1)

    """
    print()
    print(virtual_machine)
    print()
    print(avail_dict)
    print()"""

print()
for vm in virtual_machine:
    if vm in avail_dict:
        print("{0}: {1}".format(vm,avail_dict[virtual_machine]))
    else:
        print("{0}: {1}".format(vm,virtual_machine[vm]))

print()
print(avail_dict)

# print(quadruple_dict,variable_tables,procedure_directory, sep='\n\n\n')