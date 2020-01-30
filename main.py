#!/usr/bin/python3
import sys
import json
import os
import logging
import itertools
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pinboard import pinboard
from trello import TrelloClient


def timestamp_to_isodate(timestamp):
    return (
        datetime.fromtimestamp(int(timestamp), timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


CONFIG_FILE_NAME = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "config.json"
)
LOG_FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "log.txt")
AUTH_DATA_KEY = "authentication"


# Enable logging
file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=(1048576 * 5), backupCount=7)
console_handler = logging.StreamHandler()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[file_handler, console_handler],
)
logger = logging.getLogger(__name__)

# Reading configuration and authentication data
with open(CONFIG_FILE_NAME, "r") as conf_file:
    conf_data = json.load(conf_file)
auth_data = conf_data[AUTH_DATA_KEY]

# Logging in to Pinboard
pb = pinboard.Pinboard(conf_data[AUTH_DATA_KEY]["pinboard_api_token"])
logger.info("Logged in to Pinboard")

# Logging in to Trello
trello_client = TrelloClient(
    api_key=conf_data[AUTH_DATA_KEY]["trello_api_key"],
    token=conf_data[AUTH_DATA_KEY]["trello_token"],
)
logger.info("Logged in to Trello")

trello_list = trello_client.get_list(conf_data["trello_list_id"])
trello_board = trello_list.board
trello_labels = {}
for label in trello_board.get_labels():
    label.fetch()
    trello_labels[label.name] = label
logging.debug("Labels: %s", trello_labels)

trello_label_color_generator = itertools.cycle(
    [
        "green",
        "yellow",
        "orange",
        "red",
        "purple",
        "blue",
        "sky",
        "lime",
        "pink",
        "black",
    ]
)


now_timestamp = int(datetime.now().timestamp())
since_timestamp = (
    conf_data["pinboard_last_checked"]
    if "pinboard_last_checked" in conf_data
    else now_timestamp
)

new_pb_items = pb.posts.all(fromdt=timestamp_to_isodate(since_timestamp))
logger.info("Fetched new Pinboard items")

if len(new_pb_items) == 0:
    logger.info("No new items.")
    sys.exit(0)

for pb_item in new_pb_items:
    logger.debug(
        f"""Found item with
            url: {pb_item.url},
            description: {pb_item.description},
            extended: {pb_item.extended},
            tags: {pb_item.tags},
            time: {pb_item.time},
            """
    )

    card = trello_list.add_card(name=pb_item.description, desc=pb_item.extended)
    logger.info(f"Created card '{pb_item.description}')")

    card.attach(url=pb_item.url)
    logger.info(f"Attached link {pb_item.url} to item")

    for tag in pb_item.tags:
        # create new label
        if tag not in trello_labels:
            label_color = next(trello_label_color_generator)
            label = trello_board.add_label(tag, label_color)
            trello_labels[tag] = label
        card.add_label(trello_labels[tag])

conf_data["pinboard_last_checked"] = now_timestamp
with open(CONFIG_FILE_NAME, "w") as conf_file:
    json.dump(conf_data, conf_file, indent=2)
