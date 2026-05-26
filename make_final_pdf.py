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

    # Right panel — key method summary
    kx = 350
    c.setFillColor(BG3)
    c.rect(kx, dy - 12, W - kx - 28, 19, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(kx, dy - 12, 3, 19, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.setFont('KR', 10)
    c.drawString(kx + 10, dy - 3, '핵심 방법론')
    dy -= 32
    method_items = [
        (CYAN,   'SRL',    'AllenNLP SRLBert — 프레임 추출'),
        (GREEN,  'XLNet',  '2단계 분류 — SKIP/KEEP → 5-class'),
        (AMBER,  '역할',   '16가지 프라이버시 역할 매핑'),
        (PURPLE, '증강',   'textaugment 동의어 대체 (소수 클래스)'),
    ]
    for mc, ml, mt in method_items:
        c.setFillColor(mc)
        c.roundRect(kx, dy - 1, 44, 15, 2, fill=1, stroke=0)
        c.setFillColor(BG)
        c.setFont('KR', 7.5)
        c.drawCentredString(kx + 22, dy + 5, ml)
        c.setFillColor(TEXT2)
        c.setFont('KR', 10.5)
        c.drawString(kx + 52, dy + 5, mt)
        dy -= 26

    c.setFillColor(TEXT3)
    c.setFont('KR', 8)
    c.drawRightString(W - 28, 7, f'2 / {TOTAL}')
    c.showPage()

    # ── 3. Divider: 배경 & 선행연구 ──────────────────────────────────
    divider(c, '연구 배경', '& 선행 연구', 3)

    # ── 4. 배경 1: 왜 문제인가 ───────────────────────────────────────
    slide(c, '배경: 개인정보처리방침, 실제로 읽는 사람이 있을까?', [
        '===현실: 아무도 안 읽는 긴 문서',
        '평균 개인정보처리방침 길이: 약 2,500~4,000단어 → 전부 읽는 데 30분 이상 소요',
        '--연간 방문 사이트 전체 정책 다 읽으면 76일 걸린다는 연구 (McDonald & Cranor 2008)',
        '--94%의 사용자가 동의 버튼 전에 안 읽음 / 42%는 "읽기 불가능"이라고 응답',
        '--상위 500개 웹사이트 평균 독해 수준: 대학교 2학년 이상 (Flesch-Kincaid 기준)',
        '--Apple 개인정보처리방침 30,000단어 / Google 약 27,000단어로 매년 증가 추세',
        '',
        '>>개인정보처리방침: 서비스가 사용자 데이터를 어떻게 수집·사용·공유하는지 설명하는 법적 문서',
        '>>Flesch-Kincaid: 텍스트 가독성 지수. 12 이하가 대학원 수준. 정책 평균은 약 14~16',
        '',
        '===법 강화로 정책이 더 복잡해지는 악순환',
        'GDPR (2018, EU): 정보 주체 6가지 권리·13가지 고지 항목 명시 의무 → 정책 길이 증가',
        '--CCPA (2020, 캘리포니아): 판매 거부권·삭제권·차별 금지·연간 공개 보고 조항 추가',
        '--LGPD (2020, 브라질) / PIPL (2021, 중국) / 한국 개인정보보호법 2023년 개정',
        '--법이 강화될수록 정책은 더 길어지고 → 사용자는 더 이해하기 어려워지는 역설',
        '-->>#Legal-Notice 의무화: 수집 목적·보유 기간·제3자 제공 여부 등을 명시해야 하는 법적 의무',
        '>>CCPA: California Consumer Privacy Act. 50만 달러 이상 매출 기업 적용. 위반 시 건당 $7,500',
        '',
        '===기술적 해결 시도의 한계 → PolicyPulse의 출발점',
        '단락 분류 도구(Polisis 등): "이 단락이 개인정보 관련인가/아닌가" 이진 판단만 가능',
        '--실제로 필요한 것: "내 위치 데이터를 누가, 왜, 어떤 방법으로, 언제까지 수집하나"',
        '--SRL이 문장의 술어·행위자·대상·방법·시점을 동시에 추출 → 개인정보처리방침과 구조적 궁합',
        '>>NLP(Natural Language Processing): 자연어 처리. 컴퓨터가 인간 언어를 이해·분석하는 AI 분야',
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
            '--단락 수준 분류: "이 단락에 데이터 수집 내용이 있다/없다" 수준만 판단 가능',
            '--역할 추출까지 하면 실제로 어떤 데이터를 누가 어떻게 수집하는지 상세히 알 수 있음',
            '',
            '===각 도구의 구체적 한계',
            'Polisis: 107가지 세부 분류 지원하지만 각 분류가 YES/NO 이진 플래그 — 역할 구조 없음',
            '--PoliGraph: 지식 그래프로 관계 추출하지만 "제3자와 데이터 공유함" 수준, 어떤 데이터인지 모름',
            '--PurPliance: SRL 최초 도입했지만 "data collection" 목적절(purpose clause)만 분석하여 범위 매우 좁음',
            '-->>지식 그래프(Knowledge Graph): 개체(entity)와 관계(relation)를 노드-엣지 구조로 표현하는 그래프 데이터베이스',
        ])

    # ── 6. Divider: Methodology ──────────────────────────────────────
    divider(c, 'Methodology', n=6)

    # ── 7. 파이프라인 개요 ───────────────────────────────────────────
    slide(c, 'PolicyPulse 4단계 파이프라인', [
        '===Step 1  SRL (Semantic Role Labeling) — 구조 파싱',
        'AllenNLP SRLBert로 정책 문장에서 프레임(술어+인수 구조) 추출',
        '--정책당 평균 70문장 × 문장당 평균 4.3 프레임 = 정책당 평균 305.7 프레임',
        '--동사(술어) 하나당 프레임 1개 생성 → 문장에 동사 여러 개이면 여러 프레임 동시 생성',
        '--fine-tuning 없이 PropBank 사전 학습 모델 그대로 사용 (개인정보 동사와 궁합 좋음)',
        '-->>"We collect location data through cookies" → ARG0(We), V(collect), ARG1(location data), ARGM-MNR(cookies)',
        '',
        '===Step 2  프레임 분류 — 관련성 및 카테고리 판정',
        'XLNet 2단계: Level1 (SKIP/KEEP 이진) → Level2 (FPCU/TPSC/UCC/UAED/DR 5-class)',
        '--2단계인 이유: SKIP 72.6% 데이터 불균형 → 단계 분리로 소수 클래스 집중 학습',
        '--학습 데이터: OPP-115 기반 13,946개 수동 주석 프레임 / 10-겹 교차 검증',
        '-->>XLNet: 순열 기반 자기회귀 LM. BERT보다 양방향 문맥 + 자기회귀 특성 동시 보유',
        '',
        '===Step 3  프라이버시 역할 매핑 — 의미 추출',
        'PropBank 인수(ARG0·ARG1·ARGM-MNR 등) → 16가지 프라이버시 전용 역할로 변환',
        '--146개 동사 × 카테고리별 매핑 테이블 수동 구축 (같은 ARG도 동사·카테고리에 따라 의미 다름)',
        '--예: "collect" ARG1 → DATA / "share" ARG1 → THIRD_PARTY_ENTITY (카테고리: TPSC)',
        '-->>PropBank: 영어 동사 인수 구조 표준화 자원. ARG0=행위자, ARG1=대상, ARGM=수식어',
        '',
        '===Step 4  대규모 적용 — 완전성 분석',
        'Princeton Privacy Crawl (PPCrawl) — 130,604개 사이트 중 최신 1개 = 129,856개',
        '--총 39,702,767개 프레임 → KEEP 추출 → 역할별 등장 여부 집계 → 누락 통계 산출',
        '-->>PPCrawl: 프린스턴대 공개 데이터셋. 2020년 전후 130만+ 사이트 정책 수집본',
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
        '===사용 모델: AllenNLP SRLBert — 선택 이유',
        'PropBank 코퍼스 기반 사전 학습 (약 50,000개 술어, 1,118개 동사 커버)',
        '--fine-tuning 없이 AllenNLP 제공 사전 학습 모델 그대로 사용 (도메인 적응 불필요)',
        '--개인정보처리방침 동사("collect", "share", "disclose", "retain" 등) PropBank에 잘 정의됨',
        '-->>AllenNLP: Allen Institute for AI 개발 NLP 라이브러리. BERT 기반 SRL·NER·공참조 해소 모델 포함',
        '-->>PropBank: Penn Treebank 기반 동사 의미역 표준화 코퍼스. ARG0=행위자, ARG1=피행위자 등',
        '',
        '===실제 예시 — 문장 1개에서 프레임 3개 생성',
        '"We may collect location info through cookies when you use our service"',
        '--frame1 (include): [ARG1: IP address and GPS data] [V: include] → SKIP (서비스 설명)',
        '--frame2 (use): [ARG0: you] [V: use] [ARG1: our service] → SKIP (사용자 행위)',
        '--frame3 (collect): [ARG0: We] [V: collect] [ARG1: location info] [ARGM-MNR: through cookies] → KEEP(FPCU)',
        '-->>ARGM-MNR: Manner 수식어. "쿠키를 통해" / ARGM-TMP: 시간 / ARGM-PRP: 목적 / ARGM-ADV: 부사',
        '',
        '===정량 결과 및 분포',
        '129,856개 정책 / 정책당 평균 305.7 프레임 / 총 39,702,767개 프레임 생성',
        '--학습 데이터(OPP-115): 10,717문장 → 48,783 프레임 → 146개 관련 동사 필터 → 최종 13,946개',
        '--전체 프레임 분포: SKIP 74.5% / FPCU 10.2% / TPSC 8.8% / UCC 4.0% / UAED 1.3% / DR 1.1%',
        '--동사 146개 선정 기준: OPP-115 학습 데이터에 실제 등장한 동사 중 개인정보 관련성 수동 확인',
        '>>OPP-115: 115개 웹사이트 정책에 12개 프라이버시 카테고리로 수동 주석한 ACL 2016 공개 데이터셋',
    ], 9)

    # ── 10. Step 2: 프레임 분류 ─────────────────────────────────────
    slide(c, 'Step 2: XLNet 2단계 분류기', [
        '===왜 2단계로 나눴나? — 클래스 불균형 해결',
        '학습 데이터: SKIP 72.6%(10,401건) / FPCU 10.2% / TPSC 8.8% / UCC 4.0% / UAED 1.3% / DR 1.1%',
        '--6-class 직접 분류 시 UAED(182건)·DR(160건)은 전체의 1%대 → SKIP에 압도당해 학습 실패',
        '--Level1 이진 분류 → Level2 5-class 분류: 각 단계가 자기 역할에만 집중할 수 있음',
        '--Level1 후 SKIP 폐기 → Level2 입력에서 SKIP 비율 0% → 클래스 불균형 극적으로 완화',
        '-->>클래스 불균형(Class Imbalance): 학습 데이터에서 특정 레이블이 지나치게 많아 모델 편향 발생',
        '',
        '===5가지 KEEP 카테고리 — KEEP 프레임 내 비율',
        'FPCU (First Party Collection/Use): 서비스 제공자 직접 수집·사용 → 45% (가장 많음)',
        '--TPSC (Third Party Sharing/Collection): 광고사·분석사 등 제3자 공유 또는 수집 → 17%',
        '--UCC (User Choice/Control): 옵트인·옵트아웃·쿠키 설정 등 사용자 선택권 → 13%',
        '--UAED (User Access/Edit/Deletion): 데이터 접근·수정·삭제 권리 — GDPR Art.17 → 5%',
        '--DR (Data Retention): 보존 기간·방식·파기 절차 → 5%',
        '-->>GDPR Article 17 "삭제권": 개인이 서비스에 자신의 데이터 삭제를 요청할 수 있는 권리',
        '',
        '===XLNet 학습 설정 및 모델 선택 근거',
        'XLNet-base / batch size 16 / 6 epochs / max sequence length 128 토큰',
        '--검증 손실(validation loss) 기준으로 6 epoch 중 최적 모델 선택 (과적합 방지)',
        '--사전 실험 비교: BERT → XLNet보다 낮음 / SVM·Naive Bayes → XLNet보다 현저히 낮음',
        '>>XLNet: Permutation Language Modeling 기반. BERT의 마스크 토큰 의존성 한계를 극복한 모델',
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
        '===변환 원리: PropBank 인수 → 프라이버시 역할 (카테고리·동사에 따라 다름)',
        '"collect" 동사 + FPCU 카테고리:',
        '--ARG0 (행위 주체) → FIRST_PARTY_ENTITY (서비스 제공자: "We", "Company")',
        '--ARG1 (행위 대상) → DATA (수집되는 정보: "email", "location", "browsing history")',
        '--ARGM-MNR (방법) → MECHANISM (수집 방법: "through cookies", "via API", "automatically")',
        '--ARGM-TMP (시점) → USER_TRIGGER (수집 조건: "when you use our service", "upon registration")',
        '--ARGM-PRP (목적) → PURPOSE (수집 목적: "to improve our services", "for analytics")',
        '',
        '===16가지 프라이버시 역할 — 카테고리별 그룹',
        'FPCU: DATA / FIRST_PARTY_ENTITY / MECHANISM / PURPOSE / USER_TRIGGER',
        '--TPSC: THIRD_PARTY_ENTITY / SHARING_TERMS / DATA / MECHANISM',
        '--UCC: OPT_IN_MECHANISM / OPT_OUT_MECHANISM / CONSEQUENCE',
        '--UAED: USER_MECHANISM / DATA_SUBJECT / LOCATION',
        '--DR: TIME_PERIOD / RETENTION_PROCESS / RETENTION_TERMS',
        '-->>USER_MECHANISM: 사용자가 직접 데이터를 관리하는 방법. "settings page", "email us at" 등',
        '',
        '===같은 동사, 다른 카테고리 → 완전히 다른 매핑',
        '"share" + TPSC: ARG1→DATA / ARG2→THIRD_PARTY_ENTITY / ARGM-MNR→SHARING_TERMS',
        '"share" + FPCU: ARG1→DATA / ARG2→PURPOSE ("to provide better service")',
        '--이 카테고리별 차이가 자동 매핑 불가 이유 → 146개 동사 모두 수동 매핑 테이블 구축',
        '>>CONSEQUENCE: 옵트인·아웃 결과 역할. "your account may be limited", "data will be deleted" 등',
    ], 13)

    # ── 14. Step 4: 학습 데이터 ─────────────────────────────────────
    slide(c, 'Step 4: 학습 데이터 구성 (OPP-115 기반)', [
        '===기반 데이터셋: OPP-115 — 왜 이걸 선택했나',
        '115개 웹사이트 정책 / 12개 카테고리로 수동 주석된 공개 데이터셋 (ACL 2016)',
        '--공개 데이터셋 중 프라이버시 정책에 특화된 가장 광범위한 주석 코퍼스',
        '--12개 OPP-115 카테고리를 PolicyPulse의 6개 카테고리(SKIP/FPCU/TPSC/UCC/UAED/DR)로 재매핑',
        '-->>OPP-115: Online Privacy Policies 115개. 각 단락에 데이터 유형·목적 등 12개 카테고리로 태그됨',
        '',
        '===프레임 생성 및 주석 과정 — 4단계',
        '① OPP-115 10,717문장 → SRLBert로 48,783 프레임 생성',
        '--② 146개 관련 동사 기준 필터링 → 적합 프레임 추출 (관련 없는 동사 제거)',
        '--③ 최종 13,946개 프레임에 SKIP/FPCU/TPSC/UCC/UAED/DR 수동 주석',
        '--④ 독립 검증: 경력 5년+ 연구자 2명 별도 주석 → Cohen Kappa로 신뢰도 확인',
        '--주석 단계별 소요 시간: 약 6개월 (프라이버시 정책 주석 경력 3년+ 연구자 전담)',
        '>>Cohen Kappa: 주석자 간 일치도 측정 지수. 0=우연 수준 / 1=완전 일치. 0.6 이상이면 신뢰 가능',
        '',
        '===카테고리별 분포 — 불균형의 심각성',
        'SKIP 10,401 (74.5%) / FPCU 1,417 / TPSC 1,230 / UCC 556 / UAED 182 / DR 160',
        '--UAED 182건: 전체의 1.3% → 6-class 직접 분류 시 모델이 UAED 학습 거의 못 함',
        '--데이터 증강(textaugment): 동의어 치환·문맥 대체로 UAED·DR 샘플 인위적 확대',
        '>>textaugment: 파이썬 텍스트 증강 라이브러리. WordNet 동의어 대체, 문맥 기반 단어 삽입 지원',
        '',
        '===평가 방식 — 10-겹 교차 검증',
        '데이터를 10등분 → 9개로 학습, 1개로 테스트 → 10번 반복 → 평균 성능 보고',
        '--6 epoch 훈련 / 각 fold 내 검증 손실 최저 epoch 선택 (조기 종료 효과)',
        '>>과적합(Overfitting): 학습 데이터에만 성능 좋고 새 데이터에 약한 현상. 교차 검증으로 탐지 가능',
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
            '===핵심 수치 해석 — 왜 Two-Level이 압도적으로 좋은가',
            'UAED: 학습 데이터 182건 → Frame only에서 F1 0.15 (사실상 학습 실패)',
            '--FSC Augmented(증강): 0.15 → 0.84 (데이터 증강이 소수 클래스에 결정적)',
            '--FSC Two-Level: 0.84 → 0.92 (2단계 구조가 추가로 8% 향상)',
            '--Ensemble: 오히려 0.65로 하락 → 단순 앙상블은 불균형 문제 해결 못함',
            '',
            '===비교 관점 — 기존 도구와의 차이',
            'Polisis 전체 F1 (OPP-115 기준): ~0.77 → PolicyPulse 0.97로 크게 앞섬',
            '--하지만 단순 비교 주의: Polisis는 단락 분류, PolicyPulse는 프레임 분류 → 작업 범위 다름',
            '-->>Weighted Average: 각 클래스의 샘플 수에 비례해 가중 평균한 F1. SKIP이 많아서 높게 나올 수 있음',
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
        '===분석 규모 및 방법',
        '130,604개 웹사이트 → 사이트당 가장 최신 정책 1개 선택 = 129,856개 정책',
        '--총 39,702,767개 프레임 / 정책당 평균 305.7 프레임 / KEEP 평균 30개 (전체의 약 10%)',
        '--"완전성" 측정 기준: 특정 역할이 정책에 최소 1회 이상 등장하면 완전(1), 없으면 불완전(0)',
        '-->>PPCrawl 데이터: 130만+ 사이트 크롤링 → 최신 정책만 남기면 129,856개',
        '',
        '===핵심 역할 누락 비율 — 가장 충격적인 발견',
        '50%: UAED 프레임 0개 — 사용자 데이터 삭제·접근 권리를 정책에 한 줄도 안 씀',
        '--60%: USER_MECHANISM 미기재 — "어떻게 데이터 접근/삭제하나요?"를 설명 안 함',
        '--75%: CONSEQUENCE 미기재 — 옵트아웃 시 어떤 변화가 생기는지 설명 없음',
        '--40%: MECHANISM 없음 — 쿠키·SDK·픽셀 등 데이터 수집 방법 미기재',
        '--20%: USER_TRIGGER 미기재 — 데이터 수집 발생 시점·조건 미명시',
        '>>CONSEQUENCE: 옵트인·아웃 결과 역할. "data will be deleted", "service may be limited" 등',
        '',
        '===UAED 분포 분석 (Fig.2 bar chart 참조)',
        '전체 정책 50%: UAED 프레임 0개 → 삭제 관련 내용이 한 줄도 없음 (중위수 = 0)',
        '--90th percentile 기준: UAED 프레임 수 3개 이하 → 상위 10% 정책도 매우 적음',
        '--FPCU는 95%+ 정책에 등장 (데이터 수집 자체는 거의 다 언급) → 공개 의지는 있음',
        '--하지만 "사용자가 뭘 할 수 있는지"(UAED·UCC·CONSEQUENCE)는 무시되는 경향',
    ], 20)

    # ── 21. 대규모 분석 해석 ────────────────────────────────────────
    slide(c, '대규모 분석 해석 — 이게 왜 심각한 문제인가', [
        '===GDPR·CCPA가 보장하는 권리를 정책이 설명 안 함',
        'UAED = 접근·수정·삭제 권리 → GDPR Article 17 "삭제권(Right to be Forgotten)"',
        '--50% 사이트가 이 법적 권리를 정책에 명시조차 안 함 → 이 연구의 핵심 발견',
        '--USER_MECHANISM 60% 누락: 삭제권이 있다고 해도 어떻게 행사하는지를 안 알려줌',
        '--즉 "권리는 있는데 어떻게 쓰는지 모른다" 상태가 절반 이상 사이트의 현실',
        '-->>Right to be Forgotten: GDPR Article 17. 서비스에 자신의 개인 데이터 삭제를 요청 가능한 권리',
        '',
        '===CONSEQUENCE 75% 누락의 현실적 의미',
        '광고 수신 거부(옵트아웃) 버튼을 눌렀을 때 실제로 뭐가 달라지는지 안 알려줌',
        '--계정 기능 제한? 일부 데이터만 삭제? 완전 삭제? → 정책이 침묵',
        '--"동의"를 눌렀을 때도 마찬가지 — 서비스가 무엇을 하는지 결과를 안 씀',
        '>>CONSEQUENCE 역할: 옵트인·아웃 결과. "your access will be limited", "data will be deleted" 등',
        '',
        '===연구의 진짜 의의 — 정량적 증거',
        '"개인정보처리방침 읽기 어렵다"는 주관적 불만 → 수치로 "얼마나 빠져있나" 제시',
        '--129,856개 정책의 역할별 누락률을 자동 산출 → 인간이 직접 읽어야 알 수 있는 것을 자동화',
        '--규제 당국: 위반 후보 자동 선별 / 기업: 작성 시 체크리스트 / 연구자: 비교 분석',
        '--이 분야에서 이 정도 규모의 정량적 증거를 낸 연구가 이전에 없었다는 게 핵심 기여',
        '>>컴플라이언스 감사(Compliance Audit): 정책·법규 준수 여부를 체계적으로 점검하는 절차',
    ], 21, mode='interp')

    # ── 22. ChatGPT 비교 ─────────────────────────────────────────────
    slide(c, 'ChatGPT-3.5 vs PolicyPulse — 같은 정책 요약해보니', [
        '===실험 방법',
        '야후(Yahoo) 개인정보처리방침을 ChatGPT-3.5와 PolicyPulse 각각에 입력, 결과 비교',
        '--ChatGPT-3.5에게 "정책의 핵심 정보를 추출해달라" 프롬프트 제공',
        '-->>프롬프트(Prompt): LLM에 입력하는 지시문. 프롬프트 품질에 따라 결과 크게 달라짐',
        '',
        '===ChatGPT-3.5 결과의 구체적 문제',
        '제3자 데이터 공유(TPSC) 관련 내용을 요약에서 빠뜨림 → 누락(omission)',
        '--원문에 없는 구체적 광고 파트너 목록을 생성 → hallucination(환각) 발생',
        '--요약 문장이 자연스럽고 읽기 쉬워 오히려 신뢰하기 쉬운 게 더 위험할 수 있음',
        '-->>Hallucination(환각): LLM이 실제 없는 내용을 있는 것처럼 생성하는 현상. 신뢰성 문제의 핵심',
        '',
        '===PolicyPulse 결과 — 환각 없는 추출',
        '원문에 있는 프레임만 추출 → 없는 내용 생성 안 함 (결정론적 추출)',
        '--각 역할(DATA·MECHANISM·CONSEQUENCE·THIRD_PARTY_ENTITY 등) 단위로 분리',
        '--출력 형태가 구조화된 역할 목록 → 기계 처리와 검증이 용이',
        '--단점: GPT-4·Claude 등 최신 LLM과 비교 없음 / 자연어 설명 아님 (기술적 출력)',
        '',
        '===개인적 생각',
        'LLM 출력이 자연스러울수록 오히려 환각을 구별하기 어려움 → 법적 문서에서 치명적',
        '--PolicyPulse의 룰 기반 매핑은 느리고 어렵지만 "원문 근거" 보장이 핵심 강점',
    ], 22)

    # ── 23. 5가지 응용 분야 ─────────────────────────────────────────
    slide(c, '5가지 잠재적 응용 분야', [
        '===① 정책 완전성 검사 (Policy Completeness Checking)',
        '법적 필수 항목(GDPR의 USER_MECHANISM·UAED 등)이 정책에 포함됐는지 자동 체크',
        '--기업 법무팀이 정책 초안 작성 시 실시간 누락 항목 경고',
        '--규제 당국이 대규모 컴플라이언스 감사 시 수동 검토 없이 위반 후보 선별',
        '>>컴플라이언스(Compliance): 법·규정 등 준수 여부. 위반 시 GDPR은 전 세계 매출의 4% 벌금',
        '',
        '===② 짧은 공지(Short Notice) 자동 생성',
        '긴 정책에서 핵심 역할(DATA·MECHANISM·CONSEQUENCE 등)만 추출해 1페이지 요약본 자동 생성',
        '--EU·영국 ICO가 권장하는 "Layered Privacy Notice" 방식: 짧은 공지 + 전문 링크',
        '-->>Layered Privacy Notice: 정책을 짧은 요약층·상세층으로 나누는 구조. EU 권장 방식',
        '',
        '===③ 개인정보 영양 정보 라벨 (Privacy Nutrition Label)',
        '식품 성분표처럼 데이터 수집 항목·목적·기간을 표준 형식으로 제시',
        '--Carnegie Mellon 등에서 제안된 레이블 형식: PolicyPulse 추출 결과를 자동으로 채울 수 있음',
        '-->>Privacy Nutrition Label: 데이터 수집 내용을 아이콘·항목으로 시각화. CMU 연구팀 제안',
        '',
        '===④ 자동 질의응답 (Contextual Q&A System)',
        '"이 서비스가 내 위치 데이터를 광고사에 공유하나요?" → 원문 프레임 기반 자동 답변',
        '--환각 없이 원문 근거 답변 / 특정 역할(TPSC·MECHANISM) 검색으로 정확도 확보',
        '>>RAG(Retrieval-Augmented Generation): 외부 정보를 검색해 LLM 답변에 근거 추가하는 방식',
        '',
        '===⑤ 사용자 선호도 자동 대조 (Preference Matching)',
        '사용자가 설정한 프라이버시 선호(예: 마케팅 수신 거부)와 정책 CONSEQUENCE 역할 자동 비교',
        '--일치 여부 알림 시스템: "이 서비스는 옵트아웃 시 기능이 제한됩니다" 같은 경고 자동 생성',
    ], 23)

    # ── 24. Divider: Conclusion ──────────────────────────────────────
    divider(c, 'Conclusion', n=24)

    # ── 25. Conclusion ───────────────────────────────────────────────
    slide(c, 'Conclusion — 논문이 남긴 것', [
        '===핵심 기여 요약',
        'SRL + 2단계 XLNet → 단락 수준 분류에서 절(clause) 수준 세밀 추출로 발전',
        '--기존: "이 단락에 데이터 수집 내용이 있다" / 이제: "누가·무엇을·어떻게·언제"까지',
        '--Weighted avg F1 0.97 / 모든 카테고리 precision·recall 0.92 이상',
        '-->>절(Clause) 수준 분석: 문장 전체가 아닌 술어 중심 의미 단위(프레임)로 쪼개서 분석하는 방식',
        '',
        '===숫자로 보는 성과',
        '129,856개 정책 / 3,970만+ 프레임 / 16가지 역할 / 5가지 응용 분야',
        '--기존 SRL 기반 선행 연구(PurPliance)는 5개 정책 202문장 → 규모 차이가 이 논문의 강점',
        '--50%+ 정책에서 UAED 완전 누락 발견 → 규제 당국이 활용 가능한 정량적 증거 제공',
        '',
        '===보고 나서 든 생각 — 솔직한 감상',
        '"SRL이 개인정보처리방침에 잘 맞나?" 처음에 의구심이 있었는데,',
        '--PropBank의 ARG0·ARG1·ARGM 구조가 "누가·무엇을·어떻게"와 거의 1:1 대응이라 딱 맞았음',
        '--제일 인상적인 부분: UAED F1 0.15 → 0.92. 데이터 182건을 증강 + 2단계 구조로 극복',
        '--한계도 명확: 영어만 됨, 문장 간 연결 못함, GPT-4 비교 없음 → 후속 연구 여지 있음',
        '',
        '코드·데이터 공개: github.com/crisp-du/ppevo',
    ], 25)

    # ── 26. 한계점 ───────────────────────────────────────────────────
    slide(c, '한계점 & 향후 과제', [
        '===현재 한계 ① — 영어 전용',
        '영어 SRL 모델 + 영어 OPP-115 주석 데이터 기반 → 한국어·중국어 등 다국어 지원 불가',
        '--한국어 적용하려면: ① 한국어 SRL 모델(KLUE-SRL 등) ② 한국어 정책 주석 데이터 필요',
        '--한국 개인정보보호위원회 대상 컴플라이언스 체크에 활용하려면 반드시 해결해야 할 과제',
        '>>KLUE-SRL: Korean Language Understanding Evaluation. 한국어 NLP 벤치마크 데이터셋 모음',
        '',
        '===현재 한계 ② — 문장 내 분석만 가능',
        '문장 간 관계 파악 불가: "앞 문장에서 수집한 데이터를 이 문장에서 제3자와 공유한다" 연결 못 함',
        '--SRL 자체의 구조적 한계 → 담화 수준(discourse-level) 분석은 별도 연구 필요',
        '--실제 정책에서 "수집 → 사용 → 공유 → 보존" 흐름 파악을 위해선 이 한계 극복 필요',
        '>>담화 수준 분석(Discourse Analysis): 문장을 넘어 여러 문장·단락 간 의미 연결을 분석하는 NLP 작업',
        '',
        '===현재 한계 ③ — 최신 LLM 비교 없음',
        'GPT-3.5만 비교 → GPT-4·Claude 3·Gemini 등 2024~2025년 최신 모델과 차이가 불명확',
        '--최신 LLM은 환각이 크게 줄었다는 평가 → PolicyPulse의 "환각 없음" 강점이 얼마나 차별화되는지 미지수',
        '--저자도 "향후 연구 과제"로 명시 → 후속 비교 연구 기대됨',
        '',
        '===향후 연구 방향',
        '사용자 평가 연구 미수행: 생성된 짧은 공지·라벨이 실제로 이해하기 쉬운지 확인 안 됨',
        '--A/B 테스트나 실험 참가자 연구(user study) 통해 실용성 검증 필요',
        '--LLM 결합: PolicyPulse가 프레임 추출 → LLM이 자연어로 설명 생성하는 하이브리드 방식 유망',
        '>>User Study: 실제 사용자를 대상으로 인터페이스·정보 이해도 등을 측정하는 평가 실험',
    ], 26)

    # ── 27. Divider: Q&A ─────────────────────────────────────────────
    divider(c, 'Q & A', '예상 질문 & 답변', 27)

    # ── 28. Q&A 방법론 ───────────────────────────────────────────────
    slide(c, '예상 질문 & 답변 — 방법론 관련', [
        '===Q. SRL 모델을 fine-tuning 없이 써도 괜찮은가?',
        '프레임 추출(Step 1)은 PropBank 사전 학습 모델로 충분 → fine-tuning 불필요',
        '--"collect", "share", "disclose", "retain" 등 개인정보 동사가 PropBank에 이미 잘 정의됨',
        '--분류(Step 2) + 역할 매핑(Step 3)이 도메인 특화를 담당 → 파이프라인의 모듈 분리 설계 장점',
        '--단, PropBank에 없는 신조어 동사("anonymize", "pseudonymize" 등)는 커버 안 될 수 있음',
        '',
        '===Q. XLNet을 선택한 근거가 있나?',
        '논문 내 사전 실험(ablation study): BERT·SVM·Naive Bayes 대비 F1 전반적으로 우수',
        '--개인정보처리방침의 복잡한 조건절("when you use our service...")에서 차이 두드러짐',
        '--XLNet의 순열 기반 모델링이 조건·시간·방법 수식어가 많은 법적 텍스트에 적합',
        '-->>Ablation Study: 모델 구성 요소를 하나씩 제거해가며 각 요소의 기여도를 측정하는 실험',
        '',
        '===Q. 146개 동사 매핑은 어떻게 구축했나?',
        'OPP-115 학습 데이터에서 실제 등장한 동사들만 대상 → 전수 수동 분석',
        '--각 동사의 PropBank 프레임셋 참조 → 카테고리별 ARG 번호 → 역할 매핑 테이블 작성',
        '--완전 자동화가 아닌 수작업 → 신뢰성 높지만 새 동사 추가 시 테이블 수동 업데이트 필요',
        '',
        '===Q. 학습 데이터 주석 품질은 어떻게 보장했나?',
        '경력 3년+ 연구자 주석 / 경력 5년+ 연구자 2명 독립 검증 / 불일치 토론 합의',
        '--Cohen Kappa 계수 보고: 카테고리별 일치도 측정 → 주석의 객관성 확보 근거',
        '>>Inter-Annotator Agreement(IAA): 여러 주석자가 같은 데이터에 동일한 레이블을 얼마나 달았는지 측정',
    ], 28)

    # ── 29. Q&A 결과/활용 ───────────────────────────────────────────
    slide(c, '예상 질문 & 답변 — 결과 & 활용', [
        '===Q. F1 0.97인데 어떤 케이스에서 틀리나?',
        'DR·UAED 카테고리에서 상대적으로 낮음 (각 F1 0.92 → 전체 중 가장 낮음)',
        '--이유: 학습 데이터 부족 + Fig.3 공출현 분석상 UAED↔DR 공출현 높아 혼동 잦음',
        '--예: "We retain your data for 30 days after you delete your account" → UAED? DR? 둘 다?',
        '--False Positive 주로 발생: FPCU 문장을 TPSC로 오분류 (제3자 언급이 있는 경우)',
        '',
        '===Q. GPT-4·Claude와 비교하지 않은 이유?',
        '논문 제출 시점(2023~2024년 초)에 GPT-4 API 비용·접근성 제한이 있었을 가능성',
        '--저자도 "최신 LLM과의 비교는 향후 과제"로 명시 → 후속 연구에서 다뤄질 것',
        '--현실적 고려: GPT-4는 컨텍스트 길이 제한 → 30,000단어 정책을 통째로 넣기 어려움',
        '>>Prompt Chunking: 긴 문서를 LLM에 넣을 때 여러 청크로 나눠 처리하는 방식. 일관성 손실 위험 있음',
        '',
        '===Q. 한국어 개인정보처리방침에 적용 가능한가?',
        '현재는 불가 — 영어 SRL + 영어 OPP-115 주석만 사용',
        '--한국어 적용 경로: ① KLUE-SRL 기반 한국어 프레임 추출 ② 한국어 정책 주석 데이터 구축',
        '--한국 개인정보보호법·PIPA 대상 컴플라이언스 자동화에 활용 가능성 높음',
        '>>KLUE(Korean Language Understanding Evaluation): 한국어 NLP 벤치마크. SRL·NER·MRC 등 8가지 과제 포함',
        '',
        '===Q. 가장 충격적인 발견은?',
        '75%의 정책이 CONSEQUENCE 미기재 — 옵트아웃 결과가 뭔지 설명 자체를 안 하는 사이트',
        '--사용자가 "광고 수신 거부" 눌러도 실제로 뭐가 바뀌는지 정책이 침묵한다는 것',
        '--규제 강화로 정책이 길어졌는데 오히려 핵심 사용자 권리 설명은 줄어드는 역설',
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
