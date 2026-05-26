from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap

# 폰트 등록
pdfmetrics.registerFont(TTFont('Korean', '/Library/Fonts/Arial Unicode.ttf'))

W, H = landscape((1440, 810))  # 1440x810 (16:9)

NAVY   = colors.HexColor('#0A1F6B')
BLUE   = colors.HexColor('#1A3A9C')
LIGHT  = colors.HexColor('#E8EDF8')
WHITE  = colors.white
GRAY   = colors.HexColor('#555555')
ACCENT = colors.HexColor('#2E5CE6')

def draw_base(c, page_num, total):
    # 배경
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # 상단 바
    c.setFillColor(NAVY)
    c.rect(0, H - 60, W, 60, fill=1, stroke=0)

    # 하단 바
    c.setFillColor(NAVY)
    c.rect(0, 0, W, 40, fill=1, stroke=0)

    # 하단 텍스트
    c.setFillColor(WHITE)
    c.setFont('Korean', 11)
    c.drawString(30, 14, 'NDSS 2025 | PolicyPulse Paper Review')
    c.drawRightString(W - 30, 14, f'{page_num} / {total}')

def draw_title_slide(c):
    # 배경
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # 왼쪽 강조선
    c.setFillColor(ACCENT)
    c.rect(60, 200, 6, 330, fill=1, stroke=0)

    # 제목
    c.setFillColor(WHITE)
    c.setFont('Korean', 38)
    c.drawString(90, 480, 'PolicyPulse')

    c.setFont('Korean', 22)
    c.setFillColor(colors.HexColor('#A0B4F0'))
    c.drawString(90, 430, 'Precision Semantic Role Extraction for')
    c.drawString(90, 400, 'Enhanced Privacy Policy Comprehension')

    c.setFillColor(colors.HexColor('#CCCCCC'))
    c.setFont('Korean', 16)
    c.drawString(90, 340, 'Paper Review')

    # 구분선
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1)
    c.line(90, 310, 500, 310)

    # 저자 정보
    c.setFont('Korean', 14)
    c.setFillColor(colors.HexColor('#AAAAAA'))
    c.drawString(90, 280, 'Andrick Adhikari, Sanchari Das, Rinku Dewri  |  University of Denver')
    c.drawString(90, 255, 'NDSS 2025  |  Feb 2025, San Diego')

    # 오른쪽 하단 이름
    c.setFont('Korean', 13)
    c.setFillColor(colors.HexColor('#7799CC'))
    c.drawRightString(W - 60, 60, 'MK4MAX44')

