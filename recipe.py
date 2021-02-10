from ingredient import Ingredient
from rich.markdown import Markdown

class Recipe():
    def __init__(self,trello_card):
        self.name=trello_card["name"]
        self.ingredients=[]
        self.parse_ingredient(trello_card)
        self.description=Markdown(trello_card["desc"])

    def parse_ingredient(self,trello_card):
        for checklist in trello_card["checklists"]:
            if checklist["name"]=="LISTE DE COURSES":
                for item in checklist["checkItems"]:                           
                    self.ingredients.append(Ingredient(item["name"]))

    def __str__(self) -> str:
        return self.name