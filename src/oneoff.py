import argparse
import sys
from chat import Chat


if __name__ == "__main__":
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
