import pickle
import time

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

recursive_value = 0

# Convert variable_tables to virtual_machine
for _,values in variable_tables.items():
    # values ex. [['int', 0], ['symbol', 'x']]
    var_id = values[1][1]
    var_type = values[0][0]
    var_val = values[0][1]
    virtual_machine[var_id] = [var_type,var_val]


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_dim1(string):
    start = string.index('[')
    end = string.index(']')
    index_str = string[end-start]
    index_var = virtual_machine[index_str][1]
    if isinstance(index_str,int) or index_str.isdigit():
        dim1 = int(index_str)
    else:
        if index_var in avail_dict:
            dim1 = int(avail_dict[index_var])
        else:
            dim1 = int(index_var)

    return dim1


# TODO Minimize variables
def get_dim2(string):
    start = string.index('[')
    end = string.index(']')
    index_str = string[end-start]

    if isinstance(index_str, int) or index_str.isdigit():
        dim1 = int(index_str)
    else:
        index_var1 = virtual_machine[index_str][1]      # Tal vez vaya arriba de is instance
        if index_var1 in avail_dict:
            dim1 = int(avail_dict[index_var1])
        else:
            dim1 = int(index_var1)

    aux_string = string[end+1:]
    end = aux_string.index(']')
    index_str2 = aux_string[1:end]

    if isinstance(index_str2, int) or index_str2.isdigit():
        dim2 = int(index_str2)
    else:
        index_var2 = virtual_machine[index_str2][1]  # Tal vez vaya arriba de is instance
        if index_var2 in avail_dict:
            dim2 = int(avail_dict[index_var2])
        else:
            dim2 = int(index_var2)

    return dim1, dim2


def getval_from_dimension(string):
    dimension = string.count('[')
    if dimension == 1:
        dim1 = get_dim1(string)
        id_result = string.partition("[")[0]
        # if virtual_machine[id_result][1][dim1] in avail_dict:
        #     val = avail_dict[virtual_machine[id_result][1][dim1]]
        # else:
        val = virtual_machine[id_result][1][dim1]
    elif dimension == 2:
        dim1, dim2 = get_dim2(string)
        id_result = string.partition("[")[0]
        # if virtual_machine[id_result][1][dim1][dim2] in avail_dict:
        #     val = avail_dict[virtual_machine[id_result][1][dim1][dim2]]
        # else:
        val = virtual_machine[id_result][1][dim1][dim2]
    return val


def get_val_from_oper(oper):
    global recursive_value
    if virtual_machine[oper][1] in avail_dict:
        recursive_value = avail_dict[virtual_machine[oper][1]]
        return
    else:
        # we can have var3 = var2, and var2=var1, so we must cover that case
        if virtual_machine[oper][1] in virtual_machine:

            get_val_from_oper(virtual_machine[oper][1])
        else:
            var_type = virtual_machine[oper][0]
            recursive_value = int(virtual_machine[oper][1]) if var_type == 'int' else float(virtual_machine[oper][1])
            return


