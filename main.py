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
    console.log("if you have authenttication issue please access this url to authorize the application")
    token_url= trello.get_token_url('My App', expires='30days', write_access=True)
    console.log(token_url)
    console.log("once the token received, please store it in the .secret file")
    
    trello.set_token(SECRETS.TRELLO_AUTH_TOKEN)

    lists = trello.boards.get_list(board_id=SECRETS.BOARD_ID,fields="name,id")

    all_ingredients=[]
    list_to_ignore=[x.strip() for x in SECRETS.BOARD_LIST_NAME_TO_IGNORE.split(",")]
    for list in lists:
        if list["name"] not in list_to_ignore:
            console.log(f"{list['name']}")        
            cards = trello.lists.get_card(list["id"],checklists="all",fields="name,attachments,labels,desc")
            for card in cards:
                recipe=Recipe(card,SECRETS.BOARD_SHOPPING_CHECKLIST)    
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
        gnotes = keep.find(query=SECRETS.KEEP_NOTE_NAME,pinned=True)
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

