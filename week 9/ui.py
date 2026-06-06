"""Shared Streamlit UI helpers for the Interview Bias Checker."""

import html
import json
import math

import streamlit as st
import streamlit.components.v1 as components

from rules import questions_to_guide_text, suggest_rewrite

NEUTRALITY_HELP = {
    "High": "Most questions look neutral — you're in good shape for interviews.",
    "Medium": "",
    "Low": "Several questions look leading. Review the flagged items before your sessions.",
}

NEUTRALITY_COLORS = {
    "High": "#0d9488",
    "Medium": "#d97706",
    "Low": "#dc2626",
}

NEUTRALITY_PILL_BG = {
    "High": "#ccfbf1",
    "Medium": "#ffedd5",
    "Low": "#fee2e2",
}

NEUTRALITY_PILL_BORDER = {
    "High": "#99f6e4",
    "Medium": "#fed7aa",
    "Low": "#fecaca",
}

RESULTS_HERO_BG = "#ffffff"
RESULTS_HERO_BORDER = "#e5e7eb"
RESULTS_HERO_MUTED = "#6b7280"
RESULTS_HERO_TRACK = "#e5e7eb"

FLAG_RING_COLORS = {
    "green": "#22c55e",
    "yellow": "#eab308",
    "orange": "#f97316",
    "red": "#ef4444",
}

EDIT_SAVE_BG = "#60a5fa"
EDIT_SAVE_HOVER = "#3b82f6"
EDIT_PANEL_BG = "#f3f4f6"
EDIT_DIALOG_WIDTH = "520px"


def _save_action_button_css():
    selectors = (
        "div[role=\"dialog\"]:has([data-testid=\"stTextArea\"]) "
        "[data-testid=\"stButton\"]:last-of-type > button,\n  "
        "div[data-testid=\"stElementContainer\"]:has(.results-review-footer) + "
        "div[data-testid=\"stElementContainer\"] [data-testid=\"stButton\"] > button[kind=\"primary\"]"
    )
    return f"""
  {selectors} {{
    background: {EDIT_SAVE_BG} !important;
    background-color: {EDIT_SAVE_BG} !important;
    color: #ffffff !important;
    border-color: {EDIT_SAVE_BG} !important;
  }}
  {selectors} p,
  {selectors} span,
  {selectors} div {{
    color: #ffffff !important;
  }}
  {selectors}:hover {{
    background: {EDIT_SAVE_HOVER} !important;
    background-color: {EDIT_SAVE_HOVER} !important;
    border-color: {EDIT_SAVE_HOVER} !important;
    color: #ffffff !important;
  }}
  {selectors}:hover p,
  {selectors}:hover span,
  {selectors}:hover div {{
    color: #ffffff !important;
  }}
    """


RULE_SHORT = {
    "L1": "Tag / forced agreement",
    "L2": "Loaded or one-sided wording",
    "L3": "Examples baked into the question",
}

RULE_LEGEND = {
    "L1": {
        "label": "Tag / agreement",
        "description": "Pushes toward yes or no instead of open answers",
        "dot": "#7c3aed",
        "border": "#ddd6fe",
        "border_strong": "#7c3aed",
        "card_bg": "#f5f3ff",
        "badge_bg": "#ede9fe",
        "badge_text": "#5b21b6",
        "rewrite_btn_bg": "#6d28d9",
    },
    "L2": {
        "label": "Embedded framing",
        "description": "Assumes a feeling or outcome before the participant speaks",
        "dot": "#d97706",
        "border": "#fed7aa",
        "border_strong": "#d97706",
        "card_bg": "#fff7ed",
        "badge_bg": "#ffedd5",
        "badge_text": "#c2410c",
        "rewrite_btn_bg": "#9a3412",
    },
    "L3": {
        "label": "Suggested examples",
        "description": "Bakes in examples or causes the participant should supply",
        "dot": "#0d9488",
        "border": "#99f6e4",
        "border_strong": "#0d9488",
        "card_bg": "#f0fdfa",
        "badge_bg": "#ccfbf1",
        "badge_text": "#0f766e",
        "rewrite_btn_bg": "#0f766e",
    },
}

NEUTRAL_CARD = {
    "label": "Neutral",
    "border": "#e5e7eb",
    "card_bg": "#ffffff",
    "badge_bg": "#f3f4f6",
    "badge_text": "#6b7280",
    "icon_color": "#15803d",
}

ICON_OK = "✅"
ICON_WARN = "⚠️"
ICON_FLAGGED = "🚩"

QUESTION_CARD_PAD_X = "1.15rem"
QUESTION_CARD_PAD_TOP = "1rem"
QUESTION_CARD_PAD_Y = "1.15rem"
QUESTION_CARD_SECTION_GAP = "0.75rem"
QUESTION_CARD_BORDER = "#e5e7eb"


QUESTION_CARD_MARKER = '<div class="question-card-marker" aria-hidden="true"></div>'
QUESTION_CARD_SELECTOR = 'div[data-testid="stVerticalBlockBorderWrapper"]:has(.question-card-marker)'


def _question_card_css():
    card = QUESTION_CARD_SELECTOR
    return f"""
  {card} {{
    padding: 0 !important;
    border: 1px solid {QUESTION_CARD_BORDER} !important;
    border-radius: 14px !important;
    background: #ffffff !important;
    background-color: #ffffff !important;
    box-shadow: none !important;
    overflow: hidden !important;
    margin-bottom: 1.25rem !important;
  }}
  {card} > div,
  {card} [data-testid="stVerticalBlock"],
  {card} [data-testid="stElementContainer"],
  {card} [data-testid="stMarkdownContainer"],
  {card} [data-testid="stMarkdownContainer"] > div,
  {card} [data-testid="stHorizontalBlock"],
  {card} [data-testid="stButton"] {{
    background: #ffffff !important;
    background-color: #ffffff !important;
  }}
  {card} > div > div[data-testid="stVerticalBlock"] {{
    gap: 0 !important;
  }}
  {card} [data-testid="stElementContainer"] {{
    padding: 0 !important;
    margin: 0 !important;
  }}
  {card} [data-testid="stMarkdownContainer"] {{
    margin: 0 !important;
    padding: 0 !important;
  }}
  {card} .question-card-marker {{
    display: block;
    height: 0;
    margin: 0;
    padding: 0;
    overflow: hidden;
    border: none;
  }}
  {card} .question-card-inner {{
    padding: {QUESTION_CARD_PAD_TOP} {QUESTION_CARD_PAD_X} {QUESTION_CARD_PAD_Y};
    background: transparent !important;
  }}
  {card} .question-card-inner--split {{
    padding-bottom: {QUESTION_CARD_SECTION_GAP};
  }}
  {card} .question-card-comment {{
    padding: {QUESTION_CARD_SECTION_GAP} {QUESTION_CARD_PAD_X} 0;
    background: transparent !important;
  }}
  {card} .question-card-comment--end {{
    padding-bottom: {QUESTION_CARD_PAD_Y};
  }}
  {card} hr {{
    margin: 0 !important;
    padding: 0 !important;
    height: 0 !important;
    border: none !important;
    border-top: 1px solid {QUESTION_CARD_BORDER} !important;
  }}
  {card} .question-card-header {{
    display: flex !important;
    align-items: center !important;
    gap: 0.45rem !important;
    margin-bottom: 0.75rem !important;
    flex-wrap: wrap !important;
  }}
  {card} .question-text {{
    margin: 0 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    line-height: 1.45 !important;
    color: #111827 !important;
  }}
  {card} .question-review-pill {{
    display: inline-flex !important;
    align-items: center !important;
    padding: 0.18rem 0.55rem !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    line-height: 1.3 !important;
    background: #fef2f2 !important;
    border: 1px solid #fecaca !important;
    color: #dc2626 !important;
  }}
  {card} .question-rewrite-pill {{
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.2rem !important;
    padding: 0.18rem 0.55rem !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    line-height: 1.3 !important;
    background: #ecfdf5 !important;
    border: 1px solid #a7f3d0 !important;
    color: #047857 !important;
  }}
  {card}:has(.flagged-revise-actions) [data-testid="stButton"] {{
    padding: {QUESTION_CARD_SECTION_GAP} {QUESTION_CARD_PAD_X} {QUESTION_CARD_PAD_Y} !important;
    background: #ffffff !important;
    width: 100% !important;
    border-top: 1px solid {QUESTION_CARD_BORDER} !important;
    margin: 0 !important;
  }}
  {card}:has(.flagged-revise-actions) [data-testid="stButton"] > button {{
    width: 100% !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 0.85rem !important;
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    background: #ffffff !important;
    color: #374151 !important;
  }}
  {card} .flagged-revise-actions {{
    display: none !important;
  }}
  div[data-testid="stElementContainer"]:has(.flagged-revise-actions) {{
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    border: none !important;
  }}
  .question-updated-note {{
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    margin: 0 0 0.5rem;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
    font-size: 0.82rem;
    font-weight: 600;
    line-height: 1.3;
  }}
    """

