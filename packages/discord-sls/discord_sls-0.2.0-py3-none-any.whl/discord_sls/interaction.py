import logging

import requests

DISCORD_API_BASE = "https://discord.com/api/v10"


class Interaction:
    def __init__(self, command_body):
        self.command_body = command_body

    def edit_interaction(self, updated_content):
        discord_res = requests.patch(
            f"{DISCORD_API_BASE}/webhooks/{self.command_body['application_id']}/{self.command_body['token']}/messages/@original",
            json=updated_content,
        )
        if discord_res.status_code != 200:
            logging.error(discord_res.status_code)
            logging.error(discord_res.text)
        else:
            logging.info(f"successfully handled: {self.command_body['id']}")
