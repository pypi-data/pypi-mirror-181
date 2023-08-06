import json
import logging
import os
from functools import wraps

import boto3
from nacl.signing import VerifyKey

DISCORD_API_BASE = "https://discord.com/api/v10"
logging.getLogger().setLevel(logging.INFO)


def get_secrets():
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager", region_name="us-east-1"
    )
    return json.loads(
        client.get_secret_value(SecretId=os.environ["BOT_SECRETS_ARN"])[
            "SecretString"
        ]
    )


def respond(status_code, body):
    return {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, PUT, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Expose-Headers": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "statusCode": status_code,
        "body": json.dumps(body),
    }


def ping_pong(body):
    if body["type"] == 1:
        return True
    return False


def verify_signature(event):
    raw_body = event["body"]
    auth_sig = event["headers"]["x-signature-ed25519"]
    auth_ts = event["headers"]["x-signature-timestamp"]

    message = auth_ts.encode() + raw_body.encode()
    verify_key = VerifyKey(bytes.fromhex(get_secrets()["discord_public_key"]))
    verify_key.verify(message, bytes.fromhex(auth_sig))


def send_command_to_queue(body):
    boto3.client("sqs", region_name="us-east-1").send_message(
        QueueUrl=os.getenv("LONG_RESPONSE_QUEUE"), MessageBody=json.dumps(body)
    )


def bot_handler(func):
    @wraps(func)
    def wrapper(event, context):
        if event.get("source") == "aws.events":
            logging.info("cron event")
            return

        try:
            logging.info("verifying signature")
            verify_signature(event)
        except Exception as e:
            logging.error(e)
            return respond(401, {"message": "Unauthorized"})

        body = json.loads(event["body"])
        logging.info(body)
        if ping_pong(body):
            logging.info("ping pong")
            return respond(200, {"type": 1})

        try:
            res_data = func(body, send_command_to_queue)
        except Exception as e:
            logging.error(e)
            res_data = {"content": "The bot experienced an error"}

        return respond(
            200,
            {
                "type": 4,
                "data": res_data,
            },
        )

    return wrapper
