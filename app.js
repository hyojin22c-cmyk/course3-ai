/* ============================================================
   삼괴고 3학년 선택과목 가이드 — UI 로직
   ============================================================ */

const STORAGE_KEY = "course3-ai-profile-v1";

const DEFAULT_PROFILE = {
  dream_job: "",
  career_tracks: [],
  grades: Object.fromEntries(SUBJECTS.map(s => [s, 3])),
  likes: [],
  dislikes: [],
  learning_style: "골고루",
  eval_pref: "상관없어요",
  workload_pref: 3,
  grade_sens: 3,
};

let currentProfile = null;

/* ============================================================
   유틸
   ============================================================ */
function $(sel) { return document.querySelector(sel); }
function $$(sel) { return Array.from(document.querySelectorAll(sel)); }

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "html") node.innerHTML = v;
    else if (k === "text") node.textContent = v;
    else if (k.startsWith("on") && typeof v === "function") node.addEventListener(k.slice(2), v);
    else if (v === true) node.setAttribute(k, "");
    else if (v === false || v == null) {} // skip
    else node.setAttribute(k, v);
  }
  if (!Array.isArray(children)) children = [children];
  for (const c of children) {
    if (c == null || c === false) continue;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return node;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}

/* ============================================================
   사이드바 폼 동적 채우기
   ============================================================ */
function buildSidebarForm() {
  // 관심 계열 체크박스 (드롭다운 패널 안)
  const trackBox = $("#career-tracks");
  for (const trk of Object.keys(TRACK_COMBOS)) {
    trackBox.appendChild(el("label", {}, [
      el("input", {type: "checkbox", value: trk, name: "career-track", onchange: updateCareerTracksLabel}),
      " " + trk
    ]));
  }
  setupCareerTracksDropdown();

  // 5과목 등급 셀렉트
  const gradesRow = $("#grades-row");
  for (const subj of SUBJECTS) {
    const select = el("select", {id: "grade-" + subj});
    for (let i = 1; i <= 5; i++) {
      const opt = el("option", {value: i}, String(i));
      if (i === 3) opt.selected = true;
      select.appendChild(opt);
    }
    gradesRow.appendChild(el("div", {class: "grade-cell"}, [
      el("label", {for: "grade-" + subj}, subj),
      select,
    ]));
  }

  // 좋아하는/싫어하는 영역
  for (const groupId of ["likes", "dislikes"]) {
    const box = document.getElementById(groupId);
    for (const subj of SUBJECTS) {
      box.appendChild(el("label", {}, [
        el("input", {type: "checkbox", value: subj, name: groupId}),
        " " + subj
      ]));
    }
  }

  // 슬라이더 값 표시 동기화
  for (const id of ["workload-pref", "grade-sens"]) {
    const inp = $("#" + id);
    const out = $("#" + id + "-out");
    inp.addEventListener("input", () => { out.textContent = inp.value; });
  }
}

function updateCareerTracksLabel() {
  const checked = $$('input[name="career-track"]:checked').map(i => i.value);
  const label = $("#career-tracks-trigger .dropdown-label");
  if (checked.length === 0) {
    label.textContent = "선택해주세요";
    label.classList.add("placeholder");
  } else if (checked.length === 1) {
    label.textContent = checked[0];
    label.classList.remove("placeholder");
  } else {
    label.textContent = `${checked[0]} 외 ${checked.length - 1}개`;
    label.classList.remove("placeholder");
  }
}

function setupCareerTracksDropdown() {
  const dd = $("#career-tracks-dd");
  const trigger = $("#career-tracks-trigger");
  const panel = $("#career-tracks");
  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    const open = !dd.classList.contains("open");
    dd.classList.toggle("open", open);
    panel.hidden = !open;
    trigger.setAttribute("aria-expanded", open ? "true" : "false");
  });
  // 패널 내부 클릭은 닫지 않게
  panel.addEventListener("click", (e) => e.stopPropagation());
  // 외부 클릭 시 닫기
  document.addEventListener("click", () => {
    if (dd.classList.contains("open")) {
      dd.classList.remove("open");
      panel.hidden = true;
      trigger.setAttribute("aria-expanded", "false");
    }
  });
  updateCareerTracksLabel();
}

