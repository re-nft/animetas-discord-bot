import json
import discord
from discord.utils import get
from web3.auto import w3
from eth_account.messages import encode_defunct
from roles.roles import get_roles_to_assign, assign_roles
from utils.utils import send_embed_dm, get_guild, get_member
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
    recovered_address = w3.eth.account.recover_message(
        encode_defunct(text=body["message"]),
        signature=body["signature"]).lower()
    if recovered_address != address:
        err_body = {"success": False,
                    "message":
                    "Address, message or signature is incorrect."}
        return Response(json.dumps(err_body),
                        status=400, mimetype="application/json")

    roles = []
    try:
        roles = get_roles_to_assign(address)
    except Exception as e:
        err_body = {"success": False,
                    "message":
                    f"{e}"}
        return Response(json.dumps(err_body),
                        status=500, mimetype="application/json")

    if len(roles) > 0:
        guild = get_guild(body["guildId"])
        if guild is None:
            err_body = {"success": False,
                        "message":
                        "Discord Guild ID is incorrect."}
            return Response(json.dumps(err_body),
                            status=400, mimetype="application/json")
        guild_name = guild.name

        member = get_member(body["userId"], guild)
        if member is None:
            err_body = {"success": False,
                        "message":
                        "User ID is incorrect."}
            return Response(json.dumps(err_body),
                            status=400, mimetype="application/json")
        discord_roles = list(
            map(lambda role: get(guild.roles, name=role), roles))
        for i, role in enumerate(discord_roles):
            if role is None:
                err_body = {"success": False,
                            "message":
                            f"Role {roles[i]} does not exist."}
                return Response(json.dumps(err_body),
                                status=500, mimetype="application/json")

        await assign_roles(member, discord_roles)

        title = "Wallet Connected"
        body = ("Wallet is connected. " "Please check assigned roles in "
                f"**{guild_name}**. "
                "This process might take up to 2 minutes.")
        colour = int(cfg["Settings"]["colour"], 16)
        embed = discord.Embed(title=title, description=body, colour=colour)

        await send_embed_dm(member, embed)
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
    return await render_template('connect.html', user_id=user_id, guild_id=guild_id)


@app.route('/', methods=['GET'])
def home():
    return redirect("https://animetas.renft.io/")
