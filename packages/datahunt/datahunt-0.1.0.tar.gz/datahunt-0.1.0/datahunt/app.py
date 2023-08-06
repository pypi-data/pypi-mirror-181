import json
import click
import urllib3


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


@click.group()
def main():
    pass


@main.command("submit")
@click.option("--file", help="SQL File.", required=True)
@click.option("--exercise", help="Exercise code e.g esql1", required=True)
def submit(file, exercise):

    exercise = exercise.lower()

    with open(file, "r") as file_reader:
        content = file_reader.read()

    http = urllib3.PoolManager()

    data = json.dumps({"query": f"""{content}""", "exercise": exercise})

    res = http.request(
        method="POST",
        url="https://datahunt.fly.dev/checkdata",
        headers={"Content-Type": "application/json"},
        body=data,
    )

    result = json.loads(res.data)

    print(f"Exercise: {exercise}")
    if result == "True":
        print(f"Pass: {bcolors.OKGREEN}{result}{bcolors.ENDC}")
    else:
        print(f"Pass: {bcolors.WARNING}{result}{bcolors.ENDC}")


if __name__ == "__main__":
    main()
