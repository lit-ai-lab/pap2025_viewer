# 1. 백엔드 실행
echo "🔧 백엔드 서버 실행 중..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# 2. 프론트엔드 실행
echo "🌐 프론트엔드 서버 실행 중..."
cd frontend/FE
npx vite --host --port 5173