FONT_HEADING = "'Fraunces', Georgia, 'Times New Roman', serif"
FONT_BODY = "'DM Sans', system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
FONT_IMPORT = (
    "https://fonts.googleapis.com/css2?"
    "family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700"
    "&family=Fraunces:opsz,wght@9..144,600;9..144,700"
    "&display=swap"
)

UI = {
    "muted": "#6b7280",
    "placeholder": "#9ca3af",
    "text": "#374151",
    "text_strong": "#111827",
    "legend": "#374151",
    "status_ok": "#15803d",
    "status_flag": "#b45309",
    "step_card_bg": "#f9fafb",
    "step_card_text": "#374151",
    "step_num_bg": "#ffffff",
    "step_num_border": "#e5e7eb",
    "input_border": "#e5e7eb",
    "card_surface": "#ffffff",
    "button_bg": "#ffffff",
    "button_text": "#111827",
    "page_bg": "#fafafa",
    "textarea_bg": "#ffffff",
    "logo_bg": "#ede9fe",
    "logo_icon": "#5b21b6",
    "pill_bg": "#f9fafb",
    "rules": {
        "L1": {"bg": "#f5f3ff", "border": "#ddd6fe", "badge_bg": "#7c3aed"},
        "L2": {"bg": "#fff7ed", "border": "#fed7aa", "badge_bg": "#d97706"},
        "L3": {"bg": "#f0fdfa", "border": "#99f6e4", "badge_bg": "#0d9488"},
    },
    "fallback_rule": {"bg": "#f8fafc", "border": "#64748b", "badge_bg": "#64748b"},
}


def _guide_question_text(edit_index, fallback):
    questions = st.session_state.get("guide_questions")
    if questions and 0 <= edit_index < len(questions):
        return questions[edit_index]
    return fallback


def _set_guide_question(edit_index, text):
    if "guide_questions" not in st.session_state:
        return
    questions = list(st.session_state.guide_questions)
    questions[edit_index] = text.strip()
    st.session_state.guide_questions = questions


def apply_rewrite_suggestion(edit_index, suggestion, fallback_question):
    _set_guide_question(edit_index, suggestion)
    applied = set(st.session_state.get("suggestion_applied", []))
    applied.add(edit_index)
    st.session_state.suggestion_applied = list(applied)
    st.session_state["_show_update_toast"] = True


def _close_edit_modal(edit_index):
    st.session_state[f"editing_{edit_index}"] = False
    st.session_state.pop(f"modal_draft_{edit_index}", None)
    st.session_state.pop(f"modal_suggestion_pending_{edit_index}", None)
    st.session_state.pop(f"modal_suggestion_note_{edit_index}", None)


def start_question_edit(edit_index, fallback_question=""):
    st.session_state[f"editing_{edit_index}"] = True
    st.session_state[f"modal_draft_{edit_index}"] = _guide_question_text(
        edit_index, fallback_question
    )
    st.session_state.pop(f"modal_suggestion_pending_{edit_index}", None)
    st.session_state.pop(f"modal_suggestion_note_{edit_index}", None)


def cancel_question_edit(edit_index):
    _close_edit_modal(edit_index)


def _ui():
    return UI


def _rule_style(rule_id):
    ui = _ui()
    return ui["rules"].get(rule_id, ui["fallback_rule"])


def _theme_color_css(ui):
    return f"""
  .stApp {{
    background-color: {ui["page_bg"]} !important;
  }}
  .chat-header h1 {{
    color: {ui["text_strong"]} !important;
  }}
  .chat-header p {{
    color: {ui["muted"]} !important;
  }}
  .landing-header h1 {{
    color: {ui["text_strong"]} !important;
  }}
  .landing-header p {{
    color: {ui["muted"]} !important;
  }}
  [data-testid="stMarkdownContainer"] h1,
  [data-testid="stMarkdownContainer"] h2,
  [data-testid="stMarkdownContainer"] h3 {{
    color: {ui["text_strong"]} !important;
  }}
  [data-testid="stCaptionContainer"] {{
    color: {ui["muted"]} !important;
  }}
  div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-color: {ui["input_border"]} !important;
    background: {ui["card_surface"]} !important;
  }}
  div[data-testid="stButton"] > button {{
    border: 1px solid {ui["input_border"]} !important;
    background: {ui["button_bg"]} !important;
    color: {ui["button_text"]} !important;
  }}
  div[data-testid="stButton"] > button:hover {{
    border-color: {ui["muted"]} !important;
  }}
  label[data-testid="stWidgetLabel"] p,
  .stTextArea label {{
    color: {ui["text_strong"]} !important;
    font-weight: 500 !important;
  }}
  textarea {{
    color: {ui["text_strong"]} !important;
    background-color: {ui["textarea_bg"]} !important;
    caret-color: {ui["text_strong"]} !important;
    border: 1px solid {ui["input_border"]} !important;
  }}
  div[data-testid="stVerticalBlockBorderWrapper"] textarea {{
    border: none !important;
    background: transparent !important;
  }}
  textarea::placeholder {{
    color: {ui["placeholder"]} !important;
    opacity: 1 !important;
  }}
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] span,
  [data-testid="stMarkdownContainer"] strong {{
    color: {ui["text"]} !important;
  }}
  .step-card {{
    background: {ui["step_card_bg"]} !important;
    border-color: {ui["step_num_border"]} !important;
  }}
  .step-card-num {{
    border-color: {ui["step_num_border"]} !important;
    background: {ui["step_num_bg"]} !important;
    color: {ui["step_card_text"]} !important;
  }}
  .step-card-body {{
    color: {ui["step_card_text"]} !important;
  }}
  .step-card-body strong,
  .step-card-value,
  .results-copy strong {{
    color: {ui["text_strong"]} !important;
  }}
  .results-meta {{
    color: {ui["muted"]} !important;
  }}
  .results-copy {{
    color: {ui["text"]} !important;
  }}
    """


