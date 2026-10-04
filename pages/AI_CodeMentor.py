import re
import uuid

import streamlit as st
from openai import OpenAI


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AI-CodeMentor",
    page_icon="💻",
    layout="wide",
)


# =========================================================
# OPENAI
# =========================================================

try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except Exception:
    API_KEY = ""

try:
    MODEL = st.secrets["OPENAI_MODEL"]
except Exception:
    MODEL = "gpt-6-luna"

client = OpenAI(api_key=API_KEY) if API_KEY else None


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
<style>
.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

.hero {
    padding: 28px 32px;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f172a, #172554, #1d4ed8);
    margin-bottom: 22px;
}

.hero h1 {
    margin: 0;
    color: white !important;
    font-size: 46px;
}

.hero p {
    margin-top: 10px;
    margin-bottom: 0;
    color: #dbeafe !important;
    font-size: 17px;
}

.task-box {
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 15px;
}

.check-ok {
    padding: 9px 12px;
    border-radius: 9px;
    margin: 6px 0;
    background: #ecfdf5;
    color: #047857;
    border: 1px solid #a7f3d0;
}

.check-bad {
    padding: 9px 12px;
    border-radius: 9px;
    margin: 6px 0;
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.ai-box {
    padding: 18px;
    border-radius: 16px;
    background: #172554;
    border: 1px solid #1d4ed8;
    min-height: 150px;
}

.ai-box h3 {
    color: white !important;
    margin-top: 0;
}

.ai-box p {
    color: #dbeafe !important;
    line-height: 1.6;
}

textarea {
    font-family: Consolas, "Courier New", monospace !important;
    font-size: 14px !important;
    line-height: 1.55 !important;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# TASKS
# =========================================================

TASKS = {
    "for": {
        "topic": "Цикл for",
        "title": "Числа от 1 до 10",
        "description": (
            "Используя цикл for, выведите числа от 1 до 10 включительно. "
            "Каждое число должно выводиться с новой строки."
        ),
        "starter": """public class Main {
    public static void main(String[] args) {
        for (int i = 0; i < 10; i++) {
            System.out.println(i);
        }
    }
}
""",
        "hints": [
            "Посмотри, с какого значения начинается переменная i.",
            "Проверь начальное значение i и условие завершения цикла.",
            "Цикл должен начинаться с 1 и включать число 10.",
        ],
    },
    "if": {
        "topic": "Условные операторы",
        "title": "Знак числа",
        "description": (
            "Для переменной n определите её знак. "
            "Выведите «Положительное», «Отрицательное» или «Ноль»."
        ),
        "starter": """public class Main {
    public static void main(String[] args) {
        int n = -7;

        // Напишите код здесь
    }
}
""",
        "hints": [
            "Подумай, какие три состояния может иметь число относительно нуля.",
            "Проверь сначала n > 0, затем n < 0.",
            "Используй конструкцию if → else if → else.",
        ],
    },
    "while": {
        "topic": "Цикл while",
        "title": "Обратный отсчёт",
        "description": "Используя цикл while, выведите числа от 10 до 1.",
        "starter": """public class Main {
    public static void main(String[] args) {
        int i = 10;

        // Напишите цикл while
    }
}
""",
        "hints": [
            "Начальное значение уже равно 10. Подумай над условием while.",
            "После каждого вывода переменную i необходимо уменьшать.",
            "Используй i-- после System.out.println(i).",
        ],
    },
    "constructor": {
        "topic": "ООП",
        "title": "Конструктор класса Car",
        "description": (
            "Создайте класс Car с полями brand и year. "
            "Добавьте конструктор и создайте объект класса Car в методе main."
        ),
        "starter": """class Car {
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
        "hints": [
            "Имя конструктора должно полностью совпадать с именем класса.",
            "Внутри конструктора можно использовать this.brand и this.year.",
            "Объект создаётся с помощью new Car(...).",
        ],
    },
}


# =========================================================
# STRUCTURAL CHECKS
# =========================================================

def check_code(task_id: str, code: str):
    compact = re.sub(r"\s+", " ", code)
    lower = compact.lower()

    if task_id == "for":
        return [
            ("Использован цикл for", bool(re.search(r"\bfor\s*\(", code))),
            ("Счётчик начинается с 1", bool(re.search(r"\bi\s*=\s*1\b", code))),
            (
                "Число 10 включено в диапазон",
                bool(
                    re.search(r"\bi\s*<=\s*10\b", code)
                    or re.search(r"\bi\s*<\s*11\b", code)
                ),
            ),
            (
                "Выводится переменная i",
                bool(re.search(r"println\s*\(\s*i\s*\)", code)),
            ),
            (
                "Счётчик увеличивается",
                "i++" in compact or "++i" in compact or "i += 1" in compact,
            ),
        ]

    if task_id == "if":
        return [
            ("Использован оператор if", bool(re.search(r"\bif\s*\(", code))),
            ("Проверяется n > 0", bool(re.search(r"\bn\s*>\s*0\b", code))),
            ("Проверяется n < 0", bool(re.search(r"\bn\s*<\s*0\b", code))),
            ("Использован else", "else" in lower),
            ("Есть вывод результата", "system.out.println" in lower),
        ]

    if task_id == "while":
        return [
            ("Использован цикл while", bool(re.search(r"\bwhile\s*\(", code))),
            ("Начальное значение i = 10", bool(re.search(r"\bi\s*=\s*10\b", code))),
            (
                "Цикл доходит до 1",
                bool(
                    re.search(r"\bi\s*>\s*0\b", code)
                    or re.search(r"\bi\s*>=\s*1\b", code)
                ),
            ),
            (
                "Выводится i",
                bool(re.search(r"println\s*\(\s*i\s*\)", code)),
            ),
            (
                "Переменная i уменьшается",
                "i--" in compact or "--i" in compact or "i -= 1" in compact,
            ),
        ]

    if task_id == "constructor":
        return [
            ("Создан класс Car", bool(re.search(r"\bclass\s+Car\b", code))),
            ("Есть поля brand и year", "brand" in lower and "year" in lower),
            (
                "Создан конструктор Car",
                bool(re.search(r"\bCar\s*\([^)]*\)\s*\{", code)),
            ),
            ("Используется this", "this.brand" in lower and "this.year" in lower),
            ("Создан объект Car", "new car(" in lower),
        ]

    return []


def calculate_result(task_id: str, code: str):
    checks = check_code(task_id, code)
    passed = sum(ok for _, ok in checks)
    total = len(checks)
    score = round((passed / total) * 100) if total else 0

    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "score": score,
        "success": total > 0 and passed == total,
    }


# =========================================================
# AI HINT
# =========================================================

def get_ai_hint(task, code, result, level):
    if not client:
        return None

    errors = [name for name, ok in result["checks"] if not ok]

    level_instruction = {
        1: "Дай одну лёгкую наводку. Не показывай готовый код.",
        2: "Объясни основную ошибку и следующий шаг. Не давай полную программу.",
        3: (
            "Можно показать небольшой исправленный фрагмент проблемного места, "
            "но не всю программу."
        ),
    }[level]

    instructions = f"""
Ты — AI-CodeMentor, цифровой наставник начинающего студента колледжа по Java.

Твоя задача — помочь студенту самостоятельно найти и исправить ошибку.

Правила:
- отвечай по-русски;
- используй простые слова;
- 2–5 коротких предложений;
- не выполняй всё задание за студента;
- не выдавай полный готовый код;
- сфокусируйся на одной наиболее важной ошибке;
- облачная версия выполняет только структурную проверку, а не реальную компиляцию Java;
- не утверждай, что программа успешно скомпилировалась или запустилась.

Уровень помощи:
{level_instruction}
"""

    errors_text = ", ".join(errors) if errors else "структурные проверки пройдены"

    prompt = f"""
Тема: {task["topic"]}
Задание: {task["title"]}
Условие: {task["description"]}

Не пройдены проверки:
{errors_text}

Код студента:
```java
{code}
```

Дай следующую педагогическую подсказку.
"""

    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "low"},
        instructions=instructions,
        input=prompt,
        max_output_tokens=400,
    )

    return response.output_text


# =========================================================
# SESSION
# =========================================================

if "cm_student_id" not in st.session_state:
    st.session_state.cm_student_id = "ST-" + uuid.uuid4().hex[:6].upper()

if "cm_results" not in st.session_state:
    st.session_state.cm_results = {}

if "cm_hint_levels" not in st.session_state:
    st.session_state.cm_hint_levels = {}

if "cm_attempts" not in st.session_state:
    st.session_state.cm_attempts = 0


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="hero">
    <h1>💻 AI-CodeMentor</h1>
    <p>
        Пиши Java-код, проверяй решение и получай поэтапные AI-подсказки,
        не раскрывающие готовый ответ сразу.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

status_col, id_col = st.columns([3, 1])

with status_col:
    if client:
        st.success(f"AI подключён · {MODEL}")
    else:
        st.warning("OpenAI API не подключён. Будут использоваться локальные подсказки.")

with id_col:
    st.caption(f"ID студента: `{st.session_state.cm_student_id}`")


# =========================================================
# TASK
# =========================================================

task_names = {
    key: f"{value['topic']} — {value['title']}"
    for key, value in TASKS.items()
}

task_id = st.selectbox(
    "Выберите задание",
    list(TASKS.keys()),
    format_func=lambda key: task_names[key],
)

task = TASKS[task_id]

st.markdown(
    f"""
<div class="task-box">
    <b>{task["topic"]}</b>
    <h3>{task["title"]}</h3>
    <div>{task["description"]}</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# MAIN
# =========================================================

editor_col, ai_col = st.columns([1.2, 0.8], gap="large")

with editor_col:
    st.subheader("Ваш код")

    code_key = f"cm_code_{task_id}"
    editor_key = f"cm_editor_{task_id}"

    if code_key not in st.session_state:
        st.session_state[code_key] = task["starter"]

    code = st.text_area(
        "Редактор Java",
        value=st.session_state[code_key],
        height=400,
        key=editor_key,
        label_visibility="collapsed",
    )

    st.session_state[code_key] = code

    b1, b2, b3 = st.columns(3)

    with b1:
        check_button = st.button(
            "▶ Проверить",
            type="primary",
            use_container_width=True,
        )

    with b2:
        hint_button = st.button(
            "💡 Подсказка",
            use_container_width=True,
        )

    with b3:
        reset_button = st.button(
            "↻ Сбросить",
            use_container_width=True,
        )

    if reset_button:
        st.session_state[code_key] = task["starter"]
        st.session_state.pop(editor_key, None)
        st.session_state.cm_results.pop(task_id, None)
        st.session_state.cm_hint_levels[task_id] = 0
        st.session_state.pop(f"cm_feedback_{task_id}", None)
        st.rerun()

    if check_button:
        result = calculate_result(task_id, code)
        st.session_state.cm_results[task_id] = result
        st.session_state.cm_attempts += 1

    result = st.session_state.cm_results.get(task_id)

    if result:
        st.markdown("### Результат проверки")
        st.progress(result["score"] / 100)

        st.write(
            f"Пройдено: **{result['passed']} из {result['total']}** "
            f"— результат **{result['score']}%**"
        )

        for name, ok in result["checks"]:
            css_class = "check-ok" if ok else "check-bad"
            icon = "✓" if ok else "✕"

            st.markdown(
                f'<div class="{css_class}">{icon} {name}</div>',
                unsafe_allow_html=True,
            )

        if result["success"]:
            st.success("Отлично! Все структурные проверки пройдены.")


with ai_col:
    st.subheader("AI-наставник")

    hint_level = st.session_state.cm_hint_levels.get(task_id, 0)
    st.caption(f"Уровень подсказки: {hint_level}/3")

    if hint_button:
        hint_level = min(hint_level + 1, 3)
        st.session_state.cm_hint_levels[task_id] = hint_level

        current_result = calculate_result(task_id, code)
        feedback = None

        if client:
            with st.spinner("AI анализирует ваш код..."):
                try:
                    feedback = get_ai_hint(
                        task,
                        code,
                        current_result,
                        hint_level,
                    )
                except Exception as error:
                    st.error("Не удалось получить ответ от AI.")
                    st.caption(str(error))

        if not feedback:
            feedback = task["hints"][hint_level - 1]

        st.session_state[f"cm_feedback_{task_id}"] = feedback

    feedback = st.session_state.get(f"cm_feedback_{task_id}")

    if feedback:
        st.markdown(
            f"""
<div class="ai-box">
    <h3>🤖 AI-CodeMentor</h3>
    <p>{feedback}</p>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
<div class="ai-box">
    <h3>🤖 AI-CodeMentor</h3>
    <p>
        Попробуйте сначала решить задачу самостоятельно.
        Если возникнет затруднение, нажмите «Подсказка».
        Помощь будет становиться конкретнее постепенно.
    </p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("#### Уровни помощи")
    st.markdown(
        """
**1 уровень** — лёгкая наводка.  
**2 уровень** — объяснение основной ошибки.  
**3 уровень** — небольшой фрагмент исправления.
"""
    )


# =========================================================
# FOOTER STATS
# =========================================================

st.divider()

m1, m2, m3 = st.columns(3)

m1.metric("Попыток", st.session_state.cm_attempts)

m2.metric(
    "Уровень подсказки",
    st.session_state.cm_hint_levels.get(task_id, 0),
)

current_result = st.session_state.cm_results.get(task_id)

m3.metric(
    "Результат",
    f"{current_result['score']}%" if current_result else "—",
)

st.caption("AI-CodeMentor · облачная версия")

