
from __future__ import annotations
import re
import random
from datetime import datetime
from difflib import get_close_matches


class Chatbot:
    def __init__(self) -> None:
        # Simple memory for the session
        self.memory = {"name": None}

        # Intents: (pattern, handler)
        self.intents = [
            (re.compile(r"\b(hi|hello|hey|yo)\b", re.I), self._greet),
            (re.compile(r"\bhow (are|r) (you|u)\b", re.I), self._how_are_you),
            (re.compile(r"\bmy name is\s+([A-Za-z][A-Za-z\-']*)\b", re.I), self._remember_name),
            (re.compile(r"\bwhat'?s your name\b|\bwho are you\b", re.I), self._bot_name),
            (re.compile(r"\bwhat time is it\b|\bcurrent time\b|\btime\?\b", re.I), self._time),
            (re.compile(r"\bwhat'?s the date\b|\btoday'?s date\b|\bdate\?\b", re.I), self._date),
            (re.compile(r"\btell me a joke\b|\bjoke\b", re.I), self._joke),
            (re.compile(r"\b(help|commands)\b", re.I), self._help),
            (re.compile(r"\b(thank(s)?|ty)\b", re.I), self._thanks),
            (re.compile(r"\b(bye|exit|quit|goodbye)\b", re.I), self._goodbye),
            # basic sentiment check
            (re.compile(r"\b(sad|down|stressed|anxious|depressed)\b", re.I), self._support),
        ]

        # Known command keywords for suggestions (help text)
        self.commands = [
            "hello", "how are you", "my name is <Name>", "what's your name",
            "time", "date", "joke", "help", "thanks", "bye"
        ]

        # Small set of canned responses
        self.greetings = [
            "Hey there!", "Hello!", "Hi!", "Yo!",
            "Namaste!"  # 👋
        ]

        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "I told my computer I needed a break, and it said 'No problem—I'll go to sleep.'",
            "There are 10 kinds of people: those who understand binary and those who don't.",
        ]

    # === Intent handlers ===
    def _greet(self, _: re.Match) -> str:
        name = self.memory.get("name")
        base = random.choice(self.greetings)
        return f"{base} {'{0}!'.format(name) if name else ''}".strip()

    def _how_are_you(self, _: re.Match) -> str:
        return "Doing great, thanks for asking! How can I help today?"

    def _remember_name(self, m: re.Match) -> str:
        name = m.group(1).strip().title()
        self.memory["name"] = name
        return f"Nice to meet you, {name}!"

    def _bot_name(self, _: re.Match) -> str:
        return "I'm a tiny Python chatbot. You can call me PyPal."

    def _time(self, _: re.Match) -> str:
        return datetime.now().strftime("It's %I:%M %p.")

    def _date(self, _: re.Match) -> str:
        return datetime.now().strftime("Today is %A, %B %d, %Y.")

    def _joke(self, _: re.Match) -> str:
        return random.choice(self.jokes)

    def _help(self, _: re.Match) -> str:
        return (
            "Try: "
            + ", ".join(self.commands)
            + ".\nTip: Tell me your name with: 'my name is <Name>'."
        )

    def _thanks(self, _: re.Match) -> str:
        return "You're welcome!"

    def _goodbye(self, _: re.Match) -> str:
        return "Goodbye! See you soon."

    def _support(self, _: re.Match) -> str:
        return (
            "I'm sorry you're feeling that way. Want to talk about it a bit more? "
            "I'm here to listen."
        )

    # === Core logic ===
    def respond(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "Say something and I'll try to help. Type 'help' for options."

        # Match intents in order
        for pattern, handler in self.intents:
            m = pattern.search(text)
            if m:
                reply = handler(m)
                # If it's a goodbye intent, mark for exit via special token
                if handler is self._goodbye:
                    return reply + "\n__EXIT__"
                return reply

        # Fallback: suggest closest command
        suggestion = get_close_matches(text.lower(), [c.lower() for c in self.commands], n=1)
        if suggestion:
            return f"Not sure I got that. Did you mean: '{suggestion[0]}'? Type 'help' to see options."
        return "I didn't understand that. Type 'help' to see what I can do."


def chat_loop():
    bot = Chatbot()
    print("PyPal 🤖: Hi! Type 'help' to see what I can do. Type 'bye' to exit.")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nPyPal 🤖: Goodbye!")
            break
        reply = bot.respond(user)
        if reply.endswith("__EXIT__"):
            print("PyPal 🤖:", reply.replace("__EXIT__", ""))
            break
        print("PyPal 🤖:", reply)


if __name__ == "__main__":
    chat_loop()
