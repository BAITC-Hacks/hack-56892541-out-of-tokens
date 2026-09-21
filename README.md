# HackAlem AI Rehearsal — Terminal FAQ Bot

Interactive terminal FAQ chatbot developed for HackAlem AI Closed Rehearsal #3 (Track 03 — LLM Applications, Task 01). The chatbot answers five predefined questions covering rehearsal timing, team composition, track assignment, repository submission deadlines, and prize terms. If a query is unrelated or outside the rehearsal FAQ scope, the bot responds with `не знаю`. As specified by the rehearsal rules, no RAG, vector database, or external LLM APIs are used.

## How Matching Works

1. **Input Normalization:** Lowercases the user input, replaces `ё` with `е`, and removes punctuation.
2. **Topic Scoring:** Computes relevance scores across the 5 predefined FAQ topics using weighted keyword and stem matching.
3. **Answer Retrieval:** Answers are loaded dynamically from `faq.txt` (never hardcoded in Python). The entry with the highest positive score is returned.
4. **Fallback:** If no meaningful topic keywords match, the bot prints `не знаю`.

## Requirements

- Python 3 (standard library only, no external dependencies)

## How to Run

```bash
python main.py
```

or:

```bash
python3 main.py
```

To exit the chatbot, type `exit`, `quit`, or `выход`.

## Usage Example

```text
HackAlem AI — FAQ репетиции
Задайте вопрос. Для выхода: exit
> Когда репетиция?
21–22 сентября 2026 года. Соревновательный слот: 21 сентября 18:30 — 22 сентября 20:00 по времени Астаны (UTC+5). Дедлайн сдачи — 22 сентября 20:00. Это закрытая репетиция №3, а основной HackAlem AI пройдет 23 сентября 2026 года.
> Сколько человек в команде?
В команде может быть от 1 до 3 человек. Один участник может состоять только в одной команде. На команду приходится один трек и одна задача.
> Какая сегодня погода?
не знаю
> exit
```

## Project Structure

```text
.
├── main.py
├── faq.txt
└── README.md
```
