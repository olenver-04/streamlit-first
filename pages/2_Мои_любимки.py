import streamlit as st
from pathlib import Path
import base64


# =========================================================
# НАСТРОЙКИ СТРАНИЦЫ
# =========================================================

st.set_page_config(
    page_title="Мои любимки <3",
    page_icon="❤️",
    layout="wide"
)


# =========================================================
# ПУТИ К ФАЙЛАМ
# =========================================================

# Сам файл находится:
# pages/2_Мои_любимки.py
#
# .parent        -> pages
# .parent.parent -> корень проекта

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"

FRIEND1 = ASSETS_DIR / "friend1.jpg"
FRIEND2 = ASSETS_DIR / "friend2.jpg"
FRIEND3 = ASSETS_DIR / "friend3.jpg"

SONG = ASSETS_DIR / "song.mp3"


# =========================================================
# ФУНКЦИЯ ДЛЯ ФОТО
# =========================================================

def image_to_base64(path):

    if not path.exists():
        return None

    with open(path, "rb") as image_file:

        encoded = base64.b64encode(
            image_file.read()
        ).decode()

    return encoded


friend1_base64 = image_to_base64(FRIEND1)
friend2_base64 = image_to_base64(FRIEND2)
friend3_base64 = image_to_base64(FRIEND3)


# =========================================================
# ОСНОВНОЙ CSS
# =========================================================

