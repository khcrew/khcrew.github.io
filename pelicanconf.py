import os

# ── Site ──────────────────────────────────────────────────────
AUTHOR   = '경희가족한의원'
SITENAME = '경희가족한의원 건강 블로그'
TIMEZONE     = 'Asia/Seoul'
DEFAULT_LANG = 'ko'

# ── Dev server ────────────────────────────────────────────────
PORT = 9000
SITEURL  = os.environ.get('SITEURL', f'http://localhost:{PORT}')

# ── Paths ─────────────────────────────────────────────────────
PATH         = 'site/content'
OUTPUT_PATH  = 'output'
ARTICLE_PATHS = ['posts']
STATIC_PATHS  = ['extra']
EXTRA_PATH_METADATA = {
    'extra/robots.txt':   {'path': 'robots.txt'},
    'extra/favicon.ico':  {'path': 'favicon.ico'},
}
DELETE_OUTPUT_DIRECTORY = True

# ── URLs ──────────────────────────────────────────────────────
RELATIVE_URLS      = False
DEFAULT_PAGINATION = 10
ARTICLE_URL        = 'posts/{slug}.html'
ARTICLE_SAVE_AS    = 'posts/{slug}.html'
AUTHOR_URL         = ''
AUTHOR_SAVE_AS     = ''
AUTHORS_SAVE_AS    = ''

# ── Category ──────────────────────────────────────────────────
USE_FOLDER_AS_CATEGORY = False
DEFAULT_CATEGORY       = '건강정보'

# ── Feed ──────────────────────────────────────────────────────
FEED_ALL_ATOM          = 'feeds/all.atom.xml'
FEED_ALL_RSS           = 'feeds/all.rss.xml'
RSS_FEED_SUMMARY_ONLY  = False
CATEGORY_FEED_ATOM     = None
TRANSLATION_FEED_ATOM  = None
AUTHOR_FEED_ATOM       = None
AUTHOR_FEED_RSS        = None

# ── Theme ─────────────────────────────────────────────────────
THEME = 'theme'

SITE_DESCRIPTION       = '대전 관평동 경희가족한의원의 건강 정보 블로그입니다. 한의학 치료와 질환별 건강 정보를 제공합니다.'
SITE_SUBTITLE          = '대전 관평동 경희가족한의원<br>건강 정보 블로그'
SITE_OG_LOCALE         = 'ko_KR'
BUSINESS_ADDRESS_LOCALITY = '대전 관평동'
GOOGLE_ANALYTICS       = ''

# ── Plugins ───────────────────────────────────────────────────
PLUGINS = ['sitemap']
SITEMAP = {
    'format': 'xml',
    'priorities':  {'articles': 0.8, 'indexes': 0.5, 'pages': 0.5},
    'changefreqs': {'articles': 'weekly', 'indexes': 'daily', 'pages': 'monthly'},
    'exclude': [r'^tag/', r'^author/', r'^category/', r'^(authors|categories)\.html$'],
}
