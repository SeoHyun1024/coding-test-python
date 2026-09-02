"""
codeup.kr "내 제출 현황"(status.php) 페이지를 스크래핑해서, AC(정확한 풀이) 받은 코드를
GitHub 저장소에 커밋/푸시하는 백필(backfill) 스크립트.

status.php?user_id=<내아이디> 의 실제 HTML을 기반으로 만들었습니다. 구조:

  <table id=result-tab>
    <tr>
      <td>제출번호</td>                                 -> sid
      <td>사용자</td>
      <td><a href='problem.php?id=6098&rid=0' title='[기초-리스트] 성실한 개미(py)'>6098</a></td>  -> 문제번호 + 제목
      <td><a href="reinfo.php?st=4">정확한 풀이</a></td   -> 채점 결과 (AC일 때만 텍스트가 "정확한 풀이")
      <td>메모리</td> <td>시간</td>
      <td><a href=showsource.php?id=47676769>Python</a> | 수정 | <a href='downsource.php?id=47676769'>다운로드</a></td>
      <td>코드 길이</td>
      <td><a title='2026-09-01 16:43:59'>1일 전</a></td   -> title 속성에 정확한 제출 시각(KST)이 들어있음
    </tr>
    ...
  </table>
  <a href='status.php?user_id=...&top=...'>다음 →</a>    -> sid 커서 기반 페이지네이션

인증/설정 (환경변수 사용):
  - USERNAME  : codeup.kr 로그인 아이디 (필수, env에 미리 저장해두고 사용)
  - PHPSESSID : 로그인 폼을 자동화하는 대신, 이미 로그인된 브라우저의 세션 쿠키를 재사용합니다.
                브라우저 개발자도구(F12) -> Application/저장소 -> Cookies -> https://codeup.kr
                에서 PHPSESSID 값을 복사해 env로 저장하거나, 없다면 코드의 PASTE_YOUR_PHPSESSID_HERE
                자리에 직접 붙여넣기. (쿠키는 만료되면 다시 복사해야 합니다.)

저장 위치: https://github.com/SeoHyun1024/coding-test-python 저장소를 REPO_DIR 경로에
(없으면 자동 clone) 받아서, 그 안의 codeup/ 폴더에 문제별 코드 파일을 저장합니다.

동작 방식:
  1) 세션 쿠키로 status.php를 페이지네이션 따라가며 순회
  2) 결과가 "정확한 풀이"(AC)인 제출만 골라 문제번호별로 1개씩(기본: 가장 최근 AC) 모음
  3) 각 코드를 downsource.php?id={sid} 로 원본 그대로 다운로드해서 저장
  4) git commit --date 로 실제 제출 시각(KST)을 커밋 날짜로 지정
  5) 전부 끝나면 git push
"""

import os
import re
import subprocess
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# 이 스크립트와 같은 폴더에 .env 파일이 있으면 자동으로 읽어서 환경변수로 등록해줌
# (pip install python-dotenv 필요)
load_dotenv()


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value or value == "PASTE_YOUR_PHPSESSID_HERE":
        raise SystemExit(
            f"환경변수 {name}이 설정되어 있지 않습니다.\n"
            f"이 스크립트와 같은 폴더에 .env 파일을 만들고 `{name}=값` 한 줄을 추가하거나,\n"
            f"터미널에서 `export {name}=값` 실행 후 다시 실행하세요."
        )
    return value


BASE_URL = "https://codeup.kr"
USERNAME = _require_env("USERNAME")  # codeup 로그인 아이디
PHPSESSID = _require_env("PHPSESSID")  # 브라우저에서 복사한 세션 쿠키

REPO_URL = _require_env("REPO_URL")  # GitHub 저장소 URL (예:
REPO_DIR = Path("./")  # 로컬에 클론해둘 위치 (없으면 스크립트가 자동으로 clone)
CODEUP_SUBDIR = "codeup"  # 저장소 안에서 코드를 모아둘 하위 폴더

# 문제별로 AC가 여러 번이면 어떤 걸 남길지: "latest"(가장 최근 AC, 기본) 또는 "earliest"(최초로 푼 순간)
KEEP = "latest"

# language 텍스트 -> 파일 확장자
EXT_MAP = {
    "Python": "py",
    "C": "c",
    "C++": "cpp",
    "Java": "java",
}

session = requests.Session()
session.cookies.set("PHPSESSID", PHPSESSID, domain="codeup.kr")


def sanitize(name: str) -> str:
    return re.sub(r"[^\w\-]+", "_", name).strip("_")


