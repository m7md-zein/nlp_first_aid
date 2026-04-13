"""
Member 5 (alt) - CLI Interface
Run: python cli.py
"""

from chatbot import FirstAidChatbot


def run_cli():
    print("=" * 55)
    print("       🩺  FIRST AID CHATBOT (NHS Guidelines)  🩺")
    print("        Delta University — AI Programming Project")
    print("=" * 55)
    print("Type your first aid question. Type 'quit' to exit.\n")
    print("⚠️  In a REAL emergency always call 999 first!\n")

    bot = FirstAidChatbot()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'q'):
            print("Bot: Stay safe! 👋")
            break

        response, intent, confidence = bot.get_response(user_input)
        print(f"\nBot: {response}")
        print(f"     [Intent: {intent} | Confidence: {confidence:.0%}]\n")


if __name__ == "__main__":
    run_cli()
