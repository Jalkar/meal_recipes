from pattern.fr import singularize, pluralize

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
            self.text=" ".join([singularize(x) for x in self.raw.split()[1:]])
        else:
            # quantity with a unit (starting with a digit)
            if Ingredient.isdigit(self.raw[0]):
                self.text=" ".join([singularize(x) for x in self.raw.split()[1:]])
                self.quantities.append(quant)
            else:                
                self.text=" ".join([singularize(x) for x in self.raw.split()])

    def update_quantity(self,quant):
        if isinstance(quant,list):
            for q in quant:
                self.quantities.append(q)
        else:
            self.quantities.append(quant)
        self.sum_all_numeric_quantity()
    
    def sum_all_numeric_quantity(self):
        str_quant = [x for x in self.quantities if not Ingredient.isdigit(x)]
        sum_quant=sum([float(x) for x in self.quantities if Ingredient.isdigit(x)])
        self.quantities=[]
        if sum_quant > 0:
            self.quantities=[sum_quant]
        if len(str_quant):
            self.quantities+=str_quant

    def __str__(self) -> str:
        #str_q=""
        #for q in self.quantities:
        list_of_q=[]
        for q in self.quantities:
            if isinstance(q,float) and q.is_integer():
                list_of_q.append(str(int(q)))
            else:
                list_of_q.append(str(q))
        str_q = " + ".join(list_of_q)
        return f"{str_q} {self.text}"
        
    def __repr__(self) -> str:
        return str(self)

    def isdigit(x):
        try:
            float(x)
            return True
        except ValueError:
            return False
