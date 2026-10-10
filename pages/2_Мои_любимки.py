import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Мои любимки <3",
    page_icon="❤️",
    layout="wide"
)


# =========================
# СТИЛИ
# =========================

st.markdown("""
<style>

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-size: 60px;
    font-weight: 800;
    margin-bottom: 5px;

    background: linear-gradient(
        90deg,
        #ff4b7d,
        #ff8fab,
        #ff4b7d
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #888;
    margin-bottom: 30px;
}

.friend-name {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
}

.friend-text {
    text-align: center;
    color: #888;
}

</style>
""", unsafe_allow_html=True)


# =========================
# ПАДАЮЩИЕ СЕРДЕЧКИ
# =========================

components.html(
    """
    <style>

    .heart {
        position: fixed;
        top: -50px;
        font-size: 25px;
        animation: fall linear forwards;
        z-index: 9999;
        pointer-events: none;
    }

    @keyframes fall {

        0% {
            transform:
                translateY(-50px)
                rotate(0deg);
            opacity: 1;
        }

        100% {
            transform:
                translateY(100vh)
                rotate(360deg);
            opacity: 0;
        }

    }

    </style>

    <script>

    const hearts = [
        "❤️",
        "💖",
        "💕",
        "💗",
        "🩷"
    ];


    function createHeart() {

        const heart =
            document.createElement("div");

        heart.className = "heart";

        heart.innerHTML =
            hearts[
                Math.floor(
                    Math.random()
                    * hearts.length
                )
            ];


        heart.style.left =
            Math.random() * 100 + "vw";


        heart.style.animationDuration =
            (Math.random() * 4 + 4)
            + "s";


        document.body.appendChild(heart);


        setTimeout(
            () => heart.remove(),
            8000
        );

    }


    setInterval(
        createHeart,
        350
    );

    </script>
    """,
    height=0
)


# =========================
# ЗАГОЛОВОК
# =========================

st.markdown(
    '<div class="title">Мои любимки &lt;3</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Спасибо, что вы у меня есть ❤️
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# МУЗЫКА
# =========================

st.markdown("### 🎵 Наша песня")

st.audio(
    "assets/music/song.mp3"
)

st.caption(
    "Врубайте на полную ❤️"
)

st.divider()


# =========================
# ДРУЗЬЯ
# =========================

st.markdown(
    "## ❤️ Те самые люди"
)


col1, col2, col3 = st.columns(3)


# ДРУГ 1

with col1:

    st.image(
        "assets/friends/friend1.jpg",
        use_container_width=True
    )

    st.markdown(
        '<div class="friend-name">Друг 1 ❤️</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="friend-text">
            Здесь можно написать вашу прикольную фразу.
        </div>
        """,
        unsafe_allow_html=True
    )


# ДРУГ 2

with col2:

    st.image(
        "assets/friends/friend2.jpg",
        use_container_width=True
    )

    st.markdown(
        '<div class="friend-name">Друг 2 ❤️</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="friend-text">
            Здесь будет своя подпись.
        </div>
        """,
        unsafe_allow_html=True
    )


# ДРУГ 3

with col3:

    st.image(
        "assets/friends/friend3.jpg",
        use_container_width=True
    )

    st.markdown(
        '<div class="friend-name">Друг 3 ❤️</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="friend-text">
            И здесь отдельное послание.
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================
# ФИНАЛ
# =========================

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:32px;
        font-weight:700;
        padding:40px;
    ">
        Люблю вас, балбесы ❤️
    </div>
    """,
    unsafe_allow_html=True
)
