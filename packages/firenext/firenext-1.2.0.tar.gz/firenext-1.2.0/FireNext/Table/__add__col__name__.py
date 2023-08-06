from FireNext.Table.__tag__ import *


class __add__col__name__:
    def __add__col__name__(self, Column_Name):
        try:
            table = open(self.__add__(".nt"), "r").read()

            if table.__len__() == 0:
                value = ""
                for x in range(Column_Name.__len__()):
                    if Column_Name[x] == devided__tag:
                        value = value + cel__end__tag
                    else:
                        value = value + Column_Name[x]
                table = open(self.__add__(".nt"), "w")
                table.write(col__start__tag + value + col__end__tag)
                return "true"
            elif table.__len__() > 0:
                queryPermit = "false"
                duplicateCondition = "false"
                duplicateColumnName = ""
                value = ""
                updateDB = ""
                for x in range(table.__len__()):

                    if table[x] != col__end__tag and queryPermit == "false":
                        updateDB = updateDB + table[x]
                    if table[x] != col__start__tag and table[x] != cel__end__tag and table[
                        x] != col__end__tag and queryPermit == "false":
                        value = value + table[x]
                    elif table[x] == cel__end__tag and queryPermit == "false":
                        value1 = ""
                        for x1 in range(Column_Name.__len__()):
                            if Column_Name[x1] != devided__tag:
                                value1 = value1 + Column_Name[x1]
                            elif Column_Name[x1] == devided__tag:
                                if value == value1:
                                    duplicateCondition = "true"
                                    if duplicateColumnName == "":
                                        duplicateColumnName = value1
                                    else:
                                        duplicateColumnName = duplicateColumnName + cel__end__tag + value1
                                    break
                                else:
                                    value1 = ""
                            if x1 == len(Column_Name) - 1:
                                if value == value1:
                                    duplicateCondition = "true"
                                    if duplicateColumnName == "":
                                        duplicateColumnName = value1
                                    else:
                                        duplicateColumnName = duplicateColumnName + cel__end__tag + value1
                                    break
                                else:
                                    value1 = ""
                        value = ""

                    elif table[x] == col__end__tag and queryPermit == "false":
                        value1 = ""
                        for x1 in range(Column_Name.__len__()):
                            if Column_Name[x1] != devided__tag:
                                value1 = value1 + Column_Name[x1]
                            elif Column_Name[x1] == devided__tag:
                                if value == value1:
                                    duplicateCondition = "true"
                                    if duplicateColumnName == "":
                                        duplicateColumnName = value1
                                    else:
                                        duplicateColumnName = duplicateColumnName + cel__end__tag + value1
                                    break
                                else:
                                    value1 = ""
                            if x1 == len(Column_Name) - 1:
                                if value == value1:
                                    duplicateCondition = "true"
                                    if duplicateColumnName == "":
                                        duplicateColumnName = value1
                                    else:
                                        duplicateColumnName = duplicateColumnName + cel__end__tag + value1
                                    break
                                else:
                                    value1 = ""

                    if table[x] == col__end__tag and queryPermit == "false":
                        updateDB = updateDB + cel__end__tag + Column_Name + col__end__tag
                        queryPermit = "true"
                    elif queryPermit == "true":
                        updateDB = updateDB + table[x]
                    if x == len(table) - 1:
                        if duplicateCondition == "true":
                            return "'error' " + "[" + duplicateColumnName + "]" + " duplicate column name"
                        else:
                            table = open(self.__add__(".nt"), "w")
                            table.write(updateDB)
                            return "true"

        except:
            return "'error' " + '[' + self + ']' + " table not found"

    def __add__(self, param):
        pass
