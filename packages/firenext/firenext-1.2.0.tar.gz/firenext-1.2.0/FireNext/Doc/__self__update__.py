import os

from FireNext.Doc.__tag__ import *


class __self__update__:

    def __self__update__(self, child):
        parentValue = ""
        parent1 = ""
        for x in range(self.__len__()):
            if self[x] != ">":
                parentValue = parentValue + self[x]

            if self[x] == ">":
                parentValue = parentValue + self[x]
                parent1 = parent1 + parentValue
                parentValue = ""
            if x == len(self) - 1:
                dataBase = open(parentValue + ".ndb", "r").read()
                value = ""
                updateNDB = ""
                for x1 in range(dataBase.__len__()):
                    if dataBase[x1] == start__tag:
                        updateNDB = dataBase[x1]
                    if dataBase[x1] != child__end__tag and dataBase[x1] != start__tag and dataBase[x1] != end__tag:
                        value = value + dataBase[x1]
                    if dataBase[x1] == child__end__tag:
                        if value == child:
                            updateNDB = updateNDB
                        else:
                            value = value + dataBase[x1]
                            updateNDB = updateNDB + value
                        value = ""
                    if x1 == len(dataBase) - 1:
                        if value == child:
                            if updateNDB == start__tag:
                                updateNDB = updateNDB + end__tag
                                open(parentValue.__add__(".ndb"), "w").write(updateNDB)
                            else:
                                updateNDB = updateNDB[:-1] + end__tag
                                open(parentValue.__add__(".ndb"), "w").write(updateNDB)

                            if updateNDB == start__tag+""+end__tag:
                                os.remove(parentValue + ".ndb")
                                if parent1 != "":
                                    __self__update__.__self__update__1(parent1[:-1], parentValue)
                        else:
                            updateNDB = updateNDB + value + end__tag
                            open(parentValue.__add__(".ndb"), "w").write(updateNDB)

    def __self__update__1(self, child):
        parentValue = ""
        parent1 = ""
        for x in range(self.__len__()):
            if self[x] != ">":
                parentValue = parentValue + self[x]

            if self[x] == ">":
                parentValue = parentValue + self[x]
                parent1 = parent1 + parentValue
                parentValue = ""
            if x == len(self) - 1:

                dataBase = open(parentValue + ".ndb", "r").read()
                value = ""
                updateNDB = ""
                for x1 in range(dataBase.__len__()):
                    if dataBase[x1] == start__tag:
                        updateNDB = dataBase[x1]
                    if dataBase[x1] != child__end__tag and dataBase[x1] != start__tag and dataBase[x1] != end__tag:
                        value = value + dataBase[x1]
                    if dataBase[x1] == child__end__tag:
                        if value != child:
                            value = value + dataBase[x1]
                            updateNDB = updateNDB + value

                        value = ""
                    if x1 == len(dataBase) - 1:
                        if value == child:
                            if updateNDB == start__tag:
                                updateNDB = updateNDB + end__tag
                                open(parentValue.__add__(".ndb"), "w").write(updateNDB)
                            else:
                                updateNDB = updateNDB[:-1] + end__tag
                                open(parentValue.__add__(".ndb"), "w").write(updateNDB)

                            if updateNDB == start__tag+""+end__tag:
                                os.remove(parentValue + ".ndb")
                                if parent1 != "":
                                    __self__update__.__self__update__(parent1[:-1], parentValue)
                        else:
                            updateNDB = updateNDB + value + end__tag
                            updateNDB = open(parentValue.__add__(".ndb"), "w").write(updateNDB)

    def __len__(self):
        pass

    def __add__(self, other):
        pass