def _typography_css():
    return f"""
  @import url('{FONT_IMPORT}');

  html, body, .stApp, [data-testid="stAppViewContainer"] {{
    font-family: {FONT_BODY} !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }}

  .landing-header h1,
  .results-header h1,
  .results-hero-title,
  .results-question-title,
  .page-section-title,
  .results-ring-value,
  .results-stat-value,
  [data-testid="stMarkdownContainer"] h1,
  [data-testid="stMarkdownContainer"] h2 {{
    font-family: {FONT_HEADING} !important;
    font-optical-sizing: auto;
  }}

  div[data-testid="stButton"] > button,
  textarea,
  input,
  label,
  .feature-pill,
  .landing-header p,
  .input-section-hint,
  .input-section-label,
  .results-hero-desc,
  .results-hero-eyebrow,
  .results-footer-hint,
  .results-question-subtitle,
  .question-badge,
  .question-id,
  .question-flag-desc,
  .flagged-revise-label,
  .revise-zone-hint,
  .revise-zone-draft,
  .flagged-edit-label,
  .question-updated-note,
  .bias-score-pill,
  .results-ring-sub,
  .results-stat-label,
  .step-card-body,
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] span,
  .question-text {{
    font-family: {FONT_BODY} !important;
  }}
    """


def _chat_widget_css(ui):
    return f"""
  div[data-testid="stTextArea"] textarea {{
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
  }}
  div[data-testid="stButton"] > button[kind="secondary"] {{
    border-radius: 10px !important;
  }}
    """


def _inject_edit_save_button_styles():
    components.html(
        f"""
<script>
  (function () {{
    const SAVE_BG = "{EDIT_SAVE_BG}";
    const SAVE_HOVER = "{EDIT_SAVE_HOVER}";
    const doc = window.parent.document;
    let timer;

    function centerEditDialog() {{
      doc.querySelectorAll('div[role="dialog"]').forEach(function (panel) {{
        if (!panel.querySelector('[data-testid="stTextArea"]')) return;
        panel.style.setProperty("position", "fixed", "important");
        panel.style.setProperty("top", "50%", "important");
        panel.style.setProperty("left", "50%", "important");
        panel.style.setProperty("transform", "translate(-50%, -50%)", "important");
        panel.style.setProperty("margin", "0", "important");
        panel.style.setProperty("width", "min({EDIT_DIALOG_WIDTH}, calc(100vw - 2rem))", "important");
        panel.style.setProperty("max-width", "{EDIT_DIALOG_WIDTH}", "important");
      }});
    }}

    function styleEditButtons() {{
      centerEditDialog();
      doc.querySelectorAll('div[role="dialog"]').forEach(function (dialog) {{
        if (!dialog.querySelector('[data-testid="stTextArea"]')) return;
        const buttons = dialog.querySelectorAll('[data-testid="stButton"] > button');
        if (buttons.length < 1) return;
        const saveBtn = buttons[buttons.length - 1];
        saveBtn.style.setProperty("background-color", SAVE_BG, "important");
        saveBtn.style.setProperty("background", SAVE_BG, "important");
        saveBtn.style.setProperty("color", "#ffffff", "important");
        saveBtn.style.setProperty("border-color", SAVE_BG, "important");
        saveBtn.querySelectorAll("p, span, div").forEach(function (el) {{
          el.style.setProperty("color", "#ffffff", "important");
        }});
        saveBtn.onmouseenter = function () {{
          saveBtn.style.setProperty("background-color", SAVE_HOVER, "important");
          saveBtn.style.setProperty("background", SAVE_HOVER, "important");
          saveBtn.style.setProperty("border-color", SAVE_HOVER, "important");
          saveBtn.style.setProperty("color", "#ffffff", "important");
        }};
        saveBtn.onmouseleave = function () {{
          saveBtn.style.setProperty("background-color", SAVE_BG, "important");
          saveBtn.style.setProperty("background", SAVE_BG, "important");
          saveBtn.style.setProperty("border-color", SAVE_BG, "important");
          saveBtn.style.setProperty("color", "#ffffff", "important");
        }};
        if (buttons.length >= 1) {{
          const cancelBtn = buttons[0];
          cancelBtn.style.setProperty("background-color", "#ffffff", "important");
          cancelBtn.style.setProperty("background", "#ffffff", "important");
          cancelBtn.style.setProperty("color", "#374151", "important");
          cancelBtn.style.setProperty("border-color", "#d1d5db", "important");
        }}
      }});
      doc.querySelectorAll(".results-review-footer").forEach(function (marker) {{
        const container = marker.closest('[data-testid="stElementContainer"]');
        const next = container && container.nextElementSibling;
        if (!next) return;
        const reviewBtn = next.querySelector('[data-testid="stButton"] > button[kind="primary"]');
        if (!reviewBtn) return;
        reviewBtn.style.setProperty("background-color", SAVE_BG, "important");
        reviewBtn.style.setProperty("background", SAVE_BG, "important");
        reviewBtn.style.setProperty("color", "#ffffff", "important");
        reviewBtn.querySelectorAll("p, span, div").forEach(function (el) {{
          el.style.setProperty("color", "#ffffff", "important");
        }});
        reviewBtn.onmouseenter = function () {{
          reviewBtn.style.setProperty("background-color", SAVE_HOVER, "important");
          reviewBtn.style.setProperty("background", SAVE_HOVER, "important");
          reviewBtn.style.setProperty("border-color", SAVE_HOVER, "important");
          reviewBtn.style.setProperty("color", "#ffffff", "important");
        }};
        reviewBtn.onmouseleave = function () {{
          reviewBtn.style.setProperty("background-color", SAVE_BG, "important");
          reviewBtn.style.setProperty("background", SAVE_BG, "important");
          reviewBtn.style.setProperty("border-color", SAVE_BG, "important");
          reviewBtn.style.setProperty("color", "#ffffff", "important");
        }};
      }});
    }}

    function schedule() {{
      clearTimeout(timer);
      timer = setTimeout(styleEditButtons, 50);
    }}

    styleEditButtons();
    setTimeout(styleEditButtons, 100);
    setTimeout(styleEditButtons, 400);
    new MutationObserver(schedule).observe(doc.body, {{ childList: true, subtree: true }});
  }})();
</script>
        """,
        height=0,
    )


def _inject_question_card_styles():
    components.html(
        """
<script>
  (function () {
    const doc = window.parent.document;
    let timer;

    function paintQuestionCards() {
      doc.querySelectorAll(".question-card-marker").forEach(function (marker) {
        const wrapper = marker.closest('[data-testid="stVerticalBlockBorderWrapper"]');
        if (!wrapper) return;
        wrapper.style.setProperty("background-color", "#ffffff", "important");
        wrapper.style.setProperty("background", "#ffffff", "important");
        wrapper.style.setProperty("padding", "0", "important");
        wrapper.querySelectorAll("*").forEach(function (el) {
          if (
            el.classList.contains("question-review-pill") ||
            el.classList.contains("question-rewrite-pill") ||
            el.tagName === "BUTTON"
          ) {
            return;
          }
          el.style.setProperty("background-color", "#ffffff", "important");
          el.style.setProperty("background", "#ffffff", "important");
        });
      });
    }

    function schedule() {
      clearTimeout(timer);
      timer = setTimeout(paintQuestionCards, 50);
    }

    paintQuestionCards();
    setTimeout(paintQuestionCards, 100);
    setTimeout(paintQuestionCards, 400);
    new MutationObserver(schedule).observe(doc.body, { childList: true, subtree: true });
  })();
</script>
        """,
        height=0,
    )


