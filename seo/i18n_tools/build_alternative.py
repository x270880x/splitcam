# -*- coding: utf-8 -*-
"""Собирает страницу /alternatives/<rival>/ по шаблону alternatives/obs/.
Запуск:  python3 seo/i18n_tools/build_alternative.py <slug> <модуль_с_COPY>
Пример:  python3 seo/i18n_tools/build_alternative.py manycam manycam_copy
"""
import re, json, os, sys, importlib
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC  = os.path.join(ROOT, "alternatives/obs/index.html")

def build(slug, C, base="alternatives"):
    URL = (f"https://splitcam.com/{base}/{slug}" if base else f"https://splitcam.com/{slug}")
    h = open(SRC, encoding="utf-8").read()
    esc = lambda s: s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
    b = h.find("<body>"); bc = h.find('<div class="breadcrumbs">'); ft = h.find("<footer")
    assert 0 < b < bc < ft, "структура шаблона неожиданная"
    head, chrome1, chrome2 = h[:b], h[b:bc], h[ft:]

    def setm(pat, val, s):
        s2, n = re.subn(pat, lambda m: m.group(1)+val+m.group(3), s, count=1, flags=re.S)
        assert n == 1, f"мета не заменена: {pat[:40]}"
        return s2
    for pat, val in ((r'(<title>)(.*?)(</title>)', esc(C["title"])),
                     (r'(<meta name="description" content=")(.*?)(")', esc(C["description"])),
                     (r'(<meta name="keywords" content=")(.*?)(")', esc(C["keywords"])),
                     (r'(<link rel="canonical" href=")(.*?)(")', URL),
                     (r'(<meta property="og:url" content=")(.*?)(")', URL),
                     (r'(<meta property="og:title" content=")(.*?)(")', esc(C["title"])),
                     (r'(<meta property="og:description" content=")(.*?)(")', esc(C["description"])),
                     (r'(<meta name="twitter:title" content=")(.*?)(")', esc(C["title"])),
                     (r'(<meta name="twitter:description" content=")(.*?)(")', esc(C["description"]))):
        head = setm(pat, val, head)
    # локалей у новой страницы ещё нет: оставляем только self + x-default.
    # Иначе страница объявляет своим переводом чужую (шаблонную) страницу.
    head = re.sub(r'[ \t]*<link rel="alternate" hreflang="(?!en"|x-default")[^"]+" href="[^"]*"\s*/?>\n?', '', head)
    # og-картинка: шаблон OBS нёс og-obs.png — на чужой странице это чужое превью
    head = re.sub(r'(og:image" content="https://splitcam\.com/assets/)[^"]+', r'\1' + C.get("og", "og-cover.png"), head)
    head = re.sub(r'(twitter:image" content="https://splitcam\.com/assets/)[^"]+', r'\1' + C.get("og", "og-cover.png"), head)
    head = re.sub(r'(<link rel="alternate" hreflang="(?:en|x-default)" href=")[^"]*(")',
                  r'\g<1>'+URL+r'\g<2>', head)

    strip = lambda s: re.sub(r'\s+',' ', re.sub('<[^>]*>','',s)).strip()
    graph = {"@context":"https://schema.org","@graph":[
      {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"SplitCam","item":"https://splitcam.com/"},
        {"@type":"ListItem","position":2,"name":C.get("crumb2","Alternatives"),
         "item":C.get("crumb2_url","https://splitcam.com/alternatives")},
        {"@type":"ListItem","position":3,"name":C.get("crumb3",f'{C["rival"]} alternative'),"item":URL}]},
      {"@type":"SoftwareApplication","name":"SplitCam",
       "operatingSystem":"Windows 10, Windows 11, macOS 13",
       "applicationCategory":"MultimediaApplication","description":strip(C["description"]),
       "offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"url":URL},
      {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":strip(q),
        "acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in C["faq"]]}]}
    head = re.sub(r'<script type="application/ld\+json">.*?</script>',
      lambda _: '<script type="application/ld+json">\n'+json.dumps(graph,ensure_ascii=False,indent=2)+'\n</script>',
      head, count=1, flags=re.S)

    cards = lambda lst: "\n".join(
      f'      <div class="reason">\n        <h3>{t}</h3>\n        <p>{p}</p>\n      </div>' for t,p in lst)
    rows = "\n".join(f'      <tr><td>{f}</td><td class="{sc}">{sv}</td><td class="{rc}">{rv}</td></tr>'
                     for f,sc,sv,rc,rv in C["rows"])
    qa = "\n".join(f"        <li>{x}</li>" for x in C["qa"])
    faq = "\n".join(f'      <details class="faq-item">\n        <summary>{q}</summary>\n        <p>{a}</p>\n      </details>'
                    for q,a in C["faq"])
    badges = "".join(f'<span class="h-badge">{x}</span>' for x in C["badges"])
    rel = "\n".join(f'''    <a class="related-card" href="{u}">
      <span class="eyebrow">{e}</span>
      <h4>{t}</h4>
      <p>{p}</p>
    </a>''' for u,e,t,p in C["related"])

    BODY = f'''<!-- BREADCRUMBS -->
<div class="breadcrumbs">
  <a href="https://splitcam.com/">SplitCam</a><span class="sep">/</span><a href="{C.get("crumb2_url","https://splitcam.com/alternatives")}">{C.get("crumb2","Alternatives")}</a><span class="sep">/</span><span>{C.get("crumb3_short", C["rival"])}</span>
</div>

<!-- HERO -->
<section class="hero">
  <div class="hero-glow"></div>
  <span class="eyebrow">{C["eyebrow"]}</span>
  <h1 class="h1">{C["h1_pre"]}<span class="accent">{C["h1_accent"]}</span>{C["h1_post"]}</h1>
  <p class="sub">{C["sub"]}</p>
  <div class="hero-cta">
    <a href="https://splitcam.com/download" class="btn-primary btn-lg" data-dl-primary>⬇ Free Download</a>
    <a href="#compare" class="btn-ghost btn-lg">See the table ↓</a>
  </div>
  <div class="hero-badges">{badges}</div>
</section>

<!-- QUICK ANSWER -->
<div class="quick-answer">
  <div class="qa-box">
    <div class="qa-h">{C["qa_h"]}</div>
    <div class="qa-text"><ol>
{qa}
    </ol></div>
  </div>
</div>

<!-- SECTION 1 -->
<section class="section">
  <h2 class="sec-h">{C["s1_h"]}</h2>
  <p class="sec-p">{C["s1_p"]}</p>
  <div class="reasons-grid">
{cards(C["s1_cards"])}
  </div>
</section>

<!-- SECTION 2 -->
<section class="section">
  <h2 class="sec-h">{C["s2_h"]}</h2>
  <p class="sec-p">{C["s2_p"]}</p>
  <div class="reasons-grid">
{cards(C["s2_cards"])}
  </div>
</section>

<!-- HONEST: WHERE THE RIVAL WINS -->
<section class="section">
  <h2 class="sec-h">{C["win_h"]}</h2>
  <p class="sec-p">{C["win_p"]}</p>
</section>

<!-- COMPARE -->
<section class="section" id="compare">
  <h2 class="sec-h">{C["cmp_h"]}</h2>
  <p class="sec-p">{C["cmp_p"]}</p>
  <div class="table-wrap"><table class="compare-table">
    <thead>
      <tr>{"".join(f"<th>{c}</th>" for c in C.get("cols", ["Feature", "SplitCam", C["rival"]]))}</tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table></div>
</section>

<!-- FAQ -->
<section class="section">
  <h2 class="sec-h">{C.get("faq_h", C["rival"] + " alternative FAQ")}</h2>
  <div class="faq-list">
{faq}
  </div>
</section>

<!-- RELATED -->
<div class="related">
  <h3 style="font-size:18px;font-weight:700;margin-bottom:6px">Related guides</h3>
  <div class="related-grid">
{rel}
  </div>
</div>

<!-- CTA -->
<section class="cta-block">
  <h2>{C["cta_h"]}</h2>
  <p>{C["cta_p"]}</p>
  <a href="https://splitcam.com/download" class="btn-primary btn-lg" data-dl-primary>⬇ Free Download</a>
</section>

'''
    dst = os.path.join(ROOT, base, slug) if base else os.path.join(ROOT, slug)
    os.makedirs(dst, exist_ok=True)
    out = head + chrome1 + BODY + chrome2
    open(os.path.join(dst, "index.html"), "w", encoding="utf-8").write(out)
    return len(out)

if __name__ == "__main__":
    slug, mod = sys.argv[1], sys.argv[2]
    # третий аргумент — базовый путь; "" означает корень сайта
    base = sys.argv[3] if len(sys.argv) > 3 else "alternatives"
    sys.path.insert(0, os.path.join(ROOT, "seo", "i18n_tools"))   # copy-модули живут здесь
    sys.path.insert(0, os.environ.get("SCRATCH", "/tmp"))
    C = importlib.import_module(mod).COPY
    print(f"  {slug}: собрано {build(slug, C, base)} байт")
