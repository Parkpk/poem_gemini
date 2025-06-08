# gui_poem_psg.py

import os
import PySimpleGUI as sg
from dotenv import load_dotenv
from gemini import generate_three_poems

# 1) 환경 변수 로드
load_dotenv()
if not os.getenv("Gemini_API_KEY"):
    sg.popup_error("환경변수 오류", "`.env`에 Gemini_API_KEY를 설정해주세요.")
    exit(1)

# 2) 테마 설정
sg.theme('DarkTeal9')   # 어두운 청록색 계열 테마
FONT = ('맑은 고딕', 12)

# 3) 레이아웃 정의
layout = [
    [sg.Text('🔑 첫 번째 키워드', size=(15,1), font=FONT), sg.InputText(key='-KW1-', size=(20,1), font=FONT)],
    [sg.Text('🔑 두 번째 키워드', size=(15,1), font=FONT), sg.InputText(key='-KW2-', size=(20,1), font=FONT)],
    [sg.Text('🔑 세 번째 키워드', size=(15,1), font=FONT), sg.InputText(key='-KW3-', size=(20,1), font=FONT)],
    [sg.Button('📜 Generate 3 Poems', key='-GO-', font=FONT, size=(20,1))],
    [sg.HorizontalSeparator()],
    [sg.Multiline('', key='-OUTPUT-', size=(70,20), font=FONT, disabled=True, autoscroll=True)]
]

# 4) 윈도우 생성
window = sg.Window('✨ Gemini 시 생성기 ✨', layout, resizable=True)

# 5) 이벤트 루프
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == '-GO-':
        kw1, kw2, kw3 = values['-KW1-'].strip(), values['-KW2-'].strip(), values['-KW3-'].strip()
        if not (kw1 and kw2 and kw3):
            sg.popup_error("입력 오류", "세 개의 키워드를 모두 입력해주세요.")
            continue

        window['-GO-'].update(disabled=True)
        window['-OUTPUT-'].update("시 생성 중...\n")
        window.refresh()

        try:
            poems = generate_three_poems([kw1, kw2, kw3])
        except Exception as e:
            sg.popup_error("생성 오류", str(e))
            window['-GO-'].update(disabled=False)
            continue

        # 결과 출력
        out = []
        for idx, (title, body) in enumerate(poems, start=1):
            out.append(f"[버전 {idx}] {title}\n")
            out.append(body + "\n")
            out.append("-"*60 + "\n")
        window['-OUTPUT-'].update(''.join(out))
        window['-GO-'].update(disabled=False)

window.close()
