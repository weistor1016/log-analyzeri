# Logging Schema

## Base Fields
- timestamp (ISO 8601)
- level (DEBUG | INFO | WARN | ERROR)
- service
- event
- message
- request_id

## Error Logs
Additional fields:
- error_code
- stack_trace

## Example
```json
{
  "timestamp": "2026-01-22T10:15:30Z",
  "level": "ERROR",
  "service": "payment",
  "event": "charge_failed",
  "message": "Payment authorization failed",
  "user_id": "u_789",
  "error_code": "PAY_402"
}
