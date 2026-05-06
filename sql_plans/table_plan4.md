# Table Plan 4: Transport & Logistics

## Overview
Student transportation management including routes, vehicles, assignments, and billing.

## Tables (12)

### Route Management
- `school_transport_routes` - Route definitions with times and fees
- `school_route_stops` - Pickup/dropoff points with coordinates
- `school_transport_fees` - Monthly/term transportation charges

### Vehicle Fleet
- `school_vehicles` - Vehicle inventory (buses, vans) with specs
- `school_vehicle_maintenance` - Service schedules and history
- `school_vehicle_fuel_logs` - Fuel consumption tracking
- `school_vehicle_drivers` - Driver assignments and licenses

### Student Assignments
- `school_student_transport` - Student-to-route/stop mapping
- `school_vehicle_assignments` - Daily vehicle-to-route scheduling
- `school_transport_attendance` - Daily student pickup/dropoff records

### Tracking & Monitoring
- `school_vehicle_gps_logs` - Real-time location history
- `school_transport_alerts` - Route deviation and delay notifications

## Dependencies
- Requires `college_students` from core academic module

## Estimated Complexity
High - Geospatial data, scheduling conflicts, and complex fee calculations.