#!/usr/bin/env python
import requests
import json
from config import cfg

url = cfg["Settings"]["renft_query_url"]


# * run this script as python -m utils.subgraph_snapshot from src/

# ! note that this only works for up to 1000 results
# ! this is the graph protocol's limitation
# ! to expand the set of results a combination of
# ! of "first" and "skip" args in the query is
# ! required
def take_snapshot():
    query = """
    {
      lendings(
        orderBy: lenderAddress,
        orderDirection: desc
      ) {
        lenderAddress
      }
    }
    """
    body = {"query": query}

    res = requests.post(url, json=body)
    res.raise_for_status()
    lendings = map(lambda x: x["lenderAddress"], res.json()["data"]["lendings"])

    with open("animetas_lenders_snapshot.json", "w+") as f:
        f.write(json.dumps(list(lendings), indent=4))


if __name__ == "__main__":
    take_snapshot()
