#!/bin/bash
# setup-local.sh
# 로컬 개발 환경 초기 세팅: _shared → khfamily symlink 생성
# (CI에서는 actions/checkout으로 _shared/ 직접 checkout)

set -e

KHFAMILY=~/Labs/khfamily/Public/khfamily.github.io

if [ ! -d "$KHFAMILY" ]; then
  echo "❌ khfamily repo 없음: $KHFAMILY"
  exit 1
fi

# _shared symlink 생성 (이미 있으면 덮어씀)
ln -sf "$KHFAMILY" ./_shared

echo "✅ _shared → $KHFAMILY"
echo "   src, scripts, main.py, tests 심볼릭 링크 활성화됨"
