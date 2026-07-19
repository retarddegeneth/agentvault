/* kimilabs wallet connect — client-side only, no keys ever leave the browser */
(() => {
  const KEY = 'kimilabs_wallet';
  let connected = null;

  async function connect() {
    if (!window.ethereum) {
      alert('install a browser wallet first');
      return;
    }
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      await provider.send('eth_requestAccounts', []);
      const signer = await provider.getSigner();
      const address = await signer.getAddress();
      const network = await provider.getNetwork().catch(() => ({ chainId: 0n }));
      const chainId = Number(network.chainId || 0);

      if (chainId === 4663 || chainId === 46630) {
        localStorage.setItem(KEY, address);
        connected = address;
        updateUI();
        return;
      }

      const want = '0x1237';
      try {
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: want }],
        });
        localStorage.setItem(KEY, address);
        connected = address;
        updateUI();
      } catch (e) {
        if (e.code === 4902) {
          alert('add Robinhood Chain (4663) to your wallet first');
        } else {
          console.error(e);
        }
      }
    } catch (e) {
      console.error('connect error', e);
    }
  }

  function disconnect() {
    connected = null;
    localStorage.removeItem(KEY);
    updateUI();
  }

  function updateUI() {
    document.querySelectorAll('[data-wallet="addr"]').forEach(el => {
      el.textContent = connected ? connected.slice(0, 6) + '...' + connected.slice(-4) : 'disconnected';
    });
    document.querySelectorAll('[data-wallet="action"]').forEach(el => {
      el.textContent = connected ? '[disconnect]' : '[connect wallet]';
    });
    document.querySelectorAll('[data-wallet="connected"]').forEach(el => {
      el.style.display = connected ? '' : 'none';
    });
    document.querySelectorAll('[data-wallet="disconnected"]').forEach(el => {
      el.style.display = connected ? 'none' : '';
    });
  }

  window.connectWallet = () => {
    if (connected) {
      disconnect();
    } else {
      connect();
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    connected = localStorage.getItem(KEY) || null;
    updateUI();
  });
})();
