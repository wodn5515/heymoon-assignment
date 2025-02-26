# 기술과제
사전과제입니다.

# 프로젝트 소개
## ⚙️ 개발 환경
- **Language**: Python 3.11.4
- **Database**:
  - PostgreSQL 15.12
- **Framework**: Django 4.2.9
- Docker 20.10.12

## ▶️ Installation

    $ git clone https://github.com/wodn5515/heymoon-assignment.git

### 환경변수 설정
    # DB
    POSTGRES_DB_NAME="heymoon"
    POSTGRES_DB_USER="heymoon"
    POSTGRES_DB_PASSWORD="heymoon"
    POSTGRES_DB_HOST="postgres"
    POSTGRES_DB_PORT="5432"

    # Django
    DJANGO_SECRET_KEY="" # django 시크릿 키
    DJANGO_SETTINGS_MODULE="config.settings.local"


### 도커 실행

    $ docker compose -f docker-compose.yml up --build

### API 테스트용 admin 유저 생성

    $ python manage.py creastesuperuser

# 📒 API 명세

- [유저 API](#user)
  - [회원가입](#signup)
  - [로그인](#login)
  - [토큰 재발급](#refresh)
  - [로그아웃](#logout)
- [대시보드 API](#dashboard)
  - [실시간 매출 데이터 조회](#live_sales)
  - [기간 내 제품 판매 추이 조회](#sales_chart)

<a name="user"></a>
## 📌유저 API
<a name="signup"></a>
### 📍회원가입

    POST /api/users/signup

**Request**
- Body
```json
{
  "email": "로그인에 사용할 email (unique)",
  "name": "이름",
  "password": "비밀번호",
  "password_check": "비밀번호 확인용 재입력"
}
```
**Response**
- Success<br>
  STATUS_CODE: 201
  ```json
  {
    "id": 0,
    "name": "str",
    "email": "example@email.com",
    "is_active": true,
    "is_staff": false,
    "is_superuser": false
  }
  ```
- Error
  - 이미 가입한 이메일
  ```json
  {
      "status": 400,
      "code": "ALREADY_SIGNED_UP_EMAIL",
      "detail": "이미 가입된 이메일입니다."
  }
  ```
  - 비밀번호와 비밀번호검사 값이 다른경우
  ```json
  {
      "status": 400,
      "code": "PASSWORD_NOT_MATCHED",
      "detail": "비밀번호가 서로 다릅니다"
  }
  ```
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
---
<a name="login"></a>
### 📍로그인

    POST /api/users/login

**Request**
- Body
```json
{
    "email": "회원가입시 입력했던 email",
    "password": "회원가입시 입력했던 password"
}
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "user": {
        "id": 0,
        "name": "str",
        "email": "example@email.com",
        "is_active": true,
        "is_staff": false,
        "is_superuser": false
    },
    "token": {
        "refresh": "str(refresh_token)",
        "access": "str(access_token)"
    }
  }
  ```
- Error
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - 입력된 데이터로 가입된 회원이 없는경우
  ```json
  {
    "status": 401,
    "code": "AUTHENTICATED_FAILED",
    "detail": "이메일 또는 비밀번호가 올바르지 않습니다."
  }
  ```
---
<a name="refresh"></a>
### 📍토큰 재발급

    POST /api/users/refresh

**Request**
- Body
```json
{
    "refresh": "str(refresh_token)"
}
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "access": "str(access_token)"
  }
  ```
- Error
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - refresh_token이 유효하지 않은 경우
  ```json
  {
    "status": 401,
    "code": "TOKEN_IS_INVALID_OR_EXPIRED",
    "detail": "인증정보가 유효하지 않습니다. 새롭게 로그인 해주세요."
  }
  ```
---
<a name="logout"></a>
### 📍로그아웃

    POST /api/users/login

**Request**
- Header
```json
{
  "Authorization": "str(Bearer access_token)"
}
```
- Body
```json
{
  "refresh": "str(refresh_token)"
}
```
**Response**
- Success<br>
  STATUS_CODE: 204
  ```
  ```
- Error
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - refresh_token이 유효하지 않은 경우
  ```json
  {
    "status": 401,
    "code": "TOKEN_IS_INVALID_OR_EXPIRED",
    "detail": "인증정보가 유효하지 않습니다. 새롭게 로그인 해주세요."
  }
  ```
  - access token 로그인 실패시
  ```json
  {
    "status": 401,
    "code": "NOT_AUTHENTICATED",
    "detail": "로그인이 필요합니다."
  }
  ```
---
<a name="dashboard"></a>
## 📌대시보드 API
<a name="live_sales"></a>
### 📍실시간 매출 데이터 조회

    GET /api/dashboards/live-sales

**Request**
- Header
```json
{
  "Authorization": "str(Bearer access_token)"
}
```
- Params
```
start-date: "str(datetime)"
end-date: "str(datetime)"
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "results": [
      "datetime": "str(datetime)",
      "total_amount": 0,
      "customer_count": 0,
      "coupon_amount": 0,
      "first_purchase_count": 0,
      "first_purchase_amount": 0
    ]
  }
  ```
- Error
  - access token 로그인 실패시
  ```json
  {
    "status": 401,
    "code": "NOT_AUTHENTICATED",
    "detail": "로그인이 필요합니다."
  }
  ```
  - 권한이 없는 경우
  ```json
  {
    "status": 403,
    "code": "PERMISSION_DENIED",
    "detail": "권한이 없습니다."
  }
  ```
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - 시작일이 종료일보다 늦을 경우
  ```json
  {
    "status": 400,
    "code": "INVALID_DATE_RANGE",
    "detail": "시작일이 종료일보다 늦을 수 없습니다."
  }
  ```
---
<a name="sales_chart"></a>
### 📍기간 내 제품 판매 추이 조회

    GET /api/dashboards/sales-chart

**Request**
- Header
```json
{
  "Authorization": "str(Bearer access_token)"
}
```
- Params
```
start-date: "str(datetime)"
end-date: "str(datetime)"
```
**Response**
- Success<br>
  STATUS_CODE: 200
  ```json
  {
    "results": [
        {
            "product_name": "str",
            "total_amount": 0,
            "quantity": 0
        }
    ]
  }
  ```
- Error
  - access token 로그인 실패시
  ```json
  {
    "status": 401,
    "code": "NOT_AUTHENTICATED",
    "detail": "로그인이 필요합니다."
  }
  ```
  - 권한이 없는 경우
  ```json
  {
    "status": 403,
    "code": "PERMISSION_DENIED",
    "detail": "권한이 없습니다."
  }
  ```
  - 입력값 validation 실패시
  ```json
  {
    "status": 400,
    "code": "INPUT_VALIDATION_ERROR",
    "detail": "유효하지않은 입력입니다."
  }
  ```
  - 시작일이 종료일보다 늦을 경우
  ```json
  {
    "status": 400,
    "code": "INVALID_DATE_RANGE",
    "detail": "시작일이 종료일보다 늦을 수 없습니다."
  }
  ```
---
