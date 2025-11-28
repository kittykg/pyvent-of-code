from datetime import datetime
from pathlib import Path
import subprocess

now = datetime.now()

curr_year = now.year
curr_day = now.day


def git_commit():
    # Git commit
    print(">-\tGit committing...")
    commit_message = f"{curr_year} Day {curr_day:02}"

    # Commit the new files
    commands = [
        f"git add .",
        f'git commit -m "{commit_message}"',
        f"git push",
    ]

    for command in commands:
        print(f">-\t{command}")
        subprocess.run(command, shell=True)


def _create_new_files(day: int):
    assert day > 0 and day <= 25, "Day must be between 1 and 25"

    # Create a new python file
    new_python_file = Path(f"./{curr_year}/day{day:02}.py")
    with open(new_python_file, "w") as f:
        f.write(
            f"""with open("input/day{day:02}", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\\n")))
    """
        )

    # Create a blank input file
    new_input_file = Path(f"./{curr_year}/input/day{day:02}")
    with open(new_input_file, "w") as f:
        f.write("\n")

    print(
        f">-\tFinished creating new files: {new_python_file} and {new_input_file}"
    )


def create_new_files_for_target_day(day: int):
    print(f">-\tCreating new files for day {day}...")
    _create_new_files(day)


def create_new_files_for_tomorrow():
    print(">-\tCreating new files for tomorrow...")
    _create_new_files(curr_day + 1)


print(f">- Finishing off Year {curr_year} Day {curr_day}")
print(f">- Commit? (**Y**/anything else for no)")
if input() == "Y":
    git_commit()

print(f">- Create new files for tomorrow? (anything else for yes/**N**)")
if input() != "N":
    create_new_files_for_tomorrow()
else:
    print(f">- Create new files for target day? (anything else for yes/**N**)")
    if input() != "N":
        create_new_files_for_target_day(int(input(f">- Enter the day: ")))
    else:
        print(f">- No new files created.")

print(f">- Done. Bye!")
