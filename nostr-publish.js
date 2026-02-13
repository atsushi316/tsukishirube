#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');
const { getPublicKey, finalizeEvent } = require('nostr-tools');

const RELAYS = ['wss://relay.ditto.pub', 'wss://relay.primal.net', 'wss://relay.damus.io'];

async function run() {
  const config = JSON.parse(fs.readFileSync(path.join(process.env.HOME, '.openclaw', 'openclaw.json'), 'utf8'));
  const skHex = config.channels.nostr.privateKey;
  const sk = new Uint8Array(Buffer.from(skHex, 'hex'));
  const pk = getPublicKey(sk);

  const event = finalizeEvent({
    kind: 0,
    created_at: Math.floor(Date.now() / 1000),
    tags: [],
    content: JSON.stringify({
      name: 'TSUKI',
      display_name: 'TSUKI',
      picture: 'https://raw.githubusercontent.com/atsushi/memory-of-the-moon/main/avatar.png'
    })
  }, sk);

  console.log(`📤 Minimal profile update for ${pk}...`);

  RELAYS.forEach(url => {
    const ws = new WebSocket(url);
    ws.on('open', () => {
      ws.send(JSON.stringify(['EVENT', event]));
      console.log(`  ✅ Sent to ${url}`);
      setTimeout(() => ws.close(), 1000);
    });
    ws.on('error', e => console.log(`  ❌ ${url}: ${e.message}`));
  });
}
run();
