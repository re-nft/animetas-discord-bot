import dotenv
import os
from web3.auto import w3

dotenv.load_dotenv()
curr_dir = os.path.dirname(__file__)
erc20_abi_path = os.path.join(curr_dir, "erc20_abi.json")
erc20_token_abi = ""
with open(erc20_abi_path, 'r') as f:
    erc20_token_abi = f.read()

animonkeys_token_address = "0xa32422dfb5bf85b2084ef299992903eb93ff52b0"
animetas_token_address = "0x18df6c571f6fe9283b87f910e41dc5c8b77b7da5"


def verify_wallet_has_token(wallet_address: str, token_address: str, token_abi: str) -> bool:
    token = w3.eth.contract(
        address=w3.toChecksumAddress(token_address), abi=token_abi)
    token_balance = token.functions.balanceOf(
        w3.toChecksumAddress(wallet_address)).call()
    if token_balance > 0:
        return True
    return False


def verify_wallet_has_any_valid_token(address: str) -> bool:
    token_addresses = [animonkeys_token_address, animetas_token_address]
    for token_address in token_addresses:
        has_token = verify_wallet_has_token(
            address, token_address, erc20_token_abi)
        if has_token:
            return True
    return False
