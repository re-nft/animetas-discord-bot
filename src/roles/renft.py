import dotenv
import os
from typing import List, Set
import requests
from config import cfg

dotenv.load_dotenv()
api_key = os.environ.get("THE_GRAPH_API_KEY", "")
url = cfg["Settings"]["renft_query_url"].replace(
    "[api-key]", api_key)


def transform_rentings_to_nft_addresses(rentings: List[dict]) -> Set[str]:
    def transform_renting_to_nft_address(renting: dict) -> str:
        return renting["nft"]["lending"]["nftAddress"]

    return set(map(transform_renting_to_nft_address, rentings))


def get_rented_nft_addresses_for_wallet(address: str) -> Set[str]:
    query = """query {
      rentings(renterAddress: "%s") {
        nft {
          lending {
            nftAddress
          }
        }
      }
    }""" % address
    res = requests.post(url, query)
    res.raise_for_status()
    rentings = res.json()["data"]["rentings"]
    return transform_rentings_to_nft_addresses(rentings)


def verify_address_has_animetas_nft(address: str) -> bool:
    # TODO: handle The Graph not working
    nft_addresses = get_rented_nft_addresses_for_wallet(address)

    animonkey_address = "0xa32422dfb5bf85b2084ef299992903eb93ff52b0"
    animetas_address = "0x18df6c571f6fe9283b87f910e41dc5c8b77b7da5"

    valid_addresses = {animonkey_address, animetas_address}
    intersected = nft_addresses.intersection(valid_addresses)
    if len(intersected) > 0:
        return True
    return False
