import difflib, tokenize, re, sys, os, time, io, json, random
from io import BytesIO

# --- АВТО-ИМПОРТЫ ---
try:
    import pyautogui, flask
    from PIL import ImageGrab
    from flask import Flask, send_file
except: pass

# --- НАСТРОЙКИ ---
ПОКАЗЫВАТЬ_ОШИБКИ = True

# --- МЕГА-СЛОВАРЬ (v1.5.5) ---
VOCABULARY = {
    'если':'if', 'иначе':'else', 'иначе_если':'elif', 'для':'for', 'в':'in',
    'пока':'while', 'прервать':'break', 'продолжить':'continue', 'функция':'def',
    'вернуть':'return', 'класс':'class', 'пасс':'pass', 'Истина':'True', 'Ложь':'False',
    'Ничего':'None', 'и':'and', 'или':'or', 'не':'not', 'импорт':'import', 'из':'from', 'как':'as',
    'с': 'with', # ДОБАВЛЕНО: для работы с блоками файлов
    
    'напечатать':'print', 'вывести':'print', 'ввод':'input', 'диапазон':'range', 'длина':'len',
    'целое':'int', 'число':'float', 'строка':'str', 'список':'list', 'словарь':'dict',
    'разбить':'split', 'выбор':'choice', 'рандом':'random', 'радиус':'randint',
    
    'список_файлов': 'listdir', 'путь': 'path', 'это_файл': 'path.isfile',
    'архив': 'zipfile', 'создать_архив': 'zipfile.ZipFile', 'СЖАТИЕ': 'zipfile.ZIP_DEFLATED',
    'добавить': 'write', 'закрыть': 'close', 'открыть': 'open',
    
    'джсон': 'json', # ДОБАВЛЕНО: для памяти ИИ
    'сохранить_память': 'dump',
    'загрузить_память': 'load',

    'Урсина':'ursina', 'Мир':'Ursina', 'Сущность':'Entity', 'выполнить':'run',
    'мышь':'pyautogui', 'клик':'click', 'скриншот':'grab',
    'сон':'time.sleep', 'система':'os', 'команда':'os.system'
}

def translate_code(code):
    if not code.strip(): return ""
    code = code.replace('ф\\', 'f"')
    for ru, en in VOCABULARY.items():
        code = code.replace(f'\\{ru}\\', f'"{en}"')
    code = code.replace('\\', '"')
    lines = code.split('\n')
    for i, line in enumerate(lines):
        s = line.rstrip()
        if s.endswith(','): lines[i] = s[:-1] + ':'
    code = '\n'.join(lines)
    try:
        tokens = list(tokenize.tokenize(BytesIO(code.encode('utf-8')).readline))
        res = []
        for t_type, t_str, *_ in tokens:
            if t_type == tokenize.NAME and t_str in VOCABULARY: t_str = VOCABULARY[t_str]
            res.append((t_type, t_str))
        return tokenize.untokenize(res).decode('utf-8')
    except: return code

def execute_ru_code(code):
    try: exec(translate_code(code), globals())
    except Exception as e:
        if ПОКАЗЫВАТЬ_ОШИБКИ: print(f"\n🌸 Заботушка: Ошибка -> {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if os.path.exists(sys.argv[1]):
            with open(sys.argv[1], 'r', encoding='utf-8') as f: execute_ru_code(f.read())
            input("\nНажми Enter для выхода...")
    else:
        print(f"🇷🇺 РуПайтон v1.5.5 | Готов сохранять разум!")
        while True:
            try:
                inp = input("\n>>> ").strip()
                if inp.lower() in ['выход', 'exit']: break
                if not inp: continue
                if inp.endswith((':', ',')) or inp.startswith('@'):
                    lines = [inp]
                    while True:
                        line = input("... "); 
                        if not line.strip(): break
                        lines.append(line)
                    inp = '\n'.join(lines)
                execute_ru_code(inp)
            except KeyboardInterrupt: break