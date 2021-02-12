from trello import TrelloApi
from . import secrets
from .import recipe
from . import ingredient
from . import shopping_list
import gkeepapi

import azure.functions as func
import logging

SECRETS=secrets.Secrets()
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        ingredients = get_trello_check_list()
        keep_connection,note = get_checklist_from_keep()
        send_checklist_to_keep(ingredients,note) 
        sync_keep(keep_connection)

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
                for i in r.ingredients:
                    logging.info(f"    |-{i}")    
                all_ingredients += r.ingredients
                
    # print(json.dumps(cards, sort_keys=True, indent=4,ensure_ascii=False))    
    logging.info("Tous les ingrédients à prévoir:")
    logging.info(all_ingredients)
    return all_ingredients
        

def get_checklist_from_keep():
    logging.info("connexion à Google Keep")
    keep = gkeepapi.Keep()
    success = keep.login(SECRETS.KEEP_GOOGLE_ACCOUNT, SECRETS.KEEP_AUTH_TOKEN)
    if success:
        gnotes = keep.find(query=SECRETS.KEEP_NOTE_NAME,pinned=True)
        list_gnotes=list(gnotes)
        # logging.info(gnotes.title)
    if len(list_gnotes)>1:
        logging.exception("Too many notes !")
        raise ValueError(f"Too Many Pinned notes in keep with the name {SECRETS.KEEP_NOTE_NAME}")

    return keep,list_gnotes[0]

def sync_keep(keep):
    logging.info("SYNC to KEEP")
    keep.sync()

def send_checklist_to_keep(check_list,keep_note):
    logging.info("Build the note in KEEP")
    logging.debug("Read existing ingredient")
    for item in keep_note.unchecked:
        if item.text.strip():
            check_list.append(ingredient.Ingredient(item.text))
    
    logging.debug("Aggregate shopping list")
    global_shopping_list=shopping_list.Shopping_List()
    for item in check_list:
        global_shopping_list.add_ingredient(item)

    logging.debug("Clean existing Note")
    for item in keep_note.items:
        item.delete()
    
    logging.debug("Write the note")
    logging.info(global_shopping_list)
    for item in global_shopping_list.list_ingredients.items():
        keep_note.add(str(item),False)