# Ashutosh Kumar — Portfolio

Personal portfolio site for Ashutosh Kumar, Security Analyst (SOC Operations & Application Security). A single-page, dark-themed site covering summary, skills, experience, independent security projects, certifications, and contact details, with light 3D touches (tilt-on-hover cards, an animated background) and a real résumé link.

**Live site:** _add your Render URL here once deployed_

## Structure

This is a static site — no build step, no dependencies, no framework.

```
index.html   All markup, styles, and scripts (self-contained)
photo.png    Headshot used in the hero and About sections
```

Fonts (Manrope, via Google Fonts) load over the network at runtime; everything else is local.

## Running locally

Just open `index.html` in a browser — no server or build step required.

## Deploying

Deployed as a static site on [Render](https://render.com):

- **Build Command:** _(none)_
- **Publish Directory:** `.`

Any static host that serves plain files (Render, Netlify, GitHub Pages, Cloudflare Pages) works the same way.

## Updating content

Résumé data, skills, experience, and project details live directly in `index.html`. Certificate and project links point to Google Drive folders and GitHub repositories — update the `href` values in place if any of those links change.
