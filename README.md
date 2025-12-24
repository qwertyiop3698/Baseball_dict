# 야구용어 백과사전 & 선수 비교 분석

Flask 기반의 야구 정보 웹 앱입니다.

메인 화면에서는 야구용어를 검색할 수 있고, 왼쪽 하단의 `선수 비교 분석` 버튼을 누르면 `players_data.json`에 있는 선수끼리 기록을 비교할 수 있습니다.

## 주요 기능

- 야구용어 백과사전
  - OPS, WHIP, WAR, 보크, 인필드 플라이 같은 야구용어 질문 가능
  - Gemini API를 사용해 설명 생성
  - 선수 관련 질문은 선수 비교 화면으로 안내

- 선수 비교 분석
  - 투수 / 타자 유형 선택
  - 데이터 안에 있는 선수 중 `선수 1 vs 선수 2` 선택
  - 공통 기록을 비교하고 강점 지표 중심으로 요약 문장 표시

## 실행 방법

이 프로젝트는 VS Code Live Server가 아니라 Flask 서버로 실행해야 합니다.

```powershell
python app.py
```

실행 후 브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:5000
```

Live Server 주소인 `http://127.0.0.1:5500/...`로 열면 `/ask` 같은 Flask API가 동작하지 않아 405 오류가 날 수 있습니다.

## API 키 설정

프로젝트 루트에 `.env` 파일을 만들고 Gemini API 키를 설정합니다.

```env
API_KEY="your_gemini_api_key"
```

현재 앱은 `.env`에서 `API_KEY` 값을 읽어 Gemini API 호출에 사용합니다.

## 필요한 패키지

아래 패키지가 필요합니다.

```powershell
pip install flask requests
```

## 파일 구조

```text
baseball/
├─ app.py
├─ players_data.json
├─ templates/
│  ├─ dict.html
│  └─ compare.html
├─ static/
│  └─ css/
│     └─ bb.css
├─ .env
└─ .gitignore
```

## 사용 흐름

1. `python app.py`로 Flask 서버를 실행합니다.
2. `http://127.0.0.1:5000`으로 접속합니다.
3. 메인 화면에서 야구용어를 검색합니다.
4. 선수 비교가 필요하면 왼쪽 하단의 `선수 비교 분석` 버튼을 누릅니다.
5. 비교 화면에서 투수/타자를 선택하고 두 선수를 골라 기록을 비교합니다.

## 참고

- `.env`는 `.gitignore`에 포함되어 있으므로 Git에 올리지 않습니다.
- 선수 데이터는 `players_data.json`을 기준으로 표시됩니다.
- Gemini API 키가 없거나 잘못되면 용어 검색 응답에서 API 관련 오류가 표시될 수 있습니다.
