import re
import sys
from pathlib import Path

# Ensure UTF-8 I/O across platforms (especially Windows consoles/pipes)
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOPIC_KEYWORDS = {
    "TIME": {
        "strong": [
            r"\bрепетици\w*",
            r"\bслот\w*",
            r"\bрасписани\w*",
            r"\bграфик\w*",
            r"\bдлит\w*",
            r"\bдлительност\w*",
            r"\bначн\w*",
            r"\bначин\w*",
            r"\bначал\w*",
            r"\bзаконч\w*",
            r"\bзаканчива\w*",
            r"\bконец\b",
            r"\bконца\b",
        ],
        "weak": [
            r"\bкогда\b",
            r"\bврем\w*",
            r"\bдат\w*",
            r"\bчисл\w*",
            r"\bпроход\w*",
            r"\bпройдет\b",
        ],
    },
    "TEAM": {
        "strong": [
            r"\bкоманд\w*",
            r"\bучастник\w*",
            r"\bсостав\w*",
            r"\bчеловек\w*",
            r"\bлюд\w*",
            r"\bвтроем\b",
            r"\bвдвоем\b",
            r"\bсоло\b",
        ],
        "weak": [
            r"\bскольк\w*",
            r"\bразмер\w*",
            r"\bчисленност\w*",
        ],
    },
    "TRACK": {
        "strong": [
            r"\bтрек\w*",
            r"\btrack\w*",
            r"\bнаправлен\w*",
            r"\bllm\b",
            r"\bллм\b",
            r"\bзадач\w*",
            r"\bзадани\w*",
            r"\bagent\w*",
            r"\bагент\w*",
            r"\bcv\b",
            r"\bсиви\b",
            r"\bвижн\b",
            r"\bvision\b",
        ],
        "weak": [
            r"\bтемат\w*",
        ],
    },
    "SUBMISSION": {
        "strong": [
            r"\bсда\w*",
            r"\bдедлайн\w*",
            r"\bdeadline\w*",
            r"\bрепозитор\w*",
            r"\bрепо\b",
            r"\brepo\w*",
            r"\brepository\w*",
            r"\bsubmission\w*",
            r"\bsubmit\w*",
            r"\bсабмит\w*",
            r"\bгит\w*",
            r"\bgit\b",
            r"\bgithub\b",
            r"\bсрок\w*",
            r"\bотправ\w*",
        ],
        "weak": [
            r"\bкуда\b",
            r"\bзагруз\w*",
        ],
    },
    "PRIZES": {
        "strong": [
            r"\bприз\w*",
            r"\bденьг\w*",
            r"\bденеж\w*",
            r"\bфонд\w*",
            r"\bвыплат\w*",
            r"\bнаград\w*",
            r"\bпобедител\w*",
            r"\bпобед\w*",
            r"\bсертификат\w*",
            r"\bмерч\w*",
            r"\bвыигрыш\w*",
            r"\bподар\w*",
        ],
        "weak": [
            r"\bрубл\w*",
            r"\bтенге\b",
            r"\bkzt\b",
            r"\busd\b",
            r"\bдоллар\w*",
        ],
    },
}

TOPIC_ORDER = ["TIME", "TEAM", "TRACK", "SUBMISSION", "PRIZES"]


def normalize(text: str) -> str:
    """Normalize input: lowercase, ё -> е, strip punctuation."""
    text = text.lower().replace("ё", "е")
    # Replace punctuation characters with whitespace
    text = re.sub(r"[^\w\s]", " ", text)
    return text


def load_faq(filepath: Path) -> dict[str, str]:
    """Parse faq.txt and return a mapping from topic to answer."""
    if not filepath.exists():
        raise FileNotFoundError(f"FAQ file not found: {filepath}")

    content = filepath.read_text(encoding="utf-8")
    blocks = [b.strip() for b in re.split(r"\n\s*\n", content) if b.strip()]

    faq_answers = {}
    for i, block in enumerate(blocks):
        q_match = re.search(r"^Q:\s*(.+)$", block, re.MULTILINE)
        a_match = re.search(r"^A:\s*(.+)$", block, re.MULTILINE | re.DOTALL)
        if q_match and a_match:
            answer = a_match.group(1).strip()
            topic = TOPIC_ORDER[i] if i < len(TOPIC_ORDER) else f"TOPIC_{i}"
            faq_answers[topic] = answer

    return faq_answers


def score_topic(normalized_text: str, topic: str) -> float:
    """Calculate relevance score for a given topic."""
    config = TOPIC_KEYWORDS.get(topic, {})
    strong_patterns = config.get("strong", [])
    weak_patterns = config.get("weak", [])

    score = 0.0
    for pat in strong_patterns:
        matches = re.findall(pat, normalized_text)
        score += len(matches) * 2.0

    for pat in weak_patterns:
        matches = re.findall(pat, normalized_text)
        score += len(matches) * 1.0

    return score


def find_best_answer(query: str, faq_answers: dict[str, str]) -> str:
    """Find the closest FAQ answer or return 'не знаю'."""
    normalized = normalize(query)
    if not normalized.strip():
        return "не знаю"

    best_topic = None
    best_score = 0.0

    for topic in TOPIC_ORDER:
        score = score_topic(normalized, topic)
        if score > best_score:
            best_score = score
            best_topic = topic

    if best_score > 0 and best_topic and best_topic in faq_answers:
        return faq_answers[best_topic]

    return "не знаю"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    faq_path = base_dir / "faq.txt"

    faq_answers = load_faq(faq_path)

    print("HackAlem AI — FAQ репетиции")
    print("Задайте вопрос. Для выхода: exit")

    while True:
        try:
            user_input = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        cleaned = user_input.strip()
        if not cleaned:
            continue

        if cleaned.lower() in {"exit", "quit", "выход"}:
            break

        answer = find_best_answer(user_input, faq_answers)
        print(answer)


if __name__ == "__main__":
    main()
