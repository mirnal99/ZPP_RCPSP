from matplotlib import pyplot as plt
import matplotlib.patches as mpatches


"""
list_of_colors = ["black", "lightcoral", "maroon", "orangered","lightsalmon", "darksalmon", "saddlebrown", "chocolate", "darkorange", "wheat", "goldenrod", "yellow", "darkolivegreen", "greenyellow", "green", "lime","aquamarine", "lightseagreen","teal", "cyan", "lightskyblue", "dodgerblue", "navy", "mediumpurple", "darkviolet","plum", "purple", "magenta", "deeppink", "crimson","pink","grey"]
"""
list_of_colors = ['#7B4E45', '#856582', '#D609FB', '#6DA986', '#067F10', '#E225F7', '#8C241A', '#7BF7D2', '#DEDAEA', '#755234', '#995DEC', '#0BDC0B', '#202DC8', '#5103C6', '#865C12', '#DFE8F1', '#348CBD', '#43EFD5', '#F10800', '#AF9BBE', '#E4B7F3', '#ABC9C3', '#33BACF', '#E3DD87', '#863E2E', '#64D073', '#6100D6', '#CB6A51', '#FA81A0', '#409BC3', '#12C8EB', '#40F442', '#0B7811', '#33F159', '#B1362C', '#95B6A1', '#069F33', '#B71E18', '#500251', '#F49FD6', '#50C5E7', '#38EBEE', '#EF1DBC', '#49C680', '#45A7E0', '#7D5DFC', '#3E21B1', '#79ADDD', '#E195BE', '#A0A662', '#5796BB', '#1363DE', '#EBB2F2', '#5971DF', '#EC952C', '#AE2749', '#06D212', '#F30940', '#B7E9C4', '#2D973D', '#C45F25', '#059918', '#2F0695', '#C5ADD1', '#BD1829', '#561911', '#BBAF9A', '#8F02EA', '#5C2BFF', '#43498B', '#722D46', '#D5A340', '#E672BC', '#6730E4', '#0B0E71', '#BB82C4', '#E2C0C1', '#923B4B', '#83A59E', '#DEC109', '#DF2EC5', '#876144', '#8BA728', '#16A9CA', '#EC8E26', '#5FA71F', '#338838', '#3C9629', '#DFE1A0', '#8D5C87', '#FB8248', '#27E5CE', '#92306C', '#AACF5A', '#D4C064', '#49DB15', '#DABF24', '#62ADAD', '#AB6463', '#C940B3', '#E88B9D', '#C205E1', '#7C55E6', '#4E8F7A', '#7BE02C', '#F24CC3', '#4871AB', '#88ED07', '#45279A', '#69B326', '#0188EE', '#346259', '#59120B', '#9BD088', '#7F78B6', '#EF94FA', '#D8E9A1', '#F184B8', '#5C1F6D', '#0CB032', '#DC097E']

plt.rcParams["figure.figsize"] = [1, 6.5]
plt.rcParams["figure.autolayout"] = True


patches1 = []
for i in range(1,31):
        patches1.append(mpatches.Patch(color=list_of_colors[i], label=i))
patches2 = []
for i in range(31,61):
        patches2.append(mpatches.Patch(color=list_of_colors[i], label=i))
patches3 = []
for i in range(61,91):
        patches3.append(mpatches.Patch(color=list_of_colors[i], label=i))
patches4 = []
for i in range(91,121):
        patches4.append(mpatches.Patch(color=list_of_colors[i], label=i))

patches = [patches1, patches2, patches3, patches4]
for i in range(4):
        fig = plt.figure()
        fig.legend(handles=patches[i])
        fig.savefig('legend' + str(i) + '.png')
        plt.close(fig)