function readSidebarForm() {
  const checkedValues = name => $$(`input[name="${name}"]:checked`).map(i => i.value);
  const grades = {};
  for (const subj of SUBJECTS) grades[subj] = parseInt($("#grade-" + subj).value, 10);
  const checkedRadio = name => {
    const el = document.querySelector(`input[name="${name}"]:checked`);
    return el ? el.value : null;
  };
  return {
    dream_job: $("#dream-job").value.trim(),
    career_tracks_raw: checkedValues("career-track"),
    grades,
    likes: checkedValues("likes"),
    dislikes: checkedValues("dislikes"),
    learning_style: checkedRadio("learning-style") || "골고루",
    eval_pref: checkedRadio("eval-pref") || "상관없어요",
    workload_pref: parseInt($("#workload-pref").value, 10),
    grade_sens: parseInt($("#grade-sens").value, 10),
  };
}

function applyProfileToForm(profile) {
  $("#dream-job").value = profile.dream_job || "";
  for (const inp of $$('input[name="career-track"]')) inp.checked = profile.career_tracks_raw?.includes(inp.value) ?? false;
  for (const subj of SUBJECTS) $("#grade-" + subj).value = profile.grades?.[subj] ?? 3;
  for (const inp of $$('input[name="likes"]')) inp.checked = profile.likes?.includes(inp.value) ?? false;
  for (const inp of $$('input[name="dislikes"]')) inp.checked = profile.dislikes?.includes(inp.value) ?? false;
  for (const inp of $$('input[name="learning-style"]')) inp.checked = inp.value === (profile.learning_style ?? "골고루");
  for (const inp of $$('input[name="eval-pref"]')) inp.checked = inp.value === (profile.eval_pref ?? "상관없어요");
  $("#workload-pref").value = profile.workload_pref ?? 3;
  $("#grade-sens").value = profile.grade_sens ?? 3;
  $("#workload-pref-out").textContent = $("#workload-pref").value;
  $("#grade-sens-out").textContent = $("#grade-sens").value;
  updateCareerTracksLabel();
}

/* ============================================================
   프로필 저장/복원
   ============================================================ */
function saveProfile(profile) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(profile)); } catch(e) {}
}
function loadProfile() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch(e) { return null; }
}

/* ============================================================
   공통 카드 렌더러 (탭2/3/4용)
   ============================================================ */
function courseCardHtml(name, info, isRec) {
  const cls = isRec ? "course-card rec" : "course-card";
  const evCls = info.eval.includes("상대") ? "badge-eval-rel" : "badge-eval-abs";
  const rec = isRec ? '<span class="badge badge-rec">⭐ 추천</span> ' : "";
  const tracks = info.tracks.map(t => `<span class="badge badge-track">${escapeHtml(t)}</span>`).join("");
  const univ = info.univ_note ? `<div class="ai-univ-note">🎓 ${info.univ_note}</div>` : "";
  return `<div class="${cls}">
    <div class="course-name">${rec}${escapeHtml(name)}</div>
    <div style="margin-bottom:0.4rem;"><span class="badge badge-group">${escapeHtml(info.grp)} · ${info.cr}학점</span><span class="badge ${evCls}">${escapeHtml(info.eval)}</span></div>
    <div class="course-desc">${escapeHtml(info.desc)}</div>
    <div>${tracks}</div>
    ${univ}
  </div>`;
}

// 같은 (sem, grp) 안에서 추천 과목은 위에, 나머지는 expander 안에
function renderGroupSection(container, semFilter, grp, recNames) {
  const items = Object.entries(COURSES).filter(([k, v]) => v.sem === semFilter && v.grp === grp);
  const recs = items.filter(([k]) => recNames.has(k));
  const others = items.filter(([k]) => !recNames.has(k));
  for (const [n, i] of recs) {
    container.insertAdjacentHTML("beforeend", courseCardHtml(n, i, true));
  }
  if (others.length) {
    const det = el("details", {class: "expander"}, [
      el("summary", {}, `나머지 ${others.length}개 과목 보기`),
    ]);
    const body = el("div", {class: "expander-body"});
    for (const [n, i] of others) body.insertAdjacentHTML("beforeend", courseCardHtml(n, i, false));
    det.appendChild(body);
    container.appendChild(det);
  }
}

