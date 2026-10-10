import streamlit as st
from pathlib import Path
import base64


# =========================================================
# НАСТРОЙКИ
# =========================================================

st.set_page_config(
    page_title="Мои любимки <3",
    page_icon="❤️",
    layout="wide"
)


# =========================================================
# ПУТИ
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"

FRIEND1 = ASSETS_DIR / "friend1.jpg"
FRIEND2 = ASSETS_DIR / "friend2.jpg"
FRIEND3 = ASSETS_DIR / "friend3.jpg"

SONG = ASSETS_DIR / "song.mp3"


# =========================================================
# ФОТО -> BASE64
# =========================================================

def image_to_base64(path):
    if not path.exists():
        return None

    with open(path, "rb") as file:
        return base64.b64encode(
            file.read()
        ).decode("utf-8")


friend1_img = image_to_base64(FRIEND1)
friend2_img = image_to_base64(FRIEND2)
friend3_img = image_to_base64(FRIEND3)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(
            circle at 20% 10%,
            rgba(255, 120, 170, 0.35),
            transparent 35%
        ),
        radial-gradient(
            circle at 80% 20%,
            rgba(255, 60, 120, 0.25),
            transparent 40%
        ),
        linear-gradient(
            135deg,
            #1d0010,
            #520028,
            #240012
        );

    background-attachment: fixed;
}

.block-container {
    max-width: 1200px;
    padding-top: 3rem;
    padding-bottom: 6rem;
}


/* HERO */

.hero {
    text-align: center;
    padding: 50px 20px;
    margin-bottom: 35px;

    border-radius: 35px;

    background:
        rgba(255,255,255,0.08);

    border:
        1px solid rgba(255,255,255,0.15);

    box-shadow:
        0 25px 70px rgba(0,0,0,0.30);

    backdrop-filter:
        blur(18px);
}

.main-title {
    color: white;

    font-size: 65px;

    font-weight: 900;

    text-shadow:
        0 5px 25px
        rgba(255,50,120,0.5);

    animation:
        heartbeat 1.8s infinite;
}

.hero-subtitle {
    color:
        rgba(255,255,255,0.75);

    font-size: 21px;

    margin-top: 12px;
}


@keyframes heartbeat {

    0% {
        transform: scale(1);
    }

    10% {
        transform: scale(1.04);
    }

    20% {
        transform: scale(1);
    }

    30% {
        transform: scale(1.04);
    }

    40% {
        transform: scale(1);
    }

}


/* MUSIC */

.music-box {
    text-align: center;

    padding: 27px;

    margin-top: 20px;
    margin-bottom: 15px;

    border-radius: 25px;

    background:
        rgba(255,255,255,0.08);

    border:
        1px solid rgba(255,255,255,0.14);

    backdrop-filter:
        blur(15px);
}

.music-title {
    color: white;

    font-size: 28px;

    font-weight: 800;
}

.music-text {
    color:
        rgba(255,255,255,0.65);

    margin-top: 8px;
}


/* ЗАГОЛОВОК */

.section-title {
    text-align: center;

    color: white;

    font-size: 36px;

    font-weight: 900;

    margin-top: 45px;

    margin-bottom: 30px;
}


/* КАРТОЧКИ */

.friend-card {
    overflow: hidden;

    border-radius: 25px;

    background:
        rgba(255,255,255,0.10);

    border:
        1px solid rgba(255,255,255,0.15);

    box-shadow:
        0 20px 50px rgba(0,0,0,0.25);

    transition:
        0.3s ease;
}

.friend-card:hover {
    transform:
        translateY(-10px)
        scale(1.015);

    box-shadow:
        0 30px 70px
        rgba(255,40,110,0.22);
}

.friend-photo {
    display: block;

    width: 100%;

    height: 350px;

    object-fit: cover;
}

.friend-content {
    padding: 20px;

    text-align: center;
}

.friend-name {
    color: white;

    font-size: 24px;

    font-weight: 800;

    margin-bottom: 10px;
}

.friend-description {
    color:
        rgba(255,255,255,0.68);

    font-size: 15px;

    line-height: 1.5;
}


/* ФИНАЛ */

.final-message {
    text-align: center;

    color: white;

    margin-top: 60px;

    padding: 50px 20px;

    font-size: 38px;

    font-weight: 900;

    text-shadow:
        0 5px 25px
        rgba(255,50,120,0.4);
}

.final-small {
    display: block;

    margin-top: 10px;

    font-size: 20px;

    font-weight: 400;

    opacity: 0.7;
}


/* СЕРДЕЧКИ */

