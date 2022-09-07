from prepare_data import init_lists
from priority_rules import priority_rule, calc_ES_EF, calc_LS_LF

"""
Union of two lists. Lists are cast as sets, union is applied on sets which creatse
"""
def Union(lst1: list, lst2: list):
    final_list = list(set(lst1) | set(lst2))
    return final_list

def Intersection(lst1: list, lst2: list):
    final_list = list(set(lst1).intersection(set(lst2)))
    return final_list

def calc_Rk(R: list, A: list, t: int):
    Rk1 = R[0] - sum([A[t][i].res[0] for i in range(len(A[t]))])
    Rk2 = R[1] - sum([A[t][i].res[1] for i in range(len(A[t]))])
    Rk3 = R[2] - sum([A[t][i].res[2] for i in range(len(A[t]))])
    Rk4 = R[3] - sum([A[t][i].res[3] for i in range(len(A[t]))])
    return [Rk1, Rk2, Rk3, Rk4]


def calc_A(activities: list, F: list, t: int):
    ret_lst = []
    for j in range(len(activities)):
        try:
            if F[j]-activities[j].dur <= t and t < F[j]:
                ret_lst.append(activities[j])
        except:
            continue
    return ret_lst


def calc_Eg(activities: list, S: list, g: int):
    ret_lst = []
    J = list(set(activities) - set(S[g]))
    J.sort(key=lambda j: j.index)
    for j in J:
        #print(j.index, j.pred)
        if set(j.pred) <= set([S[g][i].index for i in range(len(S[g]))]):
            ret_lst.append(j)
    return ret_lst


def calc_F(activities: list, j: int, G: list, g: int, F: list, A: list, Rk: list, LF: list):

    if activities[j].pred == []:
        EFj = activities[j].dur
    else:
        EFj = max([F[h] for h in activities[j].pred]) + activities[j].dur
    #print('EFj in calc_F', EFj)

    t_temp = [i for i in range(EFj-activities[j].dur, LF[j]-activities[j].dur+1)]
    #print('temp', temp)
    t = Intersection(t_temp, G[g])
    t.sort()
    #print('t', t)

    ok = []
    for i in t:
        bool = 1
        tau_temp = [i for i in range(i,i+activities[j].dur+1)]
        tau = Intersection(tau_temp, G[g])
        tau.sort()
        #print('tau', tau)

        for k in tau:
            condition = activities[j].res[0] <= Rk[k][0] and activities[j].res[1] <= Rk[k][1] and activities[j].res[2] <= Rk[k][2] and activities[j].res[3] <= Rk[k][3]

            if Rk[k] != None:
                if not condition:
                    bool = 0
            else:
                A[k] = calc_A(activities, G, k)
                #print('A[k]', [j.index for j in A[k]])
                Rk[k] = calc_Rk(4, A, k)
                #print('Rk[k]', Rk[k])
                if not condition:
                    bool=0
        if bool:
            ok.append(i)
        else:
            if ok==[]:
                continue
            elif i-min(ok) < activities[j].dur:
                for i in range(min(ok)+activities[j].dur):
                    if i in ok:
                        ok.remove(i)
    #print('i iz calc_F', min(ok))
    return min(ok) + activities[j].dur


def serial_SGS(pr, activities, R):
    _, F, S, _, G, Rk, A, E = init_lists(activities)
    F[0] = 0
    S[0] = [activities[0]]
    A[0] = [activities[0]]
    j = 0
    ES, _ = calc_ES_EF(activities)
    LS, LF = calc_LS_LF(activities)
    for g in range(1,len(activities)):
        #print(g)
        E[g] = calc_Eg(activities, S, g-1)
        #print('E[g]', [E[g][i].index for i in range(len(E[g]))])
        G[g] = [F[j.index] for j in S[g-1]]
        #print('G[g]',G[g])
        for t in [t for t in G[g] if t!=None]:
            #print('t', t)
            A[t] = calc_A(activities, F, t)
            #print('A[t]',[A[t][i].index for i in range(len(A[t]))])
            Rk[t] = calc_Rk(R, A, t)
            #print('Rk', Rk[t])
        """
        t1 = F[j]-activities[j].dur
        t2 = F[j]
        A[t1] = calc_A(activities, F, t1)
        A[t2] = calc_A(activities, F, t2)
        Rk[t1] = calc_Rk(R, A, t1)
        Rk[t2] = calc_Rk(R, A, t2)
        """
        j = priority_rule(pr ,E[g], activities, ES, LS, LF)
        #print('j',j)
        #print('pred', activities[j].pred)
        F[j] = calc_F(activities, j, G, g, F, A, Rk, LF)
        #print('F[j]', F[j])
        S[g] = Union(S[g-1], [activities[j]])
        S[g].sort(key=lambda j: j.index)
        #print('S[g]',[S[g][i].index for i in range(len(S[g]))])
    return G