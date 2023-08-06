from pathlib import Path

import typer

app = typer.Typer()


@app.command()
def hello(
    name: str,
    create_png: bool = typer.Option(False, help="create a png."),
    file: Path = typer.Argument(default=None, help="ultisnips source", exists=True),
):
    typer.echo(f"Hello {name}, {file}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


if __name__ == "__main__":
    app()
