# Pinboard-To-Trello
A utility to create cards in a reading board in Trello out of new items saved to Pinboard.

## History

This is based on the [OrBin/Pocket-To-Trello](https://github.com/OrBin/Pocket-To-Trello) project, which I already modified with [mschuett/Pocket-To-Trello](https://github.com/mschuett/Pocket-To-Trello).

This `master` branch tries to replicate the original timestamp-based sync of the original. I do not use this myself, so this is less tested than the `reblog` branch.

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
  "pinboard_last_checked": 0
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
