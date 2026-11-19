import os
import json
import random
from datetime import datetime

DOMAIN = "https://breath-therapy.netlify.app"
OUTPUT_DIR = "./dist"

# 네이버 소유권 확인 메타 태그 (발급받은 키로 변경하세요)
NAVER_VERIFICATION = "c4c3c3682786176be905d7f374ec133a07578772"

# 1. 텍스트 스피닝(Spinning)용 문구 모음 (유사문서 회피용)
desc_variations = [
    "상세 정보와 이용 후기를 참고해 원하는 업체를 선택할 수 있습니다.",
    "실제 방문자 후기와 정확한 코스 가격을 비교하여 최적의 테라피를 경험하세요.",
    "지친 일상을 달래줄 완벽한 휴식처, 내 주변 검증된 마사지샵을 쉽게 찾아보세요."
]
greeting_variations = [
    "지친 하루를 달래고자 방문하신 여러분을 위해 따스한 환영과 감사의 마음을 올립니다.",
    "피로에 지친 고객님들께 진정한 힐링과 편안한 안식처를 제공해 드리기 위해 최선을 다하고 있습니다.",
    "정성 어린 손길과 아늑한 공간으로, 방문하시는 모든 분들께 잊지 못할 휴식을 선사합니다."
]

regions = [
    {"id": "gangnam", "name": "강남구"},
    {"id": "seocho", "name": "서초구"},
    {"id": "yeongdeungpo", "name": "영등포구"},
    {"id": "busan", "name": "부산광역시"},
    {"id": "suwon", "name": "경기 수원"}
]

# 영등포구 디자인스웨디시 상세 데이터 포함
shops = [
    {
        "id": "design_swedish", "region_id": "yeongdeungpo", "name": "디자인스웨디시", 
        "phone": "0507-0493-3729", "address": "서울 영등포구 영등포동5가", 
        "detail_address": "영등포구 영중로18길 15-1, 건물 1층", "station": "영등포시장역 3번출구", 
        "price": "130,000", "hours": "오전 09:00부터 익일 04:00까지 영업",
        "reviews": [
            {"title": "제 취향인 단발상 첫인상부터 끌렸습니다", "author": "썸리스그립", "date": "2026-09-19", "content": "칼단발 쌤. 원하는 스타일을 만나는 것부터가 일이에요. 첫인상부터 끌렸습니다!"},
            {"title": "웃으면 더 이뻐요", "author": "새라이하", "date": "2026-08-27", "content": "요즈음 기온 차가 많이 나면서 몸이 찌뿌둥해서 방문했습니다. 실장님 추천으로 뵀는데 장난 아니었습니다."}
        ]
    },
    {
        "id": "queens", "region_id": "gangnam", "name": "퀸즈홈테라피", 
        "phone": "0507-1280-3296", "address": "서울 강남구", 
        "detail_address": "상세주소 문의", "station": "강남역 인근", 
        "price": "130,000", "hours": "24시간 상시 영업", "reviews": []
    }
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sitemap_urls = []
today = datetime.now().strftime("%Y-%m-%d")

# ==========================================
# 1. 메인 페이지 생성 (출장마사지 키워드 제외)
# ==========================================
main_url = f"{DOMAIN}/index.html"
main_desc = f"숨결테라피에서 스웨디시, 아로마, 타이 테라피 샵을 전국 지역별로 검색해보세요. {random.choice(desc_variations)}"

json_ld_main = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "숨결테라피",
    "url": DOMAIN
}

main_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스웨디시·아로마·타이 마사지샵 추천｜전국 지역별 검색 - 숨결테라피</title>
    <meta name="description" content="{main_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{main_url}">
    <meta name="naver-site-verification" content="{NAVER_VERIFICATION}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="스웨디시·아로마·타이 마사지샵 추천｜전국 지역별 검색 - 숨결테라피">
    <meta property="og:description" content="{main_desc}">
    <meta property="og:url" content="{main_url}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.0.5/swiper-bundle.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/index.css">
    <script type="application/ld+json">{json.dumps(json_ld_main, ensure_ascii=False)}</script>
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
            <h2>가장 주목 받는 테라피샵</h2>
            <ul>
                {"".join([f'<li><a href="shop_{s["id"]}.html"><strong>{s["name"]}</strong></a> ({s["phone"]})</li>' for s in shops])}
            </ul>
        </section>
    </main>
