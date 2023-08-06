from FireNext.Table.__tag__ import *


class __add__data__:
    def __add__data__(self, Data):
        try:
            table = open(self.__add__(".nt"))
            if len(table.read()) < 4:
                return "'error' column name not found\nbefore add data we need to add column name"
            else:
                value = ""
                for x in range(Data.__len__()):
                    if Data[x] == devided__tag:
                        value = value + cel__end__tag
                    else:
                        value = value + Data[x]
                open(self + ".nt", "a").write(row__start__tag + value + row__end__tag)
                return "true"
        except:
            return "'error' " + '[' + self + ']' + " table not found"

    def __add__(self, param):
        pass