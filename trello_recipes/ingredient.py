class Ingredient():
    def __init__(self,ingredient):
        self.raw=ingredient
        self.quantities=[]
        self.text=""
        self.parse_ingredient()

    def parse_ingredient(self):
        quant=self.raw.split()[0]
        if Ingredient.isdigit(quant):
            self.quantities.append(float(quant))
            self.text=" ".join(self.raw.split()[1:])
        else:
            # quantity with a unit (starting with a digit)
            if Ingredient.isdigit(self.raw[0]):
                self.text=" ".join(self.raw.split()[1:])
                self.quantities.append(quant)
            else:
                self.text=self.raw

    def update_quantity(self,quant):
        if isinstance(quant,list):
            for q in quant:
                self.quantities.append(q)
        else:
            self.quantities.append(quant)
        self.sum_all_numeric_quantity()
    
    def sum_all_numeric_quantity(self):
        str_quant = [x for x in self.quantities if not Ingredient.isdigit(x)]
        self.quantities=[sum([float(x) for x in self.quantities if Ingredient.isdigit(x)])]
        if len(str_quant):
            self.quantities+=str_quant

    def __str__(self) -> str:
        return f"{self.quantities} - {self.text}"
        
    def __repr__(self) -> str:
        return str(self)

    def isdigit(x):
        try:
            float(x)
            return True
        except ValueError:
            return False
