from math import inf

def priority_rule(pr, lst, activities, ES, LS, LF):
    if pr == 'SPT':
        return SPT(lst)
    elif pr == 'MIS':
        return MIS(lst)
    elif pr == 'LST':
        return LST(lst, LS)
    elif pr == 'LFT':
        return LFT(lst, LF)
    elif pr == 'MSL':
        return MSL(lst, ES, LS)
    elif pr == 'MTS':
        return MTS(lst, activities)
    elif pr == 'GRPW':
        return GRPW(lst, activities)
    elif pr == 'GRPW2':
        return GRPW2(lst, activities)
    else:
        raise ValueError('Invalid string value given.')


def SPT(lst):
    min = inf
    ret_index = None
    for el in lst:
        if el.dur < min:
            min = el.dur
            #print(min)
            ret_index = el.index
    return ret_index


def MIS(lst):
    max = -inf
    ret_index = None
    for el in lst:
        if len(el.succ) > max:
            max = len(el.succ)
            ret_index = el.index
    return ret_index


def calc_LS_LF(activities):
    n = len(activities)
    LS = [None]*n
    LF = [None]*n
    LS[n-1] = sum([activities[i].dur for i in range(n)])
    LF[n-1] = sum([activities[i].dur for i in range(n)])
    for j in reversed(range(n-1)):
        LF[j] = min([LS[i] for i in activities[j].succ])
        LS[j] = LF[j] - activities[j].dur
    return LS, LF

def LST(lst, LS):
    min = inf
    ret_index = None
    for el in lst:
        if LS[el.index] < min:
            min = LS[el.index]
            ret_index = el.index
    return ret_index

def LFT(lst, LF):
    min = inf
    ret_index = None
    for el in lst:
        if LF[el.index] < min:
            min = LF[el.index]
            ret_index = el.index
    return ret_index


def calc_ES_EF(activities):
    n = len(activities)
    ES = [None]*n
    EF = [None]*n
    ES[0] = 0
    EF[0] = 0
    for j in range(1,n):
        ES[j] = max([EF[i] for i in activities[j].pred])
        EF[j] = ES[j] + activities[j].dur
    return ES, EF

def MSL(lst, ES, LS):
    min = inf
    ret_index = None
    for el in lst:
        if LS[el.index]-ES[el.index] < min:
            min = LS[el.index]-ES[el.index]
            ret_index = el.index
    return ret_index


def GRPW(lst, activities):
    max = -inf
    ret_index = None
    sum_j = 0
    for el in lst:
        sum_j = sum([activities[i].dur for i in el.succ])
        if el.dur + sum_j > max:
            #print(sum_j)
            max = el.dur + sum_j
            ret_index = el.index
    return ret_index


def total_successors(activities, j, lst):
    if activities[j].succ == []:
        return
    else:
        for i in activities[j].succ:
            lst.append(i)
            total_successors(activities, i, lst)
        lst = list(dict.fromkeys(lst))
        lst.sort()
        return lst

def MTS(lst, activities):
    max = -inf
    ret_index = None
    for el in lst:
        if el == activities[-1]:
            return el.index
        total_succ = total_successors(activities, el.index, [])
        if len(total_succ) > max:
            max = len(total_succ)
            #print(max)
            ret_index = el.index
    return ret_index

def GRPW2(lst, activities):
    max = -inf
    ret_index = None
    sum_j = 0
    for el in lst:
        if el == activities[-1]:
            return el.index
        total_succ = total_successors(activities, el.index, [])
        sum_j = sum([activities[i].dur for i in total_succ])
        if el.dur + sum_j > max:
            max = el.dur + sum_j
            #print(max)
            ret_index = el.index
    return ret_index
