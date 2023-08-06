import click
from textx import metamodel_from_file, get_parent_of_type
from textx.scoping.tools import resolve_model_path
import jinja2
import os
import os.path as path
import logging
from . import class_options

THIS_FOLDER = path.dirname(__file__)


@click.command()
@click.option("--file", "-f", multiple=True)
@click.option("--output", "-o")
@click.option("--options", default="")
def classdiagram(file, output, options):
    output_path = output if path.isabs(output) else path.join(os.getcwd(), output)
    if not path.exists(output_path):
        logging.info("creating dir: " + output_path)
        os.mkdir(output_path)

    if not path.isdir(output_path):
        logging.exception("output is not a directory: " + output_path)
        exit(1)

    if options and (not path.exists(options) or not path.isfile(options)):
        logging.exception(
            "--options file is not a regular file or don't exists: {}".format(options)
        )
        exit(1)

    class_uml_meta = metamodel_from_file(
        path.join(THIS_FOLDER, "grammar", "class_uml.tx")
    )
    options_meta = metamodel_from_file(
        path.join(THIS_FOLDER, "grammar", "class_options.tx")
    )
    options_model = options_meta.model_from_file(options)

    # Initialize the template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(path.join(THIS_FOLDER, "templates")),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def isModelVisible(model, visibleField):
        if hasattr(model, "options") and model.options:
            try:
                if getattr(model.options, visibleField) == "hide":
                    return False
            except:
                pass

        parent = get_parent_of_type("Package", model)
        if parent:
            return isModelVisible(parent, visibleField)
        return True

    def isModelVisibleEntry(model):
        return isModelVisible(model, "visible")

    def isEdgeVisible(model):
        visible = isModelVisible(model, "visible")
        if not visible:
            return False
        return isModelVisible(model, "visibleConnections")

    jinja_env.filters["modelVisible"] = isModelVisibleEntry
    jinja_env.filters["edgeVisible"] = isEdgeVisible

    template = jinja_env.get_template("uml.jinja")

    for f in file:
        logging.info("processing file {}".format(f))
        model = class_uml_meta.model_from_file(f)
        class_options.overrideDefaultOptions(model=model, option_model=options_model)
        if not model.options.direction:
            model.options.direction = "BT"
        if not model.options.concentrate:
            model.options.concentrate = False
        if not model.options.colorScheme:
            model.options.colorScheme = "greys"
        if not model.options.splines:
            model.options.splines = "spline"

        with open(path.join(output_path, f + ".dot"), "w") as f:
            f.write(template.render(model=model, options=options))