def operation(program_counter):
    global recursive_value
    op_code, oper1, oper2, oper_result = quadruple_dict[program_counter]

    avail_flag = True if oper_result in avail_dict else False           # check if it's from an avail

    # print("avail: ", avail_flag)
    print(program_counter, " ",quadruple_dict[program_counter])
    print("*"*10)

    # Get value of operand 1
    if isinstance(oper1, int):
        val1 = oper1
    elif oper1.isdigit():
        val1 = int(oper1)
    elif isfloat(oper1):
        val1 = float(oper1)
    elif '[' in oper1:
        val1 = getval_from_dimension(oper1)
    elif oper1 in virtual_machine:
        get_val_from_oper(oper1)
        val1 = recursive_value

        if not val1:
            val1 = 0
        """
        if virtual_machine[oper1][1] in avail_dict:
            val1 = avail_dict[virtual_machine[oper1][1]]
        else:
            # we can have var3 = var2, and var2=var1, so we must cover that case
            if virtual_machine[oper1][1] in virtual_machine:
                var1_type = virtual_machine[virtual_machine[oper1][1]][0]
                val1 = int(virtual_machine[virtual_machine[oper1][1]][1]) if var1_type == 'int' else float(virtual_machine[virtual_machine[oper1][1]][1])
            else:
                var1_type = virtual_machine[oper1][0]
                val1 = int(virtual_machine[oper1][1]) if var1_type == 'int' else float(virtual_machine[oper1][1])"""
    elif oper1 in avail_dict:
        val1 = avail_dict[oper1]
    elif oper1 in procedure_directory:
        pass
    elif oper1.isalpha():
        raise RuntimeError("Local variable unreferenced before: {0} \n".format(oper1))

    # Get value of operand 2
    if isinstance(oper2, int):
        val2 = oper2
    elif oper2.isdigit():
        val2 = int(oper2)
    elif isfloat(oper2):
        val2 = float(oper2)
    elif '[' in oper2:
        val2 = getval_from_dimension(oper2)

    elif oper2 in virtual_machine:
        get_val_from_oper(oper2)
        val2 = recursive_value
        # if virtual_machine[oper2][1] in avail_dict:
        #     val2 = avail_dict[virtual_machine[oper2][1]]
        # else:
        #     var2_type = virtual_machine[oper2][0]
        #     val2 = int(virtual_machine[oper2][1]) if var2_type == 'int' else float(virtual_machine[oper2][1])
    elif oper2 in avail_dict:
        val2 = avail_dict[oper2]
    elif oper2 in procedure_directory:
        pass
    elif oper2.isalpha():
        raise RuntimeError("Local variable unreferenced before: {0} \n".format(oper2))

    # Check if it's a dimension variable
    dimension_flag = False
    if isinstance(oper_result, str):
        if '[' in oper_result:
            dimension_flag = True

    # Operations
    if op_code == 'plus' or op_code == '++':
        aux_result = val1 + val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
        program_counter += 1
    elif op_code == '-' or op_code == '--':
        aux_result = val1 - val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
        program_counter += 1

    elif op_code == '*':
        aux_result = val1 * val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
        program_counter += 1

    elif op_code == '/':
        aux_result = val1 / val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
        program_counter += 1

    elif op_code == '=':
        # TODO check for dimensions in avail_dict
        if dimension_flag:
            dimension = oper_result.count('[')  # Get how many dimensions
            if dimension == 1:
                start = oper_result.index('[')
                end = oper_result.index(']')
                index = oper_result[end-start]
                if isinstance(index, int) or index.isdigit():
                    dim1 = int(index)
                else:
                    index_var = virtual_machine[oper_result[end-start]][1]
                    if index_var in avail_dict:
                        dim1 = avail_dict[index_var]
                    else:
                        dim1 = int(index_var)

                id_result = oper_result.partition("[")[0]
                virtual_machine[id_result][1][dim1] = oper1

            elif dimension == 2:
                start = oper_result.index('[')
                end = oper_result.index(']')
                index = oper_result[end-start]
                if isinstance(index, int) or index.isdigit():
                    dim1 = int(index)
                else:
                    index_var = virtual_machine[oper_result[end-start]][1]
                    if index_var in avail_dict:
                        dim1 = avail_dict[index_var]
                    else:
                        dim1 = int(index_var)

                aux_string = oper_result[end+1:]
                end = aux_string.index(']')

                if isinstance(aux_string[1:end], int) or aux_string[1:end].isdigit():
                    dim2 = int(aux_string[1:end])
                else:
                    dim2 = int(virtual_machine[aux_string[1:end]][1])

                id_result = oper_result.partition("[")[0]
                virtual_machine[id_result][1][dim1][dim2] = oper1
        else:
            virtual_machine[oper_result][1] = oper1
        program_counter += 1

    elif op_code == '<':
        aux_result = val1 < val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
        program_counter += 1

    elif op_code == '>':
        aux_result = val1 > val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
        program_counter += 1

    elif op_code == '==':
        aux_result = val1 == val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
        program_counter += 1

    elif op_code == '!=':
        aux_result = val1 != val2
        if avail_flag:
            avail_dict[oper_result] = aux_result
        else:
            virtual_machine[oper_result][1] = aux_result
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
        if oper_result in virtual_machine:
            get_val_from_oper(oper_result)
            val = recursive_value
            # if virtual_machine[oper_result][1] in avail_dict:
            #     print(">> ", avail_dict[virtual_machine[oper_result][1]])
            # else:
            #     print(">> ",virtual_machine[oper_result][1])
            print(">> ", str(val))
        else:
            if oper_result in avail_dict:
                print(">> ", avail_dict[str(oper_result)])
            else:
                print(">> ", str(oper_result))

        program_counter += 1

    return program_counter


while PC != EOF:
    PC = operation(PC)

    """print()
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