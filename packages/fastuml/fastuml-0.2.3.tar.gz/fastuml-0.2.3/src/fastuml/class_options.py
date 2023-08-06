def overrideOptions(model, options):
    if not model.options:
        model.options = options
    else:
        assignOpt(options, model, "visible")
        assignOpt(options, model, "visibleConnections")


def overridePackageOptions(package, option_model):
    if not option_model:
        return
    options = option_model.options

    overrideOptions(package, options)

    for p in package.packages:
        child_opt_model = getElement(option_model.packages, lambda x: x.name == p.name)
        if child_opt_model:
            overridePackageOptions(package=p, option_model=child_opt_model)

    for c in package.classes:
        child_opt_model = getElement(option_model.classes, lambda x: x.name == c.name)
        overrideClassOptions(class_model=c, option_model=child_opt_model)


def overrideClassOptions(class_model, option_model):
    if not option_model:
        return
    options = option_model.options

    overrideOptions(class_model, options)


def getElement(optList, filterFn):
    for m in optList:
        if filterFn(m):
            return m
    return None


def assignOpt(opt, package, field):
    val = getattr(opt, field)
    if val:
        setattr(package, field, val)


def overrideDefaultOptions(model, option_model):
    if hasattr(option_model, "options"):
        opts = option_model.options
        if not model.options:
            model.options = opts
        else:
            assignOpt(opts, model.options, "direction")
            assignOpt(opts, model.options, "concentrate")
            assignOpt(opts, model.options, "colorScheme")
            assignOpt(opts, model.options, "splines")

    for package in model.packages:
        optPackage = getElement(
            option_model.packages, lambda opt: opt.name == package.name
        )
        overridePackageOptions(package, optPackage)

    for c in model.classes:
        child_opt_model = getElement(option_model.classes, lambda x: x.name == c.name)
        overrideClassOptions(class_model=c, option_model=child_opt_model)
    pass
