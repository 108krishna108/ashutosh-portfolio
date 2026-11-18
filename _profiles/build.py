#!/usr/bin/env python3
"""Builds the role-specific portfolios from _profiles/data into <slug>/index.html.

Run from anywhere:  python _profiles/build.py
The Cyber Security portfolio is the hand-written site in the repository root.
"""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SLUGS = ["software-engineer", "ai-ml-engineer", "data-analyst", "sdet"]
FONTS = {
    "software-engineer": "family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700",
    "ai-ml-engineer": "family=Space+Grotesk:wght@400;500;600;700&family=Instrument+Sans:wght@400;500;600",
    "data-analyst": "family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Serif:wght@500;600",
    "sdet": "family=DM+Sans:wght@400;500;700&family=Fira+Code:wght@400;500;600",
}


def e(value):
    return html.escape(str(value), quote=True)


def joined(*parts):
    return " · ".join(e(x) for x in parts if x)


def rich(text):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", e(text))


def load(slug):
    shared = json.loads((HERE / "data" / "shared.json").read_text(encoding="utf-8"))
    profile = json.loads((HERE / "data" / f"{slug}.json").read_text(encoding="utf-8"))
    profile["shared"] = shared
    profile["cert_list"] = [shared["certificates"][key] for key in profile["certificates"]]
    for project in profile["projects"]:
        project.update(shared["projects"][project["key"]])
    return profile


def ext(url, label, cls=""):
    attr = f' class="{cls}"' if cls else ""
    return f'<a{attr} href="{e(url)}" target="_blank" rel="noopener noreferrer">{label}</a>'


def contacts(p):
    s = p["shared"]
    items = [{"kind": "Phone" if i == 0 else "Alternate Phone", "value": x["display"], "href": f'tel:{x["tel"]}', "out": False}
             for i, x in enumerate(s["phones"])]
    items += [{"kind": "Email" if i == 0 else "Alternate Email", "value": x, "href": f"mailto:{x}", "out": False}
              for i, x in enumerate(s["emails"])]
    items.append({"kind": "GitHub", "value": s["github"]["label"], "href": s["github"]["url"], "out": True})
    if p["show_linkedin"]:
        items.append({"kind": "LinkedIn", "value": s["linkedin"]["label"], "href": s["linkedin"]["url"], "out": True})
    if p["resume_url"]:
        items.append({"kind": "Resume", "value": "View full resume (PDF) ↗", "href": p["resume_url"], "out": True})
    return items


def contact_link(item, inner):
    if item["out"]:
        return ext(item["href"], inner)
    return f'<a href="{e(item["href"])}">{inner}</a>'


def resume_button(p, cls, label="View Resume"):
    return ext(p["resume_url"], label, cls) if p["resume_url"] else ""


def bullets(items):
    return "<ul>" + "".join(f"<li>{rich(x)}</li>" for x in items) + "</ul>"


def project_links(project, cls="plink"):
    return "".join(ext(x["url"], f'{e(x["label"])} <span aria-hidden="true">↗</span>', cls) for x in project["links"])


def chips(items, cls="chip"):
    return "".join(f'<span class="{cls}">{e(x)}</span>' for x in items)


def cert_cards(p):
    return "".join(
        ext(c["url"], f'<span class="cert-year">{e(c["year"])}</span><strong>{e(c["title"])}</strong>'
                      f'<span class="cert-issuer">{e(c["issuer"])}</span>'
                      f'<span class="cert-open">View certificate ↗</span>', "cert reveal")
        for c in p["cert_list"])


def edu_cards(p):
    return "".join(
        f'<div class="edu reveal"><span class="edu-years">{e(x["years"])}</span><strong>{e(x["degree"])}</strong>'
        f'<span>{e(x["school"])}</span><span class="edu-score">{e(x["score"])}</span></div>'
        for x in p["shared"]["education"])


def metric_cards(p):
    return "".join(
        f'<div class="metric reveal"><strong>{e(m["value"])}</strong><span>{e(m["label"])}</span></div>'
        for m in p["metrics"])


# --- Software Engineer: a code editor -------------------------------------------------------

