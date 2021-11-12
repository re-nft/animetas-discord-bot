# reNFT Discord Bot

## Adding/Updating Packages

If you are contributing, and would like to add a new library to the Python code, please make sure you add it to `requirements.in`. You will then need to update `requirements.txt`, following the below steps.

1. Ensure the `pip-tools` package is installed on your system. If not, install it with `pip install pip-tools`.
2. Update the `requirements.in` with the names of the new packages you want to add. (optional)
3. Run `pip-compile requirements.in > requirements.txt`, or run `pip-compile requirements.in` and copy the output to replace the contents of `requirements.txt`.

## .env file

In `src/.env` put this:

```env
PUBLIC_API_BASE_URL=<base-url>
PUBLIC_API_PORT=<port>
LOCAL_API_PORT=<port>
TOKEN=<discord-bot-token>
INFURA_PROJECT_ID=<infura-project-id>
GRAFANA_USER=<grafana-user>
GRAFANA_PASS=<grafana-password>
DISCORD_BOT_ENABLED=<true or false>
WEB_SERVER_ENABLED=<true or false>
```

If using HTTPS, also add these:

```env
CERT_FILE=<path-to-cert.pem>
KEY_FILE=<path-to-key.pem>
```

To support NFT addresses, edit `guild_nfts_config.json`.

It is in the below format:

```json
[
        {
                "name": "<name>",
                "guild_id": "<guild_id>",
                "addresses": ["<address0>", "<address1>"]
        }
]
```
