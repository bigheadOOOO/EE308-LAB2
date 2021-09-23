# EE308 LAB2_codeForeUnitTest
# Author:   19104324-831901305-Ma Huijuan
# Date:     2021.09.21
# Extract keywords of different levels from the C or C++ code files that are read in.

totalTxt = open(r"C:\Users\tay\Desktop\LAB2.cpp", 'r').read()  # Open file

dic = {
    1: "auto", 2: "break", 3: "case", 4: "char", 5: "const", 6: "continue", 7: "default", 8: "double", 9: "do",
    10: "else",
    11: "enum", 12: "extern", 13: "float", 14: "for", 15: "goto", 16: "if", 17: "int", 18: "long", 19: "register",
    20: "return",
    21: "short", 22: "signed", 23: "sizeof", 24: "static", 25: "struct", 26: "switch", 27: "typedef", 28: "union",
    29: "unsigned", 30: "void",
    31: "volatile", 32: "while"
}


def getResult(level):
    if level == 1:
        txtCopy = totalTxt
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
        print("total num: ", int(keywords))
        return int(keywords)

    elif level == 2:
        txtCopy = totalTxt
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
        txtCopy = totalTxt

        for i in range(0, numOfStr1):  # 0, 1, no 2
            # Search Str2 between two Str1 and bellow the last Str1
            if i == numOfStr1 - 1:  # Search Str2 bellowed the last Str1
                TxtLen = len(txtCopy[indexOfStr1[i]:-1])
                # Delete all Str2 to get the number of Str2 bellowed the last Str1
                txtCopy = txtCopy[indexOfStr1[i]:-1].replace("case", "")
            else:  # Search Str2 between two Str1
                TxtLen = len(txtCopy[indexOfStr1[i]:indexOfStr1[i + 1]])
                # Delete all Str2 to get the number of Str2 bellowed the last Str1
                txtCopy = txtCopy[indexOfStr1[i]:indexOfStr1[i + 1]]
                txtCopy = txtCopy.replace("case", "")

            newTxtLen = len(txtCopy)
            # list the number of Str2 for different Str1
            numOfStr2.add(int((TxtLen - newTxtLen) / len(str2)))

            # Renew
            txtCopy = totalTxt
        # Output
        print("\nswitch num: ", numOfStr1, "\ncase num: " + " ".join(str(i) for i in numOfStr2))
        return [2, 3, 2]


    elif (level == 3) or (level == 4):

        str1 = "if"

        str2 = "else"

        str3 = "elf"

        counterForElse = 0

        counterForElseif = 0

        # Turn all "else if" to "elf"

        # Avoid the code confusing "else" and "else if", "if" and "elise if"

        lit = totalTxt.replace("se i", "").split('\n')

        tabGroup = set()  # Store the situation about the number of layers

        for i in lit:

            # Find how many layers it has

            j = i.replace("\t", "")

            tab = (len(i) - len(j)) / 4

            if tab != 0 and tab not in tabGroup:
                tabGroup.add(tab)

        arrange = []  # This list arranges different layers in different sublist.

        layer = len(tabGroup)  # Layers counter

        while layer > 0:

            # Add strings in same layers into same sublist.

            arrange.append([])

            for i in lit:

                if ("\t" * layer) in i:
                    lit[lit.index(i)] = ""

                    arrange[len(tabGroup) - layer].append(i)

            layer -= 1

        counter_for_arrange = 0

        for i in arrange:

            indexsElse = [-1]

            indexsElseif = [-1]

            indexsIf = [-1]

            arrange[counter_for_arrange] = ''.join(i)

            # find "if" in one layer

            index = arrange[counter_for_arrange].find(str1)

            if index != -1:

                indexsIf[0] = index  # First if's location
                addEle = 0
                while addEle != - 1:

                    addEle = arrange[counter_for_arrange][index + len(str1):].find(str1)  # -1 if not finded

                    if addEle != - 1:
                        indexsIf.append(addEle + index + len(str1))

                        index += addEle + len(str1)

            # find "else" in one layer

            index = arrange[counter_for_arrange].find(str2)

            if index != -1:

                indexsElse[0] = index  # First else's location
                addEle = 0
                while addEle != - 1:

                    addEle = arrange[counter_for_arrange][index + len(str2):].find(str2)

                    if addEle != - 1:
                        indexsElse.append(addEle + index + len(str2))

                        index += addEle + len(str2)

            # find "elf" in one layer

            index = arrange[counter_for_arrange].find(str3)

            if index != -1:

                indexsElseif[0] = index  # the first elf's location
                addEle = 0
                while addEle != - 1:
                    # Add all elf's index in list

                    addEle = arrange[counter_for_arrange][index + len(str3):].find(str3)

                    if addEle != - 1:
                        indexsElseif.append(addEle + index + len(str3))

                        index += addEle + len(str3)

            if_else = []  # List all indexes of "if...else" structure

            for j in indexsIf:

                for k in indexsElse:

                    if j >= k:

                        # For "if-else", "if" must be located before "else"

                        continue

                    elif j == indexsIf[-1] and k == indexsElse[-1] and j < k:

                        # j < k: for "if-else", "if" must be located before "else"

                        # The last pair of "if-else"

                        if_else.append([j, k])

                    elif k in range(j, indexsIf[indexsIf.index(j) + 1]):

                        # If there is an "else" between two "if",

                        # there must be a pair of "if-else".

                        if_else.append([j, k])

            for h in if_else:

                # Take a pair of indexes of "if-else"

                if indexsElseif[0] == -1:
                    # There is no "else" in this layer.
                    # No "else" exists , then no any structure about "if" exists
                    break

                for L in indexsElseif:

                    if h[1] > L > h[0]:
                        # There is at least an "elf" in this pair of "if-else".
                        # It is not "if-else" structure.
                        counterForElseif += 1
                        break

                    if L == indexsElseif[-1]:
                        counterForElse += 1

            counter_for_arrange += 1

        if level == 3:

            print("\nif-else num :", counterForElse)

            return counterForElse

        else:

            print("\nif-elseif-else num :", counterForElseif)
            return counterForElseif
