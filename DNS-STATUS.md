# Zanoma DNS Migration Status — March 22, 2026

## Current State: WAITING ON CLOUDFLARE CACHE
- DNS records are correct ✅
- Ghost Pro activated with www.zanoma.com ✅
- Old WordPress site behind Cloudflare is still serving cached content
- Should resolve within 30-60 minutes

## DNS Records (GoDaddy)
| Type | Name | Value |
|------|------|-------|
| A | @ | 178.128.137.126 |
| CNAME | www | zanoma.ghost.io |

## Ghost Pro
- Site: zanoma.ghost.io
- Plan: Creator ($9/mo)
- Custom domain: www.zanoma.com (activated)
- Admin API key: 69c01ab69d9f6f0001cf76e3:e74200bfddb31147de9c40d56b6d51f3a2f2e466750adca7cbb678159500a754
- Admin: https://zanoma.ghost.io/ghost/
- Login: kevin.keranen@mac.com

## Old WordPress
- Host: WP Engine (wp.wpenginepowered.com)
- CDN: Cloudflare (still proxying)
- Old IPs: 141.193.213.10, 141.193.213.11 (deleted from GoDaddy)

## What's Live
- zanoma.ghost.io → NEW SITE ✅
- www.zanoma.com → still showing old site (Cloudflare cache)
- zanoma.com → redirects to www → still old site
