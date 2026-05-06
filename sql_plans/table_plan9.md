# Table Plan 9: Events, Communication & Feedback

## Overview
Campus events, messaging, surveys, support tickets, and engagement tools.

## Tables (12)

### Events & Calendar
- `school_events` - Event definitions with location, time, capacity
- `school_event_attendees` - Student/faculty registration and attendance
- `school_holidays` - Non-instructional days and breaks
- `school_academic_calendar` - Academic year milestones and deadlines

### Messaging & Communication
- `message_conversations` - Threaded chat sessions
- `message_participants` - Conversation membership
- `message_attachments` - File attachments to messages
- `message_read_receipts` - Delivery and read tracking
- `message_reactions` - Emoji/response reactions

### Surveys & Feedback
- `feedback_surveys` - Survey definitions and distribution
- `survey_questions` - Question bank with types (MCQ, text, rating)
- `survey_responses` - Individual response headers
- `survey_response_details` - Question-by-question answers

### Support System
- `support_tickets` - Issue reports with priority and status
- `ticket_replies` - Support team communications
- `ticket_categories` - Issue taxonomy and routing
- `ticket_attachments` - Evidence and screenshot uploads

## Dependencies
- Requires `college_students`, `college_teachers`, `college_parents`

## Estimated Complexity
Medium - Standard relational patterns; moderate complexity in surveys and tickets.