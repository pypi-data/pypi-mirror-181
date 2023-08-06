import os
from FireNext.Doc.__tag__ import *
from FireNext.Doc.__self__update__ import __self__update__


class __self__child__delete__:
    def __self__child__delete__(self):
        value = ""
        parent = ""
        databaseName = ""
        for x in range(self.__len__()):
            if self[x] != ">":
                value = value + self[x]
            if self[x] == ">":
                value = value + self[x]
                parent = parent + value
                value = ""

            if x == self.__len__() - 1:
                if parent != "":

                    try:
                        dataBase = open(value + ".ndb", "r").read()
                    except:
                        return "'" + value + "' child not found"
                    if dataBase == start__tag+""+end__tag or dataBase == "":
                        __self__update__.__self__update__(parent[:-1], value)
                        os.remove(value + ".ndb")
                        return "true"
                    else:
                        databaseName = value
                        value = ""
                        childFound = "true"
                        for x1 in range(dataBase.__len__()):
                            if dataBase[x1] != child__end__tag and dataBase[x1] != start__tag and dataBase[
                                x1] != end__tag:
                                value = value + dataBase[x1]
                            if dataBase[x1] == value__child__tag:
                                childFound = "false"
                            elif dataBase[x1] == child__end__tag:
                                if childFound == "true":
                                    __self__child__delete__.__self__child__delete__1(value)
                                    value = ""
                                else:
                                    value = ""
                                    childFound = "true"
                            if x1 == len(dataBase) - 1:
                                if childFound == "true":
                                    __self__child__delete__.__self__child__delete__1(value)
                                os.remove(databaseName + ".ndb")
                else:
                    try:
                        dataBase = open(value + ".ndb", "r").read()
                    except:
                        return "'" + value + "' child not found"
                    if dataBase == start__tag+""+end__tag or dataBase == "":

                        os.remove(value + ".ndb")
                        return "true"
                    else:
                        databaseName = value
                        value = ""
                        childFound = "true"
                        for x1 in range(dataBase.__len__()):
                            if dataBase[x1] != child__end__tag and dataBase[x1] != start__tag and dataBase[
                                x1] != end__tag:
                                value = value + dataBase[x1]
                            if dataBase[x1] == value__child__tag:
                                childFound = "false"
                            elif dataBase[x1] == child__end__tag:
                                if childFound == "true":
                                    __self__child__delete__.__self__child__delete__1(value)
                                    value = ""
                                else:
                                    value = ""
                                    childFound = "true"
                            if x1 == len(dataBase) - 1:
                                if childFound == "true":
                                    __self__child__delete__.__self__child__delete__1(value)
                                os.remove(databaseName + ".ndb")

        if parent != "":
            __self__update__.__self__update__(parent[:-1], databaseName)
        return "true"

    def __self__child__delete__1(self):
        value = ""
        parent = ""
        for x in range(self.__len__()):
            if self[x] != ">":
                value = value + self[x]
            if self[x] == ">":
                parent = value
                value = ""

            if x == self.__len__() - 1:
                try:
                    dataBase = open(value + ".ndb", "r").read()
                except:
                    return "'" + value + "' child not found"
                if dataBase == start__tag+""+end__tag or dataBase == "":
                    os.remove(value + ".ndb")
                    return "true"
                else:
                    databaseName = value
                    value = ""
                    childFound = "true"
                    for x1 in range(dataBase.__len__()):
                        if dataBase[x1] != child__end__tag and dataBase[x1] != start__tag and dataBase[x1] != end__tag:
                            value = value + dataBase[x1]
                        if dataBase[x1] == value__child__tag:
                            childFound = "false"
                        elif dataBase[x1] == child__end__tag:
                            if childFound == "true":
                                __self__child__delete__.__self__child__delete__2(value)
                                value = ""
                            else:
                                value = ""
                                childFound = "true"
                        if x1 == len(dataBase) - 1:
                            if childFound == "true":
                                __self__child__delete__.__self__child__delete__2(value)
                            os.remove(databaseName + ".ndb")
                            return "true"

    def __self__child__delete__2(self):
        value = ""
        parent = ""
        for x in range(self.__len__()):
            if self[x] != ">":
                value = value + self[x]
            if self[x] == ">":
                parent = value
                value = ""

            if x == self.__len__() - 1:
                try:
                    dataBase = open(value + ".ndb", "r").read()
                except:
                    return "'" + value + "' child not found"
                if dataBase == start__tag+""+end__tag or dataBase == "":
                    os.remove(value + ".ndb")
                    return "true"
                else:
                    databaseName = value
                    value = ""
                    childFound = "true"
                    for x1 in range(dataBase.__len__()):
                        if dataBase[x1] != child__end__tag and dataBase[x1] != start__tag and dataBase[x1] != end__tag:
                            value = value + dataBase[x1]
                        if dataBase[x1] == value__child__tag:
                            childFound = "false"
                        elif dataBase[x1] == child__end__tag:
                            if childFound == "true":
                                __self__child__delete__.__self__child__delete__1(value)
                                value = ""
                            else:
                                value = ""
                                childFound = "true"
                        if x1 == len(dataBase) - 1:
                            if childFound == "true":
                                __self__child__delete__.__self__child__delete__1(value)
                            os.remove(databaseName + ".ndb")
                            return "true"

    def __len__(self):
        pass

    def __add__(self, other):
        pass
