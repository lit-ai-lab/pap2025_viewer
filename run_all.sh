#!/bin/bash

#echo "📦 [1] 프론트엔드 빌드 시작"
#cd frontend/FE

# Node 모듈 설치 (처음 한 번만 설치되게 조건 처리 가능)
#if [ ! -d "node_modules" ]; then
#  echo "📦 npm install 실행 중..."
#  npm install
#fi

# Vite 빌드
#echo "⚙️ npm run build 실행 중..."
#npm run build

# 빌드 완료 후 루트로 돌아감
#cd ../..

echo "🚀 FastAPI 서버 시작 (포트 8000)"
uvicorn main:app --host 0.0.0.0 
