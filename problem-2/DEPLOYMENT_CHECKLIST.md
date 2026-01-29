# 🚂 Railway Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] All code is working locally
- [ ] `requirements.txt` is up to date
- [ ] `.gitignore` is configured
- [ ] `Procfile` exists
- [ ] `railway.json` exists
- [ ] `runtime.txt` exists

## ✅ GitHub Setup

- [ ] Git repository initialized
- [ ] All files committed
- [ ] GitHub repository created
- [ ] Code pushed to GitHub

## ✅ Railway Setup

- [ ] Railway account created
- [ ] GitHub connected to Railway
- [ ] New project created from GitHub repo
- [ ] Domain generated
- [ ] Environment variables set (optional):
  - [ ] `API_KEY` = your_secure_key

## ✅ Testing

- [ ] Root endpoint (`/`) works
- [ ] `/analyze` endpoint works with API key
- [ ] Logs show no errors
- [ ] Application is accessible via Railway URL

## 🎯 Your Deployment Info

**GitHub Repository URL:**
```
https://github.com/YOUR_USERNAME/YOUR_REPO_NAME
```

**Railway Project URL:**
```
https://railway.app/project/YOUR_PROJECT_ID
```

**Live API URL:**
```
https://your-app-name.up.railway.app
```

**API Key:**
```
my_secure_api_key_123
```

## 📝 Quick Test Commands

### Test Root Endpoint
```bash
curl https://your-app-name.up.railway.app/
```

### Test Analyze Endpoint
```bash
curl -X POST https://your-app-name.up.railway.app/analyze \
  -H "Content-Type: application/json" \
  -H "x-api-key: my_secure_api_key_123" \
  -d '{
    "session_id": "test_001",
    "message": "Send money to Bitcoin wallet 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
  }'
```

## 🔄 Redeployment Process

When you make changes:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

Railway will automatically redeploy! 🎉
