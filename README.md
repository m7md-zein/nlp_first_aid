# 🩺 First Aid Chatbot — Delta University AI Project

NLP-based chatbot using NHS first aid guidelines.  
No external ML libraries needed (TF-IDF and Logistic Regression built from scratch).

## Project Structure

```
firstaid_chatbot/
├── data/
│   └── first_aid_data.csv     # Member 1: Dataset (question, answer, intent)
├── preprocessing.py           # Member 2: Text cleaning & NLP pipeline
├── model.py                   # Member 3: TF-IDF + Logistic Regression
├── chatbot.py                 # Member 4: Backend logic
├── app.py                     # Member 5: Flask web UI
├── cli.py                     # Member 5: CLI interface
└── requirements.txt
```

## Setup & Run

```bash
pip install flask

# Web interface (recommended)
python app.py
# → open http://localhost:5000

# OR command-line
python cli.py
```

## System Flow
1. User types a question
2. `preprocessing.py` → lowercase, remove punctuation, remove stopwords, stem
3. `model.py` TfidfVectorizer → convert to feature vector
4. `model.py` OneVsRestClassifier → predict intent + confidence
5. `chatbot.py` → map intent to NHS answer + emergency detection

## Intents (14 categories)
burns | bleeding | choking | fainting | cpr | heart_attack | stroke |
recovery_position | fractures | anaphylaxis | shock | electric_shock |
drowning | poisoning | needlestick | general

## Features
- ✅ TF-IDF feature extraction (from scratch)
- ✅ Logistic Regression classifier (from scratch)  
- ✅ Text preprocessing pipeline
- ✅ Emergency keyword detection with warning
- ✅ Synonym expansion
- ✅ Confidence threshold with fallback response
- ✅ Flask web UI with quick-question buttons
- ✅ CLI interface
- ✅ No external ML libraries required

## Team Responsibilities
| # | Member | Module |
|---|--------|--------|
| 1 | Data Collection | `data/first_aid_data.csv` |
| 2 | Preprocessing | `preprocessing.py` |
| 3 | NLP Model | `model.py` |
| 4 | Backend | `chatbot.py` |
| 5 | UI & Presentation | `app.py`, `cli.py` |

## Disclaimer
This chatbot provides general first aid guidance based on NHS guidelines.
**Always call 999 in a real emergency.**
Not a substitute for professional medical training or advice.
