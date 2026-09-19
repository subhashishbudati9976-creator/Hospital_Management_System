from src.agent import agent


def print_banner() -> None:
    print("=" * 70)
    print("HOSPITAL APPOINTMENT AGENT - LANGCHAIN + OPENAI + AGENTIC AI")
    print("CLASSROOM DEMO: ALL HOSPITAL DATA IS SIMULATED")
    print("=" * 70)
    print("Examples:")
    print("  Find a dermatologist.")
    print("  What slots are available with Dr. Ananya Rao on 2026-10-15?")
    print("  Book a dermatology appointment for Venky Naidu on 2026-10-15 at 11:00.")
    print("  List the hospital departments.")
    print("  Exit with: quit")
    print("-" * 70)


def extract_text(result: dict) -> str:
    messages = result.get("messages", [])
    if not messages:
        return str(result)

    last = messages[-1]
    content = getattr(last, "content", None)

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)

    return str(content)


def main() -> None:
    print_banner()

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in {"quit", "exit"}:
            print("Assistant: Goodbye.")
            break

        if not user_input:
            continue

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input,
                        }
                    ]
                }
            )
            print("\nAssistant:")
            print(extract_text(result))

        except Exception as exc:
            print("\nApplication error:")
            print(exc)
            print(
                "Check your OpenAI API key, model name, internet connection, "
                "billing/credits, and installed packages."
            )


if __name__ == "__main__":
    main()