def render_software(p):
    s = p["shared"]
    files = [("readme", "README.md", "md"), ("skills", "skills.json", "json"), ("experience", "experience.ts", "ts"),
             ("projects", "projects.tsx", "tsx"), ("certificates", "certificates.yml", "yml"),
             ("education", "education.md", "md"), ("contact", "contact.sh", "sh")]
    explorer = "".join(
        f'<a href="#{i}" data-spy data-file="{n}"><span class="ficon f-{k}">{k}</span>{n}</a>' for i, n, k in files)

    def head(section, name):
        return f'<div class="file-head"><span>src</span><span class="sep">›</span><b>{name}</b></div>'

    lines = ['<div class="l">{</div>']
    for i, group in enumerate(p["skills"]):
        comma = "," if i < len(p["skills"]) - 1 else ""
        values = '<span class="p">, </span>'.join(f'<span class="s">"{e(x)}"</span>' for x in group["items"])
        lines.append(f'<div class="l i1"><span class="k">"{e(group["name"])}"</span><span class="p">: [</span>'
                     f'{values}<span class="p">]{comma}</span></div>')
    lines.append('<div class="l">}</div>')

    jobs = ""
    for job in p["experience"]:
        diff = ""
        if job["achievements"]:
            rows = "".join(f'<div class="add"><span aria-hidden="true">+</span><p>{rich(x)}</p></div>'
                           for x in job["achievements"])
            diff = f'<div class="diff"><div class="diff-head">Key achievements</div>{rows}</div>'
        body = "".join(bullets(g["bullets"]) for g in job["groups"])
        jobs += (f'<article class="job reveal"><p class="comment">// {joined(job["dates"], job["location"])}</p>'
                 f'<h3>{e(job["role"])}</h3><p class="co">{e(job["company"])}</p>{body}{diff}</article>')

    projects = "".join(
        f'<article class="proj reveal"><div class="proj-tab"><span class="ficon f-tsx">tsx</span>{e(x["name"])}</div>'
        f'<div class="proj-body"><h3>{e(x["name"])}</h3>{bullets(x["bullets"])}'
        f'<div class="chips">{chips(x["tags"])}</div><div class="plinks">{project_links(x)}</div></div></article>'
        for x in p["projects"])

    shell = "".join(
        f'<div class="sh"><span class="prompt">$</span><span class="cmd">{e(c["kind"].lower())}</span>'
        f'{contact_link(c, e(c["value"]))}</div>' for c in contacts(p))

    return f"""
<div class="ide">
  <header class="titlebar">
    <span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>
    <span class="tb-name">ashutosh-kumar — portfolio</span>
    <span class="tb-status"><i aria-hidden="true"></i>{e(s["availability"])}</span>
    {resume_button(p, "tb-resume", "Resume")}
  </header>
  <div class="workspace">
    <nav class="explorer" aria-label="Sections">
      <p class="ex-title">Explorer</p>
      <p class="ex-root">portfolio / src</p>
      {explorer}
    </nav>
    <main class="editor">
      <section id="readme" class="doc hero">
        {head("readme", "README.md")}
        <div class="hero-grid">
          <div>
            <p class="comment"># {e(s["location"])}</p>
            <h1>{e(s["name"])}</h1>
            <p class="role">{e(p["title"])}<span class="caret" aria-hidden="true"></span></p>
            <div class="chips">{chips(p["tagline"])}</div>
            <p class="intro">{e(p["intro"])}</p>
            <div class="actions">{resume_button(p, "btn primary")}<a class="btn" href="#projects">Open projects</a><a class="btn" href="#contact">Contact</a></div>
          </div>
          <img class="avatar" src="../photo.png" alt="Portrait of {e(s["name"])}" width="240" height="240">
        </div>
        <div class="metrics">{metric_cards(p)}</div>
      </section>
      <section id="skills" class="doc">{head("skills", "skills.json")}<h2>Skills</h2><div class="code reveal">{"".join(lines)}</div></section>
      <section id="experience" class="doc">{head("experience", "experience.ts")}<h2>Experience</h2>{jobs}</section>
      <section id="projects" class="doc">{head("projects", "projects.tsx")}<h2>Projects</h2><div class="proj-grid">{projects}</div></section>
      <section id="certificates" class="doc">{head("certificates", "certificates.yml")}<h2>Certificates</h2><div class="cards">{cert_cards(p)}</div></section>
      <section id="education" class="doc">{head("education", "education.md")}<h2>Education</h2><div class="cards two">{edu_cards(p)}</div></section>
      <section id="contact" class="doc">{head("contact", "contact.sh")}<h2>Contact</h2><div class="shell reveal">{shell}<div class="sh"><span class="prompt">$</span><span class="cmd">location</span><span>{e(s["location"])}</span></div></div></section>
    </main>
  </div>
  <footer class="statusbar"><span>⎇ main</span><span id="current-file">README.md</span><span class="sb-right">© 2026 {e(s["name"])}</span></footer>
</div>"""


