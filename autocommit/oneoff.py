import argparse
import sys
from .chat import Chat
import subprocess
import os


def add_common_args(parser: argparse.ArgumentParser):
    parser.add_argument("--engine", default="gpt3.5-turbo",
                        help="OpenAI engine to use for completion",
                        choices=["gpt-3.5-turbo", "gpt-4o", "gpt-4-turbo", "gpt-4"])
    parser.add_argument("--language", default="english",
                        help="Language of the text")
    return parser


def build_prompt(base: str, language: str) -> str:
    return f"{base}. \n\nUse language: {language}"


def tldr() -> str:
    args = add_common_args(argparse.ArgumentParser(
        "tldr", description="Summarises a text from stdin")).parse_args()
    description = build_prompt(
        "Provide a one line summarisation of the following text. Try to keep as much content as possible", args.language)
    print(Chat(description=description).send(sys.stdin.read()))


def grammarly() -> str:
    args = add_common_args(argparse.ArgumentParser(
        "grammarly", description="Corrects grammar and style of a text from stdin")).parse_args()
    description = build_prompt(
        "Please rephrase this sentence to correct any grammatical errors and improve its style. Try to keep original tone of message", args.language)
    print(Chat(description=description).send(sys.stdin.read()))


def friendly() -> str:
    args = add_common_args(argparse.ArgumentParser(
        "friendly", description="Makes a text from stdin more friendly")).parse_args()
    description = build_prompt(
        "Rephrase following text to make it sound more nice and friendly", args.language)
    print(Chat(description=description).send(sys.stdin.read()))


def title() -> str:
    args = add_common_args(argparse.ArgumentParser(
        "title", description="Generates a title for a text from stdin")).parse_args()
    description = build_prompt(
        "Write a title for the following text", args.language)
    print(Chat(description=description).send(sys.stdin.read()))

# Get output of git diff and return it


def git_diff_into_string() -> str:
    try:
        output = subprocess.check_output(
            ["git", "diff", '--cached'], universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return ""


def commit() -> str:
    args = add_common_args(argparse.ArgumentParser(
        "commit", description="Generates a commit message for a diff from stdin")).parse_args()
    description = build_prompt(
        "Write a commit message which could be applied to a following diff", args.language)

    diff = git_diff_into_string()
    if diff == "":
        print("No changes, refusing to commit")
        return
    message = Chat(description=description).send(diff)
    os.system(f"git commit -m '{message}'")


def branch() -> str:
    args = add_common_args(argparse.ArgumentParser(
        "branch", description="Generates a branch name for a diff from stdin")).parse_args()
    description = build_prompt(
        "Write a branch name which a following diff could reside in", args.language)

    diff = git_diff_into_string()
    if diff == "":
        print("No changes, refusing to create branch")
        return
    branch_name = Chat(description=description).send(diff)
    os.system(f"git checkout -b {branch_name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("preset", choices=[
                        "commit", "branch", "pr", "grammarly", "friendly", "tldr"], help="Specify preset to follow")

    args = parser.parse_args()

    try:
        match args.preset:
            case 'commit':
                description = "Write a commit message which could be applied to a following diff"

            case 'branch':
                description = "Write a branch name which a following diff could reside in"

            case 'pr':
                description = "Write a text of a pull request a following diff could be content of"

            case "grammarly":
                description = "Please rephrase this sentence to correct any grammatical errors and improve its style. Try to keep original tone of message"

            case 'friendly':
                description = "Rephrase following text to make it sound more nice and friendly"

            case 'tldr':
                description = "Provide a one line summarisation of the following text. Try to keep as much content as possible"

            case 'title':
                description = "Write a title for the following text"

            case _:
                raise BaseException("Unknown preset")

        oneoff = Chat(
            description=description
        )

        data = sys.stdin.read()
        print(oneoff.send(data))
    except KeyboardInterrupt as e:
        pass
    except BaseException as e:
        print(str(e))


if __name__ == "__main__":
    main()
