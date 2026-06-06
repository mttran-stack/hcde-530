"""
Interview Bias Checker — Streamlit UI.

Checker view: paste questions and analyze.
Results view: summary cards and per-question review.
"""

import streamlit as st

st.set_page_config(
    page_title="Interview Bias Checker",
    layout="centered",
    initial_sidebar_state="collapsed",
)

from rules import analyze_guide, questions_to_guide_text
from ui import (
    _scroll_to_score,
    render_analyze_again_footer,
    render_checker_header,
    render_checker_input,
    render_results_back,
    render_results_hero,
    setup_page,
    show_question_review,
)

DEMO_TEXT = """1. Don't you think the checkout flow is confusing?
2. Walk me through the last time you checked out.
3. How frustrating was it when the app crashed?
4. What happened when the app crashed?
5. Do you exercise, such as cycling?
6. Tell me about how you stay active."""


def _load_demo_guide():
    st.session_state.guide_text = DEMO_TEXT


def _init_analysis(guide_text, result):
    st.session_state.analysis_result = result
    st.session_state.analyzed_guide_text = guide_text
    st.session_state.guide_questions = [item["question"] for item in result["questions"]]
    st.session_state.suggestion_applied = []


def _collect_edited_questions():
    if "guide_questions" not in st.session_state:
        return [
            item["question"]
            for item in st.session_state.analysis_result["questions"]
        ]
    return [question.strip() for question in st.session_state.guide_questions]


def _request_reanalyze():
    st.session_state["_pending_reanalyze"] = True


def _reanalyze_edited_questions():
    edited = _collect_edited_questions()
    guide_text = questions_to_guide_text(edited)
    result = analyze_guide(guide_text)
    if result["total_questions"] == 0:
        st.session_state["_reanalyze_error"] = (
            "No questions found in your guide. Go back to edit your questions, "
            "then try updating your score again."
        )
        return
    st.session_state.pop("_reanalyze_error", None)
    _init_analysis(guide_text, result)
    st.session_state["_scroll_results_top"] = True


def _go_back_to_checker():
    if "guide_questions" in st.session_state:
        st.session_state.guide_text = questions_to_guide_text(
            st.session_state.guide_questions
        )
    elif "analyzed_guide_text" in st.session_state:
        st.session_state.guide_text = st.session_state.analyzed_guide_text
    st.session_state.page = "checker"


def _show_checker():
    render_checker_header()
    guide_text, analyze = render_checker_input(demo_callback=_load_demo_guide)

    if analyze:
        if not guide_text.strip():
            st.warning(
                "Add at least one interview question to analyze. "
                "Try the demo guide if you want an example."
            )
        else:
            result = analyze_guide(guide_text)

            if result["total_questions"] == 0:
                st.warning(
                    "We couldn't find any questions. Put one question per line, "
                    "or use numbered lines like 1. and 2."
                )
            else:
                _init_analysis(guide_text, result)
                st.session_state.page = "results"
                st.rerun()


def _show_results():
    if "analysis_result" not in st.session_state:
        st.markdown(
            '<div class="results-header"><h1>Results</h1>'
            "<p>Analyze your questions first.</p></div>",
            unsafe_allow_html=True,
        )
        return

    if st.session_state.pop("_pending_reanalyze", False):
        _reanalyze_edited_questions()

    scroll_to_score = st.session_state.pop("_scroll_results_top", False)
    reanalyze_error = st.session_state.pop("_reanalyze_error", None)
    if reanalyze_error:
        st.warning(reanalyze_error)
    render_results_back(on_back=_go_back_to_checker)
    render_results_hero(st.session_state.analysis_result)
    show_question_review(st.session_state.analysis_result)

    st.markdown('<div class="results-footer-spacer"></div>', unsafe_allow_html=True)
    render_analyze_again_footer(on_reanalyze=_request_reanalyze)
    if scroll_to_score:
        _scroll_to_score()


if "page" not in st.session_state:
    st.session_state.page = "checker"

setup_page(page=st.session_state.page)

if st.session_state.page == "results" and "analysis_result" in st.session_state:
    _show_results()
else:
    _show_checker()
