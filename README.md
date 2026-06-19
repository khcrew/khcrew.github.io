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

저장소 **Settings → Secrets and variables → Actions**에 아래 설정을 등록합니다.

#### 1. Secrets 등록
- `.env`에 정의된 API 키들과 변수들을 동일한 이름으로 등록합니다.
- `FIREBASE_CREDENTIALS`: `firebase-credentials.json` 파일 내용(raw JSON)을 복사하여 그대로 입력합니다.
- `GH_PAT`: 공유 소스코드 리포지토리(`khfamily/khfamily.github.io`)의 공통 모듈 및 스크립트를 가져오기 위해 필요한 Personal Access Token입니다.

> **GH_PAT 발급 방법 (Classic)**
> 1. GitHub 우측 상단 프로필 클릭 → **Settings** 이동.
> 2. 좌측 사이드바 최하단 **Developer settings** 이동.
> 3. **Personal access tokens** → **Tokens (classic)** 클릭.
> 4. **Generate new token** → **Generate new token (classic)** 클릭.
> 5. Note에 용도 입력(예: `khcrew-shared-checkout`), Scopes에서 **`repo`**를 체크하고 생성합니다.
> 6. 생성 완료된 토큰 값(ghp_...)을 복사하여 저장소 Secret에 `GH_PAT`로 등록합니다.

#### 2. GitHub Pages 설정
- 저장소 **Settings → Pages** 이동.
- **Build and deployment**의 **Source**를 **GitHub Actions**로 변경하여 배포를 활성화합니다.

#### 3. Workflow 권한 설정 (자동 커밋 허용)
- 저장소 **Settings → Actions → General** 이동.
- 최하단 **Workflow permissions** 영역에서 **Read and write permissions**를 활성화해야 생성된 새 포스트 커밋 및 푸시가 정상 작동합니다.

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
