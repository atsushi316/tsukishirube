#!/usr/bin/env node
/**
 * Verify that Tsuki's events were published to relays
 */

const WebSocket = require('ws');

const NPUB = 'rfcaqh5zwqts59zhzljefnt8z9fmp357qczn8ne';
const RELAY = 'wss://relay.ditto.pub';

console.log('🔍 Verifying Tsuki posts on Nostr\n');
console.log(`npub: ${NPUB}`);
console.log(`relay: ${RELAY}\n`);

const ws = new WebSocket(RELAY);
let eventsFound = 0;

ws.on('open', () => {
  console.log('✅ Connected to relay\n');
  
  // Query for Tsuki's events
  const filter = {
    authors: [NPUB],
    limit: 10
  };
  
  const req = JSON.stringify(['REQ', 'tsuki-verify', filter]);
  console.log('📤 Querying for events...\n');
  ws.send(req);
});

ws.on('message', (data) => {
  const msg = JSON.parse(data);
  
  if (msg[0] === 'EVENT') {
    eventsFound++;
    const event = msg[2];
    
    console.log(`📨 Event ${eventsFound}:`);
    console.log(`   kind: ${event.kind}`);
    console.log(`   created: ${new Date(event.created_at * 1000).toLocaleString()}`);
    
    if (event.kind === 0) {
      const profile = JSON.parse(event.content);
      console.log(`   name: ${profile.name}`);
      console.log(`   about: ${profile.about}`);
    } else if (event.kind === 1111) {
      console.log(`   content: ${event.content.substring(0, 50)}...`);
      console.log(`   tags: ${event.tags.map(t => t[0]).join(', ')}`);
    }
    console.log();
  } else if (msg[0] === 'EOSE') {
    console.log(`✅ Query complete. Found ${eventsFound} events\n`);
    ws.close();
  }
});

ws.on('close', () => {
  if (eventsFound === 0) {
    console.log('⚠️  No events found. Publishing may have failed.');
    console.log('Possible reasons:');
    console.log('  - Relay is not connected');
    console.log('  - Events are still propagating');
    console.log('  - Try again in a few seconds');
  } else {
    console.log('🎉 Tsuki is live on Nostr!\n');
    console.log(`📊 Total events published: ${eventsFound}`);
    console.log('Status: ✅ VERIFIED\n');
  }
});

ws.on('error', (err) => {
  console.error('❌ Connection error:', err.message);
});

// Timeout after 5 seconds
setTimeout(() => {
  ws.close();
}, 5000);
