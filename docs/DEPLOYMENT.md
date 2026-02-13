# Deployment Guide

## Custom Domain Setup (GoDaddy)

### Configuring palabrai.com to point to your EC2 instance

1. **Get your EC2 Public IP:**
   ```bash
   # SSH into your EC2 instance
   ssh -i ~/.ssh/spanish-vocab-key.pem ubuntu@YOUR_EC2_IP

   # Get the public IP (if you don't already have it)
   curl -4 ifconfig.me
   ```

2. **Configure DNS in GoDaddy:**
   - Log into your GoDaddy account at https://www.godaddy.com
   - Go to "My Products" → "Domains" → Click "DNS" next to palabrai.com
   - Add/Edit the following DNS records:

   **A Record (for palabrai.com):**
   - Type: `A`
   - Name: `@` (this represents the root domain)
   - Value: `YOUR_EC2_PUBLIC_IP`
   - TTL: `600` seconds (10 minutes)

   **A Record (for www.palabrai.com):**
   - Type: `A`
   - Name: `www`
   - Value: `YOUR_EC2_PUBLIC_IP`
   - TTL: `600` seconds

   Alternatively, you can use a CNAME for www:
   - Type: `CNAME`
   - Name: `www`
   - Value: `palabrai.com`
   - TTL: `1 Hour`

3. **Wait for DNS propagation:**
   DNS changes can take 10 minutes to 48 hours to propagate. Check status with:
   ```bash
   # Check if DNS has updated
   nslookup palabrai.com
   dig palabrai.com
   ```

4. **Update Nginx configuration:**
   SSH into EC2 and update the Nginx server configuration:
   ```bash
   sudo nano /etc/nginx/sites-available/spanish-vocab
   ```

   Update the `server_name` directive to include your new domain:
   ```nginx
   server {
       listen 80;
       server_name palabrai.com www.palabrai.com spanish-vocab.duckdns.org;

       # ... rest of your config
   }
   ```

   Test and reload Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

5. **Set up SSL certificate for palabrai.com:**
   ```bash
   # Request SSL certificate for the new domain
   sudo certbot --nginx -d palabrai.com -d www.palabrai.com

   # Follow the prompts to configure HTTPS
   # Choose option 2 to redirect HTTP to HTTPS
   ```

   Certbot will automatically:
   - Obtain SSL certificates from Let's Encrypt
   - Configure Nginx to use HTTPS
   - Set up auto-renewal

6. **Verify SSL setup:**
   ```bash
   # Check certificate status
   sudo certbot certificates

   # Test auto-renewal
   sudo certbot renew --dry-run
   ```

7. **Update application configuration (if needed):**
   If your app has domain-specific settings, update `.env`:
   ```bash
   cd ~/spanish-vocab
   nano .env
   ```

   Add or update:
   ```
   DOMAIN=palabrai.com
   ```

8. **Test the new domain:**
   - Visit https://palabrai.com in your browser
   - Visit https://www.palabrai.com in your browser
   - Both should load your application with a valid SSL certificate

### Troubleshooting DNS/Domain Issues

**DNS not resolving:**
```bash
# Check DNS propagation
nslookup palabrai.com 8.8.8.8  # Check against Google DNS
nslookup palabrai.com 1.1.1.1  # Check against Cloudflare DNS

# Flush local DNS cache (on your computer)
# Mac: sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
# Windows: ipconfig /flushdns
# Linux: sudo systemd-resolve --flush-caches
```

**SSL certificate issues:**
```bash
# Check certificate
sudo certbot certificates

# Renew certificate
sudo certbot renew

# If certificate fails, check Nginx config
sudo nginx -t

# Check if port 80 and 443 are accessible
sudo ufw status  # Check firewall
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443
```

**502 Bad Gateway:**
```bash
# Check if app is running
sudo systemctl status spanish-vocab

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

## Prerequisites on EC2

Before deploying, ensure Node.js is installed on your EC2 server:

```bash
# Install Node.js 18.x
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should be v18.x
npm --version   # Should be v9.x or v10.x
```

## Automated Deployment (CI/CD)

The app automatically deploys when you push to the `main` branch.

**What happens:**
1. GitHub Actions runs tests
2. If tests pass, it connects to EC2 via SSH
3. Pulls latest code
4. Installs npm dependencies
5. **Builds production CSS** (`npm run build:css:prod`)
6. Installs Python dependencies
7. Runs database migrations
8. Restarts the application

**View deployment logs:**
- Go to: https://github.com/abbat37/spanish-vocab/actions
- Click on the latest workflow run

## Manual Deployment

If you need to deploy manually from EC2:

```bash
# SSH into EC2
ssh -i ~/.ssh/spanish-vocab-key.pem ubuntu@YOUR_EC2_IP

