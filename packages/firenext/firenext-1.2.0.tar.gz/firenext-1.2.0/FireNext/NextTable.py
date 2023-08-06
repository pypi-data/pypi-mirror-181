from FireNext import __delete__table__
from FireNext import __create__table__
from FireNext import __read__table__
from FireNext import __convert__table__doc__
from FireNext import __read__col__name__
from FireNext import __search__data__
from FireNext import __add__col__name__
from FireNext import __update__col__data__
from FireNext import __delete__col__name__
from FireNext import __search__row__data__
from FireNext import __delete__row__
from FireNext import __search__col__data__
from FireNext import __delete__col__
from FireNext import __update__row__
from FireNext import __delete__data__
from FireNext import __update__data__
from FireNext import __add__data__


class NextTable:
    def table_to_doc(Table_Name, Column_Name):
        """
        print(NextTable.delete_col("Table_Name", "id"))

        Table_Name.nt   (Table)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Shamim                xyz@xyz.com

        output :

        document
               |---183071007
               |           |---id:183071007
               |           |---name:Mahfuz Salehin Moaz
               |           |---email:xyz@xyz.com
               |---183071008
               |           |---id:183071008
               |           |---name:Mithila Nisa
               |           |---email:xyz@xyz.com
               |---183071009
               |           |---id:183071009
               |           |---name:Shamim
               |           |---email:xyz@xyz.com

        :return true
        """
        return __convert__table__doc__.__convert__table__doc__(Table_Name, Column_Name)

    def delete_col(Table_Name, Column_Name):
        """

        print(NextTable.delete_col("Table_Name", "email"))

        output: (now)
        id                  name
        ----------------------------------------
        183071007           Mahfuz Salehin Moaz
        ----------------------------------------
        183071008           Mithila Nisa
        ----------------------------------------
        183071009           Sharmin

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return true

         Warning : When you delete a column, you los column data.

        """

        return __delete__col__.__delete__col__(Table_Name, Column_Name)

    def update_row(Table_Name, Search_Id, Update_Data):
        """

        print(NextTable.update_row("Table_Name", "Mithila Nisa", "183071008|Mithila Mithi|abc@abc.com"))

        output: (now)
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return true

        """

        raise __update__row__.__update__row__(Table_Name, Search_Id, Update_Data)

    def delete_row(Table_Name, Search_Id):
        """

        print(NextTable.delete_row("Table_Name", "Mithila Nisa"))

        output: (now)
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return true

         Warning : When you delete a row, you los this rows data.

        """
        return __delete__row__.__delete__row__(Table_Name, Search_Id)

    def delete_data(Table_Name, Search_Id, Column_Name):
        """

        print(NextTable.delete_data("Table_Name", "Mithila Nisa", "name"))

        output: (now)
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008                                  xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return true

        """
        return __delete__data__.__delete__data__(Table_Name, Search_Id, Column_Name)

    def update_data(Table_Name, Search_Id, Column_Name, Update_Data):
        """

        print(NextTable.delete_data("Table_Name", "Mithila Nisa", "email", "abc@abc.com"))

        output: (now)
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return true

        """
        return __update__data__.__update__data__(Table_Name, Search_Id, Column_Name, Update_Data)

    def search_col_data(Table_Name, Column_Name):
        """

        print(NextTable.search_col_data("Table_Name", "id"))

        output: [183071007, 183071008, 183071009]


        #################################################################

        Table_Name.nt

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return [183071007, 183071008, 183071009]

        """

        return __search__col__data__.__search__col__data__(Table_Name, Column_Name)

    def search_row_data(Table_Name, Search_Id):
        """

        print(NextTable.search_row_data("Table_Name", "183071007"))

        output:
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com


        #################################################################

        Table_Name.nt

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        :return :
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com

        """
        return __search__row__data__.__search__row__data__(Table_Name, Search_Id)

    def search_data(Table_Name, Search_Id, Column_Name):
        """

        print(NextTable.search_data("Table_Name", "183071008", "name"))

        output: Mithila Nisa


        #################################################################

        Table_Name.nt

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return Mithila Nisa

        """
        return __search__data__.__search__data__(Table_Name, Search_Id, Column_Name)

    def read_table(Table_Name):
        """

        print(NextTable.read_table("Table_Name"))

        output:

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        :return

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        :return table documents
        """

        return __read__table__.__read__table__(Table_Name)

    def add_data(Table_Name, Data):
        """

        print(NextTable.add_data("Table_Name", "183071009|Sharmin|xyz@xyz.com"))

        output: (now)
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Nisa           xyz@xyz.com


        :return true

        """
        return __add__data__.__add__data__(Table_Name, Data)

    def delete_col_name(Table_Name, Column_Name):
        """

        print(NextTable.delete_col_name("Table_Name", "email"))

        output: (now)
        id                  name
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return true

        """
        return __delete__col__name__.__delete__col__name__(Table_Name, Column_Name)

    def update_col_data(Table_Name, Column_Name, Update_Column_Name):
        """

        print(NextTable.update_col_data("Table_Name", "email", "EMAIL"))

        output: (now)
        id                  name                   EMAIL
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt   (previous)

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com


        :return true

        """
        return __update__col__data__.__update__col__data__(Table_Name, Column_Name, Update_Column_Name)

    def read_col_name(Table_Name):
        """

        print(NextTable.read_col_name("Table_Name", "email", "EMAIL"))

        output:
        id     name      email

        #################################################################

        Table_Name.nt

        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        :return id    name     email

        """
        return __read__col__name__.__read__col__name__(Table_Name)

    def add_col_name(Table_Name, Column_Name):
        """

        print(NextTable.add_col_name("Table_Name", "email"))

        output: (now)
        id                  name                   email
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        Table_Name.nt

        id                  name
        -----------------------------------------------------------------
        183071007           Mahfuz Salehin Moaz    xyz@xyz.com
        -----------------------------------------------------------------
        183071008           Mithila Mithi          abc@abc.com
        -----------------------------------------------------------------
        183071009           Sharmin                xyz@xyz.com

        #################################################################

        :return true

        """
        return __add__col__name__.__add__col__name__(Table_Name, Column_Name)

    def delete_table(Table_Name):
        """
        print(delete_table("tableName"))

        Already do you have a (tablename.nt) file then you delete this file any time.

        :return: Successfully! delete


        Warning : When you delete a table you los your table data.
        """

        return __delete__table__.__delete__table__(Table_Name)

    def create_table(Table_Name):
        """
        print(create_table("tableName"))

        When you create a table then you find a (tablename.nt) file .

        :return: true
        """

        return __create__table__.__create__table__(Table_Name)