def iter_submission_pages():
    """status.php 페이지를 '다음' 링크를 따라가며 순회, 매 페이지의 BeautifulSoup을 yield"""
    url = f"{BASE_URL}/status.php"
    params = {"user_id": USERNAME}
    seen_urls = set()

    while True:
        resp = session.get(url, params=params)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        yield soup

        next_link = None
        for a in soup.select("a"):
            if a.get_text(strip=True).startswith("다음"):
                next_link = a.get("href")
                break

        if not next_link or next_link in seen_urls:
            break
        seen_urls.add(next_link)

        url = f"{BASE_URL}/{next_link}"
        params = None  # 다음 페이지 링크에 쿼리스트링이 이미 포함되어 있음


def parse_rows(soup):
    """한 페이지의 각 제출 row에서 필요한 정보를 뽑아 dict로 yield"""
    table = soup.select_one("table#result-tab")
    if not table:
        return
    for tr in table.select("tbody tr"):
        tds = tr.find_all("td")
        if len(tds) < 9:
            continue

        sid = tds[0].get_text(strip=True)

        problem_a = tds[2].select_one("a")
        problem_id = problem_a.get_text(strip=True)
        problem_title = problem_a.get("title", "").strip()

        result_text = tds[3].get_text(strip=True)  # 예: "정확한 풀이", "시간 초과"

        lang_links = tds[6].select("a")
        language = lang_links[0].get_text(strip=True) if lang_links else ""
        download_href = None
        for a in lang_links:
            href = a.get("href", "")
            if "downsource.php" in href:
                download_href = href
                break

        time_a = tds[8].select_one("a")
        submitted_at = time_a.get("title", "").strip() if time_a else ""

        yield {
            "sid": sid,
            "problem_id": problem_id,
            "problem_title": problem_title,
            "result": result_text,
            "language": language,
            "download_href": download_href,
            "submitted_at": submitted_at,
        }


def collect_accepted_submissions(max_pages=500):
    """AC(정확한 풀이)만 걸러서 문제번호별로 하나씩 dict[problem_id] = row 로 모음"""
    picked = {}
    for page_no, soup in enumerate(iter_submission_pages(), start=1):
        if page_no > max_pages:
            break
        for row in parse_rows(soup):
            if row["result"] != "정확한 풀이":
                continue
            pid = row["problem_id"]
            if KEEP == "latest":
                # 최신 순으로 순회하므로 처음 만난 것이 가장 최근 AC -> 이후 것은 무시
                picked.setdefault(pid, row)
            else:  # "earliest"
                # 계속 덮어써서, 마지막에 남는 건 가장 오래된(=최초로 푼) AC
                picked[pid] = row
    return picked


def download_code(row) -> str:
    resp = session.get(f"{BASE_URL}/{row['download_href']}")
    resp.raise_for_status()
    return resp.text


def ensure_repo():
    """REPO_DIR에 저장소가 없으면 GitHub에서 clone"""
    if not (REPO_DIR / ".git").exists():
        print(f"{REPO_DIR} 에 {REPO_URL} 클론 중...")
        subprocess.run(["git", "clone", REPO_URL, str(REPO_DIR)], check=True)
    (REPO_DIR / CODEUP_SUBDIR).mkdir(parents=True, exist_ok=True)


def save_and_commit(row, code: str):
    ext = EXT_MAP.get(row["language"], "txt")
    title = sanitize(row["problem_title"]) or row["problem_id"]
    rel_path = f"{CODEUP_SUBDIR}/{row['problem_id']}_{title}.{ext}"
    file_path = REPO_DIR / rel_path
    file_path.write_text(code, encoding="utf-8")

    subprocess.run(["git", "-C", str(REPO_DIR), "add", rel_path], check=True)

    env = os.environ.copy()
    if row["submitted_at"]:
        env["GIT_AUTHOR_DATE"] = row["submitted_at"]
        env["GIT_COMMITTER_DATE"] = row["submitted_at"]

    commit_msg = f"solve: codeup {row['problem_id']} - {row['problem_title']}"
    result = subprocess.run(
        ["git", "-C", str(REPO_DIR), "commit", "-m", commit_msg],
        env=env,
    )
    if result.returncode != 0:
        print(f"  (커밋할 변경 사항 없음: {file_path.name})")


def main():
    ensure_repo()

    print("제출 목록 수집 중...")
    accepted = collect_accepted_submissions()
    print(f"AC 문제 {len(accepted)}개 발견")

    for pid in sorted(accepted, key=lambda x: int(x)):
        row = accepted[pid]
        print(f"- {pid} ({row['language']}, {row['submitted_at']}) 다운로드 중...")
        code = download_code(row)
        save_and_commit(row, code)

    print("push 중...")
    subprocess.run(["git", "-C", str(REPO_DIR), "push"], check=True)
    print("완료!")


if __name__ == "__main__":
    main()
