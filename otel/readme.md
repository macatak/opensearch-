# Opentelemetry for OpenSearch

### Otel 2 Data Prepper (stdout)
 - start the Data Prepper service  
 <code> bin/data-prepper config/pipelinesStdOut.yaml config/data-prepper-config.yaml</code>
 - Start the Otel service  
 <code>otelcol --config otelColConf_dPrep.yml</code>
  - Run the Python script so send telemtry  
 <code>/python3 otelCollector_1.py</code>
