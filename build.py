import os
import json
from datetime import datetime

# 1. 사이트 기본 설정 및 데이터
DOMAIN = "https://breath-therapy.netlify.app"
OUTPUT_DIR = "./dist"  # 생성된 파일이 저장될 폴더

regions = [
    {"id": "gangnam", "name": "강남구"},
    {"id": "seocho", "name": "서초구"},
    {"id": "jangchung", "name": "장충동"}, # 지역 키워드 예시
    {"id": "busan", "name": "부산광역시"}
]

shops = [
    {"id": "queens", "name": "퀸즈홈테라피", "phone": "0507-1280-3296"},
    {"id": "korean_beauty", "name": "한국미인테라피", "phone": "0507-1280-3140"},
    {"id": "tonight", "name": "오늘밤테라피", "phone": "0507-1280-3199"},
    {"id": "juju", "name": "주주테라피", "phone": "0507-1280-3197"},
    {"id": "joy", "name": "기쁨테라피", "phone": "0507-1280-3183"},
    {"id": "beauty_club", "name": "미인클럽테라피", "phone": "0507-1280-3180"}
]

# 출력 폴더가 없으면 생성
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

sitemap_urls = []
today = datetime.now().strftime("%Y-%m-%d")

# 2. 메인 페이지 생성 (출장마사지 키워드 제외)
main_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>숨결테라피 - 스웨디시·아로마·타이 전국 지역별 검색</title>
    <meta name="description" content="숨결테라피에서 스웨디시, 아로마, 타이 테라피 샵을 전국 지역별로 검색해보세요.">
</head>
<body>
    <h1>숨결테라피 메인</h1>
    <p>지역별 검색 및 제휴 업체 안내</p>
</body>
</html>"""

with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
    f.write(main_html)
sitemap_urls.append(f"{DOMAIN}/index.html")


# 3. 지역별 서브 페이지 자동 생성 (출장마사지 키워드 포함)
for region in regions:
    r_id = region["id"]
    r_name = region["name"]
    
    # JSON-LD 구조화 데이터 동적 생성
    json_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"{r_name} 출장마사지 추천",
        "itemListElement": [{"@type": "ListItem", "position": i+1, "url": f"{DOMAIN}/shop_{shop['id']}.html"} for i, shop in enumerate(shops)]
    }
    
    region_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>{r_name}출장마사지 추천 | 스웨디시·아로마 검색 - 숨결테라피</title>
    <meta name="description" content="숨결테라피에서 {r_name} 지역의 출장마사지, 스웨디시, 아로마 샵을 검색해보세요.">
    <script type="application/ld+json">
    {json.dumps(json_ld, ensure_ascii=False, indent=4)}
    </script>
</head>
<body>
    <h1>{r_name} 출장마사지 목록</h1>
</body>
</html>"""
    
    with open(f"{OUTPUT_DIR}/region_{r_id}.html", "w", encoding="utf-8") as f:
        f.write(region_html)
    sitemap_urls.append(f"{DOMAIN}/region_{r_id}.html")


# 4. 샵 상세 페이지 자동 생성 (출장마사지 키워드 포함)
for shop in shops:
    s_id = shop["id"]
    s_name = shop["name"]
    s_phone = shop["phone"]
    
    json_ld = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": s_name,
        "url": f"{DOMAIN}/shop_{s_id}.html",
        "telephone": s_phone,
        "priceRange": "₩₩"
    }
    
    shop_html = f"""<!doctype html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <title>{s_name} - 전국 출장마사지 및 스웨디시 | 숨결테라피</title>
    <meta name="description" content="{s_name}에서 부드러운 스웨디시 출장마사지를 경험하며 여유를 더해보세요. 예약문의: {s_phone}">
    <script type="application/ld+json">
    {json.dumps(json_ld, ensure_ascii=False, indent=4)}
    </script>
</head>
<body>
    <h1>{s_name} 출장마사지 전문</h1>
    <p>예약: {s_phone}</p>
</body>
</html>"""
    
    with open(f"{OUTPUT_DIR}/shop_{s_id}.html", "w", encoding="utf-8") as f:
        f.write(shop_html)
    sitemap_urls.append(f"{DOMAIN}/shop_{s_id}.html")


# 5. sitemap.xml 자동 생성
sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_content += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n  </url>\n"
sitemap_content += '</urlset>'

with open(f"{OUTPUT_DIR}/sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print(f"✅ 총 {len(sitemap_urls)}개의 HTML 파일과 sitemap.xml이 '{OUTPUT_DIR}' 폴더에 성공적으로 생성되었습니다.")