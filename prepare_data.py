from read_txt import read_txt_muli_lines, read_txt_single_line
from activity import Activity


def get_pred(succ_dict, val):

    if val == 0:
        return []

    ret_lst = []
    for key, value in succ_dict.items():
        for el in value:
            if val == el:
                ret_lst.append(key)
                continue
            
    return ret_lst


def prepare_data(num, file_dir):

    if num=='30':
        successors = read_txt_muli_lines(file_dir, 18, 50, 3)
        dur_res = read_txt_muli_lines(file_dir, 54, 86, 2)
        R = read_txt_single_line(file_dir, 89)
    elif num=='60':
        successors = read_txt_muli_lines(file_dir, 18, 80, 3)
        dur_res = read_txt_muli_lines(file_dir, 84, 146, 2)
        R = read_txt_single_line(file_dir, 149)
    elif num=='90':
        successors = read_txt_muli_lines(file_dir, 18, 110, 3)
        dur_res = read_txt_muli_lines(file_dir, 114, 206, 2)
        R = read_txt_single_line(file_dir, 209)
    elif num=='120':
        successors = read_txt_muli_lines(file_dir, 18, 140, 3)
        dur_res = read_txt_muli_lines(file_dir, 144, 266, 2)
        R = read_txt_single_line(file_dir, 269)
    else:
        raise ValueError('Invalid string passed')

    succ_dict = {}
    for el in successors:
        for i in range(len(el)):
            el[i] = el[i]-1
        succ_dict[el[0]] = el[1:]

    activities = []
    for i in range(int(num)+2):
        activities.append(Activity(i, dur_res[i][1], dur_res[i][2:], succ_dict[i], get_pred(succ_dict, i)))

    return activities, R


def init_lists(activities):
    n = len(activities)
    t = [None]*n
    F = [None]*n
    S = [None]*n
    Ag = [None]*n
    C = [None]*n
    Rk = [None]*sum([activities[j].dur for j in range(n)])
    At = [None]*sum([activities[j].dur for j in range(n)])
    E = [None]*n
    return t, F, S, Ag, C, Rk, At, E