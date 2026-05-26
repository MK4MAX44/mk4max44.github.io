from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image

pdfmetrics.registerFont(TTFont('KR', '/Library/Fonts/Arial Unicode.ttf'))

W, H = 1280, 720
TOTAL = 21

BG     = HexColor('#0D1117')
BG2    = HexColor('#161B22')
BG3    = HexColor('#21262D')
BLUE   = HexColor('#58A6FF')
BLUE_D = HexColor('#1F6FEB')
GREEN  = HexColor('#3FB950')
AMBER  = HexColor('#D29922')
CYAN   = HexColor('#39D3DD')
PURPLE = HexColor('#BC8CFF')
RED    = HexColor('#F85149')
TEXT   = HexColor('#E6EDF3')
TEXT2  = HexColor('#8B949E')
TEXT3  = HexColor('#484F58')
WHITE  = HexColor('#FFFFFF')


def wrap(text, n):
    r = []
    while len(text) > n:
        idx = text[:n + 1].rfind(' ')
        if idx <= 0:
            idx = n
        r.append(text[:idx].rstrip())
        text = text[idx:].lstrip()
    if text:
        r.append(text)
    return r or ['']


def frame(c, title, n, mode='normal'):
    if mode == 'interp':
        bg, acc = HexColor('#0A1810'), GREEN
        badge = ('논문 해석', GREEN)
    elif mode == 'image':
        bg, acc = HexColor('#0A1422'), CYAN
        badge = ('논문 원본', CYAN)
    else:
        bg, acc = BG, BLUE
        badge = None

    c.setFillColor(bg)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(BG2)
    c.rect(0, H - 54, W, 54, fill=1, stroke=0)
    c.setFillColor(acc)
    c.rect(0, H - 56, W, 2, fill=1, stroke=0)

    c.setFillColor(TEXT)
    c.setFont('KR', 17)
    c.drawString(46, H - 33, title)

    c.setFont('KR', 10)
    c.setFillColor(TEXT3)
    c.drawRightString(W - 40, H - 33, f'{n} / {TOTAL}')

    if badge:
        label, color = badge
        c.setFillColor(color)
        c.roundRect(W - 150, H - 47, 110, 20, 4, fill=1, stroke=0)
        c.setFillColor(BG)
        c.setFont('KR', 9)
        c.drawCentredString(W - 95, H - 40, label)

    c.setFillColor(BG2)
    c.rect(0, 0, W, 24, fill=1, stroke=0)
    c.setFillColor(TEXT3)
    c.setFont('KR', 8)
    c.drawString(46, 7, 'NDSS 2025  ·  PolicyPulse: Precision Semantic Role Extraction  ·  MK4MAX44')


def slide(c, title, items, n, mode='normal'):
    frame(c, title, n, mode)
    acc = GREEN if mode == 'interp' else BLUE

    y = H - 73
    for item in items:
        if not item:
            y -= 7
            continue
        if y < 36:
            break
        if item.startswith('==='):
            txt = item[3:].strip()
            c.setFillColor(BG3)
            c.rect(40, y - 6, W - 80, 23, fill=1, stroke=0)
            c.setFillColor(acc)
            c.rect(40, y - 6, 3, 23, fill=1, stroke=0)
            c.setFillColor(acc)
            c.setFont('KR', 11)
            c.drawString(52, y + 5, txt)
            y -= 31
        elif item.startswith('--'):
            txt = item[2:].strip()
            c.setFillColor(acc)
            c.circle(63, y + 4, 2, fill=1, stroke=0)
            c.setFillColor(TEXT2)
            c.setFont('KR', 11)
            lines = wrap(txt, 87)
            for i, l in enumerate(lines):
                c.drawString(72, y - i * 15, l)
            y -= len(lines) * 15 + 5
        else:
            c.setFillColor(acc)
            c.setFont('KR', 14)
            c.drawString(40, y, '▸')
            c.setFillColor(TEXT)
            c.setFont('KR', 12)
            lines = wrap(item, 85)
            for i, l in enumerate(lines):
                c.drawString(60, y - i * 16, l)
            y -= len(lines) * 16 + 8
    c.showPage()


