@echo off
echo 🚀 ATS Resume Optimizer - Deployment Script
echo ==========================================

REM Check if git is initialized
if not exist ".git" (
    echo 📦 Initializing Git repository...
    git init
)

REM Add all files
echo 📁 Adding files to Git...
git add .

REM Commit changes
echo 💾 Committing changes...
git commit -m "Deploy ATS Resume Optimizer - Production Ready"

echo.
echo 🎯 Choose your deployment platform:
echo 1. Heroku (Recommended)
echo 2. Railway
echo 3. Render
echo 4. Manual deployment
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 🚀 Deploying to Heroku...
    echo Make sure you have:
    echo 1. Heroku CLI installed
    echo 2. Heroku account created
    echo 3. OpenAI API key ready
    echo.
    pause
    
    echo Creating Heroku app...
    heroku create
    
    echo Setting environment variables...
    set /p openai_key="Enter your OpenAI API key: "
    heroku config:set OPENAI_API_KEY=%openai_key%
    heroku config:set OPENAI_MODEL=gpt-4o-mini
    
    echo Deploying to Heroku...
    git push heroku main
    
    echo ✅ Deployment complete!
    echo Your app is now live on Heroku!
) else if "%choice%"=="2" (
    echo 🚀 Deploying to Railway...
    echo 1. Push to GitHub first:
    echo    git remote add origin ^<your-github-repo-url^>
    echo    git push -u origin main
    echo 2. Connect to Railway dashboard
    echo 3. Set environment variables in Railway
) else if "%choice%"=="3" (
    echo 🚀 Deploying to Render...
    echo 1. Push to GitHub first:
    echo    git remote add origin ^<your-github-repo-url^>
    echo    git push -u origin main
    echo 2. Connect to Render dashboard
    echo 3. Set environment variables in Render
) else if "%choice%"=="4" (
    echo 📋 Manual deployment steps:
    echo 1. Push to GitHub:
    echo    git remote add origin ^<your-github-repo-url^>
    echo    git push -u origin main
    echo 2. Choose a platform and follow DEPLOYMENT.md
) else (
    echo ❌ Invalid choice. Please run the script again.
)

echo.
echo 🎉 Deployment process initiated!
echo Check DEPLOYMENT.md for detailed instructions.
pause
