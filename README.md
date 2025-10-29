# 👷 AI기반 PPE 감지 시스템

## 1. 프로젝트 개요

작업장에서 **직원의 보호장비(PPE, Personal Protective Equipment) 착용 여부를 자동으로 감지하는 AI 기반 시스템**입니다.
이미지 분석과 대화형 AI 상담 기능을 결합해, 안전관리 효율성을 높이고 사고를 사전에 예방하는 것을 목표로 합니다.

### 🧩 문제 인식

현장 안전점검 시, 관리자는 매번 사진이나 CCTV 화면을 통해  
작업자가 **안전모, 조끼 등 보호장비를 올바르게 착용했는지 직접 확인**해야 합니다.  
이 과정은 시간과 인력이 많이 소요되며, 사람의 눈으로는 누락을 놓칠 수 있습니다.

### 👷🏻‍♀️ 주요 대상

- **안전점검이 필요한 산업 현장 근로자**
- 현장 안전 관리자 및 교육 담당자

### 💡 주요 기능

#### 1️⃣ **이미지 기반 PPE 착용 감지**

- 사용자가 현장 사진 또는 직원 이미지를 업로드하면,  
  AI가 자동으로 **보호구(안전모, 안전조끼 등) 착용 여부를 분석**합니다.
- 누락된 장비가 있을 경우, **즉시 알려주어 위험을 사전에 방지**합니다.

#### 2️⃣ **대화형 AI 안전 상담**

- 사용자는 자연어로 질문을 입력하여,  
  **PPE 규정 / 안전수칙 / 장비 선택 가이드** 등에 대한  
  답변을 **Azure OpenAI (GPT-4o)** 기반 AI로부터 실시간으로 받을 수 있습니다.

## 2. 프로젝트 구조

```plaintext
ppe_check/
├── PPE_Function/                 # Azure Function 코드
│   ├── ppe_chat/                 # 대화형 질문 함수
│   │   ├── __init__.py
│   │   └── function.json
│   └── ppe_check/                # 이미지 분석 함수
│       ├── __init__.py
│       └── function.json
├── .gitignore                    # 민감정보/캐시 제외 설정
├── app.py                        # Streamlit 메인 UI
├── requirements.txt              # 의존성 목록(필요한 패키지 목록)
├── startup.txt                   # Azure 실행 스크립트
└── README.md                     # 프로젝트 설명 파일

```

## 3. 아키텍처 다이어그램

| 구성요소                     | 역할                                               |
| :--------------------------- | :------------------------------------------------- |
| 💻 **Streamlit**             | 사용자 인터페이스(UI) – 이미지 업로드 및 결과 표시 |
| 🐍 **Python**                | PPE 분석 및 대화형 로직 처리                       |
| ⚙️ **Azure Functions**       | 백엔드 서버리스 환경 – Streamlit ↔ AI 모델 연결    |
| ☁️ **Azure OpenAI (GPT-4o)** | AI 모델 – 대화형 질의응답 및 분석 수행             |

## 4. 동작흐름

```plaintext
👤 사용자가 이미지 업로드 또는 질문 입력
        │
        ▼
💻 Streamlit (프론트엔드)
        │  사용자 입력을 수집하고 시각화
        ▼
⚙️ Azure Function (백엔드)
        │  입력 데이터를 처리 후 AI에 전달
        ▼
☁️ Azure OpenAI (GPT-4o)
        │  PPE 착용 분석 및 대화형 답변 생성
        ▼
💻 Streamlit
        │  결과를 실시간으로 화면에 표시
        ▼
✅ 사용자에게 피드백 및 상담 제공
```

## 5. 파일별 담당 역할

### 1️⃣ **app.py (프론트엔드/UI)**

- **Streamlit 기반 웹 UI**

  - 사용자가 **이미지 업로드** 또는 **질문 입력**
  - 버튼 클릭으로 기능 실행:  
    📸 **PPE 착용 분석**, 💬 **AI 상담 시작**

- **UI 구성 요소**

  - 파일 업로더, 텍스트 입력창, 실행 버튼, 결과 출력 영역
  - 결과창에 **PPE 누락 항목**, **AI 응답 텍스트** 표시

- **UX 기능**
  - `st.spinner()` 로딩 표시
  - `st.session_state`로 분석 상태 유지
  - 사용자 경험 중심의 인터랙티브 구성

### 2️⃣ **PPE_Function/** _(백엔드 / Azure Function)_

- **서버리스 백엔드 로직**

  - Streamlit에서 받은 입력을 처리하고, Azure OpenAI로 전달
  - 결과를 JSON 형태로 반환해 Streamlit이 표시 가능하게 함

- **구조**

  - `ppe_check/` → 이미지 분석 함수 (AI 모델 호출)
  - `ppe_chat/` → 대화형 상담 함수 (GPT-4o 응답 생성)

