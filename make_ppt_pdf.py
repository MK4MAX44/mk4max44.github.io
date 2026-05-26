from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

pdfmetrics.registerFont(TTFont('KR', '/Library/Fonts/Arial Unicode.ttf'))

W, H = 1280, 720

DARK  = HexColor('#152141')
NAVY  = HexColor('#1A3A6C')
ACC   = HexColor('#2B5EA7')
LIGHT = HexColor('#EEF2FA')
WHITE = HexColor('#FFFFFF')
TEXT  = HexColor('#1E293B')
GRAY  = HexColor('#64748B')
LGRAY = HexColor('#CBD5E1')

TOTAL = 15


def wrap(text, n):
    r = []
    while len(text) > n:
        r.append(text[:n])
        text = text[n:]
    if text:
        r.append(text)
    return r or ['']


# ── 슬라이드 공통 프레임 ───────────────────────────────────────
def frame(c, title, n):
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # 상단 헤더
    c.setFillColor(DARK)
    c.rect(0, H - 62, W, 62, fill=1, stroke=0)
    c.setFillColor(ACC)
    c.rect(0, H - 65, W, 3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 20)
    c.drawString(40, H - 42, title)
    c.setFont('KR', 11)
    c.setFillColor(HexColor('#7A9AC0'))
    c.drawRightString(W - 30, H - 42, f'{n} / {TOTAL}')
    # 하단 푸터
    c.setFillColor(HexColor('#F1F5F9'))
    c.rect(0, 0, W, 28, fill=1, stroke=0)
    c.setFillColor(GRAY)
    c.setFont('KR', 9)
    c.drawString(30, 9, 'NDSS 2025  |  PolicyPulse Paper Review')


# ── 컨텐츠 슬라이드 ───────────────────────────────────────────
def slide(c, title, items, n):
    frame(c, title, n)
    y = H - 90
    for item in items:
        if not item:
            y -= 10
            continue
        if item.startswith('==='):      # 소제목
            txt = item[3:].strip()
            c.setFillColor(NAVY)
            c.setFont('KR', 13)
            c.drawString(40, y, txt)
            c.setFillColor(ACC)
            c.rect(40, y - 4, min(len(txt) * 8, W - 80), 1.5, fill=1, stroke=0)
            y -= 26
        elif item.startswith('--'):     # 들여쓰기 불릿
            txt = item[2:].strip()
            c.setFillColor(ACC)
            c.circle(62, y + 4, 2.5, fill=1, stroke=0)
            c.setFillColor(TEXT)
            c.setFont('KR', 11)
            lines = wrap(txt, 100)
            for i, l in enumerate(lines):
                c.drawString(72, y - i * 16, l)
            y -= len(lines) * 16 + 6
        else:                           # 메인 불릿
            txt = item
            c.setFillColor(NAVY)
            c.setFont('KR', 12)
            c.drawString(40, y, '▪')
            c.setFillColor(TEXT)
            lines = wrap(txt, 90)
            for i, l in enumerate(lines):
                c.drawString(62, y - i * 17, l)
            y -= len(lines) * 17 + 8
    c.showPage()


