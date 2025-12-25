import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# 1. 프로젝트 루트 경로를 시스템 경로에 추가
# Gunicorn 실행 위치에 상관없이 프로젝트 모듈(mypjt)을 찾을 수 있게 합니다.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# 2. .env 파일의 환경변수를 로드 (python-dotenv 설치 필요)
# Gunicorn 프로세스가 쉘의 환경변수를 읽지 못하는 문제를 해결합니다.
try:
    import dotenv
    dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))
except ImportError:
    # 로컬 환경이나 dotenv가 설치되지 않은 경우를 대비한 예외 처리
    pass

# 3. Django 설정 파일 위치 지정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypjt.settings')

# 4. WSGI 애플리케이션 생성
application = get_wsgi_application()