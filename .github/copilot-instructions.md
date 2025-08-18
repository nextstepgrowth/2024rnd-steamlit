# Copilot Instructions

이 문서는 Copilot 사용 시 프로젝트 개발 규칙과 가이드를 정의합니다.  
본 프로젝트는 **Streamlit 기반**으로 개발되며, Copilot이 생성하는 코드와 답변은 **항상 한국어**를 기준으로 합니다.

---

## 기본 규칙

### 1. 답변 언어

- Copilot이 제안하는 모든 코드 주석, 설명, 문서화는 **반드시 한국어**로 작성되어야 합니다.
- 영어 라이브러리명, 함수명은 그대로 사용하되, 설명은 한국어로 변환합니다.

### 2. 코드 스타일

- Python 표준 스타일 가이드(`PEP8`)를 준수합니다.
- 함수명, 변수명은 **snake_case**로 작성합니다.
- Streamlit의 UI 요소는 명확하게 주석 처리하여 협업자가 쉽게 이해할 수 있도록 합니다.

### 3. Streamlit 특화 지침

- `st.cache_data` 또는 `st.cache_resource`를 적극 활용해 불필요한 연산 중복을 줄입니다.
- UI 레이아웃은 `st.sidebar`, `st.columns`, `st.tabs` 등을 활용해 사용성이 좋게 만듭니다.
- 데이터 시각화 시 `matplotlib` 또는 `plotly`를 우선 활용하며, **코드 내 그래프 제목/라벨은 한국어**로 작성합니다.

---

## 기술 스택

- **프레임워크**: Streamlit
- **언어**: Python 3.x
- **시각화 라이브러리**: matplotlib, plotly (필요 시 seaborn)
- **데이터 처리**: pandas, numpy
- **환경 변수 관리**: `.env` (단, Git에는 `.env.example`만 포함)

---

## 금지 사항

- 영어로 답변/주석 작성 금지
- Streamlit 외의 프레임워크(Django, Flask 등) 코드 자동 제안 금지
- 불필요한 전역 변수 사용 금지
- API 키, 비밀 키를 코드에 직접 포함하는 행위 금지