# --- AI/ML Engineer: a neural network and agent pipeline ------------------------------------

def render_ai(p):
    s = p["shared"]
    nav = "".join(f'<a href="#{i}" data-spy>{n}</a>' for i, n in
                  [("agent", "Agent"), ("model", "Model"), ("skills", "Skills"), ("experience", "Experience"),
                   ("projects", "Projects"), ("contact", "Contact")])
    steps = [("01", "Input", "Reads device-down alerts over IMAP"),
             ("02", "Tool calls", "Site directory · Manager lookup · Live weather API"),
             ("03", "LLM", "Drafts the notification with Gemini"),
             ("04", "Fallback", "Rule-based template when the LLM fails or times out")]
    flow = "".join(f'<li class="step reveal"><span class="step-no">{n}</span><strong>{t}</strong><span>{d}</span></li>'
                   for n, t, d in steps)
    stages = ["Labelled dataset", "TF-IDF features", "Logistic Regression", "15 tuning rounds", "FastAPI", "Chrome extension"]
    train = "".join(f'<li>{x}</li>' for x in stages)
    skills = "".join(
        f'<article class="skill reveal"><h3>{e(g["name"])}</h3><div class="chips">{chips(g["items"])}</div></article>'
        for g in p["skills"])
    jobs = ""
    for job in p["experience"]:
        wins = ""
        if job["achievements"]:
            wins = '<div class="wins"><h4>Key achievements</h4>' + bullets(job["achievements"]) + "</div>"
        jobs += (f'<article class="job reveal"><div class="job-meta"><span>{e(job["dates"])}</span><span>{e(job["location"])}</span></div>'
                 f'<div><h3>{e(job["role"])}</h3><p class="co">{e(job["company"])}</p>'
                 f'{"".join(bullets(g["bullets"]) for g in job["groups"])}{wins}</div></article>')
    projects = "".join(
        f'<article class="proj reveal"><div class="chips">{chips(x["tags"])}</div><h3>{e(x["name"])}</h3>'
        f'{bullets(x["bullets"])}<div class="plinks">{project_links(x)}</div></article>' for x in p["projects"])
    links = "".join(f'<li>{contact_link(c, f"<span>{e(c["kind"])}</span>{e(c["value"])}")}</li>' for c in contacts(p))
    ring = lambda label: (f'<figure class="ring" style="--v:98.5"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52"/>'
                          f'<circle class="val" cx="60" cy="60" r="52" pathLength="100"/></svg><figcaption><strong>98.5%</strong>{label}</figcaption></figure>')
    return f"""
<canvas id="net" aria-hidden="true"></canvas>
<header class="topbar"><a class="brand" href="#top">AK<span>.ai</span></a><nav aria-label="Sections">{nav}</nav>{resume_button(p, "nav-resume", "Resume")}</header>
<main id="top">
  <section class="hero">
    <img class="avatar" src="../photo.png" alt="Portrait of {e(s["name"])}" width="124" height="124">
    <p class="status"><i aria-hidden="true"></i>{e(s["availability"])} · {e(s["location"])}</p>
    <h1>{e(s["name"])}</h1>
    <p class="role">{e(p["title"])}</p>
    <div class="chips center">{chips(p["tagline"])}</div>
    <p class="intro">{e(p["intro"])}</p>
    <div class="actions">{resume_button(p, "btn primary")}<a class="btn" href="#agent">See the agent</a><a class="btn" href="#contact">Contact</a></div>
    <div class="metrics">{metric_cards(p)}</div>
  </section>
  <section id="agent"><p class="eyebrow">Agent architecture</p><h2>NOC Auto-Responder</h2><p class="lede">A tool-using agent in daily production use.</p><ol class="flow">{flow}</ol></section>
  <section id="model"><p class="eyebrow">Model card</p><h2>Sensitive-Data-Guard classifier</h2>
    <div class="model reveal"><ol class="train">{train}</ol><div class="rings">{ring("Precision")}{ring("Recall")}</div></div></section>
  <section id="skills"><p class="eyebrow">Capabilities</p><h2>Skills</h2><div class="skill-grid">{skills}</div></section>
  <section id="experience"><p class="eyebrow">Career</p><h2>Experience</h2>{jobs}</section>
  <section id="projects"><p class="eyebrow">Selected work</p><h2>Projects</h2><div class="proj-grid">{projects}</div></section>
  <section id="credentials"><p class="eyebrow">Credentials</p><h2>Certificates &amp; education</h2><div class="cards">{cert_cards(p)}{edu_cards(p)}</div></section>
  <section id="contact"><p class="eyebrow">Get in touch</p><h2>Let's build something intelligent</h2><ul class="contact-list">{links}</ul></section>
</main>
<footer>© 2026 {e(s["name"])}</footer>"""


