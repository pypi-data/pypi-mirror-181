from FireNext.Doc.__tag__ import *
from FireNext.Doc.__self__child__delete__ import __self__child__delete__


class __self__delete__:
    def __self__delete__(self):
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

                if databaseName == "":
                    try:
                        open(value.__add__(".ndb"))
                        return __self__child__delete__.__self__child__delete__(value)
                    except:
                        return "'" + value + "' child not found"
                if value == "":
                    return "'" + databaseName + "' parent" + " child not found"

                childData = open(databaseName.__add__(".ndb"), "r").read()

                if childData.__eq__(""):
                    return "'" + value + "' child not found"
                elif childData.__ne__(""):
                    value1 = ""
                    name = ""
                    notFoundChild = ""
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
                                        childData[x2].__ne__(
                                                end__tag):
                                    readChild = readChild + childData[x2]
                                if childData[x2].__eq__(child__end__tag):
                                    if childMatch == "null" and updateNDB == start__tag:
                                        updateNDB = updateNDB
                                        childMatch = "true"
                                        continue
                                    if childMatch == "null" and updateNDB != start__tag:
                                        updateNDB = updateNDB
                                        childMatch = "true"
                                    elif childMatch == "false" and updateNDB == start__tag:
                                        updateNDB = updateNDB + readChild
                                    elif childMatch == "false" and updateNDB != "":
                                        updateNDB = updateNDB + child__end__tag + readChild
                                    readChild = ""
                                if childData[x2].__eq__(value__child__tag) and childMatch == "false":
                                    if readChild == name:
                                        childMatch = "null"
                                elif childMatch == "true":
                                    updateNDB = updateNDB + childData[x2]
                                if childData[x2].__eq__(end__tag) and x2.__eq__(len(childData) - 1):
                                    if childMatch == "true":
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                    if childMatch == "null":
                                        updateNDB = updateNDB + end__tag
                                        open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                    if childMatch == "false":
                                        notFoundChild = notFoundChild + "'" + name + "'"

                            name = ""
                            value1 = ""
                        if x1.__eq__(len(value) - 1):

                            if name == "":
                                try:
                                    open(value.__add__(".ndb"))
                                    parentDatabaseName = databaseName + ">" + value
                                    return __self__child__delete__.__self__child__delete__(parentDatabaseName)
                                except:
                                    return "'" + value + "' child not found"

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
                                    if childMatch == "null" and updateNDB == start__tag:
                                        updateNDB = updateNDB
                                        childMatch = "true"
                                        continue
                                    if childMatch == "null" and updateNDB != start__tag:
                                        updateNDB = updateNDB
                                        childMatch = "true"
                                    elif childMatch == "false" and updateNDB == start__tag:
                                        updateNDB = updateNDB + readChild
                                    elif childMatch == "false" and updateNDB != start__tag:
                                        updateNDB = updateNDB + child__end__tag + readChild
                                    readChild = ""
                                if childData[x2].__eq__(value__child__tag) and childMatch == "false":
                                    if readChild == name:
                                        childMatch = "null"
                                elif childMatch == "true":
                                    updateNDB = updateNDB + childData[x2]

                                if x2.__eq__(len(childData) - 1):

                                    if childMatch == "true":
                                        if updateNDB == start__tag+""+end__tag:
                                            open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                            if parentDatabaseName == "":
                                                parentDatabaseName = databaseName
                                            else:
                                                parentDatabaseName = parentDatabaseName + ">" + databaseName
                                            __self__child__delete__.__self__child__delete__(parentDatabaseName)
                                            return "true"
                                        else:
                                            open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                            return "true"

                                    if childMatch == "null":
                                        updateNDB = updateNDB + end__tag

                                        if updateNDB == start__tag+""+end__tag:
                                            open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                            if parentDatabaseName == "":
                                                parentDatabaseName = databaseName
                                            else:
                                                parentDatabaseName = parentDatabaseName + ">" + databaseName
                                            __self__child__delete__.__self__child__delete__(parentDatabaseName)
                                            return "true"
                                        else:
                                            open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                            return "true"

                                    if childMatch == "false":
                                        notFoundChild = notFoundChild + "'" + name + "'"

                                        updateNDB = childData[:-1] + value1 + end__tag
                                        if updateNDB == start__tag+""+end__tag:
                                            open(databaseName.__add__(".ndb"), "w").write(updateNDB)
                                            if parentDatabaseName == "":
                                                parentDatabaseName = databaseName
                                            else:
                                                parentDatabaseName = parentDatabaseName + ">" + databaseName
                                                __self__child__delete__.__self__child__delete__(parentDatabaseName)

                                        else:
                                            open(databaseName.__add__(".ndb"), "w").write(updateNDB)

                                        if notFoundChild != "":
                                            return notFoundChild + " child not found"
                    value = ""

    def __len__(self):
        pass

    def __add__(self, other):
        pass
