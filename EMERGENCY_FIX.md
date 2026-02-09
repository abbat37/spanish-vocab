# EMERGENCY FIX - CSS Not Loading

## Immediate Fix (Run on EC2)

**SSH into EC2:**
```bash
ssh -i ~/.ssh/spanish-vocab-key.pem ubuntu@YOUR_EC2_IP
```

**Check if Node.js is installed:**
```bash
node --version
npm --version
```

### If Node.js is NOT installed:

```bash
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should show v18.x
npm --version   # Should show v9.x or v10.x
```

### Deploy the fix:

```bash
cd ~/spanish-vocab

# Pull latest code (if not already)
git pull origin main

# Install npm dependencies
npm install

# Build the CSS
npm run build:css:prod

# Verify CSS was created
ls -lh app/static/css/output.css

# Restart the service
sudo systemctl restart spanish-vocab

# Check status
sudo systemctl status spanish-vocab
```

### Verify Fix:

1. Visit: https://spanish-vocab.duckdns.org
2. Refresh with hard reload: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
3. Should now see the styled version

---

## Root Cause

Node.js was not installed on EC2, so the CSS build step in CI/CD failed silently.

## Long-term Fixes

I'm implementing these now:
1. Add health check to verify CSS exists before deployment
2. Add deployment validation tests
3. Improve CI/CD error handling
4. Add CSS file size check

---

**Run the commands above now to fix the site!**
