"""
Leading-language detection for the interview bias checker.

Spec: ruleset.md (Choi & Pak 2005, Table 1 — Leading questions).
Rule-based only — predictable, auditable flags grounded in survey methodology.
"""

import re

# --- L1: Tag questions and forced agreement (Choi & Pak — "leading question") ---

TAG_PHRASES = [
    "don't you think",
    "dont you think",
    "don't you agree",
    "dont you agree",
    "don't you find",
    "dont you find",
    "wouldn't you",
    "wouldnt you",
    "wouldn't you agree",
    "isn't it",
    "isnt it",
    "isn't that",
    "isnt that",
    "aren't you",
    "arent you",
    "do you agree that",
    "would you agree that",
]

TAG_QUESTION_ENDING = ", do you?"

# --- L2: Framing — loaded / one-sided wording (Choi & Pak — "framing") ---

#Loaded words are words that carry positive or negative connotations.
LOADED_WORDS = [
    "frustrating",
    "frustrated",
    "annoying",
    "annoyed",
    "confusing",
    "confused",
    "terrible",
    "awful",
    "worst",
    "great",
    "wonderful",
    "horrible",
    "love",
    "hate",
]

#Loaded how patterns are patterns that suggest a positive or negative connotation in the form of a 'how' question.
LOADED_HOW_PATTERNS = [
    "how much do you love",
    "how much do you like",
    "how satisfied are you",
]

#One-sided how patterns assume how  users feels within the form of a 'how' question.
ONE_SIDED_HOW_PATTERNS = [
    ("how easy was", "or difficult"),
    ("how difficult was", "or easy"),
]

#Neutral openers that do not push judgment or suggest a particular answer.
NEUTRAL_OPENERS = (
    "tell me",
    "walk me through",
    "describe",
    "what happened",
    "what do you",
    "how do you",
    "what was",
    "what were",
    "what did you",
    "what tools do you",
    "what physical activity",
)

#Balanced frames suggest a neutral or balanced opinion in the question due to the use of 'or' to connect two different options.
BALANCED_FRAMES = [
    "or difficult",
    "or easy",
    "or dissatisfied",
    "or disagree",
]

#L3: Suggested answer in the question

#Proposes a cause or reason. The participant is nudged to confirm the idea instead of offering their own.
SUGGESTED_ANSWER_PATTERNS = [
    "was it because",
    "was that because",
    "is it because",
    "the reason you",
    "the reason that",
]

# Phrases that suggest a specific example (beginner-friendly — no regex)
LIKE_EXAMPLE_PHRASES = [
    " tools like ",
    " use tools like ",
    " use apps like ",
    " activities like ",
    " exercise like ",
    " do you use tools like ",
]

#Default explanations that will appear when a question is flagged for a specific rule.
EXPLANATIONS = {
    "L1": (
        "This is a tag or agreement question—wording that steers the participant "
        "toward yes or no instead of an open response."
    ),
    "L2": (
        "The question is framed with loaded or one-sided wording that suggests "
        "how the participant should feel or answer."
    ),
    "L3": (
        "The question suggests a specific answer or example rather than leaving "
        "the response open."
    ),
}

#Identifies which rule triggered the flag, the type of leading language detected, and an explanation of the rule.
def make_flag(rule_id, category):
    """Build one flag as a dictionary (beginner-friendly)."""
    return {
        "rule_id": rule_id,
        "category": category,
        "explanation": EXPLANATIONS[rule_id],
    }

#Normalizes the text to lowercase and strips whitespace.
def _normalize(text: str) -> str:
    return text.lower().strip()


def _starts_with_neutral_opener(text: str) -> bool:
    normalized = _normalize(text)
    for opener in NEUTRAL_OPENERS:
        if normalized.startswith(opener):
            return True
    return False


def _has_balanced_frame(text: str) -> bool:
    normalized = _normalize(text)
    for frame in BALANCED_FRAMES:
        if frame in normalized:
            return True
    return False


def _reflects_participant_quote(text: str, word: str) -> bool:
    """Skip loaded words the participant said, e.g. You said checkout was 'confusing'."""
    normalized = _normalize(text)
    if "you said" not in normalized:
        return False
    quote_markers = ('"', "'", "\u201c", "\u201d", "\u2018", "\u2019")
    has_quote = False
    for marker in quote_markers:
        if marker in text:
            has_quote = True
            break
    if not has_quote:
        return False
    you_said_index = normalized.find("you said")
    return word in normalized[you_said_index:]


