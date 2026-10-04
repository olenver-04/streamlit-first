import re
import uuid

import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI-CodeMentor", page_icon="💻", layout="wide")

try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    API_KEY = ""
try:
    MODEL = st.secrets["OPENAI_MODEL"]
except Exception:
    MODEL = "gpt-6-luna"

client = OpenAI(api_key=API_KEY) if API_KEY else None

st.markdown("""
<style>
.block-container{max-width:1200px;padding-top:1.2rem;padding-bottom:4rem}
.hero{padding:32px 36px;border-radius:24px;background:linear-gradient(135deg,#0f172a,#172554 55%,#1d4ed8 140%);color:white;margin-bottom:20px;box-shadow:0 18px 50px rgba(15,23,42,.15)}
.hero small{color:#bfdbfe;font-weight:800;letter-spacing:.12em;text-transform:uppercase}.hero h1{color:white;font-size:52px;line-height:1;margin:8px 0 12px}.hero p{color:#dbeafe;font-size:18px;line-height:1.6;max-width:850px}
.card{border:1px solid #e4e7ec;border-radius:18px;padding:18px;background:white;height:100%}.card h3{margin-top:0}.muted{color:#667085;line-height:1.55}
.pill{display:inline-block;border-radius:999px;padding:5px 10px;font-size:12px;font-weight:750;margin-right:6px}.blue{background:#eff6ff;color:#1d4ed8}.green{background:#ecfdf5;color:#047857}.amber{background:#fffbeb;color:#b45309}
.flow{border:1px solid #dbeafe;background:#f8fbff;border-radius:16px;padding:17px;text-align:center;color:#1e3a8a;font-weight:750;line-height:1.8}
.ok,.bad{border-radius:10px;padding:9px 11px;margin:6px 0;font-size:14px}.ok{background:#ecfdf5;color:#047857}.bad{background:#fef2f2;color:#b91c1c}
.ethics{border-left:4px solid #059669;background:#ecfdf5;color:#065f46;padding:13px 15px;border-radius:10px;line-height:1.55}
[data-testid="stMetric"]{border:1px solid #e4e7ec;border-radius:15px;padding:12px 14px;background:white}
.stButton>button{border-radius:11px;font-weight:750}
</style>
""", unsafe_allow_html=True)

TASKS = {
    "for": {
        "topic":"Цикл for","title":"Числа от 1 до 10","difficulty":"Лёгкая",
        "description":"С помощью цикла for выведите числа от 1 до 10 включительно, каждое с новой строки.",
        "starter":"""public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            System.out.println(i);
        }
    }
}
""",
        "hints":["Посмотрите на начальное значение счётчика. Какое число должно выводиться первым?","Проверьте обе границы диапазона: стартовое значение i и условие продолжения цикла.","Диапазон должен начинаться с 1 и включать число 10."],
    },
    "if": {
        "topic":"if / else","title":"Знак числа","difficulty":"Лёгкая",
        "description":"Для переменной n выведите «Положительное», «Отрицательное» или «Ноль».",
        "starter":"""public class Main {
    public static void main(String[] args) {
        int n = -7;
        // Напишите решение здесь
    }
}
""",
        "hints":["Нужно проверить три состояния: больше нуля, меньше нуля и равно нулю.","Сначала обработайте n > 0, затем отрицательное значение, а оставшийся случай — ноль.","Используйте цепочку if → else if → else."],
    },
    "while": {
        "topic":"Цикл while","title":"Обратный отсчёт","difficulty":"Лёгкая",
        "description":"С помощью while выведите числа от 10 до 1.",
        "starter":"""public class Main {
    public static void main(String[] args) {
        int i = 10;
        // Напишите while
    }
}
""",
        "hints":["Счётчик уже равен 10. При каком условии цикл должен продолжаться?","После каждого вывода значение i должно уменьшаться.","Внутри while выведите i и затем уменьшите его на 1."],
    },
    "constructor": {
        "topic":"ООП","title":"Конструктор Car","difficulty":"Средняя",
        "description":"Создайте класс Car с полями brand и year, конструктором и объектом Car в main.",
        "starter":"""class Car {
    String brand;
    int year;
    // Добавьте конструктор
}

public class Main {
    public static void main(String[] args) {
        // Создайте объект Car
    }
}
""",
        "hints":["Имя конструктора совпадает с именем класса.","Параметры можно присвоить через this.brand и this.year.","После конструктора создайте объект через new Car(...)."],
    },
}


