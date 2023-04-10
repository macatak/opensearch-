# Opentelemetry for OpenSearch

### Otel 2 Data Prepper (stdout)
 - start the Data Prepper service  
 <code> bin/data-prepper config/pipelinesStdOut.yaml config/data-prepper-config.yaml</code>
 - Start the Otel service
 <code>otelcol --config /home/bikeride/vsCode/python/otel/otelCollectorYmls/otelColConf_dPrep.yml</code?
  - Run the Python sscript so send telemtry
 <code>/python3 otelCollector_1.py
