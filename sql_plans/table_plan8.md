# Table Plan 8: Assets, Inventory & Facilities

## Overview
Physical asset management including procurement, assignments, maintenance, and depreciation.

## Tables (12)

### Asset Catalog
- `school_assets` - Asset inventory with specs, purchase info, warranty
- `school_asset_categories` - Taxonomy (electronics, furniture, lab equipment)
- `school_asset_locations` - Physical storage locations (room, building)

### Lifecycle Management
- `school_asset_assignments` - Who has what asset (student/teacher/room)
- `school_asset_maintenance_logs` - Service records and repairs
- `school_asset_depreciation` - Financial depreciation tracking
- `school_asset_insurance` - Insurance policies and claims

### Procurement & Transfer
- `school_purchase_orders` - Vendor orders and approvals
- `school_asset_transfers` - Inter-department/room transfers
- `school_asset_disposals` - Retirement, sale, or disposal records

### Inventory & Stock
- `school_inventory_items` - Consumable stock tracking
- `school_inventory_transactions` - In/out flows and adjustments
- `school_stocktaking_schedules` - Periodic inventory counts
- `school_stocktaking_results` - Count reconciliation and variance

### Equipment Booking
- `school_asset_bookings` - Reservation system for shared resources
- `school_asset_booking_conflicts` - Overlap detection

## Dependencies
- Requires `college_teachers`, `college_students`, `college_departments`

## Estimated Complexity
High - Complex tracking of physical items, barcode integration, and lifecycle.