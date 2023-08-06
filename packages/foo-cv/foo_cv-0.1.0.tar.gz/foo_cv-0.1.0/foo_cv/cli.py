import typer
from pathlib import Path
import jinja2
import json

app = typer.Typer()
app = typer.Typer(rich_markup_mode="rich")


def get_latex_jinja_env(template_base_path: Path):
    return jinja2.Environment(
        block_start_string="\BLOCK{",  # noqa:W605
        block_end_string="}",
        variable_start_string="\VAR{",  # noqa:W605
        variable_end_string="}",
        comment_start_string="\#{",  # noqa:W605
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(template_base_path),
    )


@app.command()
def generate_text(
    template: Path = typer.Argument(...),
    content: Path = typer.Argument(...),
    output: Path = typer.Argument(None),
):
    with open(content, "r") as f:
        content = json.load(f)

    latex_jinja_env = get_latex_jinja_env(template.parents[0])

    template = latex_jinja_env.get_template(template.name)

    rendered_content = template.render(**content)

    if output is None:
        print(rendered_content)
        exit(0)

    with open(output, "w") as f:
        f.write(rendered_content)


def main():
    app()
