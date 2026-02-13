# GoDaddy DNS Setup for palabrai.com

## Your EC2 Public IP: `100.26.196.173`

Follow these steps to point your domain to your server.

---

## Step-by-Step Guide

### Step 1: Log into GoDaddy

1. Go to https://www.godaddy.com
2. Click **Sign In** (top right corner)
3. Enter your GoDaddy username/email and password
4. Click **Sign In**

---

### Step 2: Navigate to DNS Management

1. After logging in, you'll see your account dashboard
2. Click on your **profile icon** or **username** in the top right
3. Select **"My Products"** from the dropdown menu
4. You'll see a list of all your products/domains

---

### Step 3: Access DNS Settings for palabrai.com

1. Find **palabrai.com** in your list of domains
2. Click the **"DNS"** button next to palabrai.com
   - If you don't see a DNS button, click the three dots menu (**⋮**) next to the domain
   - Then select **"Manage DNS"**
3. You'll be taken to the DNS Management page

---

### Step 4: Add A Record for Root Domain (palabrai.com)

You should see a section called **"DNS Records"** or **"Records"**.

**Look for an existing A record with Name "@" or "palabrai.com":**

**Option A: If an existing @ record exists:**
1. Find the row with Type = `A` and Name = `@`
2. Click the **pencil icon** (edit) on the right side of that row
3. In the **"Points to"** or **"Value"** field, enter: `100.26.196.173`
4. Set **TTL** to `600 seconds` (or 10 minutes)
5. Click **Save**

**Option B: If no @ record exists:**
1. Click the **"Add"** button (usually at the bottom of the records section)
2. Fill in the form:
   - **Type**: Select `A` from the dropdown
   - **Name**: Enter `@` (the @ symbol represents your root domain)
   - **Value** or **Points to**: Enter `100.26.196.173`
   - **TTL**: Select `Custom` and enter `600` seconds (10 minutes)
3. Click **Save** or **Add Record**

---

### Step 5: Update www Subdomain Record (www.palabrai.com)

**First, check what type of www record exists:**

Look through your DNS records for any record with Name = `www`. It could be:
- **A** record pointing to an IP
- **CNAME** record pointing to another domain
- **Forwarding** or other type

**If you see a www record (any type):**

1. Find the row with Name = `www`
2. Look at what **Type** it is:

   **If it's a CNAME record:**
   - Click the **trash/delete icon** to delete it
   - Confirm deletion
   - Then click **Add** button to create a new record:
     - **Type**: Select `A`
     - **Name**: Enter `www`
     - **Value**: Enter `100.26.196.173`
     - **TTL**: `600 seconds`
   - Click **Save**

   **If it's already an A record:**
   - Click the **pencil icon** (edit) on that row
   - Change the **"Points to"** or **"Value"** field to: `100.26.196.173`
   - Set **TTL** to `600 seconds`
   - Click **Save**

**If there's NO www record:**
1. Click the **"Add"** button
2. Fill in the form:
   - **Type**: Select `A` from the dropdown
   - **Name**: Enter `www`
   - **Value** or **Points to**: Enter `100.26.196.173`
   - **TTL**: Select `Custom` and enter `600` seconds
3. Click **Save** or **Add Record**

---

### Step 6: Check for Other Conflicting Records

**Important:** Make sure you don't have any of these conflicting records:

- **CNAME** record with Name `@` (conflicts with A record for root domain)
- **Multiple A records** for the same name pointing to different IPs
- **Forwarding** or **Parked** records that might interfere

**Common conflict: "Record name www conflicts with another record"**
- This means there's already a `www` record (likely CNAME)
- You must **delete the old www record first** before adding the new A record
- Or **edit** the existing record to change it to type A with IP `100.26.196.173`

To delete a conflicting record:
1. Find the conflicting record in your DNS records list
2. Click the **trash icon** or **three dots menu** next to it
3. Select **Delete**
4. Confirm deletion
5. Then add your new record

---

### Step 7: Verify Your DNS Records

After adding both records, your DNS Records section should show:

```
Type    Name    Value               TTL
----    ----    -----               ---
A       @       100.26.196.173      600 seconds
A       www     100.26.196.173      600 seconds
```

---

### Step 8: Save and Wait for Propagation

1. Make sure you've clicked **Save** on all changes
2. DNS changes typically take **10 minutes to 48 hours** to propagate worldwide
3. Most often, it takes about **30 minutes to 2 hours**

---

## Step 9: Check DNS Propagation

**On your local computer**, open Terminal (Mac/Linux) or Command Prompt (Windows):

### Check if palabrai.com resolves:
```bash
nslookup palabrai.com
```

You should see:
```
Server:  [some DNS server]
Address: [some IP]

Non-authoritative answer:
Name:    palabrai.com
Address: 100.26.196.173
```

### Check if www.palabrai.com resolves:
```bash
nslookup www.palabrai.com
```

You should see:
```
Non-authoritative answer:
Name:    www.palabrai.com
Address: 100.26.196.173
```

### Alternative check using dig:
```bash
dig palabrai.com +short
dig www.palabrai.com +short
```

Both should return: `100.26.196.173`

---

## Step 10: Test in Browser (Before SSL)

Once DNS has propagated:

1. Open your browser
2. Go to `http://palabrai.com` (note: HTTP, not HTTPS yet)
3. You might see a security warning - this is normal before SSL is set up
4. Try `http://www.palabrai.com` as well

If you see your application, DNS is working!

---

## What's Next?

After DNS is working, you need to:

1. **Update Nginx configuration** on your EC2 server
2. **Set up SSL certificates** with Let's Encrypt

See the main [DEPLOYMENT.md](DEPLOYMENT.md) file for these steps.

---

## Troubleshooting

### "DNS not resolving yet"
- Wait longer (up to 48 hours in rare cases)
- Clear your DNS cache:
  - **Mac**: `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
  - **Windows**: `ipconfig /flushdns`
  - **Linux**: `sudo systemd-resolve --flush-caches`

### "Still showing old IP or GoDaddy parking page"
- Check that you saved the DNS changes in GoDaddy
- Make sure there are no conflicting CNAME or forwarding records
- Try checking DNS from a different network (mobile data)

### "Can't find the DNS button in GoDaddy"
- Go to https://dcc.godaddy.com/domains (direct link to domain control center)
- Find palabrai.com and click **Manage**
- Look for **DNS** or **DNS Management** tab

---

## Summary

**What you added:**
1. A record: `@` → `100.26.196.173` (for palabrai.com)
2. A record: `www` → `100.26.196.173` (for www.palabrai.com)

**These changes will:**
- Point palabrai.com to your EC2 server
- Point www.palabrai.com to your EC2 server
- Allow visitors to access your application from both URLs

**Next steps:**
1. Wait for DNS propagation (check with `nslookup`)
2. Update Nginx configuration on EC2
3. Set up SSL with Certbot
