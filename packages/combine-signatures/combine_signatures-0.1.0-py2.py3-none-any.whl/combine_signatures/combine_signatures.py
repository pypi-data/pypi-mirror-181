from collections.abc import Mapping
import inspect

def combine_signatures(func, wrapper=None, include=None):
    from functools import partial, wraps
    from inspect import signature, _empty as insp_empty, _ParameterKind as ParKind
    from itertools import groupby

    if wrapper is None:
        return partial(combine_signatures, func, include=include)

    sig_func = signature(func)
    sig_wrapper = signature(wrapper)
    pars_func = {
        group: list(params)
        for group, params in groupby(sig_func.parameters.values(), key=lambda p: p.kind)
    }
    pars_wrapper = {
        group: list(params)
        for group, params in groupby(
            sig_wrapper.parameters.values(), key=lambda p: p.kind
        )
    }

    def render_annotation(p):
        return f"{':' + (repr(p.annotation) if not isinstance(p.annotation, type) else repr(p.annotation.__name__)) if p.annotation != insp_empty else ''}"

    def render_params(p):
        return f"{'=' + repr(p.default) if p.default != insp_empty else ''}"

    def render_by_kind(groups, key):
        parameters = groups.get(key, [])
        return [f"{p.name}{render_annotation(p)}{render_params(p)}" for p in parameters]

    pos_only = render_by_kind(pars_func, ParKind.POSITIONAL_ONLY)
    pos_or_keyword = render_by_kind(pars_func, ParKind.POSITIONAL_OR_KEYWORD)
    var_positional = [p for p in pars_func.get(ParKind.VAR_POSITIONAL, [])]
    keyword_only = render_by_kind(pars_func, ParKind.KEYWORD_ONLY)
    var_keyword = [p for p in pars_func.get(ParKind.VAR_KEYWORD, [])]

    extra_parameters = render_by_kind(pars_wrapper, ParKind.KEYWORD_ONLY)
    if include:
        if isinstance(include[0], Mapping):
            include = [
                f"{param['name']}{':' + param['annotation'] if 'annotation' in param else ''}{'=' + param['default'] if 'default' in param else ''}"
                for param in include
            ]
        else:
            include = [f"{name}=None" for name in include]

    def opt(seq, value=None):
        return ([value] if value else [", ".join(seq)]) if seq else []

    annotations = func.__annotations__.copy()
    for parameter in (pars_wrapper.get(ParKind.KEYWORD_ONLY) or ()):
        annotations[parameter.name] = parameter.annotation

    param_spec = ", ".join(
        [
            *opt(pos_only),
            *opt(pos_only, "/"),
            *opt(pos_or_keyword),
            *opt(
                keyword_only or extra_parameters,
                ("*" if not var_positional else f"*{var_positional[0].name}"),
            ),
            *opt(keyword_only),
            *opt(extra_parameters),
            *opt(include),
            *opt(var_keyword, f"**{var_keyword[0].name}" if var_keyword else ""),
        ]
    )

    coroutinedef = "async " if inspect.iscoroutinefunction(func) else ""
    declaration = f"{coroutinedef}def {func.__name__}({param_spec}): pass"

    f_globals = func.__globals__
    f_locals = {}

    exec(declaration, f_globals, f_locals)

    result = f_locals[func.__name__]
    result.__qualname__ = func.__qualname__
    result.__doc__ = func.__doc__
    result.__annotations__ = annotations

    return wraps(result)(wrapper)