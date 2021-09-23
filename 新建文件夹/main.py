# EE308 LAB2
# Author:   19104324-831901305-Ma Huijuan
# Date:     2021.09.21
# Request: Extract keywords of different levels from the C or C++ code files that are read in.
# Remind: The format in the target file must be right.
#         Do not use 4 space to replace a tab.
#         Do not have more than one space in a "else if" keyword.

import os

while True:
    filePath = input("The file address:")
    if os.path.exists(filePath):
        # Path exists
        total_txt = open(filePath, 'r').read()  # Read file as string
        break

txt_list = total_txt.split('\n')

# delete all annotation
for i in txt_list:
    if '#' in i:
        txt_list[txt_list.index(i)] = i[:i.index('#')]

dic = {
    1: "auto", 2: "break", 3: "case", 4: "char", 5: "const", 6: "continue", 7: "default", 8: "double", 9: "do",
    10: "else",
    11: "enum", 12: "extern", 13: "float", 14: "for", 15: "goto", 16: "if", 17: "int", 18: "long", 19: "register",
    20: "return",
    21: "short", 22: "signed", 23: "sizeof", 24: "static", 25: "struct", 26: "switch", 27: "typedef", 28: "union",
    29: "unsigned", 30: "void",
    31: "volatile", 32: "while"
}


def getResult():
    level = int(input("The completion level(1-4) is "))
    if level == 1:
        txtCopy = total_txt
        keywords = 0
        for index in range(1, 33):
            txtLen = len(txtCopy)
            if txtCopy.find(dic[index]) != -1:
                # The keyword is in the file.
                keywordLen = len(dic[index])
                txtCopy = txtCopy.replace(dic[index], "")  # Delete one type of keyword.
                newTxtLen = len(txtCopy)
                keywords += (txtLen - newTxtLen) / keywordLen
                # Calculate how many this keyword in file
        print("\ntotal num: ", int(keywords))
        return int(keywords)

    elif level == 2:
        txtCopy = total_txt
        str1 = "switch"
        str2 = "case"
        indexOfStr1 = []

        start = txtCopy.find(str1)  # Get the first index of Str1
        indexOfStr1.append(start)
        while start != -1:
            # Next Str1 exists.
            txtCopy = txtCopy[start + 1:]
            start = txtCopy.find(str1)
            if start == -1:
                # There is no Str1 below.
                break
            else:
                # If Str1 can still be found bellow, add it to list.
                indexOfStr1.append(start + indexOfStr1[-1])

        numOfStr1 = len(indexOfStr1)
        numOfStr2 = set()

        # Renew
        txtCopy = total_txt

        for ele in range(0, numOfStr1):  # 0, 1, no 2
            # Search Str2 between two Str1 and bellow the last Str1
            if ele == numOfStr1 - 1:  # Search Str2 bellowed the last Str1
                TxtLen = len(txtCopy[indexOfStr1[ele]:-1])
                # Delete all Str2 to get the number of Str2 bellowed the last Str1
                txtCopy = txtCopy[indexOfStr1[ele]:-1].replace("case", "")
            else:  # Search Str2 between two Str1
                TxtLen = len(txtCopy[indexOfStr1[ele]:indexOfStr1[ele + 1]])
                # Delete all Str2 to get the number of Str2 bellowed the last Str1
                txtCopy = txtCopy[indexOfStr1[ele]:indexOfStr1[ele + 1]]
                txtCopy = txtCopy.replace("case", "")

            newTxtLen = len(txtCopy)
            # list the number of Str2 for different Str1
            numOfStr2.add(int((TxtLen - newTxtLen) / len(str2)))

            # Renew
            txtCopy = total_txt
        # Output
        print("switch num: ", numOfStr1, "\ncase num: " + " ".join(str(ele) for ele in numOfStr2))
        return [2, 3, 2]

    elif (level == 3) or (level == 4):
        str1 = "if"
        str2 = "else"
        str3 = "elf"

        counter_for_else = 0
        counter_for_elseif = 0
        # Turn all "else if" to "elf"
        # Avoid the code confusing "else" and "else if", "if" and "elise if"

        lit = total_txt.replace("se i", "").split('\n')

        tab_group = set()  # Store the situation about the number of layers
        for ele in lit:
            # Find how many layers it has
            j = ele.replace("\t", "")
            tab = (len(ele) - len(j)) / 4
            if tab != 0 and tab not in tab_group:
                tab_group.add(tab)


        arrange = []  # This list arranges different layers in different sublist.
        layer = len(tab_group)  # Layers counter
        while layer > 0:
            # Add strings in same layers into same sublist.
            arrange.append([])
            for i in lit:
                if ("\t" * layer) in i:
                    lit[lit.index(i)] = ""
                    arrange[len(tab_group) - layer].append(i)
            layer -= 1

        counter_for_arrange = 0
        for i in arrange:

            indexs_else = [-1]
            indexs_elseif = [-1]
            indexs_if = [-1]
            arrange[counter_for_arrange] = ''.join(i)

            # find "if" in one layer
            index = arrange[counter_for_arrange].find(str1)
            if index != -1:
                indexs_if[0] = index  # First if's location
                while True:
                    add_ele = arrange[counter_for_arrange][index + len(str1):].find(str1)  # -1 if not finded
                    if add_ele != - 1:
                        indexs_if.append(add_ele + index + len(str1))
                        index += add_ele + len(str1)
                    else:
                        break

            # find "else" in one layer
            index = arrange[counter_for_arrange].find(str2)
            if index != -1:
                indexs_else[0] = index  # First else's location
                while True:
                    addEle = arrange[counter_for_arrange][index + len(str2):].find(str2)
                    if addEle != - 1:
                        indexs_else.append(addEle + index + len(str2))
                        index += addEle + len(str2)
                    else:
                        break
            # find "elf" in one layer
            index = arrange[counter_for_arrange].find(str3)
            if index != -1:
                indexs_elseif[0] = index  # the first elf's location
                while True:
                    # Add all elf's index in list
                    addEle = arrange[counter_for_arrange][index + len(str3):].find(str3)
                    if addEle != - 1:
                        indexs_elseif.append(addEle + index + len(str3))
                        index += addEle + len(str3)
                    else:
                        break

            if_else = []  # List all indexes of "if...else" structure
            for j in indexs_if:
                for k in indexs_else:
                    if j >= k:
                        # For "if-else", "if" must be located before "else"
                        continue
                    elif j == indexs_if[-1] and k == indexs_else[-1] and j < k:
                        # j < k: for "if-else", "if" must be located before "else"
                        # The last pair of "if-else"
                        if_else.append([j, k])
                    elif k in range(j, indexs_if[indexs_if.index(j) + 1]):
                        # If there is an "else" between two "if",
                        # there must be a pair of "if-else".
                        if_else.append([j, k])
                    else:  # "if..if..else" structure
                        continue

            # Find "if-elseif-else" and "if-else" structures
            for h in if_else:

                # Take a pair of indexes of "if-else"
                if indexs_elseif[0] == -1:
                    # There is no "else" in this layer.
                    # No "else" exists , then no any structure about "if" exists
                    break
                for L in indexs_elseif:
                    if h[1] > L > h[0]:
                        # There is at least an "elf" in this pair of "if-else".
                        # It is not "if-else" structure.
                        counter_for_elseif += 1
                        break
                    if L == indexs_elseif[-1]:
                        counter_for_else += 1

            counter_for_arrange += 1

        if level == 3:
            print("\nif-else num :", counter_for_else)
            return counter_for_else
        else:
            print("\nif-elseif-else num :", counter_for_elseif)
            return counter_for_elseif

# Run
getResult()
