# seoeunjin.com 마이크로서비스 아키텍처 전략

## 📋 목차
1. [아키텍처 개요](#아키텍처-개요)
2. [도메인별 구조](#도메인별-구조)
3. [마이그레이션 전략](#마이그레이션-전략)
4. [디렉토리 구조](#디렉토리-구조)
5. [배포 전략](#배포-전략)

---

## 🏗️ 아키텍처 개요

### 핵심 원칙
```
api.seoeunjin.com = Gateway + Security (인증/인가 전용)
├─ 모든 요청의 진입점
├─ JWT 토큰 검증
├─ OAuth 인증 (Kakao, Google, Naver)
└─ 라우팅만 담당 (비즈니스 로직 없음)

↓ 라우팅 ↓

core.seoeunjin.com = 비즈니스 로직 (마이크로서비스)
├─ 모든 비즈니스 로직
├─ 도메인별 서비스 분리
└─ DB 접근 및 데이터 처리

ai.seoeunjin.com = AI/ML/크롤링 서비스
├─ AI 모델 서빙
├─ 크롤링 서비스
└─ 데이터 파이프라인

www.seoeunjin.com = 사용자 프론트엔드 (Next.js)
└─ Vercel 배포

admin.seoeunjin.com = 관리자 프론트엔드 (Next.js)
└─ Vercel 배포
```

---

## 🎯 도메인별 구조

### 1. api.seoeunjin.com (Gateway + Security)

**역할**: 인증/인가 + 라우팅 전용
- ✅ JWT 토큰 생성/검증
- ✅ OAuth 인증 (Kakao, Google, Naver)
- ✅ API Gateway 라우팅
- ✅ Rate Limiting
- ✅ CORS 처리
- ❌ 비즈니스 로직 없음
- ❌ DB 직접 접근 없음

```
api.seoeunjin.com/
├── gateway/                    # Spring Cloud Gateway
│   ├── src/main/java/
│   │   └── com/seoeunjin/gateway/
│   │       ├── config/
│   │       │   ├── SecurityConfig.java
│   │       │   ├── GatewayConfig.java
│   │       │   └── CorsConfig.java
│   │       ├── filter/
│   │       │   ├── JwtAuthenticationFilter.java
│   │       │   └── LoggingFilter.java
│   │       └── GatewayApplication.java
│   └── Dockerfile
│
├── security/                   # Spring Security + OAuth
│   ├── src/main/java/
│   │   └── com/seoeunjin/security/
│   │       ├── oauth/
│   │       │   ├── KakaoOAuthService.java
│   │       │   ├── GoogleOAuthService.java
│   │       │   └── NaverOAuthService.java
│   │       ├── jwt/
│   │       │   ├── JwtTokenProvider.java
│   │       │   ├── JwtUtil.java
│   │       │   └── JwtProperties.java
│   │       ├── controller/
│   │       │   └── AuthController.java
│   │       └── SecurityApplication.java
│   └── Dockerfile
│
└── .env

# 라우팅 규칙 예시 (application.yaml)
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://core.seoeunjin.com
          predicates:
            - Path=/api/users/**
          filters:
            - JwtAuthenticationFilter
        
        - id: product-service
          uri: lb://core.seoeunjin.com
          predicates:
            - Path=/api/products/**
          filters:
            - JwtAuthenticationFilter
        
        - id: ai-service
          uri: lb://ai.seoeunjin.com
          predicates:
            - Path=/api/ai/**
```

---

### 2. core.seoeunjin.com (비즈니스 로직)

**역할**: 모든 비즈니스 로직 처리
- ✅ 도메인별 마이크로서비스
- ✅ DB 접근 및 데이터 처리
- ✅ 비즈니스 규칙 구현
- ✅ 이벤트 발행/구독

```
core.seoeunjin.com/
├── userservice/               # 사용자 관리
│   ├── src/main/java/
│   │   └── com/seoeunjin/user/
│   │       ├── controller/
│   │       │   └── UserController.java
│   │       ├── service/
│   │       │   └── UserService.java
│   │       ├── repository/
│   │       │   └── UserRepository.java
│   │       ├── domain/
│   │       │   └── User.java
│   │       └── UserServiceApplication.java
│   ├── Dockerfile
│   └── build.gradle
│
├── productservice/            # 상품 관리
│   ├── src/main/java/
│   │   └── com/seoeunjin/product/
│   │       ├── controller/
│   │       ├── service/
│   │       ├── repository/
│   │       └── domain/
│   ├── Dockerfile
│   └── build.gradle
│
├── orderservice/              # 주문 관리
│   ├── src/main/java/
│   │   └── com/seoeunjin/order/
│   │       ├── controller/
│   │       ├── service/
│   │       ├── repository/
│   │       └── domain/
│   ├── Dockerfile
│   └── build.gradle
│
├── paymentservice/            # 결제 관리
│   ├── src/main/java/
│   │   └── com/seoeunjin/payment/
│   ├── Dockerfile
│   └── build.gradle
│
├── notificationservice/       # 알림 서비스
│   ├── src/main/java/
│   │   └── com/seoeunjin/notification/
│   ├── Dockerfile
│   └── build.gradle
│
└── .env
```

---

### 3. ai.seoeunjin.com (AI/ML/크롤링)

**역할**: AI/ML 모델 서빙 및 크롤링
- ✅ AI 모델 추론
- ✅ 크롤링 서비스
- ✅ 데이터 파이프라인
- ✅ 배치 작업

```
ai.seoeunjin.com/
├── gateway/                   # FastAPI Gateway
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── services/
│   ├── crawlerservice/       # 크롤링 서비스
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── bs_demo/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── chatbotservice/       # 챗봇 AI 서비스
│   │   ├── app/
│   │   │   └── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── recommendservice/     # 추천 시스템
│   │   ├── app/
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── analyticsservice/     # 데이터 분석
│       ├── app/
│       ├── requirements.txt
│       └── Dockerfile
│
└── .env
```

---

### 4. www.seoeunjin.com (사용자 프론트엔드)

**역할**: 사용자용 웹 인터페이스
- ✅ Next.js 14+ (App Router)
- ✅ Vercel 배포
- ✅ SSR/SSG/ISR
- ✅ SEO 최적화

```
www.seoeunjin.com/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   ├── register/
│   │   └── oauth-callback/
│   ├── (main)/
│   │   ├── products/
│   │   ├── orders/
│   │   └── profile/
│   ├── layout.tsx
│   └── page.tsx
│
├── components/
├── lib/
│   └── api-client.ts         # api.seoeunjin.com 호출
├── public/
└── package.json
```

---

### 5. admin.seoeunjin.com (관리자 프론트엔드)

**역할**: 관리자용 대시보드
- ✅ Next.js 14+ (App Router)
- ✅ Vercel 배포
- ✅ 관리자 전용 UI

```
admin.seoeunjin.com/
├── app/
│   ├── dashboard/
│   ├── users/
│   ├── products/
│   ├── orders/
│   └── analytics/
│
├── components/
├── lib/
│   └── api-client.ts         # api.seoeunjin.com 호출
└── package.json
```

---

## 🚀 마이그레이션 전략

### Phase 1: 현재 상태 정리 (완료)
✅ 기존 `api.seoeunjin.com/services/authservice` → `core.seoeunjin.com/oauthservice`로 이동
✅ 기존 `api.seoeunjin.com/services/userservice` → `core.seoeunjin.com/userservice`로 이동
✅ `docker-compose.local.yaml` 통합 완료

### Phase 2: 디렉토리 재구성 (진행 예정)
```bash
# 1단계: core.seoeunjin.com 디렉토리 생성
mkdir core.seoeunjin.com

# 2단계: userservice 이동
mv api.seoeunjin.com/services/userservice core.seoeunjin.com/userservice

# 3단계: authservice를 oauthservice로 리팩토링
# api.seoeunjin.com/services/authservice → core.seoeunjin.com/oauthservice
# (OAuth 인증만 담당, 사용자 비즈니스 로직은 core.seoeunjin.com/userservice로)

# 4단계: 새로운 비즈니스 서비스 추가
# core.seoeunjin.com/productservice
# core.seoeunjin.com/orderservice
# 등등...
```

### Phase 3: API Gateway 라우팅 설정
```yaml
# api.seoeunjin.com/gateway/src/main/resources/application.yaml
spring:
  cloud:
    gateway:
      routes:
        # core.seoeunjin.com 라우팅
        - id: user-service
          uri: http://core.seoeunjin.com:8082
          predicates:
            - Path=/api/users/**
          
        - id: product-service
          uri: http://core.seoeunjin.com:8083
          predicates:
            - Path=/api/products/**
        
        # ai.seoeunjin.com 라우팅
        - id: ai-gateway
          uri: http://ai.seoeunjin.com:8000
          predicates:
            - Path=/api/ai/**
```

### Phase 4: docker-compose.local.yaml 재구성
```yaml
services:
  # ===== API Gateway =====
  gateway:
    build: ./api.seoeunjin.com/gateway
    ports: ["8080:8080"]
    profiles: ["api"]
  
  security:
    build: ./api.seoeunjin.com/security
    ports: ["8081:8081"]
    profiles: ["api"]
  
  # ===== Service Layer =====
  userservice:
    build: ./core.seoeunjin.com/userservice
    ports: ["8082:8082"]
    profiles: ["service"]
  
  productservice:
    build: ./core.seoeunjin.com/productservice
    ports: ["8083:8083"]
    profiles: ["service"]
  
  # ===== AI Layer =====
  ai-gateway:
    build: ./ai.seoeunjin.com
    ports: ["8000:9000"]
    profiles: ["ai"]
  
  crawlerservice:
    build: ./ai.seoeunjin.com/crawlerservice
    ports: ["9001:9001"]
    profiles: ["ai"]
  
  # ===== Infrastructure =====
  redis:
    image: redis:7-alpine
    profiles: ["infra"]
  
  postgres:
    image: postgres:15-alpine
    profiles: ["infra"]
```

---

## 📂 최종 디렉토리 구조

```
seoeunjin.COM/
│
├── api.seoeunjin.com/           # Gateway + Security
│   ├── gateway/               # Spring Cloud Gateway (8080)
│   ├── security/              # OAuth + JWT (8081)
│   └── .env
│
├── core.seoeunjin.com/       # 비즈니스 로직 (마이크로서비스)
│   ├── userservice/           # 사용자 관리 (8082)
│   ├── productservice/        # 상품 관리 (8083)
│   ├── orderservice/          # 주문 관리 (8084)
│   ├── paymentservice/        # 결제 관리 (8085)
│   ├── notificationservice/   # 알림 서비스 (8086)
│   └── .env
│
├── ai.seoeunjin.com/            # AI/ML/크롤링
│   ├── gateway/               # FastAPI Gateway (8000)
│   └── services/
│       ├── crawlerservice/    # 크롤링 (9001)
│       ├── chatbotservice/    # 챗봇 AI (9002)
│       ├── recommendservice/  # 추천 시스템 (9003)
│       └── analyticsservice/  # 데이터 분석 (9004)
│
├── www.seoeunjin.com/           # 사용자 프론트엔드 (Next.js → Vercel)
│
├── admin.seoeunjin.com/         # 관리자 프론트엔드 (Next.js → Vercel)
│
├── docker-compose.local.yaml  # 로컬 개발용 통합 설정
└── ARCHITECTURE_STRATEGY.md   # 이 문서
```

---

## 🎯 배포 전략

### Railway 배포 (백엔드)
```
api.seoeunjin.com
├── gateway (Railway Service #1)
└── security (Railway Service #2)

core.seoeunjin.com
├── userservice (Railway Service #3)
├── productservice (Railway Service #4)
└── ... (각각 독립 서비스로 배포)

ai.seoeunjin.com
├── ai-gateway (Railway Service #N)
└── crawlerservice (Railway Service #N+1)
```

### Vercel 배포 (프론트엔드)
```
www.seoeunjin.com → Vercel Project #1
admin.seoeunjin.com → Vercel Project #2
```

---

## 🔐 보안 흐름

```
사용자 요청
    ↓
[www.seoeunjin.com] (Next.js - Vercel)
    ↓ HTTP Request
[api.seoeunjin.com/gateway] (Port 8080)
    ↓ JWT 검증
[api.seoeunjin.com/security] (Port 8081)
    ↓ 인증 완료
[api.seoeunjin.com/gateway] 라우팅
    ↓
[core.seoeunjin.com/*] 비즈니스 로직 처리
    ↓
응답 반환
```

---

## 📊 통신 흐름 예시

### 사용자 로그인 흐름
```
1. www.seoeunjin.com
   └─> POST /api/auth/kakao/login
       └─> api.seoeunjin.com/gateway:8080
           └─> api.seoeunjin.com/security:8081 (OAuth 처리)
               └─> JWT 토큰 생성
                   └─> Redis에 Refresh Token 저장
                       └─> 응답 반환
```

### 사용자 정보 조회 흐름
```
1. www.seoeunjin.com
   └─> GET /api/users/me (with JWT in header)
       └─> api.seoeunjin.com/gateway:8080
           └─> JWT 검증
               └─> core.seoeunjin.com/userservice:8082
                   └─> DB에서 사용자 정보 조회
                       └─> 응답 반환
```

### AI 서비스 호출 흐름
```
1. www.seoeunjin.com
   └─> POST /api/ai/chatbot (with JWT)
       └─> api.seoeunjin.com/gateway:8080
           └─> JWT 검증
               └─> ai.seoeunjin.com/gateway:8000
                   └─> ai.seoeunjin.com/chatbotservice:9002
                       └─> AI 모델 추론
                           └─> 응답 반환
```

---

## 🎓 핵심 원칙 요약

1. **api.seoeunjin.com = Gateway + Security만**
   - 비즈니스 로직 금지
   - 인증/인가 + 라우팅만

2. **core.seoeunjin.com = 모든 비즈니스 로직**
   - 도메인별 마이크로서비스
   - DB 접근 및 데이터 처리

3. **ai.seoeunjin.com = AI/ML 전용**
   - AI 모델 서빙
   - 크롤링 및 데이터 파이프라인

4. **프론트엔드 분리**
   - www.seoeunjin.com (사용자용)
   - admin.seoeunjin.com (관리자용)
   - 둘 다 Vercel 배포

5. **마이크로서비스 원칙**
   - 서비스간 느슨한 결합
   - 각 서비스는 독립적으로 배포 가능
   - API Gateway를 통한 중앙 집중식 라우팅

---

## 🚦 다음 단계

### 즉시 진행
1. `core.seoeunjin.com` 디렉토리 생성
2. `api.seoeunjin.com/services/userservice` → `core.seoeunjin.com/userservice` 이동
3. `api.seoeunjin.com/services/authservice` → `core.seoeunjin.com/oauthservice`로 리팩토링
4. `docker-compose.local.yaml` 업데이트

### 단계적 진행
1. 새로운 비즈니스 서비스는 `core.seoeunjin.com/` 아래에 생성
2. 기존 서비스는 점진적으로 마이그레이션
3. Railway 배포 시 각 서비스를 독립적으로 배포
4. 모니터링 및 로깅 시스템 구축

---

**작성일**: 2025-12-02
**버전**: 1.0.0


