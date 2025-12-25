#!/bin/bash
# Gunicorn systemd 서비스 설정 스크립트

echo "🚀 Gunicorn systemd 서비스 설정 시작..."

# 1. 서비스 파일 복사
echo "📝 서비스 파일 복사 중..."
sudo cp gunicorn.service /etc/systemd/system/

# 2. systemd 데몬 리로드
echo "🔄 systemd 데몬 리로드..."
sudo systemctl daemon-reload

# 3. 서비스 활성화 (부팅 시 자동 시작)
echo "✅ 서비스 활성화..."
sudo systemctl enable gunicorn

# 4. 서비스 시작
echo "▶️  서비스 시작..."
sudo systemctl start gunicorn

# 5. 상태 확인
echo ""
echo "📊 서비스 상태:"
sudo systemctl status gunicorn

echo ""
echo "✅ 설정 완료!"
echo ""
echo "유용한 명령어:"
echo "  sudo systemctl start gunicorn     # 시작"
echo "  sudo systemctl stop gunicorn      # 중지"
echo "  sudo systemctl restart gunicorn   # 재시작"
echo "  sudo systemctl status gunicorn    # 상태 확인"
echo "  sudo journalctl -u gunicorn -f    # 로그 보기"
