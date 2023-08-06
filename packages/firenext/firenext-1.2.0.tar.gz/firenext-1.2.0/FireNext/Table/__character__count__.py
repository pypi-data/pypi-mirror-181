class __character__count__:
    def __character__count__(self):
        finalValue = ""

        for x in range(self.__len__()):

            value = self[x]
            if value != "0" and value != "1" and value != "2" and value != "3" and value != "4" and value != "5" and value \
                    != "6" and value != "7" and value != "8" and value != "9":
                count = finalValue.count(value, 0)
                if finalValue == "":
                    count = self.count(value, 0)
                    finalValue = value + " = " + str(count)
                elif count == 0:
                    count = self.count(value, 0)
                    finalValue = finalValue + "\n" + value + " = " + str(count)
            if x == len(self) - 1:
                for x1 in range(10):
                    count = self.count(str(x1), 0)
                    if count >= 1:
                        finalValue = finalValue + "\n" + str(x1) + " = " + str(count)

        return finalValue

    def __len__(self):
        pass