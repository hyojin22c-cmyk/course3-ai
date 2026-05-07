/* ============================================================
   AI 점수 엔진 — app.py의 점수 함수들을 1:1 포팅
   profile = {
     dream_job: string,
     career_tracks: string[],
     grades: { [subject: string]: number(1-5) },
     likes: string[], dislikes: string[],
     learning_style: "암기"|"이해"|"실습"|"골고루",
     eval_pref: "절대평가가 편해요"|"상대평가도 괜찮아요"|"상관없어요",
     workload_pref: number(1-5),
     grade_sens: number(1-5)
   }
   ============================================================ */

function scoreCareer(courseName, course, profile) {
  if (!profile.career_tracks || profile.career_tracks.length === 0) return 50;
  for (const trk of profile.career_tracks) {
    if (trk in TRACK_COMBOS) {
      const combo = TRACK_COMBOS[trk];
      for (const sem of Object.keys(combo)) {
        if (sem === "desc") continue;
        for (const grp of Object.keys(combo[sem])) {
          const items = combo[sem][grp];
          if (Array.isArray(items)) {
            if (items.includes(courseName)) return 100;
          } else {
            if (courseName === items) return 100;
          }
        }
      }
    }
  }
  const job = (profile.dream_job || "").trim().replace(/ /g, "");
  if (job) {
    const kwAll = (course.kw || []).concat([courseName]);
    if (kwAll.some(kw => job.includes(kw) || kw.includes(job))) return 90;
  }
  const pTracksStr = profile.career_tracks.join(" ");
  for (const t of course.tracks) {
    if (pTracksStr.includes(t)) return 70;
  }
  return 0;
}

function scoreAffinity(course, profile) {
  const aff = course.aff;
  let score = 0, totalW = 0;
  for (const [subj, weight] of Object.entries(aff)) {
    if (weight === 0) continue;
    totalW += weight;
    const grade = subj in profile.grades ? profile.grades[subj] : 3;
    const gradeNorm = (6 - grade) / 5;
    const likeBonus = profile.likes.includes(subj) ? 0.3 : 0;
    const dislikePen = profile.dislikes.includes(subj) ? -0.4 : 0;
    score += (gradeNorm + likeBonus + dislikePen) * weight;
  }
  if (totalW === 0) return 80;
  return Math.max(0, Math.min(100, (score / totalW) * 100));
}

function scoreLearningStyle(course, profile) {
  const style = profile.learning_style;
  if (style === "골고루") return 70;
  const styleMap = {"암기": "mem", "이해": "und", "실습": "pra"};
  const key = styleMap[style] || "und";
  return (course[key] ?? 0.5) * 100;
}

function scoreEval(course, profile) {
  const pref = profile.eval_pref;
  if (pref === "상관없어요") return 70;
  const isAbs = course.eval.includes("절대");
  if (pref === "절대평가가 편해요" && isAbs) return 100;
  if (pref === "상대평가도 괜찮아요" && !isAbs) return 80;
  if (pref === "절대평가가 편해요" && !isAbs) return 30;
  return 60;
}

function scoreWorkload(course, profile) {
  const diff = Math.abs(course.wl - profile.workload_pref);
  return Math.max(0, 100 - diff * 25);
}

function scoreGradeComp(course, profile) {
  const sens = profile.grade_sens;
  const gcMap = {"낮음": 90, "보통": 60, "높음": 30};
  const base = course.gc in gcMap ? gcMap[course.gc] : 60;
  return 70 + (base - 70) * (sens / 5);
}

// Python 3 round(x, n)와 동일한 결과를 내도록 toFixed 사용.
// 곱셈으로 factor를 곱하면 (예: 42.55 * 10) 부동소수점 결과가 정확한 425.5로
// 떨어져버려서 Python의 round 결과와 어긋날 수 있음. toFixed는 실제 IEEE 754
// 비트 표현 기준으로 반올림하기 때문에 Python과 동일한 결과가 나옴.
function roundHalfToEven(x, digits = 1) {
  return Number(x.toFixed(digits));
}