# ── 테이블 슬라이드 ───────────────────────────────────────────
def tbl_slide(c, title, headers, rows, col_w, n, note=''):
    frame(c, title, n)
    x0, y0 = 40, H - 88
    rh = 30
    # 헤더 행
    x = x0
    for h, w in zip(headers, col_w):
        c.setFillColor(NAVY)
        c.rect(x, y0 - rh, w - 2, rh, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('KR', 11)
        c.drawCentredString(x + w / 2, y0 - rh / 2 - 4, h)
        x += w
    y = y0 - rh
    for ri, row in enumerate(rows):
        rh2 = 26
        x = x0
        bg = LIGHT if ri % 2 == 0 else WHITE
        for ci, (cell, w) in enumerate(zip(row, col_w)):
            c.setFillColor(bg)
            c.rect(x, y - rh2, w - 2, rh2, fill=1, stroke=0)
            c.setFillColor(NAVY if ci == 0 else TEXT)
            c.setFont('KR', 10)
            lines = wrap(cell, max(w // 7, 4))
            for li, line in enumerate(lines):
                c.drawString(x + 5, y - 10 - li * 13, line)
            x += w
        y -= rh2
    if note:
        c.setFillColor(GRAY)
        c.setFont('KR', 9)
        c.drawString(40, y - 12, note)
    c.showPage()


# ── 섹션 구분 슬라이드 ─────────────────────────────────────────
def divider(c, title, sub=''):
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(ACC)
    c.rect(60, H / 2 + 50, W - 120, 2.5, fill=1, stroke=0)
    c.rect(60, H / 2 - 70, W - 120, 2.5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 46)
    c.drawCentredString(W / 2, H / 2 + 5, title)
    if sub:
        c.setFont('KR', 22)
        c.setFillColor(HexColor('#8BA8CC'))
        c.drawCentredString(W / 2, H / 2 - 45, sub)
    c.showPage()


# ══════════════════════════════════════════════════════════════
def make(path):
    c = canvas.Canvas(path, pagesize=(W, H))

    # ── 1. 타이틀 ──────────────────────────────────────────────
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(ACC)
    c.rect(80, 170, 5, 340, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 44)
    c.drawString(110, 490, 'PolicyPulse')
    c.setFont('KR', 19)
    c.setFillColor(HexColor('#A8C4E8'))
    c.drawString(110, 440, 'Precision Semantic Role Extraction for')
    c.drawString(110, 413, 'Enhanced Privacy Policy Comprehension')
    c.setFont('KR', 13)
    c.setFillColor(HexColor('#8BA8CC'))
    c.drawString(110, 365, 'Andrick Adhikari · Sanchari Das · Rinku Dewri  |  University of Denver')
    c.setStrokeColor(HexColor('#3A5A8A'))
    c.setLineWidth(1)
    c.line(110, 348, 720, 348)
    c.setFont('KR', 13)
    c.setFillColor(HexColor('#607590'))
    c.drawString(110, 325, 'NDSS 2025  ·  Paper Review  ·  2026.05')
    c.setFont('KR', 13)
    c.setFillColor(HexColor('#4A6A9A'))
    c.drawRightString(W - 60, 55, 'MK4MAX44')
    c.showPage()

    # ── 2. 목차 ────────────────────────────────────────────────
    c.setFillColor(DARK)
    c.rect(0, 0, 310, H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.rect(310, 0, W - 310, H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 24)
    c.drawString(40, H - 75, '목차')
    c.setFillColor(ACC)
    c.rect(40, H - 90, 230, 2, fill=1, stroke=0)
    sections = [
        ('01', 'Introduction'),
        ('02', 'State of the Art'),
        ('03', 'Methodology'),
        ('04', 'Results'),
        ('05', 'Conclusion'),
        ('06', 'References'),
    ]
    y = H - 130
    for num, name in sections:
        c.setFillColor(HexColor('#1E3A6A'))
        c.rect(34, y - 6, 242, 26, fill=1, stroke=0)
        c.setFillColor(ACC)
        c.rect(34, y - 6, 4, 26, fill=1, stroke=0)
        c.setFillColor(HexColor('#6A90C0'))
        c.setFont('KR', 11)
        c.drawString(44, y + 5, num)
        c.setFillColor(WHITE)
        c.setFont('KR', 12)
        c.drawString(68, y + 5, name)
        y -= 40

    c.setFillColor(NAVY)
    c.rect(330, H - 110, W - 350, 70, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 20)
    c.drawString(355, H - 58, 'Table of Contents')
    c.setFillColor(TEXT)
    c.setFont('KR', 11)
    desc = [
        '본 발표는 NDSS 2025에 게재된 PolicyPulse 논문을 리뷰합니다.',
        '개인정보처리방침의 SRL 기반 자동 정보 추출과',
        '130만 개 정책 분석 결과를 다룹니다.',
    ]
    dy = H - 165
    for d in desc:
        c.drawString(355, dy, d)
        dy -= 22
    c.showPage()

    # ── 3. 섹션 구분: Introduction ─────────────────────────────
    divider(c, 'Introduction', '& State of the Art')

    # ── 4. Introduction ─────────────────────────────────────────
    slide(c, 'Introduction', [
        '▪ 연구 배경: 개인정보처리방침의 비효율성',
        '--개인정보처리방침은 법적 구속력을 지닌 문서이지만 평균 70문장의 복잡한 법률 언어로 작성',
        '--사용자는 내용을 이해하지 못한 채 동의 → 가독성·모호성·접근성 모두 문제',
        '',
        '▪ 기존 NLP 도구의 한계',
        '--단락 수준 분류에 그침 → "데이터 수집 항목 있냐 없냐" 수준의 정보만 제공',
        '--누가(FIRST_PARTY), 무엇을(DATA), 어떻게(MECHANISM) 수집하는지 세부 추출 불가',
        '--특정 태스크 하나에만 특화 → 다른 응용에 재사용 불가',
        '',
        '▪ 제안하는 해결법: PolicyPulse',
        '--SRL(Semantic Role Labeling, 의미역 레이블링) 기반 세밀한 정보 추출 파이프라인',
        '--분류에서 끝내지 않고 문장 내 "누가·무엇을·왜·어떻게"를 역할 단위로 자동 추출',
        '--범용 플랫폼 → 완전성 검사·요약 생성·Q&A·선호도 확인 등 다양한 응용 지원',
    ], 4)

    # ── 5. State of the Art ─────────────────────────────────────
    slide(c, 'State of the Art', [
        '▪ 분류(Classification) 기반',
        '--Polisis (Harkous et al., USENIX 2018): OPP-115 기반 단락 수준 분류. 데이터 수집/공유 등 범주 제공',
        '--높은 정확도이나 "어떤 데이터를 누가 어떻게"는 알 수 없음 → 세부 추출 불가',
        '',
        '▪ 정보 추출(Information Extraction) 기반',
        '--PoliGraph (Cui et al., USENIX 2023): NER로 데이터 유형·주체·관계 그래프 추출',
        '--PolicyLint / PoliCheck: 정책 내 모순·앱 행동 불일치 탐지에 특화. 범용 추출 목적 아님',
        '',
        '▪ SRL 기반 (선행 연구)',
        '--Bhatia et al. (2016): 5개 정책 202개 문장 수작업 코딩 → 17개 의미역. 자동화 없음',
        '--PurPliance: 목적 절(purpose clause)에만 SRL 적용. 범위가 FPCU로 제한적',
        '',
        '▪ 결론 및 PolicyPulse의 위치',
        '--기존 도구들: 단일 태스크 특화 또는 자동화 미비',
        '--PolicyPulse: 분류 + 자동 SRL을 결합하여 다목적 정보 추출 플랫폼 실현',
    ], 5)

    # ── 6. 섹션 구분: Methodology ──────────────────────────────
    divider(c, 'Methodology')

    # ── 7. Methodology 1: SRL ───────────────────────────────────
    slide(c, 'Methodology 1: 시맨틱 프레임 추출 (SRL)', [
        '▪ 사용 모델: AllenNLP SRLBert (BERT 기반 의미역 레이블링)',
        '--PropBank 코퍼스 기반 사전 학습 (약 50,000개 술어, 1,118개 동사)',
        '--별도 fine-tuning 없이 AllenNLP 제공 사전 학습 모델 그대로 사용',
        '',
        '===추출 예시',
        '문장: "We may collect location information through cookies when you use our service"',
        '--[ARG0: We]  [V: collect]  [ARG1: location information]',
        '--[ARGM-MNR: through cookies]  [ARGM-TMP: when you use our service]',
        '--→ 하나의 문장에서 "프레임 1(collect)" + "프레임 2(use)" 2개의 프레임 생성',
        '',
        '▪ 정량적 결과',
        '--정책당 평균 70문장 · 문장당 약 4개 프레임 → 정책당 평균 305.7개 프레임 추출',
        '--129,856개 정책에서 총 39,702,767개 프레임 생성',
        '--약 32%의 문장은 SKIP 프레임만 포함 (관련 정보 전혀 없음)',
    ], 7)

    # ── 8. Methodology 2: Frame Classification (table) ─────────
    tbl_slide(c, 'Methodology 2: 프레임 분류 (XLNet 2단계 분류기)',
        ['분류 단계', '레이블', '내용', 'F1 (Two-Level)'],
        [
            ['Level 1', 'SKIP',  '개인정보 무관 프레임 — 학습 데이터의 72.6%',    '0.98'],
            ['Level 1', 'KEEP',  '5개 카테고리 중 하나에 해당하는 관련 프레임',   '0.94'],
            ['Level 2', 'FPCU',  '1자 데이터 수집·사용 (First Party Collection/Use)', '0.98'],
            ['Level 2', 'TPSC',  '제3자 공유·수집 (Third Party Sharing/Collection)',  '0.98'],
            ['Level 2', 'UCC',   '사용자 선택권·통제 — 옵트인/옵트아웃',          '0.98'],
            ['Level 2', 'UAED',  '사용자 데이터 접근·수정·삭제',                  '0.98'],
            ['Level 2', 'DR',    '데이터 보존 기간 (Data Retention)',              '0.96'],
        ],
        [110, 80, 430, 130], 8,
        note='* XLNet을 채택한 이유: 사전 실험에서 BERT 기반 모델 및 전통 분류기 대비 프레임 분류 성능이 우수')

    # ── 9. Methodology 3: Role Mapping ─────────────────────────
    slide(c, 'Methodology 3: 프라이버시 역할 매핑', [
        '▪ 146개 동사에 대해 PropBank 인수 정의 → 프라이버시 전용 역할로 변환',
        '--같은 동사라도 프레임 카테고리(FPCU / TPSC 등)에 따라 다른 역할로 매핑',
        '',
        '===예시: "collect" 동사 (FPCU 카테고리)',
        'ARG0 (행위 주체)   → FIRST_PARTY_ENTITY',
        'ARG1 (행위 대상)   → DATA',
        'ARGM-MNR (방법)   → MECHANISM',
        'ARGM-TMP (시점)   → USER_TRIGGER',
        '',
        '===추출되는 16가지 프라이버시 역할 (주요)',
        'DATA · FIRST_PARTY_ENTITY · THIRD_PARTY_ENTITY · MECHANISM · PURPOSE',
        'SHARING_TERMS · USER_TRIGGER · OPT_IN_MECHANISM · OPT_OUT_MECHANISM',
        'CONSEQUENCE · USER_MECHANISM · TIME_PERIOD · LOCATION  (외 3종)',
    ], 9)

    # ── 10. Methodology 4: Training Data ───────────────────────
    slide(c, 'Methodology 4: 학습 데이터 구성 및 훈련', [
        '▪ 기반 데이터셋: OPP-115',
        '--115개 웹사이트 정책에 12개 카테고리로 주석된 공개 데이터셋 (ACL 2016)',
        '--10,717개 문장에서 SRLBert로 48,783개 프레임 생성 후 146개 관련 동사 기준 필터링',
        '--최종 13,946개 프레임 수동 주석',
        '',
        '▪ 주석 품질 관리',
        '--주석 담당: 프라이버시 정책 주석 경력 3년+ 연구자',
        '--독립 검증: 경력 5년+ 연구자 2명',
        '',
        '▪ 카테고리별 분포 및 증강',
        '--SKIP 10,401  /  FPCU 1,417  /  TPSC 1,230  /  UCC 556  /  UAED 182  /  DR 160',
        '--UCC·UAED·DR 저빈도 카테고리: 동의어 교체 + 문맥 기반 단어 치환으로 증강',
        '',
        '▪ 평가 방식: 10-겹 교차 검증 (9:1 훈련/테스트)',
        '--최적 모델: 각 fold당 검증 손실 기준으로 선택 (6 epoch 훈련)',
    ], 10)

    # ── 11. 섹션 구분: Results & Conclusion ─────────────────────
    divider(c, 'Results', '& Conclusion')

    # ── 12. Results 1: Classification ──────────────────────────
    tbl_slide(c, 'Results: 분류 성능 비교',
        ['방법', 'SKIP', 'FPCU', 'TPSC', 'UCC', 'UAED', 'DR', 'Weighted Avg'],
        [
            ['Frame only',            '0.93', '0.72', '0.70', '0.74', '0.15', '0.24', '0.86'],
            ['FSC Augmented',         '0.92', '0.72', '0.74', '0.86', '0.84', '0.83', '0.88'],
            ['FSC Aug (Ensemble)',     '0.93', '0.79', '0.79', '0.76', '0.65', '0.65', '0.89'],
            ['★ FSC Aug (Two-Level)', '0.98', '0.93', '0.93', '0.93', '0.92', '0.92', '0.97'],
        ],
        [220, 65, 65, 65, 65, 65, 65, 110], 12,
        note='★ 최종 채택 방법. Level1 macro avg F1: 0.96 / Level2 macro avg F1: 0.98')

    # ── 13. Results 2: Large-scale ─────────────────────────────
    slide(c, 'Results: 대규모 정책 분석 (Princeton Privacy Crawl)', [
        '▪ 분석 규모',
        '--130,604개 웹사이트 최신 정책 129,856개  ·  총 39,702,767개 프레임 처리',
        '--정책당 평균 306개 프레임 생성 → KEEP은 평균 30개 (약 10%)',
        '',
        '===정책 완전성 분석: 누락된 핵심 역할',
        '50%의 정책: UAED 프레임 자체가 없음 (사용자 데이터 삭제 권리 전혀 미언급)',
        '60%의 정책: USER_MECHANISM 미기재 (데이터 접근·수정·삭제 방법 불명확)',
        '75%의 정책: CONSEQUENCE 미기재 (옵트인/아웃을 했을 때 어떤 결과인지 불명확)',
        '40%의 정책: MECHANISM 없음 (데이터 수집 방법 미기재)',
        '20%의 정책: USER_TRIGGER 미기재 (언제 수집되는지 명시 안 함)',
        '',
        '===ChatGPT-3.5 비교',
        'ChatGPT: 야후 정책 요약 시 제3자 공유 내용 누락 + 없는 내용 생성(hallucination)',
        'PolicyPulse: 원문 기반 추출 → 환각 없음',
        '--단, GPT-4 등 최신 LLM과의 비교는 향후 연구 과제로 남김',
    ], 13)

    # ── 14. Conclusion ──────────────────────────────────────────
    slide(c, 'Conclusion', [
        '▪ PolicyPulse: SRL + 2단계 XLNet 분류기를 결합한 정보 추출 파이프라인',
        '--기존 단락 수준 분류 → 절(clause) 수준 세밀 추출로 발전',
        '--Weighted avg F1-score 0.97 달성 / 모든 카테고리에서 precision·recall 0.92 이상',
        '',
        '▪ 5가지 잠재적 응용 분야',
        '--정책 완전성 검사 / 짧은 공지(Short Notice) 자동 생성',
        '--개인정보 영양 정보 라벨 / 자동 질의응답 / 사용자 선호도 자동 확인',
        '',
        '▪ 한계점 및 향후 연구',
        '--영어 전용 → 한국어 등 다국어 지원 필요',
        '--문장 간 관계 분석 불가 (문장 수준 분석 한계)',
        '--ChatGPT-3.5와 비교했으나 GPT-4 등 최신 LLM과의 비교 미수행',
        '--생성된 짧은 공지·영양 정보 라벨에 대한 실제 사용자 평가 연구 미수행',
        '',
        '▪ 코드 및 데이터 공개: github.com/crisp-du/ppevo',
    ], 14)

    # ── 15. References ──────────────────────────────────────────
    slide(c, 'References', [
        '[1]  Adhikari et al., "PolicyPulse: Precision Semantic Role Extraction for Enhanced Privacy Policy Comprehension," NDSS 2025.',
        '',
        '[2]  Harkous et al., "Polisis: Automated Analysis and Presentation of Privacy Policies Using Deep Learning," USENIX Security 2018.',
        '',
        '[3]  Cui et al., "PoliGraph: Automated Privacy Policy Analysis using Knowledge Graphs," USENIX Security 2023.',
        '',
        '[4]  Wilson et al., "The Creation and Analysis of a Website Privacy Policy Corpus (OPP-115)," ACL 2016.',
        '',
        '[5]  Yang et al., "XLNet: Generalized Autoregressive Pretraining for Language Understanding," NeurIPS 2019.',
        '',
        '[6]  Bhatia et al., "Mining Privacy Goals from Privacy Policies Using Hybridized Task Analysis," ACM TOCHI 2016.',
        '',
        '[7]  Princeton Privacy Crawl (PPCrawl) Corpus — github.com/citp/privacy-crawl',
    ], 15)

    c.save()
    print(f'✅ 저장: {path}')


make('/Users/jeondonghyeog/Desktop/PaperReview_PolicyPulse_Presentation.pdf')