# --- Data Analyst: a light analytics report --------------------------------------------------

def render_data(p):
    s = p["shared"]
    nav = "".join(f'<a href="#{i}" data-spy>{n}</a>' for i, n in
                  [("overview", "Overview"), ("impact", "Impact"), ("skills", "Skills"), ("experience", "Experience"),
                   ("projects", "Projects"), ("credentials", "Credentials"), ("contact", "Contact")])
    scale = max(c["before"] for c in p["comparisons"])
    bars = ""
    for c in p["comparisons"]:
        bars += (f'<div class="cmp reveal"><div class="cmp-head"><strong>{e(c["name"])}</strong><span class="gain">{e(c["gain"])}</span></div>'
                 f'<div class="bar-row"><span>Before</span><div class="track"><i class="bar before" style="--w:{c["before"] / scale * 100:.1f}%"></i></div><b>~{c["before"]} min</b></div>'
                 f'<div class="bar-row"><span>After</span><div class="track"><i class="bar after" style="--w:{c["after"] / scale * 100:.1f}%"></i></div><b>~{c["after"]} min</b></div></div>')
    sources = "".join(f'<tr><td>{e(x["name"])}</td><td>{e(x["domain"])}</td></tr>' for x in p["sources"])
    skills = "".join(f'<tr><th scope="row">{e(g["name"])}</th><td>{chips(g["items"])}</td></tr>' for g in p["skills"])
    jobs = ""
    for job in p["experience"]:
        wins = ""
        if job["achievements"]:
            wins = '<aside class="findings"><h4>Key achievements</h4>' + bullets(job["achievements"]) + "</aside>"
        jobs += (f'<article class="panel job reveal"><header><div><h3>{e(job["role"])}</h3><p>{joined(job["company"], job["location"])}</p></div>'
                 f'<span class="period">{e(job["dates"])}</span></header>'
                 f'{"".join(bullets(g["bullets"]) for g in job["groups"])}{wins}</article>')
    projects = "".join(
        f'<article class="panel proj reveal"><h3>{e(x["name"])}</h3><div class="tags">{chips(x["tags"])}</div>{bullets(x["bullets"])}'
        f'<div class="plinks">{project_links(x)}</div></article>' for x in p["projects"])
    rows = "".join(f'<tr><th scope="row">{e(c["kind"])}</th><td>{contact_link(c, e(c["value"]))}</td></tr>' for c in contacts(p))
    return f"""
<div class="shell">
  <aside class="rail">
    <a class="brand" href="#overview"><span>AK</span>Analytics</a>
    <nav aria-label="Sections">{nav}</nav>
    {resume_button(p, "rail-resume", "Resume")}
    <p class="rail-note"><i aria-hidden="true"></i>{e(s["availability"])}</p>
  </aside>
  <main>
    <section id="overview" class="masthead">
      <div>
        <p class="kicker">Analyst profile · {e(s["location"])}</p>
        <h1>{e(s["name"])}</h1>
        <p class="role">{e(p["title"])}</p>
        <p class="intro">{e(p["intro"])}</p>
        <div class="tags">{chips(p["tagline"])}</div>
        <div class="actions">{resume_button(p, "btn primary")}<a class="btn" href="#impact">View impact</a><a class="btn" href="#contact">Contact</a></div>
      </div>
      <img class="avatar" src="../photo.png" alt="Portrait of {e(s["name"])}" width="190" height="190">
    </section>
    <div class="kpis">{metric_cards(p)}</div>
    <section id="impact">
      <h2>Impact</h2>
      <div class="impact-grid">
        <div class="panel"><h3>Time per task, before and after automation</h3><p class="sub">Minutes per run</p>{bars}</div>
        <div class="side">
          <div class="panel reveal"><h3>Model evaluation</h3><p class="sub">Sensitive-Data-Guard, after 15 rounds</p>
            <div class="eval"><span>Precision</span><div class="track"><i class="bar after" style="--w:98.5%"></i></div><b>98.5%</b></div>
            <div class="eval"><span>Recall</span><div class="track"><i class="bar after" style="--w:98.5%"></i></div><b>98.5%</b></div></div>
          <div class="panel reveal"><h3>Data sources combined</h3><table class="tbl"><thead><tr><th scope="col">Platform</th><th scope="col">Domain</th></tr></thead><tbody>{sources}</tbody></table></div>
        </div>
      </div>
    </section>
    <section id="skills"><h2>Skills</h2><div class="panel reveal"><table class="tbl skills">{skills}</table></div></section>
    <section id="experience"><h2>Experience</h2>{jobs}</section>
    <section id="projects"><h2>Projects</h2><div class="proj-grid">{projects}</div></section>
    <section id="credentials"><h2>Certificates &amp; education</h2><div class="cards">{cert_cards(p)}{edu_cards(p)}</div></section>
    <section id="contact"><h2>Contact</h2><div class="panel reveal"><table class="tbl">{rows}<tr><th scope="row">Location</th><td>{e(s["location"])}</td></tr></table></div></section>
    <footer>© 2026 {e(s["name"])}</footer>
  </main>
</div>"""


