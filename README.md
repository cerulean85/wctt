
## [**WCTT: HTML 문서 정형화 기반 웹 크롤링 시스템**](https://kut.dcollection.net/public_resource/pdf/200000607787_20240305214629.pdf) (2022)


### 1. 연구 배경 및 필요성

* **웹 크롤러**는 SNS, 블로그, 뉴스 등 다양한 웹사이트에서 본문 데이터를 수집하는 데 필수 도구로 자리잡고 있음
* 기존 웹 크롤러는 각 웹사이트 구조에 맞게 **수동으로 HTML 태그와 스타일을 분석**해 로직을 구성해야 하기 때문에 **유지 보수와 확장성**에 한계가 있음
* 웹 페이지 구조가 바뀌거나 수집 채널이 추가되면 **수집 로직을 수정해야** 하는 번거로움이 존재

---

### 2. 기존 방법의 한계

* 단어/링크 밀도, 시각적 특징, 시퀀스 레이블링 등 다양한 자동화 기법들이 존재하나, **수집 채널마다 정확도에 편차**가 큼
* 수집 API 활용은 **데이터 제공량의 한계**가 있어 빅데이터 분석에 부적합

---

### 3. 제안 방법: WCTT 시스템

* \*\*WCTT(Web Crawling based on Tag path and Text appearance frequency)\*\*는 HTML 문서를 정형화하여 수집 채널에 관계없이 동일한 로직으로 본문을 수집할 수 있는 시스템
* **핵심 기술**:

  * DOM 트리에서 \*\*텍스트 노드의 태그 경로(Tag Path)\*\*와
  * \*\*텍스트 출현 빈도 순위(TAF: Text Appearance Frequency)\*\*를 이용하여
  * HTML 문서를 **정형화된 텍스트 블록 집합**으로 변환함

---

![image](https://github.com/user-attachments/assets/daced762-a083-46e0-ab70-cd2867991073)


### 4. 시스템 구성 요소

1. **사용자 인터페이스**: 수집 조건 입력 (채널, 키워드, 기간 등)
2. **웹 크롤러**:

   * URL 수집기 (검색 페이지를 통해 URL 수집)
   * HTML 다운로더
   * 본문 수집기 (정형화된 문서에서 본문 추출)
   * 본문 전처리기 (불용어 제거, 명사 추출)
3. **메시징 큐 (Kafka)**: URL 수집과 본문 수집의 병렬 처리 지원
4. **관계형 데이터베이스**: 수집된 데이터 저장
5. **모니터링 서버**: 수집 상태 감시

---

### 5. 주요 특징

* **DCI(Data Collection Information)**: 외부 JSON 파일로 수집 채널별 정보 관리 (태그 경로, TAF 사전 등 포함)
* **확장성 우수**: 수집 채널이 추가되어도 **로직 수정 불필요**
* **정확도**: 다양한 채널(네이버 블로그, 중앙일보, 트위터 등)에서 **높은 정확도**로 본문 추출 가능
* **전처리 기능 포함**: 키워드 네트워크 분석 등 **빅데이터 분석에 바로 활용 가능**

![image](https://github.com/user-attachments/assets/e1e22d27-450c-4703-a5e2-e676ba3e3f04)



---

### 6. 결론

WCTT는 HTML 문서를 정형화하여 채널 독립적인 본문 수집을 가능하게 만든 시스템으로, 기존 웹 크롤러의 유지 보수와 확장성 문제를 해결하고, 다양한 수집 채널에서 안정적으로 본문을 수집할 수 있는 대안임

---

### 00. 사용방법

1) Download and install **Node.js**, **Python**, **JDK** in [this LINK](https://drive.google.com/drive/folders/1JCV8mvFtIXyZU1_v2MubHQOKHQ_IluQK?usp=sharing "Google Driver").

2) Download ZIP package and unzip.

3) Execute Script file.Cancel changes

- If your OS is Windows, execute install.bat.

- If your OS is Linux, execute install.sh.

<br>

4) Start Execution file.

- If you OS is Windows, execute start.bat.

- If you OS is Linux, execute start.sh.

- Then, you can see the browser that you can enroll and control you work.


