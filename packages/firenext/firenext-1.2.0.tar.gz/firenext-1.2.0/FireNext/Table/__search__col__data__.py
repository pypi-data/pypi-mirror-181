from FireNext.Table.__tag__ import *


class __search__col__data__:
    def __search__col__data__(self, Column_Name):
        try:
            queryPosition = 0
            Cell_Size = 0
            queryPermit = "false"
            table = open(self.__add__(".nt")).read()
            value = ""
            returnValue = ""
            for x in range(table.__len__()):
                if table[x] != col__start__tag and table[x] != cel__end__tag and table[
                    x] != col__end__tag and queryPermit == "false":
                    value = value + table[x]
                elif table[x] == cel__end__tag and queryPermit == "false":
                    if value == Column_Name:
                        queryPosition = queryPosition + 1
                        queryPermit = "null"
                        value = ""

                    else:
                        queryPosition = queryPosition + 1
                        value = ""
                elif table[x] == col__end__tag and queryPermit == "false":
                    if value == Column_Name:
                        queryPosition = queryPosition + 1
                        queryPermit = "null"
                        value = ""

                    else:
                        return "'error' [" + Column_Name + "] column name not found"
                if table[x] == col__end__tag and queryPermit == "null":
                    queryPermit = "true"
                elif queryPermit == "true":

                    value = value + table[x]

                    if table[x] == row__end__tag:
                        if Cell_Size == 0:
                            dataPosition = 0
                            value2 = ""
                            for x2 in range(table.__len__()):
                                if table[x2] != cel__end__tag and table[x2] != col__start__tag and table[
                                    x2] != col__end__tag \
                                        and table[x2] != row__start__tag and table[x2] != row__end__tag:
                                    value2 = value2 + table[x2]
                                elif table[x2] == cel__end__tag:

                                    dataPosition = dataPosition + 1
                                    if dataPosition == queryPosition:
                                        if value2.__len__() > Cell_Size:
                                            Cell_Size = value2.__len__()

                                    value2 = ""
                                elif table[x2] == col__end__tag or table[x2] == row__end__tag:
                                    dataPosition = dataPosition + 1
                                    if dataPosition == queryPosition:
                                        if value2.__len__() > Cell_Size:
                                            Cell_Size = value2.__len__()

                                    value2 = ""
                                    dataPosition = 0
                        dataPosition = 0
                        data = ""
                        for x1 in range(value.__len__()):
                            if value[x1] != row__start__tag and value[x1] != cel__end__tag and value[
                                x1] != row__end__tag:
                                data = data + value[x1]
                            elif value[x1] == cel__end__tag:
                                dataPosition = dataPosition + 1
                                if dataPosition == queryPosition:
                                    if returnValue == "":
                                        returnValue = [data]
                                    else:
                                        returnValue.append(data)
                                    break
                                else:
                                    data = ""
                            elif value[x1] == row__end__tag:
                                dataPosition = dataPosition + 1
                                if dataPosition == queryPosition:
                                    if returnValue == "":
                                        returnValue = [data]
                                    else:
                                        returnValue.append(data)
                                    break
                                else:
                                    data = ""
                        value = ""
                if x == table.__len__() - 1:
                    return returnValue
        except:
            return "'error' " + '[' + self + ']' + " table not found"

    def __add__(self, param):
        pass