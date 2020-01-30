# Pinboard-To-Trello
A utility to create cards in a reading board in Trello out of new items saved to Pinboard.

## History

This is based on the [OrBin/Pocket-To-Trello](https://github.com/OrBin/Pocket-To-Trello) project, which I already modified with [mschuett/Pocket-To-Trello](https://github.com/mschuett/Pocket-To-Trello).
Now I "only" replaced the Pocket part with Pinboard. The functions stay the same:
- I use a specific tag `reblog` in Pocket,
- I want Pinboard-To-Trello to copy those items to Trello,
- After an item is copied it is deleted from Pinboard.

Differences to the Pocket version:
- Pinboard does not have an 'archive' function, so items are immediately deleted from your pinboard list after they are copied,
- Pinboard does not have images in bookmarks, so there are no images/thumbnails imported to Trello either.

## Usage

### Installing requirements
```
pip install -r requirements.txt
```

### Get Trello API key
Visit [Trello](https://trello.com/app-key) to get your Trello API key and save it for later use.

### Get Pinboard API token
Visit [Pinboard](https://pinboard.in/settings/password) to get your Pinboard API key and save it for later use.

### Creating a configuration file
A configuration file `config.json` should be placed in the same directory as the code files.

Here is an example of how the initial configuration file should look:
```
{
  "authentication": {
    "pinboard_api_token": "YOUR-PINBOARD-API-TOKEN",
    "trello_api_key": "YOUR-TRELLO-API-KEY",
  },
  "trello_list_id": "YOUR-TRELLO-LIST-ID",
  "pinboard_tag": "reblog"
}
```

### Authorizing with Trello (Should be done only once)
Authorize with Trello:
```
python authorize_trello.py
```

### Run
```
python3 main.py
```

## External packages
* [py-trello](https://github.com/sarumont/py-trello)
* [pinboard.py](https://github.com/lionheart/pinboard.py)
