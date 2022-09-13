import typer
from empiric.cli import config, net
from empiric.cli.contracts import oracle, publisher_registry
from empiric.cli.utils import coro

app = typer.Typer(help="contract deployment utilities")

app.add_typer(
    publisher_registry.app,
    name="publisher-registry",
    help="publisher registry contract utils",
)
app.add_typer(oracle.app, name="oracle", help="Oracle contract utils")


@app.command()
def list():
    """List all implemented contracts"""
    typer.echo("publisher_registry")
    typer.echo("oracle")


@app.command()
<<<<<<< HEAD
def deploy(
    ctx: typer.Context,
    config_file: str = config.DEFAULT_CONFIG,
    oracle_config: str = oracle.ORACLE_CONFIG,
):
=======
def deploy(ctx: typer.Context, config_file=config.DEFAULT_CONFIG):
>>>>>>> 0044c8d (add entity and shortcuts to cli)
    """List all implemented contracts"""
    typer.echo("deploy Publisher Registry")
    ctx.invoke(publisher_registry.deploy, config_file)
    typer.echo("oracle")
<<<<<<< HEAD
    ctx.invoke(oracle.deploy, config_file, oracle_config)
=======
    ctx.invoke(oracle.deploy, config_file)
>>>>>>> 0044c8d (add entity and shortcuts to cli)
