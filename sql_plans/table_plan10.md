# Table Plan 10: Reporting, Analytics & Generic Attachments

## Overview
Unified attachment system, reporting engine, user dashboards, and backup infrastructure.

## Tables (9)

### Generic Attachments
- `attachments` - Polymorphic attachments for any entity (assignments, notices, notes, tickets)
- `attachment_access_logs` - Who downloaded/viewed what and when

### Reports & Analytics
- `saved_reports` - User-defined report configurations
- `report_schedules` - Automated report generation and delivery
- `dashboard_widgets` - Pre-built widget definitions (charts, metrics, tables)
- `user_dashboard_preferences` - Personal dashboard layout and widget placement

### Backup & Recovery
- `backup_metadata` - Automated backup snapshots and storage location
- `restore_logs` - Data restore operations and verification

### Integration & Webhooks
- `webhook_endpoints` - External system notification URLs
- `webhook_delivery_logs` - Delivery attempts and retries

## Dependencies
- Used by all modules (attachments polymorphic)
- Optional: Exports from all reporting tables

## Implementation Priority

**Phase 10-A: Attachments Foundation**
1. `attachments` table first - enables file uploads across entire system
2. `attachment_access_logs` for audit

**Phase 10-B: Reporting Engine**
3. `saved_reports` - ad-hoc query builder output
4. `report_schedules` - automated reports
5. `dashboard_widgets` - pre-built visualizations
6. `user_dashboard_preferences` - personalization

**Phase 10-C: Infrastructure**
7. `backup_metadata` - automation integration
8. `restore_logs` - disaster recovery tracking
9. `webhook_endpoints` - third-party integrations
10. `webhook_delivery_logs` - monitoring

## Estimated Complexity
Medium - Attachment system is reusable; reporting UI requires frontend work.