import os
import json
import random
from datetime import datetime

DOMAIN = "https://breath-therapy.netlify.app"
OUTPUT_DIR = "./dist"

NAVER_VERIFICATION = "c4c3c3682786176be905d7f374ec133a07578772"

regions = [
    {"id": "gangnam", "name": "강남구"},
    {"id": "seocho", "name": "서초구"},
    {"id": "busan", "name": "부산광역시"},
    {"id": "suwon", "name": "경기 수원"}
]

# 작성해주신 5개 업체로 고정하고, 코스/관리사/인사말/후기 데이터를 세부적으로 추가했습니다.
shops = [
    {
        "id": "queens", "region_id": "gangnam", "name": "퀸즈홈테라피", "phone": "0507-1280-3296",
        "address": "서울 강남구", "detail_address": "강남구 역삼동 (상세주소 문의)", "station": "강남역 1번출구",
        "hours": "오전 09:00부터 익일 04:00까지 영업",
        "greeting": "서울 강남구의 안식처 퀸즈홈테라피가 지친 하루를 달래고자 방문하신 여러분을 위해 따스한 환영과 감사의 마음을 올립니다.<br><br>한국관리사의 따뜻한 온기가 담긴 스웨디시는 전신의 경직된 긴장을 부드럽게 풀어내며 오감을 깨우는 깊은 이완과 회복의 순간을 연출합니다. 오직 나만의 안식에 몰입할 수 있는 환경을 보장합니다.",
        "courses": [
            {"name": "스웨디시 A코스 60분", "time": "주야", "price": "130,000"},
            {"name": "스웨디시 B코스 80분", "time": "주간", "price": "150,000"},
            {"name": "스웨디시 C코스 120분", "time": "주야", "price": "260,000"}
        ],
        "managers": ["이슬", "유정", "정이", "윤영"],
        "reviews": [
            {"title": "제 취향인 단발상 첫인상부터 끌렸습니다", "author": "썸리스그립", "date": "2026-09-19", "content": "여기 자주 다녔는데 오랜만에 새로 오신 분들이 이끌려서 예약했습니다. 익숙한 곳에 새 얼굴이 생기니 또 가볼 이유가 생기더라구요. 첫인상부터 끌렸습니다!"},
            {"title": "웃으면 더 이뻐요", "author": "새라이하", "date": "2026-08-27", "content": "요즈음 기온 차가 많이 나면서 몸이 찌뿌둥해서 방문했습니다. 실장님 추천으로 뵀는데 장난 아니었습니다. 외모면 외모, 스킬이면 스킬, 다 장난 아니었습니다."}
        ]
    },
    {
        "id": "korean_beauty", "region_id": "gangnam", "name": "한국미인테라피", "phone": "0507-1280-3140",
        "address": "서울 강남구", "detail_address": "강남구 논현동 (상세주소 문의)", "station": "논현역 3번출구",
        "hours": "24시간 상시 영업",
        "greeting": "최고의 힐링을 선사하는 한국미인테라피입니다.<br><br>도심 속 작은 휴식처가 되어드릴 수 있도록, 세심한 소독 관리와 정결한 프라이빗 공간을 완비하여 누구의 방해도 받지 않고 온전한 회복을 누리실 수 있습니다.",
        "courses": [
            {"name": "베이직 코스 60분", "time": "주야", "price": "120,000"},
            {"name": "프리미엄 코스 90분", "time": "주야", "price": "160,000"}
        ],
        "managers": ["지수", "다빈", "아영"],
        "reviews": [
            {"title": "춤추듯 자유스럽게 스웨디시를 해주네요", "author": "고량화백", "date": "2026-07-28", "content": "춤추듯 자유롭게 스웨디시를 해주셨습니다. 너무 편안했고 힐링을 정말 잘했습니다. 관리사분들 교육을 잘 받으시는 건지 확실히 좋았습니다."},
            {"title": "손길에 잠이 쏟아진 힐링테라피의 끝판왕", "author": "골든리트리버", "date": "2026-06-24", "content": "본격적인 관리가 시작됐을 때는 관리사님의 손길이 너무 편안해서 잠깐 졸았던 것 같습니다. 정말 제대로 된 힐링을 경험한 느낌이었습니다."}
        ]
    },
    {
        "id": "tonight", "region_id": "seocho", "name": "오늘밤테라피", "phone": "0507-1280-3199",
        "address": "서울 서초구", "detail_address": "서초구 반포동 (상세주소 예약시 안내)", "station": "신논현역 2번출구",
        "hours": "오후 12:00부터 익일 05:00까지 영업",
        "greeting": "오늘 하루 고생한 나를 위한 특별한 안식, 오늘밤테라피입니다.<br><br>정성 어린 손길을 통해 온전한 회복과 기분 좋은 변화를 직접 누려보세요. 최상의 서비스로 보답하겠습니다.",
        "courses": [
            {"name": "감성 테라피 60분", "time": "주야", "price": "130,000"},
            {"name": "감성 테라피 90분", "time": "주야", "price": "170,000"}
        ],
        "managers": ["세아", "예은", "하은"],
        "reviews": [
            {"title": "오늘은 안 남길 수가 없었네요", "author": "만월경소작", "date": "2026-06-04", "content": "관리하시는 분 나이도 어린 것 같은데 스킬이 좋으셨어요. 올 때마다 만족스러웠지만 오늘은 더 만족스러운 마사지였어요."},
            {"title": "들어오시자마자 마음이 녹아내렸습니다", "author": "덩덩미미", "date": "2026-05-20", "content": "외모도 너무 예쁘시고 성격도 너무 착하시고, 들어오시자마자 분위기 자체가 달랐어요. 말도 계속 걸어주시면서 정말 편하게 관리 받고 갑니다."}
        ]
    },
    {
        "id": "juju", "region_id": "busan", "name": "주주테라피", "phone": "0507-1280-3197",
        "address": "부산광역시", "detail_address": "해운대구 우동 (상세주소 문의)", "station": "해운대역 5번출구",
        "hours": "24시간 상시 영업",
        "greeting": "부산 최고의 프라이빗 샵 주주테라피입니다.<br><br>지친 몸과 마음을 재충전할 수 있는 완벽한 코스가 준비되어 있습니다. 쾌적한 실내 환경에서 수준 높은 관리를 약속드립니다.",
        "courses": [
            {"name": "아로마 60분", "time": "주야", "price": "110,000"},
            {"name": "스웨디시 60분", "time": "주야", "price": "140,000"}
        ],
        "managers": ["지유", "서연", "민지"],
        "reviews": [
            {"title": "볼륨감이랑 몸매, 진짜 탑입니다!", "author": "지갑대방출", "date": "2026-04-25", "content": "관리사님 몸매 라인이 정말 예술이네요. 남다른 마인드까지 갖추고 계셔서 받는 내내 감탄했네요. 조만간 또 뵈러 와야겠습니다."},
            {"title": "주머니에 쏙 넣고 싶을 만큼 치명적인 매력", "author": "라러더댜", "date": "2026-04-03", "content": "순수해 보이시는 외모와는 달리 반전 매력이 정말 대박적입니다. 알아서 척척 만족스럽게 관리해 주시는 센스 최고!"}
        ]
    },
    {
        "id": "joy", "region_id": "suwon", "name": "기쁨테라피", "phone": "0507-1280-3183",
        "address": "경기 수원", "detail_address": "수원시 팔달구 인계동", "station": "수원시청역 8번출구",
        "hours": "오전 11:00부터 익일 04:00까지 영업",
        "greeting": "수원 인계동 기쁨테라피에서 인사드립니다.<br><br>일상의 스트레스를 잊고 온전히 쉴 수 있도록 정성을 다해 모시겠습니다. 철저한 위생 관리로 언제나 안심하고 방문하실 수 있습니다.",
        "courses": [
            {"name": "VIP 스웨디시 70분", "time": "주야", "price": "140,000"},
            {"name": "황제 코스 100분", "time": "주야", "price": "190,000"}
        ],
        "managers": ["소희", "수진", "현아"],
        "reviews": [
            {"title": "큰 키에 스탠다드한 스타일", "author": "블랭크핑제니", "date": "2026-07-13", "content": "관리는 이렇게 열심히 하는 관리사님을 본 적이 있나 싶을 정도로, 과할 만큼 정성껏 잘해주셨습니다. 저는 다시 또 뵈러 갈 것 같습니다."},
            {"title": "관리사분 스킬이 훌륭!", "author": "지렁이게임", "date": "2026-07-22", "content": "출장 중 찾아간 건데, 깔끔하고 인테리어가 좋았습니다. 카운터에서 안내하시는 사장님도 너무 친절하셨습니다."}
        ]
    }
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sitemap_urls = []
today = datetime.now().strftime("%Y-%m-%d")

# 1. 메인 페이지 생성
main_shop_list = ""
for shop in shops:
    main_shop_list += f"""
        <li class="swiper-slide">
            <a href="shop_{shop['id']}.html">
                <figure>
                    <img src="https://www.hi-massage.kr/assets/images/og.png" alt="{shop['name']}" loading="lazy">
                    <figcaption>
                        <strong>{shop['name']}</strong>
                        <span>{shop['phone']}</span>
                    </figcaption>
                </figure>
            </a>
        </li>"""

main_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스웨디시·아로마·타이 마사지샵 추천｜전국 지역별 검색 - 숨결테라피</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.0.5/swiper-bundle.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/index.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.0.5/swiper-bundle.min.js"></script>
    <script src="https://www.hi-massage.kr/assets/javascripts/index.js"></script>
</head>
<body>
    <header>
        <h1><a href="/">숨결테라피</a></h1>
        <p>스웨디시, 아로마, 타이 마사지샵 추천과 전국 지역별 검색</p>
    </header>
    <nav aria-label="주요 메뉴">
        <section>
            <h2>지역별 마사지샵 검색</h2>
            <ul>
                {"".join([f'<li><a href="region_{r["id"]}.html">{r["name"]} 마사지샵</a></li>' for r in regions])}
            </ul>
        </section>
    </nav>
    <main>
        <section>
            <h2>추천 마사지샵</h2>
            <div class="swiper">
                <ul class="swiper-wrapper">
                    {main_shop_list}
                </ul>
            </div>
        </section>
    </main>
</body>
</html>"""
with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(main_html)
sitemap_urls.append(f"{DOMAIN}/index.html")


# 2. 지역 페이지 생성
for region in regions:
    r_id = region["id"]
    r_name = region["name"]
    
    local_shops = [s for s in shops if s.get("region_id") == r_id]
    if not local_shops: 
        local_shops = shops # 샘플 노출용
        
    region_shop_list = ""
    for shop in local_shops:
        region_shop_list += f"""
        <li class="card">
            <article>
                <div class="primary" style="padding:15px;">
                    <h3><a href="shop_{shop['id']}.html"><span>출장마사지</span> <strong>{shop['name']}</strong></a></h3>
                    <p><i class="fa-solid fa-phone"></i> <a href="tel:{shop['phone']}">{shop['phone']}</a></p>
                </div>
            </article>
        </li>"""
    
    region_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{r_name} 출장마사지 추천 | 스웨디시·아로마 검색 - 숨결테라피</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/list.css">
</head>
<body>
    <header>
        <nav aria-label="상단 메뉴"><a href="index.html"><span>홈으로 가기</span></a></nav>
        <h1>{r_name} <span>출장마사지 목록</span></h1>
    </header>
    <main>
        <section class="list">
            <h2>{r_name} 마사지샵 목록</h2>
            <ol>
                {region_shop_list}
            </ol>
        </section>
    </main>
</body>
</html>"""
    with open(f"{OUTPUT_DIR}/region_{r_id}.html", "w", encoding="utf-8") as f:
        f.write(region_html)
    sitemap_urls.append(f"{DOMAIN}/region_{r_id}.html")


# 3. 샵 상세 페이지 생성 (후기 및 코스 동적 바인딩)
for shop in shops:
    s_id = shop["id"]
    
    # 3-1. 코스 리스트 HTML 생성
    course_html = ""
    for c in shop["courses"]:
        course_html += f"""
        <li>
            <article>
                <h5>{c['name']}</h5>
                <dl><dt>{c['time']}</dt><dd>{c['price']}원</dd></dl>
            </article>
        </li>"""
        
    # 3-2. 관리사 리스트 HTML 생성
    manager_html = "".join([f"<li><p>{m}</p></li>" for m in shop["managers"]])
    
    # 3-3. 후기 리스트 HTML 생성
    review_html = ""
    for r in shop["reviews"]:
        review_html += f"""
        <li>
            <article>
                <h3>{r['title']}</h3>
                <div><p>{r['content']}</p></div>
                <dl>
                    <dt><i class="fa-solid fa-user"></i> 작성자</dt><dd>{r['author']}</dd>
                    <dt><i class="fa-solid fa-calendar-days"></i> 작성일</dt><dd>{r['date']}</dd>
                </dl>
            </article>
        </li>"""

    shop_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{shop['name']} - 출장마사지 및 스웨디시 | 숨결테라피</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/shop.css">
</head>
<body>
    <header>
        <nav aria-label="상단 메뉴"><a class="back-move" href="javascript:history.back();"><span>뒤로 가기</span></a></nav>
        <h1><span>출장마사지 전문</span> {shop['name']}</h1>
    </header>
    <main>
        <!-- 코스 안내 -->
        <section class="course">
            <h2><span aria-hidden="true">&gt;&gt;</span> 코스 안내</h2>
            <section class="details">
                <ul>{course_html}</ul>
            </section>
        </section>

        <!-- 관리사 안내 -->
        <section class="masseur">
            <h2><span aria-hidden="true">&gt;&gt;</span> 관리사</h2>
            <section class="profile">
                <ul>{manager_html}</ul>
            </section>
        </section>

        <!-- 인사말 -->
        <section class="greeting">
            <h2><span aria-hidden="true">&gt;&gt;</span> 인사말</h2>
            <div>
                <p>{shop['greeting']}</p>
            </div>
        </section>

        <!-- 예약 문의 -->
        <section class="mtonet">
            <h2><span aria-hidden="true">&gt;&gt;</span> 예약 문의</h2>
            <dl>
                <dt>• <span>전화 번호</span></dt><dd><a href="tel:{shop['phone']}">{shop['phone']}</a></dd>
                <dt>• <span>연락 방법</span></dt><dd>전화 또는 문자로 상담 요망</dd>
            </dl>
        </section>

        <!-- 영업 시간 -->
        <section class="working">
            <h2><span aria-hidden="true">&gt;&gt;</span> 영업 시간</h2>
            <dl>
                <dt>• <span>예약 시간</span></dt><dd><strong>{shop['hours']}</strong></dd>
                <dt>• <span>휴무 일자</span></dt><dd>365일 연중 무휴</dd>
            </dl>
        </section>

        <!-- 찾아오는 길 -->
        <section class="direction">
            <h2><span aria-hidden="true">&gt;&gt;</span> 찾아오는 길</h2>
            <dl>
                <dt>• <span>상세 위치</span></dt><dd><strong>{shop['address']}, {shop['station']}</strong></dd>
                <dt>• <span>상세 주소</span></dt><dd>{shop['detail_address']}</dd>
                <dt>• <span>주차 여부</span></dt><dd>주차무료</dd>
            </dl>
        </section>

        <!-- 이용 후기 -->
        <section id="review" class="review">
            <h2>이용 후기 <span>총 {len(shop['reviews'])}건</span></h2>
            <ol>
                {review_html}
            </ol>
        </section>
        
        <details class="faq">
            <summary><h2>· 자주 하는 질문 <i class="fa-solid fa-chevron-down"></i></h2></summary>
            <div>
                <dl>
                    <dt><i class="fa-solid fa-q"></i> 예약과 결제는 어떻게 진행되나요?</dt>
                    <dd><i class="fa-solid fa-a"></i> 대부분 예약제로 운영되므로 반드시 전화, 문자로 예약 후에 이용해 주세요.</dd>
                </dl>
            </div>
        </details>
    </main>
</body>
</html>"""
    with open(f"{OUTPUT_DIR}/shop_{s_id}.html", "w", encoding="utf-8") as f:
        f.write(shop_html)
    sitemap_urls.append(f"{DOMAIN}/shop_{s_id}.html")

# 4. sitemap.xml & robots.txt 생성
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
sitemap_content += '</urlset>'

with open(f"{OUTPUT_DIR}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
with open(f"{OUTPUT_DIR}/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)

print(f"✅ 지정된 5개 업체 샵 상세 페이지(코스/관리사/인사말/후기 포함) 생성이 완료되었습니다.")