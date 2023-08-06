from FireNext.Table.__tag__ import *


class __update__row__:
    def __update__row__(self, Search_Id, Update_Data):
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
                                    Data = ""
                                    for x2 in range(Update_Data.__len__()):
                                        if Update_Data[x2] == devided__tag:
                                            Data = Data + cel__end__tag
                                        else:
                                            Data = Data + Update_Data[x2]
                                    updateDB = updateDB + row__start__tag + Data + row__end__tag
                                    break

                                else:
                                    data = ""
                            elif value[x1] == row__end__tag:
                                if data == Search_Id:
                                    updateData = "true"
                                    Data = ""
                                    for x2 in range(Update_Data.__len__()):
                                        if Update_Data[x2] == devided__tag:
                                            Data = Data + cel__end__tag
                                        else:
                                            Data = Data + Update_Data[x2]
                                    updateDB = updateDB + row__start__tag + Data + row__end__tag
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