#!/usr/bin/env python
import sys
import warnings

from agentic_rag.crew import AgenticRag

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the Agentic RAG crew with live user input.
    """

    question = input("\nEnter your customer question:\n> ").strip()

    if not question:
        print("Please enter a question.")
        return

    inputs = {
        "question": question
    }

    try:
        result = AgenticRag().crew().kickoff(inputs=inputs)

        print("\nFINAL ANSWER:\n")
        print(result.raw)

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
def train():
    """
    Train the crew.
    """
    inputs = {
        "question": "I received a damaged laptop. Can I get a replacement?"
    }

    try:
        AgenticRag().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgenticRag().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution.
    """
    inputs = {
        "question": "I received a damaged laptop. Can I get a replacement?"
    }

    try:
        AgenticRag().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception(
            "No trigger payload provided. Please provide JSON payload as argument."
        )

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "question": ""
    }

    try:
        result = AgenticRag().crew().kickoff(inputs=inputs)
        return result

    except Exception as e:
        raise Exception(
            f"An error occurred while running the crew with trigger: {e}"
        )