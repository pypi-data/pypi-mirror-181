from FireNext.Table.__tag__ import *
from FireNext.Table.__read__col__name__ import __read__col__name__
from FireNext.Table.__search__col__data__ import __search__col__data__
from FireNext.Table.__search__data__ import __search__data__
from FireNext.Table.__parent__update__ import __parent__update__
from FireNext.Doc.__self__add__ import __self__add__


class __convert__table__doc__:

    def __convert__table__doc__(self, child):
        value_child = __read__col__name__.__read__col__name__(self)
        child_id = __search__col__data__.__search__col__data__(self, child)
        child = ""
        for x in child_id:
            for x1 in value_child:
                value = __search__data__.__search__data__(self, x, x1)
                value = x1 + value__child__tag + value
                if child == "":
                    child = value
                else:
                    child = child + devided__tag + value

            if child != "":
                __self__add__.__self__add__(x + ">" + child)
                __parent__update__.__parent__update__(self, x)

            child = ""
        return "true"
