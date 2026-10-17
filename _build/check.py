"""Gate for the 4Levels site. Needs Playwright + Chromium (cloud workspace).
Serve the repo root first:  python3 -m http.server 8765   (from the repo root)
Then:                       python3 _build/check.py [--shots DIR]

Checks, per page: no sideways scroll at 320/375/414/768/1280 and phone landscape,
tap targets >= 24x24, no console errors, axe (WCAG 2.2 AA tags) at phone and desktop,
the phone menu opens full screen / traps focus / closes on Escape, every icon/OG/asset
URL in the head returns 200, the full house tag set, markdown mirrors and AI files exist.
"""
import asyncio, json, os, re, sys, urllib.request

BASE = "http://localhost:8765"
PAGES = ["/", "/services/", "/team/", "/clients/", "/contact/", "/404.html"]
AXE = "/tmp/fontdl/axe/package/axe.min.js"
SHOTS = sys.argv[sys.argv.index("--shots") + 1] if "--shots" in sys.argv else None
problems = []

def bad(msg):
    problems.append(msg); print("  ✗", msg)

def get(path):
    try:
        with urllib.request.urlopen(BASE + path) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except Exception as e:
        return getattr(e, "code", 0), "", b""

def static_checks():
    print("static files")
    for f in ["/llms.txt", "/llms-full.txt", "/agents.md", "/robots.txt", "/sitemap.xml", "/site.webmanifest", "/favicon.ico"]:
        s, _, b = get(f)
        if s != 200: bad(f"{f} -> {s}")
        if f in ("/llms.txt", "/llms-full.txt", "/agents.md") and b"## Site credits" not in b: bad(f"{f} missing Site credits")
    for p in PAGES[:-1]:
        s, _, b = get(p + "index.md")
        if s != 200 or b"optimized_by:" not in b: bad(f"{p}index.md missing or no front matter")
    _, _, robots = get("/robots.txt")
    if not robots.startswith(b"# AI search optimization (GEO)"): bad("robots.txt credit not first line")
    _, _, sm = get("/sitemap.xml")
    if b"<!-- AI search optimization (GEO)" not in sm.split(b"\n")[1]: bad("sitemap credit not line 2")
    for p in PAGES:
        s, _, b = get(p); h = b.decode("utf-8", "ignore")
        if "[" in re.sub(r"<script.*?</script>", "", h, flags=re.S) and re.search(r'content="[^"]*\[', h): bad(f"{p} bracket placeholder in meta")
        need = ['property="og:image"', 'og:image:width', 'og:image:alt', 'twitter:card', 'twitter:image:alt', 'rel="manifest"',
                'name="theme-color"', 'apple-touch-icon', 'rel="canonical"', 'name="DC.language"', 'GEO Optimization by',
                '<!-- AI search optimization (GEO)', '<html lang="en">', 'class="skip"', 'id="main"']
        if p != "/404.html": need.append('type="text/markdown"')
        for n in need:
            if n not in h: bad(f"{p} missing {n}")
        if p == "/" and '"Generative Engine Optimization (GEO)"' not in h: bad("home missing AI Syndicate schema block")
        for u in set(re.findall(r'(?:href|src|content)="(?:https://4-levels\.vercel\.app)?(/(?:assets|favicon|site\.web)[^"]*)"', h)):
            st, ct, _ = get(u.split(" ")[0])
            if st != 200: bad(f"{p} asset {u} -> {st}")
        if len(re.findall(r"<h1[ >]", h)) != 1: bad(f"{p} h1 count != 1")
        for m in re.findall(r'<meta name="description" content="([^"]*)"', h):
            if len(m) > 160: bad(f"{p} description {len(m)} chars")

