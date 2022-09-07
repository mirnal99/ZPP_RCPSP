import matplotlib.pyplot as plt
from serial_sgs import serial_SGS
from parallel_sgs import parallel_SGS
from prepare_data import prepare_data

"""
list_of_colors = ["black", "lightcoral", "maroon", "orangered","lightsalmon", "darksalmon", "saddlebrown", "chocolate", "darkorange", "wheat", "goldenrod", "yellow", "darkolivegreen", "greenyellow", "green", "lime","aquamarine", "lightseagreen","teal", "cyan", "lightskyblue", "dodgerblue", "navy", "mediumpurple", "darkviolet","plum", "purple", "magenta", "deeppink", "crimson","pink","grey"]
"""
list_of_colors = ['#7B4E45', '#856582', '#D609FB', '#6DA986', '#067F10', '#E225F7', '#8C241A', '#7BF7D2', '#DEDAEA', '#755234', '#995DEC', '#0BDC0B', '#202DC8', '#5103C6', '#865C12', '#DFE8F1', '#348CBD', '#43EFD5', '#F10800', '#AF9BBE', '#E4B7F3', '#ABC9C3', '#33BACF', '#E3DD87', '#863E2E', '#64D073', '#6100D6', '#CB6A51', '#FA81A0', '#409BC3', '#12C8EB', '#40F442', '#0B7811', '#33F159', '#B1362C', '#95B6A1', '#069F33', '#B71E18', '#500251', '#F49FD6', '#50C5E7', '#38EBEE', '#EF1DBC', '#49C680', '#45A7E0', '#7D5DFC', '#3E21B1', '#79ADDD', '#E195BE', '#A0A662', '#5796BB', '#1363DE', '#EBB2F2', '#5971DF', '#EC952C', '#AE2749', '#06D212', '#F30940', '#B7E9C4', '#2D973D', '#C45F25', '#059918', '#2F0695', '#C5ADD1', '#BD1829', '#561911', '#BBAF9A', '#8F02EA', '#5C2BFF', '#43498B', '#722D46', '#D5A340', '#E672BC', '#6730E4', '#0B0E71', '#BB82C4', '#E2C0C1', '#923B4B', '#83A59E', '#DEC109', '#DF2EC5', '#876144', '#8BA728', '#16A9CA', '#EC8E26', '#5FA71F', '#338838', '#3C9629', '#DFE1A0', '#8D5C87', '#FB8248', '#27E5CE', '#92306C', '#AACF5A', '#D4C064', '#49DB15', '#DABF24', '#62ADAD', '#AB6463', '#C940B3', '#E88B9D', '#C205E1', '#7C55E6', '#4E8F7A', '#7BE02C', '#F24CC3', '#4871AB', '#88ED07', '#45279A', '#69B326', '#0188EE', '#346259', '#59120B', '#9BD088', '#7F78B6', '#EF94FA', '#D8E9A1', '#F184B8', '#5C1F6D', '#0CB032', '#DC097E']

global maxF
global maxR


#Napravi usporedbu trenutne aktivnosti i s prethodnim aktivnostima koje su vec 'stavljenje u raspored', prilagodi visinu i vrati je
def overlapping(i: int, J: list, F: list, r: int, height:list, R:list):

    # usporedi trenutnu aktivnost sa svim prethodnicima
    for j in reversed(range(i)):

        # trajanje
        len_set1 = set(range(F[J[j].index]-J[j].dur, F[J[j].index]))
        len_set2 = set(range(F[J[i].index]-J[i].dur, F[J[i].index]))
        # resursi
        res_set1 = set(range(height[j], height[j]+J[j].res[r]))
        res_set2 = set(range(height[i], height[i]+J[i].res[r]))

        # ako se aktivnosti preklapaju u trajanu i resursima
        if len_set1.intersection(len_set2) and res_set1.intersection(res_set2):
            # ako ima dovoljno mjesta iznad prethodne aktivnosti, stavi trenutnu aktivnost na nju
            if R[r] - (height[j]+J[j].res[r]) >= J[i].res[r]:
                height[i] = height[j]+J[j].res[r]
            # ako ima dovoljno mjesta iznad trenutne aktivnosti, stavi prethodnu aktivnost na nju
            elif R[r] - (height[i]+J[i].res[r]) >= J[j].res[r]:
                height[j] = height[i]+J[i].res[r]
            # inace postavi visinu trenutne na dno
            else:
                height[i] = 0

    return height


