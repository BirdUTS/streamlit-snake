import random
import streamlit as st

BOARD_SIZE = 15

st.set_page_config(page_title="Snake", page_icon="🐍", layout="centered")
st.title("🐍 Streamlit Snake")
st.caption("Use W A S D buttons (or arrow buttons) to move. Eat apples 🍎 and avoid walls/self.")


def init_game():
    center = BOARD_SIZE // 2
    st.session_state.snake = [(center, center), (center, center - 1), (center, center - 2)]
    st.session_state.direction = (0, 1)  # moving right
    st.session_state.apple = spawn_apple(st.session_state.snake)
    st.session_state.score = 0
    st.session_state.game_over = False


def spawn_apple(snake):
    empty = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if (r, c) not in snake]
    return random.choice(empty) if empty else None


def step_game(new_direction=None):
    if st.session_state.game_over:
        return

    if new_direction:
        # prevent instant reverse
        dr, dc = st.session_state.direction
        nr, nc = new_direction
        if (dr + nr, dc + nc) != (0, 0):
            st.session_state.direction = new_direction

    head_r, head_c = st.session_state.snake[0]
    dr, dc = st.session_state.direction
    new_head = (head_r + dr, head_c + dc)

    # wall hit
    if not (0 <= new_head[0] < BOARD_SIZE and 0 <= new_head[1] < BOARD_SIZE):
        st.session_state.game_over = True
        return

    # self hit
    if new_head in st.session_state.snake:
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    # apple
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
                color = "#2E7D32"  # head
            elif cell in snake:
                color = "#66BB6A"  # body
            elif cell == apple:
                color = "#E53935"  # apple
            else:
                color = "#ECEFF1"
            html += f'<div style="width:24px;height:24px;border-radius:4px;background:{color};border:1px solid #CFD8DC;"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


if "snake" not in st.session_state:
    init_game()

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    up = st.button("⬆️ W", use_container_width=True)

left_col, mid_col, right_col = st.columns([1, 1, 1])
with left_col:
    left = st.button("⬅️ A", use_container_width=True)
with mid_col:
    down = st.button("⬇️ S", use_container_width=True)
with right_col:
    right = st.button("➡️ D", use_container_width=True)

st.write(f"**Score:** {st.session_state.score}")

if up:
    step_game((-1, 0))
elif down:
    step_game((1, 0))
elif left:
    step_game((0, -1))
elif right:
    step_game((0, 1))

render_board()

if st.session_state.game_over:
    st.error("Game Over! 💥")
    if st.button("Restart"):
        init_game()
        st.rerun()
else:
    if st.button("Step Forward"):
        step_game()
        st.rerun()

st.info("Tip: Press Step Forward repeatedly to keep moving, or change direction with buttons.")
