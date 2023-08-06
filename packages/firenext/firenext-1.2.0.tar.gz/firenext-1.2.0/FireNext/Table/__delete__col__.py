from FireNext.Table.__tag__ import *


class __delete__col__:
    def __delete__col__(Table_Name, Column_Name):
        try:
            queryPosition = 0
            queryPermit = "false"
            table = open(Table_Name.__add__(".nt")).read()
            value = ""
            updateDB = ""
            for x in range(table.__len__()):
                if queryPermit == "false" and table[x] == col__start__tag or queryPermit == "null" and table[
                    x] == col__start__tag:
                    updateDB = updateDB + table[x]
                if queryPermit == "null" and table[x] != col__end__tag:
                    updateDB = updateDB + table[x]
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
                        updateDB = updateDB + value + cel__end__tag
                        value = ""
                elif table[x] == col__end__tag and queryPermit == "false":
                    if value == Column_Name:
                        queryPosition = queryPosition + 1
                        updateDB = updateDB[:-1]
                        queryPermit = "null"

                        value = ""

                    else:
                        return "'error' [" + Column_Name + "] column name not found"
                if table[x] == col__end__tag and queryPermit == "null":
                    updateDB = updateDB + value + col__end__tag
                    queryPermit = "true"
                elif queryPermit == "true":

                    value = value + table[x]

                    if table[x] == row__end__tag:
                        dataPosition = 0
                        data = ""
                        for x1 in range(value.__len__()):
                            if value[x1] != row__start__tag and value[x1] != cel__end__tag and value[
                                x1] != row__end__tag:
                                data = data + value[x1]
                            if value[x1] == row__start__tag:
                                updateDB = updateDB + value[x1]
                            elif value[x1] == cel__end__tag:
                                dataPosition = dataPosition + 1
                                if dataPosition == queryPosition:
                                    updateDB = updateDB
                                    data = ""
                                else:
                                    updateDB = updateDB + data + cel__end__tag
                                    data = ""
                            if x1 == value.__len__() - 1:
                                dataPosition = dataPosition + 1
                                if dataPosition == queryPosition:
                                    updateDB = updateDB[:-1] + row__end__tag
                                    data = ""
                                else:
                                    updateDB = updateDB + data + row__end__tag
                                    data = ""
                        value = ""

                if x == table.__len__() - 1:
                    table = open(Table_Name + ".nt", "w")
                    table.write(updateDB)
                    return "true"
        except:
            return "'error' " + '[' + Table_Name + ']' + " table not found"

    def __add__(self, param):
        pass