/* ============================================================
   대학 가이드 박스 렌더러
   ============================================================ */
function univGuideBoxHtml(trkName, guide) {
  return `<div class="univ-guide-box">
    <div class="guide-title">${escapeHtml(guide.icon)} ${escapeHtml(trkName)} — 2028 대입 참고사항</div>
    <div class="guide-prereq">📌 <b>2학년 이수 확인:</b> ${guide.prereq}</div>
    <div class="guide-3rd">💡 <b>3학년 포인트:</b> ${guide.third}</div>
  </div>`;
}

/* ============================================================
   탭1: AI 맞춤 추천
   ============================================================ */
function renderAiTab(profile) {
  const empty = $("#ai-empty");
  const result = $("#ai-result");
  if (!profile) {
    empty.hidden = false;
    result.hidden = true;
    result.innerHTML = "";
    return;
  }
  empty.hidden = true;
  result.hidden = false;

  // 프로필 분석 배너
  const sortedGrades = [...Object.entries(profile.grades)].sort((a, b) => a[1] - b[1]).slice(0, 2);
  const strongText = sortedGrades.map(([s, g]) => `${s} ${g}등급`).join(", ");
  const trackText = profile.career_tracks.length ? profile.career_tracks.slice(0, 3).join(", ") : "미선택";
  const jobText = profile.dream_job || "미입력";
  const stars = "★".repeat(profile.grade_sens) + "☆".repeat(5 - profile.grade_sens);
  const wlBars = "▮".repeat(profile.workload_pref) + "▯".repeat(5 - profile.workload_pref);

  let html = `<div class="ai-profile-banner">
    <h3>📊 나의 프로필 분석 결과</h3>
    <p>🎯 희망 직업: <b>${escapeHtml(jobText)}</b> | 관심 계열: <b>${escapeHtml(trackText)}</b></p>
    <p>💪 강점 과목: <b>${escapeHtml(strongText)}</b> | 학습 성향: <b>${escapeHtml(profile.learning_style)}</b> 중심</p>
    <p>📈 등급 중요도: <b>${stars}</b> | 부담 수준: <b>${wlBars}</b></p>
  </div>`;

  // 대학 가이드 (최대 3개)
  if (profile.career_tracks.length) {
    const shown = profile.career_tracks.filter(t => t in TRACK_UNIV_GUIDE).slice(0, 3);
    for (const trk of shown) html += univGuideBoxHtml(trk, TRACK_UNIV_GUIDE[trk]);
  }

  // 전체 점수 계산
  const allScores = {};
  for (const [name, info] of Object.entries(COURSES)) {
    const { total, scores } = calcTotalScore(name, info, profile);
    const { reasons, warnings } = generateExplanation(name, info, scores, profile);
    allScores[name] = { total, breakdown: scores, reasons, warnings };
  }

  // 학기·그룹별 상위 추천
  for (const [semLabel, semFilter] of SEM_INFO) {
    html += `<div class="semester-title">${escapeHtml(semLabel)}</div>`;
    for (const grp of GRP_ORDER) {
      const grpCourses = Object.entries(COURSES).filter(([k, v]) => v.sem === semFilter && v.grp === grp);
      if (!grpCourses.length) continue;
      const sortedNames = grpCourses.map(([k]) => k).sort((a, b) => allScores[b].total - allScores[a].total);
      const pickCount = GRP_COUNT[grp];
      let cutOff;
      if (sortedNames.length >= pickCount) cutOff = allScores[sortedNames[pickCount - 1]].total;
      else cutOff = -1;
      const top = sortedNames.filter(c => allScores[c].total >= cutOff);
      const remaining = sortedNames.filter(c => allScores[c].total < cutOff);

      html += `<div class="group-title">📌 ${escapeHtml(grp)} 그룹 — ${pickCount}개 선택</div>`;
      const cap = top.length > pickCount
        ? `🏆 상위 추천 과목 (동점 포함 총 ${top.length}개)`
        : `🏆 상위 ${pickCount}개 추천 과목`;
      html += `<div class="group-caption">${cap}</div>`;

      for (let r = 0; r < top.length; r++) {
        html += aiCardHtml(top[r], COURSES[top[r]], allScores[top[r]], true);
      }
      if (remaining.length) {
        html += `<details class="expander"><summary>나머지 ${remaining.length}개 과목 보기</summary><div class="expander-body">`;
        for (const cname of remaining) html += aiCardHtml(cname, COURSES[cname], allScores[cname], false);
        html += `</div></details>`;
      }
    }
  }

  result.innerHTML = html;
}

