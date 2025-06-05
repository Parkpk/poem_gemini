import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("Gemini_API_KEY"))

def generate_poem(keywords: list) -> tuple[str, str]:
    """
    주어진 키워드들을 모두 반영하되, 제목에는 절대 키워드를 포함하지 않는 현대 시를 생성합니다.
    1) 제목: 키워드를 사용하지 않고 창의적으로 짓기
    2) 본문: 최소 3개 이상의 행으로 나뉜 시
    반환 형식:
      (title, poem_text)
    """
    # 키워드를 쉼표로 합치기
    joined = ", ".join(keywords)
    # 모델에게 보낼 프롬프트
    prompt = (
        "다음 조건을 모두 만족하는 현대적인 감성의 시를 1편 생성해주세요.\n"
        "1) 제시된 키워드들을 시 본문(내용)에 모두 반영한다.\n"
        "2) 시 제목은 반드시 키워드를 *하나도 포함하지 않아야* 한다.\n"
        "3) 제목은 독창적으로 짓되, 키워드가 없는 일반 단어로만 구성한다.\n"
        "4) 시 본문은 최소 3개 이상의 행(개행)으로 구성한다.\n"
        "5) 출력 형식:\n"
        "   제목: <여기에 제목을 작성>\n"
        "\n"
        "   <시의 첫 번째 행>\n"
        "   <시의 두 번째 행>\n"
        "   <...>\n"
        "\n"
        f"키워드: {joined}"
    )

    response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
    text = response.text.strip()

    # 생성된 텍스트를 줄 단위로 나눔
    lines = text.splitlines()
    title = ""
    poem_lines = []

    # 첫 줄이 "제목:"으로 시작하는지 확인
    if lines and lines[0].startswith("제목:"):
        # 제목 부분 추출 (콜론 이후 내용)
        title = lines[0].replace("제목:", "").strip()

        # 2번째 줄이 빈 줄이라고 가정하고, 3번째 줄부터 시 본문으로 간주
        poem_lines = lines[2:]
    else:
        # 만약 "제목:"이 없으면, title 빈 문자열 처리 후 전체를 시 본문으로 간주
        poem_lines = lines

    poem = "\n".join(poem_lines).strip()
    return title, poem
