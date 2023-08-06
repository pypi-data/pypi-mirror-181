from opencensus.trace import execution_context, samplers
from opencensus.trace.tracer import Tracer
from qualname import qualname

from sohaotel.ext.otel.trace_exporter import SohaOtelHttpExporter


def _get_function_name(func):
    module = func.__module__
    name = qualname(func)
    if hasattr(func, "__qualname__") and func.__qualname__:
        name = func.__qualname__
    return "{}.{}".format(module, name)


def instrument_trace_func(name=None, exporter=None):
    if exporter is None:
        exporter = SohaOtelHttpExporter(
            service_name="my_service",
            retry_able=True
        )

    def decorator(func):
        def wrapper(*args, **kwargs):
            current_tracer = execution_context.get_opencensus_tracer()
            if current_tracer is not None and current_tracer.span_context is not None:
                soha_tracer = Tracer(sampler=samplers.AlwaysOnSampler(), exporter=exporter, span_context=current_tracer.span_context)
            else:
                soha_tracer = Tracer(sampler=samplers.AlwaysOnSampler(), exporter=exporter)
            name_span = _get_function_name(func)
            if name is not None:
                name_span = name

            if not execution_context.get_current_span():
                with soha_tracer.start_span(name=name_span):
                    return func(*args, **kwargs)

            else:
                with soha_tracer.span(name=name_span):
                    return func(*args, **kwargs)

        return wrapper

    return decorator


def instrument_trace_restful(name=None, exporter=None):
    if exporter is None:
        exporter = SohaOtelHttpExporter(
            service_name="my_service",
            retry_able=True
        )

    def decorator(func):
        def wrapper(*args, **kwargs):
            soha_tracer = Tracer(sampler=samplers.AlwaysOnSampler(), exporter=exporter)
            name_span = _get_function_name(func)
            if name is not None:
                name_span = name
            soha_tracer.start_span(name=name_span)
            return_value = func(*args, **kwargs)
            soha_tracer.end_span()
            return return_value

        return wrapper

    return decorator
