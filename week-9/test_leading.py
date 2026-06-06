"""
Test suite for leading-language rules.

Each sub-rule (L1, L2, L3) has five questions that should flag and five that
should not — per ruleset.md and professor build-spec guidance.
"""

import unittest

from rules import analyze_question, compute_bias_score, parse_questions, suggest_rewrite


def should_flag(question: str) -> bool:
    return len(analyze_question(question)) > 0


def rule_ids(question):
    return {flag["rule_id"] for flag in analyze_question(question)}


class TestL1TagQuestions(unittest.TestCase):
    SHOULD_FLAG = [
        "Don't you think the checkout flow is confusing?",
        "Do you agree that onboarding is too long?",
        "You don't use the app daily, do you?",
        "Wouldn't you say the notifications are annoying?",
        "Isn't it frustrating when the app crashes?",
    ]

    SHOULD_NOT_FLAG = [
        "Do you agree or disagree that the layout is clear?",
        "Walk me through the last time you checked out.",
        "How do you feel about onboarding?",
        "What do you think about the checkout experience?",
        "What was going through your mind during checkout?",
    ]

    def test_flags_leading_examples(self):
        for question in self.SHOULD_FLAG:
            with self.subTest(question=question):
                self.assertTrue(should_flag(question), msg=question)
                self.assertIn("L1", rule_ids(question), msg=question)

    def test_ignores_clean_examples(self):
        for question in self.SHOULD_NOT_FLAG:
            with self.subTest(question=question):
                self.assertFalse(should_flag(question), msg=question)


class TestL2Framing(unittest.TestCase):
    SHOULD_FLAG = [
        "How frustrating was it when the app crashed?",
        "How much do you love the new dashboard?",
        "How easy was signup?",
        "Was the checkout process confusing?",
        "How annoying is it when notifications pile up?",
    ]

    SHOULD_NOT_FLAG = [
        "How easy or difficult was signup?",
        "How do you feel about the dashboard?",
        "What happened when the app crashed?",
        'You said checkout was "confusing"—what did you mean?',
        "Describe your experience with notifications.",
    ]

    def test_flags_leading_examples(self):
        for question in self.SHOULD_FLAG:
            with self.subTest(question=question):
                self.assertTrue(should_flag(question), msg=question)
                self.assertIn("L2", rule_ids(question), msg=question)

    def test_ignores_clean_examples(self):
        for question in self.SHOULD_NOT_FLAG:
            with self.subTest(question=question):
                self.assertFalse(should_flag(question), msg=question)


class TestL3SuggestedAnswer(unittest.TestCase):
    SHOULD_FLAG = [
        "Do you exercise, such as cycling?",
        "Was it because the layout was confusing?",
        "Is it because you don't trust the app?",
        "Do you use tools like Figma or Sketch?",
        "What tools do you use, such as Figma?",
    ]

    SHOULD_NOT_FLAG = [
        "What tools do you use for design?",
        "Tell me about how you stay active.",
        "Why did you stop using the app?",
        "What happened when the layout gave you trouble?",
        "Walk me through a time the layout gave you trouble.",
    ]

    def test_flags_leading_examples(self):
        for question in self.SHOULD_FLAG:
            with self.subTest(question=question):
                self.assertTrue(should_flag(question), msg=question)
                self.assertIn("L3", rule_ids(question), msg=question)

    def test_ignors_clean_examples(self):
        for question in self.SHOULD_NOT_FLAG:
            with self.subTest(question=question):
                self.assertFalse(should_flag(question), msg=question)


class TestScoringAndParsing(unittest.TestCase):
    def test_bias_score(self):
        self.assertEqual(compute_bias_score(0, 5), 0)
        self.assertEqual(compute_bias_score(2, 4), 50)
        self.assertEqual(compute_bias_score(0, 0), 0)

    def test_parse_numbered_questions(self):
        text = "1. Don't you think checkout is confusing?\n2. Walk me through checkout."
        parsed = parse_questions(text)
        self.assertEqual(len(parsed), 2)
        self.assertIn("Don't you think", parsed[0])

    def test_parse_one_question_per_line(self):
        text = (
            "Tell me about a recent time you logged into MyChart. Walk me through what happened.\n"
            "How did the experience feel as you were moving through it?\n"
            "How did you decide where to look first?\n"
            "Thinking about MyChart more broadly, how do you feel about your ability to find what you need?"
        )
        parsed = parse_questions(text)
        self.assertEqual(len(parsed), 4)


class TestRewriteSuggestions(unittest.TestCase):
    def test_l1_suggestion_opens_question(self):
        rewrite = suggest_rewrite("Don't you think the checkout flow is confusing?", [{"rule_id": "L1"}])
        self.assertIn("Walk me through", rewrite["draft"])
        self.assertFalse(analyze_question(rewrite["draft"]))

    def test_l2_suggestion_neutralizes_framing(self):
        rewrite = suggest_rewrite("How frustrating was it when the app crashed?", [{"rule_id": "L2"}])
        self.assertIn("What happened when", rewrite["draft"])
        self.assertFalse(analyze_question(rewrite["draft"]))

    def test_l3_suggestion_removes_example(self):
        rewrite = suggest_rewrite("Do you exercise, such as cycling?", [{"rule_id": "L3"}])
        self.assertIn("stay active", rewrite["draft"])
        self.assertFalse(analyze_question(rewrite["draft"]))


if __name__ == "__main__":
    unittest.main()
