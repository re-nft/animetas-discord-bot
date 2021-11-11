import dotenv
import os
import requests
from web3 import Web3
from utils.utils import get_all_nft_addresses

dotenv.load_dotenv()
project_id = os.environ.get("INFURA_PROJECT_ID", "")


def verify_wallet_has_token(wallet_address: str, token_address: str) -> bool:
    method_signature = Web3.sha3(text="balanceOf(address)").hex()[0:10]
    padding = "000000000000000000000000"
    data = method_signature + padding + wallet_address[2:]

    body = {
        "method": "eth_call",
        "id": 1,
        "jsonrpc": "2.0",
        "params": [{"to": token_address, "data": data}, "latest"],
    }

    url = "https://mainnet.infura.io/v3/" + project_id
    res = requests.post(url, json=body)
    res.raise_for_status()
    result = res.json()["result"]
    token_balance = int(result, 16)

    if token_balance > 0:
        return True
    return False


def verify_wallet_has_any_valid_token(address: str) -> bool:
    token_addresses = get_all_nft_addresses()
    for token_address in token_addresses:
        has_token = verify_wallet_has_token(address, token_address)
        if has_token:
            return True
    return False
