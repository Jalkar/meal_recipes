from trello import TrelloApi
from . import secrets
from .import recipe
from . import ingredient
import gkeepapi

import azure.functions as func
import logging

SECRETS=secrets.Secrets()
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        ingredients = get_trello_check_list()
        send_checklist_to_keep(ingredients) 
        logging.info("success!")       
        return func.HttpResponse(
             f"Succes ! The new ingredients adds are the following : {ingredients}",
             status_code=200
        )
    except Exception as e:        
        logging.exception(e)
        return func.HttpResponse(
             str(e),
             status_code=500
        )


def get_trello_check_list():
    logging.info("connexion à Trello")
    trello = TrelloApi(SECRETS.TRELLO_API_KEY)

    # if token is dead :
    logging.info("if you have authenttication issue please access this url to authorize the application")
    token_url= trello.get_token_url('My App', expires='30days', write_access=True)
    logging.info(token_url)
    logging.info("once the token received, please store it in the .secret file")
    
    trello.set_token(SECRETS.TRELLO_AUTH_TOKEN)

    lists = trello.boards.get_list(board_id=SECRETS.BOARD_ID,fields="name,id")

    all_ingredients=[]

    list_to_ignore=[x.strip() for x in SECRETS.BOARD_LIST_NAME_TO_IGNORE]
    for list in lists:
        if list["name"] not in list_to_ignore:
            logging.info(f"{list['name']}")        
            cards = trello.lists.get_card(list["id"],checklists="all",fields="name,attachments,labels,desc")
            for card in cards:
                r=recipe.Recipe(card,SECRETS.BOARD_SHOPPING_CHECKLIST)    
                logging.info(f"  |-{r}")    
                logging.info(f"    |-{r.ingredients}")    
                all_ingredients += r.ingredients
                
    # print(json.dumps(cards, sort_keys=True, indent=4,ensure_ascii=False))    
    logging.info("Tous les ingrédients à prévoir:")
    logging.info(all_ingredients)
    return all_ingredients
        

def send_checklist_to_keep(check_list):
    logging.info("connexion à Google Keep")
    keep = gkeepapi.Keep()
    success = keep.login(SECRETS.KEEP_GOOGLE_ACCOUNT, SECRETS.KEEP_AUTH_TOKEN)
    if success:
        gnotes = keep.find(query=SECRETS.KEEP_NOTE_NAME,pinned=True)
        for note in gnotes:
            logging.info(f"found {note.title}")
            for item in note.unchecked:
                if item.text.strip():
                    check_list.append(ingredient.Ingredient(item.text))
            logging.info("Liste de courses complète : ")
            logging.info(check_list)
            for item in note.items:
                item.delete()
            for item in check_list:
                note.add(str(item),False)
                
        logging.info("synchronisation de la note vers Google Keep")
        keep.sync()
    else:
        logging.info("[red]ECHEC synchronisation de la note vers Google Keep[/red]")