def setup_page(*, page="checker"):
    """Inject layout and theme styles."""
    ui = _ui()
    centered_panel = page == "checker"
    panel_css = """
  .block-container {
    max-width: 720px;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    padding-top: 2rem;
    padding-bottom: 2rem;
  }
  .landing-header {
    text-align: center;
    margin-bottom: 0;
  }
  .landing-logo {
    width: 3rem;
    height: 3rem;
    margin: 0 auto 1rem;
    border-radius: 12px;
    background: """ + ui["logo_bg"] + """;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    line-height: 1;
  }
  .results-header .landing-logo {
    background: #fffbeb;
  }
  .landing-header h1 {
    font-size: 2.35rem;
    font-weight: 700;
    margin: 0 0 0.65rem 0;
    letter-spacing: -0.02em;
    line-height: 1.15;
    color: """ + ui["text_strong"] + """;
  }
  .landing-header p {
    font-size: 1rem;
    font-weight: 400;
    margin: 0 auto 0.85rem;
    line-height: 1.55;
    color: """ + ui["muted"] + """;
  }
  .feature-pills {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
    margin: 0 0 1.5rem;
  }
  .feature-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 0.75rem;
    border-radius: 999px;
    border: 1px solid """ + ui["input_border"] + """;
    background: """ + ui["pill_bg"] + """;
    color: """ + ui["text"] + """;
    font-size: 0.82rem;
    font-weight: 500;
    white-space: nowrap;
  }
  .input-section-label {
    font-size: 0.95rem;
    font-weight: 600;
    color: """ + ui["text_strong"] + """;
    margin: 0 0 0.35rem 0;
  }
  .input-section-hint {
    font-size: 0.88rem;
    color: """ + ui["muted"] + """;
    margin: 0 0 0.85rem 0;
    line-height: 1.45;
  }
  .results-back-row {
    margin-bottom: 1rem;
  }
  .results-footer-hint {
    font-size: 0.88rem;
    color: """ + ui["muted"] + """;
    text-align: center;
    margin: 0 0 0.65rem 0;
    line-height: 1.45;
  }
  .page-section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: """ + ui["text_strong"] + """;
    margin: 0 0 1rem 0;
    letter-spacing: -0.02em;
    text-align: center;
  }
  .page-section-title-spaced {
    margin-top: 2rem;
  }
  .results-header {
    text-align: center;
    margin-bottom: 0;
  }
  .results-header h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.65rem 0;
    letter-spacing: -0.03em;
    color: """ + ui["text_strong"] + """;
  }
  .results-header p {
    font-size: 1.05rem;
    margin: 0 auto;
    line-height: 1.5;
    color: """ + ui["muted"] + """;
  }
  .bias-score-pill {
    display: inline-block;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-weight: 600;
    font-size: 1.05rem;
    line-height: 1.3;
    border: 1px solid;
    vertical-align: baseline;
  }
  .results-back-row {
    margin-bottom: 1.25rem;
  }
  .step-cards-row {
    margin: 1.25rem 0 1.5rem;
  }
  .results-footer-spacer {
    margin-top: 1.5rem;
  }
    """
    if page in ("checker", "results"):
        panel_css += """
  .stApp {
    min-height: 100dvh;
  }
  [data-testid="stAppViewContainer"] {
    min-height: 100dvh;
  }
  [data-testid="stAppViewContainer"] > section.main,
  section[data-testid="stMain"] {
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  section[data-testid="stMain"] > div.block-container,
  [data-testid="stAppViewContainer"] .block-container {
    flex: 0 0 auto;
    width: 100%;
    max-width: 720px;
    margin: 0 auto !important;
    padding-top: 0 !important;
  }
        """
        if page == "checker":
            panel_css += """
  section[data-testid="stMain"] > div.block-container,
  [data-testid="stAppViewContainer"] .block-container {
    padding-bottom: 0 !important;
  }
  [data-testid="stAppViewContainer"] > section.main,
  section[data-testid="stMain"] {
    justify-content: center;
  }
            """
        else:
            panel_css += """
  section[data-testid="stMain"] > div.block-container,
  [data-testid="stAppViewContainer"] .block-container {
    padding-bottom: 2rem !important;
  }
  [data-testid="stAppViewContainer"] > section.main,
  section[data-testid="stMain"] {
    justify-content: flex-start;
    padding-top: clamp(2.5rem, 10vh, 4.5rem);
  }
  .results-hero-card {
    background: """ + RESULTS_HERO_BG + """;
    border: 1px solid """ + RESULTS_HERO_BORDER + """;
    border-radius: 16px;
    padding: 1.65rem 1.75rem 1.5rem;
    margin-bottom: 1.5rem;
  }
  .results-hero-body {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1.5rem;
    align-items: center;
  }
  @media (max-width: 560px) {
    .results-hero-body {
      grid-template-columns: 1fr;
      justify-items: center;
      text-align: center;
    }
    .results-hero-copy {
      width: 100%;
    }
  }
  .results-ring-wrap {
    position: relative;
    width: 7.25rem;
    height: 7.25rem;
    flex-shrink: 0;
  }
  .results-ring-svg {
    display: block;
    width: 100%;
    height: 100%;
  }
  .results-ring-label {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    pointer-events: none;
  }
  .results-ring-value {
    font-size: 1.55rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
  }
  .results-ring-sub {
    font-size: 0.78rem;
    color: """ + RESULTS_HERO_MUTED + """;
    margin-top: 0.15rem;
  }
  .results-hero-title {
    font-size: 1.65rem;
    font-weight: 700;
    color: """ + ui["text_strong"] + """;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.02em;
    line-height: 1.2;
  }
  .results-hero-desc {
    font-size: 0.92rem;
    color: """ + RESULTS_HERO_MUTED + """;
    margin: 0;
    line-height: 1.5;
  }
  .results-stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.65rem;
    margin-top: 1.35rem;
    padding-top: 1.25rem;
    border-top: 1px solid """ + RESULTS_HERO_BORDER + """;
  }
  .results-stat-card {
    background: #faf8f5;
    border-radius: 12px;
    padding: 0.95rem 0.65rem 0.85rem;
    text-align: center;
  }
  .results-stat-value {
    display: block;
    font-size: 2.1rem;
    font-weight: 700;
    line-height: 1.05;
    letter-spacing: -0.02em;
  }
  .results-stat-value--review {
    color: #ea580c;
  }
  .results-stat-value--review.is-clear {
    color: #22c55e;
  }
  .results-stat-value--neutral {
    color: #15803d;
  }
  .results-stat-value--total {
    color: """ + ui["text_strong"] + """;
  }
  .results-stat-label {
    display: block;
    font-size: 0.8rem;
    color: """ + RESULTS_HERO_MUTED + """;
    margin-top: 0.3rem;
  }
  [data-testid="stMarkdownContainer"] .results-hero-title {
    color: """ + ui["text_strong"] + """ !important;
  }
  [data-testid="stMarkdownContainer"] .results-hero-desc,
  [data-testid="stMarkdownContainer"] .results-ring-sub,
  [data-testid="stMarkdownContainer"] .results-stat-label {
    color: """ + RESULTS_HERO_MUTED + """ !important;
  }
            """
    if centered_panel:
        panel_css += """
  div[data-testid="stVerticalBlockBorderWrapper"]:has(textarea) {
    padding: 1.5rem 1.75rem 1.75rem !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"]:has(textarea) > div > div[data-testid="stHorizontalBlock"] {
    border-top: 1px solid """ + ui["input_border"] + """;
    padding: 1rem 0 0 !important;
    margin: 0.75rem 0 0 !important;
    gap: 0.75rem;
  }
        """
    panel_css += """
  div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
    border: 1px solid """ + ui["input_border"] + """ !important;
    background: """ + ui["card_surface"] + """ !important;
    box-shadow: none !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"]:not(:has(.question-card-marker)) {
    padding: 1.25rem 1.5rem !important;
  }
  div[data-testid="stTextArea"],
  div[data-testid="stTextArea"] > div {
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }
  div[data-testid="stTextArea"] {
    margin-bottom: 0 !important;
    padding: 0 !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"]:has(.guide-input-marker) div[data-testid="stTextArea"] textarea {
    min-height: 150px !important;
    resize: none !important;
    overflow-y: hidden !important;
  }
  div[data-testid="stTextArea"] textarea {
    border: none !important;
    box-shadow: none !important;
    background: transparent !important;
    padding: 1rem 0.75rem 1rem 1.1rem !important;
    margin: 0 !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    text-indent: 0 !important;
  }
  div[data-testid="stTextArea"] textarea::placeholder {
    color: """ + ui["placeholder"] + """ !important;
    opacity: 1 !important;
  }
  div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    background: """ + ui["button_bg"] + """ !important;
    color: """ + ui["button_text"] + """ !important;
    border: 1px solid """ + ui["input_border"] + """ !important;
    font-weight: 600 !important;
    padding: 0.6rem 1rem !important;
    box-shadow: none !important;
  }
  div[data-testid="stButton"] > button:hover {
    border-color: """ + ui["muted"] + """ !important;
    background: """ + ui["step_card_bg"] + """ !important;
  }
  div[data-testid="stButton"] > button[kind="primary"] {
    background: """ + ui["button_bg"] + """ !important;
    color: """ + ui["button_text"] + """ !important;
    border: 1px solid """ + ui["input_border"] + """ !important;
  }
    """
    st.markdown(
        f"""
<style>
  {_typography_css()}
  section[data-testid="stSidebar"],
  button[data-testid="stSidebarCollapsedControl"],
  button[data-testid="collapsedControl"] {{
    display: none !important;
  }}
  {panel_css}
  div[data-testid="stButton"] > button {{
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
  }}
  textarea {{
    border-radius: 8px !important;
  }}
  .step-cards-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.85rem;
  }}
  .step-card {{
    border: 1px solid;
    border-radius: 12px;
    padding: 0.95rem 1rem;
    min-height: 5.75rem;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
  }}
  .step-card-num {{
    flex-shrink: 0;
    width: 1.45rem;
    height: 1.45rem;
    border-radius: 999px;
    border: 1px solid;
    font-size: 0.78rem;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }}
  .step-card-body {{
    font-size: 0.92rem;
    line-height: 1.45;
    margin: 0;
  }}
  .step-card-value {{
    display: block;
    font-size: 1.75rem;
    font-weight: 700;
    line-height: 1.2;
    margin-top: 0.2rem;
  }}
  .results-meta {{
    font-size: 0.92rem;
    margin: 0.85rem 0 0.25rem 0;
  }}
  .results-copy {{
    font-size: 0.95rem;
    line-height: 1.55;
    margin: 0.5rem 0 0 0;
  }}
  .results-question-title {{
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: {ui["text_strong"]} !important;
    margin: 2rem 0 0.35rem 0 !important;
    letter-spacing: -0.03em !important;
    text-align: left !important;
    line-height: 1.2 !important;
  }}
  .results-question-subtitle {{
    font-size: 0.92rem;
    color: {ui["muted"]};
    margin: 0 0 1.25rem 0;
    line-height: 1.5;
    text-align: left;
  }}
  [data-testid="stMarkdownContainer"] .results-question-title {{
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: {ui["text_strong"]} !important;
  }}
  .question-cards {{
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    margin-bottom: 0.5rem;
  }}
  .question-card {{
    border: 1px solid;
    border-radius: 14px;
    background: {ui["card_surface"]};
    padding: 1.35rem 1.5rem;
    box-sizing: border-box;
    margin-bottom: 1.25rem;
  }}
  .question-card--flagged {{
    border-width: 2px;
    border-color: #dc2626;
    padding: 1.2rem 1.3rem;
    box-shadow: 0 4px 18px rgba(17, 24, 39, 0.08);
  }}
  .question-card--neutral {{
    border-color: {ui["input_border"]};
    background: #ffffff;
  }}
  .question-card-header {{
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
  }}
  .question-ok-icon,
  .question-warn-icon {{
    font-size: 1rem;
    line-height: 1;
  }}
  .question-card--flagged .question-id {{
    color: {ui["text_strong"]};
    font-size: 0.88rem;
  }}
  .question-card--flagged .question-badge {{
    padding: 0.3rem 0.7rem;
    font-size: 0.78rem;
    border: 1px solid transparent;
  }}
  .question-card--flagged .question-text {{
    font-size: 1.05rem;
    font-weight: 600;
    color: {ui["text_strong"]};
  }}
  .question-card--flagged .question-flag-desc {{
    font-size: 0.92rem;
    color: {ui["text"]};
  }}
  .flagged-question-desc {{
    margin-top: 0.85rem;
  }}
  .flagged-question-desc .question-flag-desc {{
    margin: 0;
    line-height: 1.55;
  }}
  .question-id {{
    font-size: 0.82rem;
    font-weight: 600;
    color: {ui["muted"]};
  }}
  .question-badge {{
    display: inline-block;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    line-height: 1.3;
  }}
  .question-text {{
    font-size: 1rem;
    font-weight: 600;
    color: {ui["text_strong"]};
    margin: 0;
    line-height: 1.45;
  }}
  .question-flag-desc {{
    font-size: 0.88rem;
    color: {ui["muted"]};
    margin: 0.5rem 0 0 0;
    line-height: 1.5;
  }}
  {_theme_color_css(ui)}
  {_chat_widget_css(ui)}
  {_question_card_css()}
  div[role="dialog"]:has([data-testid="stTextArea"]) {{
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    right: auto !important;
    bottom: auto !important;
    transform: translate(-50%, -50%) !important;
    width: min(""" + EDIT_DIALOG_WIDTH + """, calc(100vw - 2rem)) !important;
    max-width: """ + EDIT_DIALOG_WIDTH + """ !important;
    margin: 0 !important;
    border-radius: 14px !important;
    padding: 1rem 1.25rem 1.15rem !important;
  }}
  section[data-testid="stDialog"]:has([data-testid="stTextArea"]),
  div[data-testid="stDialog"]:has([data-testid="stTextArea"]) {{
    position: fixed !important;
    inset: 0 !important;
    display: block !important;
    width: 100vw !important;
    height: 100vh !important;
    min-height: 100vh !important;
    padding: 0 !important;
    margin: 0 !important;
  }}
  section[data-testid="stDialog"]:has([data-testid="stTextArea"]) div[role="dialog"],
  div[data-testid="stDialog"]:has([data-testid="stTextArea"]) div[role="dialog"] {{
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    right: auto !important;
    bottom: auto !important;
    transform: translate(-50%, -50%) !important;
    width: min(""" + EDIT_DIALOG_WIDTH + """, calc(100vw - 2rem)) !important;
    max-width: """ + EDIT_DIALOG_WIDTH + """ !important;
    margin: 0 !important;
    border-radius: 14px !important;
    padding: 1rem 1.25rem 1.15rem !important;
  }}
  div[role="dialog"]:has([data-testid="stTextArea"]) [data-testid="stVerticalBlock"] {{
    gap: 0.35rem !important;
  }}
  div[role="dialog"]:has([data-testid="stTextArea"]) h2,
  div[role="dialog"]:has([data-testid="stTextArea"]) [data-testid="stHeading"] {{
    margin: 0 0 0.35rem 0 !important;
    padding: 0 !important;
  }}
  div[role="dialog"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"],
  div[role="dialog"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] > div,
  div[role="dialog"]:has([data-testid="stTextArea"]) [data-testid="stElementContainer"]:has([data-testid="stTextArea"]) {{
    margin-top: 0 !important;
    padding-top: 0 !important;
  }}
  div[role="dialog"]:has([data-testid="stTextArea"]) [data-testid="stTextArea"] textarea {{
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    background: #ffffff !important;
    padding: 0.85rem 1rem !important;
  }}
  div[role="dialog"]:has([data-testid="stTextArea"]) [data-testid="stButton"] > button {{
    white-space: nowrap !important;
  }}
  div[role="dialog"]:has([data-testid="stTextArea"]) .modal-suggestion-note {{
    font-size: 0.86rem;
    color: #6b7280;
    margin: 0.35rem 0 0.85rem;
  }}
  .results-review-footer {{
    display: none;
  }}
  {_save_action_button_css()}
</style>
        """,
        unsafe_allow_html=True,
    )
    if page == "results":
        _inject_edit_save_button_styles()
        _inject_question_card_styles()