function aiCardHtml(name, info, sc, isTop) {
  const cls = isTop ? "ai-card top" : "ai-card";
  const total = sc.total;
  const scCls = total >= 70 ? "high" : (total >= 50 ? "mid" : "low");
  const evCls = info.eval.includes("상대") ? "badge-eval-rel" : "badge-eval-abs";
  const tracksHtml = info.tracks.map(t => `<span class="badge badge-track">${escapeHtml(t)}</span>`).join("");
  const reasonsHtml = sc.reasons.map(r => `<li>${r}</li>`).join("");
  const warningsHtml = sc.warnings.map(w => `<li>⚠️ ${escapeHtml(w)}</li>`).join("");
  const warnBlock = sc.warnings.length ? `<div class="ai-warning"><ul style="margin:0;padding-left:1.2rem;">${warningsHtml}</ul></div>` : "";
  const univNote = info.univ_note || "";
  let univBlock = "";
  if (univNote && !sc.reasons.some(r => r.includes("🎓"))) {
    univBlock = `<div class="ai-univ-note">🎓 ${univNote}</div>`;
  }
  return `<div class="${cls}">
    <div style="display:flex;align-items:center;margin-bottom:0.4rem;">
      <span class="ai-score ${scCls}">${total}점</span>
      <span class="course-name" style="margin-bottom:0;">${escapeHtml(name)}</span>
    </div>
    <div style="margin-bottom:0.5rem;">
      <div class="score-bar-bg"><div class="score-bar-fill ${scCls}" style="width:${total}%;"></div></div>
    </div>
    <div style="margin-bottom:0.4rem;">
      <span class="badge badge-group">${escapeHtml(info.grp)} · ${info.cr}학점</span>
      <span class="badge ${evCls}">${escapeHtml(info.eval)}</span>
      ${tracksHtml}
    </div>
    <div class="course-desc">${escapeHtml(info.desc)}</div>
    <div class="ai-reason"><b>추천 이유:</b><ul style="margin:0.2rem 0 0;padding-left:1.2rem;">${reasonsHtml}</ul></div>
    ${warnBlock}
    ${univBlock}
  </div>`;
}

/* ============================================================
   탭2: 진로별 추천 조합
   ============================================================ */
function buildTrackTab() {
  const sel = $("#track-select");
  for (const trk of Object.keys(TRACK_COMBOS)) {
    sel.appendChild(el("option", {value: trk}, trk));
  }
  sel.addEventListener("change", () => renderTrackTab(sel.value));
  renderTrackTab(sel.value);
}

