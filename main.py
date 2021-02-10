from trello import TrelloApi, checklists
import json
from secrets import Secrets
from recipe import Recipe
from ingredient import Ingredient
import gkeepapi
from rich import print

from rich.console import Console

console = Console()

SECRETS=Secrets()
def main():
    ingredients = get_trello_check_list()
    send_checklist_to_keep(ingredients)


def get_trello_check_list():
    console.log("connexion à Trello")
    trello = TrelloApi(SECRETS.TRELLO_API_KEY)

    # if token is dead :
    # token_url= trello.get_token_url('My App', expires='30days', write_access=True)
    
    trello.set_token(SECRETS.TRELLO_AUTH_TOKEN)

    lists = trello.boards.get_list(board_id="60170c6aeb47ca633e7ab278",fields="name,id")

    all_ingredients=[]
    for list in lists:
        if list["name"] not in ("Base Recettes SUCRÉES","Base Recettes SALÉES"):
            console.log(f"{list['name']}")        
            cards = trello.lists.get_card(list["id"],checklists="all",fields="name,attachments,labels,desc")
            for card in cards:
                recipe=Recipe(card)    
                console.log(f"  |-{recipe}")    
                console.log(f"    |-{recipe.ingredients}")    
                all_ingredients += recipe.ingredients
                
    # print(json.dumps(cards, sort_keys=True, indent=4,ensure_ascii=False))    
    console.log("Tous les ingrédients à prévoir:")
    console.log(all_ingredients)
    return all_ingredients
        

def send_checklist_to_keep(check_list):
    console.log("connexion à Google Keep")
    keep = gkeepapi.Keep()
    success = keep.login(SECRETS.KEEP_GOOGLE_ACCOUNT, SECRETS.KEEP_AUTH_TOKEN)
    if success:
        gnotes = keep.find(query='Courses',pinned=True)
        for note in gnotes:
            console.log(f"found {note.title}")
            for item in note.unchecked:
                if item.text.strip():
                    check_list.append(Ingredient(item.text))
            console.log("Liste de courses complète : ")
            console.log(check_list)
            for item in note.items:
                item.delete()
            for item in check_list:
                note.add(str(item),False)
                
        console.log("synchronisation de la note vers Google Keep")
        keep.sync()
    else:
        console.log("[red]ECHEC synchronisation de la note vers Google Keep[/red]")

console.log("[blue][b]Bonjour, Bienvenue dans l'outils de synchronisation de recette trello/keep[/b][/blue]")
main()