</body>
</html>"""

with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(main_html)
sitemap_urls.append(main_url)

# ==========================================
# 2. 지역 페이지 생성 (출장마사지 포함, 내부 링크 강화)
# ==========================================
for region in regions:
    r_id = region["id"]
    r_name = region["name"]
    r_url = f"{DOMAIN}/region_{r_id}.html"
    r_desc = f"숨결테라피에서 {r_name} 지역의 출장마사지, 스웨디시, 아로마 샵을 검색해보세요. {random.choice(desc_variations)}"
    
    # 해당 지역의 업체만 필터링
    local_shops = [s for s in shops if s.get("region_id") == r_id]
    if not local_shops:
        local_shops = shops # 샘플 데이터 부족 방지
        
    json_ld_region = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{r_name} 출장마사지 추천",
        "url": r_url,
        "itemListElement": [{"@type": "ListItem", "position": i+1, "url": f"{DOMAIN}/shop_{shop['id']}.html"} for i, shop in enumerate(local_shops)]
    }
    
    region_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{r_name} 출장마사지 추천 | 스웨디시·아로마 검색 - 숨결테라피</title>
    <meta name="description" content="{r_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{r_url}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{r_name} 출장마사지 추천">
    <meta property="og:url" content="{r_url}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/list.css">
    <script type="application/ld+json">{json.dumps(json_ld_region, ensure_ascii=False)}</script>
</head>
<body>
    <header>
        <nav aria-label="상단 메뉴"><a href="index.html"><span>홈으로 가기</span></a></nav>
        <h1>{r_name} <span>출장마사지 목록</span></h1>
    </header>
    <main>
        <nav aria-label="현재 위치">
            <ol>
                <li><a href="/">홈</a></li>
                <li aria-current="page">{r_name}</li>
            </ol>
        </nav>
        <section class="list">
            <ol>
                {"".join([f'''
                <li class="card">
                    <article>
                        <div class="primary">
                            <h3><a href="shop_{s['id']}.html"><span>출장마사지</span> <strong>{s['name']}</strong></a></h3>
                            <p><i class="fa-solid fa-phone"></i> <a href="tel:{s['phone']}">{s['phone']}</a></p>
                        </div>
                    </article>
                </li>''' for s in local_shops])}
            </ol>
        </section>
        
        <!-- 주변 지역 내부 링크 (Silo 구조) -->
        <details class="link">
            <summary><h2>· 다른 지역 둘러보기 <i class="fa-solid fa-chevron-down"></i></h2></summary>
            <div>
                <ul>
                    {"".join([f'<li><a href="region_{r["id"]}.html">{r["name"]} 출장마사지</a></li>' for r in regions if r["id"] != r_id])}
                </ul>
            </div>
        </details>
    </main>
</body>
</html>"""
    with open(f"{OUTPUT_DIR}/region_{r_id}.html", "w", encoding="utf-8") as f:
        f.write(region_html)
    sitemap_urls.append(r_url)

