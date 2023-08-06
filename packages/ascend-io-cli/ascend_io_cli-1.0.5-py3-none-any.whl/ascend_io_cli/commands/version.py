import typer

from ascend_io_cli import __version__
from ascend_io_cli.support import print_response

app = typer.Typer(help='Show the CLI version')


@app.callback(invoke_without_command=True)
def version(ctx: typer.Context):
  ver = {'cli-version': __version__}
  print_response(ctx, ver)
  raise typer.Exit()