# Provjeri preklapanje svake aktivnosti sa svakom i popravi height
def overlappingAll(J: list, F: list, r: int, height:list, R:list):

    for i in range(len(J)):
        for j in range(len(J)):

            # nema smisla usporedivati aktivnost samu sa sobom
            if i==j:
                continue

            # trajanje
            len_set1 = set(range(F[J[j].index]-J[j].dur, F[J[j].index]))
            len_set2 = set(range(F[J[i].index]-J[i].dur, F[J[i].index]))
            # resursi
            res_set1 = set(range(height[j], height[j]+J[j].res[r]))
            res_set2 = set(range(height[i], height[i]+J[i].res[r]))

            # ako se aktivnosti preklapaju u trajanu i resursima
            if len_set1.intersection(len_set2) and res_set1.intersection(res_set2):
                # ako ima dovoljno mjesta iznad j-te aktivnosti, stavi i-tu aktivnost na nju
                if R[r] - (height[j]+J[j].res[r]) >= J[i].res[r]:
                    height[i] = height[j]+J[j].res[r]
                # ako ima dovoljno mjesta iznad i-te aktivnosti, stavi j-tu aktivnost na nju
                elif R[r] - (height[i]+J[i].res[r]) >= J[j].res[r]:
                    height[j] = height[i]+J[i].res[r]
                # (kada i-ta aktinost na vrhu y-osi)
                # ako ima mjesta ispod i-te aktivnosti, stavi j-tu aktivnost ispod nje
                elif R[r] - J[i].res[r] >= J[j].res[r]:
                    height[j] = height[i]-J[j].res[r]
                # inace stavi j-tu aktivnost na dno
                else:
                    height[j] = 0

    return height

"""
Izracunaj i vrati početnu visinu svake aktivnosti
"""
def calc_height(J:list, F:list, r:int, R:list):

    height = []

    for i in range(len(J)):

        # prva aktivnost iz skupa J ide na dno, ne provjeravaj ostale uvjete
        if i==0:
            height.append(0)
            continue

        # trajanje
        set1 = set(range(F[J[i-1].index]-J[i-1].dur, F[J[i-1].index]))
        set2 = set(range(F[J[i].index]-J[i].dur, F[J[i].index]))

        # ako se prethodna i trenutna aktivnost vremenski preklapaju
        if len(set1.intersection(set2)) > 0:
            # stavi trenutnu aktivnost na prethodnu
            height.append(height[i-1]+J[i-1].res[r])
        else: # inace ide na dno
            height.append(0)

        # ako visina trenutne aktivnosti prelazi granicu, stavi je na dno
        if (height[i]+J[i].res[r] > R[r]):
            height[i] = 0

        # update-aj aktivnost u ovisnosti s prethodnim
        overlapping(i, J, F, r, height, R)

    # (na kraju petlje)
    # provjeri sve aktivnosti jos jednom svaka sa sobom
    overlappingAll(J, F, r, height, R)

    return height

""" 
Vrati skup aktivnosti koje se pojavljuju u trenutnom resursu r i poredaj ih po vremenu početka
"""
def calc_J(activities, F, r):
    
    J = []
    for i in range(1, len(activities)-1):
        if activities[i].res[r] != 0:
            J.append(activities[i])
    J.sort(key=lambda j: F[j.index]-j.dur)

    return J

"""
Nacrtaj raspored u cetiri grafa i spremi ih kao slike
"""
def get_imgs(num, file, sgs, pr):

    activities, R = prepare_data(num, '.\\data\\' + num + '\\' + file)

    if sgs == 'Parallel':
        F = parallel_SGS(pr, activities, R)
    elif sgs == 'Serial':
        G = serial_SGS(pr, activities, R)
        F = G[-1]
    else:
        raise ValueError('Invalid string value given.')

    for r in range(len(R)):

        J = calc_J(activities, F, r)
        height = calc_height(J, F, r, R)

        maxF = max(F)
        maxR = max([r for r in R])

        plt.rcParams["figure.figsize"] = [maxF/2, maxR/4]
        plt.rcParams["figure.autolayout"] = True
        #plt.rcParams['hatch.linewidth'] = 55.0  


        fig = plt.figure()
        schedule = fig.add_subplot(111)
        #_, schedule = plt.subplots()

        # drawing activities on a graph
        for i in range(len(J)):
            schedule.broken_barh(
                [(F[J[i].index]-J[i].dur, J[i].dur)],   # [(start_time, duration)],
                (height[i], J[i].res[r]),               # (lower_yaxis, height),
                facecolor=list_of_colors[J[i].index],
                edgecolor='black', 
                linewidth = 2,
                label=J[i].index
                )

        # Set x and y axis numbers
        schedule.set_xticks(list(range(maxF+1)))
        schedule.set_yticks(list(range(R[r]+1)))

        # Label ticks and axes
        if r > 0:
            schedule.set_xticklabels('')
        else:
            schedule.set_xlabel('Time', fontsize=15)
        
        schedule.set_ylabel('R'+str(r+1), fontsize=15)

        plt.xticks(fontsize=15)
        plt.yticks(fontsize=12)

        plt.xlim([0, maxF])
        #plt.ylim([0, maxR])
        
        plt.grid(True)
        plt.savefig(".\imgs\img" + str(r) + ".png", transparent=False)
        plt.close(fig)

    return maxF, maxR