# ==========================================
# 3. 샵 상세 페이지 생성 (FAQPage, LocalBusiness 복합 JSON-LD)
# ==========================================
for shop in shops:
    s_id = shop["id"]
    s_name = shop["name"]
    s_url = f"{DOMAIN}/shop_{s_id}.html"
    r_name = next((r["name"] for r in regions if r["id"] == shop.get("region_id")), "전국")
    
    s_desc = f"전문적인 테라피가 준비된 {shop['address']} {s_name}에서 부드러운 스웨디시 출장마사지를 경험하며 여유를 더해보세요. 예약: {shop['phone']}"
    spin_greeting = random.choice(greeting_variations)
    
    # 구조화 데이터 병합 (LocalBusiness + FAQPage)
    json_ld_shop = [
        {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": s_name,
            "url": s_url,
            "telephone": shop["phone"],
            "priceRange": f"{shop['price']}원",
            "address": {"@type": "PostalAddress", "addressCountry": "KR", "addressLocality": shop["address"]}
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": f"{s_name}의 대표 코스는 무엇인가요?", "acceptedAnswer": {"@type": "Answer", "text": f"스웨디시 60분 {shop['price']}원입니다."}},
                {"@type": "Question", "name": "예약과 결제는 어떻게 진행되나요?", "acceptedAnswer": {"@type": "Answer", "text": "예약제로 운영되며 입실 전 선불 결제입니다."}}
            ]
        }
    ]
    
    review_html = ""
    if shop.get("reviews"):
        for rev in shop["reviews"]:
            review_html += f"""
            <li>
                <article>
                    <h3>{rev['title']}</h3>
                    <div><p>{rev['content']}</p></div>
                    <dl>
                        <dt><i class="fa-solid fa-user"></i> 작성자</dt><dd>{rev['author']}</dd>
                        <dt><i class="fa-solid fa-calendar-days"></i> 작성일</dt><dd>{rev['date']}</dd>
                    </dl>
                </article>
            </li>"""

    shop_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{s_name} - {r_name} 출장마사지 및 스웨디시 | 숨결테라피</title>
    <meta name="description" content="{s_desc}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{s_url}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{s_name} - {r_name} 출장마사지">
    <meta property="og:description" content="{s_desc}">
    <meta property="og:url" content="{s_url}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/shop.css">
    <script type="application/ld+json">{json.dumps(json_ld_shop, ensure_ascii=False)}</script>
</head>
<body>
    <header>
        <nav aria-label="상단 메뉴"><a class="back-move" href="javascript:history.back();"><span>뒤로 가기</span></a></nav>
        <h1><span>출장마사지 전문</span> {s_name}</h1>
    </header>
    <main>
        <section class="greeting">
            <h2><span aria-hidden="true">&gt;&gt;</span> 인사말</h2>
            <div>
                <p>{shop['address']}의 안식처 {s_name}입니다. {spin_greeting}</p>
                <p>한국관리사의 따뜻한 온기가 담긴 스웨디시는 전신의 경직된 긴장을 부드럽게 풀어내며 깊은 이완과 회복의 순간을 연출합니다.</p>
            </div>
        </section>

        <section class="course">
            <h2><span aria-hidden="true">&gt;&gt;</span> 코스 안내</h2>
            <article>
                <h5>스웨디시 60분</h5>
                <dl><dt>이용가</dt><dd>{shop['price']}원</dd></dl>
            </article>
        </section>

        <section class="mtonet">
            <h2><span aria-hidden="true">&gt;&gt;</span> 예약 문의</h2>
            <dl>
                <dt>• <span>전화 번호</span></dt><dd><a href="tel:{shop['phone']}">{shop['phone']}</a></dd>
                <dt>• <span>영업 시간</span></dt><dd>{shop['hours']}</dd>
                <dt>• <span>상세 위치</span></dt><dd>{shop['address']} {shop['station']}</dd>
            </dl>
        </section>

        <section id="review" class="review">
            <h2>이용 후기</h2>
            <ol>
                {review_html if review_html else "<li>등록된 후기가 없습니다.</li>"}
            </ol>
        </section>
        
        <!-- 주변 업체 내부 링크 (고립 페이지 방지) -->
        <section class="related">
            <h2>근처 추천 업체</h2>
            <ul>
                {"".join([f'<li><a href="shop_{s["id"]}.html">{s["name"]}</a></li>' for s in shops if s["id"] != s_id])}
            </ul>
        </section>
    </main>
</body>
</html>"""
    with open(f"{OUTPUT_DIR}/shop_{s_id}.html", "w", encoding="utf-8") as f:
        f.write(shop_html)
    sitemap_urls.append(s_url)

# ==========================================
# 4. sitemap.xml & robots.txt 자동 생성
# ==========================================
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
sitemap_content += '</urlset>'

with open(f"{OUTPUT_DIR}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
with open(f"{OUTPUT_DIR}/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)

print(f"✅ 네이버 SEO 최적화(표준URL, 메타태그, 텍스트 스피닝, 내부링크)가 적용된 파일 {len(sitemap_urls)}개가 성공적으로 생성되었습니다.")