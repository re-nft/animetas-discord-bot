import time
from dataclasses import dataclass
from typing import Set
import requests
from config import cfg
from utils.utils import get_all_nft_addresses

url = cfg["Settings"]["renft_query_url"]

DAYS_TO_SECONDS = 86400


@dataclass(frozen=True)
class Renting:
    # in days
    rent_duration: int
    # unix timestamp in seconds
    rented_at: int
    nft_address: str


def get_renting_for_wallet(address: str) -> Set[Renting]:
    query = (
        """
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
    """
        % address
    )
    body = {"query": query}

    res = requests.post(url, json=body)
    res.raise_for_status()
    user = res.json()["data"]["user"]
    if user is None or user["renting"] is None:
        return set()

    def transform_renting_item_to_dataclass(renting_item: dict) -> Renting:
        return Renting(
            int(renting_item["rentDuration"]),
            int(renting_item["rentedAt"]),
            renting_item["lending"]["nftAddress"],
        )

    return set(map(transform_renting_item_to_dataclass, user["renting"]))


def get_rented_with_configured_addresses(renting: Set[Renting]) -> Set[Renting]:
    valid_addresses = set(get_all_nft_addresses())

    return set(filter(lambda item: item.nft_address in valid_addresses, renting))


def is_currently_renting(renting: Renting) -> bool:
    rent_duration_s = int(renting.rent_duration) * DAYS_TO_SECONDS
    renting_end_time_s = int(renting.rented_at) + rent_duration_s
    current_time_s = int(time.time())
    return current_time_s < renting_end_time_s


def verify_address_currently_rents_configured_nfts(address: str) -> bool:
    renting = get_rented_with_configured_addresses(get_renting_for_wallet(address))
    return any(list(map(is_currently_renting, renting)))
