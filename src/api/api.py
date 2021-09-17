import json
import discord
from web3.auto import w3
from eth_account.messages import encode_defunct
from roles.roles import get_discord_user, assign_roles
from roles.db import add_guild_id, add_user
from utils.utils import send_embed_dm
from config import cfg
from quart import Quart, Response, redirect, request, render_template

app = Quart("")


@app.route('/api/v1/animetas/connect', methods=['POST'])
async def post_connect():
    """
    Uses a signature to recover the signer.

    With the signer's address, it verifies whether the user has an NFT
    from the animetas collection.

    If it does, it will add the user to the configurable role with the
    provided userid and redirect the user to a success page.

    If not, it will return an unsuccessful response
    with a helpful message.

    request body:
      address: str
      message: str
      signature: str
      userId: str
      guildId: str

    response body:
      success: bool
      message: str
    """
    body = await request.json
    address = body["address"].lower()
    add_guild_id(body["guildId"])
    add_user(body["guildId"], body["userId"], address)
    recovered_address = w3.eth.account.recover_message(
        encode_defunct(text=body["message"]),
        signature=body["signature"]).lower()
    if recovered_address != address:
        err_body = {"success": False,
                    "message":
                    "Address, message or signature is incorrect."}
        return Response(json.dumps(err_body),
                        status=400, mimetype="application/json")

    try:
        discord_user = get_discord_user(
            body["guildId"], body["userId"], address)
        guild_name = discord_user.guild.name
    except Exception as e:
        err_body = {"success": False,
                    "message":
                    f"{e}"}
        return Response(json.dumps(err_body),
                        status=500, mimetype="application/json")

    if len(discord_user.proposed_roles) > 0:
        await assign_roles(discord_user.member,
                           list(discord_user.proposed_roles))

        title = "Wallet Connected"
        body = ("Wallet is connected. " "Please check assigned roles in "
                f"**{guild_name}**. "
                "This process might take up to 2 minutes.")
        colour = int(cfg["Settings"]["colour"], 16)
        embed = discord.Embed(title=title, description=body, colour=colour)

        await send_embed_dm(discord_user.member, embed)
    else:
        return {"success": False, "message":
                ("You have not rented an NFT from the Animetas"
                    "or Animonkey collection, or hold $ANMK/$ANMT.")}

    return {"success": True, "message": "Your wallet has been verified."}


@app.route('/connect', methods=['GET'])
async def connect():
    # TODO: handle lack of query parameter
    user_id = request.args.get("userid")
    guild_id = request.args.get("guildid")
    return await render_template('connect.html', user_id=user_id,
                                 guild_id=guild_id)


@app.route('/', methods=['GET'])
def home():
    return redirect("https://animetas.renft.io/")
