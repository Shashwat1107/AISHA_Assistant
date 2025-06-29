class Parent():
    def __init__(self, ln, srn) -> None:
        self.last_name = ln;
        self.surname = srn
    
    def print_details(self) -> None: print("LN= {0} ::: SRN = {1}".format(self.last_name, self.surname))

class Child(Parent):
    def __init__(self, ln, srn, name) -> None:
        super().__init__(ln, srn)
        self.name = name
    
    def print_details(self) -> None:
        self.parent().print_details()
        print(f"Name={self.name}")

a = Parent("Mangulkar", "M")
b = Child()