RESULTS_LOGO_ICON = "⭐"


def _feature_pills_html():
    pills = [
        ("🚩", "Detects leading language"),
        ("⚡", "Suggests rewrites"),
        ("🔒", "Stays in your browser"),
    ]
    pills_html = "".join(
        f'<span class="feature-pill"><span aria-hidden="true">{icon}</span>{label}</span>'
        for icon, label in pills
    )
    return f'<div class="feature-pills">{pills_html}</div>'


def render_checker_header():
    st.markdown(
        f"""
<div class="landing-header">
  <h1>Interview bias checker</h1>
  <p>Check your interview guide for biased or leading language.</p>
  {_feature_pills_html()}
</div>
        """,
        unsafe_allow_html=True,
    )


def _guide_text_area_height(text: str) -> int:
    """Estimate textarea height from guide text (used after paste/demo on rerun)."""
    min_px = 150
    line_px = 26
    padding = 40
    chars_per_line = 68
    if not text or not text.strip():
        return min_px
    visual_lines = 0
    for line in text.splitlines():
        length = len(line.rstrip())
        visual_lines += max(1, math.ceil(length / chars_per_line)) if length else 1
    return max(min_px, visual_lines * line_px + padding)


def _inject_guide_textarea_autogrow():
    components.html(
        """
<script>
  (function () {
    const doc = window.parent.document;
    const MIN_H = 150;
    let scanTimer;

    function grow(textarea) {
      textarea.style.height = "auto";
      textarea.style.height = Math.max(MIN_H, textarea.scrollHeight) + "px";
    }

    function bind(textarea) {
      if (textarea.dataset.guideAutogrow) return;
      textarea.dataset.guideAutogrow = "1";
      textarea.addEventListener("input", function () { grow(textarea); });
      textarea.addEventListener("paste", function () {
        setTimeout(function () { grow(textarea); }, 0);
      });
      grow(textarea);
    }

    function scan() {
      doc.querySelectorAll(".guide-input-marker").forEach(function (marker) {
        const wrapper = marker.closest('[data-testid="stVerticalBlockBorderWrapper"]');
        if (!wrapper) return;
        const textarea = wrapper.querySelector("textarea");
        if (textarea) bind(textarea);
      });
    }

    function scheduleScan() {
      clearTimeout(scanTimer);
      scanTimer = setTimeout(scan, 50);
    }

    scan();
    setTimeout(scan, 100);
    setTimeout(scan, 400);

    const observer = new MutationObserver(scheduleScan);
    observer.observe(doc.body, { childList: true, subtree: true });
  })();
</script>
        """,
        height=0,
    )


