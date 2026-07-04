import random
from datetime import datetime

import streamlit as st


APP_TITLE = "Sports Jersey Prompt Generator"
APP_SUBTITLE = "Prompt photoshoot jersey olahraga yang realistis, natural, dan profesional."

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

QUICK_PRESETS = {
    "Match Day": {
        "jenis_model": "male professional football player",
        "jumlah_model": "1 model",
        "pose": "walking naturally toward camera",
        "ekspresi": "serious match day focus",
        "komposisi": "cinematic match day composition",
        "background": "football stadium",
        "lighting": "cinematic stadium lighting",
        "camera_angle": "slightly low angle",
        "lens_look": "50mm portrait lens look",
        "outfit": "football socks and boots",
        "mood": "natural match day atmosphere",
        "output": "portrait Instagram 4:5",
    },
    "Futsal Court": {
        "jenis_model": "futsal player",
        "jumlah_model": "2 models",
        "pose": "passing the ball in motion",
        "ekspresi": "determined training expression",
        "komposisi": "dynamic action composition with realistic motion",
        "background": "futsal court",
        "lighting": "bright indoor futsal court lighting",
        "camera_angle": "three-quarter angle",
        "lens_look": "natural documentary sports photography",
        "outfit": "futsal shoes and sport socks",
        "mood": "high energy training session",
        "output": "landscape 16:9",
    },
    "Studio Campaign": {
        "jenis_model": "sportswear campaign model",
        "jumlah_model": "1 model",
        "pose": "crossed arms hero pose",
        "ekspresi": "calm and confident expression",
        "komposisi": "centered product-focused jersey composition",
        "background": "professional studio sportswear campaign",
        "lighting": "clean commercial sportswear lighting",
        "camera_angle": "eye-level camera angle",
        "lens_look": "85mm professional portrait lens look",
        "outfit": "clean sportswear campaign styling",
        "mood": "premium sportswear campaign",
        "output": "square 1:1",
    },
    "Team Poster": {
        "jenis_model": "diverse professional sports models",
        "jumlah_model": "5 models team lineup",
        "pose": "team huddle pose",
        "ekspresi": "proud captain expression",
        "komposisi": "team poster composition",
        "background": "night stadium floodlight",
        "lighting": "night floodlight lighting",
        "camera_angle": "low angle hero shot",
        "lens_look": "high-end commercial sportswear photography",
        "outfit": "matching football shorts",
        "mood": "confident team identity campaign",
        "output": "landscape 16:9",
    },
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


def set_quick_preset(preset_name: str) -> None:
    preset_values = QUICK_PRESETS[preset_name]
    st.session_state.selected_values = preset_values
    for key, value in preset_values.items():
        st.session_state[key] = value
    st.session_state.generated_prompt = build_prompt(
        preset_values,
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


def apply_custom_style() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(40, 167, 105, 0.10), transparent 30%),
                linear-gradient(180deg, #f7fbf7 0%, #eef4f8 48%, #f8fafc 100%);
            color: #18212f;
        }

        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }

        .app-hero {
            background: linear-gradient(135deg, #10231c 0%, #1f6f4a 48%, #f0b429 100%);
            border-radius: 8px;
            padding: 30px 34px;
            color: #ffffff;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
            margin-bottom: 18px;
        }

        .app-hero h1 {
            font-size: clamp(2rem, 4vw, 3.4rem);
            line-height: 1.05;
            margin: 0 0 10px 0;
            letter-spacing: 0;
        }

        .app-hero p {
            max-width: 720px;
            font-size: 1.02rem;
            line-height: 1.6;
            margin: 0;
            color: rgba(255, 255, 255, 0.92);
        }

        .step-card {
            min-height: 108px;
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 8px;
            padding: 16px 18px;
            box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        }

        .step-card strong {
            color: #14532d;
            display: block;
            font-size: 0.95rem;
            margin-bottom: 6px;
        }

        .step-card span {
            color: #475569;
            line-height: 1.45;
            font-size: 0.92rem;
        }

        .section-title {
            color: #10231c;
            font-size: 1.2rem;
            font-weight: 700;
            margin: 14px 0 4px 0;
        }

        .soft-note {
            background: #fff7db;
            border-left: 5px solid #f0b429;
            border-radius: 8px;
            padding: 13px 15px;
            color: #4a3412;
            margin: 10px 0 18px 0;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-color: rgba(15, 23, 42, 0.09);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            background: rgba(255, 255, 255, 0.72);
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 8px;
            min-height: 42px;
            font-weight: 700;
        }

        .stTextArea textarea {
            border-radius: 8px;
            font-size: 0.95rem;
            line-height: 1.55;
        }

        div[data-baseweb="select"] > div {
            border-radius: 8px;
        }

        @media (max-width: 720px) {
            .app-hero {
                padding: 24px 20px;
            }
            .step-card {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_step_cards() -> None:
    step_1, step_2, step_3 = st.columns(3)
    with step_1:
        st.markdown(
            """
            <div class="step-card">
                <strong>1. Pilih gaya foto</strong>
                <span>Mulai dari preset cepat atau atur detail photoshoot sendiri.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_2:
        st.markdown(
            """
            <div class="step-card">
                <strong>2. Generate prompt</strong>
                <span>Aplikasi menyusun prompt rapi dengan instruksi jersey tetap sama.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_3:
        st.markdown(
            """
            <div class="step-card">
                <strong>3. Pakai di image generator</strong>
                <span>Upload desain jersey, lalu tempel prompt yang sudah dibuat.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_select(label: str, key: str, help_text: str | None = None) -> None:
    current_value = st.session_state.selected_values[key]
    st.selectbox(
        label,
        PRESETS[key],
        index=PRESETS[key].index(current_value),
        key=key,
        help=help_text,
    )


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="SJ",
    layout="wide",
)

initialize_state()
apply_custom_style()

st.markdown(
    f"""
    <div class="app-hero">
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE} Cocok untuk membuat prompt jersey bola, futsal, training kit, dan campaign sportswear dari desain jersey yang Anda upload.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_step_cards()

st.markdown('<div class="soft-note">Tips utama: upload desain jersey Anda di image generator, lalu gunakan prompt dari aplikasi ini. Prompt sudah mengunci warna, motif, logo, sponsor, nama, nomor, dan detail jersey lainnya agar tidak berubah.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-title">Mulai Cepat</div>', unsafe_allow_html=True)
preset_columns = st.columns(4)
for column, preset_name in zip(preset_columns, QUICK_PRESETS.keys()):
    with column:
        st.button(
            preset_name,
            use_container_width=True,
            on_click=set_quick_preset,
            args=(preset_name,),
        )

config_column, result_column = st.columns([1.02, 0.98], gap="large")

with config_column:
    with st.container(border=True):
        st.markdown('<div class="section-title">Atur Detail Photoshoot</div>', unsafe_allow_html=True)
        st.caption("Pilih sesuai kebutuhan. Kalau bingung, biarkan preset awal lalu klik Generate Prompt.")

        tab_subject, tab_scene, tab_style = st.tabs(["Model", "Lokasi", "Style"])

        with tab_subject:
            render_select("Jenis model", "jenis_model", "Siapa yang memakai jersey.")
            render_select("Jumlah model", "jumlah_model", "Jumlah orang di dalam foto.")
            render_select("Pose", "pose", "Gerakan atau posisi tubuh model.")
            render_select("Ekspresi", "ekspresi", "Mood wajah model.")

        with tab_scene:
            render_select("Komposisi foto", "komposisi", "Cara foto disusun agar jersey tetap terlihat jelas.")
            render_select("Background / latar sport", "background", "Lokasi photoshoot bertema olahraga.")
            render_select("Lighting", "lighting", "Arah dan rasa pencahayaan.")
            render_select("Camera angle", "camera_angle", "Sudut pengambilan kamera.")

        with tab_style:
            render_select("Lens look", "lens_look", "Karakter lensa dan kedalaman foto.")
            render_select("Outfit / bawahan", "outfit", "Bawahan dan styling pendukung.")
            render_select("Mood photoshoot", "mood", "Rasa visual keseluruhan.")
            render_select("Tipe output", "output", "Rasio gambar akhir.")

        st.text_area(
            "Catatan tambahan opsional",
            key="custom_note",
            placeholder="Contoh: make the jersey front clearly visible, add subtle rain, club announcement style",
            height=90,
        )

        action_column_1, action_column_2 = st.columns(2)
        with action_column_1:
            st.button(
                "Generate Prompt",
                type="primary",
                use_container_width=True,
                on_click=generate_from_current_selection,
            )
        with action_column_2:
            st.button(
                "Generate Random",
                use_container_width=True,
                on_click=set_random_prompt,
            )

prompt_text = st.session_state.generated_prompt
file_name = f"sports_jersey_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

with result_column:
    with st.container(border=True):
        st.markdown('<div class="section-title">Hasil Prompt</div>', unsafe_allow_html=True)
        st.caption("Prompt siap ditempel ke ChatGPT atau image generator bersama desain jersey Anda.")

        st.text_area(
            "Prompt siap pakai",
            value=prompt_text,
            height=520,
            help="Blok teks ini lalu salin jika ingin copy manual.",
        )

        st.download_button(
            "Download Prompt TXT",
            data=prompt_text,
            file_name=file_name,
            mime="text/plain",
            use_container_width=True,
            help="Mengunduh prompt sebagai file TXT.",
        )

        with st.expander("Lihat negative prompt otomatis"):
            st.write(NEGATIVE_PROMPT)

with st.sidebar:
    st.markdown("## Ringkasan")
    st.write("Aplikasi ini khusus untuk prompt photoshoot jersey olahraga realistis.")
    st.markdown("### Alur pakai")
    st.write("1. Pilih preset atau klik gaya cepat.")
    st.write("2. Klik Generate Prompt.")
    st.write("3. Upload desain jersey di image generator.")
    st.write("4. Tempel prompt hasil aplikasi.")
    st.markdown("### Instruksi penting")
    st.info(
        "Desain jersey diarahkan agar mengikuti file referensi yang Anda upload, termasuk warna, motif, logo, sponsor, nama, dan nomor."
    )