.falling-heart {
    position: fixed;

    top: -60px;

    z-index: 999999;

    pointer-events: none;

    user-select: none;

    animation-name:
        heartFall;

    animation-timing-function:
        linear;

    animation-iteration-count:
        infinite;
}


@keyframes heartFall {

    0% {
        transform:
            translateY(-80px)
            rotate(0deg);

        opacity: 0;
    }

    10% {
        opacity: 0.9;
    }

    90% {
        opacity: 0.9;
    }

    100% {
        transform:
            translateY(115vh)
            rotate(360deg);

        opacity: 0;
    }

}


/* МОБИЛЬНАЯ ВЕРСИЯ */

@media(max-width: 700px) {

    .main-title {
        font-size: 42px;
    }

    .hero-subtitle {
        font-size: 17px;
    }

    .friend-photo {
        height: 300px;
    }

    .final-message {
        font-size: 28px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# СЕРДЕЧКИ
# =========================================================

heart_symbols = [
    "❤️",
    "💖",
    "💕",
    "💗",
    "💓",
    "🩷"
]

hearts = ""

for i in range(28):

    left = (i * 37) % 100

    duration = 6 + (i % 6)

    delay = -((i * 0.7) % 10)

    size = 16 + (i % 5) * 5

    heart = heart_symbols[
        i % len(heart_symbols)
    ]

    hearts += (
        f'<span class="falling-heart" '
        f'style="left:{left}%;'
        f'font-size:{size}px;'
        f'animation-duration:{duration}s;'
        f'animation-delay:{delay}s;">'
        f'{heart}</span>'
    )


st.markdown(
    hearts,
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

hero_html = (
    '<div class="hero">'
    '<div class="main-title">'
    'Мои любимки &lt;3'
    '</div>'
    '<div class="hero-subtitle">'
    'Спасибо, что вы у меня есть ❤️'
    '</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True
)


# =========================================================
# МУЗЫКА
# =========================================================

music_html = (
    '<div class="music-box">'
    '<div class="music-title">'
    '🎵 Наша песня'
    '</div>'
    '<div class="music-text">'
    'Врубайте звук ❤️'
    '</div>'
    '</div>'
)

st.markdown(
    music_html,
    unsafe_allow_html=True
)


if SONG.exists():

    st.audio(
        str(SONG),
        format="audio/mpeg"
    )

else:

    st.error(
        "Файл assets/song.mp3 не найден."
    )


# =========================================================
# КНОПКА
# =========================================================

left, center, right = st.columns(
    [1, 1, 1]
)


with center:

    if st.button(
        "❤️ Послать любовь",
        use_container_width=True
    ):

        st.balloons()

        st.toast(
            "Люблю вас ❤️"
        )


# =========================================================
# ДРУЗЬЯ
# =========================================================

st.markdown(
    '<div class="section-title">'
    '❤️ Те самые люди'
    '</div>',
    unsafe_allow_html=True
)


friends = [

    {
        "image": friend1_img,
        "name": "Любимка №1 ❤️",
        "description":
            "Тут будет ваша локальная шутка "
            "или что-нибудь милое."
    },

    {
        "image": friend2_img,
        "name": "Любимка №2 ❤️",
        "description":
            "Тут напиши что-нибудь "
            "про второго друга."
    },

    {
        "image": friend3_img,
        "name": "Любимка №3 ❤️",
        "description":
            "А здесь отдельное послание "
            "для третьего друга."
    }

]


columns = st.columns(3)


for column, friend in zip(
    columns,
    friends
):

    with column:

        if friend["image"]:

            photo = (
                f'<img '
                f'class="friend-photo" '
                f'src="data:image/jpeg;base64,'
                f'{friend["image"]}">'
            )

        else:

            photo = (
                '<div class="friend-photo" '
                'style="display:flex;'
                'align-items:center;'
                'justify-content:center;'
                'background:#52142e;'
                'color:white;">'
                'Фото не найдено'
                '</div>'
            )


        card_html = (
            '<div class="friend-card">'
            f'{photo}'
            '<div class="friend-content">'
            f'<div class="friend-name">'
            f'{friend["name"]}'
            '</div>'
            f'<div class="friend-description">'
            f'{friend["description"]}'
            '</div>'
            '</div>'
            '</div>'
        )


        st.markdown(
            card_html,
            unsafe_allow_html=True
        )


# =========================================================
# ФИНАЛ
# =========================================================

final_html = (
    '<div class="final-message">'
    'Люблю вас ❤️'
    '<span class="final-small">'
    'Вы лучшие &lt;3'
    '</span>'
    '</div>'
)

st.markdown(
    final_html,
    unsafe_allow_html=True
)