def check_l1(text):
    normalized = _normalize(text)
    if "or disagree" in normalized:
        return None

    if normalized.endswith(TAG_QUESTION_ENDING):
        return make_flag("L1", "Leading question — tag questions and forced agreement")

    for phrase in TAG_PHRASES:
        if phrase in normalized:
            return make_flag("L1", "Leading question — tag questions and forced agreement")

    return None


def check_l2(text):
    if check_l1(text):
        return None

    normalized = _normalize(text)
    if _has_balanced_frame(text):
        return None

    if _starts_with_neutral_opener(text):
        return None

    for pattern, counterpart in ONE_SIDED_HOW_PATTERNS:
        if pattern in normalized and counterpart not in normalized:
            return make_flag("L2", "Framing — one-sided or loaded wording")

    for pattern in LOADED_HOW_PATTERNS:
        if pattern in normalized:
            return make_flag("L2", "Framing — one-sided or loaded wording")

    for word in LOADED_WORDS:
        if word in normalized and not _reflects_participant_quote(text, word):
            return make_flag("L2", "Framing — one-sided or loaded wording")

    return None


def check_l3(text):
    normalized = _normalize(text)

    for pattern in SUGGESTED_ANSWER_PATTERNS:
        if pattern in normalized:
            return make_flag("L3", "Leading question — suggested answer in the question")

    if "such as" in normalized:
        return make_flag("L3", "Leading question — suggested answer in the question")

    for phrase in LIKE_EXAMPLE_PHRASES:
        if phrase in normalized:
            return make_flag("L3", "Leading question — suggested answer in the question")

    return None


def analyze_question(text):
    """Return all rule matches for one question (list of flag dictionaries)."""
    if not text.strip():
        return []

    flags = []
    seen_rule_ids = set()

    for checker in (check_l1, check_l2, check_l3):
        result = checker(text)
        if result and result["rule_id"] not in seen_rule_ids:
            seen_rule_ids.add(result["rule_id"])
            flags.append(result)

    return flags


def parse_questions(text: str) -> list[str]:
    """Split pasted guide text into individual questions.

    Format A: one non-empty line = one question (no numbers).
    Format B: numbered/bulleted lines (1., 2., -, *) — strip marker, one line = one question.
    """
    if not text.strip():
        return []

    numbered = re.compile(r"^\d+[\).\s]+")
    bulleted = re.compile(r"^[-*•]\s+")

    questions: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        cleaned = numbered.sub("", line)
        cleaned = bulleted.sub("", cleaned).strip()
        if cleaned:
            questions.append(cleaned)

    if not questions:
        blocks = re.split(r"\n\s*\n", text.strip())
        for block in blocks:
            cleaned_block = block.strip()
            if cleaned_block:
                questions.append(cleaned_block)

    return questions


def questions_to_guide_text(questions: list[str]) -> str:
    """Rebuild pasted guide text from a list of question strings."""
    return "\n".join(f"{index}. {question}" for index, question in enumerate(questions, start=1))


def analyze_guide(text: str) -> dict:
    """Analyze a full pasted guide. Returns score, counts, and per-question flags."""
    questions = parse_questions(text)
    results = []
    flagged_count = 0

    for question in questions:
        flags = analyze_question(question)
        if flags:
            flagged_count += 1
        results.append({"question": question, "flags": flags})

    score = compute_bias_score(flagged_count, len(questions))
    return {
        "questions": results,
        "total_questions": len(questions),
        "flagged_questions": flagged_count,
        "bias_score": score,
        "score_band": score_band(score),
    }


def compute_bias_score(flagged_count: int, total_questions: int) -> int:
    """Overall bias score 0–100. Higher = more leading language detected."""
    if total_questions == 0:
        return 0
    return round(100 * flagged_count / total_questions)


def score_band(score: int) -> str:
    if score <= 33:
        return "Low"
    if score <= 66:
        return "Medium"
    return "High"


def _rule_priority(rule_id: str) -> int:
    return {"L1": 0, "L2": 1, "L3": 2}.get(rule_id, 9)


def _primary_flag_rule_id(flags: list[dict]) -> str:
    return min((flag["rule_id"] for flag in flags), key=_rule_priority)


