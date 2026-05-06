# Table Plan 5: Canteen & Food Services

## Overview
Canteen operations including menu management, ordering, meal plans, and nutrition tracking.

## Tables (10)

### Menu & Inventory
- `school_canteen_menu_items` - Daily/weekly menu with pricing
- `school_canteen_inventory` - Ingredient and supply tracking
- `school_canteen_vendors` - External vendor management (if applicable)

### Ordering & Service
- `school_canteen_orders` - Student/faculty order headers
- `school_canteen_order_items` - Line items with quantities and status
- `school_meal_plans` - Subscription-based meal packages
- `school_student_meal_plans` - Student enrollment in plans

### Operations & Quality
- `school_canteen_attendance` - Student meal consumption records
- `school_canteen_feedback` - Quality ratings and complaints
- `school_canteen_suppliers` - Procurement and vendor management

### Nutrition & Compliance
- `school_food_nutrition` - Nutritional information per item
- `school_allergen_alerts` - Allergen tracking for safety

## Dependencies
- Requires `college_students` and `college_teachers`
- Optional integration with `college_attendance` for meal eligibility

## Estimated Complexity
Medium - Order management and inventory tracking with moderate complexity.