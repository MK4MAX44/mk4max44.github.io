from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from PIL import Image

pdfmetrics.registerFont(TTFont('KR', '/Library/Fonts/Arial Unicode.ttf'))

W, H = 1280, 720
TOTAL = 30

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
        badge = ('해석', GREEN)
    elif mode == 'image':
        bg, acc = HexColor('#0A1422'), CYAN
        badge = ('논문 원본', CYAN)
    else:
        bg, acc = BG, BLUE
        badge = None

    c.setFillColor(bg)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BG2)
    c.rect(0, H - 52, W, 52, fill=1, stroke=0)
    c.setFillColor(acc)
    c.rect(0, H - 54, W, 2, fill=1, stroke=0)
    c.setFillColor(TEXT)
    c.setFont('KR', 16)
    c.drawString(44, H - 31, title)
    c.setFont('KR', 10)
    c.setFillColor(TEXT3)
    c.drawRightString(W - 38, H - 31, f'{n} / {TOTAL}')
    if badge:
        label, color = badge
        c.setFillColor(color)
        c.roundRect(W - 130, H - 45, 90, 18, 4, fill=1, stroke=0)
        c.setFillColor(BG)
        c.setFont('KR', 8)
        c.drawCentredString(W - 85, H - 39, label)
    c.setFillColor(BG2)
    c.rect(0, 0, W, 22, fill=1, stroke=0)
    c.setFillColor(TEXT3)
    c.setFont('KR', 7.5)
    c.drawString(44, 6, 'NDSS 2025  ·  PolicyPulse: Precision Semantic Role Extraction  ·  MK4MAX44')


def slide(c, title, items, n, mode='normal'):
    frame(c, title, n, mode)
    acc = GREEN if mode == 'interp' else BLUE
    y = H - 68
    for item in items:
        if not item:
            y -= 5
            continue
        if y < 34:
            break
        if item.startswith('==='):
            txt = item[3:].strip()
            c.setFillColor(BG3)
            c.rect(38, y - 6, W - 76, 21, fill=1, stroke=0)
            c.setFillColor(acc)
            c.rect(38, y - 6, 3, 21, fill=1, stroke=0)
            c.setFillColor(acc)
            c.setFont('KR', 10.5)
            c.drawString(48, y + 4, txt)
            y -= 28
        elif item.startswith('>>'):
            # Term definition
            txt = item[2:].strip()
            c.setFillColor(HexColor('#0D1E14'))
            c.roundRect(44, y - 6, W - 88, 19, 3, fill=1, stroke=0)
            c.setFillColor(AMBER)
            c.roundRect(44, y - 6, 2, 19, 1, fill=1, stroke=0)
            c.setFillColor(AMBER)
            c.setFont('KR', 8)
            c.drawString(52, y + 2, '용어  ')
            # Split term: definition
            if ':' in txt:
                term_part, def_part = txt.split(':', 1)
                c.setFillColor(TEXT2)
                c.setFont('KR', 8.5)
                c.drawString(80, y + 2, f'{term_part.strip()}: {def_part.strip()[:110]}')
            else:
                c.setFillColor(TEXT2)
                c.setFont('KR', 8.5)
                c.drawString(80, y + 2, txt[:115])
            y -= 23
        elif item.startswith('--'):
            txt = item[2:].strip()
            c.setFillColor(acc)
            c.circle(60, y + 3.5, 1.8, fill=1, stroke=0)
            c.setFillColor(TEXT2)
            c.setFont('KR', 10.5)
            lines = wrap(txt, 90)
            for i, l in enumerate(lines):
                c.drawString(68, y - i * 14, l)
            y -= len(lines) * 14 + 4
        else:
            c.setFillColor(acc)
            c.setFont('KR', 13)
            c.drawString(38, y, '▸')
            c.setFillColor(TEXT)
            c.setFont('KR', 11.5)
            lines = wrap(item, 87)
            for i, l in enumerate(lines):
                c.drawString(56, y - i * 15, l)
            y -= len(lines) * 15 + 7
    c.showPage()


