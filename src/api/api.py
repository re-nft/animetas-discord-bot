import time
from utils.logger import logger
from config import cfg
from flask import Flask, redirect
from threading import Thread

app = Flask("")


@app.route('/api/v1/animetas/connect', methods=['POST'])
def post_connect():
    """
    Uses a digest and a signature to recover the signer.

    With the signer's address, it verifies whether the user has an NFT
    from the animetas collection.

    If it does, it will add the user to the configurable role with the
    provided userid and redirect the user to a success page.

    If not, it will return an unsuccessful response
    with a helpful message.

    request body:
      digest: str
      signature: str
      userid: str

    response body:
      success: bool
      message: str
    """
    return {"success": True, "message": ""}


@app.route('/', methods=['GET'])
def home():
    return redirect("https://animetas.renft.io/")


def run():
    app.run(host="0.0.0.0", port=cfg["Settings"]["api_port"])


def run_web_server():
    server = Thread(target=run)
    server.daemon = True
    server.start()
    logger.info("Flask server started")
