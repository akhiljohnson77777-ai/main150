from groq import generate_response

def get_essay_details():
    print("\n=== AI Essay Refinement Assistant ===\n")

    topic = input("What is the topic of your essay? ").strip()
    essay_type = input(
        "What type of essay? (Argumentative/Expository/Descriptive/Persuasive/Analytical): "
    ).strip()

    print("\nSelect the desired essay word count:")
    print("1) 300 words\n2) 900 words\n3) 1200 words\n4) 2000 words")
    choice = input("Enter choice (1-4): ").strip()

    length_map = {
        "1": "300",
        "2": "900",
        "3": "1200",
        "4": "2000"
    }

    length = length_map.get(choice, "300")

    target_audience = input(
        "Who is the target audience? "
    ).strip()

    specific_points = input(
        "Any specific points that must be included? "
    ).strip()

    writing_style = input(
        "Preferred writing style? (Formal/Conversational): "
    ).strip()

    return {
        "topic": topic,
        "essay_type": essay_type,
        "length": length,
        "target_audience": target_audience,
        "specific_points": specific_points,
        "writing_style": writing_style
    }


def generate_initial_essay(d):
    try:
        temp = float(
            input("\nEnter temperature (0.2 structured, 0.7 creative): ").strip()
        )

        if not 0.0 <= temp <= 1.0:
            raise ValueError

    except ValueError:
        print("Invalid temperature. Using 0.3.")
        temp = 0.3

    prompt = f"""Write a complete {d['essay_type']} essay on '{d['topic']}'.

Target audience: {d['target_audience']}
Word count: approximately {d['length']} words
Writing style: {d['writing_style']}
Important points: {d['specific_points']}

The essay must contain:
1. An introduction
2. A clear and well-developed body
3. A strong conclusion

Make the essay clear, organized and suitable for the target audience."""

    essay = generate_response(
        prompt,
        temperature=temp,
        max_tokens=2048
    )

    print("\n=== GENERATED ESSAY ===\n")
    print(essay)

    return essay, temp


def refine_essay(essay, d, temp):
    print("\n=== REFINING THE ESSAY ===")

    intro_prompt = f"""Revise only the introduction of the following essay.

Topic: {d['topic']}
Target audience: {d['target_audience']}
Writing style: {d['writing_style']}

Make the introduction more engaging, create a strong hook, and make sure it
matches the target audience.

Essay:
{essay}

Return only the improved introduction."""

    introduction = generate_response(
        intro_prompt,
        temperature=temp,
        max_tokens=1024
    )

    body_prompt = f"""Revise only the body of the following essay.

Topic: {d['topic']}
Target audience: {d['target_audience']}
Writing style: {d['writing_style']}

Make the body clear and well structured.
Break long paragraphs into shorter paragraphs.
Make sure every major point is fully developed.
Improve transitions, clarity and logical flow.

Essay:
{essay}

Return only the improved body."""

    body = generate_response(
        body_prompt,
        temperature=temp,
        max_tokens=2048
    )

    conclusion_prompt = f"""Revise only the conclusion of the following essay.

Topic: {d['topic']}
Target audience: {d['target_audience']}
Writing style: {d['writing_style']}

Create a strong and memorable conclusion.
Summarize the main ideas without unnecessary repetition.
End with an impactful final point.

Essay:
{essay}

Return only the improved conclusion."""

    conclusion = generate_response(
        conclusion_prompt,
        temperature=temp,
        max_tokens=1024
    )

    print("\n=== REFINED INTRODUCTION ===\n")
    print(introduction)

    print("\n=== REFINED BODY ===\n")
    print(body)

    print("\n=== REFINED CONCLUSION ===\n")
    print(conclusion)

    refined_essay = (
        introduction
        + "\n\n"
        + body
        + "\n\n"
        + conclusion
    )

    return refined_essay


def adapt_writing_style(essay, d, temp):
    style_prompt = f"""Rewrite the following essay in a {d['writing_style']} style.

Target audience: {d['target_audience']}
Topic: {d['topic']}

Preserve the main ideas and important information.
Do not change the meaning.
Make the language and tone appropriate for the requested style.

Essay:
{essay}

Return only the adapted essay."""

    adapted = generate_response(
        style_prompt,
        temperature=temp,
        max_tokens=2048
    )

    print("\n=== STYLE-ADAPTED ESSAY ===\n")
    print(adapted)

    return adapted


def create_feedback(essay, d, temp):
    feedback_prompt = f"""Review the following refined essay.

Topic: {d['topic']}
Target audience: {d['target_audience']}
Writing style: {d['writing_style']}

Provide feedback on:

1. Structure
2. Tone
3. Content
4. Clarity
5. Effectiveness

Explain what is working well and how the essay could be improved further.
Keep the feedback concise and practical.

Essay:
{essay}"""

    feedback = generate_response(
        feedback_prompt,
        temperature=temp,
        max_tokens=1024
    )

    with open("feedback.txt", "w", encoding="utf-8") as file:
        file.write("AI ESSAY FEEDBACK\n")
        file.write("=================\n\n")
        file.write(feedback)

    print("\n=== FEEDBACK ===\n")
    print(feedback)
    print("\nFeedback saved to feedback.txt")


def run_activity():
    print("\nWelcome to the AI Essay Refinement Assistant!")

    details = get_essay_details()

    if not details["topic"] or not details["essay_type"]:
        print("Please provide a topic and essay type to continue.")
        return

    essay, temperature = generate_initial_essay(details)

    refined_essay = refine_essay(
        essay,
        details,
        temperature
    )

    adapt_choice = input(
        "\nWould you like to adapt the essay to the selected writing style? (Yes/No): "
    ).strip().lower()

    if adapt_choice in ("yes", "y"):
        final_essay = adapt_writing_style(
            refined_essay,
            details,
            temperature
        )
    else:
        final_essay = refined_essay

    create_feedback(
        final_essay,
        details,
        temperature
    )

    print("\n=== ACTIVITY COMPLETED ===")
    print("The essay has been refined and feedback has been saved.")


if __name__ == "__main__":
    run_activity()