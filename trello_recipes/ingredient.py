class Ingredient():
    def __init__(self,ingredient):
        self.raw=ingredient
        self.quantity=0
        self.text=""
        self.parse_ingredient()

    def parse_ingredient(self):
        self.quantity=self.raw.split()[0]
        if self.quantity.isdigit():
            self.text=" ".join(self.raw.split()[1:])
        else:
            self.text=self.raw
            self.quantity=""

    def __str__(self) -> str:
        return str(self.raw)
        
    def __repr__(self) -> str:
        return str(self.raw)