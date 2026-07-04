import random
from datetime import datetime

import streamlit as st


APP_TITLE = "Sports Jersey Prompt Generator"

JERSEY_REFERENCE_TEXT = (
    "Use the uploaded jersey design as the main reference. "
    "Apply the jersey design exactly the same as the provided design reference, "
    "without changing any detail."
)

JERSEY_LOCK_TEXT = (
    "Keep every jersey detail unchanged: colors, pattern, motif, logo placement, "
    "sponsor placement, collar shape, sleeve details, side panels, stitching details, "
    "front design, back design, names, numbers, and all graphic elements."
)

NEGATIVE_PROMPT = (
    "Negative prompt: cartoon, anime, illustration, CGI, 3D render, plastic skin, "
    "overly glossy jersey, unrealistic fabric, distorted body, extra fingers, missing fingers, "
    "deformed hands, bad anatomy, duplicated person, blurry face, low resolution, pixelated, "
    "warped logo, changed jersey design, wrong colors, wrong pattern, moved sponsor logo, "
    "incorrect number, incorrect name, unreadable text, fake badge, altered collar, altered sleeves, "
    "messy composition, harsh overexposure, underexposure, watermark, signature, frame, text overlay."
)


PRESETS = {
    "jenis_model": [
        "male professional football player",
        "female professional football player",
        "young adult athletic model",
        "senior team captain",
        "youth academy player",
        "futsal player",
        "goalkeeper",
        "winger with athletic build",
        "midfielder with natural sports physique",
        "sportswear campaign model",
        "diverse professional sports models",
    ],
    "jumlah_model": [
        "1 model",
        "2 models",
        "3 models",
        "5 models team lineup",
        "full starting eleven team group",
    ],
    "pose": [
        "standing confidently with arms relaxed",
        "crossed arms hero pose",
        "walking naturally toward camera",
        "adjusting jersey collar",
        "holding a football under one arm",
        "tying boot laces before match",
        "celebration pose after scoring",
        "pre-match focus pose",
        "sprint action pose",
        "passing the ball in motion",
        "team huddle pose",
        "locker room seated portrait",
    ],
    "ekspresi": [
        "calm and confident expression",
        "serious match day focus",
        "natural relaxed smile",
        "intense competitive look",
        "proud captain expression",
        "energetic celebration expression",
        "determined training expression",
        "friendly sports campaign expression",
    ],
    "komposisi": [
        "clean professional sports portrait composition",
        "full body fashion campaign composition",
        "half body editorial sports composition",
        "dynamic action composition with realistic motion",
        "team poster composition",
        "centered product-focused jersey composition",
        "cinematic match day composition",
        "minimal campaign layout with strong jersey visibility",
    ],
    "background": [
        "football stadium",
        "futsal court",
        "stadium tunnel",
        "locker room",
        "training ground",
        "running track",
        "gym sport campaign",
        "night stadium floodlight",
        "urban football court",
        "professional studio sportswear campaign",
        "grass pitch during golden hour",
        "indoor arena with clean sport branding",
        "stadium seats background",
        "concrete street football environment",
        "rainy match day stadium",
    ],
    "lighting": [
        "natural daylight",
        "soft studio lighting",
        "cinematic stadium lighting",
        "golden hour sunlight",
        "night floodlight lighting",
        "dramatic side lighting",
        "clean commercial sportswear lighting",
        "soft locker room practical lighting",
        "bright indoor futsal court lighting",
    ],
    "camera_angle": [
        "eye-level camera angle",
        "slightly low angle",
        "low angle hero shot",
        "slightly high angle",
        "side angle",
        "three-quarter angle",
        "front-facing camera angle",
        "over-the-shoulder sport campaign angle",
    ],
    "lens_look": [
        "realistic 35mm lens look",
        "50mm portrait lens look",
        "85mm professional portrait lens look",
        "24-70mm sports campaign lens look",
        "shallow depth of field",
        "crisp editorial sports photography",
        "natural documentary sports photography",
        "high-end commercial sportswear photography",
    ],
    "outfit": [
        "matching football shorts",
        "black athletic shorts",
        "white athletic shorts",
        "training pants",
        "compression leggings",
        "football socks and boots",
        "futsal shoes and sport socks",
        "clean sportswear campaign styling",
    ],
    "mood": [
        "realistic professional photoshoot",
        "natural match day atmosphere",
        "premium sportswear campaign",
        "cinematic football editorial",
        "clean modern club announcement",
        "high energy training session",
        "confident team identity campaign",
        "authentic grassroots football mood",
    ],
    "output": [
        "portrait Instagram 4:5",
        "landscape 16:9",
        "square 1:1",
        "vertical story 9:16",
    ],
}


OUTPUT_GUIDANCE = {
    "portrait Instagram 4:5": "Final image format: portrait Instagram 4:5, optimized for feed post.",
    "landscape 16:9": "Final image format: landscape 16:9, wide campaign banner style.",
    "square 1:1": "Final image format: square 1:1, balanced social media post.",
    "vertical story 9:16": "Final image format: vertical story 9:16, full-body composition with safe margins.",
}