def checks(task_id, code):
    compact = re.sub(r"\s+", " ", code)
    low = compact.lower()
    if task_id == "for":
        return [
            ("Использован for", bool(re.search(r"\bfor\s*\(", code))),
            ("Счётчик начинается с 1", bool(re.search(r"\bi\s*=\s*1\b", code))),
            ("Число 10 включено", bool(re.search(r"\bi\s*<=\s*10\b", code) or re.search(r"\bi\s*<\s*11\b", code))),
            ("Выводится i", bool(re.search(r"println\s*\(\s*i\s*\)", code))),
            ("Счётчик увеличивается", "i++" in compact or "++i" in compact or "i += 1" in compact),
        ]
    if task_id == "if":
        return [
            ("Есть if", bool(re.search(r"\bif\s*\(", code))),
            ("Проверяется n > 0", bool(re.search(r"\bn\s*>\s*0\b", code))),
            ("Проверяется n < 0", bool(re.search(r"\bn\s*<\s*0\b", code))),
            ("Есть else", "else" in low),
            ("Есть вывод", "system.out.println" in low),
        ]
    if task_id == "while":
        return [
            ("Использован while", bool(re.search(r"\bwhile\s*\(", code))),
            ("Старт с 10", bool(re.search(r"\bi\s*=\s*10\b", code))),
            ("Цикл доходит до 1", bool(re.search(r"\bi\s*>\s*0\b", code) or re.search(r"\bi\s*>=\s*1\b", code))),
            ("Выводится i", bool(re.search(r"println\s*\(\s*i\s*\)", code))),
            ("Счётчик уменьшается", "i--" in compact or "--i" in compact or "i -= 1" in compact),
        ]
    if task_id == "constructor":
        return [
            ("Есть class Car", bool(re.search(r"\bclass\s+Car\b", code))),
            ("Есть brand и year", "brand" in low and "year" in low),
            ("Есть конструктор Car(...) ", bool(re.search(r"\bCar\s*\([^)]*\)\s*\{", code))),
            ("Использован this", "this.brand" in low and "this.year" in low),
            ("Создаётся new Car", "new car(" in low),
        ]
    return []


def validate(task_id, code):
    items = checks(task_id, code)
    passed = sum(ok for _, ok in items)
    total = len(items)
    return {"items":items,"passed":passed,"total":total,"score":round(100*passed/total) if total else 0,"ok":total>0 and passed==total}


def get_ai_hint(task, code, result, level):
    if not client:
        return None
    failed = [name for name, ok in result["items"] if not ok]
    rule = {1:"Дай одну мягкую подсказку без кода.",2:"Объясни главную ошибку и следующий шаг без полного решения.",3:"Можно показать маленький исправленный фрагмент, но не всю программу."}[level]
    instructions = f"""Ты AI-CodeMentor — педагогический наставник начинающего студента колледжа по Java.
Отвечай по-русски, 2–5 коротких предложений. Не выполняй задание вместо студента.
Предварительная проверка не является реальной компиляцией, поэтому не утверждай, что код запускается.
Сфокусируйся на одной наиболее полезной правке. {rule}"""
    prompt = f"""Тема: {task['topic']}
Задание: {task['title']}
Условие: {task['description']}
Не пройдены проверки: {', '.join(failed) if failed else 'нет'}
Код студента:\n```java\n{code}\n```"""
    response = client.responses.create(model=MODEL, reasoning={"effort":"low"}, instructions=instructions, input=prompt, max_output_tokens=400)
    return response.output_text


if "cm_student" not in st.session_state:
    st.session_state.cm_student = "ST-" + uuid.uuid4().hex[:6].upper()
if "cm_attempts" not in st.session_state: st.session_state.cm_attempts = 0
if "cm_hints" not in st.session_state: st.session_state.cm_hints = 0
if "cm_done" not in st.session_state: st.session_state.cm_done = []
if "cm_levels" not in st.session_state: st.session_state.cm_levels = {}
if "cm_results" not in st.session_state: st.session_state.cm_results = {}

st.markdown("""
<div class="hero">
<small>Конкурс «Прорывные проекты» · направление «Искусственный интеллект в образовании»</small>
<h1>AI-CodeMentor</h1>
<p>Интеллектуальный цифровой наставник для персонализированного обучения программированию студентов колледжа.</p>
</div>
""", unsafe_allow_html=True)

