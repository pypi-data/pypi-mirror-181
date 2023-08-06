from FireNext.Table.__tag__ import *


class __delete__row__:
    def __delete__row__(self, Search_Id):
        try:

            queryPermit = "false"
            updateData = "false"
            table = open(self.__add__(".nt")).read()
            value = ""
            updateDB = ""
            for x in range(table.__len__()):
                if queryPermit == "false" or queryPermit == "null":
                    updateDB = updateDB + table[x]
                if table[x] == col__end__tag and queryPermit == "false":
                    queryPermit = "true"

                elif queryPermit == "true":

                    value = value + table[x]

                    if table[x] == row__end__tag:
                        data = ""
                        for x1 in range(value.__len__()):
                            if value[x1] != row__start__tag and value[x1] != cel__end__tag and value[
                                x1] != row__end__tag:
                                data = data + value[x1]

                            elif value[x1] == cel__end__tag:
                                if data == Search_Id:
                                    updateData = "true"
                                    break

                                else:
                                    data = ""
                            elif value[x1] == row__end__tag:
                                if data == Search_Id:
                                    updateData = "true"
                                    break
                            if x1 == value.__len__() - 1:
                                updateDB = updateDB + value
                        value = ""
                if x == table.__len__() - 1 and updateData == "false":
                    return "'error' [Search Id : " + Search_Id + "] not found"
                elif x == table.__len__() - 1:
                    table = open(self + ".nt", "w")
                    table.write(updateDB)
                    return "true"
        except:
            return "'error' " + '[' + self + ']' + " table not found"

    def __add__(self, param):
        pass