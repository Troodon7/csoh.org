# Cloud Security Office Hours (CSOH)

A community-run cloud-security resource hub, built as a static website. Weekly Zoom sessions, a curated resources catalog, news aggregation, and an RSS feed.

[![GitHub](https://img.shields.io/badge/GitHub-CloudSecurityOfficeHours/csoh.org-blue)](https://github.com/CloudSecurityOfficeHours/csoh.org)
[![Discord](https://img.shields.io/badge/Discord-2000%2B%20Members-5865F2)](https://discord.gg/AVzAY97D8E)
[![License](https://img.shields.io/badge/License-Open%20Content-green)](LICENSE)

---

## About CSOH

Cloud Security Office Hours is a vendor-neutral, free community founded in February 2023. What's here:

- Weekly Zoom sessions, Fridays at 7am PT with guest speakers.
- A curated resources catalog (CTFs, labs, tools, certifications).
- Cloud-security news aggregated every 3 hours from 39 RSS feeds.
- The RSS feed itself at [csoh.org/feed.xml](https://csoh.org/feed.xml).
- Discord for real-time discussion.

---

## 🎓 Getting Started

**New to cloud security?** Cloud security is the practice of protecting data, applications, and infrastructure hosted in cloud environments like AWS, Azure, and Google Cloud. As organizations move to the cloud, securing these environments has become one of the fastest-growing and most in-demand areas in cybersecurity.

Here's our recommended learning path:

1. **Start with Resources**: Browse [CTF Challenges](resources.html#ctf-challenges) and [Labs](resources.html#labs-training) for hands-on practice
2. **Get Certified**: Explore [Certifications](resources.html#certifications) path for your cloud platform
3. **Join Community**: Register for [Weekly Zoom Sessions](sessions.html) (Fridays 7am PT)
4. **Stay Updated**: Check [News](news.html) for latest threats and updates
5. **Subscribe to RSS**: Add our [RSS feed](https://csoh.org/feed.xml) to your reader — see [RSS_FEED_README.md](RSS_FEED_README.md) for setup
6. **Network**: Join [Discord](https://discord.gg/AVzAY97D8E) for real-time discussions

---

## 📄 Website Pages

### 🏠 Homepage (`index.html`)
Central hub featuring:
- Community overview and value proposition
- Featured resource categories with quick navigation
- Call-to-action buttons for Zoom registration and Discord
- Enhanced schema markup for improved SERP visibility
- Testimonials and member count (2000+)

### 📚 Resources (`resources.html`)
Comprehensive catalog of **200+ cloud security resources** organized by 6 categories:

#### 🎯 CTF Challenges & Vulnerable Environments
- **CloudGoat** - Open-source, AWS vulnerable environments by Rhino Security Labs
- **AWSGoat** - Vulnerable AWS stack from INE (formerly AppSecEngineer)
- **Kubernetes Goat** - K8s containerized application with intentional vulnerabilities
- **AIGoat** - AI/ML vulnerable applications
- **Blue Team Labs** - Hands-on security scenarios
- Plus 15+ additional CTF platforms (OWASP, HackTheBox, TryHackMe, etc.)

#### 🧪 Hands-On Labs & Training Platforms
- **Cybr** - Free AWS security labs
- **Digital Cloud Training** - Comprehensive challenge labs
- **AWS Well-Architected Labs** - Official AWS security training
- **Immersive Labs** - Interactive cybersecurity training
- **SecureFlag** - GCP security labs
- **Pwned Labs** - Realistic penetration testing scenarios
- Plus 20+ additional training platforms

#### 🛡️ Security Tools & Platforms (60+ Tools)
- **CNAPP (Cloud Native Application Protection)** - Runtime protection tools
- **CSPM (Cloud Security Posture Management)** - Configuration & compliance scanning
- **KSPM (Kubernetes Security Posture Management)** - K8s-specific security
- **SIEM & Threat Detection** - Splunk, ELK Stack, AWS Security Hub, etc.
- **Compliance & Config Management** - Terraform, Ansible, CloudFormation
- **Vulnerability Management** - Snyk, Qualys, Tenable, etc.

#### 🎓 Certifications & Professional Development (40+ Certs)
- **AWS** - Security Specialty, Solutions Architect, Database Specialty
- **Azure** - Security Engineer Associate, Administrator Associate
- **Google Cloud** - Professional Cloud Security Engineer
- **Cloud Security Alliance** - CCSK Certification
- **Kubernetes** - CKA, CKAD, CKS
- **General Security** - CISSP, CEH, SC-300, AZ-305
- **Bootcamps & Prep Courses** - Pwned Labs, AWSome Day, etc.

#### 🤖 AI Security (15+ Resources)
- **AI Security Tools** - Trend Micro Workload Security, etc.
- **AI Vulnerable Environments** - AIGoat, AI Security CTFs
- **AI Security Research** - Papers, whitepapers, research resources

#### 💼 Job Search Resources (20+ Listings)
- **Job Boards** - LinkedIn, Dice, CyberSecJobs, CloudSecurityJobs
- **Resume Services** - Resume optimization platforms
- **Interview Prep** - Technical interview guides
- **Career Development** - Mentorship, networking resources

#### 📰 Cloud Security News (120+ Articles)
- **Latest articles** sorted by publication date (newest first)
- **Multi-source aggregation** - SecurityWeek, KrebsOnSecurity, CrowdStrike, AWS Security Blog, Microsoft MSRC, SANS ISC, The Register, BleepingComputer, Dark Reading, Palo Alto Unit 42, CISA, and more
- **Searchable & filterable** by source, topic, date
- **Auto-updated every 3 hours** via Python news aggregation script
- **Rich snippet optimization** for featured search results

### 💬 Chat Resources (`chat-resources.html`)
Community-shared resources from weekly Zoom sessions:
- **557+ URLs** shared by community members during live sessions
- **Security validated** - All URLs automatically checked for malicious patterns
- **Filterable by date, person, category** - Find resources from specific sessions
- **Descriptive titles** - Auto-generated from page content
- **Continuous protection** - GitHub Actions workflow validates new URLs before merge

### 📅 Zoom Sessions (`sessions.html`)
Information about weekly community gatherings:
- **When:** Every Friday at 7am PT
- **Format:** Expert presentations + open discussion + Q&A
- **Cost:** Completely free
- **Registration Link:** https://sendfox.com/CSOH
- Format details and speaker information

### 🎬 Presentations (`presentations.html`)
Archive of past Zoom session presentations:
- Recorded sessions from industry experts
- Topic tags (AWS, Azure, GCP, Kubernetes, CSPM, CNAPP, etc.)
- Dates and presentation descriptions
- Direct video links

### 📝 Meeting Recaps (`meetings.html`)
Topic-by-topic recaps of every weekly session:
- **91+ meeting recaps** with per-topic summaries and speaker notes
- Searchable, filterable by tag (AWS, Azure, AI, supply chain, conferences, etc.)
- Auto-ingested from Zoom AI Companion summaries or VTT transcripts via `tools/add_meeting.py`

### 🚩 Cloud CTFs (`ctfs.html`)
Dedicated directory for hands-on cloud CTF challenges:
- **39+ challenges** across AWS, Azure, GCP, Kubernetes, and AI security
- Includes the full Wiz Cloud Security Championship calendar
- Submit a new CTF with `python3 tools/submit_ctf.py` — see [CONTRIBUTING_CTFS.md](CONTRIBUTING_CTFS.md)

### 📡 RSS Subscribe (`rss.html`)
Plain-English landing page for the `feed.xml` feed: explains what RSS is, recommends readers (Feedly, Inoreader, NetNewsWire, Thunderbird), and gives one-click subscribe instructions.

---

## 🔗 Breach Kill Chains (`breach-timeline.html`)

A community-maintained library of **step-by-step cloud breach reconstructions**, mapped to MITRE ATT&CK Cloud techniques and sourced from official post-mortems.

### Current incidents covered

| Incident | Year | Provider | Key Techniques |
|---|---|---|---|
| Mitnick / Novell | 1994 | On-Prem | Social engineering, pretexting, credential theft |
| Capital One | 2019 | AWS | T1190, T1552.005, T1619, T1530 |
| SolarWinds | 2020 | Azure AD / AWS | T1195.002, T1071.004, T1606.002, T1114.002 |
| Uber | 2022 | AWS / GCP | T1078, T1621, T1552.001, T1078.004 |
| LastPass | 2022–2023 | LastPass / AWS S3 | T1195.002, T1203, T1555, T1530 |
| Storm-0558 | 2023 | Azure | T1078, T1552, T1606.001, T1114.002 |
| Microsoft SAS Leak | 2023 | Azure | T1552.004, T1530 |
| Scattered Spider / MGM | 2023 | Okta / Azure | T1598, T1078, T1484, T1486 |
| Snowflake / UNC5537 | 2024 | Snowflake | T1078.004, T1555.003, T1530, T1657 |
| Promptware | 2024–2026 | AI / LLM (Gemini, Copilot) | T1566, T1071.001, T1534, T1530 |

### How to contribute a kill chain

See **[CONTRIBUTING_KILL_CHAINS.md](CONTRIBUTING_KILL_CHAINS.md)** for the full guide including:
- What qualifies as a good kill chain entry
- A list of candidate incidents with good post-mortems
- The HTML template to copy for a new entry
- The quality checklist before submitting

To **nominate an incident** without writing it yourself, open an issue using the **"🔗 New Kill Chain Request"** template.

### The standard

Kill chain entries require:
- A real post-mortem or official technical disclosure (vendor blog, CISA advisory, court documents)
- Step-by-step technical detail — not just a summary
- Every step mapped to a MITRE ATT&CK Cloud technique
- Actionable defender recommendations tied to specific controls

This is intentionally high-bar. A small number of deeply researched entries is more valuable than many shallow ones.

---

## 🔬 Threat Research (`threat-research.html`)

A curated directory of primary sources for cloud-focused threat research. Unlike Breach Kill Chains (which documents specific historical incidents), this page is a living index of where cloud defenders go for ongoing intel.

### Sections

- **Vendor Research Teams** — Wiz Research, Unit 42, Mandiant, Microsoft Threat Intelligence, Google TAG, CrowdStrike Counter Adversary Ops, SentinelLabs, Datadog Security Labs, Sysdig TRT, Aqua Nautilus, Permiso, Cado Security, AWS Security Bulletins, MSRC, IBM X-Force, Trellix, Proofpoint
- **Annual Threat Reports** — Mandiant M-Trends, CrowdStrike Global Threat Report, Unit 42 Cloud Threat Report, Verizon DBIR, IBM X-Force Index, Datadog State of Cloud Security, CSA Top Threats, ENISA, Sophos State of Ransomware
- **Notable Incidents & Post-Mortems** — cross-links to `breach-timeline.html` plus primary sources for Capital One, Storm-0558, SolarWinds, LastPass, Scattered Spider/MGM, Snowflake/UNC5537, Uber, Microsoft SAS Token Leak, Codecov, Okta HAR
- **IOC Feeds & Threat Intel Platforms** — AlienVault OTX, abuse.ch, VirusTotal, MISP, Shodan, GreyNoise, Censys, CIRCL, Feodo Tracker, Spamhaus, IBM X-Force Exchange, OSINT Framework
- **Attack Frameworks & Matrices** — MITRE ATT&CK Cloud / Containers, D3FEND, Microsoft Kubernetes Threat Matrix, OWASP Cloud-Native Top 10, TheHive, Sigma, Elastic Detection Rules
- **Government & Regulatory Advisories** — CISA (+KEV), FBI IC3, NSA, UK NCSC, ACSC, NIST NVD, CVE.org

### How to contribute a source

Edit `threat-research.html` directly — each link is a standard `.resource-card` in the same format as `resources.html` and `presentations.html`. Open a PR with:

- A link to the primary research output (blog index, report landing page, or feed URL — not a marketing page)
- A one-sentence description of what's unique about the source
- 2–3 tags (use existing tag classes where possible: `ctf`, `tool`, `lab`, `certification`, `job`, `ai-security`, `new`)

---


## Features

- Static HTML — no database, no server-side code; deploys to GitHub Pages, Vercel, S3.
- URL-safety gate — every PR is scanned for unsafe URLs before merge (`check_all_site_urls.py`).
- RSS feed — `feed.xml` regenerated with each news update. See [RSS_FEED_README.md](RSS_FEED_README.md).
- Dark mode — toggle plus `prefers-color-scheme` detection, persisted in `localStorage`.
- Schema markup — NewsArticle, FAQPage, Organization, Event, CollectionPage.
- Accessibility — semantic HTML5, ARIA labels, WCAG AA contrast in both themes.
- Search + tag filtering on news and resources pages.

---

## 📁 Project Structure

```
csoh.org/
├── index.html                  # Homepage with hero section & category overview
├── resources.html              # Main resource directory (200+ resources in 6 categories)
├── news.html                   # Cloud security news (120+ articles)
├── chat-resources.html         # Community-shared URLs from Zoom sessions (557+ URLs)
├── sessions.html               # Weekly Zoom session information
├── presentations.html          # Archive of recorded presentations
├── meetings.html               # Weekly meeting recaps (91+ entries, topic-by-topic)
├── ctfs.html                   # Dedicated cloud CTF directory (39+ challenges)
├── rss.html                    # Landing page explaining the RSS feed to subscribers
├── breach-timeline.html        # Cloud breach kill chain library
├── threat-research.html        # Curated cloud threat research directory
├── contribute.html             # General contributions guide
├── contribute-resources.html   # Resource submission web form / guide
├── security-policy.html        # Security disclosure policy page
├── kevin-mitnick.html          # Special resource page
├── 403.html                    # Custom 403 (Forbidden) error page
├── 404.html                    # Custom 404 (Not Found) error page
│
├── style.css                   # Main stylesheet (responsive design + dark mode)
├── main.js                     # Shared interactive features (search, filter, sort, dark mode)
├── chat-resources.js           # chat-resources.html-specific filtering/search
├── meetings.js                 # meetings.html-specific index + filters
├── breach-timeline.css         # breach-timeline.html-specific styles
├── breach-timeline.js          # breach-timeline.html-specific tab/panel logic
├── feed.xml                    # RSS feed (auto-generated by update_news.py)
│
├── sitemap.xml                 # XML sitemap for search engines
├── robots.txt                  # Search engine crawling rules
├── security.txt                # Security.txt (root copy)
├── .well-known/                # Well-known endpoints
│   └── security.txt            # Security.txt (RFC 9116 location)
│
├── img/                        # Images and preview thumbnails
│   └── previews/               # Resource preview images
├── chat-screenshots/           # Per-URL screenshots shown in chat-resources.html
│
├── tools/                      # Automation and maintenance scripts
│   ├── submit_resource.py                  # Interactive tool for submitting new resources
│   ├── submit_news_source.py               # Interactive tool for submitting news sources
│   ├── submit_ctf.py                       # Interactive tool for submitting cloud CTFs
│   ├── add_meeting.py                      # Append a new meeting recap from an Apple Notes HTML export
│   ├── fetch_zoom_transcript.py            # Pull a VTT transcript from a Zoom cloud recording (OAuth)
│   ├── backfill_zoom_summaries.py          # Bulk-import Zoom AI Companion meeting summaries
│   ├── generate_preview.py                 # Generate preview screenshots for resources
│   ├── generate_rss.py                     # Regenerate feed.xml from news.html
│   ├── normalize_urls.py                   # URL normalizer (tracking params, HTTPS, redirects)
│   ├── check_url_safety.py                 # Core URL safety validator with pattern matching
│   ├── check_all_site_urls.py              # Comprehensive site-wide URL scanner
│   ├── update_sitemap.py                   # Refresh sitemap.xml <lastmod> dates from git history
│   ├── update_presentations_schema.py      # Regenerate VideoObject JSON-LD on presentations.html
│   ├── SUBMIT_RESOURCE_README.md           # Interactive resource submission docs
│   ├── SUBMIT_RESOURCE_EXAMPLE.md          # Walkthrough example for the resource tool
│   ├── SUBMIT_NEWS_SOURCE_README.md        # News source submission docs
│   ├── SUBMIT_CTF_README.md                # CTF submission docs
│   ├── ADD_MEETING_README.md               # Meeting recap ingest docs
│   ├── FETCH_ZOOM_TRANSCRIPT_README.md     # Zoom transcript fetch docs (OAuth setup)
│   ├── BACKFILL_ZOOM_SUMMARIES_README.md   # Bulk Zoom AI Companion backfill docs
│   ├── GENERATE_PREVIEW_README.md          # Preview image generation docs
│   ├── CHECK_URL_SAFETY_README.md          # URL safety checker docs
│   ├── UPDATE_NEWS_README.md               # News aggregation pipeline docs
│   ├── UPDATE_SRI_README.md                # SRI hash generator docs
│   ├── UPDATE_SITEMAP_README.md            # Sitemap refresher docs
│   └── UPDATE_PRESENTATIONS_SCHEMA_README.md # Presentations VideoObject schema docs
│
├── update_news.py              # News aggregation script (39 RSS feeds, runs every 3 hours)
├── update_sri.py               # Updates SRI hashes & cache-bust params across HTML files
│
├── .github/workflows/
│   ├── update-news.yml              # Automated news + RSS feed updates (every 3 hours)
│   ├── site-update-deploy.yml       # Unified workflow: SRI, URL normalization, previews, presentations schema, sitemap, deploy
│   ├── check-url-safety.yml         # URL safety validation on PRs + weekly
│   ├── normalize-urls.yml           # Monthly URL normalization (tracking params, redirects)
│   ├── validate-html.yml            # HTML5 validation on PRs + weekly
│   ├── check-broken-links.yml       # Broken link checker (PRs + weekly)
│   └── CHECK_URL_SAFETY_WORKFLOW.md # Workflow configuration notes
│
├── preview-mapping.json        # Metadata for resource previews
│
├── .htaccess                   # Apache server config (security headers, caching, compression)
├── nginx.conf                  # Nginx server config (Docker deployments)
├── Dockerfile                  # Container build for local/Docker deployments
├── docker-compose.yml          # Compose config for the Dockerized site
├── .env.example                # Template for Zoom OAuth + other secrets (.env is gitignored)
├── .lychee.toml                # Config for the broken-link-checker workflow
├── .editorconfig               # Editor consistency rules
├── .dockerignore               # Files excluded from the Docker build context
│
├── CONTRIBUTING.md             # Umbrella contributing guide
├── CONTRIBUTING_RESOURCES.md   # Contributing resources specifically
├── CONTRIBUTING_CTFS.md        # Contributing CTFs specifically
├── CONTRIBUTING_KILL_CHAINS.md # Contributing breach kill chains specifically
├── DEVELOPMENT.md              # Local development setup & architecture
├── SECURITY.md                 # Security reporting policy
├── RSS_FEED_README.md          # RSS feed usage guide for subscribers
├── .gitignore                  # Git exclusion rules
├── README.md                   # This file
└── LICENSE                     # Open content license
```

---

## 🛠️ Managing Content

### Adding a New Resource

**Fastest option:** Run `python3 tools/submit_resource.py` to add a resource interactively.
**Script guide:** [tools/SUBMIT_RESOURCE_README.md](tools/SUBMIT_RESOURCE_README.md)

1. **Open `resources.html`** in your editor
2. **Locate the appropriate section** (CTF, Labs, Tools, etc.)
3. **Add a new resource card** before the closing `</div>` of the section:

```html
<a href="https://resource-url.com" target="_blank" class="card-link" rel="noopener noreferrer">
    <div class="resource-card" data-tooltip="Extended 2-3 sentence description shown on hover. Cover what makes it unique, who benefits most, and prerequisites or cost.">
        <img src="img/previews/resource-url.com.jpg" alt="Preview" class="resource-preview">
        <h3>Resource Name</h3>
        <p>Brief description of what this resource offers and why it's valuable for cloud security professionals.</p>
        <div class="resource-tags">
            <span class="tag">AWS</span>
            <span class="tag">Security</span>
            <span class="tag new">NEW</span>
        </div>
    </div>
</a>
```

**Preview images:** If you do not have a preview image, the workflow will automatically capture a screenshot and update `preview-mapping.json` after you open a PR.

4. **Commit and push** to update the live site

### Adding a New Article to News

News articles are **updated automatically** — you don't need to add them by hand. A GitHub Actions workflow runs every 3 hours, pulls articles from 39 cloud security RSS feeds, and creates a pull request with the new content. See the [How Automation Works](#-how-automation-works) section below for details, or read the full docs in [tools/UPDATE_NEWS_README.md](tools/UPDATE_NEWS_README.md).

To **add a new news source**, either:

1. Run `python3 tools/submit_news_source.py` (interactive, recommended)
2. Or edit the `FEEDS` list at the top of `update_news.py` manually

**Script guide:** [tools/SUBMIT_NEWS_SOURCE_README.md](tools/SUBMIT_NEWS_SOURCE_README.md)

### Adding a New Zoom Session or Presentation

1. **For Sessions:** Edit `sessions.html` to add session details

2. **For Presentations:** Edit `presentations.html` and add a new card with:
   - Date and title
   - Speaker name
   - Description
   - Topic tags
   - Video/presentation link

### Adding a New Meeting Recap

Meeting recaps live on `meetings.html` and are ingested from Zoom, not written by hand. Two automation paths:

- **Single meeting from a VTT transcript:** `python3 tools/fetch_zoom_transcript.py` pulls the transcript from your Zoom cloud recording, then `python3 tools/add_meeting.py <note>` appends a new `<article>` block to `meetings.html`. See [tools/FETCH_ZOOM_TRANSCRIPT_README.md](tools/FETCH_ZOOM_TRANSCRIPT_README.md) and [tools/ADD_MEETING_README.md](tools/ADD_MEETING_README.md).
- **Bulk backfill from Zoom AI Companion summaries:** `python3 tools/backfill_zoom_summaries.py` imports every AI Companion summary on the account in one pass. See [tools/BACKFILL_ZOOM_SUMMARIES_README.md](tools/BACKFILL_ZOOM_SUMMARIES_README.md).

Both require Zoom Server-to-Server OAuth credentials in a local `.env` (see `.env.example`).

### Adding a New CTF

Run `python3 tools/submit_ctf.py` to add a challenge to `ctfs.html` interactively. See [tools/SUBMIT_CTF_README.md](tools/SUBMIT_CTF_README.md) for the script, or [CONTRIBUTING_CTFS.md](CONTRIBUTING_CTFS.md) for the full contribution guide.

### Customizing the Homepage

Edit the "Resource Categories" section in `index.html` to:
- Change category descriptions
- Modify call-to-action buttons
- Adjust hero section messaging

---

## 🤖 How Automation Works


This site uses **GitHub Actions workflows** to automate all major site updates. Most automation is now handled by a **unified workflow** that runs all key steps in sequence, only when needed.

### Unified Site Update & Deploy Workflow

**Workflow file:** `.github/workflows/site-update-deploy.yml`

**Triggers on pushes to `main` when these files change:**
- `style.css`, `main.js`, `chat-resources.js`, `update_sri.py`
- `resources.html`, `chat-resources.html`
- `chat-screenshots/**` (new chat resource screenshots)
- Manual trigger via the GitHub Actions tab

**What it does:**
- Updates SRI hashes and cache-busting tags if CSS/JS changed (using `update_sri.py`)
- Checks URL safety — blocks deploy if unsafe URLs are detected (using `check_all_site_urls.py`)
- Normalizes URLs — strips tracking parameters, upgrades HTTP to HTTPS, resolves redirects (using `normalize_urls.py`)
- Regenerates the `VideoObject` JSON-LD on `presentations.html` (using `update_presentations_schema.py`)
- Refreshes `<lastmod>` dates in `sitemap.xml` from git history (using `update_sitemap.py`)
- Generates preview images for new resources in `resources.html` (using `generate_preview.py`)
- Checks for broken links (non-blocking warning)
- Deploys the site to the web server via FTP in smart passes:
  - **Pass 1:** Always deploys all HTML/CSS/JS and other site files (excludes images)
  - **Pass 2:** Only uploads `img/previews/` when new preview images were generated
  - **Pass 3:** Always syncs news source banner images
  - **Pass 4:** Only uploads `chat-screenshots/` when new screenshots were added

**How it works:**
1. Checks for any changes that require SRI updates, URL normalization, new previews, or new chat screenshots
2. Runs each step in order: SRI → URL safety → URL normalization → previews → link check → deploy
3. URL safety check and normalization must pass before previews are generated or the site is deployed

**News updates** are still handled by a separate scheduled workflow (`update-news.yml`) that runs every 3 hours and creates a PR with new articles. Once merged, the unified workflow deploys the site.

### Standalone URL Normalization Workflow

**Workflow file:** `.github/workflows/normalize-urls.yml`

In addition to the URL normalization that runs as part of every deploy, a **standalone monthly workflow** performs a deeper pass across all HTML files:

- **Schedule:** Monthly on the 1st at 08:00 UTC (also available via manual trigger)
- **What it does:**
  - Checks URL safety first — blocks normalization if unsafe URLs are found
  - Strips tracking parameters (`utm_*`, `fbclid`, `gclid`, `msclkid`, etc.)
  - Upgrades HTTP links to HTTPS
  - Resolves redirecting URLs to their final destinations
- **Output:** Creates a PR with a detailed report of all changes, auto-approved for review

**Full docs:** See [tools/UPDATE_SRI_README.md](tools/UPDATE_SRI_README.md), [tools/GENERATE_PREVIEW_README.md](tools/GENERATE_PREVIEW_README.md), [tools/UPDATE_NEWS_README.md](tools/UPDATE_NEWS_README.md), and [tools/CHECK_URL_SAFETY_README.md](tools/CHECK_URL_SAFETY_README.md)

### Setup Note

Workflows use a **Personal Access Token (PAT)** stored as a GitHub repo secret called `PAT_TOKEN`. If workflows start failing with permission errors, the PAT may need to be rotated — see setup instructions in [tools/UPDATE_NEWS_README.md](tools/UPDATE_NEWS_README.md#setup-requirements).

---

## 🔍 SEO & Search Optimization

### Rich Snippets Enabled
- ✅ **NewsArticle Schema** - Top articles on `news.html` regenerated each run for Google News carousel eligibility
- ✅ **VideoObject Schema** - Each YouTube talk on `presentations.html` marked up for video-rich results
- ✅ **FAQPage Schema** - 5 high-relevance Q&A pairs for featured snippets
- ✅ **Organization Schema** - Domain authority signals (4.8★ rating, 2000+ members)
- ✅ **CollectionPage Schema** - Resource pages eligible for rich results
- ✅ **Event Schema** - Weekly Zoom session marked up for search visibility
- ✅ **BreadcrumbList** - Navigation hierarchy for SERP display
- ✅ **Fresh `<lastmod>` sitemap dates** - refreshed from git history on every deploy

## 🤝 Contributing

Want to help improve CSOH? We have **beginner-friendly guides** for contributing—no coding experience needed!

### 📚 Contribution Guides

- **[Interactive Resource Submission Tool](tools/SUBMIT_RESOURCE_README.md)** - Automated Python script with URL validation and PR creation
- **[Interactive News Source Submission Tool](tools/SUBMIT_NEWS_SOURCE_README.md)** - Add RSS/Atom feeds with the interactive script
- **[How to Add a Resource](contribute-resources.html)** - Step-by-step guide for adding cloud security resources (tools, labs, certifications, etc.)
- **[General Contributions](contribute.html)** - Guide for all other contributions:
  - Adding news sources for our automated news aggregation
  - Improving descriptions and content
  - Suggesting resource reorganization
  - Reporting bugs or broken links
  - Feature requests and ideas

### Quick Start

**Easy options (no coding required):**
1. [Report an issue](https://github.com/CloudSecurityOfficeHours/csoh.org/issues) - Found a bug? Have a suggestion?
2. [Join Discord](https://discord.gg/AVzAY97D8E) - Discuss ideas with the community
3. [Add a resource](contribute-resources.html) - Use our web-based guide (copy/paste method)
4. [Use the submission tool](tools/SUBMIT_RESOURCE_README.md) - Interactive Python script (automated)
5. [Add a news source](tools/SUBMIT_NEWS_SOURCE_README.md) - Interactive Python script

**For developers:**
See **[DEVELOPMENT.md](DEVELOPMENT.md)** for the full local setup guide, project architecture, and testing instructions.

1. Fork the repository
2. Create a feature branch: `git checkout -b add-resource`
3. Run `python3 -m http.server 8091` and preview at `http://localhost:8091`
4. Make changes and test locally (check light mode, dark mode, and mobile layout)
5. Commit with clear messages: `git commit -m "Add AWS security labs resource"`
6. Push to your fork: `git push origin add-resource`
7. Create a Pull Request

### Contribution Guidelines

- All resources must be **free or freemium** (or worth including as premium option)
- Ensure **working links** before submitting
- Add **descriptive tags** (AWS, Azure, GCP, Kubernetes, CTF, Tools, Labs)
- Maintain **vendor neutrality** - no paid sponsorships without disclosure
- Follow existing **HTML/CSS conventions**

---

## 📞 Community & Support

### Join the Community
- **Discord**: https://discord.gg/AVzAY97D8E - 2000+ members, real-time discussions
- **Zoom Sessions**: https://sendfox.com/CSOH - Fridays at 7am PT
- **GitHub**: https://github.com/CloudSecurityOfficeHours/csoh.org

### Need Help?
- **Discord**: Ask in #general or #resources channel
- **Issues**: Create a [GitHub issue](https://github.com/CloudSecurityOfficeHours/csoh.org/issues)
- **Contact**: Reach out via Discord to community admins

### Support CSOH
- ❤️ **Star** this repository
- 🔗 **Share** CSOH with your network
- 💬 **Contribute** resources or improvements
- 💰 **Donate** via [PayPal](https://www.paypal.com/paypalme/cloudsec) (optional, fully community-run)

---

## 📜 License

- **Website Code**: MIT License - Feel free to fork and customize
- **Resource Descriptions**: Creative Commons Attribution
- **Linked Resources**: Property of their respective creators/owners
- **News Articles**: Linked to original sources with proper attribution

Copyright © 2023-2026 Cloud Security Office Hours

---

For the latest updates and announcements, follow us on Discord.