status_col, id_col = st.columns([3,1])
with status_col:
    if client: st.success(f"AI online · {MODEL}")
    else: st.warning("AI API не настроен. Демо-проверка продолжает работать без AI.")
with id_col:
    st.caption(f"Обезличенный ID: `{st.session_state.cm_student}`")

about, practice, pilot, teacher, ethics = st.tabs(["О проекте","Практика Java","Апробация","Для преподавателя","Честность и данные"])

with about:
    st.subheader("Педагогическая проблема → решение")
    c1,c2,c3=st.columns(3)
    with c1: st.markdown('<div class="card"><h3>Проблема</h3><div class="muted">У студентов разный темп и уровень подготовки, а преподаватель не может одновременно дать каждому персональную обратную связь по коду.</div></div>',unsafe_allow_html=True)
    with c2: st.markdown('<div class="card"><h3>Цель</h3><div class="muted">Организовать персонализированную практику: проверка решения, поэтапные подсказки и повторная попытка без подмены самостоятельной работы.</div></div>',unsafe_allow_html=True)
    with c3: st.markdown('<div class="card"><h3>Целевая группа</h3><div class="muted">Студенты 1–2 курсов ТиПО, изучающие Java, алгоритмы и основы ООП.</div></div>',unsafe_allow_html=True)
    st.write("")
    st.markdown('<div class="flow">Задание → Код студента → Проверка → AI-подсказка → Повторная попытка → Прогресс</div>',unsafe_allow_html=True)
    st.write("")
    left,right=st.columns(2)
    with left:
        st.markdown("### Облачная версия")
        st.write("Публичная витрина на Streamlit: задания, структурная проверка, AI-подсказки и демонстрация методики. Доступна комиссии по ссылке без установки ПО.")
    with right:
        st.markdown("### Полная локальная версия")
        st.write("XAMPP + MySQL + javac + Docker sandbox + открытые/скрытые тесты + Teacher Studio. Предназначена для компьютерного класса.")
    st.markdown('<div class="ethics"><b>Ключевое отличие:</b> AI используется как педагогический слой. В полной версии технический результат определяют компилятор и тесты, а AI объясняет его студенту.</div>',unsafe_allow_html=True)

with practice:
    st.subheader("Практика Java")
    labels={k:f"{v['topic']} · {v['title']}" for k,v in TASKS.items()}
    task_id=st.selectbox("Задание",list(TASKS),format_func=lambda x:labels[x],key="cm_task")
    task=TASKS[task_id]
    st.markdown(f"<span class='pill blue'>{task['topic']}</span><span class='pill amber'>{task['difficulty']}</span>",unsafe_allow_html=True)
    st.markdown(f"### {task['title']}")
    st.write(task["description"])

    code_key=f"cm_code_{task_id}"
    editor_key=f"cm_editor_{task_id}"
    if code_key not in st.session_state: st.session_state[code_key]=task["starter"]
    left,right=st.columns([1.15,.85],gap="large")
    with left:
        code=st.text_area("Код студента",value=st.session_state[code_key],height=360,key=editor_key)
        st.session_state[code_key]=code
        a,b,c=st.columns([1.1,1,.8])
        with a: do_check=st.button("Проверить решение",type="primary",use_container_width=True)
        with b: do_hint=st.button("Получить подсказку",use_container_width=True)
        with c:
            if st.button("Сбросить",use_container_width=True):
                st.session_state[code_key]=task["starter"]
                st.session_state.pop(editor_key,None)
                st.session_state.cm_results.pop(task_id,None)
                st.rerun()
        if do_check:
            result=validate(task_id,code)
            st.session_state.cm_results[task_id]=result
            st.session_state.cm_attempts+=1
            if result["ok"] and task_id not in st.session_state.cm_done: st.session_state.cm_done.append(task_id)
        result=st.session_state.cm_results.get(task_id)
        if result:
            st.progress(result["score"]/100)
            st.caption(f"Предварительная структурная проверка: {result['passed']}/{result['total']} ({result['score']}%)")
            for name,ok in result["items"]:
                st.markdown(f'<div class="{"ok" if ok else "bad"}">{"✓" if ok else "✕"} {name}</div>',unsafe_allow_html=True)
            if result["ok"]: st.success("Структурные критерии выполнены. В полной версии следующий этап — javac и Docker-тесты.")
    with right:
        st.markdown("### AI-наставник")
        level=st.session_state.cm_levels.get(task_id,0)
        st.caption(f"Уровень помощи: {level}/3")
        if do_hint:
            level=min(level+1,3); st.session_state.cm_levels[task_id]=level; st.session_state.cm_hints+=1
            result_ai=validate(task_id,code)
            if client:
                with st.spinner("Анализирую код..."):
                    try: feedback=get_ai_hint(task,code,result_ai,level)
                    except Exception as exc:
                        feedback=None; st.error("AI временно недоступен"); st.caption(str(exc))
            else: feedback=None
            st.session_state[f"cm_feedback_{task_id}"]=feedback or task["hints"][level-1]
        feedback=st.session_state.get(f"cm_feedback_{task_id}")
        if feedback: st.info(feedback)
        else: st.info("Сначала попробуйте решить задачу. Если застрянете, получите подсказку по текущему коду.")
        st.markdown("#### Лестница помощи")
        st.write("**1 уровень:** направление мысли\n\n**2 уровень:** объяснение основной ошибки\n\n**3 уровень:** небольшой фрагмент исправления")
        st.caption("Облачная версия не запускает произвольный Java-код. Безопасный запуск реализован в локальном Docker sandbox.")