async def run():
    from playwright.async_api import async_playwright
    axe_src = open(AXE).read()
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        for w, h, mobile in [(320, 640, True), (375, 812, True), (414, 896, True), (768, 1024, True), (844, 390, True), (1280, 800, False), (1440, 900, False)]:
            ctx = await b.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
            page = await ctx.new_page()
            errs = []
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errs.append(str(e)))
            for p in PAGES:
                await page.goto(BASE + p, wait_until="networkidle")
                await page.wait_for_timeout(400)
                sw = await page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                if sw[0] > sw[1]: bad(f"{w}x{h} {p} sideways scroll {sw}")
                small = await page.evaluate("""() => [...document.querySelectorAll('a,button,input,select,textarea')].filter(e=>{
                    const r=e.getBoundingClientRect(); const st=getComputedStyle(e);
                    if(!r.width||st.visibility==='hidden'||e.closest('[hidden]')||e.closest('.hp')) return false;
                    if(e.closest('p') && e.tagName==='A' && !e.classList.contains('btn')) return false; /* inline text links are exempt */
                    return r.width<24||r.height<24 }).map(e=>e.outerHTML.slice(0,80))""")
                for s in small: bad(f"{w} {p} small target {s}")
                if w in (375, 1440):
                    await page.evaluate(axe_src)
                    res = await page.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}).then(r=>r.violations.map(v=>v.id+': '+v.nodes.length+' '+v.nodes[0].target.join(' ')))")
                    for v in res: bad(f"axe {w} {p} {v}")
                if SHOTS and w in (375, 768, 1440):
                    H = await page.evaluate("document.documentElement.scrollHeight")
                    y = 0; i = 0
                    while y < H and i < 14:
                        await page.evaluate(f"window.scrollTo(0,{y})"); await page.wait_for_timeout(350)
                        name = p.strip("/").replace("/", "_").replace(".html", "") or "home"
                        await page.screenshot(path=f"{SHOTS}/{name}-{w}-{i:02d}.png")
                        y += h; i += 1
            for e in errs: bad(f"console {w}: {e[:160]}")
            await ctx.close()
        # phone menu behaviour
        ctx = await b.new_context(viewport={"width": 375, "height": 812}, is_mobile=True, has_touch=True)
        page = await ctx.new_page(); await page.goto(BASE + "/services/")
        await page.tap("#menuBtn"); await page.wait_for_timeout(200)
        box = await page.evaluate("(()=>{const r=document.getElementById('menu').getBoundingClientRect();return [r.width,r.height,innerWidth,innerHeight]})()")
        if box[0] < box[2] or box[1] < box[3]: bad(f"menu not full screen {box}")
        focus = await page.evaluate("document.activeElement.id")
        if focus != "menuClose": bad(f"menu focus went to {focus}")
        for _ in range(12): await page.keyboard.press("Tab")
        inside = await page.evaluate("document.getElementById('menu').contains(document.activeElement)")
        if not inside: bad("focus escaped the open menu")
        await page.keyboard.press("Escape"); await page.wait_for_timeout(100)
        st = await page.evaluate("[document.getElementById('menu').hidden, document.activeElement.id, document.body.classList.contains('menu-open')]")
        if st != [True, "menuBtn", False]: bad(f"escape close state {st}")
        await page.set_viewport_size({"width": 844, "height": 390}); await page.tap("#menuBtn"); await page.wait_for_timeout(200)
        sc = await page.evaluate("(()=>{const m=document.getElementById('menu');return [m.scrollHeight>m.clientHeight?'scrolls':'fits', getComputedStyle(m).overflowY]})()")
        print("  landscape menu:", sc)
        # form guard: empty submit shows error, no network call
        await page.goto(BASE + "/contact/")
        await page.click("#sendBtn"); await page.wait_for_timeout(150)
        t = await page.evaluate("[document.getElementById('formMsg').textContent, document.activeElement.id, document.getElementById('f-name').getAttribute('aria-invalid')]")
        if "name" not in t[0].lower() or t[1] != "f-name": bad(f"form guard {t}")
        # wire draws on scroll
        await page.set_viewport_size({"width": 1440, "height": 900}); await page.goto(BASE + "/")
        await page.evaluate("document.getElementById('levelsTrack').scrollIntoView({block:'center'})"); await page.wait_for_timeout(1500)
        lit = await page.evaluate("document.querySelectorAll('.lvl.lit').length")
        print("  wire: cards lit mid-scroll =", lit)
        if lit == 0: bad("wire never lit a card")
        # reduced motion: everything visible
        ctx2 = await b.new_context(viewport={"width": 1280, "height": 800}, reduced_motion="reduce")
        pg = await ctx2.new_page(); await pg.goto(BASE + "/")
        hid = await pg.evaluate("[...document.querySelectorAll('.reveal')].filter(e=>getComputedStyle(e).opacity==='0').length")
        if hid: bad(f"reduced motion: {hid} reveal blocks invisible")
        await b.close()

static_checks()
asyncio.run(run())
print("\nPROBLEMS:", len(problems))
sys.exit(1 if problems else 0)
