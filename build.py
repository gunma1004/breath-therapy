import os
import json
from datetime import datetime

# 1. 사이트 기본 설정 및 데이터
DOMAIN = "https://breath-therapy.netlify.app"
OUTPUT_DIR = "./dist"

regions = [
    {"id": "gangnam", "name": "강남구"},
    {"id": "seocho", "name": "서초구"},
    {"id": "busan", "name": "부산광역시"},
    {"id": "suwon", "name": "경기 수원"}
]

shops = [
    {"id": "queens", "name": "퀸즈홈테라피", "phone": "0507-1280-3296"},
    {"id": "korean_beauty", "name": "한국미인테라피", "phone": "0507-1280-3140"},
    {"id": "tonight", "name": "오늘밤테라피", "phone": "0507-1280-3199"},
    {"id": "juju", "name": "주주테라피", "phone": "0507-1280-3197"},
    {"id": "joy", "name": "기쁨테라피", "phone": "0507-1280-3183"},
    {"id": "beauty_club", "name": "미인클럽테라피", "phone": "0507-1280-3180"}
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sitemap_urls = []
today = datetime.now().strftime("%Y-%m-%d")

# 2. 메인 페이지 생성 (디자인 적용 및 출장마사지 키워드 제외)
main_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>스웨디시·아로마·타이 마사지샵 추천｜전국 지역별 검색 - 숨결테라피</title>
    <meta name="description" content="숨결테라피에서 스웨디시, 아로마, 타이 마사지샵을 지역별로 검색해보세요.">
    <!-- 원본 사이트의 디자인(CSS) 및 폰트 불러오기 -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.0.5/swiper-bundle.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/index.css">
</head>
<body>
    <header>
        <h1><a href="/">숨결테라피</a></h1>
        <p>스웨디시, 아로마, 타이 마사지샵 추천과 전국 지역별 검색</p>
        <p>스웨디시, 아로마, 타이 마사지샵을 전국 지역별로 검색해보세요. 상세 정보와 이용 후기를 참고해 원하는 업체를 선택할 수 있습니다.</p>
    </header>
    
    <nav aria-label="주요 메뉴">
        <section>
            <h2>지역별 마사지샵 검색</h2>
            <ul>
                <li><a href="region_gangnam.html"><span aria-hidden="true">11.</span> 서울 강남구 <span>마사지샵</span></a></li>
                <li><a href="region_seocho.html"><span aria-hidden="true">12.</span> 서울 서초구 <span>마사지샵</span></a></li>
                <li><a href="region_busan.html"><span aria-hidden="true">31.</span> 부산광역시 <span>마사지샵</span></a></li>
                <li><a href="region_suwon.html"><span aria-hidden="true">47.</span> 경기 수원 <span>마사지샵</span></a></li>
            </ul>
        </section>
    </nav>

    <main>
        <section>
            <h2>가장 주목 받는 테라피샵</h2>
            <p>&gt;&gt; 내가 찾고 싶은 마사지샵</p>
            <div style="padding: 20px;">
                <ul style="list-style:none; padding:0; margin:0; line-height:2.5;">
                    <li><a href="shop_queens.html" style="font-size:16px; font-weight:bold;">퀸즈홈테라피</a> (0507-1280-3296)</li>
                    <li><a href="shop_korean_beauty.html" style="font-size:16px; font-weight:bold;">한국미인테라피</a> (0507-1280-3140)</li>
                    <li><a href="shop_tonight.html" style="font-size:16px; font-weight:bold;">오늘밤테라피</a> (0507-1280-3199)</li>
                    <li><a href="shop_juju.html" style="font-size:16px; font-weight:bold;">주주테라피</a> (0507-1280-3197)</li>
                    <li><a href="shop_joy.html" style="font-size:16px; font-weight:bold;">기쁨테라피</a> (0507-1280-3183)</li>
                    <li><a href="shop_beauty_club.html" style="font-size:16px; font-weight:bold;">미인클럽테라피</a> (0507-1280-3180)</li>
                </ul>
            </div>
        </section>
    </main>
    
    <footer>
        <p>
            <small>당사는 통신 판매 중개자로서 서비스 제공의 당사자가 아니며, 입점 업체가 등록한 콘텐츠에 대해서 일체 책임을 지지 않습니다.</small>
            <small>COPYRIGHT breath-therapy.netlify.app ALL RIGHTS RESERVED.</small>
        </p>
    </footer>
</body>
</html>"""

with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(main_html)
sitemap_urls.append(f"{DOMAIN}/index.html")

# 3. 지역별 서브 페이지 자동 생성 (출장마사지 키워드 포함)
for region in regions:
    r_id = region["id"]
    r_name = region["name"]
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{r_name} 출장마사지 추천",
        "itemListElement": [{"@type": "ListItem", "position": i+1, "url": f"{DOMAIN}/shop_{shop['id']}.html"} for i, shop in enumerate(shops)]
    }
    
    # 지역 페이지에도 CSS 디자인 적용
    region_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>{r_name} 출장마사지 추천 | 스웨디시·아로마 검색 - 숨결테라피</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/list.css">
    <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
    <header>
        <nav aria-label="상단 메뉴"><a href="index.html"><span>홈으로 가기</span><i class="fa-solid fa-chevron-left"></i></a></nav>
        <h1>{r_name} <span>출장마사지 목록</span></h1>
    </header>
    <main>
        <section class="list">
            <ol>
                <li class="card">
                    <div class="primary" style="padding:20px;">
                        <h3><a href="shop_queens.html"><strong>퀸즈홈테라피</strong></a></h3>
                        <p><i class="fa-solid fa-phone"></i> <a href="tel:0507-1280-3296">0507-1280-3296</a></p>
                    </div>
                </li>
                <!-- 추가 업체 리스트 생략 -->
            </ol>
        </section>
    </main>
</body>
</html>"""
    
    with open(f"{OUTPUT_DIR}/region_{r_id}.html", "w", encoding="utf-8") as f:
        f.write(region_html)
    sitemap_urls.append(f"{DOMAIN}/region_{r_id}.html")

# 4. 샵 상세 페이지 자동 생성
for shop in shops:
    s_id = shop["id"]
    s_name = shop["name"]
    s_phone = shop["phone"]
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": s_name,
        "url": f"{DOMAIN}/shop_{s_id}.html",
        "telephone": s_phone
    }
    
    # 샵 상세 페이지에도 CSS 디자인 적용
    shop_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>{s_name} - 전국 출장마사지 및 스웨디시 | 숨결테라피</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/global.css">
    <link rel="stylesheet" href="https://www.hi-massage.kr/assets/stylesheets/shop.css">
    <script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>
</head>
<body>
    <header>
        <nav aria-label="상단 메뉴"><a class="back-move" href="javascript:history.back();"><span>뒤로 가기</span><i class="fa-solid fa-chevron-left"></i></a></nav>
        <h1><span>출장마사지 전문</span> {s_name}</h1>
    </header>
    <main>
        <section class="mtonet">
            <h2><span aria-hidden="true">&gt;&gt;</span> 예약 문의</h2>
            <dl>
                <dt>• <span>전화 번호</span></dt>
                <dd><a href="tel:{s_phone}">{s_phone}</a></dd>
            </dl>
        </section>
    </main>
</body>
</html>"""
    
    with open(f"{OUTPUT_DIR}/shop_{s_id}.html", "w", encoding="utf-8") as f:
        f.write(shop_html)
    sitemap_urls.append(f"{DOMAIN}/shop_{s_id}.html")

# 5. sitemap.xml & robots.txt 생성
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
sitemap_content += '</urlset>'

with open(f"{OUTPUT_DIR}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
with open(f"{OUTPUT_DIR}/robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_content)

print(f"✅ 화려한 디자인이 적용된 HTML 파일들이 생성되었습니다.")