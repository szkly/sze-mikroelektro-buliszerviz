import logging

from api import database, notifications
from driver import Driver
from flask import Flask, g, jsonify, render_template, request
from utils import constants

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s')


app = Flask(__name__)

# loading config (variables with FLASK prefix) from a .env file
app.config.from_prefixed_env()

bot = notifications.TelegramBot(
    token=app.config["TELEGRAM_BOT_TOKEN"], chat_id=app.config["TELEGRAM_CHAT_ID"])

driver = Driver(url=app.config["TELEGRAM_WEBHOOK_URL"],
                song_file_path=app.config["SONG_FILE_PATH"])


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = database.Database(
            app.config["DB_FILE_PATH"], "db/schema.sql")

    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/send-name", methods=["POST"])
def send_name():
    payload = request.get_json()

    try:
        name_to_send = payload["name"]

        if has_been_processed(name_to_send):
            logging.info(
                f"Name {name_to_send} has already beeen processed, ignoring it!")
            return jsonify({"status": constants.ResponseStatus.ERROR, "message": f"Name {name_to_send} has already been processed"}), 400

        logging.info(f"Sending name {name_to_send} to Telegram group...")

        message = f"{name_to_send} be szeretne jönni!"
        bot.send_message(message, send_with_keyboard=True)

        return jsonify({"status": constants.ResponseStatus.SUCCESS, "message": f"Successfully sent name {name_to_send}"}), 200
    except:
        logging.error(constants.LogMessage.SEND_NAME_ERROR)

        return jsonify({"status": constants.ResponseStatus.ERROR, "message": constants.ResponseMessage.SEND_NAME_ERROR}), 503


def has_been_processed(name):
    events = get_db().get_events(json=False)

    names_already_processed = [event["name"] for event in events]

    return name in names_already_processed


@app.route("/stats")
def stats():
    return render_template("stats.html")


@app.route("/api/stats")
def get_statistics():
    events = get_db().get_events()

    approvals = list(filter(lambda e: e["is_approved"] == 1, events))
    denials = list(filter(lambda e: e["is_approved"] == 0, events))

    datasets = {
        "approvals": generate_dataset(approvals, events),
        "denials": generate_dataset(denials, events),
    }

    labels = [event["timestamp"] for event in events]
    names = [event["name"] for event in events]

    return jsonify({"status": constants.ResponseStatus.SUCCESS, "datasets": datasets, "labels": labels, "names": names}), 200


def generate_dataset(dataset, events):
    """
    Generating a list with the length corresponding 
    to the number of events in the dataset
    """

    normalized_values = []
    number_of_events = 0

    i = 0
    dataset_idx = 0

    while dataset_idx < len(dataset) and i < len(events):
        if dataset[dataset_idx]["event_id"] == events[i]["event_id"]:
            number_of_events += 1
            dataset_idx += 1

        normalized_values.append(number_of_events)

        i += 1

    return normalized_values


@app.route("/events")
def get_events():
    events = get_db().get_events()

    return jsonify({"status": constants.ResponseStatus.SUCCESS, "events": events}), 200


@app.route(f"/{app.config['TELEGRAM_BOT_TOKEN']}", methods=["POST"])
def respond():
    response_message, response_status_code = None, None

    try:
        # retrieve the message in JSON and then transform it to Telegram object
        message_id, message_content, name = bot.process_update(
            request.get_json(force=True))

        response_message, response_status_code = process_command(
            command=message_content, message_id=message_id, name=name)
    except Exception as e:
        logging.error(e)
        logging.error(constants.LogMessage.RESPOND_ERROR.value)

        return jsonify({"status": constants.ResponseStatus.ERROR, "message": constants.ResponseMessage.RESPOND_ERROR}), 503

    return jsonify({"status": constants.ResponseStatus.SUCCESS, "message": response_message}), response_status_code


def process_command(command, message_id, name):
    should_open = command == constants.Command.APPROVE

    # Has to use <enum>.value when logging strings contained in an enum
    log_message = constants.LogMessage.RESPOND_ON_APPROVE.value if should_open else constants.LogMessage.RESPOND_ON_DENY.value
    logging.info(log_message)

    reply = constants.CommandBotReply.ON_APPROVE if should_open else constants.CommandBotReply.ON_DENY
    bot.send_message(message=reply, reply_to_message_id=message_id)

    db = get_db()
    message, status_code = None, 200
    if should_open:
        driver.on_approval()
        db.add_event(name=name, is_approved=True)
        message = constants.ResponseMessage.RESPOND_ON_APPROVE
    else:
        driver.on_denial()
        db.add_event(name=name, is_approved=False)
        message = constants.ResponseMessage.RESPOND_ON_DENY

    # Returning to an idle state
    driver.idle()

    return message, status_code


@app.route("/set-webhook", methods=["GET", "POST"])
def set_webhook():
    is_webhook_set = bot.set_webhook(app.config["TELEGRAM_WEBHOOK_URL"])

    if is_webhook_set:
        logging.info(constants.LogMessage.WEBHOOK_SET.value)
        return jsonify({"status": constants.ResponseStatus.SUCCESS, "message": constants.ResponseMessage.WEBHOOK_SET}), 200
    else:
        logging.error(constants.LogMessage.WEBHOOK_ERROR.value)
        return jsonify({"status": constants.ResponseStatus.ERROR, "message": constants.ResponseMessage.WEBHOOK_ERROR}), 503
