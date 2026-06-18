@echo off
REM Quick start script for Docker Compose on Windows

echo 🐳 Proiect Backend - Docker Quick Start
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop.
    exit /b 1
)

echo ✓ Docker found
echo.

REM Ask user what they want to do
echo What would you like to do?
echo 1) Start containers ^(docker-compose up^)
echo 2) Stop containers ^(docker-compose down^)
echo 3) View logs
echo 4) Access database shell
echo 5) Full rebuild
echo 6) Clean everything ^(remove volumes^)
echo.

set /p option="Choose option (1-6): "

if "%option%"=="1" (
    echo 🚀 Starting containers...
    docker-compose up -d
    echo ✓ Containers started!
    echo.
    echo API available at: http://localhost:8000
    echo API docs at: http://localhost:8000/docs
    echo.
    echo View logs with: docker-compose logs -f
) else if "%option%"=="2" (
    echo 🛑 Stopping containers...
    docker-compose down
    echo ✓ Containers stopped!
) else if "%option%"=="3" (
    echo 📋 Showing logs ^(press Ctrl+C to exit^)...
    docker-compose logs -f
) else if "%option%"=="4" (
    echo 🗄️  Connecting to database...
    docker-compose exec db psql -U proiect_user -d proiect_db
) else if "%option%"=="5" (
    echo 🔨 Full rebuild...
    docker-compose down -v
    docker-compose build --no-cache
    docker-compose up -d
    echo ✓ Rebuild complete!
    echo.
    echo API available at: http://localhost:8000
) else if "%option%"=="6" (
    echo 🧹 Cleaning up everything...
    docker-compose down -v
    docker image prune -a --force
    docker volume prune --force
    echo ✓ Cleanup complete!
) else (
    echo ❌ Invalid option
    exit /b 1
)
