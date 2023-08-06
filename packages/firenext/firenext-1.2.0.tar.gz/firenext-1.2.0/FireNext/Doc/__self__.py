from FireNext.Doc.__tag__ import *


class __self__:
    def __self__read__(self):
        return open(self.__add__(".ndb"), "r").read()

    def __self__(self):
        database = __self__.__self__read__(self)
        childValue = ""
        spaceLength = len(self)
        childName = ""
        returnValue = ""
        for x in range(database.__len__()):
            if database[x] != start__tag and database[x] != child__end__tag and database[x] != end__tag:
                childValue = childValue + database[x]
            if database[x] == value__child__tag:
                childName = childValue
                childValue = ""
            if database[x] == child__end__tag:
                if childName != "":
                    if returnValue == "":
                        returnValue = self + "\n".ljust(spaceLength, " ") + devided__tag + line__tag + childName + childValue
                    else:
                        returnValue = returnValue + "\n".ljust(spaceLength,
                                                               " ") + devided__tag + line__tag + childName + childValue
                    childName = ""
                    childValue = ""
                else:
                    space = "".ljust(spaceLength - 1, " ") + devided__tag + "".ljust(len(childValue) + 2) + devided__tag
                    value = __self__.__self__1(childValue, space)
                    if returnValue == "":
                        returnValue = self + "\n".ljust(spaceLength, " ") + devided__tag + line__tag + value
                    else:
                        returnValue = returnValue + "\n".ljust(spaceLength, " ") + devided__tag + line__tag + value

                    childValue = ""
            if x == len(database) - 1:
                if childName != "":
                    if returnValue == "":
                        returnValue = self + "\n".ljust(spaceLength, " ") + devided__tag + line__tag + childName + childValue
                    else:
                        returnValue = returnValue + "\n".ljust(spaceLength,
                                                               " ") + devided__tag + line__tag + childName + childValue
                else:
                    space = "".ljust(spaceLength - 1, " ") + devided__tag + "".ljust(len(childValue) + 2) + devided__tag
                    value = __self__.__self__1(childValue, space)
                    if returnValue == "":
                        returnValue = self + "\n".ljust(spaceLength, " ") + devided__tag + line__tag + value
                    else:
                        returnValue = returnValue + "\n".ljust(spaceLength, " ") + devided__tag + line__tag + value
        return returnValue

    def __self__1(self, parentSpace):
        database = __self__.__self__read__(self)
        childValue = ""
        spaceLength = parentSpace
        childName = ""
        returnValue = ""
        for x in range(database.__len__()):
            if database[x] != start__tag and database[x] != child__end__tag and database[x] != end__tag:
                childValue = childValue + database[x]
            if database[x] == value__child__tag:
                childName = childValue
                childValue = ""
            if database[x] == child__end__tag:
                if childName != "":
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + childName + childValue
                    elif returnValue != "":
                        returnValue = returnValue + "\n" + spaceLength + line__tag + childName + childValue

                    childName = ""
                    childValue = ""
                else:
                    space = spaceLength + "".ljust(len(childValue) + 2) + devided__tag
                    value = __self__.__self__2(childValue, space)
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + value
                    else:
                        returnValue = returnValue + "\n" + spaceLength + line__tag + value

                    childValue = ""

            if x == len(database) - 1:
                if childName != "":
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + childName + childValue
                    elif returnValue != "":
                        returnValue = returnValue + "\n" + spaceLength + line__tag + childName + childValue

                else:
                    space = spaceLength + "".ljust(len(childValue) + 2) + devided__tag
                    value = __self__.__self__2(childValue, space)
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + value
                    else:
                        returnValue = returnValue + "\n" + spaceLength + line__tag + value

        return returnValue

    def __self__2(self, parentSpace):
        database = __self__.__self__read__(self)
        childValue = ""
        spaceLength = parentSpace
        childName = ""
        returnValue = ""
        for x in range(database.__len__()):
            if database[x] != start__tag and database[x] != child__end__tag and database[x] != end__tag:
                childValue = childValue + database[x]
            if database[x] == value__child__tag:
                childName = childValue
                childValue = ""
            if database[x] == child__end__tag:
                if childName != "":
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + childName + childValue
                    elif returnValue != "":
                        returnValue = returnValue + "\n" + spaceLength + line__tag + childName + childValue

                    childName = ""
                    childValue = ""
                else:
                    space = spaceLength + "".ljust(len(childValue) + 2) + devided__tag
                    value = __self__.__self__1(childValue, space)
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + value
                    else:
                        returnValue = returnValue + "\n" + spaceLength + line__tag + value

                    childValue = ""

            if x == len(database) - 1:
                if childName != "":
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + childName + childValue
                    elif returnValue != "":
                        returnValue = returnValue + "\n" + spaceLength + line__tag + childName + childValue

                else:
                    space = spaceLength + "".ljust(len(childValue) + 2) + devided__tag
                    value = __self__.__self__1(childValue, space)
                    if returnValue == "":
                        returnValue = self + "\n" + spaceLength + line__tag + value
                    else:
                        returnValue = returnValue + "\n" + spaceLength + line__tag + value

        return returnValue

    def __add__(self, param):
        pass

    def __len__(self):
        pass