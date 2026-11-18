# Ashutosh Kumar — Portfolio

Personal portfolio site for Ashutosh Kumar, SOC Analyst (Incident Response · Threat Hunting · Phishing & Identity Defense · Security Automation). The homepage is a single-page, dark cyber/terminal-themed overview (JetBrains Mono, a falling-code canvas background, glitch-text heading, a typewriter line) covering summary, skills, experience, independent security projects, certifications, and contact details, with hover-tilt cards and scroll-reveal animation, plus a real résumé link. Each of those sections also has its own dedicated deep-dive page with its own distinct font and background theme, reachable from the nav bar.

**Live site:** https://ashutosh-portfolio-3x68.onrender.com/

## Structure

This is a static site — no build step, no dependencies, no framework.

```
index.html           Homepage: Hero, About, Skills, Experience, Projects, Certifications, Contact (full scroll overview) — "cyber/terminal" theme (JetBrains Mono + Manrope, green, matrix-rain canvas)
skills.html           Dedicated Skills page — "constellation" theme (Sora font, blue/violet)
experience.html       Dedicated Experience page — "signal timeline" theme (Space Grotesk font, gold/violet)
projects.html         Dedicated Projects page — "terminal/hacker" theme (JetBrains Mono font, green)
certifications.html   Dedicated Certifications page — "certificate/seal" theme (Fraunces font, gold)
contact.html          Dedicated Contact page — "radar/beacon" theme (Outfit font, cyan)
photo.png             Headshot used in the hero and About sections
```

Every page is self-contained (markup, styles, and scripts inline). The five dedicated pages share the same animated circuit/grid/floating-cube background system, recolored to each page's own accent; the homepage instead runs its own matrix-rain canvas background to match its cyber/terminal theme. Fonts load over Google Fonts at runtime; everything else is local.

## Role-specific portfolios

Each résumé links to its own portfolio. The portfolios do not link to each other.

| Résumé | Path | Source |
|---|---|---|
| Cyber Security | `/` (`/cyber-security/` redirects there) | Root HTML pages, edited by hand |
| Software Engineer | `/software-engineer/` | `_profiles/data/software-engineer.json` |
| AI/ML Engineer | `/ai-ml-engineer/` | `_profiles/data/ai-ml-engineer.json` |
| Data Analyst | `/data-analyst/` | `_profiles/data/data-analyst.json` |
| SDET | `/sdet/` | `_profiles/data/sdet.json` |

Contact details, project links, certificates and education for the four generated portfolios live in `_profiles/data/shared.json`, and each design lives in `_profiles/themes/`. To add a résumé link, set `resume_url` in that profile's JSON file. After any change, run `python _profiles/build.py` and commit the regenerated `<slug>/index.html`.

## Navigation model

- The homepage (`index.html`) is a complete single-page overview — scrolling it shows every section in full, same as before.
- The nav bar's Skills / Experience / Projects / Certifications / Contact links each open that section's own dedicated page instead of jumping to an anchor, for a deeper, differently-themed read.
- Every dedicated page links back to `index.html` and across to the other dedicated pages via its own nav bar.

## Running locally

Just open `index.html` in a browser — no server or build step required.

## Deploying

Deployed as a static site on [Render](https://render.com):

- **Build Command:** _(none)_
- **Publish Directory:** `.`

Any static host that serves plain files (Render, Netlify, GitHub Pages, Cloudflare Pages) works the same way.

## Updating content

Résumé data, skills, experience, and project details are duplicated between `index.html` (the homepage overview) and the matching dedicated page (e.g. experience details live in both `index.html` and `experience.html`) — update both when the underlying facts change. Certificate and project links point to Google Drive folders and GitHub repositories — update the `href` values in place (in both files) if any of those links change.