def render_checker_input(*, demo_callback):
    with st.container(border=True):
        st.markdown(
            '<p class="input-section-hint">Paste your interview questions here</p>'
            '<div class="guide-input-marker"></div>',
            unsafe_allow_html=True,
        )
        guide_text = st.text_area(
            "Your questions",
            height=_guide_text_area_height(st.session_state.get("guide_text", "")),
            placeholder="1. Walk me through the last time you used this product.\n2. What was hardest about that experience?",
            key="guide_text",
            label_visibility="collapsed",
        )

        btn_analyze, btn_demo = st.columns([3.2, 1])
        with btn_analyze:
            analyze = st.button("Analyze questions", type="primary", use_container_width=True)
        with btn_demo:
            st.button("Try demo", on_click=demo_callback, use_container_width=True)

    _inject_guide_textarea_autogrow()

    return guide_text, analyze


def _neutrality_score(result) -> int:
    return 100 - result["bias_score"]


def _neutrality_band(score: int) -> str:
    if score >= 67:
        return "High"
    if score >= 34:
        return "Medium"
    return "Low"


def _neutrality_styles(score: int) -> dict:
    band = _neutrality_band(score)
    return {
        "band": band,
        "color": NEUTRALITY_COLORS.get(band, "#64748b"),
        "pill_bg": NEUTRALITY_PILL_BG.get(band, "#f3f4f6"),
        "pill_border": NEUTRALITY_PILL_BORDER.get(band, "#e5e7eb"),
        "help": NEUTRALITY_HELP.get(band, ""),
    }


def _results_status_copy(result):
    flagged = result["flagged_questions"]
    total = result["total_questions"]
    neutral = total - flagged
    if flagged == 0:
        return (
            "Looking good 🎉",
            "Most questions look neutral — ready for fielding.",
        )
    review_noun = "question" if flagged == 1 else "questions"
    return (
        f"{flagged} {review_noun} need review",
        f"{neutral} of {total} are clear — here's what to fix.",
    )


def _flagged_ring_color(flagged: int, total: int) -> str:
    if total == 0 or flagged == 0:
        return FLAG_RING_COLORS["green"]
    ratio = flagged / total
    if ratio <= 0.33:
        return FLAG_RING_COLORS["yellow"]
    if ratio <= 0.66:
        return FLAG_RING_COLORS["orange"]
    return FLAG_RING_COLORS["red"]


