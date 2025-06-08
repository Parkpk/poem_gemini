# gemini.py
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("Gemini_API_KEY"))

def is_korean(text: str) -> bool:
    return any('\uac00' <= ch <= '\ud7a3' for ch in text)

def generate_three_poems(keywords: list[str]) -> list[tuple[str, str]]:
    joined = ", ".join(keywords)
    korean_mode = any(is_korean(kw) for kw in keywords)

    if korean_mode:
        prompt = (
            "다음 조건을 모두 만족하는 현대적인 감성의 한국어 시 3편을 생성해주세요:\n"
            "1) 시 본문에는 제시된 키워드를 모두 반영하세요.\n"
            "2) 각 시 제목에는 키워드를 하나도 포함하지 않아야 하며, 세 제목은 서로 달라야 합니다.\n"
            "3) 각 시 본문은 최소 10개 이상의 행으로 구성하고, 2~3연(단락)으로 작성합니다.\n"
            "4) 각 시마다 번호를 매기되 “1.”, “2.”, “3.” 으로 표기하고, 번호 다음 줄(두 줄 아래)에 “제목: <제목>”을 쓰세요.\n"
            "5) 출력 형식은 아래 예시와 정확히 일치해야 합니다:\n\n"
            "1.\n\n"
            "제목: 첫 번째 제목\n\n"
            "시의 첫 번째 행\n"
            "시의 두 번째 행\n"
            "...\n\n"
            "2.\n\n"
            "제목: 두 번째 제목\n\n"
            "시의 첫 번째 행\n"
            "...\n\n"
            "3.\n\n"
            "제목: 세 번째 제목\n\n"
            "시의 첫 번째 행\n"
            "...\n\n"
            f"키워드: {joined}"
        )
    else:
        prompt = (
            "Please generate 3 distinct modern-style poems in English, following these rules:\n"
            "1) Each poem body must use all of the given keywords; the Title must include none of them.\n"
            "2) The three Titles must be different from each other.\n"
            "3) Each poem body should have at least 10 lines, organized into 2–3 stanzas.\n"
            "4) Number each poem with “1.”, “2.”, “3.” on its own line, then two blank lines, then “Title: <title>”.\n"
            "5) Output in this exact format:\n\n"
            "1.\n\n"
            "Title: Your first title here\n\n"
            "Line 1 of poem 1\n"
            "Line 2 of poem 1\n"
            "...\n\n"
            "2.\n\n"
            "Title: Your second title here\n\n"
            "Line 1 of poem 2\n"
            "...\n\n"
            "3.\n\n"
            "Title: Your third title here\n\n"
            "Line 1 of poem 3\n"
            "...\n\n"
            f"Keywords: {joined}"
        )

    resp = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
    text = resp.text.strip()

    poems: list[tuple[str, str]] = []
    # 공통: “1.”, “2.”, “3.” 로 split
    parts = re.split(r"^\d+\.", text, flags=re.MULTILINE)
    for block in parts:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        # 첫 줄은 빈칸(제거 후), 두 번째 줄이 제목 마커인 줄을 찾음
        # lines[0] 이 제목일 수도 있어서 유연하게 처리
        title = ""
        body_lines: list[str] = []
        for i, line in enumerate(lines):
            if line.startswith("제목:") or line.startswith("Title:"):
                title = line.split(":",1)[1].strip()
                # 본문은 제목 다음 두 줄(즉 i+2 index)에 이어지는 행 전체
                body_lines = lines[i+2 :]
                break
        if title and body_lines:
            poems.append((title, "\n".join(body_lines).strip()))

    if len(poems) != 3:
        raise RuntimeError(f"시가 3편 파싱되지 않았습니다 (parsed {len(poems)}):\n{text}")

    return poems
