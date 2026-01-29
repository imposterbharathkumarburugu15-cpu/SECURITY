# 🚂 Railway Deployment Guide for Agentic Honey-Pot API

This guide will walk you through deploying your FastAPI application to Railway.

## 📋 Prerequisites

- [ ] A GitHub account
- [ ] A Railway account (sign up at https://railway.app)
- [ ] Git installed on your computer
- [ ] Your project code ready

## 🚀 Step-by-Step Deployment Process

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Agentic Honey-Pot API"
   ```

2. **Create a GitHub Repository**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `agentic-honeypot`)
   - **DO NOT** initialize with README (you already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Railway

1. **Sign Up/Login to Railway**:
   - Go to https://railway.app
   - Click "Login" and sign in with your GitHub account
   - Authorize Railway to access your GitHub repositories

2. **Create a New Project**:
   - Click "New Project" on the Railway dashboard
   - Select "Deploy from GitHub repo"
   - Choose your repository (e.g., `agentic-honeypot`)
   - Railway will automatically detect it's a Python project

3. **Configure Environment Variables** (Optional but Recommended):
   - In your Railway project dashboard, go to the "Variables" tab
   - Add the following variable:
     - `API_KEY` = `my_secure_api_key_123` (or your preferred secure key)
   - Note: You'll need to update `app/main.py` to use `os.getenv("API_KEY")` instead of hardcoded value

4. **Deploy**:
   - Railway will automatically start building and deploying
   - Wait for the build to complete (usually 2-5 minutes)
   - You'll see logs in the "Deployments" tab

5. **Generate a Public URL**:
   - Go to the "Settings" tab
   - Scroll to "Networking" section
   - Click "Generate Domain"
   - Railway will provide you with a URL like: `https://your-app-name.up.railway.app`

### Step 3: Verify Deployment

1. **Test the Root Endpoint**:
   ```bash
   curl https://your-app-name.up.railway.app/
   ```
   
   Expected response:
   ```json
   {"status": "active", "service": "Agentic Honey-Pot"}
   ```

2. **Test the /analyze Endpoint**:
   ```bash
   curl -X POST https://your-app-name.up.railway.app/analyze \
     -H "Content-Type: application/json" \
     -H "x-api-key: my_secure_api_key_123" \
     -d '{
       "session_id": "test_session_001",
       "message": "URGENT: Send $500 to Bitcoin wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
     }'
   ```

### Step 4: Monitor Your Application

1. **View Logs**:
   - In Railway dashboard, click on your service
   - Go to "Deployments" tab
   - Click on the latest deployment to see real-time logs

2. **Check Metrics**:
   - Railway provides CPU, Memory, and Network usage metrics
   - Monitor these to ensure your app is running smoothly

## 🔧 Configuration Files Explained

### `Procfile`
Tells Railway how to start your application:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### `railway.json`
Railway-specific configuration for build and deployment settings.

### `runtime.txt`
Specifies the Python version to use (Python 3.11).

### `requirements.txt`
Lists all Python dependencies that Railway will install.

## 🔐 Security Best Practices

1. **Use Environment Variables**:
   Update `app/main.py` to use environment variables:
   ```python
   import os
   API_KEY = os.getenv("API_KEY", "my_secure_api_key_123")
   ```

2. **Set API_KEY in Railway**:
   - Go to Variables tab
   - Add: `API_KEY` = `your_secure_random_key_here`

3. **Generate a Strong API Key**:
   ```bash
   # On Windows PowerShell:
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
   ```

## 🐛 Troubleshooting

### Build Fails
- Check the build logs in Railway dashboard
- Ensure `requirements.txt` is in the root directory
- Verify all dependencies are listed

### Application Crashes
- Check deployment logs
- Ensure the start command is correct
- Verify all required files are committed to Git

### Port Issues
- Railway automatically sets the `$PORT` environment variable
- Make sure your start command uses `--port $PORT`

### API Key Issues
- Ensure the header name is exactly `x-api-key`
- Check that the API key matches what's in your environment variables

## 📝 Quick Reference Commands

```bash
# Check deployment status
railway status

# View logs (if Railway CLI is installed)
railway logs

# Redeploy
git add .
git commit -m "Update message"
git push origin main
# Railway auto-deploys on push!
```

## 🎯 Your Deployment URL

Once deployed, your API will be available at:
```
https://your-app-name.up.railway.app
```

**Submit this URL for your hackathon!**

## 📞 Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Create an issue in your repository

---

**🎉 Congratulations! Your Agentic Honey-Pot API is now live on Railway!**