def _neutral_progress_ring_svg(neutral: int, total: int, flagged: int) -> str:
    radius = 52
    circumference = 2 * math.pi * radius
    ratio = (neutral / total) if total else 0
    dash = circumference * ratio
    accent = _flagged_ring_color(flagged, total)
    return f"""
<svg class="results-ring-svg" viewBox="0 0 120 120" aria-hidden="true">
  <circle cx="60" cy="60" r="{radius}" fill="none"
    stroke="{RESULTS_HERO_TRACK}" stroke-width="9"/>
  <circle cx="60" cy="60" r="{radius}" fill="none"
    stroke="{accent}" stroke-width="9"
    stroke-dasharray="{dash} {circumference}"
    stroke-linecap="round"
    transform="rotate(-90 60 60)"/>
</svg>
    """.strip()


def _results_stats_html(*, flagged: int, neutral: int, total: int) -> str:
    review_class = "results-stat-value--review"
    if flagged == 0:
        review_class += " is-clear"
    return f"""
<div class="results-stats-row">
  <div class="results-stat-card">
    <span class="results-stat-value {review_class}">{flagged}</span>
    <span class="results-stat-label">To review</span>
  </div>
  <div class="results-stat-card">
    <span class="results-stat-value results-stat-value--neutral">{neutral}</span>
    <span class="results-stat-label">Neutral</span>
  </div>
  <div class="results-stat-card">
    <span class="results-stat-value results-stat-value--total">{total}</span>
    <span class="results-stat-label">Total</span>
  </div>
</div>
    """.strip()


def render_results_back(*, on_back):
    back_col, _ = st.columns([1.4, 4])
    with back_col:
        st.button("← Edit guide", on_click=on_back, type="secondary", use_container_width=True)


def render_results_header(result):
    flagged = result["flagged_questions"]
    total = result["total_questions"]
    neutral = total - flagged
    title, description = _results_status_copy(result)
    accent = _flagged_ring_color(flagged, total)
    ring_svg = _neutral_progress_ring_svg(neutral, total, flagged)
    stats_html = _results_stats_html(flagged=flagged, neutral=neutral, total=total)
    st.markdown(
        f"""
<div class="results-hero-card" id="results-top">
  <div class="results-hero-body">
    <div class="results-ring-wrap">
      {ring_svg}
      <div class="results-ring-label">
        <span class="results-ring-value" style="color: {accent};">{neutral}/{total}</span>
        <span class="results-ring-sub">neutral</span>
      </div>
    </div>
    <div class="results-hero-copy">
      <h2 class="results-hero-title">{html.escape(title)}</h2>
      <p class="results-hero-desc">{html.escape(description)}</p>
    </div>
  </div>
  {stats_html}
</div>
        """,
        unsafe_allow_html=True,
    )


def _scroll_to_score():
    components.html(
        """
<script>
  (function () {
    function scrollToScore() {
      const doc = window.parent.document;
      const target = doc.getElementById("results-top");
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }
      const view = doc.querySelector('[data-testid="stAppViewContainer"]');
      if (view) {
        view.scrollTo({ top: 0, behavior: "smooth" });
        return;
      }
      const main = doc.querySelector("section.main") || doc.querySelector(".main");
      if (main) {
        main.scrollTo({ top: 0, behavior: "smooth" });
        return;
      }
      window.parent.scrollTo({ top: 0, behavior: "smooth" });
    }
    scrollToScore();
    setTimeout(scrollToScore, 100);
    setTimeout(scrollToScore, 300);
    setTimeout(scrollToScore, 600);
  })();
</script>
        """,
        height=0,
    )


def render_results_hero(result):
    render_results_header(result)


def _questions_for_export(result):
    if "guide_questions" in st.session_state:
        return [question.strip() for question in st.session_state.guide_questions]
    return [item["question"] for item in result["questions"]]


def request_copy_guide():
    result = st.session_state.get("analysis_result")
    if not result:
        return
    st.session_state["_clipboard_guide"] = questions_to_guide_text(
        _questions_for_export(result)
    )


def _inject_clipboard_copy(text):
    components.html(
        f"""
<script>
  (function () {{
    const text = {json.dumps(text)};
    const target = window.parent.navigator.clipboard || navigator.clipboard;
    if (target && target.writeText) {{
      target.writeText(text).catch(function () {{
        copyFallback(text);
      }});
      return;
    }}
    copyFallback(text);

    function copyFallback(value) {{
      const doc = window.parent.document;
      const area = doc.createElement("textarea");
      area.value = value;
      doc.body.appendChild(area);
      area.select();
      doc.execCommand("copy");
      doc.body.removeChild(area);
    }}
  }})();
</script>
        """,
        height=0,
    )


def render_analyze_again_footer(*, on_reanalyze):
    if clipboard_text := st.session_state.pop("_clipboard_guide", None):
        _inject_clipboard_copy(clipboard_text)
        st.toast("Copied to clipboard!", icon="📋")

    st.markdown('<div class="results-review-footer"></div>', unsafe_allow_html=True)
    copy_col, review_col = st.columns([1, 1.4], gap="medium")
    with copy_col:
        st.button(
            "📋  Copy",
            key="copy_guide_btn",
            type="secondary",
            use_container_width=True,
            on_click=request_copy_guide,
        )
    with review_col:
        st.button(
            "Review questions again",
            type="primary",
            use_container_width=True,
            on_click=on_reanalyze,
        )


def _summary_card_html(circle, label, value, value_color=None):
    color_style = f' style="color: {value_color};"' if value_color else ""
    return f"""
<div class="step-card">
  <span class="step-card-num">{circle}</span>
  <p class="step-card-body">
    <strong>{label}</strong>
    <span class="step-card-value"{color_style}>{value}</span>
  </p>
</div>
    """


def render_summary_cards(result):
    ui = _ui()
    total = result["total_questions"]
    flagged = result["flagged_questions"]
    neutral = total - flagged
    cards = [
        ("Q", "Total questions", total, ui["text_strong"]),
        (ICON_FLAGGED, "Total flagged", flagged, ui["status_flag"]),
        (ICON_OK, "Total neutral", neutral, ui["status_ok"]),
    ]
    cards_html = "".join(
        _summary_card_html(circle, label, value, color) for circle, label, value, color in cards
    )
    st.markdown(f'<div class="step-cards-row">{cards_html}</div>', unsafe_allow_html=True)


def _primary_rule_id(flags):
    priority = {"L1": 0, "L2": 1, "L3": 2}
    return min((flag["rule_id"] for flag in flags), key=lambda rule_id: priority.get(rule_id, 9))


def _review_question_pill_html():
    return (
        '<span class="question-badge question-review-pill" '
        'style="display:inline-flex;align-items:center;'
        "padding:0.18rem 0.55rem;font-size:0.75rem;font-weight:600;"
        'line-height:1.3;background:#fef2f2;border:1px solid #fecaca;color:#dc2626;">'
        "Review question"
        "</span>"
    )


def _rewrite_applied_pill_html():
    return (
        '<span class="question-badge question-rewrite-pill" '
        'style="display:inline-flex;align-items:center;gap:0.2rem;'
        "padding:0.18rem 0.55rem;font-size:0.75rem;font-weight:600;"
        'line-height:1.3;background:#ecfdf5;border:1px solid #a7f3d0;color:#047857;">'
        '<span aria-hidden="true"></span> Rewrite applied'
        "</span>"
    )


