"""Output for the user."""

from datetime import datetime, timedelta
from typing import NoReturn
import sys

from rich.console import Console
from rich.theme import Theme

from .diff import colored_diff
from ..metadata import NAME, VERSION
from ..model import Label, Quiz


theme = Theme({
    "secondary": "grey69",
    "quiz": "medium_purple1",
    "inserted": "bright_green",
    "deleted": "bright_red"
})

console = Console(theme=theme)

WELCOME = f"""👋 Welcome to [underline]{NAME} [white not bold]v{VERSION}[/white not bold][/underline]!

Practice as many words and phrases as you like, for as long as you like.

[secondary]{NAME} quizzes you on words and phrases repeatedly. Each time you answer
a quiz correctly, {NAME} will wait longer before repeating it. If you
answer incorrectly, you get one additional attempt to give the correct
answer. If the second attempt is not correct either, {NAME} will reset
the quiz interval.

How does it work?
● To answer a quiz: type the answer, followed by Enter.
● To repeat the spoken text: type Enter without answer.
● To skip to the answer immediately: type ?, followed by Enter.
● To read more about an [link=https://en.wiktionary.org/wiki/underlined]underlined[/link] word: keep ⌘ (the command key) pressed
  while clicking the word. Not all terminals may support this.
● To quit: type Ctrl-C or Ctrl-D.
[/secondary]"""

DONE = f"""👍 Good job. You're done for now. Please come back later or try a different topic.
[secondary]Type `{NAME.lower()} -h` for more information.[/secondary]
"""

TRY_AGAIN = "⚠️  Incorrect. Please try again."

CORRECT = "✅ Correct.\n"


def format_duration(duration: timedelta) -> str:
    """Format the duration in a human friendly way."""
    if duration.days > 1:
        return f"{duration.days} days"
    seconds = duration.seconds + (24 * 3600 if duration.days else 0)
    if seconds >= 1.5 * 3600:  # 1.5 hours
        hours = round(seconds / 3600)
        return f"{hours} hours"
    if seconds >= 1.5 * 60:  # 1.5 minutes
        minutes = round(seconds / 60)
        return f"{minutes} minutes"
    return f"{seconds} seconds"


def format_datetime(date_time: datetime) -> str:
    """Return a human readable version of the datetime"""
    return date_time.isoformat(sep=" ", timespec="minutes")


def linkify(text: str) -> str:
    """Return a version of the text where each word is turned into a link to a dictionary."""
    return " ".join(f"[link=https://en.wiktionary.org/wiki/{word.lower()}]{word}[/link]" for word in text.split())


def feedback_correct(guess: Label, quiz: Quiz) -> str:
    """Return the feedback about a correct result."""
    return CORRECT + meaning(quiz) + other_answers(guess, quiz)


def feedback_incorrect(guess: Label, quiz: Quiz) -> str:
    """Return the feedback about an incorrect result."""
    evaluation = "" if guess == "?" else "❌ Incorrect. "
    return f'{evaluation}The correct answer is "{colored_diff(guess, quiz.answer)}".\n' + meaning(quiz)


def meaning(quiz: Quiz) -> str:
    """Return the quiz's meaning, if any."""
    if quiz.meanings:
        meanings = ", ".join(f'"{meaning}"' for meaning in quiz.meanings)
        return f'[secondary]Meaning {meanings}.[/secondary]\n'
    return ""


def other_answers(guess: Label, quiz: Quiz) -> str:
    """Return the quiz's other answers, if any."""
    if answers := quiz.other_answers(guess):
        label = "Another correct answer is" if len(answers) == 1 else "Other correct answers are"
        enumerated_answers = ", ".join([f'"{answer}"' for answer in answers])
        return f"""[secondary]{label} {enumerated_answers}.[/secondary]\n"""
    return ""


def instruction(quiz: Quiz) -> str:
    """Return the instruction for the quiz."""
    return f"[quiz]{quiz.instruction()}:[/quiz]"


def show_error_and_exit(message: str) -> NoReturn:
    """Print the error message to stderr and exit."""
    sys.stderr.write(message)
    sys.exit(2)