# --- SDET: a CI pipeline and test report ------------------------------------------------------

def render_sdet(p):
    s = p["shared"]
    stages = [("summary", "Summary"), ("skills", "Skills"), ("experience", "Experience"), ("projects", "Projects"),
              ("credentials", "Credentials"), ("contact", "Contact")]
    pipeline = "".join(f'<a href="#{i}" data-spy><i aria-hidden="true"></i>{n}</a>' for i, n in stages)
    run = "".join(f'<div class="t-line" style="--i:{i}"><span>{e(c)}</span><b>PASSED</b></div>' for i, c in enumerate(p["checks"]))
    count = len(p["checks"])
    skills = "".join(
        f'<article class="suite reveal"><h3><span class="tick" aria-hidden="true">✓</span>{e(g["name"])}<em>{len(g["items"])}</em></h3>'
        f'<div class="chips">{chips(g["items"])}</div></article>' for g in p["skills"])

    def checks(items):
        return '<ul class="checks">' + "".join(f"<li>{rich(x)}</li>" for x in items) + "</ul>"

    jobs = ""
    for job in p["experience"]:
        suites = ""
        for g in job["groups"]:
            if g["title"]:
                suites += (f'<details class="group" open><summary><span>{e(g["title"])}</span>'
                           f'<em>{len(g["bullets"])} checks</em></summary>{checks(g["bullets"])}</details>')
            else:
                suites += checks(g["bullets"])
        wins = ""
        if job["achievements"]:
            wins = '<div class="wins"><h4>Key achievements</h4>' + checks(job["achievements"]) + "</div>"
        jobs += (f'<article class="job reveal"><header><div><h3>{e(job["role"])}</h3><p>{joined(job["company"], job["location"])}</p></div>'
                 f'<span class="badge">{e(job["dates"])}</span></header>{suites}{wins}</article>')
    projects = "".join(
        f'<article class="proj reveal"><span class="pass">PASS</span><h3>{e(x["name"])}</h3><div class="chips">{chips(x["tags"])}</div>'
        f'{checks(x["bullets"])}<div class="plinks">{project_links(x)}</div></article>' for x in p["projects"])
    links = "".join(f'<li>{contact_link(c, f"<span>{e(c["kind"])}</span>{e(c["value"])}")}</li>' for c in contacts(p))
    return f"""
<header class="pipeline"><a class="brand" href="#summary">AK<span>/qa</span></a><nav aria-label="Sections">{pipeline}</nav>{resume_button(p, "pipe-resume", "Resume")}<div class="progress" aria-hidden="true"><i id="progress"></i></div></header>
<main>
  <section id="summary" class="hero">
    <div>
      <p class="build"><i aria-hidden="true"></i>{e(s["availability"])} · {e(s["location"])}</p>
      <h1>{e(s["name"])}</h1>
      <p class="role">{e(p["title"])}</p>
      <div class="chips">{chips(p["tagline"])}</div>
      <p class="intro">{e(p["intro"])}</p>
      <div class="actions">{resume_button(p, "btn primary")}<a class="btn" href="#experience">View test record</a><a class="btn" href="#contact">Contact</a></div>
    </div>
    <div class="side">
      <img class="avatar" src="../photo.png" alt="Portrait of {e(s["name"])}" width="120" height="120">
      <div class="terminal" role="img" aria-label="Test run summary: {count} checks passed">
        <div class="t-bar"><i></i><i></i><i></i><span>career_test_report</span></div>
        <div class="t-body"><div class="t-cmd">$ pytest career/ -v</div>{run}<div class="t-sum" style="--i:{count}">{count} passed</div></div>
      </div>
    </div>
  </section>
  <div class="metrics">{metric_cards(p)}</div>
  <section id="skills"><p class="stage">Stage 01</p><h2>Skills</h2><div class="suite-grid">{skills}</div></section>
  <section id="experience"><p class="stage">Stage 02</p><h2>Experience</h2>{jobs}</section>
  <section id="projects"><p class="stage">Stage 03</p><h2>Projects</h2><div class="proj-grid">{projects}</div></section>
  <section id="credentials"><p class="stage">Stage 04</p><h2>Certificates &amp; education</h2><div class="cards">{cert_cards(p)}{edu_cards(p)}</div></section>
  <section id="contact"><p class="stage">Stage 05</p><h2>Contact</h2><ul class="contact-list reveal">{links}</ul></section>
</main>
<footer>© 2026 {e(s["name"])}</footer>"""


