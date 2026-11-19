import os
import json
import random
from datetime import datetime

DOMAIN = "https://breath-therapy.netlify.app"
OUTPUT_DIR = "./dist"
NAVER_VERIFICATION = "c4c3c3682786176be905d7f374ec133a07578772"

# ==========================================
# 1. 지역 데이터 (SEO를 위한 고유 에세이 본문 추가)
# ==========================================
regions = [
    {
        "id": "gangnam", "name": "강남구", 
        "seo_text": "강남구 테헤란로 일대의 바쁜 직장인들에게 퇴근 후 스웨디시 관리는 하루의 스트레스를 날려버리는 최고의 휴식입니다. 역삼, 선릉, 삼성역 주변에는 접근성이 뛰어나고 프라이빗한 1인샵과 로드샵들이 밀집해 있습니다. 특히 주차 공간을 완비하고 24시간 운영하는 곳이 많아 야근 후에도 부담 없이 방문할 수 있다는 것이 강남구 마사지샵들의 가장 큰 장점입니다. 청결한 시설과 검증된 실력을 갖춘 곳들을 엄선했습니다."
    },
    {
        "id": "seocho", "name": "서초구", 
        "seo_text": "서초구 방배동과 서초동, 강남역 인근은 조용하고 고급스러운 분위기의 테라피 샵이 주를 이룹니다. 번잡한 도심 속에서 완벽한 차음을 제공하는 프라이빗 룸에서 아로마와 스웨디시 관리를 받다 보면 어느새 깊은 이완을 경험하게 됩니다. 서초구 지역의 업체들은 특히 위생 관리가 철저하며, 다년간의 경력을 자랑하는 전문 테라피스트들이 상주하고 있어 VIP 수준의 대우를 원하는 분들께 강력히 추천드립니다."
    },
    {
        "id": "yeongdeungpo", "name": "영등포구", 
        "seo_text": "여의도 금융가와 영등포시장역, 당산역 주변은 직장인들의 피로 회복을 위한 힐링 스팟이 곳곳에 숨어 있습니다. 특히 오래 앉아있는 업무 특성상 목과 어깨 뭉침을 호소하는 분들을 위해 부드럽게 림프를 순환시켜주는 감성 테라피가 큰 인기를 끌고 있습니다. 영등포구 지역은 교통이 편리하고 가성비 좋은 코스를 제공하는 샵들이 많아, 주말은 물론 평일 점심시간이나 퇴근길에 가볍게 들러 재충전하기에 안성맞춤입니다."
    },
    {
        "id": "busan", "name": "부산광역시", 
        "seo_text": "부산 해운대와 서면, 광안리 일대는 관광객과 현지인 모두에게 사랑받는 프리미엄 테라피 샵들이 모여 있는 곳입니다. 바다를 보며 쌓인 여행의 피로를 씻어내거나, 일상에 지친 몸을 달래기 위해 찾는 분들이 많습니다. 부산 지역 샵들은 친절한 서비스와 넓고 쾌적한 실내 환경을 자랑하며, 스웨디시부터 정통 타이 마사지까지 선택의 폭이 매우 넓습니다. 내 주변 가장 가까운 휴식처를 지금 바로 확인해보세요."
    },
    {
        "id": "suwon", "name": "경기 수원", 
        "seo_text": "수원 인계동과 광교 신도시, 영통 일대는 젊은 감각의 트렌디한 마사지샵들이 빠르게 늘어나고 있는 핫플레이스입니다. 깔끔하고 모던한 인테리어 속에서 전문적인 교육을 수료한 관리사들의 세심한 케어를 받을 수 있습니다. 커플 단위 방문객을 위한 동반 할인이나 첫 방문객을 위한 파격적인 이벤트도 자주 열리므로, 방문 전 혜택을 꼼꼼히 챙기신다면 더욱 기분 좋은 힐링 타임을 가지실 수 있을 것입니다."
    }
]

