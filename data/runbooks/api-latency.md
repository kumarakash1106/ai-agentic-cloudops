
# API Latency Runbook

## Purpose
Investigate increased API response times.

## Investigation steps
1. Compare the deployment time with the latency increase.
2. Check whether the database connection pool is saturated.
3. Inspect slow database operations and database timeouts.
4. Compare the new release with the previous version.
5. Review application errors and service metrics.
6. Record the evidence supporting each finding.

## Safety
- Do not assume correlation proves causation.
- Do not execute a rollback automatically.
- Rollback must only be considered after human review and approval.

