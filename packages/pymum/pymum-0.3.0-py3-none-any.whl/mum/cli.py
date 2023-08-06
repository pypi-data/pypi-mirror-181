import click
import readline

from rich.console import Console

from mum.command import Command, MAP_COMMAND_TO_FUNC
from mum.constants import PROMPT
from mum.enums import CommandEnum
from mum.todo_file import TodoFile


def auto_completion(incomplete_text, state):
    commands = [
        command
        for command in MAP_COMMAND_TO_FUNC.keys()
        if command.startswith(incomplete_text)
    ]
    if state < len(commands):
        return commands[state]

    return None


class Mum:
    def __init__(self, todo_file: TodoFile) -> None:
        self._todo_file = todo_file
        self._console = Console()

    def run(self) -> None:
        while (input_ := self._console.input(PROMPT)) != CommandEnum.quit:
            command = Command(self._todo_file, input_, self._console)
            if command.run_command() is False:
                self._console.print(f"Command {input_} is not valid.")
                continue


@click.command()
def mum() -> None:
    todo_file = TodoFile()
    app = Mum(todo_file)
    readline.parse_and_bind("tab: complete")
    readline.set_completer(auto_completion)
    app.run()


if __name__ == "__main__":
    mum()
