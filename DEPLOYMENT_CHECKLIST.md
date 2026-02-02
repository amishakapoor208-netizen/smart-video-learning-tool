# Production Deployment Checklist

This file provides a quick reference for deploying the Smart Video Learning Tool to production.

## 📋 Pre-Deployment Checklist

### Backend Preparation
- [ ] All environment variables defined in `.env.example`
- [ ] `.env` file created locally (NOT committed to git)
- [ ] `OPENAI_API_KEY` obtained and ready
- [ ] Health check endpoint tested locally: `GET /`
- [ ] CORS configuration reviewed and matches frontend URL
- [ ] No hardcoded secrets in code
- [ ] Debug mode set to False in production env

### Frontend Preparation
- [ ] `.env.production` configured with production API URL
- [ ] Build tested locally: `npm run build`
- [ ] API client properly imports from `./api/client.js`
- [ ] No hardcoded API URLs in components
- [ ] Environment variables use `VITE_` prefix

### Repository
- [ ] `.env` files added to `.gitignore`
- [ ] No sensitive keys in git history
- [ ] All code committed and pushed to main branch
- [ ] Repository is public (for free tier deployments)

---

## 🚀 Deployment Steps (15 minutes)

### Step 1: Deploy Backend (5 minutes)

#### Using Render.com (Recommended for beginners):
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: `smart-video-learning-tool-api`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   ```
   OPENAI_API_KEY=sk-your-actual-key
   APP_ENV=production
   DEBUG=false
   FRONTEND_URL=https://[your-frontend-url]
   ```
7. Click "Create Web Service"
8. **Note backend URL** (e.g., https://your-api-name.onrender.com)

#### Using Railway.app (Alternative):
1. Go to https://railway.app
2. Create account and connect GitHub
3. New Project → Deploy from GitHub → Select repo
4. Railway auto-detects Python and creates service
5. Add environment variables in Variables tab
6. **Note backend URL** from deployment

---

### Step 2: Deploy Frontend (5 minutes)

#### Using Vercel (Recommended for beginners):
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add New..." → "Project"
4. Select your GitHub repository
5. Configure:
   - Framework: Vite
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Add Environment Variables:
   ```
   VITE_API_BASE_URL=https://your-backend-url.onrender.com
   VITE_APP_ENV=production
   ```
7. Click "Deploy"
8. **Note frontend URL** (e.g., https://your-app.vercel.app)

#### Using Netlify (Alternative):
1. Go to https://netlify.com
2. Connect GitHub account
3. Click "Add new site" → "Import an existing project"
4. Select your repository
5. Configure:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
6. Add Environment Variables:
   ```
   VITE_API_BASE_URL=https://your-backend-url.onrender.com
   VITE_APP_ENV=production
   ```
7. Deploy

---

### Step 3: Update Frontend with Backend URL (2 minutes)

After backend is deployed:
1. Get your backend URL from Render/Railway dashboard
2. Go to Vercel/Netlify Dashboard
3. Navigate to Environment Variables
4. Update `VITE_API_BASE_URL` with actual backend URL
5. Trigger redeployment (push a commit or redeploy button)

---

### Step 4: Test Production (3 minutes)

#### Test Backend:
```bash
curl https://your-backend-url.onrender.com/

# Should return:
# {
#   "status": "Backend running successfully",
#   "environment": "production",
#   "version": "0.1.0",
#   "message": "Smart Video Learning Tool API is active"
# }
```

#### Test Frontend:
1. Open `https://your-frontend.vercel.app`
2. Check browser console (F12) for errors
3. Verify page loads without CORS errors

#### Test API Communication:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Trigger any API calls
4. Verify requests go to production backend URL
5. Check for 200 status codes

---

## 🔗 Final Production URLs

After successful deployment:

```
Frontend:  https://your-frontend.vercel.app
Backend:   https://your-backend.onrender.com
API Docs:  https://your-backend.onrender.com/docs
Health:    https://your-backend.onrender.com/
```

Share these URLs for college evaluation.

---

## 🆘 Troubleshooting

### Frontend shows CORS error
- Verify backend URL in Vercel environment variables
- Ensure `FRONTEND_URL` in backend .env matches frontend URL
- Check backend CORS configuration in `app/main.py`
- Trigger frontend redeployment after backend is ready

### Backend returns 500 error
- Check Render/Railway logs for error details
- Verify `OPENAI_API_KEY` is set in environment variables
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Verify Python version is 3.8+ in deployment settings

### "cannot find module" errors
- Ensure `requirements.txt` includes all dependencies
- Check file paths are correct
- Verify root directory settings (backend vs root)

### Deployment stuck
- Check platform logs for build errors
- Verify build commands are correct
- Try manual redeployment
- Ensure git push to main completes

---

## 📊 What's Included

✅ Frontend with React + Vite + Tailwind
✅ Backend with FastAPI + Uvicorn
✅ Environment-aware configuration
✅ Production CORS setup
✅ Health check endpoints
✅ API documentation (Swagger UI)
✅ Deployment configurations (Vercel, Netlify, Render, Railway)
✅ Security best practices (no hardcoded secrets)
✅ Auto-deployment on git push
✅ Free tier support on all platforms

---

## 📈 Next Steps After Deployment

1. Share live URLs with evaluators
2. Test all endpoints via API documentation
3. Begin implementing Phase 1: API Integration
4. Add video processing endpoints
5. Integrate OpenAI API
6. Build frontend components

---

## 💡 Tips for Success

- **Start with backend deployment** - It takes longer and is independent
- **Test health endpoints first** - Ensures basic connectivity
- **Use environment variables** - Never hardcode secrets
- **Keep git clean** - Only push code, not .env files
- **Monitor logs** - Use platform dashboards to debug issues
- **Test thoroughly** - Verify each component before moving forward

---

**Time to Production: 15-20 minutes**
**Difficulty Level: Beginner-friendly**
**Cost: Free (using free tiers)**

Good luck! 🚀