def split_slide(c, title, img_path, interp_items, caption, n):
    frame(c, title, n, 'image')
    lx, ly, lw, lh = 32, 30, 564, H - 92
    c.setFillColor(WHITE)
    c.rect(lx, ly, lw, lh, fill=1, stroke=0)
    c.setStrokeColor(CYAN)
    c.setLineWidth(1.5)
    c.rect(lx, ly, lw, lh, fill=0, stroke=1)
    c.drawImage(ImageReader(img_path), lx + 4, ly + 4, lw - 8, lh - 8,
                preserveAspectRatio=True, anchor='c')
    c.setFillColor(TEXT3)
    c.setFont('KR', 7.5)
    c.drawCentredString(lx + lw / 2, 10, caption)

    rx, rw = 608, W - 608 - 28
    c.setFillColor(HexColor('#070F1C'))
    c.rect(rx, ly, rw, lh, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(rx, ly, 2, lh, fill=1, stroke=0)

    y = H - 68
    for item in interp_items:
        if not item:
            y -= 5
            continue
        if y < 38:
            break
        if item.startswith('==='):
            txt = item[3:].strip()
            c.setFillColor(HexColor('#0C2218'))
            c.rect(rx + 8, y - 5, rw - 10, 20, fill=1, stroke=0)
            c.setFillColor(GREEN)
            c.rect(rx + 8, y - 5, 2, 20, fill=1, stroke=0)
            c.setFillColor(GREEN)
            c.setFont('KR', 10)
            c.drawString(rx + 16, y + 4, txt)
            y -= 27
        elif item.startswith('--'):
            txt = item[2:].strip()
            c.setFillColor(GREEN)
            c.circle(rx + 18, y + 3.5, 1.8, fill=1, stroke=0)
            c.setFillColor(TEXT2)
            c.setFont('KR', 10)
            lines = wrap(txt, 42)
            for i, l in enumerate(lines):
                c.drawString(rx + 26, y - i * 13, l)
            y -= len(lines) * 13 + 4
        elif item.startswith('>>'):
            txt = item[2:].strip()
            c.setFillColor(HexColor('#0D1E14'))
            c.roundRect(rx + 8, y - 5, rw - 10, 17, 2, fill=1, stroke=0)
            c.setFillColor(AMBER)
            c.setFont('KR', 8)
            c.drawString(rx + 14, y + 1, txt[:55])
            y -= 21
        else:
            c.setFillColor(GREEN)
            c.setFont('KR', 12)
            c.drawString(rx + 8, y, '▸')
            c.setFillColor(TEXT)
            c.setFont('KR', 11)
            lines = wrap(item, 40)
            for i, l in enumerate(lines):
                c.drawString(rx + 24, y - i * 14, l)
            y -= len(lines) * 14 + 6
    c.showPage()


def tbl_slide(c, title, headers, rows, col_w, n, note='', extra=None):
    frame(c, title, n)
    x0, y0 = 34, H - 66
    rh = 28

    x = x0
    for h, w in zip(headers, col_w):
        c.setFillColor(BLUE_D)
        c.rect(x, y0 - rh, w - 1, rh, fill=1, stroke=0)
        c.setFillColor(BLUE)
        c.rect(x, y0 - rh, w - 1, 1.5, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('KR', 9.5)
        c.drawCentredString(x + w / 2, y0 - rh / 2 - 4, h)
        x += w

    y = y0 - rh
    for ri, row in enumerate(rows):
        rh2 = 24
        x = x0
        is_star = any('★' in cell for cell in row)
        bg = HexColor('#14261A') if is_star else (BG3 if ri % 2 == 0 else BG2)
        for ci, (cell, w) in enumerate(zip(row, col_w)):
            c.setFillColor(bg)
            c.rect(x, y - rh2, w - 1, rh2, fill=1, stroke=0)
            c.setFillColor(GREEN if is_star else (CYAN if ci == 0 else TEXT2))
            c.setFont('KR', 9.5)
            lines = wrap(cell, max(w // 7, 4))
            for li, line in enumerate(lines):
                c.drawString(x + 4, y - 9 - li * 11, line)
            x += w
        y -= rh2

    if note:
        c.setFillColor(TEXT3)
        c.setFont('KR', 7.5)
        c.drawString(34, y - 8, note)
        y -= 18

    if extra:
        y -= 6
        for item in extra:
            if not item:
                y -= 4
                continue
            if y < 34:
                break
            if item.startswith('==='):
                txt = item[3:].strip()
                c.setFillColor(BG3)
                c.rect(34, y - 5, W - 68, 19, fill=1, stroke=0)
                c.setFillColor(BLUE)
                c.rect(34, y - 5, 2, 19, fill=1, stroke=0)
                c.setFillColor(BLUE)
                c.setFont('KR', 9.5)
                c.drawString(42, y + 4, txt)
                y -= 25
            elif item.startswith('--'):
                txt = item[2:].strip()
                c.setFillColor(BLUE)
                c.circle(52, y + 3, 1.5, fill=1, stroke=0)
                c.setFillColor(TEXT2)
                c.setFont('KR', 10)
                lines = wrap(txt, 90)
                for i, l in enumerate(lines):
                    c.drawString(60, y - i * 13, l)
                y -= len(lines) * 13 + 4
            else:
                c.setFillColor(BLUE)
                c.setFont('KR', 12)
                c.drawString(36, y, '▸')
                c.setFillColor(TEXT)
                c.setFont('KR', 11)
                lines = wrap(item, 88)
                for i, l in enumerate(lines):
                    c.drawString(54, y - i * 14, l)
                y -= len(lines) * 14 + 6
    c.showPage()


def divider(c, title, sub='', n=None):
    c.setFillColor(HexColor('#060A12'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BLUE_D)
    c.rect(0, 0, 5, H, fill=1, stroke=0)
    c.rect(W - 5, 0, 5, H, fill=1, stroke=0)
    c.setFillColor(BG2)
    c.rect(5, 0, 26, H, fill=1, stroke=0)
    c.rect(W - 31, 0, 26, H, fill=1, stroke=0)
    c.setFillColor(HexColor('#1C2A42'))
    c.rect(68, H / 2 + 50, W - 136, 1.5, fill=1, stroke=0)
    c.rect(68, H / 2 - 62, W - 136, 1.5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 50)
    c.drawCentredString(W / 2, H / 2 + 6, title)
    if sub:
        c.setFont('KR', 20)
        c.setFillColor(TEXT2)
        c.drawCentredString(W / 2, H / 2 - 42, sub)
    if n:
        c.setFillColor(TEXT3)
        c.setFont('KR', 9)
        c.drawRightString(W - 40, 12, f'{n} / {TOTAL}')
    c.showPage()


def make(path):
    crops = [
        ('/tmp/paper_page-03.png', (40, 100, 1240, 550), '/tmp/final_fig1.png'),
        ('/tmp/paper_page-05.png', (40, 80,  1240, 1300), '/tmp/final_tbl12.png'),
        ('/tmp/paper_page-06.png', (40, 95,  1240, 490), '/tmp/final_tbl3.png'),
        ('/tmp/paper_page-07.png', (30, 90,  1245, 1020), '/tmp/final_fig2.png'),
        ('/tmp/paper_page-07.png', (30, 1080, 1245, 1420), '/tmp/final_tbl4.png'),
        ('/tmp/paper_page-08.png', (30, 130, 1245, 450), '/tmp/final_fig3.png'),
    ]
    for src, box, out in crops:
        Image.open(src).crop(box).save(out)
    print('이미지 크롭 완료')

    c = canvas.Canvas(path, pagesize=(W, H))

    # ── 1. Title ─────────────────────────────────────────────────────
    c.setFillColor(HexColor('#060A12'))
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BG2)
    c.rect(W - 300, 0, 300, H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(W - 303, 0, 3, H, fill=1, stroke=0)
    c.setFillColor(BG3)
    for gx in range(W - 280, W - 16, 24):
        for gy in range(16, H - 16, 24):
            c.circle(gx, gy, 1.5, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(68, 220, 4, 248, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 46)
    c.drawString(88, 408, 'PolicyPulse')
    c.setFillColor(HexColor('#79C0FF'))
    c.setFont('KR', 15)
    c.drawString(88, 360, 'Precision Semantic Role Extraction for')
    c.drawString(88, 337, 'Enhanced Privacy Policy Comprehension')
    c.setStrokeColor(BG3)
    c.setLineWidth(1)
    c.line(88, 320, 620, 320)
    c.setFillColor(TEXT2)
    c.setFont('KR', 12)
    c.drawString(88, 296, 'Andrick Adhikari · Sanchari Das · Rinku Dewri')
    c.drawString(88, 274, 'University of Denver')
    c.setFillColor(TEXT3)
    c.setFont('KR', 10)
    c.drawString(88, 242, 'NDSS 2025  ·  Network and Distributed System Security Symposium')
    c.drawString(88, 222, 'Paper Review  ·  2026.05')

    # Right panel info
    tags = [
        (BLUE, '학회', 'NDSS 2025'),
        (CYAN, '주제', '개인정보 자동 분석'),
        (GREEN, '성능', 'F1 Score 0.97'),
        (AMBER, '규모', '129,856개 정책'),
        (PURPLE, '코드', 'github.com/crisp-du/ppevo'),
    ]
    ry = H - 80
    for color, label, text in tags:
        c.setFillColor(color)
        c.roundRect(W - 280, ry - 2, 48, 17, 3, fill=1, stroke=0)
        c.setFillColor(BG)
        c.setFont('KR', 8)
        c.drawCentredString(W - 256, ry + 5, label)
        c.setFillColor(TEXT2)
        c.setFont('KR', 11)
        c.drawString(W - 224, ry + 5, text)
        ry -= 34

    c.setFillColor(BLUE)
    c.roundRect(88, 66, 118, 24, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 10)
    c.drawCentredString(147, 76, 'MK4MAX44')
    c.showPage()

    # ── 2. TOC ───────────────────────────────────────────────────────
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(BG2)
    c.rect(0, 0, 322, H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(322, 0, 2, H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('KR', 24)
    c.drawString(36, H - 62, '목  차')
    c.setFillColor(BLUE)
    c.rect(36, H - 76, 248, 2, fill=1, stroke=0)

    sections = [
        ('01', '연구 배경 & 선행 연구', BLUE, '슬라이드 3–5'),
        ('02', 'Methodology',           CYAN, '슬라이드 6–14'),
        ('03', 'Results & Analysis',    GREEN, '슬라이드 15–22'),
        ('04', 'Conclusion',            AMBER, '슬라이드 23–25'),
        ('05', 'Q & A',                 PURPLE, '슬라이드 26–28'),
        ('06', 'References',            TEXT2, '슬라이드 29–30'),
    ]
    y = H - 110
    for num, name, acc, pg in sections:
        c.setFillColor(BG3)
        c.rect(28, y - 8, 280, 26, fill=1, stroke=0)
        c.setFillColor(acc)
        c.rect(28, y - 8, 3, 26, fill=1, stroke=0)
        c.setFillColor(acc)
        c.setFont('KR', 9.5)
        c.drawString(40, y + 5, num)
        c.setFillColor(TEXT)
        c.setFont('KR', 11.5)
        c.drawString(64, y + 5, name)
        c.setFillColor(TEXT3)
        c.setFont('KR', 8.5)
        c.drawRightString(304, y + 5, pg)
        y -= 41

    c.setFillColor(WHITE)
    c.setFont('KR', 19)
    c.drawString(350, H - 62, 'Table of Contents')
    c.setFillColor(BG3)
    c.rect(350, H - 76, W - 378, 1.5, fill=1, stroke=0)

    tags_r = [
        (BLUE,   '논문',  'PolicyPulse — NDSS 2025'),
        (CYAN,   '저자',  'Adhikari · Das · Dewri  (Univ. of Denver)'),
        (GREEN,  '주제',  '개인정보처리방침 자동 정보 추출 (SRL 기반)'),
        (AMBER,  '규모',  '129,856개 정책 / 3,970만 프레임 분석'),
        (PURPLE, '성능',  'Weighted Avg F1 = 0.97 달성'),
        (RED,    '핵심',  '60% 정책이 USER_MECHANISM 미기재'),
    ]
    dy = H - 120
    for color, label, text in tags_r:
        c.setFillColor(color)
        c.roundRect(350, dy - 2, 50, 17, 3, fill=1, stroke=0)
        c.setFillColor(BG)
        c.setFont('KR', 8)
        c.drawCentredString(375, dy + 5, label)
        c.setFillColor(TEXT2)
        c.setFont('KR', 11)
        c.drawString(408, dy + 5, text)
        dy -= 30

    c.setFillColor(TEXT3)
    c.setFont('KR', 8)
    c.drawRightString(W - 28, 7, f'2 / {TOTAL}')
    c.showPage()

    # ── 3. Divider: 배경 & 선행연구 ──────────────────────────────────
    divider(c, '연구 배경', '& 선행 연구', 3)

    # ── 4. 배경 1: 왜 문제인가 ───────────────────────────────────────
    slide(c, '배경: 개인정보처리방침, 실제로 읽는 사람이 있을까?', [
        '현실적인 문제',
        '--평균 개인정보처리방침 길이: 약 2,500단어 → 읽는 데 30분 이상 소요',
        '--연간 방문하는 모든 사이트 정책 다 읽으면 약 76일이 걸린다는 연구 있음',
        '--실제로 94%의 사용자가 동의 버튼 누르기 전에 안 읽는다고 응답',
        '',
        '>>개인정보처리방침: 서비스가 사용자 데이터를 어떻게 수집·사용·공유하는지 설명하는 법적 문서. 동의 시 법적 구속력 발생',
        '',
        '법적 환경 변화로 더 복잡해지는 중',
        '--GDPR (2018, EU): 정보 주체 권리 명시 의무 강화 → 정책이 더 길고 복잡해짐',
        '--CCPA (2020, 캘리포니아): 판매 거부권·삭제 요청권 등 신규 조항 추가',
        '--한국 개인정보보호법도 지속적으로 강화 → 사용자는 이해하기 더 어려워짐',
        '',
        '>>GDPR: General Data Protection Regulation — EU 개인정보보호 규정. 위반 시 전 세계 매출의 4% 또는 2,000만 유로 중 큰 금액 벌금',
        '',
        'NLP로 해결할 수 있지 않을까? → 그게 이 논문의 시작점',
        '--기존 도구들이 있긴 한데, 한계가 뚜렷함 (다음 슬라이드)',
    ], 4)

    # ── 5. 배경 2: 기존 도구 비교 ───────────────────────────────────
    tbl_slide(c, '선행 연구: 기존 도구와 PolicyPulse 비교',
        ['도구', '주요 기법', '세부 역할 추출', '범용성', '확장성'],
        [
            ['Polisis\n(2018)',    'OPP-115 기반\n딥러닝 분류',   '✗ 단락 수준만',  '✗ 분류 전용',  '△'],
            ['PoliGraph\n(2023)', 'NER + 지식그래프',             '△ 관계만 추출',  '✗ 특화됨',    '○'],
            ['PolicyLint',        '규칙 + 논리 분석',             '✗',              '✗ 모순 탐지만','△'],
            ['PurPliance',        'SRL (목적절 한정)',             '△ FPCU만',       '✗',           '△'],
            ['★ PolicyPulse',    'SRL + XLNet\n2단계 분류',       '✓ 16가지 역할',  '✓ 5가지 응용','✓'],
        ],
        [150, 190, 210, 160, 100], 5,
        note='SRL: Semantic Role Labeling (의미역 레이블링) / NER: Named Entity Recognition (개체명 인식)',
        extra=[
            '===PolicyPulse가 기존 도구보다 나은 핵심 이유',
            'SRL 기반이라 "누가(AGENT) · 무엇을(DATA) · 어떻게(MECHANISM) · 언제(TRIGGER)" 동시 추출 가능',
            '--단락 수준 분류 도구는 "이 단락에 데이터 수집 내용이 있다/없다"만 알려줌',
            '--역할 추출까지 하면 실제로 어떤 데이터를 누가 어떻게 수집하는지 알 수 있음',
        ])

    # ── 6. Divider: Methodology ──────────────────────────────────────
    divider(c, 'Methodology', n=6)

    # ── 7. 파이프라인 개요 ───────────────────────────────────────────
    slide(c, 'PolicyPulse 4단계 파이프라인', [
        '===Step 1  SRL (Semantic Role Labeling)',
        'AllenNLP SRLBert로 정책 문장에서 프레임(술어+인수 구조) 추출',
        '--정책당 평균 70문장 × 문장당 ~4 프레임 = 정책당 평균 305.7 프레임',
        '-->>SRL: 문장에서 술어(동사)와 그 인수(행위자·대상·방법 등)의 의미 역할을 분석하는 NLP 기술',
        '',
        '===Step 2  프레임 분류',
        'XLNet 2단계 분류기: Level1(SKIP/KEEP) → Level2(FPCU/TPSC/UCC/UAED/DR)',
        '-->>XLNet: 순열 기반 자기회귀 언어 모델. BERT의 한계를 보완한 사전 학습 모델 (Yang et al., 2019)',
        '',
        '===Step 3  프라이버시 역할 매핑',
        'PropBank 인수(ARG0·ARG1·ARGM-MNR 등) → 16가지 프라이버시 전용 역할로 변환',
        '--146개 동사에 대해 카테고리별 역할 매핑 테이블 수동 구축',
        '-->>PropBank: 동사의 인수 구조를 표준화한 대규모 언어 자원. ARG0=행위자, ARG1=대상 등',
        '',
        '===Step 4  대규모 적용',
        'Princeton Privacy Crawl 데이터셋 — 129,856개 정책에 전체 파이프라인 적용',
        '--총 39,702,767개 프레임 처리 / KEEP 프레임만 추출해 정책 완전성 분석',
    ], 7)

    # ── 8. Fig.1 split ───────────────────────────────────────────────
    split_slide(c, '논문 원본 Fig.1 — PolicyPulse 파이프라인 전체 흐름', '/tmp/final_fig1.png', [
        '===Fig.1 왼쪽: SRL 단계',
        '입력 문장에서 SRL이',
        '3개의 프레임 생성',
        '--frame1: include (FPCU)',
        '--frame2: use (SKIP)',
        '--frame3: collect (FPCU)',
        '',
        '===Fig.1 오른쪽: 역할 변환',
        'FPCU 프레임에서',
        'ARG0 → FIRST_PARTY',
        'ARG1 → DATA',
        'ARGM-MNR → MECHANISM',
        'ARGM-TMP → USER_TRIGGER',
        '',
        '===핵심 관찰',
        '문장 하나에서 여러',
        '프레임 동시 생성됨',
        '',
        'SKIP 프레임(frame2)은',
        '분류 단계에서 제거',
        '→ 관련 정보만 남김',
        '',
        '>>ARG0: PropBank 표기. 술어의 주체(Agent) 역할. "We collect data"에서 We에 해당',
    ], 'Fig. 1 — Overview of privacy-specific role extraction in PolicyPulse', 8)

    # ── 9. Step 1: SRL 상세 ─────────────────────────────────────────
    slide(c, 'Step 1: SRL (Semantic Role Labeling) 상세', [
        '사용 모델: AllenNLP SRLBert',
        '--PropBank 코퍼스 기반 사전 학습 (약 50,000개 술어, 1,118개 동사)',
        '--BERT 기반 → fine-tuning 없이 AllenNLP 제공 사전 학습 모델 그대로 사용',
        '-->>AllenNLP: Allen Institute for AI가 개발한 NLP 연구용 오픈소스 라이브러리',
        '',
        '실제 예시 분석',
        '--문장: "We may collect location information through cookies when you use our service"',
        '--frame1 (include): [ARG2: location information] [V: include] [ARG1: IP address and GPS data]',
        '--frame2 (use): [ARG0: you] [V: use] [ARG1: our service] → SKIP (개인정보 무관)',
        '--frame3 (collect): [ARG0: We] [V: collect] [ARG1: location info] [ARGM-MNR: through cookies]',
        '',
        '정량적 결과',
        '--129,856개 정책 / 정책당 평균 306 프레임 / 총 39,702,767개 프레임 생성',
        '--프레임 중 약 32%는 SKIP 프레임만 포함 (완전히 개인정보 무관 문장)',
        '-->>ARGM-MNR: 방법(Manner) 수식어. "쿠키를 통해"처럼 행위 방식을 나타냄',
    ], 9)

    # ── 10. Step 2: 프레임 분류 ─────────────────────────────────────
    slide(c, 'Step 2: XLNet 2단계 분류기', [
        '왜 2단계로 나눴나?',
        '--학습 데이터에서 SKIP이 72.6%(10,401건) — 직접 6-class 분류 시 소수 클래스 학습 어려움',
        '--Level1에서 SKIP/KEEP 먼저 분리 → Level2에서 5가지 카테고리만 집중 분류',
        '-->>SKIP/KEEP: PolicyPulse의 1차 분류. SKIP은 개인정보와 무관한 프레임(ex. 서비스 이용 조건 등)',
        '',
        '5가지 KEEP 카테고리',
        '--FPCU (First Party Collection/Use): 서비스 제공자가 직접 데이터 수집·사용',
        '--TPSC (Third Party Sharing/Collection): 제3자와 데이터 공유 또는 제3자가 수집',
        '--UCC (User Choice/Control): 사용자의 옵트인/옵트아웃 등 선택권',
        '--UAED (User Access/Edit/Deletion): 사용자의 데이터 접근·수정·삭제 권리',
        '--DR (Data Retention): 데이터 보존 기간',
        '',
        'XLNet을 선택한 이유',
        '--순열 기반(permutation-based) 언어 모델링 → 양방향 문맥 + 자기회귀 특성 동시 보유',
        '--사전 실험에서 BERT, SVM, Naive Bayes 대비 프레임 분류 성능 우수 확인',
        '-->>옵트아웃: 데이터 수집·활용에 동의를 철회하는 행위. 반대는 옵트인(사전 동의)',
    ], 10)

    # ── 11. TABLE I/II split ─────────────────────────────────────────
    split_slide(c, '논문 원본 TABLE I/II — 분류 방법별 성능 비교', '/tmp/final_tbl12.png', [
        '===TABLE I 읽는 법',
        '행 = 4가지 학습 방법',
        '열 = 카테고리별 F1',
        '',
        'Frame only',
        '--기본 프레임 텍스트만',
        '--UAED F1 = 0.15 (최저)',
        '',
        'FSC Augmented',
        '--데이터 증강 후',
        '--UAED 0.15 → 0.84',
        '',
        'FSC (Ensemble)',
        '--앙상블로도 한계',
        '',
        '★ FSC (Two-Level)',
        '--최종 채택 방법',
        '--전체 F1 = 0.97',
        '',
        '===TABLE II',
        'Level1 따로: macro 0.96',
        'Level2 따로: macro 0.98',
        '--두 단계 모두 독립적',
        '  고성능 확인',
        '',
        '>>F1-score: 정밀도(Precision)와 재현율(Recall)의 조화평균. 1에 가까울수록 좋음',
    ], 'TABLE I/II — XLNet Cross-Validation Scores (pr: Precision, re: Recall, f1: F1)', 11)

    # ── 12. TABLE I/II 해석 ──────────────────────────────────────────
    slide(c, 'TABLE I/II 해석 — 왜 이 방법이 효과적인가', [
        '===데이터 불균형 문제 해결',
        'SKIP이 72.6% → 6-class 직접 분류 시 모델이 SKIP에만 편향됨',
        '--Two-Level로 SKIP/KEEP 분리 → 각 단계가 자기 문제에만 집중',
        '--결과: UAED F1 0.15 → 0.92 (약 6배 향상), DR 0.24 → 0.92',
        '',
        '>>클래스 불균형: 학습 데이터에서 특정 레이블이 지나치게 많을 때 모델이 다수 클래스에 편향되는 문제',
        '',
        '===데이터 증강의 역할',
        'UAED(182건), DR(160건)은 절대적으로 샘플 부족',
        '--동의어 교체: "collect" → "gather", "obtain" 등',
        '--문맥 기반 단어 치환: textaugment 라이브러리 활용',
        '--증강 없이는 UAED 0.15에서 멈춤 → 증강이 핵심 요소',
        '',
        '===개인적으로 인상적이었던 부분',
        'UAED가 원래 F1 0.15였다는 게 놀라웠음 — 학습 데이터 182건이면 사실상 학습이 안 됨',
        '--근데 증강 + 2단계 구조로 0.92까지 끌어올린 게 이 논문의 진짜 기여라고 생각',
        '-->>textaugment: 텍스트 데이터 증강 라이브러리. 동의어·문맥 대체 등 다양한 방법 지원',
    ], 12, mode='interp')

    # ── 13. Step 3: 역할 매핑 ───────────────────────────────────────
    slide(c, 'Step 3: 프라이버시 역할 매핑 (16가지 역할)', [
        '===변환 원리: PropBank 인수 → 프라이버시 역할',
        '"collect" 동사 / FPCU 카테고리에서:',
        '--ARG0 (행위 주체)   →   FIRST_PARTY_ENTITY (서비스 제공자)',
        '--ARG1 (행위 대상)   →   DATA (수집되는 개인 정보)',
        '--ARGM-MNR (방법)   →   MECHANISM (수집 방법: 쿠키, API 등)',
        '--ARGM-TMP (시점)   →   USER_TRIGGER (수집 시점 조건)',
        '',
        '===16가지 프라이버시 역할 목록',
        'DATA / FIRST_PARTY_ENTITY / THIRD_PARTY_ENTITY',
        'MECHANISM / PURPOSE / SHARING_TERMS',
        'USER_TRIGGER / OPT_IN_MECHANISM / OPT_OUT_MECHANISM',
        'CONSEQUENCE / USER_MECHANISM / TIME_PERIOD',
        'LOCATION / DATA_SUBJECT / RETENTION_PROCESS / RETENTION_TERMS',
        '',
        '===같은 동사라도 카테고리에 따라 역할이 달라짐',
        '"share" 동사가 TPSC(제3자 공유)이면: ARG2 → THIRD_PARTY_ENTITY',
        '"share" 동사가 FPCU(1자 사용)이면: ARG2 → PURPOSE',
        '-->>PURPOSE: 데이터 수집·사용 목적. "for advertising"처럼 왜 쓰는지 나타냄',
    ], 13)

    # ── 14. Step 4: 학습 데이터 ─────────────────────────────────────
    slide(c, 'Step 4: 학습 데이터 구성 (OPP-115 기반)', [
        '===기반 데이터셋: OPP-115',
        '115개 웹사이트 정책 / 12개 카테고리로 수동 주석된 공개 데이터셋 (ACL 2016)',
        '-->>OPP-115: Online Privacy Policies 115개. 각 단락에 데이터 유형·목적 등 12개 카테고리로 태그됨',
        '',
        '===프레임 생성 및 주석 과정',
        '10,717문장 → SRLBert로 48,783 프레임 생성 → 146개 관련 동사 기준 필터링',
        '--최종 13,946개 프레임에 카테고리 수동 주석',
        '--주석 담당: 프라이버시 정책 주석 경력 3년+ 연구자',
        '--독립 검증: 경력 5년+ 연구자 2명 → 불일치 시 토론으로 합의',
        '',
        '===카테고리별 분포 (불균형 심각)',
        'SKIP 10,401  /  FPCU 1,417  /  TPSC 1,230  /  UCC 556  /  UAED 182  /  DR 160',
        '--SKIP이 전체의 74.5%로 압도적 → 2단계 분류 + 증강이 필수였던 이유',
        '',
        '===평가 방식',
        '10-겹 교차 검증 (9:1 훈련/테스트 분할)',
        '--6 epoch 훈련 / 각 fold당 검증 손실 기준으로 최적 모델 선택',
        '-->>교차 검증: 데이터를 10등분하여 9개로 학습, 1개로 평가를 반복해 평균 성능 측정',
    ], 14)

    # ── 15. Divider: Results ─────────────────────────────────────────
    divider(c, 'Results', '& Analysis', 15)

    # ── 16. Results: 분류 성능 테이블 ───────────────────────────────
    tbl_slide(c, 'Results: 분류 성능 비교 (F1-score)',
        ['방법', 'SKIP', 'FPCU', 'TPSC', 'UCC', 'UAED', 'DR', 'W.Avg'],
        [
            ['Frame only',        '0.93', '0.72', '0.70', '0.74', '0.15', '0.24', '0.86'],
            ['FSC Augmented',     '0.92', '0.72', '0.74', '0.86', '0.84', '0.83', '0.88'],
            ['FSC (Ensemble)',    '0.93', '0.79', '0.79', '0.76', '0.65', '0.65', '0.89'],
            ['★ FSC (Two-Level)','0.98', '0.93', '0.93', '0.93', '0.92', '0.92', '0.97'],
        ],
        [220, 62, 62, 62, 62, 62, 62, 90], 16,
        note='★ 최종 채택. Level1 macro avg F1: 0.96 / Level2 macro avg F1: 0.98 / W.Avg = Weighted Average',
        extra=[
            '===수치 해석',
            'UAED와 DR: 학습 데이터 각 182·160건이지만 증강 + Two-Level로 F1 0.92 달성',
            '--FSC Augmented에서 UAED 0.15 → 0.84로 급등: 데이터 증강이 결정적 역할',
            '--Ensemble은 오히려 성능이 떨어지는 경우도 있음 → 구조적 접근(Two-Level)이 더 효과적',
            'precision·recall 모두 각 카테고리에서 0.92 이상 → 과적합 없이 균형잡힌 성능',
        ])

    # ── 17. TABLE III split ──────────────────────────────────────────
    split_slide(c, '논문 원본 TABLE III — 16가지 프라이버시 역할 정의', '/tmp/final_tbl3.png', [
        '===핵심 역할 요약',
        'DATA',
        '--개인·민감 정보 총칭',
        '  (이름·위치·이메일 등)',
        '',
        'MECHANISM',
        '--수집 방법·절차',
        '  (쿠키·API·로그 등)',
        '',
        'USER_MECHANISM',
        '--사용자가 직접',
        '  데이터 관리하는 방법',
        '  (설정 페이지·이메일 등)',
        '',
        'CONSEQUENCE',
        '--옵트인/아웃 결과',
        '  (서비스 제한·데이터 삭제)',
        '',
        'USER_TRIGGER',
        '--수집 발생 조건',
        '  (서비스 이용 시·가입 시)',
        '',
        '===왜 중요한가',
        'USER_MECHANISM이',
        '60% 정책에서 누락',
        '→ GDPR 위반 소지',
    ], 'TABLE III — Privacy-Specific Roles Mapped from PropBank Frame Arguments', 17)

    # ── 18. Fig.2 split ──────────────────────────────────────────────
    split_slide(c, '논문 원본 Fig.2 + TABLE IV — 대규모 분석 프레임 분포', '/tmp/final_fig2.png', [
        '===Fig.2 왼쪽 그래프',
        '전체 vs KEEP 프레임',
        '정책별 분포',
        '',
        '총 프레임: 오른쪽으로',
        '길게 치우친 분포',
        '→ 정책마다 길이 편차',
        '  매우 큼',
        '',
        '===Fig.2 오른쪽 그래프',
        'KEEP 프레임 분포',
        '(90th percentile 기준)',
        '',
        '중위수(median) = 30',
        '→ 절반의 정책은',
        '  30개 이하 KEEP',
        '',
        '===TABLE IV',
        'KEEP 프레임 중 카테고리',
        '별 비율 (평균)',
        '',
        'FPCU 45% / TPSC 17%',
        'UCC 13% / UAED 5%',
        '→ UAED가 가장 적음',
        '',
        '>>중위수(Median): 데이터를 크기 순으로 정렬했을 때 정중앙 값. 극단값에 덜 민감',
    ], 'Fig. 2 — Frame distribution / TABLE IV — KEEP frame composition', 18)

    # ── 19. Fig.3 split ──────────────────────────────────────────────
    split_slide(c, '논문 원본 Fig.3 — 카테고리 간 공출현(Co-occurrence) 분석', '/tmp/final_fig3.png', [
        '===Fig.3 읽는 법',
        '행·열 = 5개 카테고리',
        '숫자 = 공출현 비율',
        '1.0 = 자기 자신',
        '',
        '===주요 관찰',
        'FPCU ↔ TPSC: 0.64',
        '--같은 문장에서',
        '  1자·3자 수집이',
        '  함께 나오는 경우',
        '  매우 흔함',
        '',
        'FPCU ↔ DR: 0.63',
        '--데이터 수집 언급 시',
        '  보존 기간도 함께',
        '  나오는 편',
        '',
        'UAED ↔ DR: 0.47',
        '--삭제 권리 + 보존',
        '  기간은 자주 같이',
        '  나옴 (연관성 높음)',
        '',
        '===시사점',
        '카테고리 간 공출현이',
        '높으면 분류가 어려움',
        '→ Two-Level 구조가',
        '  더 필요한 이유',
    ], 'Fig. 3 — Co-occurrence proportion between KEEP frame categories', 19)

    # ── 20. 대규모 분석: 정책 완전성 ────────────────────────────────
    slide(c, 'Results: 대규모 분석 — 129,856개 정책의 완전성 점검', [
        '분석 규모',
        '--130,604개 웹사이트 → 사이트당 가장 최신 정책 1개 선택 = 129,856개',
        '--총 39,702,767개 프레임 처리 / KEEP 평균 30개 (전체의 약 10%)',
        '-->>Princeton Privacy Crawl (PPCrawl): 2020년 전후 130만+ 사이트 정책 수집 데이터셋',
        '',
        '===핵심 역할 누락 비율 (법적·윤리적 문제)',
        '50%: UAED 프레임 자체 없음 — 사용자 데이터 삭제 권리를 아예 언급 안 함',
        '60%: USER_MECHANISM 미기재 — 어떻게 접근·수정·삭제하는지 방법을 안 알려줌',
        '75%: CONSEQUENCE 미기재 — 옵트인/아웃 했을 때 뭐가 달라지는지 설명 없음',
        '40%: MECHANISM 없음 — 어떤 방법으로 데이터를 수집하는지 미기재',
        '20%: USER_TRIGGER 미기재 — 언제 데이터가 수집되는지 조건을 명시 안 함',
        '',
        '===UAED 분포 (중위수 = 0)',
        '전체 정책의 50%는 UAED 프레임이 0개 — 삭제 관련 내용이 한 줄도 없음',
        '--나머지 50%도 평균 UAED 프레임 수는 매우 적음 (분포 오른쪽 치우침)',
    ], 20)

    # ── 21. 대규모 분석 해석 ────────────────────────────────────────
    slide(c, '대규모 분석 해석 — 이게 왜 심각한 문제인가', [
        '===GDPR·CCPA가 보장하는 권리를 정책이 설명 안 함',
        'UAED = 사용자 데이터 접근·수정·삭제 권리 → GDPR Article 17 "삭제권(Right to be Forgotten)"',
        '--절반의 사이트가 이 법적 권리를 정책에 명시조차 안 한다는 게 이 연구의 핵심 발견',
        '-->>Right to be Forgotten (삭제권): GDPR에서 보장하는 권리. 서비스에 자신의 데이터 삭제를 요청 가능',
        '',
        '===CONSEQUENCE 75% 누락의 현실적 의미',
        '광고 수신 거부(옵트아웃) 버튼을 눌렀을 때 실제로 뭐가 달라지는지 안 알려줌',
        '--계정 기능 제한? 일부 데이터만 삭제? 완전 삭제? → 정책이 침묵하고 있음',
        '--사용자는 동의를 철회해도 그게 어떤 효과를 낳는지 알 방법이 없는 셈',
        '',
        '===연구의 진짜 의의',
        '"개인정보처리방침 읽기 어렵다"는 주관적 불만과 달리 정량적 증거를 제공',
        '--130만 개 정책을 자동 분석해서 "어떤 내용이 얼마나 빠져있나"를 수치로 보여줌',
        '--규제 당국이 컴플라이언스 검사에, 사용자가 권리 확인에, 연구자가 비교 분석에 활용 가능',
        '-->>컴플라이언스(Compliance): 법·규정·내부 정책 등을 준수하는 것. 미준수 시 벌금·제재 가능',
    ], 21, mode='interp')

    # ── 22. ChatGPT 비교 ─────────────────────────────────────────────
    slide(c, 'ChatGPT-3.5 vs PolicyPulse — 같은 정책 요약해보니', [
        '===실험 방법',
        '야후(Yahoo) 개인정보처리방침을 ChatGPT-3.5와 PolicyPulse에 각각 넣고 결과 비교',
        '',
        '===ChatGPT-3.5 결과의 문제점',
        '제3자 데이터 공유 관련 내용을 요약에서 빠뜨림 (누락)',
        '--원문에는 없는 내용을 추가로 생성 → hallucination(환각) 발생',
        '-->>Hallucination(환각): LLM이 실제 없는 내용을 있는 것처럼 생성하는 현상. 신뢰성 문제의 핵심',
        '',
        '===PolicyPulse 결과',
        '원문에 있는 프레임만 추출 → 없는 내용 생성 안 함 (환각 없음)',
        '--각 역할(DATA·MECHANISM·CONSEQUENCE 등) 단위로 정확하게 분리 추출',
        '--단점: GPT-4 등 최신 LLM과는 비교하지 않음 (저자도 향후 과제로 명시)',
        '',
        '===내 생각',
        'LLM이 유연하고 자연스럽지만 개인정보처리방침 같은 법적 문서에서는',
        '--환각이 단 한 번만 나와도 신뢰할 수 없는 도구가 됨',
        '--PolicyPulse처럼 룰 기반 매핑이 확실성 면에서 더 안전한 선택일 수 있음',
    ], 22)

    # ── 23. 5가지 응용 분야 ─────────────────────────────────────────
    slide(c, '5가지 잠재적 응용 분야', [
        '===① 정책 완전성 검사 (Policy Completeness Checking)',
        '법적 필수 항목(GDPR의 USER_MECHANISM 등)이 정책에 포함됐는지 자동 체크',
        '--기업이 정책 작성 시, 규제 당국이 컴플라이언스 감사 시 활용 가능',
        '',
        '===② 짧은 공지(Short Notice) 자동 생성',
        '긴 정책에서 핵심 역할만 추출해 1페이지 요약본 자동 생성',
        '--EU·영국 규제 기관이 권장하는 "Layered Privacy Notice" 방식과 연결 가능',
        '',
        '===③ 개인정보 영양 정보 라벨',
        '식품 성분표처럼 데이터 수집 항목·목적·기간을 표준화된 형식으로 제시',
        '-->>영양 정보 라벨 방식: 복잡한 정책을 아이콘·항목 형식으로 시각화하는 접근. 여러 연구에서 제안됨',
        '',
        '===④ 자동 질의응답 (Q&A System)',
        '"이 서비스가 내 위치 데이터를 제3자에게 공유하나요?" 같은 질문에 자동 답변',
        '--추출된 프레임 기반이라 환각 없이 원문에 근거한 답변 제공',
        '',
        '===⑤ 사용자 선호도 자동 확인',
        '사용자가 설정한 프라이버시 선호(ex. 마케팅 수신 거부)와 정책 내용 자동 비교·알림',
    ], 23)

    # ── 24. Divider: Conclusion ──────────────────────────────────────
    divider(c, 'Conclusion', n=24)

    # ── 25. Conclusion ───────────────────────────────────────────────
    slide(c, 'Conclusion — 논문이 남긴 것', [
        '===핵심 기여 요약',
        'SRL + 2단계 XLNet 분류기 → 단락 수준 분류에서 절(clause) 수준 세밀 추출로 발전',
        '--기존: "이 단락에 데이터 수집 내용이 있다" / 이제: "누가·무엇을·어떻게·언제"까지',
        '--Weighted avg F1 0.97 / 모든 카테고리 precision·recall 0.92 이상',
        '',
        '===숫자로 보는 성과',
        '129,856개 정책 분석 / 3,970만+ 프레임 처리 / 16가지 프라이버시 역할 추출',
        '--처리 규모 자체가 기존 SRL 기반 연구(5개 정책, 202문장)와 비교도 안 됨',
        '',
        '===보고 나서 든 생각',
        '솔직히 처음 봤을 때 "SRL이 개인정보처리방침에 이렇게 잘 맞나?" 싶었는데',
        '--PropBank 인수 구조가 "누가·무엇을·어떻게"를 자연스럽게 추출해주는 게 딱 맞았음',
        '--데이터 증강으로 희소 카테고리 문제를 해결한 것도 실용적인 접근이라 인상적이었음',
        '',
        '코드·데이터 공개: github.com/crisp-du/ppevo',
    ], 25)

    # ── 26. 한계점 ───────────────────────────────────────────────────
    slide(c, '한계점 & 향후 과제', [
        '===현재 한계',
        '영어 전용 → 한국어·중국어 등 다국어 지원 불가',
        '--한국어 개인정보처리방침 분석하려면 한국어 SRL 모델 + 주석 데이터 필요',
        '-->>한국어 SRL: KLUE-SRL 등 한국어 의미역 레이블링 데이터셋 존재. 추후 연구 가능성 있음',
        '',
        '문장 내 분석은 되지만 문장 간 관계는 모름',
        '--"앞 문장에서 수집한 데이터를 이 문장에서 제3자와 공유한다"는 연결 불가',
        '--SRL 자체의 한계 — 담화 수준(discourse-level) 분석은 별도 연구 필요',
        '',
        'GPT-4 등 최신 LLM과 정면 비교 안 함',
        '--GPT-3.5만 비교 → 실제 현업 도구(GPT-4, Claude 등)와의 차이가 궁금',
        '--저자도 "추후 연구 과제"로 명시 → 2025년 이후 후속 연구 기대',
        '',
        '===향후 연구 방향',
        '생성된 짧은 공지·영양 정보 라벨에 대한 실제 사용자 평가 연구 미수행',
        '--이게 실제로 이해하기 쉬운지 A/B 테스트나 사용자 실험 필요',
        '--다국어 확장 / LLM 결합(PolicyPulse로 추출 + LLM으로 자연어 설명) 연구 가능',
    ], 26)

    # ── 27. Divider: Q&A ─────────────────────────────────────────────
    divider(c, 'Q & A', '예상 질문 & 답변', 27)

    # ── 28. Q&A 방법론 ───────────────────────────────────────────────
    slide(c, '예상 질문 & 답변 — 방법론 관련', [
        '===Q. SRL 모델을 fine-tuning 없이 써도 괜찮은가?',
        '프레임 추출 자체(Step 1)는 PropBank 사전 학습으로 충분히 커버됨',
        '--"collect", "share" 같은 동사는 PropBank에 잘 정의돼 있음',
        '--분류(Step 2)와 역할 매핑(Step 3)이 도메인 특화를 담당 → 역할 분리 설계의 장점',
        '',
        '===Q. XLNet을 선택한 근거가 있나?',
        '논문 내 사전 실험(ablation study): BERT·SVM·Naive Bayes 대비 F1 성능 우수',
        '--특히 복잡한 조건절("when you use our service")이 많은 개인정보처리방침에서 차이 남',
        '-->>Ablation Study: 모델 구성 요소를 하나씩 제거해가며 각 요소의 기여도를 측정하는 실험',
        '',
        '===Q. 146개 동사 매핑은 어떻게 구축했나?',
        'OPP-115 학습 데이터에서 실제 나온 동사들만 대상 → 전수 수동 분석',
        '--각 동사의 PropBank 프레임셋 참조 → 카테고리별 역할 매핑 테이블 구축',
        '--완전 자동화가 아닌 수작업 → 신뢰성 높지만 확장성은 제한',
        '',
        '===Q. 학습 데이터 주석 품질은 어떻게 보장했나?',
        '경력 3년+ 연구자 주석 / 경력 5년+ 연구자 2명 독립 검증 / 불일치 토론 합의',
        '--Cohen Kappa 계수(주석자 간 일치도) 등 품질 지표를 논문에서 보고함',
    ], 28)

    # ── 29. Q&A 결과/활용 ───────────────────────────────────────────
    slide(c, '예상 질문 & 답변 — 결과 & 활용', [
        '===Q. F1 0.97인데 어떤 케이스에서 틀리나?',
        'DR(Data Retention), UAED 카테고리에서 상대적으로 낮음',
        '--이유: 학습 데이터 부족 + 다른 카테고리(FPCU 등)와 문장이 같이 나오는 경우 혼동',
        '--예: "We retain your data for 30 days after you delete your account" → UAED인가 DR인가?',
        '',
        '===Q. GPT-4와 비교하지 않은 이유?',
        '논문 작성 시점(2024년 초)에 GPT-4 API 비용 및 접근성 문제가 있었을 가능성',
        '--저자도 "GPT-4 등 최신 LLM과의 비교는 향후 과제"라고 명시',
        '--GPT-4는 환각 감소됐지만 여전히 발생 → PolicyPulse의 환각 없는 추출과 비교 흥미로울 것',
        '',
        '===Q. 한국어 개인정보처리방침에 적용 가능한가?',
        '현재는 불가. 영어 SRL 모델 + 영어 주석 데이터만 사용',
        '--한국어 적용하려면: ① 한국어 SRL 모델(KLUE 등) ② 한국어 정책 주석 데이터 필요',
        '-->>KLUE: Korean Language Understanding Evaluation. 한국어 NLP 벤치마크 데이터셋 모음',
        '',
        '===Q. 가장 충격적인 발견은?',
        '60%의 정책이 USER_MECHANISM 미기재 + 75%가 CONSEQUENCE 미기재',
        '--법적으로 보장된 권리인데 절반 이상의 사이트가 정책에 설명조차 안 하고 있다는 것',
    ], 29)

    # ── 30. References ───────────────────────────────────────────────
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
        '[7]  Lippi et al., "CLAUDETTE: An Automated Detector of Potentially Unfair Clauses in Online Terms of Service," AI & Law 2019.',
        '',
        '[8]  Princeton Privacy Crawl (PPCrawl) — github.com/citp/privacy-crawl',
    ], 30)

    c.save()
    print(f'✅ 저장 완료: {path}  ({TOTAL}슬라이드)')


make('/Users/jeondonghyeog/Desktop/PaperReview_PolicyPulse_Final.pdf')
