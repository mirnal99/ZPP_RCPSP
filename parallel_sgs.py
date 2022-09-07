from prepare_data import init_lists
from priority_rules import priority_rule, calc_ES_EF, calc_LS_LF

def Union(lst1, lst2):
    final_list = list(set(lst1) | set(lst2))
    return final_list

def not_scheduled(J, C):
    return list(set(J) - set(C))


def cacl_Cg(activities, F, tg) :
    ret_lst = []
    for j in range(len(activities)):
        try:
            if F[j] <= tg:
                ret_lst.append(activities[j])
        except:
            continue
    return ret_lst

def calc_Ag(activities, F, tg):
    ret_lst = []
    for j in range(len(activities)):
        try:
            if F[j]-activities[j].dur <= tg and tg < F[j]:
                ret_lst.append(activities[j])
        except:
            continue
    return ret_lst

def calc_Rk(R, A, g):
    Rk1 = R[0] - sum([A[g][i].res[0] for i in range(len(A[g]))])
    Rk2 = R[1] - sum([A[g][i].res[1] for i in range(len(A[g]))])
    Rk3 = R[2] - sum([A[g][i].res[2] for i in range(len(A[g]))])
    Rk4 = R[3] - sum([A[g][i].res[3] for i in range(len(A[g]))])
    return [Rk1, Rk2, Rk3, Rk4]

def calc_Eg(activities, C, A, Rk, t, g):
    ret_lst = []
    J = list(set(activities) - set(Union(C[g],A[g])))
    J.sort(key=lambda j: j.index)
    #print([j.index for j in J])
    for j in J:
        if set(j.pred) <= set([C[g][i].index for i in range(len(C[g]))]) and (j.res[0] <= Rk[t[g]][0] and j.res[1] <= Rk[t[g]][1] and j.res[2] <= Rk[t[g]][2] and j.res[3] <= Rk[t[g]][3]):
                ret_lst.append(j)
    return ret_lst


def parallel_SGS(pr, activities, R):
    t, F, _, A, C, Rk, _, E = init_lists(activities)
    g=0
    t[g] = 0
    A[0] = [activities[0]]
    C[0] = [activities[0]]
    Rk[0] = [R,R,R,R]
    F[0] = 0
    ES, _ = calc_ES_EF(activities)
    LS, LF = calc_LS_LF(activities)
    while len(Union(A[g],C[g])) <= len(activities)-2:
        g += 1
        t[g] = min([F[j.index] for j in A[g-1]])
        C[g] = cacl_Cg(activities, F, t[g])
        #print([C[g][i].index for i in range(len(C[g]))])
        A[g] = calc_Ag(activities, F, t[g])
        #print(t[g])
        Rk[t[g]] = calc_Rk(R, A, g)
        #print("slobodni resursi", Rk[t[g]])
        #print("tg", t[g])
        E[g] = calc_Eg(activities, C, A, Rk, t, g)
        #print([E[g][i].index for i in range(len(E[g]))])
        while len(E[g]) > 0:
            #print([E[g][i].index for i in range(len(E[g]))])
            j = priority_rule(pr, E[g], activities, ES, LS, LF)
            #print(j)
            F[j] = t[g] + activities[j].dur
            A[g] = calc_Ag(activities, F, t[g])
            #print([A[g][i].index for i in range(len(A[g]))])
            Rk[t[g]] = calc_Rk(R, A, g)
            #print("slobodni resursi (u)", Rk[t[g]])
            #print("tg (u)", t[g])
            E[g] = calc_Eg(activities, C, A, Rk, t, g)
            #print(len(E[g]))
    F[len(activities)-1] = max([F[h] for h in activities[len(activities)-1].pred])
    #print(Rk)
    return F