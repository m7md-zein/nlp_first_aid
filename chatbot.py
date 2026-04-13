"""
Member 4 - Backend / Chatbot Logic
Handles: intent prediction, response mapping, confidence threshold, emergency detection
"""

import os
from preprocessing import preprocess_text
from model import train_model, load_model, BASE_DIR

# ─── Emergency keywords ───────────────────────────────────────────────────────
EMERGENCY_KEYWORDS = [
    'not breathing', 'stopped breathing', 'no pulse', 'heart stopped',
    'unconscious', 'collapsed', 'not responding', 'dying', 'dead',
    'severe bleeding', 'blood everywhere', 'cannot breathe', 'choking bad',
    'anaphylaxis', 'severe allergic', 'overdose', 'poisoned', 'electrocuted',
    'drowning', 'stroke', 'heart attack'
]

EMERGENCY_MSG = (
    "\n⚠️  EMERGENCY WARNING ⚠️\n"
    "This sounds like a serious emergency!\n"
    "Please call 999 (UK) or your local emergency number IMMEDIATELY.\n"
    "Do not delay — follow first aid steps while waiting for help.\n"
)

# ─── Synonym / keyword expansion map ─────────────────────────────────────────
SYNONYMS = {
    'burned': 'burn', 'burning': 'burn', 'scalded': 'scald', 'scald': 'burn',
    'bleeding': 'bleed', 'cut': 'bleed', 'wound': 'bleed',
    'choking': 'choke', 'choked': 'choke',
    'fainted': 'faint', 'passed out': 'faint', 'unconscious': 'faint',
    'heart attack': 'heart attack', 'cardiac': 'heart attack',
    'stroke': 'stroke', 'cpr': 'cpr', 'resuscitation': 'cpr',
    'broken': 'fracture', 'fracture': 'fracture', 'sprain': 'fracture',
    'allergy': 'anaphylaxis', 'allergic': 'anaphylaxis', 'epipen': 'anaphylaxis',
    'electrocuted': 'electric shock', 'electric': 'electric shock',
    'drowning': 'drowning', 'drowned': 'drowning',
    'poison': 'poisoning', 'overdose': 'poisoning',
}

# Confidence threshold — below this we ask for clarification
CONFIDENCE_THRESHOLD = 0.15

# Keyword override: if these words are in the input, force the intent
KEYWORD_OVERRIDE = {
    'chok': 'choking',
    'heimlich': 'choking',
    'abdominal thrust': 'choking',
    'back blow': 'choking',
    'airway block': 'choking',
    'not breathing': 'cpr',
    'stopped breathing': 'cpr',
    'no pulse': 'cpr',
    'cardiac arrest': 'cpr',
    'cpr': 'cpr',
    'chest compression': 'cpr',
    'recovery position': 'recovery_position',
    'unconscious': 'recovery_position',
    'epipen': 'anaphylaxis',
    'anaphylaxis': 'anaphylaxis',
    'anaphylactic': 'anaphylaxis',
    'needlestick': 'needlestick',
    'needle stick': 'needlestick',
    'electrocuted': 'electric_shock',
    'electric shock': 'electric_shock',
    'drowning': 'drowning',
    'drowned': 'drowning',
    'overdose': 'poisoning',
    'poisoned': 'poisoning',
    'fast stroke': 'stroke',
    'stroke': 'stroke',
}


class FirstAidChatbot:
    def __init__(self, data_path='data/first_aid_data.csv'):
        self.model = None
        self.vectorizer = None
        self.intent_answers = None
        self._load_or_train(data_path)

    def _load_or_train(self, data_path):
        model_path = os.path.join(BASE_DIR, 'model', 'model.pkl')
        if os.path.exists(model_path):
            print("Loading saved model...")
            self.model, self.vectorizer, self.intent_answers = load_model()
        else:
            print("Training model for the first time...")
            self.model, self.vectorizer, self.intent_answers, _ = train_model(data_path)

    def _apply_synonyms(self, text):
        """Expand known synonyms in text."""
        text_lower = text.lower()
        for syn, replacement in SYNONYMS.items():
            text_lower = text_lower.replace(syn, replacement)
        return text_lower

    def _is_emergency(self, text):
        text_lower = text.lower()
        return any(kw in text_lower for kw in EMERGENCY_KEYWORDS)

    def predict_intent(self, user_input):
        """Preprocess → TF-IDF → predict intent + confidence."""
        expanded = self._apply_synonyms(user_input)
        processed = preprocess_text(expanded)
        vec = self.vectorizer.transform([processed])[0]
        probas = self.model.predict_proba_single(vec)
        best_intent = max(probas, key=probas.get)
        confidence = probas[best_intent]
        return best_intent, confidence, probas

    def get_response(self, user_input):
        """Full pipeline: input → intent → response string."""
        if not user_input.strip():
            return "Please type a first aid question."

        # Check for emergency
        emergency = self._is_emergency(user_input)

        # Check keyword override first (handles stems/variants the model misses)
        text_lower = user_input.lower()
        override_intent = None
        for kw, mapped_intent in KEYWORD_OVERRIDE.items():
            if kw in text_lower:
                override_intent = mapped_intent
                break

        # Predict intent
        intent, confidence, _ = self.predict_intent(user_input)
        if override_intent:
            intent = override_intent
            confidence = max(confidence, 0.80)  # treat override as high confidence

        # Build response
        if confidence < CONFIDENCE_THRESHOLD:
            response = (
                "I'm not sure I understood that. Could you rephrase?\n"
                "I can help with: burns, bleeding, choking, fainting, CPR, "
                "heart attack, stroke, fractures, anaphylaxis, shock, "
                "poisoning, electric shock, drowning."
            )
        else:
            response = self.intent_answers.get(intent, "Sorry, I don't have information on that.")

        if emergency:
            response = EMERGENCY_MSG + "\n" + response

        return response, intent, confidence


if __name__ == "__main__":
    bot = FirstAidChatbot()
    tests = [
        "What do I do for a burn?",
        "Someone is choking!",
        "How to do CPR?",
        "I have a headache",
    ]
    print("\n=== Backend Test ===")
    for q in tests:
        resp, intent, conf = bot.get_response(q)
        print(f"Q: {q}")
        print(f"   Intent: {intent} (conf: {conf:.2f})")
        print(f"   Answer: {resp[:80]}...\n")