RENDERERS = {"software-engineer": render_software, "ai-ml-engineer": render_ai, "data-analyst": render_data, "sdet": render_sdet}


def page(p):
    slug = p["slug"]
    themes = HERE / "themes"
    css = (themes / "_base.css").read_text(encoding="utf-8") + (themes / f"{slug}.css").read_text(encoding="utf-8")
    js = (themes / "_base.js").read_text(encoding="utf-8")
    theme_js = themes / f"{slug}.js"
    if theme_js.exists():
        js += theme_js.read_text(encoding="utf-8")
    name = p["shared"]["name"]
    description = f'{name}, {p["title"]}. {p["intro"]}'
    ambient = "" if slug == "ai-ml-engineer" else '<canvas id="ambient" aria-hidden="true"></canvas>'
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex">
<title>{e(name)} — {e(p["title"])}</title>
<meta name="description" content="{e(description)}">
<script>document.documentElement.className='js'</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[slug]}&display=swap">
<style>
{css}</style>
</head>
<body>
{ambient}
{RENDERERS[slug](p)}
<script>
{js}</script>
</body>
</html>
"""


def main():
    for slug in SLUGS:
        out = ROOT / slug
        out.mkdir(exist_ok=True)
        (out / "index.html").write_text(page(load(slug)), encoding="utf-8", newline="\n")
        print(f"built {slug}/index.html")


if __name__ == "__main__":
    main()