# Run the deployment script
cd ~/spanish-vocab
./deploy.sh
```

Or run commands individually:

```bash
cd ~/spanish-vocab
git pull origin main
npm install
npm run build:css:prod
source venv/bin/activate
pip install -r requirements.txt
python3 -m flask db upgrade
sudo systemctl restart spanish-vocab
```

## Verifying Deployment

Check if the service is running:

```bash
sudo systemctl status spanish-vocab
```

Check application logs:

```bash
sudo journalctl -u spanish-vocab -n 50 --no-pager
```

Check Nginx logs:

```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

## CSS Build Process

The deployment automatically builds optimized CSS:

```bash
npm run build:css:prod
```

This creates `app/static/css/output.css` (17KB minified) from `app/static/css/input.css`.

**Important:** The output.css file is gitignored, so it must be built on the server during deployment.

## Troubleshooting

### CSS not loading

```bash
# Check if output.css exists
ls -lh ~/spanish-vocab/app/static/css/output.css

# Rebuild CSS
cd ~/spanish-vocab
npm run build:css:prod

# Restart service
sudo systemctl restart spanish-vocab
```

### Node.js not found

```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Service won't start

```bash
# Check logs
sudo journalctl -u spanish-vocab -n 100

# Check if port is in use
sudo lsof -i :8000

# Restart manually
cd ~/spanish-vocab
source venv/bin/activate
gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"
```

### Database migration issues

```bash
cd ~/spanish-vocab
source venv/bin/activate

# Check current migration
python3 -m flask db current

# Show migration history
python3 -m flask db history

# Upgrade to latest
python3 -m flask db upgrade
```

## Rollback Procedure

If something goes wrong:

```bash
# SSH into EC2
ssh -i ~/.ssh/spanish-vocab-key.pem ubuntu@YOUR_EC2_IP

# Navigate to app
cd ~/spanish-vocab

# View recent commits
git log --oneline -5

# Rollback to previous commit
git reset --hard HEAD~1

# Rebuild
npm run build:css:prod
source venv/bin/activate
pip install -r requirements.txt

# Restart
sudo systemctl restart spanish-vocab
```

## First-Time Setup on New EC2 Instance

If deploying to a brand new EC2 instance:

```bash
# Install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git postgresql postgresql-contrib nginx certbot python3-certbot-nginx

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Clone repository
git clone https://github.com/abbat37/spanish-vocab.git
cd spanish-vocab

# Set up Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up Node environment and build CSS
npm install
npm run build:css:prod

# Configure .env file
cp .env.example .env
nano .env  # Add your production secrets

# Set up database
# ... (see main README for PostgreSQL setup)

# Set up systemd service
# ... (see main README for systemd setup)

# Set up Nginx
# ... (see main README for Nginx setup)

# Set up SSL
sudo certbot --nginx -d spanish-vocab.duckdns.org
```

## Monitoring

Check app health:

```bash
# Service status
sudo systemctl status spanish-vocab

# Recent logs
sudo journalctl -u spanish-vocab -f

# Resource usage
htop

# Disk space
df -h

# Check if CSS file was built
ls -lh ~/spanish-vocab/app/static/css/output.css
```

## Performance

**CSS Optimization:**
- Development: `npm run build:css` (25KB, readable)
- Production: `npm run build:css:prod` (17KB, minified)
- Always use production build on EC2

**Caching:**
- Nginx caches static files (CSS, JS, images)
- CSS has cache headers for browser caching
- Update cache-busting if CSS doesn't update: append `?v=VERSION` to CSS link

## Security Notes

- The `.env` file contains secrets (never commit!)
- SSH key should have 400 permissions
- Always use HTTPS in production
- Keep Node.js and npm updated
- Regularly update system packages: `sudo apt update && sudo apt upgrade`
