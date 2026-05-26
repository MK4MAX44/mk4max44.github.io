from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

pdfmetrics.registerFont(TTFont('Korean', '/Library/Fonts/Arial Unicode.ttf'))

# ── 색상 팔레트 ──────────────────────────────
NAVY   = colors.HexColor('#0A1F6B')
BLUE   = colors.HexColor('#1A3A9C')
ACCENT = colors.HexColor('#2E5CE6')
LIGHT  = colors.HexColor('#E8EDF8')
MINT   = colors.HexColor('#E6F4F1')
MINT_D = colors.HexColor('#1A7A6A')
WHITE  = colors.white
GRAY   = colors.HexColor('#555555')
LGRAY  = colors.HexColor('#AAAAAA')

W, H = landscape((1440, 810))  # 발표자료 크기

# ══════════════════════════════════════════════
#  발표자료 PDF 헬퍼
# ══════════════════════════════════════════════

def base(c, n, total):
    c.setFillColor(WHITE); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(NAVY);  c.rect(0,H-60,W,60,fill=1,stroke=0)
    c.setFillColor(NAVY);  c.rect(0,0,W,40,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('Korean',11)
    c.drawString(30,14,'NDSS 2025 | PolicyPulse Paper Review')
    c.drawRightString(W-30,14,f'{n} / {total}')

def title_slide(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(ACCENT); c.rect(60,200,6,330,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('Korean',38); c.drawString(90,490,'PolicyPulse')
    c.setFont('Korean',20); c.setFillColor(colors.HexColor('#A0B4F0'))
    c.drawString(90,440,'Precision Semantic Role Extraction for Enhanced Privacy Policy Comprehension')
    c.setFont('Korean',16); c.setFillColor(colors.HexColor('#CCCCCC'))
    c.drawString(90,390,'논문 리뷰 발표자료')
    c.setStrokeColor(ACCENT); c.setLineWidth(1); c.line(90,360,500,360)
    c.setFont('Korean',13); c.setFillColor(colors.HexColor('#AAAAAA'))
    c.drawString(90,330,'Andrick Adhikari, Sanchari Das, Rinku Dewri  |  University of Denver')
    c.drawString(90,305,'NDSS 2025  |  Feb 2025, San Diego')
    c.setFont('Korean',13); c.setFillColor(colors.HexColor('#7799CC'))
    c.drawRightString(W-60,60,'MK4MAX44')

def content_slide(c, title, items, n, total):
    base(c, n, total)
    c.setFillColor(WHITE); c.setFont('Korean',22); c.drawString(40,H-42,title)
    c.setFillColor(ACCENT); c.rect(30,55,4,H-130,fill=1,stroke=0)
    y = H-100
    for item in items:
        if item.startswith('##'):
            txt = item[2:].strip()
            c.setFillColor(NAVY); c.setFont('Korean',15); c.drawString(50,y,txt)
            c.setFillColor(ACCENT); c.rect(50,y-5,min(len(txt)*8,W-100),2,fill=1,stroke=0)
            y -= 30
        elif item.startswith('--'):
            txt = item[2:].strip()
            c.setFillColor(GRAY); c.setFont('Korean',12)
            lines = wrap(txt, 100)
            for i,l in enumerate(lines): c.drawString(80,y-i*18,l)
            y -= len(lines)*18+6
        elif item == '':
            y -= 12
        else:
            c.setFillColor(ACCENT); c.circle(58,y+5,4,fill=1,stroke=0)
            c.setFillColor(colors.HexColor('#111111')); c.setFont('Korean',13)
            lines = wrap(item, 92)
            for i,l in enumerate(lines): c.drawString(72,y-i*18,l)
            y -= len(lines)*18+10

def interp_slide(c, title, items, n, total):
    """해설 슬라이드 - 민트 계열 배경"""
    c.setFillColor(MINT); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(MINT_D); c.rect(0,H-60,W,60,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('Korean',22); c.drawString(40,H-42,'💡 '+title)
    c.setFillColor(MINT_D); c.rect(0,0,W,40,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('Korean',11)
    c.drawString(30,14,'해설 슬라이드')
    c.drawRightString(W-30,14,f'{n} / {total}')
    c.setFillColor(MINT_D); c.rect(30,55,4,H-130,fill=1,stroke=0)
    y = H-100
    for item in items:
        if item.startswith('##'):
            txt = item[2:].strip()
            c.setFillColor(MINT_D); c.setFont('Korean',15); c.drawString(50,y,txt)
            y -= 30
        elif item.startswith('--'):
            txt = item[2:].strip()
            c.setFillColor(colors.HexColor('#335533')); c.setFont('Korean',12)
            lines = wrap(txt, 100)
            for i,l in enumerate(lines): c.drawString(80,y-i*18,l)
            y -= len(lines)*18+6
        elif item == '':
            y -= 12
        else:
            c.setFillColor(MINT_D); c.circle(58,y+5,4,fill=1,stroke=0)
            c.setFillColor(colors.HexColor('#223322')); c.setFont('Korean',13)
            lines = wrap(item, 92)
            for i,l in enumerate(lines): c.drawString(72,y-i*18,l)
            y -= len(lines)*18+10

def table_slide(c, title, headers, rows, n, total):
    base(c, n, total)
    c.setFillColor(WHITE); c.setFont('Korean',22); c.drawString(40,H-42,title)
    col_w = [200,470,470]
    xs, y0, rh = 40, H-90, 65
    x = xs
    for h,w in zip(headers,col_w):
        c.setFillColor(NAVY); c.rect(x,y0-rh+8,w-4,rh-4,fill=1,stroke=0)
        c.setFillColor(WHITE); c.setFont('Korean',12)
        c.drawCentredString(x+w/2, y0-rh/2+10, h)
        x += w
    y = y0-rh
    for ri,row in enumerate(rows):
        x = xs; bg = LIGHT if ri%2==0 else WHITE
        for ci,(cell,w) in enumerate(zip(row,col_w)):
            c.setFillColor(bg); c.rect(x,y-rh+8,w-4,rh-4,fill=1,stroke=0)
            c.setFillColor(NAVY if ci==0 else colors.HexColor('#111111'))
            c.setFont('Korean',10)
            for li,line in enumerate(wrap(cell, w//8)):
                c.drawString(x+6, y-14-li*14, line)
            x += w
        y -= rh

def end_slide(c):
    c.setFillColor(NAVY); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(ACCENT); c.rect(0,H//2-3,W,6,fill=1,stroke=0)
    c.setFillColor(WHITE); c.setFont('Korean',40); c.drawCentredString(W/2,H/2+60,'Thank You')
    c.setFont('Korean',15); c.setFillColor(colors.HexColor('#AAAAAA'))
    c.drawCentredString(W/2,H/2+10,'PolicyPulse: Precision Semantic Role Extraction for Enhanced Privacy Policy Comprehension')
    c.drawCentredString(W/2,H/2-20,'NDSS 2025  |  Adhikari, Das, Dewri  |  github.com/crisp-du/ppevo')
    c.setFont('Korean',13); c.setFillColor(colors.HexColor('#7799CC'))
    c.drawCentredString(W/2,60,'MK4MAX44')

def wrap(text, n):
    r=[]
    while len(text)>n: r.append(text[:n]); text=text[n:]
    if text: r.append(text)
    return r or ['']

# ══════════════════════════════════════════════
#  발표자료 PDF 생성
# ══════════════════════════════════════════════

def make_slides(path):
    c = canvas.Canvas(path, pagesize=(W,H))
    T = 22  # 총 슬라이드 수

    # 1. 타이틀
    title_slide(c); c.showPage()

    # 2. 목차
    content_slide(c,'목차',[
        '논문 선택 이유','문제 정의','핵심 아이디어',
        '방법론 1 — SRL','방법론 2 — 프레임 분류','방법론 3 — 역할 매핑',
        '실험 결과','실제 정책 분석','저자 vs 내 생각','한계점','앞으로 해볼 것',
    ],2,T); c.showPage()

    # 3. 논문 선택 이유
    content_slide(c,'논문을 고른 이유',[
        '제목에 "Privacy Policy"가 있어서 눈에 띄었다',
        '앱 설치할 때 그냥 동의 누르는 그 문서 — 자동 분석이 된다는 게 신기했다',
        'NLP(자연어처리)랑 프라이버시를 같이 다룬다는 게 보안 공부랑 자연스럽게 연결됐다',
        '','##학회: NDSS 2025',
        'Network and Distributed System Security Symposium',
        '네트워크·시스템 보안 분야 탑4 학회 중 하나',
    ],3,T); c.showPage()

    # 4. 문제 정의
    content_slide(c,'문제 정의',[
        '개인정보처리방침 — 아무도 안 읽는 중요한 문서',
        '--평균 70문장, 복잡한 법률 언어. 읽어도 무슨 말인지 모른다',
        '--법적으로 구속력 있는 문서인데 사용자는 내용을 모르고 동의한다',
        '','##기존 NLP 도구의 한계',
        '"이 정책에 제3자 공유 항목이 있냐 없냐" 수준에 그침',
        '단락 단위 분류 → 누가·무엇을·어떻게 수집하는지 알 수 없음',
        '특정 태스크 하나에만 특화 → 다른 용도로 재사용 불가',
    ],4,T); c.showPage()

    # 5. 해설 — 문제 정의
    interp_slide(c,'문제 정의 해설',[
        '쉽게 말하면: 개인정보처리방침은 읽기 불편하게 만들어져 있다',
        '기존 도구들은 "카테고리가 있냐 없냐"는 알려줬지만 "뭘"은 몰랐다',
        '','##왜 이게 문제인가?',
        '"제3자에게 데이터 공유함"이라고 나오는데, 어떤 데이터를 누구한테 왜 공유하는지는?',
        '단락 수준 분류로는 그 안의 세부 내용이 그냥 뭉개진다',
        '','##연구자들이 채우려 한 간극',
        '분류(Classification)에서 → 세밀한 정보 추출(Extraction)로',
    ],5,T); c.showPage()

    # 6. 핵심 아이디어
    content_slide(c,'핵심 아이디어 — SRL 기반 접근',[
        '문장을 분류하는 데서 끝내지 말고, 의미 있는 정보를 세밀하게 뽑아내자',
        '','##예시 문장 분해',
        '"We may collect location information through cookies when you use our service"',
        '--수집 주체(FIRST_PARTY): We',
        '--수집 데이터(DATA): location information',
        '--수집 방법(MECHANISM): through cookies',
        '--수집 조건(USER_TRIGGER): when you use our service',
        '','이걸 130만 개 정책에 자동으로 적용하겠다는 게 PolicyPulse의 목표',
    ],6,T); c.showPage()

    # 7. 해설 — 핵심 아이디어
    interp_slide(c,'핵심 아이디어 해설',[
        'SRL이란? 문장에서 "누가-무엇을-왜-어떻게" 했는지 역할별로 분리하는 기술',
        '영어 수업에서 5W1H 찾기랑 비슷한 개념인데 이걸 자동으로 한다',
        '','##기존 방식과의 차이',
        '기존: "이 문단은 데이터 수집 관련입니다" (단락 → 라벨)',
        'PolicyPulse: "We가 location information을 cookies로 수집합니다" (문장 → 세부 정보)',
        '','##왜 이게 중요하냐면',
        '사용자 입장에서 "수집함"과 "GPS 데이터를 쿠키로 수집함"은 완전히 다른 정보다',
    ],7,T); c.showPage()

    # 8. 방법론 1 — SRL
    content_slide(c,'방법론 1 — 시맨틱 프레임 추출',[
        'BERT 기반 SRLBert 모델 (AllenNLP 플랫폼 제공 모델 사용)',
        '문장 → 동사(predicate) 중심으로 행위자·행위·대상 역할 분리',
        '','##하나의 문장에서 여러 프레임이 추출됨',
        '문장 하나 평균 4개 프레임 생성 (정책 전체 평균 306개 프레임)',
        '그 중 실제 관련 있는 KEEP 프레임은 평균 30개 — 전체의 약 10%',
        '','##SKIP 프레임 72.6%의 의미',
        '개인정보처리방침의 70% 이상은 핵심 정보가 아니다',
        '사용자한테 중요한 내용은 극히 일부에 집중되어 있다',
    ],8,T); c.showPage()

    # 9. 방법론 2 — 프레임 분류
    content_slide(c,'방법론 2 — XLNet 2단계 분류기',[
        '##1단계: SKIP vs KEEP',
        '개인정보와 관련 없는 프레임 걸러내기',
        '','##2단계: 5가지 카테고리 분류',
        '--FPCU: 데이터 수집·사용 (First Party Collection/Use)',
        '--TPSC: 제3자 공유 (Third Party Sharing/Collection)',
        '--UCC: 사용자 선택권 — 옵트인/옵트아웃 (User Choice/Control)',
        '--UAED: 사용자 데이터 접근·수정·삭제 (User Access, Edit, Delete)',
        '--DR: 데이터 보존 기간 (Data Retention)',
        '','훈련 데이터: OPP-115에서 추출한 13,946개 프레임을 직접 손으로 주석',
        '주석자: 경력 3년+ 연구자, 5년+ 2명이 검증',
    ],9,T); c.showPage()

    # 10. 해설 — 분류기
    interp_slide(c,'분류기 해설',[
        '왜 2단계로 나눴을까?',
        '처음엔 한 모델로 다 하려 했는데, SKIP이 압도적으로 많아서 성능이 안 나왔다',
        'SKIP/KEEP을 먼저 나누고 나서 카테고리 분류를 하니 성능이 크게 올랐다',
        '','##왜 XLNet을 썼나?',
        '사전 실험에서 BERT 기반 모델보다 프레임 분류에서 성능이 좋았다',
        '(BERT가 더 유명하지만 이 태스크에서는 XLNet이 더 잘 맞았다)',
        '','##13,946개 직접 주석이 얼마나 힘든 건가',
        '하나하나 읽고 "이게 FPCU인지 TPSC인지 SKIP인지" 판단해야 한다',
        '3년 경력자가 달고 5년 이상 두 명이 따로 검증 — 진짜 노가다',
    ],10,T); c.showPage()

    # 11. 방법론 3 — 역할 매핑
    content_slide(c,'방법론 3 — 프라이버시 역할 매핑',[
        '146개 동사에 대해 PropBank 인수 → 프라이버시 전용 역할로 변환',
        '','##예시: collect 동사 (FPCU 카테고리)',
        '--ARG0 (행위 주체) → FIRST_PARTY_ENTITY',
        '--ARG1 (행위 대상) → DATA',
        '--ARGM-MNR (방법)  → MECHANISM',
        '--ARGM-TMP (시점)  → USER_TRIGGER',
        '','##추출되는 16가지 프라이버시 역할',
        'DATA / FIRST_PARTY_ENTITY / THIRD_PARTY_ENTITY / MECHANISM / PURPOSE',
        'SHARING_TERMS / USER_TRIGGER / OPT_IN / OPT_OUT / CONSEQUENCE 등',
    ],11,T); c.showPage()

    # 12. 실험 결과
    content_slide(c,'평가 및 결과',[
        '##분류 성능 (Weighted avg F1-score)',
        '전체: 0.97  |  1단계(SKIP/KEEP): 0.96  |  2단계(카테고리): 0.98',
        '','##대규모 적용 결과',
        '130,604개 웹사이트, 1,071,488개 정책, 3,970만+ 프레임 처리',
        '','##실제 정책 분석에서 나온 충격적인 수치',
        '--90% 정책: 사용자 데이터 삭제 방법(USER_MECHANISM) 미기재',
        '--75% 정책: 옵트인/아웃 결과(CONSEQUENCE) 미기재',
        '--40% 정책: 데이터 수집 방법(MECHANISM) 미기재',
        '--50% 정책: UAED 프레임 자체가 아예 없음',
        '','##ChatGPT-3.5 비교',
        'ChatGPT: 제3자 공유 빠뜨리거나 환각(없는 내용 생성) 발생',
        'PolicyPulse: 원문 기반 추출 → 환각 없음',
    ],12,T); c.showPage()

    # 13. 해설 — 결과
    interp_slide(c,'결과 해설',[
        '"90%의 정책이 데이터 삭제 방법을 안 알려준다"는 게 무슨 말이냐면',
        'GDPR이나 개인정보보호법에 "사용자는 자기 데이터 삭제 요청할 수 있다"고 돼 있는데',
        '그 방법을 실제 정책에서 90%가 명시 안 한다는 거다 — 법적으로 문제가 될 수 있다',
        '','##SKIP 프레임 72.6%의 실제 의미',
        '정책 문서의 30페이지 중 3페이지만 진짜 중요한 내용이다',
        'PolicyPulse는 그 3페이지 분량만 정확하게 뽑아낼 수 있다',
        '','##ChatGPT 비교에서 배운 것',
        'LLM은 "그럴듯한 요약"을 만드는 데 특화 → 정확성 보장 안 됨',
        '프라이버시처럼 민감한 영역에서는 이 차이가 매우 크다',
    ],13,T); c.showPage()

    # 14. 저자 vs 내 생각 (표)
    table_slide(c,'저자의 생각 vs 내 생각',
        ['주제','저자의 입장','내 생각'],
        [
            ['기존 도구 한계','단락 수준 분류라 세부 정보를 못 뽑는다','맞는 말인데, 간단한 있냐없냐 확인용으론 충분할 수도 있지 않나'],
            ['ChatGPT 비교','LLM은 신뢰하기 어렵다','동의. 프롬프트 잘 짜면 더 잘 될 수도 있지 않을까 싶지만, 논문에서 이미 테스트해서 여전히 틀렸다고 함'],
            ['F1 0.97','높은 성능으로 범용 플랫폼 가능','3%에서 틀리는 케이스가 실서비스에선 생각보다 클 수 있다'],
            ['영어 전용','한계로 인정, 미래 과제','한국어 지원 없으면 실용성이 많이 떨어진다'],
            ['13,946개 직접 주석','수동 주석으로 고품질 데이터 확보','하나하나 읽고 역할 분류해야 하는 거라 진짜 노가다다'],
        ],
        14,T); c.showPage()

    # 15. 한계점
    content_slide(c,'한계점',[
        '영어 전용 — 한국어 등 다른 언어 정책은 분석 불가',
        '','DR / UAED 카테고리 성능 상대적으로 낮음',
        '--학습 데이터 수가 다른 카테고리보다 적음 (DR: 160개, UAED: 182개)',
        '--데이터 증강으로 보완했지만 완전하지 않음',
        '','문장 간 관계 파악 불가 — 문장 수준 분석에 한정',
        'ChatGPT-4 같은 최신 LLM과의 비교 없음',
        '생성된 요약(Short Notice, Nutrition Label)에 대한 사용자 평가 없음',
    ],15,T); c.showPage()

    # 16. 앞으로 해볼 것
    content_slide(c,'앞으로 해볼 것',[
        '##더 읽어볼 논문',
        'PoliGraph (Cui et al.) — NER 기반 유사 연구, PolicyPulse가 직접 비교한 논문',
        'PurPliance — SRL을 프라이버시 목적 절 분석에 먼저 적용',
        'Polisis — 기존 단락 수준 분류 대표 연구',
        '','##다른 분야 적용 가능성',
        '이용약관, 금융상품 설명서, 보험 약관 — "아무도 안 읽는 중요한 문서"들',
        '','##프로젝트 아이디어',
        'KoBERT 기반 한국어 개인정보처리방침 분석기',
        '앱 설치 시 자동 요약 보여주는 브라우저 확장',
    ],16,T); c.showPage()

    # 17. 마무리
    end_slide(c); c.showPage()
    c.save()
    print(f'✅ 발표자료 저장: {path}')


# ══════════════════════════════════════════════
#  한국어 논문 번역 PDF 생성
# ══════════════════════════════════════════════

def make_korean_paper(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=22*mm, bottomMargin=22*mm)

    styles = getSampleStyleSheet()
    def sty(name, font, size, leading, space_before=4, space_after=4, align=TA_JUSTIFY, color=colors.black, bold=False):
        return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading,
            spaceBefore=space_before, spaceAfter=space_after, alignment=align, textColor=color)

    KR       = sty('KR',      'Korean', 10, 16)
    KR_J     = sty('KR_J',    'Korean', 10, 17, align=TA_JUSTIFY)
    H1       = sty('H1',      'Korean', 18, 24, 14, 6, TA_CENTER, NAVY)
    H2       = sty('H2',      'Korean', 13, 18, 12, 4, TA_LEFT,   NAVY)
    H3       = sty('H3',      'Korean', 11, 16,  8, 3, TA_LEFT,   BLUE)
    AUTHOR   = sty('AUTHOR',  'Korean', 10, 14,  2, 2, TA_CENTER, GRAY)
    ABSTRACT = sty('ABSTRACT','Korean',  9, 15,  6, 6, TA_JUSTIFY, colors.HexColor('#333333'))
    CAPTION  = sty('CAPTION', 'Korean',  8, 12,  4, 8, TA_CENTER, GRAY)
    SMALL    = sty('SMALL',   'Korean',  8, 12,  2, 2)

    def hr(): return Table([['']],colWidths=[170*mm],
        style=TableStyle([('LINEABOVE',(0,0),(0,0),0.5,NAVY),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))

    def box(text, bg=LIGHT, fc=NAVY):
        return Table([[Paragraph(text, sty('box','Korean',9,14,align=TA_JUSTIFY))]],
            colWidths=[170*mm],
            style=TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('LEFTPADDING',(0,0),(-1,-1),8),
                ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
                ('BOX',(0,0),(-1,-1),0.5,fc)]))

    story = []

    # ── 제목 페이지 ─────────────────────────
    story += [
        Spacer(1, 10*mm),
        Paragraph('PolicyPulse', H1),
        Paragraph('개인정보처리방침 이해를 위한 정밀 의미역 추출', sty('sub','Korean',13,18,4,4,TA_CENTER,BLUE)),
        Spacer(1, 4*mm), hr(), Spacer(1, 3*mm),
        Paragraph('Andrick Adhikari · Sanchari Das · Rinku Dewri', AUTHOR),
        Paragraph('University of Denver', AUTHOR),
        Paragraph('andrick.adhikari@du.edu · sanchari.das@du.edu · rinku.dewri@du.edu', AUTHOR),
        Spacer(1, 2*mm),
        Paragraph('Network and Distributed System Security (NDSS) Symposium 2025', AUTHOR),
        Paragraph('2025년 2월 24-28일, 샌디에이고, 미국', AUTHOR),
        Spacer(1, 5*mm), hr(), Spacer(1, 4*mm),
    ]

    # ── 초록 ────────────────────────────────
    story.append(Paragraph('초록', H2))
    story.append(box(
        '자연어 개인정보처리방침의 효과는 가독성·모호성·접근성 문제로 인해 계속해서 제한받고 있다. '
        '여러 대안적 설계가 제안되었음에도 불구하고, 자연어 정책은 여전히 조직이 사용자에게 개인정보 처리 방식을 '
        '전달하는 주요 형식으로 사용되고 있다. 현재 NLP 기법들은 대개 고수준 개요 생성에 집중하거나, '
        '소비자 프라이버시 커뮤니케이션의 단일 측면에만 특화되어 있어 다양한 태스크에 유연하게 적용하기 어렵다. '
        '이를 해결하기 위해 본 논문은 PolicyPulse를 제안한다. PolicyPulse는 개인정보처리방침을 '
        '활용 가능한 형식으로 처리하는 정보 추출 파이프라인이다. '
        'PolicyPulse는 특화된 XLNet 분류기를 활용하고 BERT 기반 모델을 의미역 레이블링에 적용하여, '
        '술어와 인수 사이의 의미 관계를 유지하면서 정책 문장에서 구절을 추출한다. '
        '분류 모델은 13,946개의 수동 주석 의미 프레임으로 훈련되었으며, '
        '문장 내 절을 통해 전달되는 개인정보 처리 방식 식별에서 F1-점수 0.97을 달성했다. '
        '요구사항 기반 정책 표시, 질의응답 시스템, 개인정보 선호도 확인을 지원하는 '
        '프로토타입 응용 프로그램을 통해 PolicyPulse의 범용성을 입증한다.'
    ))
    story.append(Spacer(1,4*mm))

    # ── 1. 서론 ─────────────────────────────
    story.append(Paragraph('1. 서론', H2))
    story.append(Paragraph(
        '개인정보처리방침은 조직이 사용자 정보에 접근하고 활용하는 방식을 전달하며 관련 규정 준수를 보장하는 법적 문서이다. '
        '그러나 현재의 개인정보처리방침은 길고 복잡하며 모호하여 사용자가 효과적으로 활용하기 어렵다는 여러 문제에 직면해 있다. '
        '주요 장애물로는 가독성, 모호성, 접근성 문제가 있다.', KR_J))
    story.append(Paragraph(
        '이를 해결하기 위해 자연어 정책의 문제를 완화하는 NLP 기법들이 연구되어 왔다. '
        'NLP는 정보 추출, 내용 요약, 자동 질의응답, 텍스트 분류 등 다양한 분야에서 활용되고 있다. '
        '그러나 기존 접근법은 단락 수준 분류에 집중하거나 특정 태스크에만 특화되어 있어 '
        '여러 태스크에 유연하게 적용하기 어렵다는 한계가 있다. '
        '본 논문은 이 간극을 채우고자 PolicyPulse를 제안한다.', KR_J))
    story.append(Spacer(1,3*mm))

    story.append(Paragraph('주요 기여', H3))
    contrib_data = [
        ['기여 1', 'PolicyPulse 제안 — 의미 프레임을 이용한 영어 개인정보처리방침 맥락화. 정보 분류에서 F1-점수 0.97 달성'],
        ['기여 2', '정책 완전성 검사, 대안 표시(짧은 공지, 영양 정보 라벨), 자동 질의응답, 사용자 선호도 확인 등 다양한 응용 가능성 입증'],
        ['기여 3', 'OPP-115 코퍼스에서 추출한 13,946개 의미 프레임을 수동 주석하여 129,856개 정책의 프레임 수준 분류 데이터 제공'],
        ['기여 4', '개인정보처리방침에서 자주 사용되는 146개 동사에 대해 PropBank 인수를 프라이버시 특화 역할로 매핑'],
    ]
    story.append(Table(contrib_data, colWidths=[20*mm,150*mm],
        style=TableStyle([
            ('BACKGROUND',(0,0),(0,-1),LIGHT),('FONTNAME',(0,0),(-1,-1),'Korean'),
            ('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),
            ('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('TEXTCOLOR',(0,0),(0,-1),NAVY),
        ])))
    story.append(Spacer(1,4*mm))

    # ── 2. 배경 ─────────────────────────────
    story.append(Paragraph('2. 배경 및 PolicyPulse의 위치', H2))
    story.append(Paragraph(
        '개인정보처리방침은 가독성, 모호성, 접근성 측면에서 심각한 문제를 안고 있다. '
        '이를 해결하기 위한 NLP 기반 접근법들은 크게 두 가지로 나뉜다.', KR_J))

    bg_data = [
        ['분류 (Classification)', '단락 또는 문장이 어떤 개인정보 범주에 속하는지 식별. 예: Polisis는 단락 수준에서 데이터 수집, 제3자 공유 등의 카테고리로 분류함'],
        ['정보 추출 (IE)', '특정 엔티티(데이터 유형, 수집 주체, 목적 등)를 추출. 예: PolicyLint, PoliCheck는 데이터 유형과 엔티티를 연결하고 모순을 탐지함'],
        ['의미역 분석 (SRL)', '문장 내 술어에 대해 행위자·행위·대상 등 의미 역할을 레이블링. 기존 연구(Bhatia et al.)는 소규모로 수작업 코딩을 했지만 자동화는 부족했음'],
    ]
    story.append(Table(bg_data, colWidths=[40*mm,130*mm],
        style=TableStyle([
            ('BACKGROUND',(0,0),(0,-1),LIGHT),('FONTNAME',(0,0),(-1,-1),'Korean'),
            ('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),
            ('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('TEXTCOLOR',(0,0),(0,-1),NAVY),
        ])))
    story.append(Spacer(1,3*mm))
    story.append(Paragraph(
        'PolicyPulse는 자동화된 분류와 트랜스포머 기반 의미 정보 추출을 결합한다. '
        '문장 수준이 아닌 세밀한 절(clause) 수준에서 정책을 분해하고, '
        '프라이버시 관련 구성 요소에 의미 역할을 부여하면서 술어-인수 간 의미 관계를 보존한다.', KR_J))
    story.append(Spacer(1,4*mm))

    # ── 3. 방법론 ────────────────────────────
    story.append(Paragraph('3. 프라이버시 역할 추출 방법론', H2))
    story.append(Paragraph('PolicyPulse는 세 단계로 구성된다.', KR))
    story.append(Spacer(1,2*mm))

    story.append(Paragraph('3.1 의미역 레이블링 (SRL)', H3))
    story.append(Paragraph(
        'SRL은 문장 내 각 단어가 특정 술어에 대해 어떤 역할을 하는지 식별하는 NLP 태스크이다. '
        'PolicyPulse는 AllenNLP 플랫폼의 SRLBert 모델을 사용한다. '
        'SRLBert는 BERT 아키텍처를 활용하며, 영어 PropBank 코퍼스의 SRL 주석(약 50,000개 술어, 1,118개 동사)을 기반으로 훈련되었다. '
        '하나의 정책 문장에서 평균 4개의 의미 프레임이 추출되며, 정책 전체로는 평균 306개의 프레임이 생성된다.', KR_J))
    story.append(box(
        '예시: "We may collect location information through cookies when you use our service"\n\n'
        '→ 프레임 1: [ARG0: We] [V: collect] [ARG1: location information] [ARGM-MNR: through cookies] [ARGM-TMP: when you use our service]\n'
        '→ 프레임 2: [ARG0: you] [V: use] [ARG1: our service]', MINT, MINT_D))
    story.append(Spacer(1,3*mm))

    story.append(Paragraph('3.2 프레임 분류 (Frame Classification)', H3))
    story.append(Paragraph(
        '추출된 프레임이 개인정보 처리 방식과 관련 있는지 판별하기 위해 XLNet 분류기를 사용한다. '
        'XLNet은 사전 실험에서 BERT 기반 모델보다 프레임 분류에서 우수한 성능을 보였다. '
        '분류는 2단계로 이루어진다.', KR_J))

    cls_data = [
        ['1단계', 'SKIP vs KEEP', '개인정보와 무관한 프레임(72.6%)을 걸러냄'],
        ['2단계', 'FPCU', '1자 데이터 수집·사용 (First Party Collection/Use)'],
        ['',      'TPSC', '제3자 공유 (Third Party Sharing/Collection)'],
        ['',      'UCC',  '사용자 선택권·통제 (User Choice/Control) — 옵트인/아웃'],
        ['',      'UAED', '사용자 데이터 접근·수정·삭제 (User Access, Edit, Delete)'],
        ['',      'DR',   '데이터 보존 기간 (Data Retention)'],
    ]
    story.append(Table(cls_data, colWidths=[18*mm,22*mm,130*mm],
        style=TableStyle([
            ('BACKGROUND',(0,0),(0,-1),LIGHT),('BACKGROUND',(1,0),(1,-1),colors.HexColor('#F0F4FF')),
            ('FONTNAME',(0,0),(-1,-1),'Korean'),('FONTSIZE',(0,0),(-1,-1),9),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),
            ('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('TEXTCOLOR',(0,0),(0,-1),NAVY),('TEXTCOLOR',(1,0),(1,-1),BLUE),
            ('SPAN',(0,1),(0,5)),
        ])))
    story.append(Paragraph(
        '훈련 데이터: OPP-115에서 추출한 13,946개 의미 프레임을 프라이버시 정책 주석 경력 3년 이상의 연구자가 직접 주석하고, '
        '5년 이상 경력자 2명이 검증. 10-겹 교차 검증(9:1 훈련/테스트 분할) 사용.', KR_J))
    story.append(Spacer(1,3*mm))

    story.append(Paragraph('3.3 프라이버시 역할 매핑 (Privacy Role Mapping)', H3))
    story.append(Paragraph(
        '146개 동사에 대해 PropBank의 범용 인수 정의를 프라이버시 특화 역할로 변환한다. '
        '같은 동사라도 프레임 카테고리에 따라 다른 역할로 매핑될 수 있다.', KR_J))

    role_data = [
        ['DATA', '사용자에 관한 개인·민감·비개인 정보'],
        ['FIRST_PARTY_ENTITY', '사용자와 직접 상호작용하는 조직 (데이터 수집·사용 책임자)'],
        ['THIRD_PARTY_ENTITY', '1자 조직과 협력하는 외부 조직 또는 엔티티'],
        ['MECHANISM', '데이터 수집에 사용되는 절차 및 방법 (예: 쿠키)'],
        ['PURPOSE', '데이터 수집·사용·공유의 구체적인 이유'],
        ['SHARING_TERMS', '제3자와 데이터를 공유하는 조건과 합의'],
        ['USER_TRIGGER', '데이터 수집·사용·공유를 유발할 수 있는 사용자 행동/이벤트'],
        ['OPT_IN_MECHANISM', '사용자가 데이터 수집에 명시적으로 동의하는 방법'],
        ['OPT_OUT_MECHANISM', '사용자가 데이터 수집을 거부·중단하는 방법'],
        ['CONSEQUENCE', '사용자 선택·행동의 잠재적 결과 또는 영향'],
        ['USER_MECHANISM', '사용자가 자신의 데이터에 접근·수정·삭제하는 방법'],
        ['TIME_PERIOD', '사용자 데이터 보존 기간'],
    ]
    story.append(Table([['역할','설명']]+role_data, colWidths=[50*mm,120*mm],
        style=TableStyle([
            ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
            ('BACKGROUND',(0,1),(0,-1),LIGHT),
            ('FONTNAME',(0,0),(-1,-1),'Korean'),('FONTSIZE',(0,0),(-1,-1),8.5),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),
            ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
            ('TEXTCOLOR',(0,1),(0,-1),NAVY),
        ])))
    story.append(Spacer(1,4*mm))

    # ── 4. 결과 ─────────────────────────────
    story.append(Paragraph('4. 실험 및 결과', H2))
    story.append(Paragraph('4.1 분류 성능', H3))
    story.append(Paragraph(
        '2단계 XLNet 분류기는 weighted avg F1-score 0.97을 달성했다. '
        '1단계(SKIP/KEEP 분류)는 macro avg F1 0.96, 2단계(카테고리 분류)는 macro avg F1 0.98을 기록했다.', KR_J))

    perf_data = [
        ['방법','SKIP F1','FPCU F1','TPSC F1','UCC F1','UAED F1','DR F1','Weighted Avg'],
        ['Frame only','0.93','0.72','0.70','0.74','0.15','0.24','0.86'],
        ['FSC Augmented','0.92','0.72','0.74','0.86','0.84','0.83','0.88'],
        ['FSC Aug (Two-Level)','0.98','0.93','0.93','0.93','0.92','0.92','0.97'],
    ]
    story.append(Table(perf_data, colWidths=[45*mm]+[18*mm]*7,
        style=TableStyle([
            ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
            ('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#E6F0FF')),
            ('FONTNAME',(0,0),(-1,-1),'Korean'),('FONTSIZE',(0,0),(-1,-1),8),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
            ('ALIGN',(1,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ])))
    story.append(Spacer(1,3*mm))

    story.append(Paragraph('4.2 대규모 정책 분석 결과', H3))
    story.append(Paragraph(
        'Princeton Privacy Crawl(PPCrawl) 코퍼스의 130,604개 웹사이트 정책 129,856개를 분석하여 '
        '3,970만 개 이상의 의미 프레임을 처리했다. '
        '정책 하나당 평균 306개의 프레임이 생성되었으나, 실제 개인정보와 관련 있는 KEEP 프레임은 평균 30개에 불과했다.', KR_J))

    missing_data = [
        ['누락된 역할 항목','누락 정책 비율','의미'],
        ['USER_MECHANISM (데이터 삭제 방법)','약 90%','사용자가 데이터를 삭제하는 방법을 알 수 없음'],
        ['CONSEQUENCE (옵트인/아웃 결과)','약 75%','옵트인/아웃을 했을 때 어떤 결과가 생기는지 미기재'],
        ['MECHANISM (수집 방법)','약 40%','어떤 방법으로 데이터를 수집하는지 안 나옴'],
        ['USER_TRIGGER (수집 조건)','약 20%','언제 데이터가 수집되는지 미기재'],
        ['UAED 프레임 자체','약 50%','접근·수정·삭제 관련 내용이 아예 없음'],
    ]
    story.append(Table(missing_data, colWidths=[65*mm,30*mm,75*mm],
        style=TableStyle([
            ('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),WHITE),
            ('FONTNAME',(0,0),(-1,-1),'Korean'),('FONTSIZE',(0,0),(-1,-1),8.5),
            ('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),
            ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
            ('TEXTCOLOR',(1,1),(1,-1),colors.HexColor('#CC2200')),('ALIGN',(1,0),(1,-1),'CENTER'),
        ])))
    story.append(Spacer(1,3*mm))

    story.append(Paragraph('4.3 ChatGPT-3.5 비교', H3))
    story.append(Paragraph(
        'PolicyPulse와 ChatGPT-3.5를 비교한 결과, ChatGPT는 야후 2018 개인정보처리방침 요약 시 '
        '제3자 데이터 공유 내용을 누락하거나 부정확한 정보를 생성하는 환각(hallucination) 문제를 보였다. '
        'PolicyPulse는 원문 기반으로 추출하므로 이러한 문제가 없다. '
        '단, 저자들은 GPT-4 등 최신 LLM과의 비교는 향후 연구 과제로 남겼다.', KR_J))
    story.append(Spacer(1,4*mm))

    # ── 5. 응용 ─────────────────────────────
    story.append(Paragraph('5. 잠재적 응용 분야', H2))
    app_data = [
        ['정책 완전성 검사','추출된 역할 정보를 바탕으로 정책이 필수 정보를 포함하는지 자동 검사. 정책 작성자에게 누락 항목 피드백 제공 가능'],
        ['짧은 공지 생성','FPCU·TPSC·DR 프레임에서 핵심 정보를 추출하여 간결한 요약문 자동 생성'],
        ['개인정보 영양 정보 라벨','Kelley et al. 제안 형식을 따라, 수집 데이터·공유 목적·제3자 등을 표 형태로 자동 생성'],
        ['자동 질의응답','특정 역할(예: TIME_PERIOD)과 의미 유사도를 이용해 사용자 질문에 정책 원문 기반 답변 제공'],
        ['사용자 선호도 자동 확인','사용자가 설정한 프라이버시 선호도와 추출된 정책 정보를 자동 대조하여 위반 시 알림'],
    ]
    story.append(Table(app_data, colWidths=[40*mm,130*mm],
        style=TableStyle([
            ('BACKGROUND',(0,0),(0,-1),LIGHT),('FONTNAME',(0,0),(-1,-1),'Korean'),
            ('FONTSIZE',(0,0),(-1,-1),9),('GRID',(0,0),(-1,-1),0.3,colors.HexColor('#CCCCCC')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),
            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('TEXTCOLOR',(0,0),(0,-1),NAVY),
        ])))
    story.append(Spacer(1,4*mm))

    # ── 6. 한계점 ────────────────────────────
    story.append(Paragraph('6. 한계점 및 향후 연구', H2))
    story.append(Paragraph(
        '현재 PolicyPulse는 영어 개인정보처리방침에만 적용 가능하다. '
        'DR 및 UAED 카테고리는 학습 데이터가 적어 상대적으로 낮은 성능을 보이며, '
        '데이터 증강으로 일부 보완했지만 완전하지 않다. '
        '또한 문장 수준 분석에 한정되어 문장 간 관계 파악이 어렵고, '
        '생성된 요약(짧은 공지, 영양 정보 라벨)에 대한 사용자 평가 연구가 수행되지 않았다.', KR_J))
    story.append(Paragraph(
        '향후 연구 방향으로는 문장 간 관계 포착, 분류 기반 역할 매핑, 다국어 지원, '
        'GDPR 및 캘리포니아 Delete Act 등 규정 준수 분석에의 적용이 제시되었다.', KR_J))
    story.append(Spacer(1,4*mm))

    # ── 7. 결론 ─────────────────────────────
    story.append(Paragraph('7. 결론', H2))
    story.append(box(
        'PolicyPulse는 의미역 레이블링과 프레임 분류를 결합하여 개인정보처리방침에서 세밀한 정보를 자동으로 추출하는 파이프라인이다. '
        '130만 개 이상의 정책을 분석한 결과, 대부분의 정책이 사용자 데이터 삭제 방법(90%)이나 '
        '옵트인/아웃 결과(75%) 등 중요한 정보를 제대로 명시하지 않는다는 점을 발견했다. '
        'PolicyPulse는 이러한 누락을 자동으로 식별하고, 다양한 형태의 사용자 친화적인 정책 표시를 '
        '추가적인 저자 작업 없이 자동 생성할 수 있는 기반을 제공한다. '
        '코드 및 데이터: github.com/crisp-du/ppevo'
    ))
    story.append(Spacer(1,5*mm))

    # ── 참고문헌 ─────────────────────────────
    story.append(Paragraph('주요 참고문헌', H2))
    refs = [
        'Harkous et al., "Polisis: Automated Analysis and Presentation of Privacy Policies Using Deep Learning," USENIX Security 2018.',
        'Cui et al., "PoliGraph: Automated Privacy Policy Analysis using Knowledge Graphs," USENIX Security 2023.',
        'Bhatia et al., "Mining Privacy Goals from Privacy Policies Using Hybridized Task Analysis," ACM TOCHI 2016.',
        'Yang et al., "XLNet: Generalized Autoregressive Pretraining for Language Understanding," NeurIPS 2019.',
        'Wilson et al., "The Creation and Analysis of a Website Privacy Policy Corpus (OPP-115)," ACL 2016.',
    ]
    for r in refs:
        story.append(Paragraph('• '+r, SMALL))
        story.append(Spacer(1,1*mm))

    doc.build(story)
    print(f'✅ 한국어 번역 논문 저장: {path}')


# ══════════════════════════════════════════════
make_slides('/Users/jeondonghyeog/Desktop/PaperReview_PolicyPulse_slides.pdf')
make_korean_paper('/Users/jeondonghyeog/Desktop/PaperReview_PolicyPulse_Korean.pdf')