def _strip_tag_phrases(text: str) -> str:
    cleaned = text.strip()
    normalized = _normalize(cleaned)
    for phrase in TAG_PHRASES:
        if phrase in normalized:
            start = normalized.index(phrase)
            cleaned = cleaned[:start] + cleaned[start + len(phrase) :]
            normalized = _normalize(cleaned)
    if normalized.endswith(TAG_QUESTION_ENDING):
        cleaned = cleaned[: -len(TAG_QUESTION_ENDING)]
    return cleaned.strip(" .?,;:")


def _suggest_rewrite_l1(text: str) -> str:
    topic = _strip_tag_phrases(text)
    if topic.lower().startswith("that "):
        topic = topic[5:]
    topic = topic.strip(" ?")
    if not topic:
        return "Tell me about your experience with this topic."
    topic_lower = topic.lower()
    for prefix in ("the ", "a ", "an "):
        if topic_lower.startswith(prefix):
            subject = topic[len(prefix) :]
            if subject.lower().endswith(" is confusing"):
                subject = subject[: -len(" is confusing")]
                return f"Walk me through your experience with {prefix}{subject.strip()}."
            if subject.lower().endswith(" was confusing"):
                subject = subject[: -len(" was confusing")]
                return f"Walk me through your experience with {prefix}{subject.strip()}."
    if topic.endswith("?"):
        topic = topic[:-1].strip()
    return f"Tell me about {topic}."


def _suggest_rewrite_l2(text: str) -> str:
    normalized = _normalize(text)
    if normalized.startswith("how frustrating was it when "):
        event = text.split("when ", 1)[-1].strip(" ?")
        return f"What happened when {event}?"
    if normalized.startswith("how annoying is it when "):
        event = text.split("when ", 1)[-1].strip(" ?")
        return f"What happens when {event}?"
    for pattern, counterpart in ONE_SIDED_HOW_PATTERNS:
        if pattern in normalized and counterpart not in normalized:
            return re.sub(
                re.escape(pattern),
                pattern.replace("how easy was", "how easy or difficult was")
                .replace("how difficult was", "how difficult or easy was"),
                text,
                count=1,
                flags=re.IGNORECASE,
            )
    if normalized.startswith("was ") and text.strip().endswith("?"):
        topic = text.strip()[4:].strip(" ?")
        return f"Tell me about {topic}."
    if normalized.startswith("how much do you love"):
        topic = text.split("love", 1)[-1].strip(" ?")
        return f"How do you feel about {topic}?"
    if normalized.startswith("how much do you like"):
        topic = text.split("like", 1)[-1].strip(" ?")
        return f"How do you feel about {topic}?"
    return "What happened when you used this?"


def _suggest_rewrite_l3(text: str) -> str:
    normalized = _normalize(text)
    if "such as" in normalized:
        before = text[: normalized.index("such as")].strip(" ,?")
        before_lower = before.lower()
        if "exercise" in before_lower or "active" in before_lower or "stay active" in before_lower:
            return "Tell me about how you stay active."
        if before_lower.startswith("do you "):
            topic = before[7:].strip(" ?")
            return f"Tell me about {topic}."
        if before_lower.startswith("what tools do you use"):
            return "What tools do you use?"
        return f"{before}?"
    for pattern in SUGGESTED_ANSWER_PATTERNS:
        if pattern in normalized:
            return "What led to that?"
    for phrase in LIKE_EXAMPLE_PHRASES:
        if phrase in normalized:
            draft = re.sub(r",?\s*like\s+[^?.]+", "", text, count=1, flags=re.IGNORECASE)
            draft = draft.strip(" ,?")
            if not draft.endswith("?"):
                draft += "?"
            return draft
    return "What do you do in that situation?"


def suggest_rewrite(question: str, flags: list[dict]) -> dict:
    """Return a rule-based draft rewrite for a flagged question."""
    if not flags:
        return {"draft": question, "rule_id": None}

    rule_id = _primary_flag_rule_id(flags)
    generators = {
        "L1": _suggest_rewrite_l1,
        "L2": _suggest_rewrite_l2,
        "L3": _suggest_rewrite_l3,
    }
    draft = generators[rule_id](question)
    return {
        "draft": draft,
        "rule_id": rule_id,
    }
