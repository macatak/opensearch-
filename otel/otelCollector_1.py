
'''
Add attributes to a span
https://opentelemetry.io/docs/instrumentation/python/manual/
'''

# new
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, BatchSpanProcessor, ConsoleSpanExporter

# collector setup??
# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "otel_42"
})

provider = TracerProvider(resource=resource)
# local
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True))
# docker
#processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:9417", insecure=True))

provider.add_span_processor(processor)
trace.set_tracer_provider(provider)


# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)


if __name__ == "__main__":
    # print("current span: ", trace.get_current_span())  
    with tracer.start_as_current_span("parent") as parent:
        # do some work that 'parent' tracks
        print("doing some work...")
        # set some values
        current_span = trace.get_current_span()
        current_span.set_attribute("operation.vaue", 1)
        current_span.set_attribute("operation.name", "spam and eggs!")
        current_span.set_attribute("operation.other-stuff", [1, 2, 3])
        with tracer.start_as_current_span("child") as child:
            # do some work that 'child' tracks
            print("doing some nested work...")
            current_span = trace.get_current_span()
            current_span.set_attribute("operation.vaue", 2)
            current_span.set_attribute("operation.name", "eggs and spam!")
            current_span.set_attribute("operation.other-stuff", [2, 3, 1])
            # the nested span is closed when it's out of scope
    print("span info: ", trace.get_current_span()) 
    # This span is also closed when it goes out of scope