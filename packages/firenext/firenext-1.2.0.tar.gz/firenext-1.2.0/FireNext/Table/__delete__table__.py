class __delete__table__:
    def __delete__table__(self):
        import os
        if os.path.exists(self.__add__(".nt")):
            os.remove(self.__add__(".nt"))
            return "true"
        else:
            return "'error' [" + self + "] table not found"

    def __add__(self, param):
        pass