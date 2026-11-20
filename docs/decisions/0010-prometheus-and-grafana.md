# Prometheus and Grafana for local monitoring

Use the Session 4 monitoring stack for the financial analyst service. Prometheus collects the request measurements on a schedule and stores them across API restarts. Grafana reads those stored measurements and displays their history.

The API exports the same counters and rolling measurements that feed its built-in dashboard. The Prometheus endpoint contains aggregates. The application still writes individual predictions and model version information to its audit log. The dashboard labels the rolling application p95 separately from the client p95 measured by the workload script.

The Compose monitoring profile starts two additional containers and supplies the data source and dashboard from version-controlled configuration. It uses the same tagged images as the Session 4 practical. The services listen on local host ports. Browser access to the local Grafana dashboard uses the Viewer role.

See the [monitoring guide](../monitoring.md) for startup, ports and the repeatable workload.
