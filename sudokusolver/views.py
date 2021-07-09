from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

dict_val = {}
dict_val = {1:4, 2:0, 3:4, 4:6, 5:1, 6:9, 7:4, 8:0, 9:4}
# count = {'count': range(1,10)}
count = {
    1: ['','','','','','','','',''], 
    2: ['','','','','','','','',''], 
    3: ['','','','','','','','',''], 
    4: ['','','','','','','','',''], 
    5: ['','','','','','','','',''], 
    6: ['','','','','','','','',''], 
    7: ['','','','','','','','',''], 
    8: ['','','','','','','','',''], 
    9: ['','','','','','','','','']}

box_dict = {}
option_dict = {}
row_dict = {}
row_dict = {
    1: list(' 23497 85'), 
    2: list('58  2 7 4'), 
    3: list('7 65 3   '), 
    4: list(' 9 76  51'), 
    5: list('   35  2 '), 
    6: list(' 6   9   '), 
    7: list('472 3    '), 
    8: list('    45 97'), 
    9: list('95   8  2')}

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
                return r_dict
            else:
                rw_dict = update_unique_options(r_dict)
                rw_dict = update_missing_numbers_all_dic(rw_dict)
                cl_dict = transpose(rw_dict)
                cl_dict = update_unique_options(cl_dict)
                rw_dict = transpose(cl_dict)
                rw_dict = update_missing_numbers_all_dic(rw_dict)
                bx_dict = transpose_box(rw_dict)
                bx_dict = update_unique_options(bx_dict)
                rw_dict = transpose_box(bx_dict)
                rw_dict = update_missing_numbers_all_dic(rw_dict)

                if r_dict == rw_dict:
                    if isresolved(rw_dict):
                        return rw_dict
                    else:
                        return rw_dict
                else:
                    dic = rw_dict
        else:
            dic = r_dict

def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {'dict_val': count, 'msg': 'enter'})
    elif request.method == 'POST':
        if request.POST.get('reset') == 'Reset':
            return redirect(reverse('home'), {'dict_val': count, 'msg': 'enter'})
        else:
            box_values = request.POST.getlist('box[]')
            flag_data_found = False

            for v in box_values:
                if v != '':
                    flag_data_found = True

            if flag_data_found:
                val_dict = {}
                j = 1

                for i in range(1, len(box_values)+1):
                    val = lambda x:val_dict[x] if x in val_dict else ''
                    temp_list = list(val(j))
                    if box_values[i-1] == '':
                        value = ' '
                    else:
                        value = box_values[i-1]
                    temp_list.append(value)
                    val_dict[j] = temp_list
                    if i % 9 == 0:
                        j = j + 1
                        temp_list = []

                solved_dict = {}
                solved_dict = resolve(val_dict)
                return render(request, 'home.html', {'dict_val': solved_dict, 'msg': 'done'})
            else:
                return render(request, 'home.html', {'dict_val': count, 'msg': 'error'})

def sample(request):
    if request.method == 'GET':
        return render(request, 'home.html', {'dict_val': row_dict, 'msg': 'sample'})
    elif request.method == 'POST':
        return home(request)

def reset(request):
    if request.method == 'GET':
        return render(request, 'home.html', {'dict_val': count, 'msg': 'enter'})
    elif request.method == 'POST':
        return home(request)