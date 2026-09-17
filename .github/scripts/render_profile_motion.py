#!/usr/bin/env python3
import datetime as dt, html, json, os, sys, urllib.request
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "miguelalmeida0")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/profile")
OUT.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    ("01", "SECOND VOICE", "REWRITE · PRIVACY · ROUTING"),
    ("02", "FLOW", "VOICE · INTERACTION · STATE"),
    ("03", "LEU", "NATIVE IOS · LEARNING · PDF"),
    ("04", "VIGIA", "GEOSPATIAL · INCIDENTS · POSTGIS"),
]
THEMES = {
    "light": dict(bg="#FAF9F6", text="#171717", muted="#6B6B67", line="#C9C5BB", accent="#B7872F"),
    "dark": dict(bg="#0D1117", text="#F2F0EB", muted="#9EA3A8", line="#30363D", accent="#D3A84E"),
}

def esc(s): return html.escape(s, quote=True)

def hero(theme):
    c = THEMES[theme]
    xs = [100, 330, 500, 650]
    groups = []
    for i, ((num, name, meta), x) in enumerate(zip(PROJECTS, xs), start=1):
        groups.append(f'''
        <g class="project p{i}" transform="translate({x} 194)">
          <text class="num" x="0" y="0">{num}</text>
          <text class="pname" x="32" y="0">{esc(name)}</text>
          <text class="pmeta" x="32" y="19">{esc(meta)}</text>
        </g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="250" viewBox="0 0 1000 250" role="img" aria-labelledby="title desc">
<title id="title">Miguel Almeida — Frontend and Design Engineer</title>
<desc id="desc">Animated editorial header highlighting Second Voice, Flow, Leu and VIGIA.</desc>
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
.eyebrow{{fill:{c["accent"]};font-size:12px;font-weight:700;letter-spacing:3.1px}}
.name{{fill:{c["text"]};font-size:42px;font-weight:760;letter-spacing:-1.4px}}
.role{{fill:{c["muted"]};font-size:17px;font-weight:520}}
.small{{fill:{c["muted"]};font-size:11px;font-weight:650;letter-spacing:1.7px}}
.hair{{stroke:{c["line"]};stroke-width:1}}
.accent{{stroke:{c["accent"]};stroke-width:2;stroke-linecap:round}}
.num{{fill:{c["accent"]};font-size:10px;font-weight:750;letter-spacing:1.4px}}
.pname{{fill:{c["text"]};font-size:12px;font-weight:730;letter-spacing:.5px}}
.pmeta{{fill:{c["muted"]};font-size:8.5px;font-weight:620;letter-spacing:.7px}}
.project{{opacity:.42;animation:focus 12s infinite}}
.p2{{animation-delay:3s}} .p3{{animation-delay:6s}} .p4{{animation-delay:9s}}
.signal{{fill:{c["accent"]};animation:pulse 2.6s ease-in-out infinite}}
.intro{{animation:intro 1s ease both}}
@keyframes focus{{0%,19%,100%{{opacity:.42}}5%,14%{{opacity:1}}}}
@keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
@keyframes intro{{from{{opacity:0;transform:translateY(7px)}}to{{opacity:1;transform:none}}}}
@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}.project{{opacity:.82}}}}
</style>
<defs><filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2"/></filter></defs>
<rect width="1000" height="250" rx="18" fill="{c["bg"]}"/>
<g class="intro">
  <circle class="signal" cx="87" cy="39" r="3"/>
  <text class="eyebrow" x="103" y="43">MIGUEL ALMEIDA</text>
  <text class="name" x="84" y="102">Frontend &amp; Design Engineer</text>
  <text class="role" x="86" y="132">AI product interfaces · Berlin</text>
  <text class="small" x="790" y="43">SELECTED SYSTEMS</text>
  <line class="hair" x1="86" y1="158" x2="914" y2="158"/>
  <line class="accent" x1="86" y1="158" x2="180" y2="158"/>
  {''.join(groups)}
  <line class="hair" x1="86" y1="225" x2="914" y2="225"/>
  <text class="small" x="86" y="242">INTERACTION STATE · ACCESSIBILITY · SECURITY BOUNDARIES · END-TO-END VERIFICATION</text>
  <circle r="4" cy="158" fill="{c["accent"]}" filter="url(#soft)">
    <animate attributeName="cx" values="86;914;86" dur="12s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values=".2;1;.2" dur="12s" repeatCount="indefinite"/>
  </circle>
</g>
</svg>'''

def contribution_days():
    if not TOKEN:
        return []
    query = "query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query":query,"variables":{"login":USERNAME}}).encode(),
        headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json","User-Agent":"profile-motion"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [(d["date"], int(d["contributionCount"])) for w in weeks for d in w["contributionDays"]][-364:]

def weekly_counts(days):
    vals = [sum(v for _, v in days[i:i+7]) for i in range(0, len(days), 7)]
    vals = vals[-52:]
    return [0]*(52-len(vals)) + vals

def activity(theme, weekly):
    c = THEMES[theme]
    maxv = max(max(weekly), 1)
    bars = []
    for i, value in enumerate(weekly):
        n = value / maxv
        h = 5 + n*42
        x = 86 + i*15.45
        y = 86 - h
        delay = (i*0.045) % 2.4
        opacity = .28 + n*.58
        bars.append(f'<rect class="bar" x="{x:.1f}" y="{y:.1f}" width="7.2" height="{h:.1f}" rx="3.6" opacity="{opacity:.2f}" style="animation-delay:{delay:.2f}s"/>')
    today = dt.date.today().isoformat()
    total = sum(weekly)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="128" viewBox="0 0 1000 128" role="img" aria-labelledby="title desc">
<title id="title">Miguel Almeida build pulse</title>
<desc id="desc">Animated 52-week GitHub contribution ribbon.</desc>
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
.label{{fill:{c["text"]};font-size:12px;font-weight:730;letter-spacing:1.4px}}
.meta{{fill:{c["muted"]};font-size:10px;font-weight:600;letter-spacing:.7px}}
.bar{{fill:{c["text"]};transform-box:fill-box;transform-origin:center bottom;animation:breathe 2.8s ease-in-out infinite}}
.track{{stroke:{c["line"]};stroke-width:1}}
@keyframes breathe{{0%,100%{{transform:scaleY(.94);opacity:.55}}50%{{transform:scaleY(1.06);opacity:1}}}}
@media(prefers-reduced-motion:reduce){{.bar{{animation:none}}}}
</style>
<defs><filter id="soft" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="2"/></filter></defs>
<rect width="1000" height="128" rx="16" fill="{c["bg"]}"/>
<text class="label" x="86" y="29">BUILD PULSE · 52 WEEKS</text>
<text class="meta" x="914" y="29" text-anchor="end">UPDATED {today} · {total} CONTRIBUTIONS</text>
<line class="track" x1="86" y1="91" x2="914" y2="91"/>
{''.join(bars)}
<circle cy="91" r="4" fill="{c["accent"]}" filter="url(#soft)">
  <animate attributeName="cx" values="86;914" dur="9s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;1;0" dur="9s" repeatCount="indefinite"/>
</circle>
<text class="meta" x="86" y="113">RECENT ACTIVITY, GENERATED FROM GITHUB · NO THIRD-PARTY STATS SERVICE</text>
</svg>'''

weeks = weekly_counts(contribution_days())
for theme in ("light","dark"):
    (OUT/f"hero-{theme}.svg").write_text(hero(theme), encoding="utf-8")
    (OUT/f"activity-{theme}.svg").write_text(activity(theme, weeks), encoding="utf-8")
print("generated", OUT)
