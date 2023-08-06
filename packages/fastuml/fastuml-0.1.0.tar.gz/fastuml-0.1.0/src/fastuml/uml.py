import click
from textx import metamodel_from_file
import jinja2
import os
import os.path as path

THIS_FOLDER = path.dirname(__file__)


@click.command()
@click.option("--file", "-f", multiple=True)
@click.option("--output", "-o")
def classdiagram(file, output):
    output_path = output if path.isabs(output) else path.join(os.getcwd(), output)
    if not path.exists(output_path):
        print("creating dir: " + output_path)
        os.mkdir(output_path)
    if not path.isdir(output_path):
        print("output is not a directory: " + output_path)
        return
    class_uml_meta = metamodel_from_file(path.join(THIS_FOLDER, "grammar", "uml.tx"))

    # Initialize the template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path.join(THIS_FOLDER, "templates")),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = jinja_env.get_template("uml.jinja")

    for f in file:
        print("processing" + f)
        model = class_uml_meta.model_from_file(f)
        if not model.options.concentrate:
            model.options.concentrate = False
        if not model.options.colorscheme:
            model.options.colorscheme = "greys"
        if not model.options.splines:
            model.options.splines = "spline"

        with open(path.join(output_path, f + ".dot"), "w") as f:
            f.write(template.render(model=model))
