import time
from dataclasses import dataclass
from typing import Set
import requests
from config import cfg

url = cfg["Settings"]["renft_query_url"]


@dataclass(frozen=True)
class Renting:
    # in days
    rent_duration: int
    # unix timestamp in seconds
    rented_at: int
    nft_address: str


def get_renting_for_wallet(address: str) -> Set[Renting]:
    query = """
    {
      user(id:"%s") {
        renting {
          rentDuration
          rentedAt
          lending {
            nftAddress
          }
        }
      }
    }
    """ % address
    body = {"query": query}

    res = requests.post(url, json=body)
    res.raise_for_status()
    user = res.json()["data"]["user"]
    if user is None or user["renting"] is None:
        return set()

    def transform_renting_item_to_dataclass(renting_item: dict) -> Renting:
        return Renting(renting_item["rentDuration"], renting_item["rentedAt"],
                       renting_item["lending"]["nftAddress"])

    return set(map(transform_renting_item_to_dataclass, user["renting"]))


def get_rented_with_configured_addresses(renting:
                                         Set[Renting]) -> Set[Renting]:
    animonkey_address = "0xa32422dfb5bf85b2084ef299992903eb93ff52b0"
    animetas_address = "0x18df6c571f6fe9283b87f910e41dc5c8b77b7da5"
    valid_addresses = {animonkey_address, animetas_address}

    return set(
        filter(lambda item: item.nft_address in valid_addresses, renting))


def is_currently_renting(renting: Renting) -> bool:
    DAYS_TO_SECONDS = 86400
    rent_duration_s = renting.rent_duration * DAYS_TO_SECONDS
    renting_end_time_s = renting.rented_at + rent_duration_s
    # convert to int for precision in seconds
    current_time_s = int(time.time())
    return current_time_s < renting_end_time_s


def verify_address_currently_rents_configured_nfts(address: str) -> bool:
    renting = get_rented_with_configured_addresses(
        get_renting_for_wallet(address))
    return any(list(map(is_currently_renting, renting)))
