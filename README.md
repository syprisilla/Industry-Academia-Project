
# 🎙️ 바른발음 (Bareun Bareum)

### 목소리로 몬스터를 물리치는 스토리 기반 발음 훈련 게임

**바른발음(Bareun Bareum)**은 기능적 조음장애(Functional Articulation Disorder, FAD) 아동의 반복적인 발음 연습을 돕기 위해 개발한 **스토리 기반 기능성 게임(Serious Game)**입니다.

아동은 작은 유령과 함께 저주받은 아파트를 탐험하며, 자신의 목소리로 몬스터를 물리칩니다. 게임은 한국어 마찰음 **/ㅅ/**을 중심으로 발음 수준을 평가하고, 사용자에게 맞는 핵심 단어와 연습 단어를 제공하도록 설계되었습니다.

![게임 메인 메뉴 배경](game/gui/main_menu_hallway.png)

> 본 프로젝트는 발음 훈련을 지원하기 위한 교육·연구용 프로토타입으로, 의료적 진단이나 전문적인 언어치료를 대체하지 않습니다.

---

## 📌 목차

- [프로젝트 목표](#-프로젝트-목표)
- [주요 기능](#-주요-기능)
- [게임 진행 방식](#-게임-진행-방식)
- [발음 분석 및 판정](#-발음-분석-및-판정)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [참고 사항](#-참고-사항)
- [라이선스](#-라이선스)

## 🎯 프로젝트 목표

- **개인 맞춤형 훈련:** 초기 발음 평가를 통해 비교적 정확한 음절과 연습이 필요한 음절을 구분합니다.
- **훈련 동기 부여:** 단순한 발음 반복을 몬스터 전투, 이야기 진행, 캐릭터 피드백으로 연결합니다.
- **음향 기반 피드백:** 녹음된 발화에서 /ㅅ/ 마찰 구간을 분석하고 음향 지표를 이용해 발음 결과를 제시합니다.
- **점진적 난이도:** 음절(CV·VCV)부터 단어, 긴 단어와 문장까지 단계적으로 연습합니다.
- **학습 기록 확인:** 성공률과 재시도 횟수, 몬스터별·단어별 결과를 확인할 수 있도록 합니다.

## ✨ 주요 기능

| 기능 | 설명 |
| --- | --- |
| 초기 발음 평가 | `시`, `세`, `사`, `서`, `소`, `수`, `스` 7개 음절을 녹음하고 상대적으로 명확한 음절과 연습 음절을 선정 |
| 핵심 단어 선택 | 명확하게 발음한 음절을 바탕으로 핵심 단어(Core Word) 후보를 제시하고 사용자가 선택 |
| 짝자극 접근법 | 핵심 단어를 먼저 연습한 뒤 목표 음절·단어를 발음하는 Paired-Stimulus 방식 적용 |
| 실시간 발음 피드백 | 마이크 녹음 → /ㅅ/ 마찰 구간 분석 → 음향 지표 판정 → 결과·피드백 표시 |
| 몬스터 전투 | 발음 성공을 공격과 몬스터 체력 감소로 연결 |
| 재도전 시스템 | 실패가 누적되면 Retry/Exit 선택지를 제공하고, 일반 몬스터는 다른 연습 단어로 변경 가능 |
| 문장 발음 평가 | 문장 속 /ㅅ/ 소리를 검출하고 각 목표 발음의 성공 여부를 판정 |
| 훈련 결과 확인 | 성공률, 첫 시도 성공률, 평균 재시도 횟수, 몬스터 정화 현황 등 제공 |
| 발음 비교 | 시작 단계와 최종 보스 단계에서 녹음한 동일 문장의 분석 결과 비교 화면 제공 |

## 🎮 게임 진행 방식

### 전체 흐름

1. 게임 시작 및 이름 입력
2. 초기 문장 녹음
3. 7개 음절 발음 평가
4. 핵심 단어 선택
5. Chapter 1: CV·VCV 음절 훈련
6. Chapter 2: 단어 훈련
7. Chapter 3: 긴 단어 훈련
8. 최종 보스: 음절·단어·문장 훈련
9. 엔딩 및 훈련 결과 확인

### 챕터 구성

| 구분 | 훈련 내용 | 등장 몬스터 |
| --- | --- | --- |
| **Chapter 1** | /ㅅ/ 포함 CV·VCV 음절 연습 | Dust Monster, Echo Monster, Shadow Monster |
| **Chapter 2** | /ㅅ/ 포함 단어 연습 | Whisper Monster, Toy Monster, Clock Monster |
| **Chapter 3** | 긴 단어 연습 및 최종 문장 평가 | Letter Monster, Thorny Vine Monster, Final Boss |

최종 보스에서는 **취약 음절 → 관련 단어 → 문장** 순서로 발음을 연습합니다. 마지막 문장 녹음은 게임 도입부에 사용한 문장과 비교할 수 있도록 구성되어 있습니다.

### 전투 및 재도전 규칙

1. 매 공격 전에 선택한 **핵심 단어**를 제시한 다음 **목표 단어**의 발음을 녹음합니다.
2. 발음에 성공하면 공격이 적용되며, **성공 3회**로 해당 몬스터를 처치합니다.
3. 발음 실패는 누적되며, **실패 3회** 시 `Retry` / `Exit` 화면을 표시합니다.
4. **일반 몬스터:** `Retry` 시 기존 성공 횟수(몬스터 HP)를 유지하고, 동일한 연습 음절 그룹에서 다른 목표 단어를 선택합니다. 해당 그룹에 대체 단어가 없으면 같은 단어를 사용합니다.
5. **최종 보스:** `Retry` 시 성공·실패 횟수를 초기화하고 전투를 처음부터 다시 진행합니다. `Exit` 시 실패 엔딩으로 연결됩니다.
6. 녹음이 제대로 측정되지 않은 경우(`unrecognized`)에는 성공·실패 횟수에 반영하지 않고 다시 녹음하도록 합니다.

## 🔊 발음 분석 및 판정

게임 화면은 **Ren'Py**, 음성 녹음·분석은 **Python 기반 음성 엔진**이 담당합니다.

1. **마이크 입력 및 WAV 녹음** — 사용자 발화를 녹음합니다.
2. **녹음 품질 확인** — 음량과 주변 소음 등을 확인합니다.
3. **/ㅅ/ 마찰 구간 추출** — 녹음에서 분석할 구간을 검출합니다.
4. **CoG·Spectral SD 계산** — 주요 음향 지표를 추출합니다.
5. **기준 범위 비교** — 측정값과 설정된 참고 범위를 비교합니다.
6. **발음 결과 처리** — 성공·실패·측정 불가로 구분합니다.
7. **게임에 반영** — 발음 피드백과 몬스터 전투에 결과를 적용합니다.

