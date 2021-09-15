# animetas-discord-bot

## Adding/Updating Packages

If you are contributing, and would like to add a new library to the Python code, please make sure you add it to `requirements.in`. You will then need to update `requirements.txt`, following the below steps.

1. Ensure the `pip-tools` package is installed on your system. If not, install it with `pip install pip-tools`.
2. Update the `requirements.in` with the names of the new packages you want to add. (optional)
3. Run `pip-compile requirements.in > requirements.txt`, or run `pip-compile requirements.in` and copy the output to replace the contents of `requirements.txt`.


## .env file

In `src/.env` put this:

```
TOKEN=<discord-bot-token>
INFURA_PROJECT_ID=<infura-project-id>
``