def _question_card_header_html(index, item, *, rewrite_applied=False):
    flags = item["flags"]
    if not flags:
        style = NEUTRAL_CARD
        icon = f'<span class="question-ok-icon" aria-label="Neutral">{ICON_OK}</span>'
        badge = style["label"]
        badge_style = f'background: {style["badge_bg"]}; color: {style["badge_text"]};'
        badge_html = f'<span class="question-badge" style="{badge_style}">{badge}</span>'
    else:
        icon = f'<span class="question-warn-icon" aria-label="Flagged">{ICON_WARN}</span>'
        if rewrite_applied:
            badge_html = _rewrite_applied_pill_html()
        else:
            badge_html = _review_question_pill_html()

    return f"""
<div class="question-card-header">
  {icon}
  <span class="question-id">Q{index}</span>
  {badge_html}
</div>
    """


def _question_card_inner_html(index, item, question_text, *, rewrite_applied=False):
    return (
        f"{_question_card_header_html(index, item, rewrite_applied=rewrite_applied)}"
        f'<p class="question-text">{html.escape(question_text)}</p>'
    )


def _question_card_inner_padding(*, split=False):
    bottom = QUESTION_CARD_SECTION_GAP if split else QUESTION_CARD_PAD_Y
    return f"padding:{QUESTION_CARD_PAD_TOP} {QUESTION_CARD_PAD_X} {bottom};"


def _question_card_comment_padding(*, end=False):
    bottom = QUESTION_CARD_PAD_Y if end else "0"
    return f"padding:{QUESTION_CARD_SECTION_GAP} {QUESTION_CARD_PAD_X} {bottom};"


def render_neutral_question_card(index, item):
    card_html = (
        QUESTION_CARD_MARKER
        + f'<div class="question-card-inner" style="{_question_card_inner_padding()}">'
        f'{_question_card_inner_html(index, item, item["question"])}'
        f"</div>"
    )
    with st.container(border=True):
        st.markdown(card_html, unsafe_allow_html=True)


@st.dialog("Edit your question", width="medium")
def _edit_question_dialog(edit_index, flags, fallback_question):
    draft_key = f"modal_draft_{edit_index}"
    pending_key = f"modal_suggestion_pending_{edit_index}"
    if draft_key not in st.session_state:
        st.session_state[draft_key] = _guide_question_text(edit_index, fallback_question)
    if pending_key in st.session_state:
        st.session_state[draft_key] = st.session_state.pop(pending_key)

    draft = st.text_area(
        "Edit your question",
        height=90,
        label_visibility="collapsed",
        key=draft_key,
    )
    rewrite = suggest_rewrite(draft, flags)
    if st.session_state.get(f"modal_suggestion_note_{edit_index}") and rewrite.get("draft"):
        st.markdown(
            '<p class="modal-suggestion-note">Suggestion applied — review before saving.</p>',
            unsafe_allow_html=True,
        )

    cancel_col, suggest_col, save_col = st.columns([1, 1.35, 1], gap="small")
    with cancel_col:
        if st.button("Cancel", use_container_width=True, key=f"modal_cancel_{edit_index}"):
            cancel_question_edit(edit_index)
            st.rerun()
    with suggest_col:
        if st.button(
            "✦  Get suggestion",
            use_container_width=True,
            key=f"modal_suggest_{edit_index}",
            disabled=not rewrite.get("draft"),
        ):
            st.session_state[pending_key] = rewrite["draft"]
            st.session_state[f"modal_suggestion_note_{edit_index}"] = True
            st.rerun()
    with save_col:
        if st.button(
            "Save",
            use_container_width=True,
            key=f"modal_save_{edit_index}",
        ):
            _set_guide_question(edit_index, st.session_state.get(draft_key, draft))
            if st.session_state.get(f"modal_suggestion_note_{edit_index}"):
                applied = set(st.session_state.get("suggestion_applied", []))
                applied.add(edit_index)
                st.session_state.suggestion_applied = list(applied)
            _close_edit_modal(edit_index)
            st.rerun()


def _flagged_comment_html(flags):
    parts = []
    for index, flag in enumerate(flags):
        margin = "0" if index == len(flags) - 1 else "0 0 0.65rem 0"
        parts.append(
            f'<p style="font-style:italic;color:#6b7280;font-size:0.92rem;'
            f'margin:{margin};line-height:1.6;">'
            f"<em>{html.escape(flag['explanation'])}</em></p>"
        )
    return "".join(parts)


def render_flagged_question_card(index, item):
    edit_index = index - 1
    editing_key = f"editing_{edit_index}"
    rule_id = _primary_rule_id(item["flags"])
    is_editing = st.session_state.get(editing_key, False)
    suggestion_applied = edit_index in set(st.session_state.get("suggestion_applied", []))
    question_text = _guide_question_text(edit_index, item["question"])
    desc_html = _flagged_comment_html(item["flags"]) if item["flags"] else ""
    show_edit = not suggestion_applied
    footer_parts = [desc_html] if desc_html else []
    has_footer = bool(footer_parts)
    split_inner = has_footer or show_edit
    inner_class = (
        "question-card-inner question-card-inner--split"
        if split_inner
        else "question-card-inner"
    )
    card_html = (
        QUESTION_CARD_MARKER
        + f'<div class="{inner_class}" style="{_question_card_inner_padding(split=split_inner)}">'
        f"{_question_card_inner_html(index, item, question_text, rewrite_applied=suggestion_applied)}"
        f"</div>"
    )
    if has_footer:
        comment_class = "question-card-comment"
        if not show_edit:
            comment_class += " question-card-comment--end"
        card_html += (
            '<hr style="border:none;border-top:1px solid #e5e7eb;margin:0;height:0;" />'
            f'<div class="{comment_class}" style="{_question_card_comment_padding(end=not show_edit)}">'
            f'{"".join(footer_parts)}</div>'
        )

    with st.container(border=True):
        st.markdown(card_html, unsafe_allow_html=True)

        if show_edit:
            st.markdown('<div class="flagged-revise-actions"></div>', unsafe_allow_html=True)
            st.button(
                "✏️  Edit",
                key=f"edit_btn_{edit_index}",
                type="secondary",
                use_container_width=True,
                on_click=start_question_edit,
                kwargs={
                    "edit_index": edit_index,
                    "fallback_question": item["question"],
                },
            )

    if is_editing:
        _edit_question_dialog(edit_index, item["flags"], item["question"])


def render_question_cards(questions):
    for index, item in enumerate(questions, start=1):
        if item["flags"]:
            render_flagged_question_card(index, item)
        else:
            render_neutral_question_card(index, item)


def show_overall_results(result):
    render_summary_cards(result)


def show_question_review(result):
    questions = result["questions"]

    if st.session_state.pop("_show_update_toast", False):
        st.toast(
            "Rewrite applied. Click Update score to refresh your neutrality score.",
            icon="✅",
        )

    st.markdown(
        """
<h1 class="results-question-title">Question review</h1>
<p class="results-question-subtitle">Edit any flagged questions below, then click <strong>Review questions again</strong> when you're done to see your updated results.</p>
        """,
        unsafe_allow_html=True,
    )

    render_question_cards(questions)