def draw_section_divider(c, section_title):
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.rect(0, H//2 - 3, W, 6, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('Korean', 42)
    c.drawCentredString(W / 2, H / 2 + 30, section_title)

def draw_content_slide(c, title, bullets, page_num, total, note=None):
    draw_base(c, page_num, total)

    # 상단 제목 영역
    c.setFillColor(NAVY)
    c.rect(0, H - 60, W, 60, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Korean', 22)
    c.drawString(40, H - 42, title)

    # 좌측 강조선
    c.setFillColor(ACCENT)
    c.rect(30, 55, 4, H - 130, fill=1, stroke=0)

    y = H - 100
    for item in bullets:
        if item.startswith('##'):  # 소제목
            text = item[2:].strip()
            c.setFillColor(NAVY)
            c.setFont('Korean', 16)
            c.drawString(50, y, text)
            c.setFillColor(ACCENT)
            c.rect(50, y - 4, len(text) * 9, 2, fill=1, stroke=0)
            y -= 32
        elif item.startswith('--'):  # 들여쓴 항목
            text = item[2:].strip()
            c.setFillColor(GRAY)
            c.setFont('Korean', 13)
            lines = wrap_text(text, 95)
            for i, line in enumerate(lines):
                c.drawString(80, y - i * 20, '  ' + line)
            y -= len(lines) * 20 + 8
        elif item == '':
            y -= 14
        else:
            c.setFillColor(ACCENT)
            c.circle(58, y + 5, 4, fill=1, stroke=0)
            c.setFillColor(colors.HexColor('#222222'))
            c.setFont('Korean', 14)
            lines = wrap_text(item, 88)
            for i, line in enumerate(lines):
                c.drawString(72, y - i * 20, line)
            y -= len(lines) * 20 + 12

    if note:
        c.setFillColor(LIGHT)
        c.rect(30, 45, W - 60, 28, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.setFont('Korean', 11)
        c.drawString(40, 53, '📌 ' + note)

def draw_table_slide(c, title, headers, rows, page_num, total):
    draw_base(c, page_num, total)

    c.setFillColor(NAVY)
    c.rect(0, H - 60, W, 60, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Korean', 22)
    c.drawString(40, H - 42, title)

    col_w = [200, 480, 480]
    x_start = 40
    y_start = H - 90
    row_h = 68

    # 헤더
    x = x_start
    for i, (h, w) in enumerate(zip(headers, col_w)):
        c.setFillColor(NAVY)
        c.rect(x, y_start - row_h + 10, w - 4, row_h - 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Korean', 13)
        c.drawCentredString(x + w / 2, y_start - row_h / 2 + 12, h)
        x += w

    y = y_start - row_h
    for ri, row in enumerate(rows):
        x = x_start
        bg = LIGHT if ri % 2 == 0 else WHITE
        for ci, (cell, w) in enumerate(zip(row, col_w)):
            c.setFillColor(bg)
            c.rect(x, y - row_h + 10, w - 4, row_h - 4, fill=1, stroke=0)
            c.setFillColor(colors.HexColor('#222222') if ci > 0 else NAVY)
            c.setFont('Korean', 11)
            lines = wrap_text(cell, w // 9)
            for li, line in enumerate(lines):
                c.drawString(x + 8, y - 14 - li * 16, line)
            x += w
        y -= row_h

def wrap_text(text, max_chars):
    result = []
    while len(text) > max_chars:
        split = max_chars
        result.append(text[:split])
        text = text[split:]
    if text:
        result.append(text)
    return result

def make_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize=(W, H))
    total = 14

    # 1. 타이틀
    draw_title_slide(c)
    c.showPage()

    # 2. 목차
    draw_content_slide(c, '목차', [
        '논문을 고른 이유',
        '문제 정의',
        '핵심 아이디어',
        '방법론 / 시스템 설명',
        '평가 및 결과',
        '저자의 생각 vs 내 생각',
        '한계점',
        '느낀 점',
        '앞으로 해볼 것',
    ], 2, total)
    c.showPage()

    # 3. 논문 고른 이유
    draw_content_slide(c, '논문을 고른 이유', [
        '제목에 "Privacy Policy"가 있어서 눈에 띄었다',
        '앱 설치할 때 그냥 동의 누르는 그 문서가 자동으로 분석된다는 게 신기했다',
        'NLP(자연어처리)랑 프라이버시를 같이 다룬다는 게 보안 공부하면서 자연스럽게 연결됐다',
        '',
        '##NDSS란?',
        'Network and Distributed System Security Symposium',
        '네트워크·시스템 보안 분야 탑4 학회 중 하나',
    ], 3, total)
    c.showPage()

    # 4. 문제 정의
    draw_content_slide(c, '문제 정의', [
        '개인정보처리방침 — 아무도 안 읽는 중요한 문서',
        '--평균 70문장, 복잡한 법률 언어로 구성',
        '--법적 구속력이 있지만 사용자는 내용을 모르고 동의',
        '',
        '##기존 NLP 도구의 한계',
        '"이 정책에 제3자 공유 항목이 있냐 없냐" 수준의 분류에 그침',
        '단락 단위 분류 → 누가, 무슨 데이터를, 어떻게 수집하는지 알 수 없음',
        '특정 용도 하나에만 쓸 수 있어 범용성 부족',
    ], 4, total)
    c.showPage()

    # 5. 핵심 아이디어
    draw_content_slide(c, '핵심 아이디어', [
        '문장을 분류하는 데서 끝내지 말고, 의미 있는 정보를 세밀하게 추출하자',
        '',
        '##SRL (Semantic Role Labeling) 기반 접근',
        '"We may collect location information through cookies when you use our service"',
        '--수집 주체 (FIRST_PARTY): We',
        '--수집 데이터 (DATA): location information',
        '--수집 방법 (MECHANISM): through cookies',
        '--수집 조건 (USER_TRIGGER): when you use our service',
        '',
        '이걸 130만 개 정책에 자동으로 적용하는 게 PolicyPulse의 목표',
    ], 5, total)
    c.showPage()

    # 6. 방법론
    draw_content_slide(c, '방법론 / 시스템 설명', [
        '##1단계: 시맨틱 프레임 추출',
        'BERT 기반 SRL 모델로 문장을 행위자·행위·대상 역할로 분해',
        '',
        '##2단계: XLNet 2단계 분류기',
        '1단계: SKIP(무관) vs KEEP(관련) 분류',
        '2단계: FPCU / TPSC / UCC / UAED / DR 5가지 카테고리로 분류',
        '',
        '##3단계: 프라이버시 역할 매핑',
        '146개 동사에 대해 PropBank 인수 → 프라이버시 특화 역할로 변환',
        '훈련 데이터: OPP-115에서 뽑은 13,946개 프레임을 직접 손으로 주석',
    ], 6, total)
    c.showPage()

    # 7. 평가 및 결과
    draw_content_slide(c, '평가 및 결과', [
        '##분류 성능',
        'Weighted avg F1-score: 0.97',
        '1단계 (SKIP/KEEP): macro avg F1 0.96',
        '2단계 (카테고리): macro avg F1 0.98',
        '',
        '##대규모 적용',
        '130,604개 웹사이트, 1,071,488개 개인정보처리방침 분석',
        '3,970만 개 이상 시맨틱 프레임 처리',
        '평균 KEEP 프레임의 48%가 FPCU, 33%가 TPSC',
        '',
        '##ChatGPT-3.5 비교',
        'ChatGPT는 제3자 공유 내용을 빠뜨리거나 없는 내용을 생성하는 환각 발생',
        'PolicyPulse는 원문 기반 추출 → 환각 문제 없음',
    ], 7, total)
    c.showPage()

    # 8. 저자 vs 내 생각 (표)
    draw_table_slide(c, '저자의 생각 vs 내 생각',
        ['주제', '저자의 입장', '내 생각'],
        [
            ['기존 도구 문제', '단락 수준 분류라 세부 정보를 못 뽑는다', '맞는 말인데, 간단한 확인용으론 충분할 수도 있지 않나'],
            ['ChatGPT 비교', 'LLM은 개인정보처리방침 분석에 신뢰하기 어렵다', '동의하는데, 프롬프트를 잘 짜면 더 잘 될 수도 있지 않을까'],
            ['F1 0.97의 의미', '높은 성능으로 범용 플랫폼이 될 수 있다', '나머지 3% 오류가 실서비스에선 생각보다 문제될 수도 있다'],
            ['영어 전용 한계', '한계로 인정하고 미래 연구 과제로 남겼다', '한국어 지원 없으면 실용성이 많이 떨어진다'],
            ['13,946개 직접 주석', '수동 주석으로 높은 품질의 훈련 데이터 확보', '하나하나 읽고 역할 분류하는 게 진짜 노가다다'],
        ],
        8, total
    )
    c.showPage()

    # 9. 한계점
    draw_content_slide(c, '한계점', [
        '영어 전용 — 한국어 개인정보처리방침은 분석 불가',
        '',
        'DR(데이터 보존), UAED(사용자 접근) 카테고리 성능 상대적으로 낮음',
        '--학습 데이터 부족이 원인',
        '--데이터 증강(augmentation)으로 보완했지만 완전하진 않음',
        '',
        '문장 수준 분석만 가능 — 문장 간 관계 파악 불가',
        'ChatGPT와 비교는 했지만 GPT-4 같은 최신 LLM과 비교는 없음',
    ], 9, total)
    c.showPage()

    # 10. 느낀 점
    draw_content_slide(c, '느낀 점', [
        '처음에 NLP 논문이라 어렵겠다고 생각했는데, 문제의식 자체는 공감이 됐다',
        '개인정보처리방침 한 번도 제대로 안 읽어봤는데 — 내가 뭘 동의한 건지 모르고 썼다는 게 좀 무서웠다',
        '',
        '"있냐 없냐"에서 "누가, 어떤 데이터를, 어떻게, 어떤 조건에서"까지 — 이 차이가 사용자 입장에서 엄청 크다',
        '',
        'LLM이 프라이버시처럼 민감한 영역에서 아직 신뢰하기 어렵다는 것도 새로 알았다',
        '--틀린 내용을 그럴듯하게 뱉으면 실제 문제가 생길 수 있으니까',
        '--이런 특화 도구가 따로 필요하다는 게 이해됐다',
    ], 10, total)
    c.showPage()

    # 11. 앞으로 해볼 것
    draw_content_slide(c, '앞으로 해볼 것', [
        '##더 읽어볼 논문',
        'PoliGraph (Cui et al.) — NER 기반으로 비슷한 문제 다룬 연구',
        'PurPliance — SRL을 목적 절 분석에 먼저 적용한 연구',
        'Polisis — 기존 단락 수준 분류 대표 연구',
        '',
        '##다른 분야 적용 가능성',
        '이용약관, 금융상품 설명서, 보험 약관 — "아무도 안 읽는 중요한 문서"들',
        '"이 서비스는 사용자 데이터를 팔 수 있다" 같은 내용 자동 추출',
        '',
        '##프로젝트 아이디어',
        'KoBERT 기반 한국어 개인정보처리방침 분석기',
        '앱 설치 시 자동 요약 보여주는 브라우저 확장',
    ], 11, total)
    c.showPage()

    # 12. 마무리
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    c.setFillColor(ACCENT)
    c.rect(0, H//2 - 3, W, 6, fill=1, stroke=0)

    c.setFillColor(WHITE)
    c.setFont('Korean', 36)
    c.drawCentredString(W / 2, H / 2 + 60, 'Thank You')

    c.setFont('Korean', 16)
    c.setFillColor(colors.HexColor('#AAAAAA'))
    c.drawCentredString(W / 2, H / 2 + 10, 'PolicyPulse: Precision Semantic Role Extraction for Enhanced Privacy Policy Comprehension')
    c.drawCentredString(W / 2, H / 2 - 20, 'NDSS 2025  |  Adhikari, Das, Dewri')

    c.setFont('Korean', 13)
    c.setFillColor(colors.HexColor('#7799CC'))
    c.drawCentredString(W / 2, 60, 'MK4MAX44')

    c.showPage()
    c.save()
    print(f'PDF 생성 완료: {output_path}')

make_pdf('/Users/jeondonghyeog/Desktop/PaperReview_PolicyPulse.pdf')