function renderTrackTab(track) {
  const out = $("#track-result");
  const combo = TRACK_COMBOS[track];
  const recNames = getRecNames(combo);

  let html = "";
  if (track in TRACK_UNIV_GUIDE) {
    const guide = TRACK_UNIV_GUIDE[track];
    html += `<div class="univ-guide-box">
      <div class="guide-title">${escapeHtml(guide.icon)} 2028 대입 참고사항</div>
      <div class="guide-prereq">📌 <b>2학년 이수 확인:</b> ${guide.prereq}</div>
      <div class="guide-3rd">💡 <b>3학년 포인트:</b> ${guide.third}</div>
    </div>`;
  }

  html += `<div class="combo-box">
    <div class="combo-title">🎯 ${escapeHtml(track)}</div>
    <div class="course-desc" style="margin-bottom:0.8rem;">${escapeHtml(combo.desc)}</div>`;
  for (const sk of ["1학기", "2학기"]) {
    const sd = combo[sk];
    html += `<div class="combo-sem">${sk === "1학기" ? "📘" : "📗"} 3학년 ${sk}</div>`;
    for (const grp of GRP_ORDER) {
      if (!(grp in sd)) continue;
      const items = sd[grp];
      const itemsStr = Array.isArray(items) ? items.join(", ") : items;
      html += `<div class="combo-item"><b>${escapeHtml(grp)}:</b> ${escapeHtml(itemsStr)}</div>`;
    }
  }
  html += `</div>`;

  html += `<hr style="margin:1.5rem 0;border:none;border-top:1px solid #e2e8f0;">`;
  html += `<h4 style="margin:0 0 0.3rem;">과목 상세 정보</h4>`;
  html += `<p class="caption" style="margin-top:0;">⭐ 추천 과목이 상단에, 같은 그룹의 나머지 과목은 펼쳐서 볼 수 있습니다.</p>`;

  out.innerHTML = html;

  for (const [semLabel, semFilter] of SEM_INFO) {
    const semTitle = el("div", {class: "semester-title", text: semLabel});
    out.appendChild(semTitle);
    for (const grp of GRP_ORDER) {
      const grpItems = Object.entries(COURSES).filter(([k, v]) => v.sem === semFilter && v.grp === grp);
      if (!grpItems.length) continue;
      out.appendChild(el("div", {class: "group-title", text: `📌 ${grp} 그룹 — ${GRP_COUNT[grp]}개 선택`}));
      renderGroupSection(out, semFilter, grp, recNames);
    }
  }
}

/* ============================================================
   탭3: 키워드 검색
   ============================================================ */
function setupSearchTab() {
  const inp = $("#search-input");
  inp.addEventListener("input", () => renderSearchResults(inp.value));
}

function renderSearchResults(q) {
  const out = $("#search-result");
  const trimmed = q.trim();
  if (!trimmed) {
    out.innerHTML = `<div class="info-box">👆 키워드를 입력하면 관련 과목을 검색하고, 같은 선택 그룹의 나머지 과목도 함께 보여줍니다.</div>`;
    return;
  }
  const qs = trimmed.split(",").map(x => x.trim().toLowerCase()).filter(Boolean);
  const matched = new Set();
  for (const [name, info] of Object.entries(COURSES)) {
    const txt = (name + " " + info.desc + " " + info.kw.join(" ") + " " + info.tracks.join(" ")).toLowerCase();
    if (qs.some(kw => txt.includes(kw))) matched.add(name);
  }
  out.innerHTML = `<p class="search-count">총 <b>${matched.size}개</b> 과목이 검색되었습니다.</p>`;
  if (!matched.size) {
    out.insertAdjacentHTML("beforeend", `<div class="warning-text">검색 조건에 맞는 과목이 없습니다. 다른 키워드를 시도해보세요.</div>`);
    return;
  }
  for (const [semLabel, semFilter] of SEM_INFO) {
    const semMatches = [...matched].filter(k => COURSES[k].sem === semFilter);
    if (!semMatches.length) continue;
    out.appendChild(el("div", {class: "semester-title", text: semLabel}));
    const grps = [...new Set(semMatches.map(k => COURSES[k].grp))].sort((a, b) => GRP_ORDER.indexOf(a) - GRP_ORDER.indexOf(b));
    for (const grp of grps) {
      out.appendChild(el("div", {class: "group-title", text: `📌 ${grp} 그룹 — ${GRP_COUNT[grp]}개 선택`}));
      renderGroupSection(out, semFilter, grp, matched);
    }
  }
}

/* ============================================================
   탭4: 전체 과목 보기
   ============================================================ */
function setupAllTab() {
  for (const id of ["f-rel", "f-abs", "f-pf"]) {
    $("#" + id).addEventListener("change", renderAllTab);
  }
  renderAllTab();
}

