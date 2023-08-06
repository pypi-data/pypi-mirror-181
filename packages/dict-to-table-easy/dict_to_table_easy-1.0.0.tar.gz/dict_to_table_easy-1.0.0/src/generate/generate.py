class Table:

    def  __init__(self):
        self.result =""
    def view(self, data, columns):
        self.cell_size = max(map(len, columns))+8
        self.data = data
        self.print_base_line()
        self.print_column_name(columns=columns)
        self.print_base_line()
        self.print_table_value()
        self.print_base_line()
        print(self.result)

    def print_base_line(self):
        self.result+="+"+"-"*self.cell_size+"+"+"-"*self.cell_size+"+\n"

    def print_column_name(self, columns=None):
        for column in columns:
            self.result+="|"+" "*4+str(column)+" "*(self.cell_size-(4+len(str(column))))
        self.result+="|\n"

    def print_table_value(self):

        for columns in self.data.items():
            self.print_column_name(columns=columns)