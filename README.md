# 복권 웹사이트 프로젝트

## 프로젝트 개요

본 프로젝트는 Django와 Docker를 기반으로 구축된 온라인 복권 웹사이트로, 사용자 회원가입, 복권 구매, 추첨 관리 등의 기능을 제공합니다.

## 기능 특징

### 사용자 기능
- 사용자 회원가입 및 로그인
- 계정 충전
- 복권 구매 (수동 번호 선택 및 자동 선택)
- 구매 이력 조회
- 당첨 조회 및 상금 교환
- 개인 프로필 관리

### 관리자 기능
- 복권 유형 관리
- 추첨 회차 관리
- 추첨 작업 실행
- 판매 통계 보고서
- 사용자 관리
- 당첨 확인

### 시스템 특징
- 반응형 웹 인터페이스
- 안전한 사용자 인증
- 자동 당첨 검출
- 거래 기록 추적
- Docker 컨테이너화 배포

## 기술 스택

- **백엔드 프레임워크**: Django 3.2.25
- **데이터베이스**: PostgreSQL (운영 환경) / SQLite (개발 환경)
- **프론트엔드**: Bootstrap 5 + HTML/CSS/JavaScript
- **컨테이너화**: Docker + Docker Compose
- **Python 버전**: 3.7+

## 프로젝트 구조

```
lottery_project/
├── accounts/              # 사용자 계정 애플리케이션
├── lottery/               # 복권 핵심 기능
├── management/            # 관리자 기능
├── templates/             # HTML 템플릿
├── static/                # 정적 파일
├── lottery_project/       # 프로젝트 설정
├── requirements.txt       # Python 의존성
├── Dockerfile            # Docker 이미지 설정
├── docker-compose.yml    # Docker 오케스트레이션 설정
└── manage.py             # Django 관리 스크립트
```

## 설치 및 실행

### 방법1: Docker 배포 (권장)

1. Docker와 Docker Compose가 설치되어 있는지 확인

2. 프로젝트 클론
```bash
git clone <repository-url>
cd lottery_project
```

3. 서비스 시작
```bash
docker-compose up -d
```

4. 웹사이트 접속
```
http://localhost:8000
```

### 방법2: 로컬 개발

1. Python 의존성 설치
```bash
pip install -r requirements.txt
```

2. 데이터베이스 마이그레이션 실행
```bash
python manage.py migrate
```

3. 테스트 데이터 초기화
```bash
python manage.py init_data
```

4. 개발 서버 시작
```bash
python manage.py runserver
```

## 기본 계정

시스템 초기화 후 다음 테스트 계정이 생성됩니다:

- **관리자 계정**: 
  - 사용자명: admin
  - 비밀번호: admin123
  - 권한: 관리자 권한, 관리 백엔드 접근 가능

- **테스트 사용자**: 
  - 사용자명: testuser
  - 비밀번호: test123
  - 잔액: 500원

## 데이터 모델

### 핵심 모델

1. **LotteryType** - 복권 유형
   - 복권 이름, 설명, 가격
   - 번호 선택 규칙 (번호 범위, 선택 수량)

2. **LotteryDraw** - 추첨 회차
   - 회차 번호, 추첨 시간
   - 당첨 번호, 추첨 상태

3. **LotteryTicket** - 복권
   - 사용자, 회차, 선택 번호
   - 당첨 상태, 상금 금액

4. **UserProfile** - 사용자 프로필
   - 계정 잔액, 소비 통계
   - 연락처 정보

5. **Transaction** - 거래 기록
   - 거래 유형, 금액, 설명
   - 타임스탬프

## API 인터페이스

### 사용자 관련
- `/accounts/register/` - 사용자 회원가입
- `/accounts/login/` - 사용자 로그인
- `/accounts/profile/` - 개인 센터
- `/accounts/recharge/` - 계정 충전

### 복권 관련
- `/` - 홈페이지
- `/lottery/` - 복권 홀
- `/purchase/<id>/` - 복권 구매
- `/my-tickets/` - 내 복권
- `/check-winnings/` - 당첨 확인
- `/draw-results/` - 추첨 결과

### 관리 기능
- `/management/` - 관리 백엔드
- `/management/draw-management/` - 추첨 관리
- `/management/conduct-draw/<id>/` - 추첨 실행
- `/management/sales-report/` - 판매 보고서

## 테스트

테스트 케이스 실행:
```bash
python manage.py test
```

테스트 커버리지:
- 모델 기능 테스트
- 뷰 기능 테스트
- 사용자 인증 테스트
- 복권 구매 프로세스 테스트
- 당첨 검출 테스트

## 배포 설명

### 운영 환경 배포

1. `docker-compose.yml`의 환경 변수 수정
2. 안전한 데이터베이스 비밀번호 설정
3. 도메인 및 SSL 인증서 구성
4. 운영 환경 설정 활성화

### 환경 변수

`.env` 파일 생성:
```
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@db:5432/lottery_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 보안 고려사항

- CSRF 보호 사용
- 비밀번호 해시 저장
- 사용자 권한 제어
- SQL 인젝션 방어
- XSS 공격 방어

## 기여

프로젝트 개선을 위한 Issue 및 Pull Request 제출을 환영합니다.

## 연락처

문의사항이 있으시면 프로젝트 관리자에게 연락해 주세요.
