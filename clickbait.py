import re


def clickbait_score(text):

    score = 0
    reasons = []

    text_lower = text.lower()


    # 1. Sensational words
    sensational_words = [
        "shocking",
        "unbelievable",
        "amazing",
        "incredible",
        "secret",
        "exposed",
        "breaking",
        "disturbing",
        "miracle",
        "you won't believe"
    ]

    found_words = []

    for word in sensational_words:

        if word in text_lower:
            found_words.append(word)


    if found_words:

        score += min(len(found_words) * 10, 30)

        reasons.append(
            "Sensational words: "
            + ", ".join(found_words)
        )


    # 2. Too many exclamation marks

    exclamation_count = text.count("!")

    if exclamation_count >= 2:

        score += 20

        reasons.append(
            "Excessive exclamation marks"
        )


    # 3. Too many question marks

    question_count = text.count("?")

    if question_count >= 2:

        score += 15

        reasons.append(
            "Excessive question marks"
        )


    # 4. Capital letters

    letters = [
        char for char in text
        if char.isalpha()
    ]

    if len(letters) > 0:

        capital_letters = sum(
            1 for char in letters
            if char.isupper()
        )

        capital_percentage = (
            capital_letters / len(letters)
        ) * 100

    else:

        capital_percentage = 0


    if capital_percentage > 25:

        score += 20

        reasons.append(
            "Excessive capitalization"
        )


    # 5. Curiosity phrases

    curiosity_phrases = [
        "you won't believe",
        "what happens next",
        "this is why",
        "find out",
        "what they don't want you to know",
        "before it's too late"
    ]

    found_phrases = []

    for phrase in curiosity_phrases:

        if phrase in text_lower:
            found_phrases.append(phrase)


    if found_phrases:

        score += 20

        reasons.append(
            "Curiosity-gap phrases: "
            + ", ".join(found_phrases)
        )


    # Maximum score = 100

    score = min(score, 100)


    # Determine level

    if score >= 60:

        level = "HIGH CLICKBAIT"

    elif score >= 30:

        level = "MODERATE CLICKBAIT"

    else:

        level = "LOW CLICKBAIT"


    return score, level, reasons
if __name__ == "__main__":

    news = input("\nEnter a headline: ")

    score, level, reasons = clickbait_score(news)

    print("\nClickbait Score:", score)
    print("Level:", level)

    print("\nReasons:")

    if reasons:

        for reason in reasons:
            print("✓", reason)

    else:

        print("✓ No major clickbait indicators detected")