function calcTotalScore(courseName, course, profile) {
  const weights = {career: 0.35, affinity: 0.25, style: 0.10, eval: 0.10, workload: 0.10, grade: 0.10};
  const scores = {
    career:   scoreCareer(courseName, course, profile),
    affinity: scoreAffinity(course, profile),
    style:    scoreLearningStyle(course, profile),
    eval:     scoreEval(course, profile),
    workload: scoreWorkload(course, profile),
    grade:    scoreGradeComp(course, profile),
  };
  let total = 0;
  for (const k of Object.keys(weights)) total += scores[k] * weights[k];
  if (profile.career_tracks && profile.career_tracks.length > 0 && scores.career === 0) {
    total *= 0.7;
  }
  const job = (profile.dream_job || "").trim().replace(/ /g, "");
  if (job) {
    const kwAll = (course.kw || []).concat([courseName]);
    if (kwAll.some(kw => kw.includes(job) || job.includes(kw))) {
      total = Math.min(100, total + 15);
    }
  }
  let comboBonus = 0;
  for (const trk of (profile.career_tracks || [])) {
    if (trk in TRACK_COMBOS) {
      const combo = TRACK_COMBOS[trk];
      for (const sem of ["1학기", "2학기"]) {
        for (const grp of Object.keys(combo[sem])) {
          const items = combo[sem][grp];
          if (Array.isArray(items)) {
            if (items.includes(courseName)) {
              const idx = items.indexOf(courseName);
              comboBonus = Math.max(comboBonus, (items.length - idx) * 2.0);
            }
          } else {
            if (courseName === items) {
              comboBonus = Math.max(comboBonus, 2.0);
            }
          }
        }
      }
    }
  }
  total = Math.min(100, total + comboBonus);
  return { total: roundHalfToEven(total, 1), scores };
}

function generateExplanation(courseName, course, scores, profile) {
  const reasons = [], warnings = [];
  if (scores.career >= 70) reasons.push("선택한 진로 계열과 높은 연관성이 있어요");
  if (scores.affinity >= 70) {
    let topSubj = null, topVal = -Infinity;
    for (const [k, v] of Object.entries(course.aff)) {
      if (v > topVal) { topVal = v; topSubj = k; }
    }
    reasons.push(`${topSubj} 실력이 뒷받침되어 잘 맞아요`);
  } else if (scores.affinity >= 50) {
    reasons.push("기초 과목 성적과 적절히 매칭돼요");
  }
  if (scores.style >= 70) reasons.push("선호하는 학습 방식과 잘 맞아요");
  if (scores.eval >= 80) reasons.push("선호하는 평가 방식이에요");
  if (scores.grade >= 80 && profile.grade_sens >= 3) reasons.push("등급 받기에 비교적 유리해요");
  if (scores.workload >= 80) reasons.push("원하는 공부 부담 수준과 잘 맞아요");
  if (reasons.length === 0) reasons.push("전반적으로 균형 잡힌 선택이에요");

  const univNote = course.univ_note || "";
  if (univNote && scores.career >= 70) reasons.push(`🎓 ${univNote}`);

  const rmg = course.rmg || {};
  for (const [subj, minG] of Object.entries(rmg)) {
    const studentG = subj in profile.grades ? profile.grades[subj] : 3;
    if (studentG > minG) {
      warnings.push(`${subj} 현재 ${studentG}등급 — 기초가 부족하면 어려울 수 있어요`);
    }
  }
  if (scores.workload < 40) warnings.push("원하는 부담 수준보다 학습량이 많을 수 있어요");
  if (course.diff >= 4 && scores.affinity < 50) warnings.push("난이도가 높은 과목이라 관련 기초 과목 성적을 확인해보세요");
  if (profile.career_tracks && profile.career_tracks.length > 0 && scores.career === 0) {
    warnings.push("선택하신 희망 진로 계열과 무관한 과목입니다. 단순 성적 관리가 목적이 아니라면 재고해보세요.");
  }
  return { reasons, warnings };
}

/* 헬퍼: 콤보에서 추천 과목명 set 추출 (render_group용) */
function getRecNames(combo) {
  const names = new Set();
  for (const sk of ["1학기", "2학기"]) {
    const s = combo[sk];
    for (const grp of Object.keys(s)) {
      const items = s[grp];
      if (Array.isArray(items)) {
        for (const x of items) names.add(x);
      } else {
        names.add(items);
      }
    }
  }
  return names;
}

/* 직업명 → 자동 매핑 트랙명 확장 */
function expandTracksFromJob(dreamJob, manualTracks) {
  const all = new Set(manualTracks || []);
  if (!dreamJob) return [...all];
  const autoTracks = new Set();
  for (const [jobKw, trkList] of Object.entries(JOB_TO_TRACKS)) {
    if (dreamJob.includes(jobKw)) {
      for (const t of trkList) autoTracks.add(t);
    }
  }
  for (const at of autoTracks) {
    for (const tk of Object.keys(TRACK_COMBOS)) {
      if (tk.includes(at)) all.add(tk);
    }
  }
  return [...all];
}
