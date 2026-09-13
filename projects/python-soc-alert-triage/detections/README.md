# Detection Content

Portable detection examples for the synthetic Cedarline Systems SOC scenario.

## Contents

- Four Sigma YAML rules for reusable detection logic
- Splunk SPL queries for the bundled raw authentication and proxy formats
- Microsoft Sentinel KQL queries using example custom tables

The Sigma rules use normalized fields such as `source.ip`, `user.name`, `process.name`, `process.command_line`, `destination.domain`, and `network.bytes_out`. Map them to the local SIEM schema before deployment.

The SPL examples assume `index=cedarline` with `linux:sshd` and `cedarline:proxy` sourcetypes. The KQL examples assume `CedarlineAuth_CL` and `CedarlineProxy_CL` custom tables with a `RawData` column.

These rules are educational starting points. Validate field mappings, allowlists, thresholds, and schedules against approved activity before production use. The Python engine remains the authoritative executable implementation for this scenario.
