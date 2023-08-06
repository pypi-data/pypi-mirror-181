from FireNext.Doc.__tag__ import *


class __self__child__:
    def __self__child__(self):
        value = ""
        databaseName = ""
        parentDatabaseName = ""
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
                        return "'" + value + "' database not found"
                elif databaseName.__ne__(""):

                    childData = open(databaseName.__add__(".ndb"), "r").read()
                    if childData.__eq__(""):
                        return "'" + value + "' child not found"
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
                                    try:
                                        open(value.__add__(".ndb"), "r")
                                        if parentDatabaseName == "":
                                            parentDatabaseName = databaseName
                                        else:
                                            parentDatabaseName = parentDatabaseName + ">" + databaseName
                                        databaseName = value
                                        value = ""
                                        break
                                    except:
                                        return "'" + value + "' database not found"
                                readChild = ""

                            if childData[x1].__eq__(end__tag) and x1.__eq__(len(childData) - 1):
                                if readChild.__eq__(value):
                                    try:
                                        open(value.__add__(".ndb"), "r")
                                        if parentDatabaseName == "":
                                            parentDatabaseName = databaseName
                                        else:
                                            parentDatabaseName = parentDatabaseName + ">" + databaseName
                                        databaseName = value
                                        value = ""
                                    except:
                                        return "'" + value + "' database not found"
                                else:
                                    return "'" + value + "' child not found"

                    value = ""

            if x.__eq__(len(self) - 1):
                try:
                    childData = open(databaseName.__add__(".ndb"), "r").read()
                except:
                    return print("'" + databaseName + "' child not found")

                if childData.__eq__(""):
                    return "false"
                elif childData.__ne__(""):
                    readChild = ""
                    updateNDB = ""
                    childMatch = "false"
                    childData = open(databaseName.__add__(".ndb"), "r").read()
                    for x2 in range(childData.__len__()):
                        if childData[x2].__ne__(start__tag) and childData[x2].__ne__(child__end__tag) and childData[
                            x2].__ne__(end__tag):
                            readChild = readChild + childData[x2]
                        if childData[x2].__eq__(child__end__tag):
                            if readChild == value:
                                return "true"
                            readChild = ""
                        if childData[x2].__eq__(value__child__tag):
                            if readChild == value:
                                return "true"
                        if x2.__eq__(len(childData) - 1):
                            if readChild == value:
                                return "true"
                            else:
                                return "false"

    def __len__(self):
        pass

    def __add__(self, other):
        pass