- **핵심 역할**
  - 요청 파라미터 검증
  - Azure OpenAI API 호출 및 결과 파싱
  - HTTP Trigger 기반 함수 실행

### 3️⃣ **requirements.txt (의존성 목록)**

- 프로젝트 실행에 필요한 패키지 모음

  ```bash
  streamlit
  azure-functions
  requests
  openai
  pillow

  ```

- 한 줄 설치
  ```bash
  pip install -r requirements.txt
  ```

### 4️⃣ **startup.txt (실행 스크립트)**

- Azure Web App에서 Streamlit과 Azure Function을 동시에 실행하도록 설정

  ```bash
  python -m streamlit run app.py --server.port=8000
  ```

- Web App 시작 시 자동 실행되도록 구성

### 5️⃣ **.gitignore**

- Azure Web App에서 Streamlit과 Azure Function을 동시에 실행하도록 설정

  ```bash
  .venv/
  .vscode/
  __pycache__/
  local.settings.json

  ```

- `.venv`와 설정 파일은 깃허브 업로드 시 자동 무시

### 6️⃣ **README.md (프로젝트 문서)**

- 프로젝트 개요, 아키텍처, 실행 방법, 향후 개선 방향 정리
- 깃허브 첫 화면에서 프로젝트 설명 제공
- 포트폴리오 및 발표 자료로도 활용 가능

## 🔑 파일별 역할에 따른 핵심 기술 포인트

| 기능                               | 설명                                                                |
| :--------------------------------- | :------------------------------------------------------------------ |
| 🧤 **이미지 업로드 기반 PPE 감지** | Streamlit에서 이미지 업로드 → Azure Function → AI 분석 후 결과 표시 |
| 💬 **대화형 AI 상담 (GPT-4o)**     | 사용자의 질문을 GPT-4o에 전달해 실시간 답변 생성                    |
| ☁️ **Azure Functions 연동**        | Streamlit과 OpenAI API를 연결하는 서버리스 백엔드 구성              |
| 🧩 **간결한 구조**                 | `app.py`(UI) + `PPE_Function`(AI 백엔드) 로 역할 분리               |
| ⚙️ **확장성 고려된 설계**          | 이미지 분석, 텍스트 상담, 클라우드 배포를 손쉽게 확장 가능          |

---

## 6. 실행 방법

### 1️⃣ 저장소 클론 & 진입

```bash
git clone https://github.com/ejkimm25/ppe_check.git
cd ppe_check
```

### 2️⃣ 가상환경 생성 및 패키지 설치

```bash
python -m venv .venv
.\.venv\Scripts\activate     # (Windows PowerShell)
pip install -r requirements.txt
```

### 3️⃣ 로컬 환경 설정 (선택)

- Azure Functions 실행 시 local.settings.json을 사용할 수 있음
- Streamlit만 사용할 경우 추가 환경 설정은 필요 없음
- (만약 Azure OpenAI API를 직접 연결할 경우)

```bash
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

### 4️⃣ 앱 실행

- Streamlit 실행

```bash
streamlit run app.py
```

→ 실행 후 브라우저에서 http://localhost:8501 접속

- Azure Functions 실행 (선택)

```bash
func start
```

→ 로컬 백엔드 테스트용 (http://localhost:7071)

---

## 7. 라이브 데모

- **이미지 업로드 기능**  
  사용자가 작업자 이미지를 업로드하면  
  AI가 자동으로 **PPE(보호장비) 착용 여부를 분석**하고 누락된 항목을 시각적으로 표시합니다.

- **대화형 AI 상담 기능**  
  사용자가 **자연어로 질문을 입력**하면  
  GPT-4o 모델이 PPE 관련 규정, 안전 수칙, 장비 선택 등을 실시간으로 안내합니다.

- **분석 결과 표시**  
  분석 결과는 Streamlit 화면에  
  ✅ 착용 장비 / ⚠️ 미착용 장비 목록 형태로 표시되며 누락 항목을 강조해 시각적으로 보여줍니다.

---

## 8. 시연 영상

---

## 9. 앞으로 하고 싶은 것

- 🦺 **PPE 종류 확장**  
  현재는 안전모, 장갑, 조끼 등의 기본 항목만 인식하지만,  
  앞으로 **보안경, 안전화, 귀마개, 방진마스크 등 다양한 보호장비**를 추가 감지할 수 있도록 모델을 확장할 예정

- 🎯 **착용 정확도 향상 및 세부 인식 고도화**  
  단순 착용 여부뿐 아니라 **착용 상태(정확히 썼는지, 벗겨져 있는지)** 까지 판별하는 세밀한 감지 알고리즘을 도입할 예정

- 📸 **실시간 카메라 연동**  
  CCTV 또는 웹캠과 연동해 **실시간 PPE 착용 여부를 모니터링**하고, 미착용 시 **경고 알림(이메일 등)** 기능을 추가할 계획
