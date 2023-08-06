class __create__table__:
    def __create__table__(self):
        try:
            open(self.__add__(".nt"), "x")
            return "true"
        except:
            return "already" + ' "' + self + '" ' + "table created"

    def __add__(self, param):
        pass