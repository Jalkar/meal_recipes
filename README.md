# meal_recipes
Export meal recipes from Trello to Google Keep

## .env file

```ini
TRELLO_API_KEY = # api_key for the current app
TRELLO_AUTH_TOKEN = # trello authentication token - can be obtain from the api_key ()
KEEP_AUTH_TOKEN = # cf https://gkeepapi.readthedocs.io/en/latest/#faq
KEEP_GOOGLE_ACCOUNT = # your mail account
BOARD_ID = # found in the board url
BOARD_LIST_NAME_TO_IGNORE = # list of "storage list", comma separated value
BOARD_SHOPPING_CHECKLIST = #checklist name with the ingredients
KEEP_NOTE_NAME = # name of the shopping note in keep
```

