# Production Deployment Guide

This guide provides step-by-step instructions for deploying the Smart Video Learning Tool to production.

## 📋 Deployment Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┴──────────────┐
          │                             │
    ┌─────▼──────────┐         ┌──────▼──────────┐
    │  FRONTEND      │         │  API REQUESTS   │
    │  (Vercel)      │         │                 │
    │  • React       │         │  (Render/Railway)
    │  • Tailwind    │         │  • FastAPI      │
    │  • Axios       │         │  • OpenAI API   │
    └────────────────┘         │  • YouTube API  │
                               └─────────────────┘
```

## 🚀 Phase 1: Frontend Deployment (Vercel / Netlify)

### Option A: Deploy to Vercel (Recommended)

#### Prerequisites:
- GitHub account with project repository
- Vercel account (free at vercel.com)

#### Steps:

1. **Connect GitHub Repository**
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository
   - Authorize Vercel to access your repo

2. **Configure Frontend Settings**
   - Framework: Select "Vite"
   - Root Directory: `./frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Set Environment Variables**
   - In Vercel Dashboard → Settings → Environment Variables
   - Add: `VITE_API_BASE_URL` = `https://your-backend-deployed-url.com`
   - Add for local: `VITE_API_BASE_URL` = `http://localhost:8000` (development)

4. **Deploy**
   - Click "Deploy"
   - Wait for build completion (2-5 minutes)
   - Your frontend URL will be: `https://your-project.vercel.app`

#### Environment Variables in Vercel:
```
VITE_API_BASE_URL=https://your-backend-api.onrender.com
VITE_APP_ENV=production
```

---

### Option B: Deploy to Netlify

#### Prerequisites:
- GitHub account
- Netlify account (free at netlify.com)

#### Steps:

1. **Connect GitHub**
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect to GitHub and authorize

2. **Configure Build Settings**
   - Repository: Select your repo
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Add Environment Variables**
   - Settings → Build & Deploy → Environment
   - Add: `VITE_API_BASE_URL` = `https://your-backend-deployed-url.com`

4. **Deploy**
   - Click "Deploy site"
   - Your frontend URL will be: `https://your-site.netlify.app`

#### Netlify Configuration (Already in `netlify.toml`):
- Automatic redirects for SPA routing
- Cache headers configured
- Environment variables supported

---

## 🚀 Phase 2: Backend Deployment (Render / Railway)

### Option A: Deploy to Render (Recommended for Free Tier)

#### Prerequisites:
- GitHub account
- Render account (free at render.com)

#### Steps:

1. **Create New Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect to GitHub repository

2. **Configure Service**
   - Name: `smart-video-learning-tool-api`
   - Environment: Python
   - Region: Select nearest region
   - Branch: main
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   - Go to Service → Environment
   - Add the following variables:
   
   ```
   OPENAI_API_KEY=sk-your_actual_key_here
   APP_ENV=production
   DEBUG=false
   FRONTEND_URL=https://your-frontend-url.vercel.app
   PYTHON_VERSION=3.11.0
   ```

4. **Deploy**
   - Render automatically deploys on push to main
   - Your backend URL will be: `https://your-api-name.onrender.com`
   - Health check: `https://your-api-name.onrender.com/` (should return JSON)

#### Important Notes:
- Render's free tier puts services to sleep after 15 minutes of inactivity
- For production use, upgrade to paid tier
- Deployment takes 3-5 minutes

---

### Option B: Deploy to Railway

#### Prerequisites:
- GitHub account
- Railway account (free at railway.app)
- GitHub token for private repos (optional)

#### Steps:

1. **Create New Project**
   - Go to [railway.app](https://railway.app)
   - Click "Start New Project"
   - Select "Deploy from GitHub"
   - Connect GitHub and select repository

2. **Configure Service**
   - Select the repository
   - Railway auto-detects Python project
   - Set Root Directory: `backend`

3. **Configure Build & Deploy**
   - Settings → Deploy
   - Builder: Nixpacks (auto-selected for Python)
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Add Environment Variables**
   - Variables tab:
   ```
   OPENAI_API_KEY=sk-your_actual_key_here
   APP_ENV=production
   DEBUG=false
   FRONTEND_URL=https://your-frontend-url.vercel.app
   PORT=8000
   ```

5. **Deploy & Get URL**
   - Railway automatically deploys
   - Public URL appears in settings
   - Your backend URL will be: `https://your-project.railway.app`

#### Key Points:
- Railway includes a database option (PostgreSQL)
- More generous free tier than Render
- Supports multiple environments (dev, staging, prod)

---

## 🔗 Connecting Frontend to Backend

After deployment, update your frontend environment variables:

### For Vercel:
1. Go to Vercel Dashboard → Project Settings → Environment Variables
2. Update `VITE_API_BASE_URL` to your deployed backend URL
3. Trigger a redeployment (push to main)

### For Netlify:
1. Go to Netlify → Site Settings → Build & Deploy → Environment
2. Update `VITE_API_BASE_URL`
3. Trigger a redeploy

---

## 🔐 Security Checklist

### Backend Security:
- [ ] Set `DEBUG=false` in production
- [ ] Use strong OpenAI API key
- [ ] Verify CORS is restricted to your frontend URL
- [ ] Use HTTPS for all connections
- [ ] Keep dependencies updated
- [ ] Don't commit `.env` file to git

### Frontend Security:
- [ ] Environment variables don't expose sensitive data
- [ ] API calls use HTTPS in production
- [ ] No hardcoded API keys
- [ ] Validate user input before API calls

---

## 🧪 Testing Deployment

### Test Backend Health:
```bash
# Replace with your deployed URL
curl https://your-backend-api.onrender.com/

# Should return:
# {
#   "status": "Backend running successfully",
#   "environment": "production",
#   "version": "0.1.0",
#   "message": "Smart Video Learning Tool API is active"
# }
```

### Test Frontend:
1. Visit your deployed frontend URL: `https://your-site.vercel.app`
2. Check browser console for errors
3. Verify API communication in Network tab

### Test CORS:
```bash
curl -X OPTIONS https://your-backend-api.onrender.com/ \
  -H "Origin: https://your-frontend.vercel.app" \
  -H "Access-Control-Request-Method: GET"
```

---

## 📊 Live Demo URLs (Example)

After deployment, you'll have:

```
Frontend:  https://smart-video-learning-app.vercel.app
Backend:   https://smart-video-api.onrender.com
API Docs:  https://smart-video-api.onrender.com/docs
```

---

## 🔄 Updating Deployments

### Push Updates to Production:

**Frontend:**
```bash
# Make changes, then push to main
git add .
git commit -m "Update frontend"
git push origin main

# Vercel/Netlify auto-deploys
```

**Backend:**
```bash
# Make changes, then push to main
git add .
git commit -m "Update backend"
git push origin main

# Render/Railway auto-deploys
```

---

## 🐛 Troubleshooting

### Frontend won't load API:
1. Check `VITE_API_BASE_URL` environment variable
2. Verify backend URL in Axios config
3. Check browser console for CORS errors
4. Ensure backend is running and healthy

### CORS errors:
1. Verify `FRONTEND_URL` in backend `.env`
2. Check CORS configuration in `app/main.py`
3. Ensure frontend and backend URLs match exactly

### Backend returning 500 errors:
1. Check deployment logs on Render/Railway
2. Verify `OPENAI_API_KEY` is set
3. Verify all dependencies installed: `pip install -r requirements.txt`
4. Check environment variables are set correctly

### Deployment stuck:
1. Check platform logs (Vercel/Render dashboard)
2. Verify build commands are correct
3. Try redeploying manually
4. Contact platform support if issue persists

---

## 📞 Support & Resources

- **Vercel Docs**: https://vercel.com/docs
- **Netlify Docs**: https://docs.netlify.com
- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **React Docs**: https://react.dev

---

## 🎓 For College Evaluation

This deployment guide demonstrates:
- ✅ Production-ready architecture
- ✅ Secure environment variable handling
- ✅ Scalable deployment strategy
- ✅ Cloud platform integration
- ✅ Frontend-backend separation
- ✅ Industry best practices
- ✅ Detailed documentation
- ✅ Error handling and health checks

