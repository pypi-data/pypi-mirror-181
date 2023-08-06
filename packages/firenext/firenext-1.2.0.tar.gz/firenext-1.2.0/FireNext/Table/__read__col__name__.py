from FireNext.Table.__tag__ import *


class __read__col__name__:
    def __read__col__name__(self):
        try:
            table = open(self.__add__(".nt"), "r").read()
            value = ""
            value2 = ""

            for x1 in range(table.__len__()):
                if table[x1] != cel__end__tag and table[x1] != col__start__tag and table[x1] != col__end__tag:
                    value = value + table[x1]

                elif table[x1] == cel__end__tag:
                    if value2 == "":
                        value2 = [value]
                    else:
                        value2.append(value)
                    value = ""
                elif table[x1] == col__end__tag:
                    if value2 == "":
                        value2 = [value]
                    else:
                        value2.append(value)
                    return value2
        except:
            return "'error' " + '[' + self + ']' + " table not found"

    def __add__(self, param):
        pass