st.markdown(
    """
<style>

/* =========================================
   ФОН
========================================= */

.stApp {

    background:
        radial-gradient(
            circle at 20% 10%,
            rgba(255, 140, 180, 0.35),
            transparent 35%
        ),

        radial-gradient(
            circle at 80% 20%,
            rgba(255, 80, 130, 0.30),
            transparent 40%
        ),

        linear-gradient(
            135deg,
            #290018,
            #4d0028,
            #210012
        );

    background-attachment: fixed;
}


/* =========================================
   ОСНОВНОЙ КОНТЕЙНЕР
========================================= */

.block-container {

    max-width: 1200px;

    padding-top: 3rem;

    padding-bottom: 6rem;
}


/* =========================================
   ЗАГОЛОВОК
========================================= */

.hero {

    text-align: center;

    margin-bottom: 40px;

    padding: 50px 20px;

    border-radius: 35px;

    background:
        rgba(255,255,255,0.08);

    backdrop-filter:
        blur(20px);

    border:
        1px solid
        rgba(255,255,255,0.15);

    box-shadow:
        0 25px 80px
        rgba(0,0,0,0.30);
}


.main-title {

    font-size: 70px;

    font-weight: 900;

    color: white;

    margin: 0;

    text-shadow:

        0 5px 20px
        rgba(255, 40, 110, 0.45);

    animation:
        heartbeat 1.8s infinite;
}


.hero-subtitle {

    margin-top: 15px;

    font-size: 21px;

    color:
        rgba(255,255,255,0.8);
}


@keyframes heartbeat {

    0% {
        transform: scale(1);
    }

    10% {
        transform: scale(1.035);
    }

    20% {
        transform: scale(1);
    }

    30% {
        transform: scale(1.035);
    }

    40% {
        transform: scale(1);
    }

}


/* =========================================
   ЗАГОЛОВКИ РАЗДЕЛОВ
========================================= */

.section-title {

    text-align: center;

    color: white;

    font-size: 35px;

    font-weight: 800;

    margin-top: 25px;

    margin-bottom: 30px;
}


/* =========================================
   КАРТОЧКИ ДРУЗЕЙ
========================================= */

.friend-card {

    background:
        rgba(255,255,255,0.10);

    backdrop-filter:
        blur(15px);

    border-radius: 25px;

    overflow: hidden;

    border:
        1px solid
        rgba(255,255,255,0.16);

    box-shadow:
        0 20px 50px
        rgba(0,0,0,0.25);

    transition:
        transform 0.35s ease,
        box-shadow 0.35s ease;

    margin-bottom: 20px;
}


.friend-card:hover {

    transform:
        translateY(-10px)
        scale(1.02);

    box-shadow:
        0 30px 80px
        rgba(255,60,120,0.25);
}


.friend-photo {

    width: 100%;

    height: 330px;

    object-fit: cover;

    display: block;
}


.friend-content {

    padding:
        20px 15px 25px 15px;

    text-align: center;
}


.friend-name {

    color: white;

    font-size: 25px;

    font-weight: 800;

    margin-bottom: 10px;
}


.friend-description {

    color:
        rgba(255,255,255,0.70);

    font-size: 15px;

    line-height: 1.6;
}


/* =========================================
   БЛОК С МУЗЫКОЙ
========================================= */

.music-box {

    padding: 30px;

    margin-top: 15px;

    margin-bottom: 15px;

    border-radius: 25px;

    text-align: center;

    background:
        rgba(255,255,255,0.08);

    border:
        1px solid
        rgba(255,255,255,0.15);

    backdrop-filter:
        blur(15px);
}


.music-title {

    color: white;

    font-size: 27px;

    font-weight: 800;
}


.music-text {

    margin-top: 8px;

    color:
        rgba(255,255,255,0.65);
}


/* =========================================
   ФИНАЛ
========================================= */

.final-message {

    text-align: center;

    margin-top: 60px;

    padding: 50px 20px;

    color: white;

    font-size: 38px;

    font-weight: 900;

    text-shadow:
        0 5px 30px
        rgba(255,50,120,0.4);
}


/* =========================================
   ПАДАЮЩИЕ СЕРДЕЧКИ
========================================= */

.falling-heart {

    position: fixed;

    top: -80px;

    z-index: 999999;

    pointer-events: none;

    user-select: none;

    animation-name: heartFall;

    animation-timing-function: linear;

    animation-iteration-count: infinite;

    filter:
        drop-shadow(
            0 5px 6px
            rgba(0,0,0,0.15)
        );
}


@keyframes heartFall {

    0% {

        transform:
            translateY(-100px)
            rotate(0deg);

        opacity: 0;

    }

    10% {

        opacity: 0.95;

    }

    90% {

        opacity: 0.9;

    }

    100% {

        transform:
            translateY(115vh)
            rotate(420deg);

        opacity: 0;

    }

}


/* =========================================
   МОБИЛЬНАЯ ВЕРСИЯ
========================================= */

@media (max-width: 700px) {

    .main-title {

        font-size: 43px;

    }

    .hero {

        padding:
            35px 15px;

    }

    .hero-subtitle {

        font-size: 17px;

    }

    .friend-photo {

        height: 300px;

    }

    .final-message {

        font-size: 27px;

    }

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# ПАДАЮЩИЕ СЕРДЦА
# =========================================================

heart_symbols = [
    "❤️",
    "💖",
    "💕",
    "💗",
    "💓",
    "💘",
    "🩷"
]


hearts_html = ""


for i in range(38):

    left = (i * 29) % 100

    duration = 5 + (i % 7) * 0.7

    delay = -((i * 0.63) % 8)

    size = 17 + (i % 6) * 6

    heart = heart_symbols[
        i % len(heart_symbols)
    ]


    hearts_html += f"""
    <div
        class="falling-heart"
        style="
            left:{left}%;
            font-size:{size}px;
            animation-duration:{duration}s;
            animation-delay:{delay}s;
        "
    >
        {heart}
    </div>
    """


st.markdown(
    hearts_html,
    unsafe_allow_html=True
)


# =========================================================
# ГЛАВНЫЙ БЛОК
# =========================================================

st.markdown(
    """
<div class="hero">

    <div class="main-title">
        Мои любимки &lt;3
    </div>

    <div class="hero-subtitle">
        Спасибо, что вы у меня есть ❤️
    </div>

</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# МУЗЫКА
# =========================================================

st.markdown(
    """
<div class="music-box">

    <div class="music-title">
        🎵 Наша песня
    </div>

    <div class="music-text">
        Врубайте звук ❤️
    </div>

</div>
""",
    unsafe_allow_html=True
)


if SONG.exists():

    with open(
        SONG,
        "rb"
    ) as audio_file:

        audio_bytes = audio_file.read()


    st.audio(
        audio_bytes,
        format="audio/mpeg"
    )

else:

    st.error(
        "Не найден файл assets/song.mp3"
    )


# =========================================================
# КНОПКА
# =========================================================

button_col1, button_col2, button_col3 = st.columns(
    [1, 1, 1]
)


with button_col2:

    if st.button(
        "❤️ Послать любовь",
        use_container_width=True
    ):

        st.balloons()

        st.toast(
            "Люблю вас ❤️"
        )


# =========================================================
# ЗАГОЛОВОК ДРУЗЕЙ
# =========================================================

st.markdown(
    """
<div class="section-title">
    ❤️ Те самые люди
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# ДАННЫЕ ДРУЗЕЙ
# =========================================================

friends = [

    {
        "image": friend1_base64,

        "name": "Любимка №1 ❤️",

        "description":
            "Тут можешь написать что-нибудь "
            "личное или смешное про первого друга."
    },

    {
        "image": friend2_base64,

        "name": "Любимка №2 ❤️",

        "description":
            "Тут будет ваша локальная шутка "
            "или тёплая подпись."
    },

    {
        "image": friend3_base64,

        "name": "Любимка №3 ❤️",

        "description":
            "И здесь отдельное послание "
            "для третьего друга."
    }

]


# =========================================================
# КАРТОЧКИ
# =========================================================

columns = st.columns(3)


for column, friend in zip(
    columns,
    friends
):

    with column:

        if friend["image"]:

            image_html = f"""
            <img
                src="data:image/jpeg;base64,{friend['image']}"
                class="friend-photo"
            >
            """

        else:

            image_html = """
            <div
                style="
                    height:330px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    background:#55132f;
                "
            >
                Фото не найдено
            </div>
            """


        st.markdown(
            f"""
<div class="friend-card">

    {image_html}

    <div class="friend-content">

        <div class="friend-name">
            {friend["name"]}
        </div>

        <div class="friend-description">
            {friend["description"]}
        </div>

    </div>

</div>
""",
            unsafe_allow_html=True
        )


# =========================================================
# ФИНАЛЬНАЯ НАДПИСЬ
# =========================================================

st.markdown(
    """
<div class="final-message">

    Люблю вас❤️

    <br>

    <span
        style="
            font-size:20px;
            font-weight:400;
            opacity:0.7;
        "
    >
        Вы лучшие &lt;3
    </span>

</div>
""",
    unsafe_allow_html=True
)
