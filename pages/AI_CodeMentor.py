import re
import uuid

import streamlit as st
from openai import OpenAI


# =========================================================
# НАСТРОЙКИ
# =========================================================

st.set_page_config(
    page_title="AI-CodeMentor",
    page_icon="💻",
    layout="wide"
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
# ДИЗАЙН
# =========================================================

st.markdown("""
<style>

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
}

.hero {
    padding: 28px 32px;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #0f172a,
        #172554,
        #1d4ed8
    );
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

.status {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    background: #ecfdf5;
    color: #047857;
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
    font-family: Consolas, monospace !important;
    font-size: 14px !important;
    line-height: 1.55 !important;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# ЗАДАНИЯ
# =========================================================

TASKS = {

    "for": {
        "topic": "Цикл for",
        "title": "Числа от 1 до 10",
        "description":
            "Используя цикл for, выведите числа "
            "от 1 до 10 включительно. "
            "Каждое число должно выводиться с новой строки.",

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
            "Цикл должен начинаться с 1 и включать число 10."
        ]
    },


    "if": {
        "topic": "Условные операторы",
        "title": "Знак числа",
        "description":
            "Для переменной n определите её знак. "
            "Выведите «Положительное», "
            "«Отрицательное» или «Ноль».",

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
            "Используй конструкцию if → else if → else."
        ]
    },


    "while": {
        "topic": "Цикл while",
        "title": "Обратный отсчёт",
        "description":
            "Используя цикл while, "
            "выведите числа от 10 до 1.",

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
            "Используй i-- после System.out.println(i)."
        ]
    },


    "constructor": {
        "topic": "ООП",
        "title": "Конструктор класса Car",
        "description":
            "Создайте класс Car с полями brand и year. "
            "Добавьте конструктор и создайте объект "
            "класса Car в методе main.",

        "starter": """class Car {

    String brand;
    int year;

    // Конструктор

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
            "Объект создаётся с помощью new Car(...)."
        ]
    }
}


# =========================================================
# ПРОВЕРКА РЕШЕНИЯ
# =========================================================

def check_code(task_id, code):

    compact = re.sub(r"\\s+", " ", code)
    lower = compact.lower()

    if task_id == "for":

        return [
            (
                "Использован цикл for",
                bool(re.search(r"\\bfor\\s*\\(", code))
            ),

            (
                "Счётчик начинается с 1",
                bool(re.search(r"\\bi\\s*=\\s*1\\b", code))
            ),

            (
                "Число 10 включено в диапазон",
                bool(
                    re.search(r"\\bi\\s*<=\\s*10\\b", code)
                    or
                    re.search(r"\\bi\\s*<\\s*11\\b", code)
                )
            ),

            (
                "Выводится переменная i",
                bool(
                    re.search(
                        r"println\\s*\\(\\s*i\\s*\\)",
                        code
                    )
                )
            ),

            (
                "Счётчик увеличивается",
                (
                    "i++" in compact
                    or "++i" in compact
                    or "i += 1" in compact
                )
            )
        ]


    if task_id == "if":

        return [
            (
                "Использован оператор if",
                bool(re.search(r"\\bif\\s*\\(", code))
            ),

            (
                "Проверяется n > 0",
                bool(re.search(r"\\bn\\s*>\\s*0\\b", code))
            ),

            (
                "Проверяется n < 0",
                bool(re.search(r"\\bn\\s*<\\s*0\\b", code))
            ),

            (
                "Использован else",
                "else" in lower
            ),

            (
                "Есть вывод результата",
                "system.out.println" in lower
            )
        ]


    if task_id == "while":

        return [
            (
                "Использован цикл while",
                bool(re.search(r"\\bwhile\\s*\\(", code))
            ),

            (
                "Начальное значение i = 10",
                bool(re.search(r"\\bi\\s*=\\s*10\\b", code))
            ),

            (
                "Цикл доходит до 1",
                bool(
                    re.search(r"\\bi\\s*>\\s*0\\b", code)
                    or
                    re.search(r"\\bi\\s*>=\\s*1\\b", code)
                )
            ),

            (
                "Выводится i",
                bool(
                    re.search(
                        r"println\\s*\\(\\s*i\\s*\\)",
                        code
                    )
                )
            ),

            (
                "Переменная i уменьшается",
                (
                    "i--" in compact
                    or "--i" in compact
                    or "i -= 1" in compact
                )
            )
        ]


    if task_id == "constructor":

        return [
            (
                "Создан класс Car",
                bool(
                    re.search(
                        r"\\bclass\\s+Car\\b",
                        code
                    )
                )
            ),

            (
                "Есть поля brand и year",
                (
                    "brand" in lower
                    and
                    "year" in lower
                )
            ),

            (
                "Создан конструктор Car",
                bool(
                    re.search(
                        r"\\bCar\\s*\\([^)]*\\)\\s*\\{",
                        code
                    )
                )
            ),

            (
                "Используется this",
                (
                    "this.brand" in lower
                    and
                    "this.year" in lower
                )
            ),

            (
                "Создан объект Car",
                "new car(" in lower
            )
        ]


    return []


def calculate_result(task_id, code):

    checks = check_code(
        task_id,
        code
    )

    passed = sum(
        ok
        for _, ok in checks
    )

    total = len(checks)

    score = (
        round(
            passed
            / total
            * 100
        )
        if total
        else 0
    )

    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "score": score,
        "success": passed == total
    }


# =========================================================
# AI-ПОДСКАЗКА
# =========================================================

def get_ai_hint(
    task,
    code,
    result,
    level
):

    if not client:
        return None


    errors = [
        name
        for name, ok
        in result["checks"]
        if not ok
    ]


    if level == 1:

        level_instruction = """
Дай только одну лёгкую наводку.
Не показывай готовый код.
Заставь студента подумать самостоятельно.
"""


    elif level == 2:

        level_instruction = """
Объясни основную ошибку.
Подскажи, что именно нужно проверить.
Не давай полную программу.
"""


    else:

        level_instruction = """
Можно показать маленький исправленный
фрагмент проблемного места,
но не выдавай всю программу целиком.
"""


    system_instruction = f"""
Ты AI-CodeMentor.

Ты цифровой наставник начинающего
студента колледжа по Java.

Твоя задача — не решить задание
вместо студента, а помочь ему
самостоятельно найти ошибку.

Правила:

- отвечай на русском языке;
- используй простые слова;
- ответ должен быть коротким;
- 2–5 предложений;
- не выдавай полный код решения;
- обращай внимание на текущий код студента;
- выбери одну наиболее важную ошибку;
- не утверждай, что программа
  успешно скомпилирована;
- облачная версия выполняет
  структурную проверку кода.

Уровень помощи:

{level_instruction}
"""


    errors_text = (
        ", ".join(errors)
        if errors
        else
        "структурные проверки пройдены"
    )


    user_prompt = f"""
Тема:
{task["topic"]}

Задание:
{task["title"]}

Условие:
{task["description"]}

Не пройдены проверки:
{errors_text}

Код студента:

```java
{code}