### 핵심 음향 지표

| 지표 | 의미 | 활용 |
| --- | --- | --- |
| **Center of Gravity (CoG)** | 마찰음 스펙트럼의 에너지가 집중된 중심 주파수 | /ㅅ/ 마찰음의 주파수 특성 분석 |
| **Spectral Standard Deviation (SD)** | 스펙트럼 에너지가 중심 주파수 주변에 퍼져 있는 정도 | 마찰음 에너지 분포 분석 |

현재 판정 코드(`game/python/Judge.py`)는 두 지표가 모두 설정된 기준 범위에 포함되고 /ㅅ/ 마찰 구간이 실제로 검출되어야 성공으로 처리합니다. 기준 범위는 각 지표의 **평균 ± 1.5 × 표준편차**로 정의되어 있습니다.

> **참고:** `Judge.py`의 판정 기준은 코드상 잠정값(provisional)으로 표시되어 있습니다. `game/data/reference_by_syllable.json`에는 음절별 참고 통계가 별도로 저장되어 있으나, 현재 판정 로직이 이 파일을 직접 읽어 사용하는 것은 아닙니다.

녹음 과정에서는 과도한 음량, 너무 작은 소리, 주변 소음 등의 상태를 확인합니다. 분석이 어려운 경우에는 잘못된 발음으로 단정하지 않고 재녹음을 유도합니다.

### 주요 구현 파일

- [`Audio_recording.py`](game/python/Audio_recording.py) — 마이크 녹음 및 입력 품질 확인
- [`Pronunciation_analysis.py`](game/python/Pronunciation_analysis.py) — 마찰 구간 검출 및 음향 특징 추출
- [`Judge.py`](game/python/Judge.py) — 기준 범위 기반 성공 여부 판정
- [`Feedback.py`](game/python/Feedback.py) — 발음 결과에 따른 안내 메시지 생성
- [`Gauge.py`](game/python/Gauge.py) — 음향 지표 시각화
- [`Voice_engine.py`](game/python/Voice_engine.py) — 음성 분석 기능 통합 및 명령행 실행

## 🛠 기술 스택

| 분야 | 기술 |
| --- | --- |
| 게임 엔진 및 UI | Ren'Py |
| 음성 분석 및 처리 | Python, NumPy, Praat-Parselmouth |
| 녹음 및 WAV 입출력 | SoundDevice, SoundFile |
| 데이터 시각화 | Matplotlib |
| 게임·훈련 데이터 | JSON, Ren'Py Persistent Data |
| 데이터베이스 관련 모듈 | SQLite (별도 보조 코드 포함) |
| 음성 엔진 실행 파일 빌드 | PyInstaller |

