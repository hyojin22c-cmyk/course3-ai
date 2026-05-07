---
title: 삼괴고 3학년 선택과목 가이드
emoji: 📚
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# 📚 삼괴고 3학년 선택과목 가이드

2025학년도 입학생 교육과정 편제표 기준, 3학년 선택과목 추천 사이트입니다.

## 기능
- **AI 맞춤 추천**: 진로·성적·학습 스타일·평가 선호 등을 입력하면 학기·그룹별로 점수 기반 상위 추천
- **진로별 추천 조합**: 14개 진로 트랙별 추천 풀세트 + 대입 가이드
- **키워드 검색**: 진로 키워드(의대, 반도체, 외교 등) 입력 → 관련 과목 필터링
- **전체 과목 보기**: 학기별·선택그룹별 정렬, 평가방식(5등급 상대평가/절대평가/PF) 필터
- **localStorage 저장**: 새로고침해도 입력값 보존

## 구조
- `index.html` — 메인 페이지
- `style.css` — 스타일
- `data.js` — 과목/진로/직업 데이터 (수정은 여기서)
- `scoring.js` — 추천 점수 엔진
- `app.js` — UI 로직, 4개 탭 렌더링

## 로컬 실행
```bash
python3 -m http.server 8000
# 브라우저에서 http://localhost:8000
```

## 배포
- **Hugging Face Spaces** (`sdk: static`): 정적 호스팅, 동시접속 무제한
- (이전 버전) Streamlit Community Cloud: app.py 기반 (현재는 리다이렉트 용도)

---
삼괴고등학교 교육과정부
