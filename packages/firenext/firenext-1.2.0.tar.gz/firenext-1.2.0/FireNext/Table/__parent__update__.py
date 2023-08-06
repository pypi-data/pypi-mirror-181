from FireNext.Table.__tag__ import *


class __parent__update__:
    def __parent__update__(self, child):
        try:
            database = open(self + ".ndb", "r").read()
            value = ""
            updateDB = ""
            child_update = "false"
            for x2 in range(database.__len__()):
                if database[x2] != start__tag and database[x2] != child__end__tag and database[
                    x2] != end__tag:
                    value = value + database[x2]
                if database[x2] == child__end__tag:
                    if child == value:
                        child_update = "true"
                        if updateDB == "":
                            updateDB = value + child__end__tag
                        else:
                            updateDB = updateDB + value + child__end__tag
                    else:
                        if updateDB == "":
                            updateDB = value + child__end__tag
                        else:
                            updateDB = updateDB + value + child__end__tag
                    value = ""
                if x2 == len(database) - 1:
                    if child != value:
                        if child_update == "false":
                            updateDB = updateDB + value + child__end__tag + child
                        else:
                            updateDB = updateDB + value
                    if child == value:
                        if updateDB == "":
                            updateDB = value
                        else:
                            updateDB = updateDB + value

            open(self + ".ndb", "w").write(start__tag + updateDB + end__tag)

        except:
            open(self + ".ndb", "w").write(start__tag + child + end__tag)