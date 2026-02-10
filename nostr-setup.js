#!/usr/bin/env node
/**
 * Nostr keypair setup for Tsuki (月)
 * Generates keypair securely and saves nsec encrypted
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// Install nostr-tools if needed
try {
  require('nostr-tools');
} catch (e) {
  console.error('❌ nostr-tools not found. Install with: npm install nostr-tools');
  process.exit(1);
}

const { generateSecretKey, getPublicKey, nip19 } = require('nostr-tools');

// Generate keypair
const nsec = generateSecretKey();
const npub = getPublicKey(nsec);

// Convert to bech32 format (human readable)
const nsecBech32 = nip19.nsecEncode(nsec);
const npubBech32 = nip19.npubEncode(npub);

console.log('🌙 Nostr Keypair Generation');
console.log('==========================\n');

console.log('✅ Public Key (npub):');
console.log(npubBech32);
console.log('\n📝 Save this to MEMORY.md\n');

console.log('🔐 Secret Key (nsec):');
console.log(nsecBech32);
console.log('\n⚠️  KEEP THIS SAFE - DO NOT SHARE\n');

// Encrypt and save nsec
const nostrDir = path.join(process.env.HOME, '.nostr');
if (!fs.existsSync(nostrDir)) {
  fs.mkdirSync(nostrDir, { mode: 0o700 });
  console.log(`✅ Created ${nostrDir} with restricted permissions (700)`);
}

const algorithm = 'aes-256-cbc';
const salt = crypto.randomBytes(8);
const passphrase = process.env.NOSTR_PASSPHRASE || 'default';

// Key derivation (PBKDF2)
const key = crypto.pbkdf2Sync(passphrase, salt, 100000, 32, 'sha256');
const iv = crypto.randomBytes(16);

const cipher = crypto.createCipheriv(algorithm, key, iv);
let encrypted = cipher.update(nsecBech32, 'utf8', 'hex');
encrypted += cipher.final('hex');

// Save: salt + iv + encrypted
const encryptedData = salt.toString('hex') + ':' + iv.toString('hex') + ':' + encrypted;
const encPath = path.join(nostrDir, 'nsec.enc');

fs.writeFileSync(encPath, encryptedData, { mode: 0o600 });
console.log(`✅ Encrypted nsec saved to ${encPath}`);
console.log(`   Permissions: 600 (only user can read)\n`);

console.log('🎯 Next steps:');
console.log('1. Save npub above to MEMORY.md');
console.log('2. Set NOSTR_PASSPHRASE env var (or use "default")');
console.log('3. Run: NOSTR_PASSPHRASE="your-passphrase" node nostr-post.js\n');