Python 패키지의 상세 버전은 [`game/python/Requirements.txt`](game/python/Requirements.txt)를 참고하세요.

## 📁 프로젝트 구조

```text
Industry-Academia-Project/
├── README.md
├── LICENSE
├── game/
│   ├── audio/                     # 배경 음악 및 효과음
│   ├── config/                    # 게임 변수 및 설정
│   ├── data/
│   │   ├── words.json             # 핵심 단어·몬스터별 목표 단어
│   │   ├── sentences.json         # 문장 평가용 데이터
│   │   └── reference_by_syllable.json  # 음절별 음향 참고값
│   ├── database/                  # SQLite 연동 관련 코드
│   ├── gui/                       # 메뉴 및 기본 GUI 리소스
│   ├── images/                    # 배경·캐릭터·전투 이미지
│   ├── python/
│   │   ├── Audio_recording.py
│   │   ├── Pronunciation_analysis.py
│   │   ├── Judge.py
│   │   ├── Feedback.py
│   │   ├── Gauge.py
│   │   ├── Voice_engine.py
│   │   ├── Requirements.txt
│   │   └── voice_engine.spec      # PyInstaller 빌드 설정
│   ├── scripts/
│   │   ├── intro.rpy              # 도입부·초기 평가 연결
│   │   ├── chapter1.rpy
│   │   ├── chapter2.rpy
│   │   ├── chapter3.rpy
│   │   └── battle/                # 공통 전투 및 성공·실패 처리
│   ├── systems/                   # 평가·전투·결과 UI와 게임 상태
│   ├── voice.rpy                  # Ren'Py ↔ 음성 엔진 연동
│   ├── screens.rpy                # 공통 게임 화면
│   └── options.rpy                # Ren'Py 프로젝트 설정
└── show_schema.py
```

## 🚀 설치 및 실행

현재 `game/voice.rpy`는 Windows 실행 파일인 `voice_engine.exe`를 호출하도록 작성되어 있으므로, 아래는 **Windows + Ren'Py SDK** 기준입니다.

### 1. 사전 준비

- [Ren'Py SDK](https://www.renpy.org/latest.html)
- Python 및 `pip`
- 작동하는 마이크와 Windows 마이크 접근 권한
- Git

### 2. 저장소 복제

```powershell
git clone https://github.com/syprisilla/Industry-Academia-Project.git
cd Industry-Academia-Project
```

### 3. Python 가상환경 및 의존성 설치

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r game/python/Requirements.txt
python -m pip install pyinstaller
```

### 4. 음성 엔진 빌드

저장소에는 빌드된 `voice_engine.exe`가 포함되어 있지 않으므로 별도 빌드가 필요합니다.

```powershell
cd game/python
pyinstaller --noconfirm --clean voice_engine.spec
Copy-Item -Path .\dist\voice_engine -Destination .\voice_engine -Recurse -Force
cd ../..
```

다음 파일이 생성되었는지 확인합니다.

```text
game/python/voice_engine/voice_engine.exe
```

마이크 입력 상태는 다음과 같이 확인할 수 있습니다.

```powershell
.\game\python\voice_engine\voice_engine.exe mic-test
```

### 5. Ren'Py에서 실행

1. **Ren'Py Launcher**를 엽니다.
2. Projects Directory를 **`Industry-Academia-Project` 폴더의 상위 디렉터리**로 설정합니다.
3. 프로젝트 목록에서 `Industry-Academia-Project`를 선택합니다.
4. **Launch Project**를 클릭합니다.

게임 내 발음 평가를 사용하려면 음성 엔진 실행 파일이 지정된 위치에 있어야 합니다.

### 6. 음성 분석 모듈만 실행하기 (선택)

```powershell
# 입력 가능한 마이크 목록
python game/python/Voice_engine.py devices

# 마이크 상태 점검
python game/python/Voice_engine.py mic-test

# 기존 WAV 파일 분석 및 판정
python game/python/Voice_engine.py judge sample.wav
```

## 📝 참고 사항

- 초기 평가·단어 선택 데이터는 `game/data/*.json` 파일을 기반으로 처리하며, 게임 진행 정보와 일부 훈련 기록은 Ren'Py Persistent Data에도 저장됩니다.
- `game/database/` 및 `game/python/db_server.py`에 SQLite 연동용 보조 코드가 있지만, 위 기본 게임 실행 절차에서 별도 DB 서버 구동을 요구하지는 않습니다.
- `game/python/Requirements.txt`는 음성 분석용 Python 패키지를 정의합니다. PyInstaller는 실행 파일 빌드를 위해 별도로 설치합니다.
- 현재 발음 판정 기준과 피드백 문구는 검증·보완이 필요한 프로토타입 설정입니다.

## 📄 라이선스

본 저장소는 [MIT License](LICENSE)를 따릅니다.
