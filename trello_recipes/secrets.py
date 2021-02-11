from dotenv import load_dotenv
import os


class Secrets():
    def __init__(self) -> None:   
        load_dotenv()             
        self.TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
        self.TRELLO_AUTH_TOKEN = os.getenv("TRELLO_AUTH_TOKEN")
        self.KEEP_AUTH_TOKEN = os.getenv("KEEP_AUTH_TOKEN")
        self.KEEP_GOOGLE_ACCOUNT = os.getenv("KEEP_GOOGLE_ACCOUNT")
        self.BOARD_ID = os.getenv("BOARD_ID")
        self.BOARD_LIST_NAME_TO_IGNORE = os.getenv("BOARD_LIST_NAME_TO_IGNORE").split(",")
        self.BOARD_SHOPPING_CHECKLIST = os.getenv("BOARD_SHOPPING_CHECKLIST")
        self.KEEP_NOTE_NAME = os.getenv("KEEP_NOTE_NAME")