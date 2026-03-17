import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

BOARD_SIZE = 15

st.set_page_config(page_title="Snake", page_icon="🐍", layout="centered")
st.title("🐍 Streamlit Snake (Auto Move) v2")
st.caption("Snake moves automatically. Use direction buttons to steer.")
st.write("Version: auto-v2")


def spawn_apple(snake):
    empty = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if (r, c) not in snake]
    return random.choice(empty) if empty else None


def init_game():
    center = BOARD_SIZE // 2
    st.session_state.snake = [(center, center), (center, center - 1), (center, center - 2)]
    st.session_state.direction = (0, 1)
    st.session_state.apple = spawn_apple(st.session_state.snake)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.running = True


def set_direction(new_direction):
    dr, dc = st.session_state.direction
    nr, nc = new_direction
    if (dr + nr, dc + nc) != (0, 0):
        st.session_state.direction = new_direction


def step_game():
    if st.session_state.game_over or not st.session_state.running:
        return

    head_r, head_c = st.session_state.snake[0]
    dr, dc = st.session_state.direction
    new_head = (head_r + dr, head_c + dc)

    if not (0 <= new_head[0] < BOARD_SIZE and 0 <= new_head[1] < BOARD_SIZE):
        st.session_state.game_over = True
        st.session_state.running = False
        return

    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        st.session_state.running = False
        return

    st.session_state.snake.insert(0, new_head)

    if st.session_state.apple and new_head == st.session_state.apple:
        st.session_state.score += 1
        st.session_state.apple = spawn_apple(st.session_state.snake)
    else:
        st.session_state.snake.pop()


def render_board():
    snake = set(st.session_state.snake)
    apple = st.session_state.apple

    html = '<div style="display:grid;grid-template-columns:repeat(%d,24px);gap:2px;justify-content:center;">' % BOARD_SIZE
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            cell = (r, c)
            if cell == st.session_state.snake[0]:
                color = "#2E7D32"
            elif cell in snake:
                color = "#66BB6A"
            elif cell == apple:
                color = "#E53935"
            else:
                color = "#ECEFF1"
            html += f'<div style="width:24px;height:24px;border-radius:4px;background:{color};border:1px solid #CFD8DC;"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


if "snake" not in st.session_state:
    init_game()

# Controls
speed_ms = st.slider("Speed (ms per step)", min_value=80, max_value=500, value=180, step=20)

c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    if st.button("▶️ Start", use_container_width=True):
        if not st.session_state.game_over:
            st.session_state.running = True
with c2:
    if st.button("⏸️ Pause", use_container_width=True):
        st.session_state.running = False
with c3:
    if st.button("🔄 Restart", use_container_width=True):
        init_game()
        st.rerun()

u1, u2, u3 = st.columns([1, 1, 1])
with u2:
    if st.button("⬆️", use_container_width=True):
        set_direction((-1, 0))

m1, m2, m3 = st.columns([1, 1, 1])
with m1:
    if st.button("⬅️", use_container_width=True):
        set_direction((0, -1))
with m3:
    if st.button("➡️", use_container_width=True):
        set_direction((0, 1))

l1, l2, l3 = st.columns([1, 1, 1])
with l2:
    if st.button("⬇️", use_container_width=True):
        set_direction((1, 0))

if st.session_state.running and not st.session_state.game_over:
    st_autorefresh(interval=speed_ms, key="snake-tick")
    step_game()

st.write(f"**Score:** {st.session_state.score}")
render_board()

if st.session_state.game_over:
    st.error("Game Over! 💥 Press Restart to play again.")