function renderAllTab() {
  const sr = $("#f-rel").checked;
  const sa = $("#f-abs").checked;
  const sp = $("#f-pf").checked;
  const out = $("#all-result");
  out.innerHTML = "";
  for (const [semLabel, semFilter] of SEM_INFO) {
    out.appendChild(el("div", {class: "semester-title", text: semLabel}));
    for (const grp of GRP_ORDER) {
      const grpItems = Object.entries(COURSES).filter(([k, v]) => v.sem === semFilter && v.grp === grp);
      if (!grpItems.length) continue;
      out.appendChild(el("div", {class: "group-title", text: `📌 ${grp} 그룹 — ${GRP_COUNT[grp]}개 선택`}));
      for (const [name, info] of grpItems) {
        if (info.eval.includes("상대") && !sr) continue;
        if (info.eval.includes("절대") && !sa) continue;
        if (info.eval.includes("P/F") && !sp) continue;
        out.insertAdjacentHTML("beforeend", courseCardHtml(name, info, false));
      }
    }
  }
}

/* ============================================================
   탭 전환
   ============================================================ */
function setupTabs() {
  for (const btn of $$(".tab-btn")) {
    btn.addEventListener("click", () => {
      const target = btn.dataset.tab;
      for (const b of $$(".tab-btn")) b.classList.toggle("active", b === btn);
      for (const p of $$(".tab-pane")) p.classList.toggle("active", p.id === "tab-" + target);
    });
  }
}

/* ============================================================
   사이드바 모바일 토글
   ============================================================ */
function setupSidebarToggle() {
  const btn = $("#sidebar-toggle");
  const sidebar = $("#sidebar");
  btn.addEventListener("click", () => {
    document.body.classList.toggle("sidebar-open");
    btn.textContent = document.body.classList.contains("sidebar-open") ? "✖ 닫기" : "🤖 프로필 설정";
  });
  // 폼 제출 후 자동 닫기 (모바일에서)
  sidebar.addEventListener("submit", () => {
    if (window.matchMedia("(max-width: 900px)").matches) {
      document.body.classList.remove("sidebar-open");
      btn.textContent = "🤖 프로필 설정";
    }
  });
}

/* ============================================================
   폼 제출 → 프로필 생성 → 탭1 렌더
   ============================================================ */
function handleSubmit(e) {
  e.preventDefault();
  const raw = readSidebarForm();
  // 직업명 키워드로 트랙 자동 확장
  const expanded = expandTracksFromJob(raw.dream_job, raw.career_tracks_raw);
  const profile = {
    dream_job: raw.dream_job,
    career_tracks: expanded,
    grades: raw.grades,
    likes: raw.likes,
    dislikes: raw.dislikes,
    learning_style: raw.learning_style,
    eval_pref: raw.eval_pref,
    workload_pref: raw.workload_pref,
    grade_sens: raw.grade_sens,
    // raw 트랙은 폼 복원용으로 별도 저장
    career_tracks_raw: raw.career_tracks_raw,
  };
  currentProfile = profile;
  saveProfile(profile);
  renderAiTab(profile);
  // AI 탭으로 자동 이동
  for (const b of $$(".tab-btn")) b.classList.toggle("active", b.dataset.tab === "ai");
  for (const p of $$(".tab-pane")) p.classList.toggle("active", p.id === "tab-ai");
  // 결과 영역으로 스크롤
  $("#tab-ai").scrollIntoView({behavior: "smooth", block: "start"});
}

/* ============================================================
   초기화
   ============================================================ */
document.addEventListener("DOMContentLoaded", () => {
  buildSidebarForm();
  buildTrackTab();
  setupSearchTab();
  setupAllTab();
  setupTabs();
  setupSidebarToggle();

  // 저장된 프로필 복원 (있다면)
  const saved = loadProfile();
  if (saved) {
    applyProfileToForm(saved);
    currentProfile = saved;
    renderAiTab(saved);
  }

  $("#profile-form").addEventListener("submit", handleSubmit);
});