# ==========================================
# 2. 업체 데이터 (지역 1:1 매칭 완료)
# ==========================================
shops = [
    # 강남구
    {"id": "queens", "region_id": "gangnam", "name": "퀸즈홈테라피", "phone": "0507-1280-3296", "address": "서울 강남구", "detail_address": "강남구 역삼동", "station": "강남역 1번출구", "hours": "24시간 상시 영업", "price": "130,000", "courses": [{"name": "A코스 60분", "time": "주야", "price": "130,000"}, {"name": "B코스 90분", "time": "주야", "price": "180,000"}], "managers": ["이슬", "유정"], "reviews": [{"title": "제 취향인 첫인상부터 끌렸습니다", "author": "썸리스그립", "date": "2026-09-19", "content": "여기 자주 다녔는데 오랜만에 새로 오신 분들이 이끌려서 예약했습니다. 만족스럽네요."}]},
    {"id": "korean_beauty", "region_id": "gangnam", "name": "한국미인테라피", "phone": "0507-1280-3140", "address": "서울 강남구", "detail_address": "강남구 논현동", "station": "논현역 3번출구", "hours": "오전 10:00 - 익일 05:00", "price": "120,000", "courses": [{"name": "베이직 60분", "time": "주야", "price": "120,000"}], "managers": ["지수", "다빈"], "reviews": [{"title": "자유스럽게 스웨디시를 해주네요", "author": "고량화백", "date": "2026-07-28", "content": "너무 편안했고 힐링을 정말 잘했습니다. 관리사분들 교육을 잘 받으시는 건지 확실히 좋았습니다."}]},
    # 서초구
    {"id": "tonight", "region_id": "seocho", "name": "오늘밤테라피", "phone": "0507-1280-3199", "address": "서울 서초구", "detail_address": "서초구 반포동", "station": "신논현역 2번출구", "hours": "오후 12:00 - 익일 04:00", "price": "140,000", "courses": [{"name": "감성 테라피 60분", "time": "주야", "price": "140,000"}], "managers": ["세아", "예은"], "reviews": [{"title": "오늘은 안 남길 수가 없었네요", "author": "만월경소작", "date": "2026-06-04", "content": "스킬이 좋으셨어요. 올 때마다 만족스러웠지만 오늘은 더 만족스러운 마사지였어요."}]},
    # 영등포구
    {"id": "design_swedish", "region_id": "yeongdeungpo", "name": "디자인스웨디시", "phone": "0507-0493-3729", "address": "서울 영등포구 영등포동5가", "detail_address": "영등포구 영중로18길 15-1", "station": "영등포시장역 3번출구", "hours": "오전 09:00 - 익일 04:00", "price": "130,000", "courses": [{"name": "A코스 60분", "time": "주야", "price": "130,000"}], "managers": ["정이", "윤영"], "reviews": [{"title": "단발상 첫인상부터 끌렸습니다", "author": "단발조아", "date": "2026-08-15", "content": "칼단발 쌤. 원하는 스타일 찾기 힘든데 여긴 최고입니다."}]},
    {"id": "pretty_girl", "region_id": "yeongdeungpo", "name": "예쁨여대생", "phone": "0507-0493-3856", "address": "서울 영등포구", "detail_address": "여의도동 전지역", "station": "여의도역", "hours": "24시간 상시 영업", "price": "70,000", "courses": [{"name": "타이 60분", "time": "주야", "price": "70,000"}], "managers": ["나나", "모모"], "reviews": []},
    # 부산
    {"id": "juju", "region_id": "busan", "name": "주주테라피", "phone": "0507-1280-3197", "address": "부산광역시", "detail_address": "해운대구 우동", "station": "해운대역 5번출구", "hours": "24시간 상시 영업", "price": "110,000", "courses": [{"name": "아로마 60분", "time": "주야", "price": "110,000"}], "managers": ["지유", "서연"], "reviews": [{"title": "볼륨감이랑 몸매, 진짜 탑입니다!", "author": "지갑대방출", "date": "2026-04-25", "content": "관리사님 라인이 예술이네요. 남다른 마인드까지 감탄했습니다."}]},
    # 수원
    {"id": "joy", "region_id": "suwon", "name": "기쁨테라피", "phone": "0507-1280-3183", "address": "경기 수원", "detail_address": "수원시 팔달구 인계동", "station": "수원시청역 8번출구", "hours": "오전 11:00 - 익일 04:00", "price": "140,000", "courses": [{"name": "VIP 스웨디시 70분", "time": "주야", "price": "140,000"}], "managers": ["소희", "수진"], "reviews": [{"title": "스킬이 훌륭!", "author": "지렁이게임", "date": "2026-07-22", "content": "출장 중 찾아간 건데 깔끔하고 인테리어가 좋았습니다."}]}
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sitemap_urls = []
today = datetime.now().strftime("%Y-%m-%d")

# ==========================================
# 3. HTML 생성 로직
# ==========================================

# (1) 메인 페이지
main_shop_list = "".join([f'<li class="swiper-slide"><a href="shop_{s["id"]}.html"><figure><img src="https://www.hi-massage.kr/assets/images/og.png" alt="{s["name"]}" loading="lazy"><figcaption><strong>{s["name"]}</strong><span>{s["phone"]}</span></figcaption></figure></a></li>' for s in shops])
json_ld_main = {"@context": "https://schema.org", "@type": "WebSite", "name": "숨결테라피", "url": DOMAIN}

main_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스웨디시·아로마·타이 마사지샵 추천｜전국 지역별 검색 - 숨결테라피</title>
    <meta name="description" content="숨결테라피에서 스웨디시, 아로마, 타이 마사지샵을 지역별로 검색해보세요. 실제 이용 후기와 상세 정보를 제공합니다.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{DOMAIN}/index.html">
    <meta name="naver-site-verification" content="{NAVER_VERIFICATION}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.0.5/swiper-bundle.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/index.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.0.5/swiper-bundle.min.js"></script>
    <script src="https://www.hi-massage.kr/assets/javascripts/index.js"></script>
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
            <ul>{"".join([f'<li><a href="region_{r["id"]}.html">{r["name"]} 출장마사지</a></li>' for r in regions])}</ul>
        </section>
    </nav>
    <main>
        <section>
            <h2>가장 주목 받는 테라피샵</h2>
            <div class="swiper"><ul class="swiper-wrapper">{main_shop_list}</ul></div>
        </section>
    </main>
</body>
</html>"""
with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(main_html)
sitemap_urls.append(f"{DOMAIN}/index.html")

# (2) 지역 페이지 (에세이 및 1:1 매칭 적용)
for region in regions:
    r_id = region["id"]
    r_name = region["name"]
    local_shops = [s for s in shops if s["region_id"] == r_id]
    
    region_shop_list = "".join([f'<li class="card"><article><div class="primary" style="padding:15px;"><h3><a href="shop_{s["id"]}.html"><span>출장마사지</span> <strong>{s["name"]}</strong></a></h3><p><i class="fa-solid fa-phone"></i> <a href="tel:{s["phone"]}">{s["phone"]}</a></p></div></article></li>' for s in local_shops])
    json_ld_region = {"@context": "https://schema.org", "@type": "ItemList", "name": f"{r_name} 출장마사지", "url": f"{DOMAIN}/region_{r_id}.html", "itemListElement": [{"@type": "ListItem", "position": i+1, "url": f"{DOMAIN}/shop_{s['id']}.html"} for i, s in enumerate(local_shops)]}
    
    region_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{r_name} 출장마사지 추천 | 스웨디시·아로마 검색 - 숨결테라피</title>
    <meta name="description" content="{r_name} 지역의 검증된 출장마사지, 스웨디시, 아로마 샵 정보를 제공합니다. 가격 및 후기를 확인하세요.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{DOMAIN}/region_{r_id}.html">
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
        <!-- SEO 고유 텍스트 (누락 방지) -->
        <section style="padding:20px; background:#f9f9f9; font-size:14px; color:#555; line-height:1.7;">
            {region["seo_text"]}
        </section>
        
        <section class="list">
            <h2>{r_name} 샵 리스트</h2>
            <ol>{region_shop_list if region_shop_list else "<li style='padding:20px;'>현재 등록 준비 중인 지역입니다.</li>"}</ol>
        </section>
        
        <!-- 주변 지역 내부 링크 -->
        <details class="link">
            <summary><h2>· 다른 지역 둘러보기 <i class="fa-solid fa-chevron-down"></i></h2></summary>
            <div><ul>{"".join([f'<li><a href="region_{r["id"]}.html">{r["name"]} 출장마사지</a></li>' for r in regions if r["id"] != r_id])}</ul></div>
        </details>
    </main>
</body>
</html>"""
    with open(f"{OUTPUT_DIR}/region_{r_id}.html", "w", encoding="utf-8") as f:
        f.write(region_html)
    sitemap_urls.append(f"{DOMAIN}/region_{r_id}.html")

# (3) 샵 상세 페이지
for shop in shops:
    s_id = shop["id"]
    r_name = next(r["name"] for r in regions if r["id"] == shop["region_id"])
    
    course_html = "".join([f"<li><article><h5>{c['name']}</h5><dl><dt>{c['time']}</dt><dd>{c['price']}원</dd></dl></article></li>" for c in shop["courses"]])
    manager_html = "".join([f"<li><p>{m}</p></li>" for m in shop["managers"]])
    review_html = "".join([f"<li><article><h3>{r['title']}</h3><div><p>{r['content']}</p></div><dl><dt><i class='fa-solid fa-user'></i> 작성자</dt><dd>{r['author']}</dd><dt><i class='fa-solid fa-calendar-days'></i> 작성일</dt><dd>{r['date']}</dd></dl></article></li>" for r in shop["reviews"]])
    
    json_ld_shop = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": shop["name"], "url": f"{DOMAIN}/shop_{s_id}.html", "telephone": shop["phone"], "priceRange": f"{shop['price']}원", "address": {"@type": "PostalAddress", "addressCountry": "KR", "addressLocality": shop["address"]}}

    shop_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{shop['name']} - {r_name} 출장마사지 및 스웨디시 | 숨결테라피</title>
    <meta name="description" content="{r_name} {shop['name']}에서 부드러운 스웨디시 출장마사지를 경험해보세요. 예약 및 문의: {shop['phone']}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{DOMAIN}/shop_{s_id}.html">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/shop.css">
    <script type="application/ld+json">{json.dumps(json_ld_shop, ensure_ascii=False)}</script>
</head>
<body>
    <header>
        <nav aria-label="상단 메뉴"><a class="back-move" href="javascript:history.back();"><span>뒤로 가기</span></a></nav>
        <h1><span>출장마사지 전문</span> {shop['name']}</h1>
    </header>
    <main>
        <section class="course"><h2><span aria-hidden="true">&gt;&gt;</span> 코스 안내</h2><section class="details"><ul>{course_html}</ul></section></section>
        <section class="masseur"><h2><span aria-hidden="true">&gt;&gt;</span> 관리사</h2><section class="profile"><ul>{manager_html}</ul></section></section>
        <section class="greeting"><h2><span aria-hidden="true">&gt;&gt;</span> 인사말</h2><div><p>{shop['address']}의 안식처 {shop['name']}가 여러분을 환영합니다. 한국관리사의 따뜻한 온기가 담긴 스웨디시로 깊은 이완과 회복의 순간을 경험해보세요.</p></div></section>
        <section class="mtonet">
            <h2><span aria-hidden="true">&gt;&gt;</span> 예약 문의</h2>
            <dl><dt>• <span>전화 번호</span></dt><dd><a href="tel:{shop['phone']}">{shop['phone']}</a></dd></dl>
        </section>
        <section class="working">
            <h2><span aria-hidden="true">&gt;&gt;</span> 영업 시간</h2>
            <dl><dt>• <span>영업 시간</span></dt><dd><strong>{shop['hours']}</strong></dd></dl>
        </section>
        <section class="direction">
            <h2><span aria-hidden="true">&gt;&gt;</span> 찾아오는 길</h2>
            <dl><dt>• <span>위치</span></dt><dd><strong>{shop['detail_address']} ({shop['station']})</strong></dd></dl>
        </section>
        <section id="review" class="review">
            <h2>이용 후기 <span>총 {len(shop['reviews'])}건</span></h2>
            <ol>{review_html if review_html else "<li>등록된 후기가 없습니다.</li>"}</ol>
        </section>
    </main>
</body>
</html>"""
    with open(f"{OUTPUT_DIR}/shop_{s_id}.html", "w", encoding="utf-8") as f:
        f.write(shop_html)
    sitemap_urls.append(f"{DOMAIN}/shop_{s_id}.html")

# (4) sitemap.xml & robots.txt
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
sitemap_content += '</urlset>'

with open(f"{OUTPUT_DIR}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
with open(f"{OUTPUT_DIR}/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)

print(f"✅ 네이버 실전 SEO 적용 완료: 총 {len(sitemap_urls)}개의 파일이 생성되었습니다.")