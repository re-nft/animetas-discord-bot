# animetas-discord-bot
Queries the reNFT's collateral-free registry, if the address is renting Animetas or Animonkey, give the Discord user a role

# Problem background

We have a registry contract implemented on the mainnet, that is called on https://animetas.renft.io. This is the contract: https://etherscan.io/address/0xa8D3F65b6E2922fED1430b77aC2b557e1fa8DA4a

This contract enables the lender to send their NFT into the contract, and then to be rented by another party. Renting does not send the NFT to renter. It is not possible to rent the same NFT twice. The contract does not have a read function that returns the rentings of a given address. For that reason, we have deployed a subgraph: https://thegraph.com/studio/subgraph/renft-registry/. This subgraph indexes all the events emitted by the contract and keeps track of information such as who rents what, who lends what, and represents the whole set of information available.

Subgraphs can be queried using GraphQL. Here is an example query for the above subgraph

```graphql
{
  lendings(first: 5) {
    id
    nftAddress
    tokenID
    lenderAddress
  }
  rentings(first: 5) {
    id
    renterAddress
    rentAmount
    rentDuration
  }
}
```

We will need to use this subgraph to check if a particular address is renting any Animonkey: `0xa32422dfb5bf85b2084ef299992903eb93ff52b0` or Animetas: `0x18df6c571f6fe9283b87f910e41dc5c8b77b7da5` NFT and assign them a "renter" role in Discord.

# Spec

- Language: Python
- Discord user types a command to verify that they are a renter.
- The bot pulls their metamask address (similar to / like CollabLand).
- The script queries our registry subgraph for this particular address.
- The script checks if this address is renting Animetas or Animonkey NFT.
- If they are not renting, the user does not get a role.
- If they are renting, the user gets a "renter" role.
