from FireNext.Doc.__tag__ import *


class __self__check__:
    def __self__check__(self, condition):

        parent = ""
        valueChild = ""
        value = ""
        if condition == "add":
            for x in range(len(self)):

                if x >= 0:

                    if value == "" and self[x] == ' ':

                        value = ""

                    else:

                        value = value + self[x]

                if self[x] == '>':

                    if valueChild == "":

                        parent = parent + value
                        value = ""
                    else:
                        return "syntax"

                if self[x] == value__child__tag:

                    if len(value) != 1:
                        valueChild += value
                        value = ""
                    else:

                        return "child"

                if x == len(self) - 1:

                    if valueChild != "" and parent == "":
                        return "parent"
                    elif parent == "":

                        return "parent"

                    elif valueChild == "":

                        return "child"

                    else:

                        return parent + valueChild + value

        if condition == "child":

            for x in range(len(self)):

                if x >= 0:

                    if value == "" and self[x] == ' ':

                        value = ""

                    else:

                        value = value + self[x]

                if self[x] == '>':

                    if valueChild == "":

                        parent = parent + value
                        value = ""
                    else:
                        return "syntax"

                if self[x] == value__child__tag:

                    if len(value) != 1:
                        valueChild += value
                        value = ""
                    else:
                        return "child"
                if x == len(self) - 1:
                    return parent + valueChild + value

        if condition == "delete":

            for x in range(len(self)):

                if x >= 0:

                    if value == "" and self[x] == ' ':
                        value = ""
                    else:
                        value = value + self[x]

                if self[x] == '>':

                    if valueChild == "":

                        parent = parent + value
                        value = ""
                    else:
                        return "syntax"

                if self[x] == value__child__tag:

                    if len(value) != 1:
                        valueChild += value
                        value = ""
                    else:
                        return "child"
                if x == len(self) - 1:

                    if valueChild != "" and value != "":
                        return "syntax"
                    else:
                        return parent + valueChild + value

        if condition == "query":

            for x in range(len(self)):

                if x >= 0:

                    if value == "" and self[x] == ' ':
                        value = ""
                    else:
                        value = value + self[x]

                if self[x] == '>':

                    if valueChild == "":

                        parent = parent + value
                        value = ""
                    else:
                        return "syntax"

                if self[x] == value__child__tag:

                    if len(value) != 1:
                        valueChild += value
                        value = ""
                    else:
                        return "child"
                if x == len(self) - 1:

                    if parent == "":
                        return "parent"
                    else:
                        return parent + valueChild + value

        return parent + valueChild + value
