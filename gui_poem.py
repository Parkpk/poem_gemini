# gui_poem.py

import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from dotenv import load_dotenv
from gemini import generate_three_poems  # gemini.py에 정의한 함수

# 1) .env에서 API 키 로드
load_dotenv()
if not os.getenv("Gemini_API_KEY"):
    raise RuntimeError("환경변수 Gemini_API_KEY가 설정되어 있지 않습니다.")

# 2) 콜백: 버튼 클릭 시 실행
def on_generate():
    kw1 = entry1.get().strip()
    kw2 = entry2.get().strip()
    kw3 = entry3.get().strip()
    if not (kw1 and kw2 and kw3):
        messagebox.showerror("입력 오류", "세 개의 키워드를 모두 입력해주세요.")
        return

    # 버튼 비활성화 & 출력영역 초기화
    btn_generate.config(state="disabled")
    output_txt.delete("1.0", tk.END)

    try:
        poems = generate_three_poems([kw1, kw2, kw3])
    except Exception as e:
        messagebox.showerror("생성 오류", f"시 생성 중 오류가 발생했습니다:\n{e}")
        btn_generate.config(state="normal")
        return

    # 출력
    for idx, (title, body) in enumerate(poems, start=1):
        output_txt.insert(tk.END, f"[버전 {idx}] {title}\n\n")
        output_txt.insert(tk.END, body + "\n")
        output_txt.insert(tk.END, "\n" + ("-"*40) + "\n\n")

    btn_generate.config(state="normal")


# 3) Tkinter 윈도우 구성
root = tk.Tk()
root.title("Gemini 시 생성기")

frm = tk.Frame(root, padx=10, pady=10)
frm.pack()

# 입력 필드
tk.Label(frm, text="첫 번째 키워드:").grid(row=0, column=0, sticky="e")
entry1 = tk.Entry(frm, width=15)
entry1.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frm, text="두 번째 키워드:").grid(row=1, column=0, sticky="e")
entry2 = tk.Entry(frm, width=15)
entry2.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frm, text="세 번째 키워드:").grid(row=2, column=0, sticky="e")
entry3 = tk.Entry(frm, width=15)
entry3.grid(row=2, column=1, padx=5, pady=2)

# Generate 버튼
btn_generate = tk.Button(frm, text="Generate 3 Poems", command=on_generate)
btn_generate.grid(row=3, column=0, columnspan=2, pady=10)

# 출력용 스크롤 텍스트
output_txt = scrolledtext.ScrolledText(root, width=60, height=20, wrap=tk.WORD)
output_txt.pack(padx=10, pady=(0,10))

root.mainloop()
