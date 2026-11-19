// 네이버 서치어드바이저 및 SEO 메타태그, JSON-LD를 동적으로 삽입하는 스크립트
function initSEO(pageData) {
    document.title = pageData.title;

    const metaTags = {
        "description": pageData.description,
        "og:title": pageData.title,
        "og:description": pageData.description,
        "og:url": pageData.url,
        "og:type": "website",
        "naver-site-verification": "발급받은_네이버_인증키_입력"
    };

    for (const [key, value] of Object.entries(metaTags)) {
        let meta = document.createElement('meta');
        if (key.startsWith('og:')) {
            meta.setAttribute('property', key);
        } else {
            meta.setAttribute('name', key);
        }
        meta.content = value;
        document.head.appendChild(meta);
    }

    const canonical = document.createElement('link');
    canonical.rel = 'canonical';
    canonical.href = pageData.url;
    document.head.appendChild(canonical);

    if (pageData.jsonLd) {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.text = JSON.stringify(pageData.jsonLd);
        document.head.appendChild(script);
    }
}