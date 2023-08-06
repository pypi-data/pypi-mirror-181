from FireNext.Doc.__tag__ import *


class __self__add__:
    def __self__add__(self):
        value = ""
        databaseName = ""
        for x in range(self.__len__()):
            if ">" != self[x]:
                value = value.__add__(self[x])
            if ">".__eq__(self[x]):
                if databaseName.__eq__(""):
                    try:
                        open(value.__add__(".ndb"), "r")
                        databaseName = value
                        value = ""
                    except:
                        open(value.__add__(".ndb"), "x")
                        databaseName = value
                        value = ""
                elif databaseName.__ne__(""):

                    childData = open(databaseName.__add__(".ndb"), "r").read()
                    if childData.__eq__(""):
                        open(databaseName.__add__(".ndb"), "w").write(start__tag + value + end__tag)
                        open(value.__add__(".ndb"), "x")
                        databaseName = value
                    elif childData.__ne__(""):
                        readChild = ""
                        updateNDB = ""
                        for x1 in range(childData.__len__()):
                            if childData[x1].__ne__(end__tag):
                                updateNDB = updateNDB + childData[x1]
                            if childData[x1].__ne__(start__tag) and childData[x1].__ne__(child__end__tag) and childData[
                                x1].__ne__(end__tag):
                                readChild = readChild + childData[x1]
                            if childData[x1].__eq__(child__end__tag):
                                if readChild.__eq__(value):
                                    databaseName = value
                                    break
                                readChild = ""

                            if childData[x1].__eq__(end__tag) and x1.__eq__(len(childData) - 1):
                                if readChild.__eq__(value):
                                    databaseName = value
                                else:
                                    updateNDB = updateNDB + child__end__tag + value + childData[x1]
                                    open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                    open(value.__add__(".ndb"), "x")
                                    databaseName = value

                    value = ""

            if x.__eq__(len(self) - 1):

                childData = open(databaseName.__add__(".ndb"), "r").read()

                if childData.__eq__(""):
                    value1 = ""
                    for x1 in range(value.__len__()):
                        if value[x1] != devided__tag:
                            value1 = value1 + value[x1]
                        if value[x1] == devided__tag:
                            value1 = value1 + child__end__tag
                    open(databaseName.__add__(".ndb"), "w").write(start__tag + value1 + end__tag)
                else:
                    value1 = ""
                    name = ""
                    for x1 in range(value.__len__()):
                        if value[x1] != devided__tag:
                            value1 = value1 + value[x1]
                        if value[x1] == value__child__tag:
                            name = value1
                            value1 = ""
                        if value[x1] == devided__tag:
                            readChild = ""
                            updateNDB = ""
                            childMatch = "false"
                            childData = open(databaseName.__add__(".ndb"), "r").read()
                            for x2 in range(childData.__len__()):
                                if childData[x2].__eq__(start__tag):
                                    updateNDB = childData[x2]
                                if childData[x2].__ne__(start__tag) and childData[x2].__ne__(child__end__tag) and \
                                        childData[x2].__ne__(end__tag):
                                    readChild = readChild + childData[x2]
                                if childData[x2].__eq__(child__end__tag):
                                    if childMatch == "null":
                                        updateNDB = updateNDB + name + value1
                                        childMatch = "true"
                                    if childMatch == "false":
                                        updateNDB = updateNDB + readChild + child__end__tag
                                    readChild = ""
                                if childData[x2].__eq__(value__child__tag):
                                    if readChild == name:
                                        childMatch = "null"
                                if childMatch == "true":
                                    updateNDB = updateNDB + childData[x2]
                                if childData[x2].__eq__(end__tag) and x2.__eq__(len(childData) - 1):
                                    if childMatch == "true":
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                    if childMatch == "null":
                                        updateNDB = updateNDB + name + value1 + end__tag
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                    if childMatch == "false":
                                        updateNDB = childData[:-1] + child__end__tag + name + value1 + end__tag
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                            name = ""
                            value1 = ""
                        if x1.__eq__(len(value) - 1):
                            readChild = ""
                            updateNDB = ""
                            childMatch = "false"
                            childData = open(databaseName.__add__(".ndb"), "r").read()
                            for x2 in range(childData.__len__()):
                                if childData[x2].__eq__(start__tag):
                                    updateNDB = childData[x2]
                                if childData[x2].__ne__(start__tag) and childData[x2].__ne__(child__end__tag) and \
                                        childData[x2].__ne__(
                                            end__tag):
                                    readChild = readChild + childData[x2]
                                if childData[x2].__eq__(child__end__tag):
                                    if childMatch == "null":
                                        updateNDB = updateNDB + name + value1
                                        childMatch = "true"
                                    if childMatch == "false":
                                        updateNDB = updateNDB + readChild + child__end__tag
                                    readChild = ""
                                if childData[x2].__eq__(value__child__tag):
                                    if readChild == name:
                                        childMatch = "null"
                                if childMatch == "true":
                                    updateNDB = updateNDB + childData[x2]
                                if x2.__eq__(len(childData) - 1):
                                    if childMatch == "true":
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)

                                    if childMatch == "null":
                                        updateNDB = updateNDB + name + value1 + end__tag
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                    if childMatch == "false":
                                        updateNDB = childData[:-1] + child__end__tag + name + value1 + end__tag
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)

                    return "true"
        return "true"

    def __len__(self):
        pass

    def __add__(self, other):
        pass
