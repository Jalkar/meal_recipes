try:
    from . import ingredient
except:
    from trello_recipes import ingredient

class Shopping_List():
    def __init__(self) -> None:
        self.list_ingredients=dict()
    
    def add_ingredient(self,ing:ingredient.Ingredient) -> None:
        if ing.text.lower() in self.list_ingredients.keys():
            self.list_ingredients[ing.text.lower()].update_quantity(ing.quantities)
        else:
            self.list_ingredients[ing.text.lower()]=ing
    
    def __str__(self) -> str:
        str_string=""
        for key,ing in self.list_ingredients.items():
            str_string+=f"{key} - {str(ing.quantities)}\n"
        return str_string


    def __repr__(self) -> str:
        return str(self)


# testShoppingList=Shopping_List()
# testShoppingList.add_ingredient(ingredient.Ingredient("1 Oignon"))
# testShoppingList.add_ingredient(ingredient.Ingredient("1 Oignon"))
# testShoppingList.add_ingredient(ingredient.Ingredient("0.5 Oignon"))
# testShoppingList.add_ingredient(ingredient.Ingredient("1.4g Oignon"))
# testShoppingList.add_ingredient(ingredient.Ingredient("0.5d Oignon"))

# print(testShoppingList)
# print(testShoppingList.list_ingredients.values())