def pick_random_values() -> dict[str, str]:
    return {key: random.choice(values) for key, values in PRESETS.items()}


def build_prompt(values: dict[str, str], custom_note: str) -> str:
    note = custom_note.strip()
    note_line = f"\nAdditional direction: {note}" if note else ""

    return f"""Realistic professional sports jersey photoshoot.

Main subject: {values["jumlah_model"]}, {values["jenis_model"]}.
Pose: {values["pose"]}.
Expression: {values["ekspresi"]}.
Composition: {values["komposisi"]}.
Background: {values["background"]}.
Lighting: {values["lighting"]}.
Camera angle: {values["camera_angle"]}.
Lens look: {values["lens_look"]}.
Outfit styling: {values["outfit"]}.
Mood: {values["mood"]}.
{OUTPUT_GUIDANCE[values["output"]]}{note_line}

Jersey reference instruction:
{JERSEY_REFERENCE_TEXT}
{JERSEY_LOCK_TEXT}

Make the jersey look like real sportswear fabric worn by real athletes. Preserve the exact uploaded jersey design while making the photoshoot natural, realistic, sharp, professional, and ready for a sports club or sportswear campaign.

{NEGATIVE_PROMPT}
"""


def set_random_prompt() -> None:
    random_values = pick_random_values()
    st.session_state.selected_values = random_values
    for key, value in random_values.items():
        st.session_state[key] = value
    st.session_state.generated_prompt = build_prompt(
        st.session_state.selected_values,
        st.session_state.get("custom_note", ""),
    )


def generate_from_current_selection() -> None:
    st.session_state.selected_values = {
        key: st.session_state[key] for key in PRESETS.keys()
    }
    st.session_state.generated_prompt = build_prompt(
        st.session_state.selected_values,
        st.session_state.get("custom_note", ""),
    )


def initialize_state() -> None:
    if "selected_values" not in st.session_state:
        st.session_state.selected_values = {
            key: values[0] for key, values in PRESETS.items()
        }
    for key, value in st.session_state.selected_values.items():
        st.session_state.setdefault(key, value)
    if "generated_prompt" not in st.session_state:
        st.session_state.generated_prompt = build_prompt(
            st.session_state.selected_values,
            "",
        )


def render_select(label: str, key: str) -> None:
    current_value = st.session_state.selected_values[key]
    st.selectbox(
        label,
        PRESETS[key],
        index=PRESETS[key].index(current_value),
        key=key,
    )


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="SJ",
    layout="wide",
)

initialize_state()

st.title(APP_TITLE)
st.caption(
    "Buat prompt photoshoot jersey olahraga yang realistis, natural, dan profesional."
)

with st.expander("Panduan singkat", expanded=True):
    st.write(
        "Pilih preset di bawah, klik **Generate Prompt**, lalu copy atau download hasilnya. "
        "Saat memakai prompt ini di image generator, upload juga gambar desain jersey Anda sebagai referensi utama."
    )

left_column, right_column = st.columns([1, 1])

with left_column:
    st.subheader("Preset Photoshoot")
    render_select("Jenis model", "jenis_model")
    render_select("Jumlah model", "jumlah_model")
    render_select("Pose", "pose")
    render_select("Ekspresi", "ekspresi")
    render_select("Komposisi foto", "komposisi")
    render_select("Background / latar sport", "background")

with right_column:
    st.subheader("Style Foto")
    render_select("Lighting", "lighting")
    render_select("Camera angle", "camera_angle")
    render_select("Lens look", "lens_look")
    render_select("Outfit / bawahan", "outfit")
    render_select("Mood photoshoot", "mood")
    render_select("Tipe output", "output")

st.text_area(
    "Catatan tambahan opsional",
    key="custom_note",
    placeholder="Contoh: add subtle rain, make the jersey front clearly visible, club announcement style",
    height=90,
)

button_column_1, button_column_2, button_column_3 = st.columns([1, 1, 1])

with button_column_1:
    st.button("Generate Prompt", type="primary", on_click=generate_from_current_selection)

with button_column_2:
    st.button("Generate Random Prompt", on_click=set_random_prompt)

prompt_text = st.session_state.generated_prompt
file_name = f"sports_jersey_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with button_column_3:
    st.download_button(
        "Copy/Download Prompt TXT",
        data=prompt_text,
        file_name=file_name,
        mime="text/plain",
        help="Browser akan mengunduh prompt sebagai file TXT. Untuk copy manual, blok teks prompt di bawah lalu tekan Ctrl+C.",
    )

st.subheader("Hasil Prompt")
st.text_area(
    "Prompt siap pakai",
    value=prompt_text,
    height=430,
    help="Blok teks ini lalu tekan Ctrl+C jika ingin menyalin manual.",
)

st.info(
    "Tips: upload gambar desain jersey Anda ke image generator, lalu tempel prompt ini. "
    "Instruksi di prompt sudah meminta desain jersey dipertahankan persis seperti referensi."
)
