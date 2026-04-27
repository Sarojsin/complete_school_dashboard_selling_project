# Plan 12: Notices & Messages Page Enhancement

## Objective
Enhance notices and messaging pages to match backup/templates quality.

## Current State (React)
- Notices page exists with basic list
- Messages through chat module
- No priority badges
- No content preview
- No filtering

## Required Changes

### 12.1 Student/Teacher Notices Page

#### Notice Cards List
Each notice should show:
- Title (bold)
- Priority badge (Urgent/High/Normal) with color
- Content preview (150 chars)
- Posted date
- Posted by (authority name)
- "Read More" link

#### Filter by Priority
- All
- Urgent
- High
- Normal

#### Create Notice (for teachers/authority)
- Title input
- Priority dropdown
- Content textarea
- Submit button

### 12.2 Authority Notices Management

#### Notices Dashboard
- List of all notices
- Create new notice
- Edit existing
- Delete
- Toggle active/inactive

#### Notice Analytics
- Total notices
- By priority breakdown
- Views count (if tracking)

### 12.3 Messages/Chat Enhancement

#### Chat List
- Contact name
- Last message preview
- Unread count badge
- Online status indicator

#### Chat Window
- Message bubbles (sent/received)
- Timestamp
- Read receipts
- File attachment support
- Emoji support

## Priority
MEDIUM - Communication is key

## Estimated Time
4-5 hours

## Files to Modify
- Modify: `frontend/src/modules/school/school_student/pages/Notices.jsx`
- Modify: `frontend/src/modules/school/school_teacher/pages/TeacherNotices.jsx`
- Modify: `frontend/src/modules/school/school_chat/pages/ChatList.jsx`
- Modify: `frontend/src/modules/school/school_chat/pages/ChatWindow.jsx`