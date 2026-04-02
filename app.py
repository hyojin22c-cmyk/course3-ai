import streamlit as st

st.set_page_config(page_title="삼괴고 3학년 선택과목 가이드", page_icon="📚", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    html, body, .stApp { font-family: 'Noto Sans KR', sans-serif; }
    .main-header { text-align: center; padding: 1.2rem 0 0.8rem; }
    .main-header h1 { font-size: 1.8rem; font-weight: 700; color: #1a365d; margin-bottom: 0.2rem; }
    .main-header p { color: #64748b; font-size: 0.9rem; }
    .semester-title { font-size: 1.3rem; font-weight: 700; color: #0f3460; border-bottom: 3px solid #0f3460; padding-bottom: 0.3rem; margin: 1.5rem 0 0.8rem; }
    .group-title { font-size: 1rem; font-weight: 600; color: #334155; margin: 1rem 0 0.5rem; padding: 0.4rem 0.8rem; background: #f1f5f9; border-radius: 8px; display: inline-block; }
    .course-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.6rem; }
    .course-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.07); }
    .course-card.rec { border-left: 4px solid #2563eb; background: #f0f7ff; }
    .course-name { font-size: 1.05rem; font-weight: 700; color: #1e293b; margin-bottom: 0.3rem; }
    .course-desc { font-size: 0.85rem; color: #475569; line-height: 1.55; margin-bottom: 0.4rem; }
    .badge { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 20px; font-size: 0.72rem; font-weight: 500; margin-right: 0.3rem; margin-bottom: 0.2rem; }
    .badge-rec { background: #dbeafe; color: #1d4ed8; font-weight: 700; }
    .badge-group { background: #f0fdf4; color: #15803d; }
    .badge-eval-rel { background: #fef3c7; color: #92400e; }
    .badge-eval-abs { background: #ede9fe; color: #6d28d9; }
    .badge-track { background: #fce7f3; color: #9d174d; }
    .combo-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem; }
    .combo-title { font-size: 1.1rem; font-weight: 700; color: #1a365d; margin-bottom: 0.6rem; }
    .combo-sem { font-weight: 600; color: #0f3460; margin: 0.6rem 0 0.3rem; font-size: 0.95rem; }
    .combo-item { font-size: 0.88rem; color: #334155; padding: 0.15rem 0; line-height: 1.5; }
    .ai-profile-banner { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem; }
    .ai-profile-banner h3 { color: white; margin-bottom: 0.5rem; font-size: 1.1rem; }
    .ai-profile-banner p { color: rgba(255,255,255,0.9); font-size: 0.88rem; margin: 0.2rem 0; }
    .ai-card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; }
    .ai-card.top { border-left: 4px solid #7c3aed; background: #faf5ff; }
    .ai-score { font-size: 1.3rem; font-weight: 700; margin-right: 0.5rem; }
    .ai-score.high { color: #059669; }
    .ai-score.mid { color: #d97706; }
    .ai-score.low { color: #9ca3af; }
    .ai-reason { font-size: 0.82rem; color: #475569; line-height: 1.6; margin: 0.3rem 0; }
    .ai-warning { font-size: 0.82rem; color: #dc2626; line-height: 1.6; }
    .score-bar-bg { background: #e5e7eb; border-radius: 6px; height: 8px; width: 100%; }
    .score-bar-fill { border-radius: 6px; height: 8px; }
    .score-bar-fill.high { background: linear-gradient(90deg, #059669, #34d399); }
    .score-bar-fill.mid { background: linear-gradient(90deg, #d97706, #fbbf24); }
    .score-bar-fill.low { background: linear-gradient(90deg, #9ca3af, #d1d5db); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 과목 데이터
# ============================================================
COURSES = {
    "정치": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"민주주의의 원리, 정치 과정, 선거 제도, 지방자치 등 정치 현상 전반을 탐구합니다.","tracks":["인문사회","법·정치","행정"],"kw":["정치","민주주의","선거","국회","시민","공무원","행정","외교"],
        "aff":{"국어":0.4,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.9},"diff":3,"mem":0.5,"und":0.4,"pra":0.1,"wl":3,"gc":"보통","rmg":{"사회":3}},
    "법과 사회": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"법의 기본 원리, 헌법, 민법, 형법 등 생활 속 법률 지식을 학습합니다.","tracks":["법·정치","인문사회","행정"],"kw":["법","변호사","판사","검사","법학","헌법","인권","로스쿨"],
        "aff":{"국어":0.5,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.8},"diff":3,"mem":0.5,"und":0.4,"pra":0.1,"wl":3,"gc":"보통","rmg":{"사회":3}},
    "금융과 경제 생활": {"sem":"3-1","grp":"택3","cr":3,"eval":"절대평가","desc":"금융 시장, 자산 관리, 신용, 투자 등 실생활 경제·금융 지식을 배웁니다.","tracks":["상경계","경제금융"],"kw":["경제","금융","주식","투자","은행","회계","경영","세무"],
        "aff":{"국어":0.2,"수학":0.5,"영어":0.1,"과학":0.0,"사회":0.7},"diff":3,"mem":0.3,"und":0.5,"pra":0.2,"wl":3,"gc":"낮음","rmg":{"사회":3}},
    "윤리문제 탐구": {"sem":"3-1","grp":"택3","cr":3,"eval":"절대평가","desc":"생명윤리, 환경윤리, 정보윤리 등 현대 사회의 윤리적 쟁점을 다양한 관점에서 탐구합니다.","tracks":["인문사회","철학윤리","교육"],"kw":["윤리","철학","도덕","생명윤리","AI윤리","인권","정의"],
        "aff":{"국어":0.5,"수학":0.0,"영어":0.1,"과학":0.1,"사회":0.7},"diff":3,"mem":0.3,"und":0.6,"pra":0.1,"wl":3,"gc":"낮음","rmg":{"사회":3}},
    "도시의 미래 탐구": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"도시의 형성과 변화, 도시 문제, 지속가능한 도시 개발 등을 탐구합니다.","tracks":["인문사회","환경도시","건축"],"kw":["도시","건축","도시계획","부동산","스마트시티","교통","환경","지리"],
        "aff":{"국어":0.2,"수학":0.1,"영어":0.1,"과학":0.3,"사회":0.7},"diff":2,"mem":0.3,"und":0.5,"pra":0.2,"wl":2,"gc":"보통","rmg":{"사회":3}},
    "고급 물리학": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"역학, 전자기학, 양자역학 등 물리학의 심화 내용을 다룹니다.","tracks":["이공계","자연과학","의약계"],"kw":["물리","역학","전자기","양자","반도체","우주","공학","기계","전기전자","항공"],
        "aff":{"국어":0.1,"수학":0.9,"영어":0.1,"과학":0.9,"사회":0.0},"diff":5,"mem":0.2,"und":0.7,"pra":0.1,"wl":5,"gc":"높음","rmg":{"수학":2,"과학":2}},
    "고급 화학": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"화학 결합, 반응 속도, 화학 평형 등 화학의 심화 개념을 학습합니다.","tracks":["이공계","자연과학","의약계"],"kw":["화학","약학","화공","신소재","바이오","제약","화학공학"],
        "aff":{"국어":0.1,"수학":0.7,"영어":0.1,"과학":0.9,"사회":0.0},"diff":5,"mem":0.3,"und":0.6,"pra":0.1,"wl":5,"gc":"높음","rmg":{"수학":2,"과학":2}},
    "고급 생명과학": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"세포생물학, 유전공학, 생태학 등 생명과학의 심화 내용을 다룹니다.","tracks":["의약계","자연과학","이공계"],"kw":["생명과학","의대","약대","간호","생명공학","유전","바이오","수의","한의"],
        "aff":{"국어":0.1,"수학":0.5,"영어":0.1,"과학":0.9,"사회":0.0},"diff":5,"mem":0.4,"und":0.5,"pra":0.1,"wl":5,"gc":"높음","rmg":{"과학":3}},
    "물리학 실험": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"물리학 개념을 실험을 통해 직접 확인하고 탐구합니다.","tracks":["이공계","자연과학"],"kw":["물리","실험","공학","연구","반도체","전기전자"],
        "aff":{"국어":0.0,"수학":0.6,"영어":0.1,"과학":0.8,"사회":0.0},"diff":3,"mem":0.1,"und":0.4,"pra":0.5,"wl":3,"gc":"보통","rmg":{"과학":3}},
    "지구과학 실험": {"sem":"3-1","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"지질, 기상, 천문 등 지구과학 분야의 실험·관측 활동을 수행합니다.","tracks":["자연과학","이공계","환경도시"],"kw":["지구과학","기상","천문","지질","해양","환경","기후","우주"],
        "aff":{"국어":0.0,"수학":0.3,"영어":0.1,"과학":0.8,"사회":0.1},"diff":2,"mem":0.2,"und":0.3,"pra":0.5,"wl":2,"gc":"보통","rmg":{"과학":3}},
    "일본 문화": {"sem":"3-1","grp":"택1","cr":3,"eval":"5등급 상대평가","desc":"일본의 사회, 문화, 생활양식 등을 폭넓게 이해합니다.","tracks":["어문계","국제외교"],"kw":["일본","일본어","일본문화","통역","번역","관광","무역"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.2,"과학":0.0,"사회":0.5},"diff":2,"mem":0.4,"und":0.4,"pra":0.2,"wl":2,"gc":"보통","rmg":{}},
    "중국 문화": {"sem":"3-1","grp":"택1","cr":3,"eval":"5등급 상대평가","desc":"중국의 사회, 문화, 역사 등을 폭넓게 이해합니다.","tracks":["어문계","국제외교"],"kw":["중국","중국어","중국문화","통역","번역","무역"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.2,"과학":0.0,"사회":0.5},"diff":2,"mem":0.4,"und":0.4,"pra":0.2,"wl":2,"gc":"보통","rmg":{}},
    "교육의 이해": {"sem":"3-1","grp":"택1","cr":3,"eval":"P/F","desc":"교육의 개념, 목적, 역사, 심리학적 기초 등 교육학 전반을 배웁니다.","tracks":["교육","인문사회"],"kw":["교육","교사","사범대","교직","유아교육","특수교육","상담"],
        "aff":{"국어":0.5,"수학":0.1,"영어":0.2,"과학":0.1,"사회":0.6},"diff":3,"mem":0.4,"und":0.5,"pra":0.1,"wl":3,"gc":"낮음","rmg":{}},
    "인간과 심리": {"sem":"3-1","grp":"택1","cr":3,"eval":"P/F","desc":"인간의 행동과 정신 과정을 과학적으로 탐구합니다.","tracks":["인문사회","교육","의약계"],"kw":["심리","상담","심리학","정신건강","사회복지","임상심리","범죄심리","광고"],
        "aff":{"국어":0.3,"수학":0.1,"영어":0.2,"과학":0.3,"사회":0.6},"diff":3,"mem":0.3,"und":0.6,"pra":0.1,"wl":3,"gc":"낮음","rmg":{}},
    "보건": {"sem":"3-1","grp":"택1","cr":3,"eval":"P/F","desc":"건강 증진, 질병 예방, 응급처치 등 보건·건강 관련 지식을 배웁니다.","tracks":["의약계","보건간호"],"kw":["보건","간호","건강","의료","응급처치","공중보건","영양"],
        "aff":{"국어":0.1,"수학":0.1,"영어":0.1,"과학":0.7,"사회":0.2},"diff":2,"mem":0.5,"und":0.4,"pra":0.1,"wl":2,"gc":"낮음","rmg":{}},
    "데이터 과학": {"sem":"3-1","grp":"택1","cr":3,"eval":"5등급 상대평가","desc":"데이터 수집, 분석, 시각화의 기초를 배웁니다. 프로그래밍과 통계를 결합한 과목입니다.","tracks":["이공계","상경계","IT"],"kw":["데이터","프로그래밍","코딩","AI","인공지능","통계","빅데이터","컴퓨터","IT","소프트웨어"],
        "aff":{"국어":0.0,"수학":0.8,"영어":0.2,"과학":0.3,"사회":0.0},"diff":3,"mem":0.1,"und":0.4,"pra":0.5,"wl":3,"gc":"보통","rmg":{"수학":3}},
    "화법과 언어": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"효과적인 말하기·듣기 능력과 국어 문법 지식을 심화 학습합니다.","tracks":["인문사회","어문계","교육","법·정치"],"kw":["국어","문법","말하기","토론","언어학","국문학","아나운서","기자"],
        "aff":{"국어":0.9,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.2},"diff":3,"mem":0.4,"und":0.5,"pra":0.1,"wl":3,"gc":"보통","rmg":{"국어":3}},
    "언어생활 탐구": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"일상에서의 언어 사용 현상을 탐구합니다. 매체 언어, 방언, 언어 변화 등을 다룹니다.","tracks":["인문사회","어문계"],"kw":["국어","언어","매체","미디어","소통","언어학","국문학"],
        "aff":{"국어":0.8,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.3},"diff":2,"mem":0.3,"und":0.5,"pra":0.2,"wl":2,"gc":"보통","rmg":{}},
    "문학 감상과 비평": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"다양한 문학 작품을 감상하고 비평하는 역량을 기릅니다.","tracks":["인문사회","어문계","교육"],"kw":["문학","소설","시","비평","국문학","작가","창작","출판","인문학"],
        "aff":{"국어":0.9,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.2},"diff":3,"mem":0.3,"und":0.5,"pra":0.2,"wl":3,"gc":"보통","rmg":{"국어":3}},
    "경제 수학": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"수학적 개념을 경제·경영 분야에 적용하는 방법을 학습합니다.","tracks":["상경계","경제금융"],"kw":["경제","경영","수학","금융","회계","통계","보험수리"],
        "aff":{"국어":0.1,"수학":0.9,"영어":0.1,"과학":0.0,"사회":0.4},"diff":3,"mem":0.2,"und":0.6,"pra":0.2,"wl":3,"gc":"보통","rmg":{"수학":2}},
    "고급 대수": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"행렬, 벡터, 일차변환 등 대수학의 심화 내용을 다룹니다.","tracks":["이공계","자연과학"],"kw":["수학","대수","행렬","공학","수학과","물리","컴퓨터과학"],
        "aff":{"국어":0.0,"수학":1.0,"영어":0.1,"과학":0.3,"사회":0.0},"diff":5,"mem":0.2,"und":0.7,"pra":0.1,"wl":5,"gc":"높음","rmg":{"수학":2}},
    "고급 미적분": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"미적분학의 심화 내용(급수, 다변수 함수 등)을 학습합니다.","tracks":["이공계","자연과학","의약계"],"kw":["수학","미적분","공학","물리","의대","자연과학"],
        "aff":{"국어":0.0,"수학":1.0,"영어":0.1,"과학":0.3,"사회":0.0},"diff":5,"mem":0.2,"und":0.7,"pra":0.1,"wl":5,"gc":"높음","rmg":{"수학":2}},
    "영어독해와 작문": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"영어 지문 독해력과 영작문 능력을 심화합니다.","tracks":["어문계","국제외교","인문사회"],"kw":["영어","독해","작문","영문학","통역","번역","유학","국제"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.9,"과학":0.0,"사회":0.1},"diff":3,"mem":0.3,"und":0.4,"pra":0.3,"wl":3,"gc":"보통","rmg":{"영어":3}},
    "심화 영어": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"고급 수준의 영어 읽기·쓰기·말하기·듣기를 통합적으로 학습합니다.","tracks":["어문계","국제외교"],"kw":["영어","영문학","유학","해외대학","통역","번역","외교","국제기구"],
        "aff":{"국어":0.1,"수학":0.0,"영어":1.0,"과학":0.0,"사회":0.1},"diff":4,"mem":0.3,"und":0.4,"pra":0.3,"wl":4,"gc":"높음","rmg":{"영어":3}},
    "미디어 영어": {"sem":"3-1","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"뉴스, 영화, SNS 등 다양한 영어 매체 자료를 활용하여 영어 능력을 기릅니다.","tracks":["어문계","미디어"],"kw":["영어","미디어","방송","저널리즘","영화","콘텐츠","유튜브","광고"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.8,"과학":0.0,"사회":0.2},"diff":2,"mem":0.2,"und":0.4,"pra":0.4,"wl":2,"gc":"보통","rmg":{}},
    "음악연주와 창작": {"sem":"3-1","grp":"택4","cr":3,"eval":"절대평가","desc":"악기 연주와 음악 창작 활동을 통해 음악적 표현 능력을 심화합니다.","tracks":["예체능"],"kw":["음악","연주","작곡","밴드","실용음악","클래식","악기"],
        "aff":{"국어":0.1,"수학":0.0,"영어":0.0,"과학":0.0,"사회":0.0},"diff":2,"mem":0.1,"und":0.2,"pra":0.7,"wl":2,"gc":"낮음","rmg":{}},
    "스포츠 생활2": {"sem":"3-1","grp":"택4","cr":3,"eval":"절대평가","desc":"다양한 스포츠 활동에 참여하며 체력과 스포츠맨십을 기릅니다.","tracks":["예체능"],"kw":["체육","스포츠","운동","체육교육","레저","건강"],
        "aff":{"국어":0.0,"수학":0.0,"영어":0.0,"과학":0.0,"사회":0.0},"diff":1,"mem":0.0,"und":0.1,"pra":0.9,"wl":1,"gc":"낮음","rmg":{}},
    "사회문제 탐구": {"sem":"3-2","grp":"택3","cr":3,"eval":"절대평가","desc":"현대 사회의 다양한 문제(빈곤, 차별, 환경 등)를 탐구하고 해결 방안을 모색합니다.","tracks":["인문사회","법·정치","행정"],"kw":["사회","사회문제","빈곤","불평등","인권","복지","NGO","사회학"],
        "aff":{"국어":0.4,"수학":0.0,"영어":0.1,"과학":0.1,"사회":0.8},"diff":2,"mem":0.3,"und":0.5,"pra":0.2,"wl":2,"gc":"낮음","rmg":{}},
    "기후변화와 지속가능한 세계": {"sem":"3-2","grp":"택3","cr":3,"eval":"절대평가","desc":"기후변화의 원인과 영향, 지속가능발전 목표(SDGs) 등을 학습합니다.","tracks":["환경도시","국제외교","인문사회"],"kw":["기후","환경","지속가능","SDGs","탄소중립","에너지","국제기구","NGO"],
        "aff":{"국어":0.2,"수학":0.1,"영어":0.2,"과학":0.4,"사회":0.6},"diff":2,"mem":0.3,"und":0.5,"pra":0.2,"wl":2,"gc":"낮음","rmg":{}},
    "역사로 탐구하는 현대 세계": {"sem":"3-2","grp":"택3","cr":3,"eval":"절대평가","desc":"현대 세계의 주요 사건과 흐름을 역사적 관점에서 탐구합니다.","tracks":["인문사회","국제외교"],"kw":["역사","세계사","현대사","국제관계","전쟁","냉전","문명"],
        "aff":{"국어":0.3,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.9},"diff":2,"mem":0.5,"und":0.4,"pra":0.1,"wl":2,"gc":"낮음","rmg":{}},
    "여행지리": {"sem":"3-2","grp":"택3","cr":3,"eval":"절대평가","desc":"세계 여러 지역의 자연환경과 문화를 여행의 관점에서 탐구합니다.","tracks":["인문사회","관광"],"kw":["여행","지리","관광","문화","세계지리","호텔","항공"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.2,"과학":0.1,"사회":0.7},"diff":1,"mem":0.4,"und":0.4,"pra":0.2,"wl":1,"gc":"낮음","rmg":{}},
    "국제 관계의 이해": {"sem":"3-2","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"국제 사회의 구조, 외교, 국제기구, 국제법 등을 학습합니다.","tracks":["국제외교","법·정치","인문사회"],"kw":["국제관계","외교","UN","국제기구","국제법","안보","무역","글로벌"],
        "aff":{"국어":0.3,"수학":0.0,"영어":0.4,"과학":0.0,"사회":0.8},"diff":3,"mem":0.4,"und":0.5,"pra":0.1,"wl":3,"gc":"보통","rmg":{"사회":3}},
    "생명과학 실험": {"sem":"3-2","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"생명과학 개념을 실험을 통해 확인하고 탐구합니다.","tracks":["의약계","자연과학","이공계"],"kw":["생명과학","실험","의대","생명공학","바이오","연구","약학"],
        "aff":{"국어":0.0,"수학":0.3,"영어":0.1,"과학":0.9,"사회":0.0},"diff":3,"mem":0.2,"und":0.3,"pra":0.5,"wl":3,"gc":"보","rmg":{"과학":3}},
    "화학 실험": {"sem":"3-2","grp":"택3","cr":3,"eval":"5등급 상대평가","desc":"화학 반응과 물질의 성질을 실험을 통해 탐구합니다.","tracks":["이공계","자연과학","의약계"],"kw":["화학","실험","화공","신소재","약학","연구"],
        "aff":{"국어":0.0,"수학":0.4,"영어":0.1,"과학":0.9,"사회":0.0},"diff":3,"mem":0.2,"und":0.3,"pra":0.5,"wl":3,"gc":"보통","rmg":{"과학":3}},
    "기후변화와 환경생태": {"sem":"3-2","grp":"택3","cr":3,"eval":"절대평가","desc":"기후변화가 생태계에 미치는 영향과 환경 보전 방안을 과학적으로 탐구합니다.","tracks":["환경도시","자연과학"],"kw":["환경","생태","기후","보전","환경공학","탄소"],
        "aff":{"국어":0.1,"수학":0.1,"영어":0.1,"과학":0.7,"사회":0.4},"diff":2,"mem":0.3,"und":0.5,"pra":0.2,"wl":2,"gc":"낮음","rmg":{}},
    "과학의 역사와 문화": {"sem":"3-2","grp":"택3","cr":3,"eval":"절대평가","desc":"과학의 발전 과정과 사회·문화적 맥락을 탐구합니다.","tracks":["자연과학","인문사회"],"kw":["과학사","과학철학","융합","인문","과학기술"],
        "aff":{"국어":0.3,"수학":0.1,"영어":0.1,"과학":0.5,"사회":0.4},"diff":2,"mem":0.4,"und":0.5,"pra":0.1,"wl":2,"gc":"낮음","rmg":{}},
    "융합과학 탐구": {"sem":"3-2","grp":"택3","cr":3,"eval":"절대평가","desc":"물리·화학·생명과학·지구과학의 경계를 넘어 융합적 주제를 탐구합니다.","tracks":["이공계","자연과학"],"kw":["융합","과학탐구","STEAM","연구","과학"],
        "aff":{"국어":0.1,"수학":0.4,"영어":0.1,"과학":0.8,"사회":0.0},"diff":3,"mem":0.2,"und":0.5,"pra":0.3,"wl":3,"gc":"낮음","rmg":{}},
    "심화 일본어": {"sem":"3-2","grp":"택1","cr":3,"eval":"5등급 상대평가","desc":"일본어의 읽기·쓰기·말하기·듣기를 심화 수준으로 학습합니다.","tracks":["어문계","국제외교"],"kw":["일본어","일본","통역","번역","무역","관광"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.2,"과학":0.0,"사회":0.2},"diff":3,"mem":0.5,"und":0.3,"pra":0.2,"wl":3,"gc":"높음","rmg":{}},
    "심화 중국어": {"sem":"3-2","grp":"택1","cr":3,"eval":"5등급 상대평가","desc":"중국어의 읽기·쓰기·말하기·듣기를 심화 수준으로 학습합니다.","tracks":["어문계","국제외교"],"kw":["중국어","중국","통역","번역","무역","관광"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.2,"과학":0.0,"사회":0.2},"diff":3,"mem":0.5,"und":0.3,"pra":0.2,"wl":3,"gc":"높음","rmg":{}},
    "생태와 환경": {"sem":"3-2","grp":"택1","cr":3,"eval":"P/F","desc":"생태계의 구조와 기능, 환경 문제, 지속가능한 발전 등을 배웁니다.","tracks":["환경도시","자연과학"],"kw":["환경","생태","지속가능","환경공학","조경","산림","해양"],
        "aff":{"국어":0.1,"수학":0.1,"영어":0.1,"과학":0.7,"사회":0.3},"diff":3,"mem":0.4,"und":0.5,"pra":0.1,"wl":3,"gc":"낮음","rmg":{}},
    "인간과 철학": {"sem":"3-2","grp":"택1","cr":3,"eval":"P/F","desc":"인간 존재와 삶의 의미에 대한 철학적 질문을 탐구합니다.","tracks":["인문사회","철학윤리","교육"],"kw":["철학","인문학","사상","윤리","논리","존재론"],
        "aff":{"국어":0.6,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.6},"diff":3,"mem":0.3,"und":0.6,"pra":0.1,"wl":3,"gc":"낮음","rmg":{}},
    "간호의 기초": {"sem":"3-2","grp":"택1","cr":3,"eval":"P/F","desc":"간호학의 기본 개념, 건강 사정, 기초 간호 기술 등을 배웁니다.","tracks":["보건간호","의약계"],"kw":["간호","간호사","보건","의료","병원","간호학과","응급"],
        "aff":{"국어":0.1,"수학":0.1,"영어":0.1,"과학":0.7,"사회":0.1},"diff":3,"mem":0.4,"und":0.4,"pra":0.2,"wl":3,"gc":"낮음","rmg":{}},
    "생활과학 탐구": {"sem":"3-2","grp":"택1","cr":3,"eval":"5등급 상대평가","desc":"의·식·주 등 일상생활과 관련된 과학적 원리를 탐구합니다.","tracks":["자연과학","생활과학"],"kw":["생활과학","식품","영양","의류","소비자","가정","조리"],
        "aff":{"국어":0.1,"수학":0.1,"영어":0.0,"과학":0.5,"사회":0.3},"diff":1,"mem":0.3,"und":0.4,"pra":0.3,"wl":1,"gc":"보통","rmg":{}},
    "주제 탐구 독서": {"sem":"3-2","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"특정 주제에 대해 깊이 있는 독서와 탐구 활동을 수행합니다.","tracks":["인문사회","어문계","교육"],"kw":["독서","탐구","논문","인문학","비판적사고","학술","연구"],
        "aff":{"국어":0.8,"수학":0.0,"영어":0.1,"과학":0.1,"사회":0.4},"diff":3,"mem":0.3,"und":0.5,"pra":0.2,"wl":3,"gc":"보통","rmg":{"국어":3}},
    "독서 토론과 글쓰기": {"sem":"3-2","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"독서를 바탕으로 토론하고 논리적 글쓰기를 연습합니다.","tracks":["인문사회","어문계","법·정치","교육"],"kw":["독서","토론","글쓰기","논술","에세이","국어","기자","작가"],
        "aff":{"국어":0.9,"수학":0.0,"영어":0.1,"과학":0.0,"사회":0.3},"diff":3,"mem":0.2,"und":0.5,"pra":0.3,"wl":3,"gc":"보통","rmg":{"국어":3}},
    "수학과제 탐구": {"sem":"3-2","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"수학적 주제를 선정하여 자기주도적으로 탐구하고 발표합니다.","tracks":["이공계","자연과학"],"kw":["수학","탐구","연구","수학과","수리과학","프로젝트"],
        "aff":{"국어":0.1,"수학":0.9,"영어":0.1,"과학":0.2,"사회":0.0},"diff":3,"mem":0.1,"und":0.5,"pra":0.4,"wl":3,"gc":"보통","rmg":{"수학":3}},
    "수학과 문화": {"sem":"3-2","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"수학의 역사, 예술과의 관계, 실생활 속 수학 등을 탐구합니다.","tracks":["인문사회","교육"],"kw":["수학","수학사","문화","융합","인문수학"],
        "aff":{"국어":0.2,"수학":0.6,"영어":0.0,"과학":0.1,"사회":0.3},"diff":2,"mem":0.3,"und":0.5,"pra":0.2,"wl":2,"gc":"보통","rmg":{"수학":3}},
    "영어 발표와 토론": {"sem":"3-2","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"영어로 발표하고 토론하는 능력을 집중적으로 훈련합니다.","tracks":["어문계","국제외교"],"kw":["영어","발표","토론","스피킹","디베이트","국제","외교"],
        "aff":{"국어":0.2,"수학":0.0,"영어":0.9,"과학":0.0,"사회":0.2},"diff":4,"mem":0.2,"und":0.3,"pra":0.5,"wl":4,"gc":"높음","rmg":{"영어":3}},
    "세계 문화와 영어": {"sem":"3-2","grp":"택4","cr":3,"eval":"5등급 상대평가","desc":"세계 여러 나라의 문화를 영어를 통해 탐구합니다.","tracks":["어문계","국제외교","관광"],"kw":["영어","세계문화","글로벌","다문화","국제이해","관광"],
        "aff":{"국어":0.1,"수학":0.0,"영어":0.7,"과학":0.0,"사회":0.4},"diff":2,"mem":0.3,"und":0.4,"pra":0.3,"wl":2,"gc":"보통","rmg":{"영어":3}},
    "음악감상과 비평": {"sem":"3-2","grp":"택4","cr":3,"eval":"절대평가","desc":"다양한 장르의 음악을 감상하고 비평하는 능력을 기릅니다.","tracks":["예체능"],"kw":["음악","감상","비평","클래식","대중음악"],
        "aff":{"국어":0.3,"수학":0.0,"영어":0.0,"과학":0.0,"사회":0.1},"diff":1,"mem":0.2,"und":0.4,"pra":0.4,"wl":1,"gc":"낮음","rmg":{}},
    "스포츠 경기 기술": {"sem":"3-2","grp":"택4","cr":3,"eval":"절대평가","desc":"다양한 스포츠 종목의 경기 기술을 체계적으로 학습하고 실습합니다.","tracks":["예체능"],"kw":["체육","스포츠","경기","운동","체육교육","코치"],
        "aff":{"국어":0.0,"수학":0.0,"영어":0.0,"과학":0.0,"사회":0.0},"diff":1,"mem":0.0,"und":0.1,"pra":0.9,"wl":1,"gc":"낮음","rmg":{}},
}

# ============================================================
# 진로별 추천 풀세트 조합
# ============================================================
TRACK_COMBOS = {
    "이공계 (공학·반도체·전기전자·기계)": {
        "desc": "공학, 반도체, 전기전자, 기계공학, 항공우주, 컴퓨터공학 등",
        "1학기": {"택3": ["고급 물리학", "고급 화학", "물리학 실험"], "택1": "데이터 과학", "택4": ["고급 미적분", "고급 대수", "영어독해와 작문", "화법과 언어"]},
        "2학기": {"택3": ["화학 실험", "융합과학 탐구", "기후변화와 환경생태"], "택1": "생태와 환경", "택4": ["수학과제 탐구", "영어 발표와 토론", "독서 토론과 글쓰기", "주제 탐구 독서"]},
    },
    "IT·컴퓨터·AI": {
        "desc": "컴퓨터과학, 소프트웨어, 인공지능, 데이터사이언스 등",
        "1학기": {"택3": ["고급 물리학", "물리학 실험", "고급 화학"], "택1": "데이터 과학", "택4": ["고급 미적분", "고급 대수", "영어독해와 작문", "심화 영어"]},
        "2학기": {"택3": ["융합과학 탐구", "화학 실험", "과학의 역사와 문화"], "택1": "생태와 환경", "택4": ["수학과제 탐구", "영어 발표와 토론", "독서 토론과 글쓰기", "주제 탐구 독서"]},
    },
    "의약계 (의대·치대·한의대·약대·수의대)": {
        "desc": "의학, 치의학, 한의학, 약학, 수의학 등",
        "1학기": {"택3": ["고급 생명과학", "고급 화학", "윤리문제 탐구"], "택1": "보건", "택4": ["고급 미적분", "영어독해와 작문", "화법과 언어", "문학 감상과 비평"]},
        "2학기": {"택3": ["생명과학 실험", "화학 실험", "융합과학 탐구"], "택1": "간호의 기초", "택4": ["수학과제 탐구", "영어 발표와 토론", "독서 토론과 글쓰기", "주제 탐구 독서"]},
    },
    "보건·간호": {
        "desc": "간호학, 보건학, 물리치료, 임상병리 등 보건의료 계열",
        "1학기": {"택3": ["고급 생명과학", "고급 화학", "윤리문제 탐구"], "택1": "보건", "택4": ["영어독해와 작문", "화법과 언어", "고급 미적분", "문학 감상과 비평"]},
        "2학기": {"택3": ["생명과학 실험", "화학 실험", "사회문제 탐구"], "택1": "간호의 기초", "택4": ["독서 토론과 글쓰기", "영어 발표와 토론", "주제 탐구 독서", "수학과제 탐구"]},
    },
    "자연과학 (수학·물리·화학·생명·지구과학)": {
        "desc": "기초과학 연구, 수학과, 물리학과, 화학과, 생명과학, 지구과학 등",
        "1학기": {"택3": ["고급 물리학", "고급 화학", "고급 생명과학"], "택1": "데이터 과학", "택4": ["고급 미적분", "고급 대수", "영어독해와 작문", "화법과 언어"]},
        "2학기": {"택3": ["생명과학 실험", "화학 실험", "융합과학 탐구"], "택1": "생태와 환경", "택4": ["수학과제 탐구", "영어 발표와 토론", "독서 토론과 글쓰기", "주제 탐구 독서"]},
    },
    "인문·사회 (인문학·사회학·심리학)": {
        "desc": "국문학, 사학, 철학, 사회학, 심리학, 사회복지 등",
        "1학기": {"택3": ["정치", "법과 사회", "윤리문제 탐구"], "택1": "인간과 심리", "택4": ["화법과 언어", "문학 감상과 비평", "영어독해와 작문", "경제 수학"]},
        "2학기": {"택3": ["사회문제 탐구", "역사로 탐구하는 현대 세계", "국제 관계의 이해"], "택1": "인간과 철학", "택4": ["독서 토론과 글쓰기", "주제 탐구 독서", "영어 발표와 토론", "수학과 문화"]},
    },
    "법·정치·행정": {
        "desc": "법학, 정치외교학, 행정학, 공공정책, 공무원 등",
        "1학기": {"택3": ["정치", "법과 사회", "금융과 경제 생활"], "택1": "인간과 심리", "택4": ["화법과 언어", "영어독해와 작문", "문학 감상과 비평", "경제 수학"]},
        "2학기": {"택3": ["국제 관계의 이해", "사회문제 탐구", "역사로 탐구하는 현대 세계"], "택1": "인간과 철학", "택4": ["독서 토론과 글쓰기", "주제 탐구 독서", "영어 발표와 토론", "세계 문화와 영어"]},
    },
    "상경계 (경영·경제·금융·회계)": {
        "desc": "경영학, 경제학, 금융, 회계, 무역, 세무 등",
        "1학기": {"택3": ["금융과 경제 생활", "정치", "법과 사회"], "택1": "데이터 과학", "택4": ["경제 수학", "영어독해와 작문", "화법과 언어", "심화 영어"]},
        "2학기": {"택3": ["국제 관계의 이해", "사회문제 탐구", "기후변화와 지속가능한 세계"], "택1": "인간과 철학", "택4": ["독서 토론과 글쓰기", "영어 발표와 토론", "주제 탐구 독서", "세계 문화와 영어"]},
    },
    "교육 (사범대·교직)": {
        "desc": "초등교육, 국어교육, 영어교육, 수학교육, 특수교육, 유아교육 등",
        "1학기": {"택3": ["윤리문제 탐구", "정치", "법과 사회"], "택1": "교육의 이해", "택4": ["화법과 언어", "문학 감상과 비평", "영어독해와 작문", "경제 수학"]},
        "2학기": {"택3": ["사회문제 탐구", "역사로 탐구하는 현대 세계", "기후변화와 지속가능한 세계"], "택1": "인간과 철학", "택4": ["독서 토론과 글쓰기", "주제 탐구 독서", "영어 발표와 토론", "수학과 문화"]},
    },
    "어문·외국어 (영문·국문·통번역)": {
        "desc": "영어영문학, 국어국문학, 통번역, 언어학 등",
        "1학기": {"택3": ["정치", "윤리문제 탐구", "법과 사회"], "택1": "인간과 심리", "택4": ["심화 영어", "영어독해와 작문", "화법과 언어", "문학 감상과 비평"]},
        "2학기": {"택3": ["국제 관계의 이해", "역사로 탐구하는 현대 세계", "사회문제 탐구"], "택1": "인간과 철학", "택4": ["영어 발표와 토론", "독서 토론과 글쓰기", "주제 탐구 독서", "세계 문화와 영어"]},
    },
    "국제·외교 (국제학·외교·국제기구)": {
        "desc": "국제학, 정치외교학, 국제통상, 국제기구, NGO 등",
        "1학기": {"택3": ["정치", "금융과 경제 생활", "법과 사회"], "택1": "중국 문화", "택4": ["심화 영어", "영어독해와 작문", "화법과 언어", "경제 수학"]},
        "2학기": {"택3": ["국제 관계의 이해", "기후변화와 지속가능한 세계", "역사로 탐구하는 현대 세계"], "택1": "심화 중국어", "택4": ["영어 발표와 토론", "세계 문화와 영어", "독서 토론과 글쓰기", "주제 탐구 독서"]},
    },
    "환경·도시·건축": {
        "desc": "환경공학, 도시계획, 건축학, 조경, 토목 등",
        "1학기": {"택3": ["도시의 미래 탐구", "고급 물리학", "고급 화학"], "택1": "데이터 과학", "택4": ["고급 미적분", "영어독해와 작문", "화법과 언어", "고급 대수"]},
        "2학기": {"택3": ["기후변화와 지속가능한 세계", "기후변화와 환경생태", "융합과학 탐구"], "택1": "생태와 환경", "택4": ["수학과제 탐구", "독서 토론과 글쓰기", "영어 발표와 토론", "주제 탐구 독서"]},
    },
    "미디어·언론·광고": {
        "desc": "신문방송학, 미디어학, 광고홍보, 영상, 콘텐츠 등",
        "1학기": {"택3": ["정치", "법과 사회", "윤리문제 탐구"], "택1": "인간과 심리", "택4": ["미디어 영어", "화법과 언어", "문학 감상과 비평", "영어독해와 작문"]},
        "2학기": {"택3": ["사회문제 탐구", "역사로 탐구하는 현대 세계", "국제 관계의 이해"], "택1": "인간과 철학", "택4": ["독서 토론과 글쓰기", "영어 발표와 토론", "주제 탐구 독서", "세계 문화와 영어"]},
    },
    "관광·호텔·항공": {
        "desc": "관광경영, 호텔경영, 항공서비스 등",
        "1학기": {"택3": ["금융과 경제 생활", "정치", "도시의 미래 탐구"], "택1": "일본 문화", "택4": ["심화 영어", "영어독해와 작문", "화법과 언어", "미디어 영어"]},
        "2학기": {"택3": ["여행지리", "국제 관계의 이해", "기후변화와 지속가능한 세계"], "택1": "심화 일본어", "택4": ["세계 문화와 영어", "영어 발표와 토론", "독서 토론과 글쓰기", "주제 탐구 독서"]},
    },
    "예체능 (음악·체육·미술)": {
        "desc": "음악, 체육, 미술, 실용음악, 체육교육, 무용 등",
        "1학기": {"택3": ["윤리문제 탐구", "정치", "도시의 미래 탐구"], "택1": "인간과 심리", "택4": ["음악연주와 창작", "스포츠 생활2", "영어독해와 작문", "화법과 언어"]},
        "2학기": {"택3": ["사회문제 탐구", "기후변화와 지속가능한 세계", "역사로 탐구하는 현대 세계"], "택1": "인간과 철학", "택4": ["음악감상과 비평", "스포츠 경기 기술", "독서 토론과 글쓰기", "주제 탐구 독서"]},
    },
}

GRP_COUNT = {"택3": 3, "택1": 1, "택4": 4}
GRP_ORDER = ["택3", "택1", "택4"]
SEM_INFO = [("📘 3학년 1학기", "3-1", "1학기"), ("📗 3학년 2학기", "3-2", "2학기")]

# ============================================================
# 희망 직업 → 진로 계열 매핑
# ============================================================
JOB_TO_TRACKS = {
    "의사": ["의약계", "자연과학"], "간호사": ["보건간호", "의약계"],
    "프로그래머": ["IT", "이공계"], "개발자": ["IT", "이공계"],
    "변호사": ["법·정치", "인문사회"], "교사": ["교육", "인문사회"],
    "회계사": ["상경계", "경제금융"], "기자": ["미디어", "인문사회"],
    "건축": ["환경도시", "이공계"], "외교관": ["국제외교", "법·정치"],
    "약사": ["의약계", "자연과학"], "치과의사": ["의약계", "자연과학"],
    "한의사": ["의약계", "자연과학"], "수의사": ["의약계", "자연과학"],
    "물리치료사": ["보건간호", "의약계"], "방사선사": ["보건간호", "의약계"],
    "임상병리사": ["보건간호", "의약계"], "영양사": ["보건간호", "생활과학"],
    "공무원": ["행정", "법·정치"], "경찰": ["법·정치", "행정"],
    "소방관": ["행정", "보건간호"], "군인": ["행정", "이공계"],
    "판사": ["법·정치", "인문사회"], "검사": ["법·정치", "인문사회"],
    "세무사": ["상경계", "경제금융"], "관세사": ["상경계", "국제외교"],
    "은행원": ["상경계", "경제금융"], "펀드매니저": ["상경계", "경제금융"],
    "경영": ["상경계", "경제금융"], "마케팅": ["상경계", "미디어"],
    "디자이너": ["예체능", "미디어"], "작가": ["어문계", "인문사회"],
    "아나운서": ["미디어", "어문계"], "PD": ["미디어", "예체능"],
    "영화감독": ["미디어", "예체능"], "배우": ["예체능", "미디어"],
    "음악가": ["예체능", "교육"], "체육": ["예체능", "교육"],
    "통역사": ["어문계", "국제외교"], "번역가": ["어문계", "국제외교"],
    "상담사": ["교육", "인문사회"], "심리학자": ["인문사회", "교육"],
    "사회복지사": ["인문사회", "교육"], "연구원": ["자연과학", "이공계"],
    "교수": ["교육", "자연과학"], "과학자": ["자연과학", "이공계"],
    "엔지니어": ["이공계", "자연과학"], "반도체": ["이공계", "자연과학"],
    "로봇": ["이공계", "IT"], "항공": ["이공계", "관광"],
    "조종사": ["이공계", "관광"], "승무원": ["관광", "어문계"],
    "호텔리어": ["관광", "어문계"], "관광가이드": ["관광", "어문계"],
    "환경": ["환경도시", "자연과학"], "도시계획": ["환경도시", "건축"],
    "조경": ["환경도시", "자연과학"], "토목": ["환경도시", "이공계"],
    "데이터": ["IT", "상경계"], "AI": ["IT", "이공계"],
    "보험": ["상경계", "경제금융"], "유튜버": ["미디어", "IT"],
    "웹디자이너": ["IT", "미디어"], "게임": ["IT", "예체능"],
    "수학": ["이공계", "자연과학"], "과학": ["자연과학", "이공계"],
    "물리": ["이공계", "자연과학"], "화학": ["자연과학", "의약계"],
    "생명": ["의약계", "자연과학"], "지구": ["환경도시", "자연과학"],
    "국어": ["어문계", "인문사회"], "영어": ["어문계", "국제외교"],
    "역사": ["인문사회"], "지리": ["인문사회", "관광"],
    "사회": ["인문사회"], "윤리": ["인문사회", "철학윤리"],
    "음악": ["예체능", "교육"], 
    "미술": ["예체능", "교육"], 
    "체육": ["예체능", "교육"], 
    "정보": ["IT", "이공계", "교육"],
    "컴퓨터": ["IT", "이공계", "교육"],
    "보건": ["보건간호", "의약계", "교육"],
}

SUBJECTS = ["국어", "수학", "영어", "과학", "사회"]

# ============================================================
# AI 점수 엔진
# ============================================================
def score_career(course_name, course, profile):
    if not profile["career_tracks"]:
        return 50
        
    # 1. 과목에 설정된 자체 태그 검사
    p_tracks_str = " ".join(profile["career_tracks"])
    for t in course["tracks"]:
        if t in p_tracks_str:
            return 100
            
    # 🚨 [새로 추가된 로직] 희망 직업(dream_job) 키워드 텍스트 직접 매칭!
    job = profile.get("dream_job", "").strip().replace(" ", "")
    if job:
        kw_all = course.get("kw", []) + [course_name]
        # 예: 과목 키워드("영어")가 희망 직업("영어교사")에 들어있으면 무조건 진로 만점!
        if any(job in kw or kw in job for kw in kw_all):
            return 100

    # 3. TRACK_COMBOS 추천 목록에 들어있는 과목인지 검사
    for trk in profile["career_tracks"]:
        if trk in TRACK_COMBOS:
            combo = TRACK_COMBOS[trk]
            for sem in ["1학기", "2학기"]:
                for grp in ["택3", "택1", "택4"]:
                    items = combo[sem][grp]
                    if isinstance(items, list):
                        if course_name in items: return 100
                    else:
                        if course_name == items: return 100
                        
    return 0

def score_affinity(course, profile):
    aff = course["aff"]
    score, total_w = 0, 0
    for subj, weight in aff.items():
        if weight == 0:
            continue
        total_w += weight
        grade_norm = (6 - profile["grades"].get(subj, 3)) / 5
        like_bonus = 0.3 if subj in profile["likes"] else 0
        dislike_pen = -0.4 if subj in profile["dislikes"] else 0
        score += (grade_norm + like_bonus + dislike_pen) * weight
        
    # 🚨 수정 포인트 1: 국영수과사 반영이 0인 체육 같은 과목이 
    # 기본 50점을 받아 억울하게 점수가 깎이는 걸 막기 위해 기본점수를 80점으로 상향!
    return max(0, min(100, (score / total_w) * 100)) if total_w else 80

def score_learning_style(course, profile):
    style = profile["learning_style"]
    if style == "골고루":
        return 70
    style_map = {"암기": "mem", "이해": "und", "실습": "pra"}
    return course.get(style_map.get(style, "und"), 0.5) * 100

def score_eval(course, profile):
    pref = profile["eval_pref"]
    if pref == "상관없어요":
        return 70
    is_abs = "절대" in course["eval"]
    if pref == "절대평가가 편해요" and is_abs:
        return 100
    if pref == "상대평가도 괜찮아요" and not is_abs:
        return 80
    if pref == "절대평가가 편해요" and not is_abs:
        return 30
    return 60

def score_workload(course, profile):
    diff = abs(course["wl"] - profile["workload_pref"])
    return max(0, 100 - diff * 25)

def score_grade_comp(course, profile):
    sens = profile["grade_sens"]
    gc_map = {"낮음": 90, "보통": 60, "높음": 30}
    base = gc_map.get(course["gc"], 60)
    return 70 + (base - 70) * (sens / 5)

def calc_total_score(course_name, course, profile):
    weights = {"career": 0.35, "affinity": 0.25, "style": 0.10, "eval": 0.10, "workload": 0.10, "grade": 0.10}
    scores = {
        "career": score_career(course_name, course, profile),
        "affinity": score_affinity(course, profile),
        "style": score_learning_style(course, profile),
        "eval": score_eval(course, profile),
        "workload": score_workload(course, profile),
        "grade": score_grade_comp(course, profile),
    }
    total = sum(scores[k] * weights[k] for k in weights)
    
    if profile["career_tracks"] and scores["career"] == 0:
        total *= 0.7  
        
    job = profile.get("dream_job", "").strip().replace(" ", "")
    if job:
        kw_all = course.get("kw", []) + [course_name]
        if any(kw in job or job in kw for kw in kw_all):
            # 🚨 수정 포인트 2: 희망 직업("체육")과 키워드("체육")가 겹치면 
            # 가산점을 무려 +15점 줘서 음악, 미술을 제치고 압도적 1위를 하도록 세팅!
            total = min(100, total + 15) 
            
    return round(total, 1), scores

def generate_explanation(course_name, course, scores, profile):
    reasons, warnings = [], []
    if scores["career"] >= 70:
        reasons.append("선택한 진로 계열과 높은 연관성이 있어요")
    if scores["affinity"] >= 70:
        top_subj = max(course["aff"], key=course["aff"].get)
        reasons.append(f"{top_subj} 실력이 뒷받침되어 잘 맞아요")
    elif scores["affinity"] >= 50:
        reasons.append("기초 과목 성적과 적절히 매칭돼요")
    if scores["style"] >= 70:
        reasons.append("선호하는 학습 방식과 잘 맞아요")
    if scores["eval"] >= 80:
        reasons.append("선호하는 평가 방식이에요")
    if scores["grade"] >= 80 and profile["grade_sens"] >= 3:
        reasons.append("등급 받기에 비교적 유리해요")
    if scores["workload"] >= 80:
        reasons.append("원하는 공부 부담 수준과 잘 맞아요")
    if not reasons:
        reasons.append("전반적으로 균형 잡힌 선택이에요")
        
    for subj, min_g in course.get("rmg", {}).items():
        student_g = profile["grades"].get(subj, 3)
        if student_g > min_g:
            warnings.append(f"{subj} 현재 {student_g}등급 — 기초가 부족하면 어려울 수 있어요")
    if scores["workload"] < 40:
        warnings.append("원하는 부담 수준보다 학습량이 많을 수 있어요")
    if course["diff"] >= 4 and scores["affinity"] < 50:
        warnings.append("난이도가 높은 과목이라 관련 기초 과목 성적을 확인해보세요")
        
    # 🚨 [추가된 로직] 경고 문구 추가
    if profile["career_tracks"] and scores["career"] == 0:
        warnings.append("선택하신 희망 진로 계열과 무관한 과목입니다. 단순 성적 관리가 목적이 아니라면 재고해보세요.")
        
    return reasons, warnings
# ============================================================
# 렌더링 함수
# ============================================================
def render_card(name, info, is_rec=False):
    cls = "course-card rec" if is_rec else "course-card"
    ev_cls = "badge-eval-rel" if "상대" in info["eval"] else "badge-eval-abs"
    rec = '<span class="badge badge-rec">⭐ 추천</span> ' if is_rec else ""
    tracks = "".join(f'<span class="badge badge-track">{t}</span>' for t in info["tracks"])
    
    # 🚨 여기부터 들여쓰기 절대 금지! 🚨
    st.markdown(f"""<div class="{cls}">
<div class="course-name">{rec}{name}</div>
<div style="margin-bottom:0.4rem;"><span class="badge badge-group">{info["grp"]} · {info["cr"]}학점</span><span class="badge {ev_cls}">{info["eval"]}</span></div>
<div class="course-desc">{info["desc"]}</div><div>{tracks}</div>
</div>""", unsafe_allow_html=True)

def render_group(sem_filter, grp, rec_names):
    items = {k: v for k, v in COURSES.items() if v["sem"] == sem_filter and v["grp"] == grp}
    recs = {k: v for k, v in items.items() if k in rec_names}
    others = {k: v for k, v in items.items() if k not in rec_names}
    for n, i in recs.items():
        render_card(n, i, True)
    if others:
        with st.expander(f"나머지 {len(others)}개 과목 보기"):
            for n, i in others.items():
                render_card(n, i, False)

def render_combo_summary(combo):
    for sem_label, sem_filter, _ in SEM_INFO:
            st.markdown(f'<div class="semester-title">{sem_label}</div>', unsafe_allow_html=True)
            for grp in GRP_ORDER:
                grp_courses = {k: v for k, v in COURSES.items() if v["sem"] == sem_filter and v["grp"] == grp}
                if not grp_courses:
                    continue
                    
                # 1. 점수순 정렬
                sorted_courses = sorted(grp_courses.keys(), key=lambda x: all_scores[x]["total"], reverse=True)
                pick_count = GRP_COUNT[grp]
                
                # 🚨 [추가된 로직] 동점자 처리를 위한 커트라인(문닫고 들어가는) 점수 확인
                if len(sorted_courses) >= pick_count:
                    cut_off_score = all_scores[sorted_courses[pick_count - 1]]["total"]
                else:
                    cut_off_score = -1

                # 🚨 [추가된 로직] 커트라인 점수 이상인 과목은 모두 '상위 추천'으로, 미만은 '나머지'로 분리
                top_courses = [c for c in sorted_courses if all_scores[c]["total"] >= cut_off_score]
                remaining = [c for c in sorted_courses if all_scores[c]["total"] < cut_off_score]

                st.markdown(f'<div class="group-title">📌 {grp} 그룹 — {pick_count}개 선택</div>', unsafe_allow_html=True)
                
                # 동점자 때문에 추천 개수가 늘어났다면 안내 문구도 센스있게 변경!
                if len(top_courses) > pick_count:
                    st.caption(f"🏆 상위 추천 과목 (동점 포함 총 {len(top_courses)}개)")
                else:
                    st.caption(f"🏆 상위 {pick_count}개 추천 과목")

                # 상위 추천 과목 출력 (동점자 모두 포함)
                for rank, cname in enumerate(top_courses, 1):
                    sc = all_scores[cname]
                    render_ai_card(rank, cname, COURSES[cname], sc["total"], sc["breakdown"], sc["reasons"], sc["warnings"])

                # 나머지 과목은 접어두기
                if remaining:
                    with st.expander(f"나머지 {len(remaining)}개 과목 보기"):
                        for i, cname in enumerate(remaining):
                            # 순위 번호가 이어서 나오도록 계산
                            rank = len(top_courses) + i + 1 
                            sc = all_scores[cname]
                            render_ai_card(rank, cname, COURSES[cname], sc["total"], sc["breakdown"], sc["reasons"], sc["warnings"])

def get_rec_names(combo):
    names = set()
    for sk in ["1학기", "2학기"]:
        s = combo[sk]
        names.update(s["택3"])
        names.add(s["택1"])
        names.update(s["택4"])
    return names

def render_ai_card(rank, name, info, total_score, scores, reasons, warnings):
    cls = "ai-card top" if rank <= 3 else "ai-card"
    sc_cls = "high" if total_score >= 70 else ("mid" if total_score >= 50 else "low")
    ev_cls = "badge-eval-rel" if "상대" in info["eval"] else "badge-eval-abs"
    tracks_html = "".join(f'<span class="badge badge-track">{t}</span>' for t in info["tracks"])
    reasons_html = "".join(f"<li>{r}</li>" for r in reasons)
    warnings_html = "".join(f"<li>⚠️ {w}</li>" for w in warnings)
    warn_block = f'<div class="ai-warning"><ul style="margin:0;padding-left:1.2rem;">{warnings_html}</ul></div>' if warnings else ""
    
    # 🚨 여기부터 들여쓰기 절대 금지! 🚨
    st.markdown(f"""<div class="{cls}">
<div style="display:flex;align-items:center;margin-bottom:0.4rem;">
<span class="ai-score {sc_cls}">{total_score}점</span>
<span class="course-name" style="margin-bottom:0;">{name}</span>
</div>
<div style="margin-bottom:0.5rem;">
<div class="score-bar-bg"><div class="score-bar-fill {sc_cls}" style="width:{total_score}%;"></div></div>
</div>
<div style="margin-bottom:0.4rem;">
<span class="badge badge-group">{info["grp"]} · {info["cr"]}학점</span>
<span class="badge {ev_cls}">{info["eval"]}</span>
{tracks_html}
</div>
<div class="course-desc">{info["desc"]}</div>
<div class="ai-reason"><b>추천 이유:</b><ul style="margin:0.2rem 0 0;padding-left:1.2rem;">{reasons_html}</ul></div>
{warn_block}
</div>""", unsafe_allow_html=True)

# ============================================================
# 기본 세팅 (앱 최초 실행 시 빈 화면 방지)
# ============================================================
if "profile" not in st.session_state:
    st.session_state.profile = {
        "dream_job": "",
        "career_tracks": [],
        "grades": {subj: 3 for subj in SUBJECTS},
        "likes": [],
        "dislikes": [],
        "learning_style": "골고루",
        "eval_pref": "상관없어요",
        "workload_pref": 3,
        "grade_sens": 3,
    }

# ============================================================
# 사이드바 프로필 폼
# ============================================================
st.sidebar.markdown("### 🤖 나의 프로필 설정")
st.sidebar.caption("프로필을 입력하면 AI 맞춤 추천을 받을 수 있어요!")

with st.sidebar.form("profile_form"):
    st.markdown("**🎯 진로**")
    dream_job = st.text_input("희망 직업", placeholder="예: 프로그래머, 간호사, 교사 ...")
    career_tracks = st.multiselect("관심 계열 (복수 선택 가능)", list(TRACK_COMBOS.keys()))
    st.markdown("---")
    st.markdown("**📊 현재 성적 (2학년 기준)**")
    grades = {}
    gcols = st.columns(len(SUBJECTS))
    for i, subj in enumerate(SUBJECTS):
        with gcols[i]:
            grades[subj] = st.selectbox(subj, list(range(1, 6)), index=2, key=f"g_{subj}")
    st.markdown("---")
    st.markdown("**💡 과목 호불호**")
    likes = st.multiselect("좋아하는/잘하는 영역", SUBJECTS, key="likes")
    dislikes = st.multiselect("싫어하는/어려운 영역", SUBJECTS, key="dislikes")
    st.markdown("---")
    st.markdown("**📝 학습 스타일**")
    learning_style = st.radio("선호하는 학습 방식", ["암기", "이해", "실습", "골고루"], index=3, horizontal=True)
    eval_pref = st.radio("평가 방식 선호", ["상대평가도 괜찮아요", "절대평가가 편해요", "상관없어요"], index=2)
    workload_pref = st.slider("공부 부담 수준", 1, 5, 3, help="1=여유롭게, 5=빡빡하게")
    grade_sens = st.slider("내신 등급 중요도", 1, 5, 3, help="1=배우고 싶은 거 위주, 5=등급 유리한 과목 위주")
    submitted = st.form_submit_button("🚀 AI 추천 받기", use_container_width=True)

if submitted:
    auto_tracks = set()
    for job_kw, trk_list in JOB_TO_TRACKS.items():
        if dream_job and job_kw in dream_job:
            auto_tracks.update(trk_list)
    all_track_names = set(career_tracks)
    for at in auto_tracks:
        for tk in TRACK_COMBOS:
            if at in tk:
                all_track_names.add(tk)
    st.session_state.profile = {
        "dream_job": dream_job, "career_tracks": list(all_track_names),
        "grades": grades, "likes": likes, "dislikes": dislikes,
        "learning_style": learning_style, "eval_pref": eval_pref,
        "workload_pref": workload_pref, "grade_sens": grade_sens,
    }

# ============================================================
# UI
# ============================================================
st.markdown("""<div class="main-header"><h1>📚 삼괴고 3학년 선택과목 가이드</h1>
<p>2025학년도 입학생 교육과정 편제 기준 · 진로별 추천 조합 & AI 맞춤 추천</p></div>""", unsafe_allow_html=True)

# 🚨 메인 페이지 상단 안내/경고 문구 추가
st.markdown("""
<div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-left: 6px solid #f59e0b; border-radius: 8px; padding: 1.2rem 1.5rem; margin-bottom: 2rem;">
    <div style="font-size: 1.15rem; font-weight: 700; color: #b45309; margin-bottom: 0.4rem;">
        ⚠️ 과목 선택 전 반드시 읽어주세요!
    </div>
    <div style="color: #92400e; font-size: 0.95rem; line-height: 1.6;">
        본 가이드 및 AI 맞춤 추천 결과는 학생 여러분의 선택을 돕기 위한 <b>참고자료</b>일 뿐입니다.<br>
        최종 과목 선택은 본인의 희망 진로, 목표 대학의 입시 요강을 꼼꼼히 확인하고, <b>교과 담당 선생님 및 담임 선생님, 부모님 등과 충분한 상담을 통해 신중하게 결정</b>하시기 바랍니다.
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI 맞춤 추천", "🎯 진로별 추천 조합", "🔍 키워드 검색", "📋 전체 과목 보기"])

# ── 탭1 ──
with tab1:
    profile = st.session_state.get("profile")
    if not profile:
        st.markdown("""<div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">🤖</div>
            <h3 style="color:#1a365d;">AI 맞춤 추천을 받아보세요!</h3>
            <p style="color:#64748b;font-size:0.95rem;max-width:500px;margin:0.5rem auto;">
                왼쪽 사이드바에서 <b>나의 프로필</b>을 입력하고<br>
                <b>AI 추천 받기</b> 버튼을 눌러주세요.</p></div>""", unsafe_allow_html=True)
    else:
        # Profile summary banner
        strong_subjs = sorted(profile["grades"].items(), key=lambda x: x[1])[:2]
        strong_text = ", ".join(f"{s} {g}등급" for s, g in strong_subjs)
        track_text = ", ".join(profile["career_tracks"][:3]) if profile["career_tracks"] else "미선택"
        job_text = profile["dream_job"] if profile["dream_job"] else "미입력"
        st.markdown(f"""<div class="ai-profile-banner">
            <h3>📊 나의 프로필 분석 결과</h3>
            <p>🎯 희망 직업: <b>{job_text}</b> | 관심 계열: <b>{track_text}</b></p>
            <p>💪 강점 과목: <b>{strong_text}</b> | 학습 성향: <b>{profile["learning_style"]}</b> 중심</p>
            <p>📈 등급 중요도: <b>{"★" * profile["grade_sens"]}{"☆" * (5 - profile["grade_sens"])}</b> | 부담 수준: <b>{"▮" * profile["workload_pref"]}{"▯" * (5 - profile["workload_pref"])}</b></p>
        </div>""", unsafe_allow_html=True)

        # Calculate all scores
        all_scores = {}
        for name, info in COURSES.items():
            total, breakdown = calc_total_score(name, info, profile)
            reasons, warnings = generate_explanation(name, info, breakdown, profile)
            all_scores[name] = {"total": total, "breakdown": breakdown, "reasons": reasons, "warnings": warnings}

        # Display by semester and group
        for sem_label, sem_filter, _ in SEM_INFO:
            st.markdown(f'<div class="semester-title">{sem_label}</div>', unsafe_allow_html=True)
            for grp in GRP_ORDER:
                grp_courses = {k: v for k, v in COURSES.items() if v["sem"] == sem_filter and v["grp"] == grp}
                if not grp_courses:
                    continue
                sorted_courses = sorted(grp_courses.keys(), key=lambda x: all_scores[x]["total"], reverse=True)
                pick_count = GRP_COUNT[grp]
                st.markdown(f'<div class="group-title">📌 {grp} 그룹 — {pick_count}개 선택</div>', unsafe_allow_html=True)
                st.caption(f"🏆 상위 {pick_count}개 추천 과목")
                for rank, cname in enumerate(sorted_courses, 1):
                    sc = all_scores[cname]
                    if rank <= pick_count:
                        render_ai_card(rank, cname, COURSES[cname], sc["total"], sc["breakdown"], sc["reasons"], sc["warnings"])
                    else:
                        break
                remaining = sorted_courses[pick_count:]
                if remaining:
                    with st.expander(f"나머지 {len(remaining)}개 과목 보기"):
                        for rank, cname in enumerate(remaining, pick_count + 1):
                            sc = all_scores[cname]
                            render_ai_card(rank, cname, COURSES[cname], sc["total"], sc["breakdown"], sc["reasons"], sc["warnings"])

# ── 탭2 ──
with tab2:
    sel = st.selectbox("관심 진로를 선택하세요", list(TRACK_COMBOS.keys()))
    combo = TRACK_COMBOS[sel]
    rec_names = get_rec_names(combo)

    st.markdown(f'<div class="combo-box"><div class="combo-title">🎯 {sel}</div><div class="course-desc" style="margin-bottom:0.8rem;">{combo["desc"]}</div>', unsafe_allow_html=True)
    render_combo_summary(combo)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 과목 상세 정보")
    st.caption("⭐ 추천 과목이 상단에, 같은 그룹의 나머지 과목은 펼쳐서 볼 수 있습니다.")

    for sem_label, sem_filter, _ in SEM_INFO:
        st.markdown(f'<div class="semester-title">{sem_label}</div>', unsafe_allow_html=True)
        for grp in GRP_ORDER:
            st.markdown(f'<div class="group-title">📌 {grp} 그룹 — {GRP_COUNT[grp]}개 선택</div>', unsafe_allow_html=True)
            render_group(sem_filter, grp, rec_names)

# ── 탭3 ──
with tab3:
    q = st.text_input("키워드를 입력하세요", placeholder="예: 의대, 반도체, 외교, 코딩, 간호 ...")
    st.caption("쉼표로 여러 키워드를 입력할 수 있어요")
    if q.strip():
        qs = [x.strip().lower() for x in q.split(",") if x.strip()]
        matched = set()
        for name, info in COURSES.items():
            txt = (name + " " + info["desc"] + " " + " ".join(info["kw"]) + " " + " ".join(info["tracks"])).lower()
            if any(kw in txt for kw in qs):
                matched.add(name)
        st.markdown(f'<p style="color:#64748b;font-size:0.9rem;">총 <b>{len(matched)}개</b> 과목이 검색되었습니다.</p>', unsafe_allow_html=True)
        if matched:
            for sem_label, sem_filter, _ in SEM_INFO:
                sem_match = {k for k in matched if COURSES[k]["sem"] == sem_filter}
                if not sem_match:
                    continue
                st.markdown(f'<div class="semester-title">{sem_label}</div>', unsafe_allow_html=True)
                grps = sorted({COURSES[k]["grp"] for k in sem_match}, key=lambda x: GRP_ORDER.index(x))
                for grp in grps:
                    st.markdown(f'<div class="group-title">📌 {grp} 그룹 — {GRP_COUNT[grp]}개 선택</div>', unsafe_allow_html=True)
                    render_group(sem_filter, grp, matched)
        else:
            st.warning("검색 조건에 맞는 과목이 없습니다. 다른 키워드를 시도해보세요.")
    else:
        st.info("👆 키워드를 입력하면 관련 과목을 검색하고, 같은 선택 그룹의 나머지 과목도 함께 보여줍니다.")

# ── 탭4 ──
with tab4:
    c1, c2, c3 = st.columns(3)
    with c1:
        sr = st.checkbox("5등급 상대평가 과목", True, key="a_r")
    with c2:
        sa = st.checkbox("절대평가 과목", True, key="a_a")
    with c3:
        sp = st.checkbox("P/F 과목", True, key="a_p")
    for sem_label, sem_filter, _ in SEM_INFO:
        st.markdown(f'<div class="semester-title">{sem_label}</div>', unsafe_allow_html=True)
        for grp in GRP_ORDER:
            st.markdown(f'<div class="group-title">📌 {grp} 그룹 — {GRP_COUNT[grp]}개 선택</div>', unsafe_allow_html=True)
            for name, info in COURSES.items():
                if info["sem"] != sem_filter or info["grp"] != grp:
                    continue
                if "상대" in info["eval"] and not sr:
                    continue
                if "절대" in info["eval"] and not sa:
                    continue
                if "P/F" in info["eval"] and not sp:
                    continue
                render_card(name, info)

st.markdown("""<div style="text-align:center;color:#94a3b8;font-size:0.8rem;padding:1rem 0;">
삼괴고등학교 교육과정부 · 2025학년도 입학생 교육과정 편제표 기준<br>
해당 내용은 어디까지나 참고 자료일 뿐, 꼭 해당 과목으로 선택해야 하는 것은 아닙니다<br>
※ 과목별 상세 내용은 담당 교과 선생님께 문의하세요</div>""", unsafe_allow_html=True)
