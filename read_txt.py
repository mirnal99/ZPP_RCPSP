def read_txt_muli_lines(file_name, start_line, finish_line, del_num):
    """
    This method extract lines from start_line to finish_line from file_name removing new lines.
    From that, it then strips lines by spaces and removes all white spaces from them resulting in list with non white space characters.
    Returns list of lists with lines without white spaces and new line.
    """
    with open(file_name) as f:
        lines = f.readlines()
        temp = lines[start_line:finish_line] # extract lines
        # list with lines without new line char
        list = []
        for line in temp:
            list.append(line.rstrip('\n'))

        return_list = []
        for l in list:
            lsplit = l.split(' ') # split by space
            # remove spaces from list
            temp_list = []
            for el in lsplit:
                if el.strip():
                    el = int(el)
                    temp_list.append(el)

            del temp_list[1:del_num]
            return_list.append(temp_list)

        return return_list

def read_txt_single_line(file_name, line):
    """
    This method reads line from file, strips it by new line and splits it by white spaces.
    Return list with line without white spaces and new line.
    """
    with open(file_name) as f:
        lines = f.readlines()
        return_list = lines[line].rstrip('\n').split()
        for i in range(len(return_list)):
            return_list[i] = int(return_list[i])
        return return_list


if __name__ == "__main__":
    file_name = 'j301_1.txt'
    print(read_txt_muli_lines(file_name, 54, 86, 2))
    #print(read_txt_single_line(file_name, 89))