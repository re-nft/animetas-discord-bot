var web3js;
const message = "Sign this message to prove ownership / rentership";

window.addEventListener("load", function () {
  if (typeof window.ethereum !== "undefined") {
    console.log("MetaMask is installed!");
  }
});

async function initWeb3() {
  const addresses = await window.ethereum.request({
    method: "eth_requestAccounts",
  });

  web3js = new Web3(window.ethereum);
  return addresses[0];
}

function sign(address) {
  return web3js.eth.personal.sign(message, address, "");
}

async function verifyWithServer(address, signature, userId, guildId) {
  const data = {
    address: address,
    message: message,
    signature: signature,
    userId: userId,
    guildId: guildId,
  };
  const res = await fetch(connectUrl, {
    method: "POST",
    cache: "no-cache",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return res.json();
}

async function connectToWallet() {
  const address = await initWeb3();
  const signature = await sign(address);
  const resBody = await verifyWithServer(address, signature, userId, guildId);
  if (resBody.success === true) {
    alertify.success(resBody.message);
  } else {
    alertify.error(resBody.message);
  }
}
