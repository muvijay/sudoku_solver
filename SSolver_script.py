box_dict = {}
option_dict = {}
row_dict = {}

# Easy level
# row_dict = {
#     1: list(' 23497 85'), 
#     2: list('58  2 7 4'), 
#     3: list('7 65 3   '), 
#     4: list(' 9 76  51'), 
#     5: list('   35  2 '), 
#     6: list(' 6   9   '), 
#     7: list('472 3    '), 
#     8: list('    45 97'), 
#     9: list('95   8  2')}

# Medium level
# row_dict = {
#     1: list('     45  '), 
#     2: list('83 2579  '), 
#     3: list('  5 68  7'), 
#     4: list('   8713 6'), 
#     5: list(' 18 43   '), 
#     6: list('3 7 2 8  '), 
#     7: list(' 7     95'), 
#     8: list('186795   '), 
#     9: list(' 5       ')}

# Hard level
row_dict = {
    1: list('   5    8'), 
    2: list('2  9    4'), 
    3: list('5 93   7 '), 
    4: list(' 1  2  8 '), 
    5: list(' 58      '), 
    6: list('7   6   1'), 
    7: list('         '), 
    8: list('9   4   7'), 
    9: list('1  2  3  ')}

# for i in range(1,10):
#     input_data = input(f"enter the number for row-{i}: ")
#     row_dict[i] = list(str(input_data))

def pause():
    x = input('Continue..? ')
    if x == 'y':
        return False
    else:
        return True

def transpose(dic):
    col_dict = {}
    temp_col_list = []
    for key in dic:
        temp_col_list = dic[key]
        for j in range(1,10):
            val = lambda x:col_dict[x] if x in col_dict else ''
            temp_list = list(val(j))
            temp_list.append(temp_col_list[j-1])
            col_dict[j] = temp_list
    return col_dict
    
def transpose_box(dic):
    box_dict = {}
    temp_box_list = []
    box_counter = 1
    for key in dic:
        temp_box_list = dic[key]
        box_initial_pointer = box_counter
        for k in range(1,10):
            val1 = lambda y:box_dict[y] if y in box_dict else ''
            temp_list = list(val1(box_counter))
            temp_list.append(temp_box_list[k-1])
            box_dict[box_counter] = temp_list
            if k == 3 or k == 6:
                box_counter = box_counter + 1
            elif k == 9:
                box_counter = box_initial_pointer
        if key == 3 or key == 6:
            box_counter = box_counter + 3
    return box_dict

def print_table(dict):
    row_counter = 1
    col_counter = 1
    print("-------------------------\n", end='')
    for k in dict:
        print('| ', end='')
        for char in dict[k]:
            print(f'{char} ', end='')
            if col_counter % 3 == 0:
                print("| ", end='')
            col_counter += 1
        print("\n", end='')
        if row_counter % 3 == 0:
            print("-------------------------\n", end='')
        row_counter += 1

def find_missing_numbers(lst):
    miss = set()
    for a in range(1,10):
        if lst.count(str(a)) == 0:
            miss.add(str(a))
    return miss

def update_missing_numbers_single_dic(dic):
    flag_do_it_again = False
    while True:
        for key in dic:
            vlist = dic[key]
            for num in range(0,9):
                if vlist[num] == ' ':
                    vlist[num] = find_missing_numbers(vlist)
                elif isinstance(vlist[num], set):
                    vlist[num] = vlist[num].intersection(find_missing_numbers(vlist))

                if isinstance(vlist[num], set) and len(vlist[num]) == 1:
                    vlist[num] = ''.join(list(map(str, vlist[num])))
                    flag_do_it_again = True
        if not flag_do_it_again:
            break
        else:
            flag_do_it_again = False
    return dic

def update_missing_numbers_all_dic(dic):
    while True:
        r_dict = update_missing_numbers_single_dic(dic)
        c_dict = transpose(r_dict)
        c_dict = update_missing_numbers_single_dic(c_dict)
        r_dict = transpose(c_dict)
        b_dict = transpose_box(r_dict)
        b_dict = update_missing_numbers_single_dic(b_dict)
        r_dict = transpose_box(b_dict)
        if dic == r_dict:
            break
        else:
            dic = r_dict
    return dic

def isresolved(rrdic):
    dic1 = dict(rrdic)
    for key in dic1:
        no_options = True
        row_solved = True
        klist = dic1[key]
        for a in range(0,9):
            if isinstance(klist[a], set):
                no_options = False
        if no_options:
            sorted_list = []
            sorted_list = list(klist)
            sorted_list.sort()
            res = ''.join(list(map(str, sorted_list)))
            if res != '123456789':
                row_solved = False
        if not no_options or not row_solved:
            return False
    return True

def update_unique_options(dic):
    for key in dic:
        ylist = dic[key]
        tlist = []
        for i in range(0,9):
            if isinstance(ylist[i], set):
                tlist = tlist + list(ylist[i])
        for item in tlist:
            if tlist.count(item) == 1:
                for j in range(0,9):
                    if isinstance(ylist[j], set):
                        if item in ylist[j]:
                            ylist[j] = item
    return dic

def resolve(dic):
    while True:
        r_dict = update_missing_numbers_all_dic(dic)

        if dic == r_dict:
            if isresolved(r_dict):
                print('\nSudoku Puzzle Solved..!!!')
                return r_dict
            else:
                # print('Running row unique...')
                rw_dict = update_unique_options(r_dict)
                rw_dict = update_missing_numbers_all_dic(rw_dict)
                # print_table(rw_dict)
                cl_dict = transpose(rw_dict)
                # print('Running col unique...')
                cl_dict = update_unique_options(cl_dict)
                # print_table(cl_dict)
                rw_dict = transpose(cl_dict)
                rw_dict = update_missing_numbers_all_dic(rw_dict)
                bx_dict = transpose_box(rw_dict)
                # print('Running box unique...')
                bx_dict = update_unique_options(bx_dict)
                # print_table(bx_dict)
                rw_dict = transpose_box(bx_dict)
                rw_dict = update_missing_numbers_all_dic(rw_dict)

                if r_dict == rw_dict:
                    if isresolved(rw_dict):
                        print('\nSudoku Puzzle Solved..!!!')
                        return rw_dict
                    else:
                        print('Complex puzzle. Unable to resolve..!')
                        return rw_dict
                else:
                    dic = rw_dict
        else:
            dic = r_dict

        # if pause():
        #     break

def main():
    re_dict = row_dict
    re_dict = resolve(re_dict)
    # print_table(re_dict)
    return re_dict
    
if __name__ == '__main__':
    main()
