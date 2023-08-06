from FireNext import __self__add__
from FireNext import __self__read__
from FireNext import __self__child__
from FireNext import __self__query__
from FireNext import __self__delete__
from FireNext import __self__check__


class NextDatabase:
    def add(path):
        """
           print(NextDatabase.add_data("USER>001>name:Mahfuz Salehin Moaz|age:26|nationality:Bangladesh"))
           output :
           USER
               |---001
               |     |---name:Mahfuz Salehin Moaz
               |     |---age:26
               |     |---nationality:Bangladesh

           ---------------------------------------------
           USER
               |---001
               |     |---name:Mahfuz Salehin Moaz
               |     |---age:26
               |     |---nationality:Bangladesh
               |---002
               |     |---name:Mithila Nisa
               |     |---age:23
               |     |---nationality:Bangladesh
               |---003
               |     |---name:Sharmin
               |     |---age:22
               |     |---nationality:Bangladesh
           ----------------------------------------------



           print(NextDatabase.add_data("USER>001>name:"))
           output :
           USER
               |---001
               |     |---name:

           ---------------------------------------------
           USER
               |---001
               |     |---name:
               |     |---age:26
               |     |---nationality:Bangladesh
               |---002
               |     |---name:Mithila Nisa
               |     |---age:23
               |     |---nationality:Bangladesh
               |---003
               |     |---name:Sharmin
               |     |---age:22
               |     |---nationality:Bangladesh
           ----------------------------------------------
        """
        check = __self__check__.__self__check__(path, "add")
        if check == "child":
            return "value child not found"
        if check == "parent":
            return "parent not found"
        if check == "syntax":
            return "'error' "+path

        return __self__add__.__self__add__(check)

    def read(path):
        """
           print(NextDatabase.read("USER>001>name:"))
           output : Mahfuz Salehin Moaz


           print(NextDatabase.read("USER"))
           output:
           --------------------------------------------
           USER
               |---001
               |     |---name:Mahfuz Salehin Moaz
               |     |---age:26
               |     |---nationality:Bangladesh
               |---002
               |     |---name:Mithila Nisa
               |     |---age:23
               |     |---nationality:Bangladesh
               |---003
               |     |---name:Sharmin
               |     |---age:22
               |     |---nationality:Bangladesh
           ----------------------------------------------

           print(NextDatabase.read("USER>001"))
           output:
           ---------------------------------
           001
             |---name:Mahfuz Salehin Moaz
             |---age:26
             |---nationality:Bangladesh
           ---------------------------------
        """
        check = __self__check__.__self__check__(path, "child")
        if check == "child":
            return "value child not found"
        if check == "syntax":
            return "'error' " + path
        return __self__read__.__self__read__(check)

    def hasChild(path):
        """
           print(NextDatabase.hasChild("USER>001>name:"))
           output : true

           ---------------------------------------------
           USER
               |---001
               |     |---name:Mahfuz Salehin Moaz
               |     |---age:26
               |     |---nationality:Bangladesh
               |---002
               |     |---name:Mithila Nisa
               |     |---age:23
               |     |---nationality:Bangladesh
               |---003
               |     |---name:Sharmin
               |     |---age:22
               |     |---nationality:Bangladesh
           ----------------------------------------------
        """
        check = __self__check__.__self__check__(path, "child")
        if check == "child":
            return "value child not found"
        if check == "syntax":
            return "'error' " + path
        return __self__child__.__self__child__(check)

    def query(path):
        """
           child = NextDatabase.query("USER>name:")
           output : [001,002,003]

           for x in child:

             if NextDatabase.hasChild("USER>"+x">name:") == "true":
                print(NextDatabase.read_data("USER>"+x">name:"))

           output : Mahfuz Salehin Moaz
                    Mithila Nisa
                    Sharmin
           ---------------------------------------------
           USER
               |---001
               |     |---name:Mahfuz Salehin Moaz
               |     |---age:26
               |     |---nationality:Bangladesh
               |---002
               |     |---name:Mithila Nisa
               |     |---age:23
               |     |---nationality:Bangladesh
               |---003
               |     |---name:Sharmin
               |     |---age:22
               |     |---nationality:Bangladesh
           ----------------------------------------------
        """
        check = __self__check__.__self__check__(path, "query")
        if check == "child":
            return "value child not found"
        if check == "parent":
            return "parent not found"
        if check == "syntax":
            return "'error' " + path
        return __self__query__.__self__query__(path)

    def delete(path):
        """
           print(NextDatabase.read_data("USER>001>name:"))
           output:
           ---------------------------------------------
           USER
               |---001
               |     |---age:26
               |     |---nationality:Bangladesh
               |---002
               |     |---name:Mithila Nisa
               |     |---age:23
               |     |---nationality:Bangladesh
               |---003
               |     |---name:Sharmin
               |     |---age:22
               |     |---nationality:Bangladesh
           ----------------------------------------------


           print(NextDatabase.read_data("USER>001))
           output:
           ---------------------------------------------
           USER
               |---002
               |     |---name:Mithila Nisa
               |     |---age:23
               |     |---nationality:Bangladesh
               |---003
               |     |---name:Sharmin
               |     |---age:22
               |     |---nationality:Bangladesh
           ----------------------------------------------
        """
        check = __self__check__.__self__check__(path, "delete")
        if check == "child":
            return "value child not found"
        if check == "syntax":
            return "'error' " + path
        return __self__delete__.__self__delete__(check)

