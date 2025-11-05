# Get APS Credentials in 5 Minutes

## Step-by-Step (Follow Exactly)

### 1. Open This URL
**→ https://aps.autodesk.com/myapps**

### 2. Sign In
- Use your Autodesk account (same as Revit/AutoCAD)
- Don't have one? Click "Sign Up" (free!)

### 3. Create App
- Click blue **"Create App"** button
- App Name: `Revit Family Maker`
- Description: `AI family generation`
- Callback URL: `http://localhost:3000`
- Click **"Create"**

### 4. Enable Design Automation
- You'll see your new app
- Click on it to open settings
- Find **"APIs"** section
- Check the box: **"Design Automation API v3"**
- Click **"Save"** at bottom

### 5. Copy Your Credentials

You'll see two things:

**Client ID** (looks like this):
```
abc123def456ghi789jkl012mno345pqr678stu901
```

**Client Secret** (click "Show" to see it):
```
XyZ789AbC123DeF456
```

### 6. Paste Here

Once you have them, paste them in your terminal like this:

```
APS_CLIENT_ID: abc123def456ghi789jkl012mno345pqr678stu901
APS_CLIENT_SECRET: XyZ789AbC123DeF456
```

I'll automatically update your .env file!

---

**Total Time: 5 minutes**

**Stuck?**
- Can't find "Design Automation API"? → Make sure you're on the app settings page
- Can't see Client Secret? → Click the "Show" button next to it
- App creation failed? → Check you accepted the terms of service

---

**Alternative: Skip This For Now**

We can:
1. ✅ Test everything except real Revit generation (works now!)
2. ✅ Prepare C# build scripts
3. ✅ Set up templates
4. ✅ Test the agent with OpenAI

Then come back to APS when you're ready for real Revit families.

What do you want to do?