def split_slide(c, title, img_path, interp_items, caption, n):
    frame(c, title, n, 'image')

    # Left: white image card
    lx, ly, lw, lh = 34, 32, 562, H - 96
    c.setFillColor(WHITE)
    c.rect(lx, ly, lw, lh, fill=1, stroke=0)
    c.setStrokeColor(CYAN)
    c.setLineWidth(1.5)
    c.rect(lx, ly, lw, lh, fill=0, stroke=1)
    c.drawImage(ImageReader(img_path), lx + 5, ly + 5, lw - 10, lh - 10,
                preserveAspectRatio=True, anchor='c')

    # Caption
    c.setFillColor(TEXT3)
    c.setFont('KR', 8)
    c.drawCentredString(lx + lw / 2, 12, caption)

    # Right: interpretation panel
    rx = 610
    rw = W - rx - 30
    c.setFillColor(HexColor('#07131F'))
    c.rect(rx, ly, rw, lh, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(rx, ly, 2, lh, fill=1, stroke=0)

    y = H - 73
    for item in interp_items:
        if not item:
            y -= 6
            continue
        if y < 40:
            break
        if item.startswith('==='):
            txt = item[3:].strip()
            c.setFillColor(HexColor('#0E2218'))
            c.rect(rx + 10, y - 5, rw - 12, 21, fill=1, stroke=0)
            c.setFillColor(GREEN)
            c.rect(rx + 10, y - 5, 2, 21, fill=1, stroke=0)
            c.setFillColor(GREEN)
            c.setFont('KR', 10)
            c.drawString(rx + 18, y + 4, txt)
            y -= 29
        elif item.startswith('--'):
            txt = item[2:].strip()
            c.setFillColor(GREEN)
            c.circle(rx + 20, y + 4, 1.8, fill=1, stroke=0)
            c.setFillColor(TEXT2)
            c.setFont('KR', 10)
            lines = wrap(txt, 41)
            for i, l in enumerate(lines):
                c.drawString(rx + 28, y - i * 14, l)
            y -= len(lines) * 14 + 5
        else:
            c.setFillColor(GREEN)
            c.setFont('KR', 12)
            c.drawString(rx + 10, y, '▸')
            c.setFillColor(TEXT)
            c.setFont('KR', 11)
            lines = wrap(item, 39)
            for i, l in enumerate(lines):
                c.drawString(rx + 26, y - i * 15, l)
            y -= len(lines) * 15 + 7
    c.showPage()


def tbl_slide(c, title, headers, rows, col_w, n, note=''):
    frame(c, title, n)
    x0, y0 = 34, H - 70
    rh = 30

    x = x0
    for h, w in zip(headers, col_w):
        c.setFillColor(BLUE_D)
        c.rect(x, y0 - rh, w - 1, rh, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.rect(x, y0 - rh, w - 1, 1.5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('KR', 10)
        c.drawCentredString(x + w / 2, y0 - rh / 2 - 4, h)
        x += w

    y = y0 - rh
    for ri, row in enumerate(rows):
        rh2 = 26
        x = x0
        is_star = any('★' in cell for cell in row)
        bg = HexColor('#14261A') if is_star else (BG3 if ri % 2 == 0 else BG2)
        for ci, (cell, w) in enumerate(zip(row, col_w)):
            c.setFillColor(bg)
            c.rect(x, y - rh2, w - 1, rh2, fill=1, stroke=0)
            c.setFillColor(GREEN if is_star else (CYAN if ci == 0 else TEXT2))
            c.setFont('KR', 10)
            lines = wrap(cell, max(w // 7, 4))
            for li, line in enumerate(lines):
                c.drawString(x + 5, y - 10 - li * 12, line)
            x += w
        y -= rh2

    if note:
        c.setFillColor(TEXT3)
        c.setFont('KR', 8)
        c.drawString(34, y - 10, note)
    c.showPage()


def divider(c, title, sub='', n=None):
    c.setFillColor(HexColor('#060A12'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BLUE_D)
    c.rect(0, 0, 5, H, fill=1, stroke=0)
    c.rect(W - 5, 0, 5, H, fill=1, stroke=0)
    c.setFillColor(BG2)
    c.rect(5, 0, 28, H, fill=1, stroke=0)
    c.rect(W - 33, 0, 28, H, fill=1, stroke=0)
    c.setFillColor(HexColor('#1C2A42'))
    c.rect(70, H / 2 + 52, W - 140, 1.5, fill=1, stroke=0)
    c.rect(70, H / 2 - 64, W - 140, 1.5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 52)
    c.drawCentredString(W / 2, H / 2 + 8, title)
    if sub:
        c.setFont('KR', 21)
        c.setFillColor(TEXT2)
        c.drawCentredString(W / 2, H / 2 - 44, sub)
    if n:
        c.setFillColor(TEXT3)
        c.setFont('KR', 9)
        c.drawRightString(W - 42, 12, f'{n} / {TOTAL}')
    c.showPage()


def make(path):
    # Crop paper images
    crops = [
        ('/tmp/paper_page-03.png', (40, 100, 1240, 550), '/tmp/final_fig1.png'),
        ('/tmp/paper_page-05.png', (40, 80,  1240, 1300), '/tmp/final_tbl12.png'),
        ('/tmp/paper_page-06.png', (40, 95,  1240, 490), '/tmp/final_tbl3.png'),
    ]
    for src, box, out in crops:
        Image.open(src).crop(box).save(out)
    print('이미지 크롭 완료')

    c = canvas.Canvas(path, pagesize=(W, H))

    # ── 1. Title ─────────────────────────────────────────────────────
    c.setFillColor(HexColor('#060A12'))
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(BG2)
    c.rect(W - 310, 0, 310, H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(W - 313, 0, 3, H, fill=1, stroke=0)

    c.setFillColor(BG3)
    for gx in range(W - 290, W - 18, 26):
        for gy in range(18, H - 18, 26):
            c.circle(gx, gy, 1.5, fill=1, stroke=0)

    c.setFillColor(BLUE)
    c.rect(70, 230, 4, 240, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('KR', 48)
    c.drawString(90, 415, 'PolicyPulse')

    c.setFillColor(HexColor('#79C0FF'))
    c.setFont('KR', 16)
    c.drawString(90, 368, 'Precision Semantic Role Extraction for')
    c.drawString(90, 345, 'Enhanced Privacy Policy Comprehension')

    c.setStrokeColor(BG3)
    c.setLineWidth(1)
    c.line(90, 327, 630, 327)

    c.setFillColor(TEXT2)
    c.setFont('KR', 13)
    c.drawString(90, 304, 'Andrick Adhikari · Sanchari Das · Rinku Dewri')
    c.drawString(90, 282, 'University of Denver')

    c.setFillColor(TEXT3)
    c.setFont('KR', 11)
    c.drawString(90, 248, 'NDSS 2025  ·  Paper Review  ·  2026.05')

    c.setFillColor(BLUE)
    c.roundRect(90, 66, 120, 26, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 11)
    c.drawCentredString(150, 76, 'MK4MAX44')

    c.showPage()

    # ── 2. TOC ───────────────────────────────────────────────────────
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BG2)
    c.rect(0, 0, 326, H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(326, 0, 2, H, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('KR', 26)
    c.drawString(38, H - 66, '목  차')
    c.setFillColor(BLUE)
    c.rect(38, H - 80, 250, 2, fill=1, stroke=0)

    sections = [
        ('01', 'Introduction & State of the Art', BLUE),
        ('02', 'Methodology',                      CYAN),
        ('03', 'Results & Analysis',               GREEN),
        ('04', 'Conclusion',                       AMBER),
        ('05', 'Q & A',                            PURPLE),
        ('06', 'References',                       TEXT2),
    ]
    y = H - 116
    for num, name, acc in sections:
        c.setFillColor(BG3)
        c.rect(30, y - 8, 282, 27, fill=1, stroke=0)
        c.setFillColor(acc)
        c.rect(30, y - 8, 3, 27, fill=1, stroke=0)
        c.setFillColor(acc)
        c.setFont('KR', 10)
        c.drawString(42, y + 5, num)
        c.setFillColor(TEXT)
        c.setFont('KR', 12)
        c.drawString(68, y + 5, name)
        y -= 44

    c.setFillColor(WHITE)
    c.setFont('KR', 20)
    c.drawString(356, H - 66, 'Table of Contents')
    c.setFillColor(BG3)
    c.rect(356, H - 80, W - 386, 1.5, fill=1, stroke=0)

    tags = [
        (BLUE,   '논문',  'PolicyPulse — NDSS 2025'),
        (CYAN,   '저자',  'Adhikari · Das · Dewri  (Univ. of Denver)'),
        (GREEN,  '주제',  '개인정보처리방침 자동 정보 추출 (SRL 기반)'),
        (AMBER,  '규모',  '129,856개 정책 / 3,970만 프레임 분석'),
        (PURPLE, '성능',  'Weighted Avg F1 = 0.97'),
        (RED,    '발견',  '60% 정책이 USER_MECHANISM 미기재'),
    ]
    dy = H - 126
    for color, label, text in tags:
        c.setFillColor(color)
        c.roundRect(356, dy - 2, 52, 18, 3, fill=1, stroke=0)
        c.setFillColor(BG)
        c.setFont('KR', 9)
        c.drawCentredString(382, dy + 5, label)
        c.setFillColor(TEXT2)
        c.setFont('KR', 12)
        c.drawString(416, dy + 5, text)
        dy -= 32

    c.setFillColor(TEXT3)
    c.setFont('KR', 8)
    c.drawRightString(W - 30, 8, f'2 / {TOTAL}')
    c.showPage()

    # ── 3. Divider: Introduction ─────────────────────────────────────
    divider(c, 'Introduction', '& State of the Art', 3)

    # ── 4. Introduction ──────────────────────────────────────────────
    slide(c, 'Introduction', [
        '연구 배경: 개인정보처리방침의 비효율성',
        '--평균 70문장의 복잡한 법률 언어로 작성 → 사용자 대부분 이해 못 한 채 동의',
        '--가독성·모호성·접근성 세 가지 모두 문제',
        '',
        '기존 NLP 도구의 한계',
        '--단락 수준 분류에 그침 → "데이터 수집 항목 있냐 없냐" 수준만 제공',
        '--누가(FIRST_PARTY), 무엇을(DATA), 어떻게(MECHANISM) 세부 추출 불가',
        '--특정 태스크 하나에만 특화 → 다른 응용에 재사용 불가',
        '',
        '제안: PolicyPulse',
        '--SRL(Semantic Role Labeling) 기반 세밀한 정보 추출 파이프라인',
        '--분류에서 끝내지 않고 문장 내 누가·무엇을·왜·어떻게를 역할 단위로 자동 추출',
        '--범용 플랫폼 → 완전성 검사·요약 생성·Q&A·선호도 확인 등 다양한 응용 지원',
    ], 4)

    # ── 5. State of the Art ──────────────────────────────────────────
    slide(c, 'State of the Art', [
        '분류(Classification) 기반',
        '--Polisis (Harkous et al., USENIX 2018): OPP-115 기반 단락 수준 분류',
        '--높은 정확도이나 누가·무엇을·어떻게는 알 수 없음',
        '',
        '정보 추출(Information Extraction) 기반',
        '--PoliGraph (Cui et al., USENIX 2023): NER로 데이터 유형·주체·관계 그래프 추출',
        '--PolicyLint / PoliCheck: 정책 내 모순·앱 행동 불일치 탐지 특화',
        '',
        'SRL 기반 (선행 연구)',
        '--Bhatia et al. (2016): 5개 정책 202문장 수작업 코딩 → 자동화 없음',
        '--PurPliance: 목적 절에만 SRL 적용, FPCU 범위로 제한',
        '',
        '결론 — PolicyPulse의 위치',
        '--기존 도구: 단일 태스크 특화 또는 자동화 미비',
        '--PolicyPulse: 분류 + 자동 SRL 결합 → 다목적 정보 추출 플랫폼',
    ], 5)

    # ── 6. Divider: Methodology ──────────────────────────────────────
    divider(c, 'Methodology', n=6)

    # ── 7. Methodology: Pipeline ─────────────────────────────────────
    slide(c, 'Methodology: PolicyPulse 파이프라인 (4단계)', [
        'Step 1 — SRL: AllenNLP SRLBert로 문장에서 프레임 추출',
        '--PropBank 기반 사전 학습 (약 50,000 술어) — fine-tuning 불필요',
        '--정책당 평균 70문장 × 문장당 약 4 프레임 → 정책당 평균 305.7 프레임',
        '',
        'Step 2 — 프레임 분류: XLNet 2단계 분류기',
        '--Level 1: SKIP vs KEEP (개인정보 무관 vs 관련)',
        '--Level 2: KEEP 프레임을 FPCU · TPSC · UCC · UAED · DR 중 하나로 분류',
        '',
        'Step 3 — 프라이버시 역할 매핑: PropBank → 16가지 전용 역할',
        '--FIRST_PARTY_ENTITY · DATA · MECHANISM · PURPOSE · USER_MECHANISM 등',
        '',
        'Step 4 — 대규모 적용: Princeton Privacy Crawl 129,856개 정책',
        '--총 39,702,767개 프레임 처리 → 정책 완전성 분석',
    ], 7)

    # ── 8. Fig.1 split ───────────────────────────────────────────────
    split_slide(c, '논문 원본 Fig.1 — PolicyPulse 전체 파이프라인', '/tmp/final_fig1.png', [
        '===Fig.1 흐름',
        '① 입력 문장에서',
        '   SRL이 프레임 추출',
        '',
        '② 각 프레임을 FPCU/',
        '   SKIP 등으로 분류',
        '',
        '③ KEEP 프레임의 인수를',
        '   프라이버시 역할로 변환',
        '',
        '===논문 예시 문장',
        '"We may collect location',
        ' information through',
        ' cookies when you use',
        ' our service"',
        '',
        '--frame1: include → FPCU',
        '--frame2: use → SKIP',
        '--frame3: collect → FPCU',
        '→ ARG0=FIRST_PARTY',
        '→ ARG1=DATA',
        '→ ARGM-MNR=MECHANISM',
    ], 'Fig. 1 — Overview of privacy-specific role extraction in PolicyPulse', 8)

    # ── 9. Frame Classification Table ────────────────────────────────
    tbl_slide(c, 'Methodology: 프레임 분류 레이블 (Level 1 + Level 2)',
        ['레이블', '설명', 'F1 (Two-Level)'],
        [
            ['SKIP',  '개인정보 무관 프레임 — 학습 데이터의 72.6% / 실제 분석의 약 90%',  '0.98'],
            ['FPCU',  'First Party Collection/Use — 1자 데이터 수집·사용',                 '0.98'],
            ['TPSC',  'Third Party Sharing/Collection — 제3자 공유·수집',                  '0.98'],
            ['UCC',   'User Choice/Control — 사용자 선택권·통제 (옵트인/아웃)',             '0.98'],
            ['UAED',  'User Access/Edit/Deletion — 사용자 데이터 접근·수정·삭제',          '0.98'],
            ['DR',    'Data Retention — 데이터 보존 기간',                                  '0.96'],
        ],
        [82, 900, 100], 9,
        note='실제 학습 데이터 분포: SKIP 10,401 / FPCU 1,417 / TPSC 1,230 / UCC 556 / UAED 182 / DR 160  →  저빈도 클래스 증강 필요')

    # ── 10. TABLE I/II split ─────────────────────────────────────────
    split_slide(c, '논문 원본 TABLE I/II — 분류 방법별 성능 비교', '/tmp/final_tbl12.png', [
        '===TABLE I 핵심',
        '4가지 방법 F1 비교',
        '',
        'Frame only',
        '--UAED F1 = 0.15',
        '→ 데이터 부족 문제',
        '',
        'FSC Augmented',
        '--증강 후 UAED 0.84',
        '→ 증강 효과 확인',
        '',
        '★ FSC (Two-Level)',
        '--SKIP 먼저 분리 후',
        '  5-class 분류',
        '--전체 F1 = 0.97',
        '',
        '===TABLE II',
        'Level1 macro: 0.96',
        'Level2 macro: 0.98',
        '--두 단계 모두 높음',
    ], 'TABLE I/II — XLNet Cross-Validation Performance Scores (pr: Precision, re: Recall, f1: F1-Score)', 10)

    # ── 11. TABLE I/II 해석 ──────────────────────────────────────────
    slide(c, 'TABLE I/II 해석 — Two-Level 방식이 효과적인 이유', [
        '===데이터 불균형 문제',
        'SKIP이 학습 데이터의 72.6% → 직접 6-class 분류 시 소수 클래스 학습 어려움',
        '--Two-Level: SKIP vs KEEP 먼저 분리 → KEEP만 따로 5-class 분류 → 집중 학습 가능',
        '',
        '===데이터 증강의 효과 (UAED: 0.15 → 0.92)',
        'UAED(182건)·DR(160건)은 절대적으로 학습 데이터 부족',
        '--동의어 교체 + 문맥 기반 단어 치환으로 저빈도 클래스 데이터 보강',
        '--UAED F1이 약 6배 향상 → 증강이 핵심 역할',
        '',
        '===XLNet이 BERT보다 나은 이유',
        'XLNet: 순열 기반 언어 모델링 → 양방향 문맥 + 자기회귀 특성 동시 활용',
        '--프라이버시 정책의 복잡한 조건절 구조 처리에 더 적합',
        '--사전 실험에서 BERT 및 전통 분류기 대비 프레임 분류 성능 우수 확인',
    ], 11, mode='interp')

    # ── 12. Role Mapping + Training Data ─────────────────────────────
    slide(c, 'Methodology: 역할 매핑 + 학습 데이터 구성', [
        '===프라이버시 역할 매핑 (146개 동사 커버)',
        '"collect" 동사 (FPCU): ARG0→FIRST_PARTY · ARG1→DATA · ARGM-MNR→MECHANISM',
        '같은 동사라도 카테고리(FPCU/TPSC 등)에 따라 다른 역할로 매핑',
        '16가지 전용 역할: DATA · FIRST_PARTY_ENTITY · MECHANISM · PURPOSE · CONSEQUENCE 등',
        '',
        '===학습 데이터: OPP-115 기반',
        '115개 웹사이트 → SRLBert로 48,783 프레임 → 최종 13,946개 수동 주석',
        '--주석 담당: 경력 3년+ / 독립 검증: 경력 5년+ 2명',
        '--10-겹 교차 검증 (9:1 훈련/테스트, 6 epoch 훈련)',
        '',
        '▶ 다음 슬라이드: 논문 TABLE III 원본 — 16가지 역할 정의 확인',
    ], 12)

    # ── 13. Divider: Results ─────────────────────────────────────────
    divider(c, 'Results', '& Analysis', 13)

    # ── 14. Results: Classification Table ────────────────────────────
    tbl_slide(c, 'Results: 분류 성능 비교 (F1-score)',
        ['방법', 'SKIP', 'FPCU', 'TPSC', 'UCC', 'UAED', 'DR', 'Weighted Avg'],
        [
            ['Frame only',        '0.93', '0.72', '0.70', '0.74', '0.15', '0.24', '0.86'],
            ['FSC Augmented',     '0.92', '0.72', '0.74', '0.86', '0.84', '0.83', '0.88'],
            ['FSC (Ensemble)',    '0.93', '0.79', '0.79', '0.76', '0.65', '0.65', '0.89'],
            ['★ FSC (Two-Level)','0.98', '0.93', '0.93', '0.93', '0.92', '0.92', '0.97'],
        ],
        [230, 58, 58, 58, 58, 58, 58, 110], 14,
        note='★ 최종 채택. Level1 macro avg F1: 0.96  /  Level2 macro avg F1: 0.98  /  모든 카테고리 precision·recall 0.92 이상')

    # ── 15. TABLE III split ───────────────────────────────────────────
    split_slide(c, '논문 원본 TABLE III — 16가지 프라이버시 역할 정의', '/tmp/final_tbl3.png', [
        '===주요 역할',
        'DATA',
        '--개인·민감 정보 총칭',
        '',
        'FIRST_PARTY_ENTITY',
        '--데이터 수집 주체',
        '',
        'MECHANISM',
        '--데이터 수집 방법',
        '',
        'USER_MECHANISM',
        '--사용자가 접근·수정·',
        '  삭제하는 방법',
        '',
        'CONSEQUENCE',
        '--옵트인/아웃 결과',
        '',
        '===왜 중요한가',
        '이 역할들이 정책에',
        '얼마나 빠져있는지',
        '→ 다음 슬라이드',
    ], 'TABLE III — PropBank to Privacy-Specific Role Definitions', 15)

    # ── 16. Results: Large-Scale ─────────────────────────────────────
    slide(c, 'Results: 대규모 정책 분석 (Princeton Privacy Crawl)', [
        '분석 규모',
        '--130,604개 웹사이트 → 129,856개 최신 정책 / 총 39,702,767개 프레임 처리',
        '--정책당 평균 306 프레임 → KEEP 평균 30개 (약 10%)',
        '',
        '===정책 완전성 분석: 누락된 핵심 역할',
        '50%: UAED 프레임 자체 없음 — 사용자 데이터 삭제 권리 전혀 미언급',
        '60%: USER_MECHANISM 미기재 — 데이터 접근·수정·삭제 방법 불명확',
        '75%: CONSEQUENCE 미기재 — 옵트인/아웃 결과 불명확',
        '40%: MECHANISM 없음 — 데이터 수집 방법 미기재',
        '20%: USER_TRIGGER 미기재 — 언제 수집되는지 명시 안 함',
        '',
        '===ChatGPT-3.5 비교',
        'ChatGPT: 야후 정책 요약 시 제3자 공유 내용 누락 + 없는 내용 생성 (hallucination)',
        'PolicyPulse: 원문 기반 추출 → 환각 없음 / 단, GPT-4 비교는 향후 과제',
    ], 16)

    # ── 17. 대규모 분석 해석 ─────────────────────────────────────────
    slide(c, '대규모 분석 결과 해석', [
        '===50%가 UAED 없다는 게 왜 심각한가',
        'UAED = 사용자가 자신의 데이터를 접근·수정·삭제할 권리',
        '--GDPR(유럽)·CCPA(캘리포니아) 등 개인정보보호법이 보장하는 핵심 권리',
        '--절반의 사이트가 정책에 이 내용을 아예 명시하지 않는다는 뜻',
        '',
        '===75%가 CONSEQUENCE 미기재',
        '옵트아웃 버튼 눌렀을 때 "어떻게 되는지" 안 알려줌',
        '--마케팅 수신 거부 → 계정 기능 제한? 데이터 삭제? → 정책이 침묵',
        '',
        '===연구의 의의',
        '"개인정보처리방침이 어렵다"는 주관적 불만이 아니라',
        '--129,856개 정책 자동 분석 → "어떤 내용이 얼마나 빠져 있는가"를 정량화',
        '--규제 당국·연구자·사용자 모두에게 객관적 근거 제공',
    ], 17, mode='interp')

    # ── 18. Divider: Conclusion ───────────────────────────────────────
    divider(c, 'Conclusion', '& Q / A', 18)

    # ── 19. Conclusion ────────────────────────────────────────────────
    slide(c, 'Conclusion', [
        'PolicyPulse: SRL + 2단계 XLNet → 절(clause) 수준 세밀 추출',
        '--기존 단락 분류 방식 대비 훨씬 구체적인 정보 제공',
        '--Weighted avg F1 0.97 / 모든 카테고리 precision·recall 0.92 이상',
        '',
        '===5가지 잠재적 응용 분야',
        '정책 완전성 검사 — 법적 필수 항목 자동 체크',
        '짧은 공지(Short Notice) 자동 생성',
        '개인정보 영양 정보 라벨 (식품 성분표 스타일)',
        '자동 질의응답 시스템 / 사용자 선호도 자동 확인',
        '',
        '===한계점 및 향후 과제',
        '영어 전용 → 한국어 등 다국어 지원 필요',
        '문장 간 관계 분석 불가 / GPT-4 비교 미수행',
        '',
        '코드·데이터 공개: github.com/crisp-du/ppevo',
    ], 19)

    # ── 20. Q&A ───────────────────────────────────────────────────────
    slide(c, '예상 질문 & 답변', [
        '===방법론',
        'Q. SRL 모델 fine-tuning 없이 써도 괜찮은가?',
        '--프레임 추출 자체는 충분. 분류는 XLNet이 따로 담당하므로 구조적 문제 없음',
        '',
        'Q. XLNet 채택 이유는?',
        '--사전 실험에서 BERT·전통 분류기 대비 프레임 분류 성능 우수. TABLE I 참고',
        '',
        '===결과',
        'Q. F1 0.97인데 틀리는 케이스는?',
        '--DR·UAED 카테고리 상대적으로 낮음. 학습 데이터 적고 타 카테고리 문장과 혼동',
        '',
        'Q. ChatGPT-4와 비교는?',
        '--GPT-3.5만 비교. 저자도 최신 LLM과 깊은 비교는 향후 과제라고 명시',
        '',
        '===활용',
        'Q. 한국어 적용?   →   현재 영어 전용. 한국어 BERT + 주석 데이터 추가 필요',
        'Q. 가장 충격적인 발견?   →   60% USER_MECHANISM 미기재 / 75% CONSEQUENCE 미기재',
    ], 20)

    # ── 21. References ────────────────────────────────────────────────
    slide(c, 'References', [
        '[1]  Adhikari et al., "PolicyPulse: Precision Semantic Role Extraction for Enhanced Privacy Policy Comprehension," NDSS 2025.',
        '',
        '[2]  Harkous et al., "Polisis: Automated Analysis and Presentation of Privacy Policies Using Deep Learning," USENIX 2018.',
        '',
        '[3]  Cui et al., "PoliGraph: Automated Privacy Policy Analysis using Knowledge Graphs," USENIX 2023.',
        '',
        '[4]  Wilson et al., "The Creation and Analysis of a Website Privacy Policy Corpus (OPP-115)," ACL 2016.',
        '',
        '[5]  Yang et al., "XLNet: Generalized Autoregressive Pretraining for Language Understanding," NeurIPS 2019.',
        '',
        '[6]  Bhatia et al., "Mining Privacy Goals from Privacy Policies Using Hybridized Task Analysis," ACM TOCHI 2016.',
        '',
        '[7]  Princeton Privacy Crawl (PPCrawl) Corpus — github.com/citp/privacy-crawl',
    ], 21)

    c.save()
    print(f'✅ 저장 완료: {path}')


make('/Users/jeondonghyeog/Desktop/PaperReview_PolicyPulse_Final.pdf')
