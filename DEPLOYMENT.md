# 🚀 Deployment Guide - ATS Resume Optimizer

This guide will help you deploy your React + FastAPI resume optimization system for free.

## 🌐 Free Deployment Options

### Option 1: Heroku (Recommended)

**Backend (FastAPI) + Frontend (React)**

1. **Create Heroku Account**
   - Go to [heroku.com](https://heroku.com)
   - Sign up for free account

2. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   # Or use package manager:
   # Windows: choco install heroku-cli
   # Mac: brew install heroku/brew/heroku
   ```

3. **Login to Heroku**
   ```bash
   heroku login
   ```

4. **Create Heroku App**
   ```bash
   heroku create your-resume-optimizer
   ```

5. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-openai-api-key-here
   heroku config:set OPENAI_MODEL=gpt-4o-mini
   ```

6. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

### Option 2: Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Connect Repository**
   - Connect your GitHub repository
   - Railway will auto-detect the project

3. **Set Environment Variables**
   - Add `OPENAI_API_KEY` in Railway dashboard
   - Add `OPENAI_MODEL=gpt-4o-mini`

4. **Deploy**
   - Railway will automatically deploy
   - Get your live URL

### Option 3: Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for free

2. **Create Web Service**
   - Connect your GitHub repository
   - Choose "Web Service"

3. **Configure**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python api_server.py`
   - Add environment variables

4. **Deploy**
   - Render will build and deploy automatically

## 🔧 Environment Variables

Set these in your deployment platform:

```bash
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

## 📁 Project Structure (Cleaned)

```
resume_react/
├── api_server.py           # FastAPI backend
├── Procfile               # Heroku deployment config
├── runtime.txt           # Python version
├── requirements.txt      # Python dependencies
├── package.json         # React dependencies
├── tailwind.config.js   # Tailwind CSS config
├── public/              # React public assets
├── src/                 # React source code
├── crew_app/           # AI processing backend
└── README.md           # Project documentation
```

## 🚀 Quick Deploy Commands

### For Heroku:
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit"

# Create and deploy to Heroku
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

### For Railway:
```bash
# Just push to GitHub, then connect in Railway dashboard
git push origin main
```

## 🌍 Live URLs

After deployment, you'll get:
- **Backend API**: `https://your-app-name.herokuapp.com`
- **Frontend**: `https://your-app-name.herokuapp.com` (if serving React from same domain)

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check Python version in `runtime.txt`
   - Verify all dependencies in `requirements.txt`

2. **API Key Issues**
   - Ensure `OPENAI_API_KEY` is set correctly
   - Check API key has sufficient credits

3. **CORS Errors**
   - Backend CORS is configured for `localhost:3000`
   - Update CORS settings for production domain

## 📊 Monitoring

- **Heroku**: Use Heroku dashboard for logs
- **Railway**: Built-in monitoring dashboard
- **Render**: Logs available in dashboard

## 💰 Cost

All recommended platforms offer:
- **Free tier** with limited hours
- **Automatic scaling**
- **Easy upgrades** when needed

## 🎯 Next Steps

1. Choose your deployment platform
2. Set up environment variables
3. Deploy your application
4. Test the live application
5. Share your resume optimizer with the world!

---

**Ready to deploy? Choose your platform and follow the steps above!** 🚀
