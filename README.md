# 경희가족한의원 서브블로그 자동화

네이버 블로그를 크롤링하고, Gemini로 새 글을 생성해 GitHub Pages에 자동 발행하는 파이프라인.

GitHub Actions을 통해 자동 실행.

---

## Quick Start

```bash
uv sync
cp .env.example .env   # API 키 입력 후 저장
```

최초 1회만 실행 — 기존 네이버 블로그 포스트를 Firebase에 적재합니다.

```bash
uv run python scripts/init_1_fetch_post_list.py
uv run python scripts/init_2_crawl_posts.py
uv run python scripts/daily_2_generate_embeddings.py
uv run python scripts/daily_3_upload_firebase.py
```

이후 매일 실행:

```bash
uv run python main.py
```

---

## 상세 설정

### Firebase 서비스 계정 키 발급

Firebase Console → 프로젝트 설정 → 서비스 계정 → **새 비공개 키 생성** 후 `firebase-credentials.json`으로 저장.

### GitHub Actions

저장소 **Settings → Secrets and variables**에 아래를 등록합니다.

- Secrets: `.env`의 키들을 동일한 이름으로 등록. `FIREBASE_CREDENTIALS`는 `firebase-credentials.json` 파일 내용(raw JSON)을 값으로 입력.
- GitHub Pages: Settings → Pages → Source를 `gh-pages` 브랜치로 설정.

---

## 단계별 실행 및 필요 환경변수

```
Naver Blog RSS
      │
      ▼
 daily_1: 신규 포스트 크롤링
      │
      ▼
 daily_2: 임베딩 생성 ──── GEMINI_API_KEY*
      │
      ▼
 daily_3: Firebase 업로드 ──── FIREBASE_CREDENTIALS*
      │
      ▼
 daily_4: 글 생성 ──────────── GEMINI_API_KEY*
      │                         FIREBASE_CREDENTIALS*
      │                         MINIMAX_API_KEY (선택, fallback)
      ▼
 daily_5: Pelican 빌드 → gh-pages 발행
      │
      ▼
 main.py 알림 ───────────────── TELEGRAM_BOT_TOKEN
                                 TELEGRAM_CHAT_ID
```

- `GEMINI_API_KEY*`: `GEMINI_API_KEY`로 시작하는 변수를 자동 탐지해 멀티키 로테이션 (Quota 소진 시 다음 키로 전환)
- `FIREBASE_CREDENTIALS*`: 로컬은 `FIREBASE_CREDENTIALS_PATH`(파일 경로), GitHub Actions는 `FIREBASE_CREDENTIALS`(JSON 직접 입력)

```bash
uv run python scripts/daily_1_crawl_new_posts.py
uv run python scripts/daily_2_generate_embeddings.py
uv run python scripts/daily_3_upload_firebase.py
uv run python scripts/daily_4_generate_post.py [--topic 주제] [--query-id logNo]
uv run python scripts/daily_5_publish_site.py
```

`daily_4`는 Firebase에서 랜덤 포스트를 기준으로 유사 포스트 5개를 선택해 글을 생성합니다. Gemini 실패 시 MiniMax로 자동 전환하며, 후처리로 외국어 문자 교정 및 전화번호 제거가 적용됩니다.

---

## 로컬 미리보기

```bash
uv run python -m pelican site/content -o output -s pelicanconf.py --listen
```
