from ingredient import Ingredient
from rich.markdown import Markdown

class Recipe():
    def __init__(self,trello_card,checklist_name):
        self.name=trello_card["name"]
        self.ingredients=[]
        self.parse_ingredient(trello_card,checklist_name)
        self.description=Markdown(trello_card["desc"])

    def parse_ingredient(self,trello_card,checklist_name):
        for checklist in trello_card["checklists"]:
            if checklist["name"]==checklist_name:
                for item in checklist["checkItems"]:                           
                    self.ingredients.append(Ingredient(item["name"]))

    def __str__(self) -> str:
        return self.name