with pilot:
    st.subheader("Апробация и результативность")
    st.info("Публичный раздел подготовлен под реальные данные. Вымышленные результаты не используются.")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Входной результат","—");c2.metric("Итоговый результат","—");c3.metric("Среднее число попыток","—");c4.metric("Полезность 1–5","—")
    st.markdown("### План апробации")
    st.markdown("1. Входное задание без AI-CodeMentor.\n2. Работа в тренажёре с фиксацией попыток и подсказок.\n3. Итоговое сопоставимое задание.\n4. Короткая анонимная обратная связь.\n5. Сравнение показателей «до / после».")
    st.markdown("### Измеряемые показатели")
    a,b=st.columns(2)
    with a: st.write("• результат, %\n\n• число попыток\n\n• уровень подсказки\n\n• ошибки компиляции")
    with b: st.write("• доля пройденных тестов\n\n• выполненные задания\n\n• оценка полезности\n\n• анонимный комментарий")

with teacher:
    st.subheader("Для преподавателя")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Попыток в демо",st.session_state.cm_attempts)
    c2.metric("Подсказок",st.session_state.cm_hints)
    c3.metric("Выполнено",f"{len(st.session_state.cm_done)}/{len(TASKS)}")
    c4.metric("Прогресс",f"{round(len(st.session_state.cm_done)/len(TASKS)*100)}%")
    st.markdown("### Что есть в полной Teacher Studio")
    a,b,c=st.columns(3)
    with a: st.markdown('<div class="card"><h3>Контент</h3><div class="muted">Темы, задания, стартовый Java-код, сложность, уровни подсказок.</div></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="card"><h3>Тестирование</h3><div class="muted">javac, Docker sandbox, открытые и скрытые тест-кейсы, таймауты.</div></div>',unsafe_allow_html=True)
    with c: st.markdown('<div class="card"><h3>Аналитика</h3><div class="muted">Попытки, ошибки, тесты, подсказки, AI-ответы и проблемные темы группы.</div></div>',unsafe_allow_html=True)

with ethics:
    st.subheader("Академическая честность, этика и защита данных")
    items=[
        ("Минимизация данных","Используется обезличенный ID. ФИО, ИИН, телефон и адрес для практики не нужны."),
        ("Подсказка вместо ответа","AI повышает конкретность помощи по уровням и не должен сразу отдавать готовую программу."),
        ("Объективная проверка","В полной версии технический результат подтверждают javac и тесты, а не мнение AI."),
        ("Контроль преподавателя","Итоговое педагогическое оценивание остаётся за преподавателем."),
    ]
    for i in range(0,len(items),2):
        cols=st.columns(2)
        for col,(name,desc) in zip(cols,items[i:i+2]):
            with col: st.markdown(f'<div class="card"><h3>{name}</h3><div class="muted">{desc}</div></div>',unsafe_allow_html=True)
        st.write("")
    st.markdown('<div class="ethics"><b>Принцип:</b> AI-CodeMentor должен увеличивать самостоятельность студента, а не подменять её.</div>',unsafe_allow_html=True)

st.divider()
st.caption("AI-CodeMentor · облачная конкурсная версия")
