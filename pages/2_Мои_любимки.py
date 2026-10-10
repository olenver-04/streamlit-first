import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Мои любимки <3",
    page_icon="❤️",
    layout="wide"
)


# Убираем лишние отступы Streamlit
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }

    header {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)


components.html(
    """
<!DOCTYPE html>
<html lang="ru">

<head>

<meta charset="UTF-8">

<style>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    overflow: hidden;
    font-family: Arial, sans-serif;
}


/* ОСНОВНОЙ ФОН */

.container {

    width: 100%;
    height: 750px;

    position: relative;
    overflow: hidden;

    display: flex;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle at top,
            #ff9eb5,
            #ff5c8a,
            #d81b60
        );
}


/* НЕЖНОЕ СВЕЧЕНИЕ */

.glow {

    position: absolute;

    width: 500px;
    height: 500px;

    background: rgba(255,255,255,0.15);

    border-radius: 50%;

    filter: blur(80px);

    animation: glowMove 6s ease-in-out infinite alternate;
}


@keyframes glowMove {

    from {
        transform: translate(-150px, -100px);
    }

    to {
        transform: translate(180px, 100px);
    }

}


/* ЦЕНТРАЛЬНЫЙ БЛОК */

.content {

    position: relative;

    z-index: 10;

    text-align: center;

    padding: 60px;

    border-radius: 35px;

    background: rgba(255,255,255,0.12);

    backdrop-filter: blur(15px);

    border: 1px solid rgba(255,255,255,0.30);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.20);

    animation: appear 1.5s ease;
}


@keyframes appear {

    from {

        opacity: 0;

        transform: scale(0.8);

    }

    to {

        opacity: 1;

        transform: scale(1);

    }

}


/* ГЛАВНЫЙ ТЕКСТ */

.title {

    color: white;

    font-size: 70px;

    font-weight: 800;

    text-shadow:

        0 3px 15px rgba(0,0,0,0.25),

        0 0 30px rgba(255,255,255,0.30);

    animation: heartbeat 1.7s infinite;
}


@keyframes heartbeat {

    0% {
        transform: scale(1);
    }

    10% {
        transform: scale(1.05);
    }

    20% {
        transform: scale(1);
    }

    30% {
        transform: scale(1.05);
    }

    40% {
        transform: scale(1);
    }

}


/* ПОДПИСЬ */

.subtitle {

    margin-top: 20px;

    color: rgba(255,255,255,0.9);

    font-size: 22px;

    letter-spacing: 1px;
}


/* СЕРДЕЧКИ */

.heart {

    position: absolute;

    top: -60px;

    z-index: 2;

    user-select: none;

    pointer-events: none;

    animation-name: fall;

    animation-timing-function: linear;

    animation-iteration-count: infinite;
}


@keyframes fall {

    0% {

        transform:
            translateY(-100px)
            rotate(0deg);

        opacity: 0;

    }

    10% {
        opacity: 1;
    }

    90% {
        opacity: 1;
    }

    100% {

        transform:
            translateY(850px)
            rotate(360deg);

        opacity: 0;

    }

}


/* МОБИЛЬНАЯ ВЕРСИЯ */

@media (max-width: 700px) {

    .title {
        font-size: 42px;
    }

    .subtitle {
        font-size: 17px;
    }

    .content {
        padding: 35px 20px;
        width: 90%;
    }

}

</style>

</head>


<body>

<div class="container" id="container">

    <div class="glow"></div>


    <div class="content">

        <div class="title">
            Мои любимки &lt;3
        </div>

        <div class="subtitle">
            ❤️ спасибо, что вы у меня есть ❤️
        </div>

    </div>

</div>


<script>

const container =
    document.getElementById("container");


const hearts = [
    "❤️",
    "💖",
    "💕",
    "💗",
    "💓",
    "💘",
    "🩷"
];


function createHeart() {

    const heart =
        document.createElement("div");

    heart.classList.add("heart");


    heart.innerHTML =
        hearts[
            Math.floor(
                Math.random() * hearts.length
            )
        ];


    // случайное положение
    heart.style.left =
        Math.random() * 100 + "%";


    // случайный размер
    const size =
        Math.random() * 30 + 18;

    heart.style.fontSize =
        size + "px";


    // скорость падения
    const duration =
        Math.random() * 5 + 5;

    heart.style.animationDuration =
        duration + "s";


    // небольшая задержка
    heart.style.animationDelay =
        Math.random() * 2 + "s";


    container.appendChild(heart);


    setTimeout(() => {

        heart.remove();

    }, (duration + 3) * 1000);

}


/* постоянно создаём сердечки */

setInterval(
    createHeart,
    180
);


/* сердечки сразу после открытия */

for (
    let i = 0;
    i < 30;
    i++
) {

    setTimeout(
        createHeart,
        i * 80
    );

}

</script>

</body>

</html>
""",
    height=750,
    scrolling=False
)
