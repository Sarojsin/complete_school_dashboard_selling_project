# Missing Endpoints Migration Plan - Priority 3: Communication Modules

**Plan 3: Communication & Social Features**

This plan covers Chat, Groups, and Messages modules.

## Module Overview

| Module | Missing Endpoints | Priority |
|--------|------------------|----------|
| Chat | 10 endpoints | MEDIUM |
| Groups | 16 endpoints | MEDIUM |
| Messages | 3 endpoints | MEDIUM |

---

## 1. Chat Module

**Target Location:** `modules/shared/chat/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/chat/conversations` | Get conversations | backup/api/endpoints/chat.py |
| GET | `/api/chat/messages/{other_user_id}` | Get messages | backup/api/endpoints/chat.py |
| POST | `/api/chat/messages/{receiver_id}` | Send message | backup/api/endpoints/chat.py |
| POST | `/api/chat/mark-read/{sender_id}` | Mark messages read | backup/api/endpoints/chat.py |
| GET | `/api/chat/unread-count` | Get unread count | backup/api/endpoints/chat.py |
| GET | `/api/chat/online-users` | Get online users | backup/api/endpoints/chat.py |
| GET | `/api/chat/search/{query}` | Search users | backup/api/endpoints/chat.py |
| GET | `/api/chat/contacts/parent` | Get parent contacts | backup/api/endpoints/chat.py |
| GET | `/api/chat/contacts/teacher` | Get teacher contacts | backup/api/endpoints/chat.py |
| GET | `/api/chat/search-messages/{query}` | Search messages | backup/api/endpoints/chat.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/shared/chat/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   ├── constants.py
   └── websocket.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/chat_repository.py`

3. **Implement WebSocket support:**
   - Add real-time messaging capability

4. **Implement API endpoints**

5. **Test endpoints**

---

## 2. Groups Module

**Target Location:** `modules/shared/groups/`

### Missing Endpoints to Implement

#### Group Management

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/groups/` | List groups | backup/api/endpoints/groups.py |
| GET | `/api/groups/create` | Create group page | backup/api/endpoints/groups.py |
| POST | `/api/groups/create` | Create group | backup/api/endpoints/groups.py |
| GET | `/api/groups/{group_id}` | Group detail | backup/api/endpoints/groups.py |
| GET | `/api/groups/{group_id}/edit` | Edit group page | backup/api/endpoints/groups.py |
| POST | `/api/groups/{group_id}/edit` | Update group | backup/api/endpoints/groups.py |
| GET | `/api/groups/{group_id}/manage` | Manage members page | backup/api/endpoints/groups.py |
| POST | `/api/groups/{group_id}/members/add` | Add members | backup/api/endpoints/groups.py |
| POST | `/api/groups/{group_id}/members/{user_id}/remove` | Remove member | backup/api/endpoints/groups.py |
| GET | `/api/groups/api/{group_id}/members` | Get group members API | backup/api/endpoints/groups.py |

#### Group Posts

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/group-posts/` | List posts | backup/api/endpoints/group_posts.py |
| GET | `/api/group-posts/create` | Create post page | backup/api/endpoints/group_posts.py |
| POST | `/api/group-posts/create` | Create post | backup/api/endpoints/group_posts.py |
| GET | `/api/group-posts/{post_id}` | View post | backup/api/endpoints/group_posts.py |
| POST | `/api/group-posts/{post_id}/delete` | Delete post | backup/api/endpoints/group_posts.py |
| GET | `/api/group-posts/api/posts` | Get posts API | backup/api/endpoints/group_posts.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/shared/groups/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   ├── constants.py
   └── web.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/group_repository.py`
   - Source: `backup/repositories/group_post_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## 3. Messages Module

**Target Location:** `modules/shared/messages/`

### Missing Endpoints to Implement

| Method | Endpoint | Description | Source File |
|--------|----------|-------------|-------------|
| GET | `/api/messages/all` | Get all messages | backup/api/endpoints/admin_messages.py |
| DELETE | `/api/messages/{message_id}` | Delete message | backup/api/endpoints/admin_messages.py |
| GET | `/api/messages/analytics` | Get message analytics | backup/api/endpoints/admin_messages.py |

### Implementation Steps

1. **Create module structure:**
   ```
   modules/shared/messages/
   ├── __init__.py
   ├── api.py
   ├── models.py
   ├── schemas.py
   ├── repository.py
   ├── service.py
   └── constants.py
   ```

2. **Copy models from backup:**
   - Source: `backup/repositories/message_repository.py`

3. **Implement API endpoints**

4. **Test endpoints**

---

## Migration Strategy

### Step 1: Analyze Existing Code
- Review `backup/api/endpoints/chat.py`
- Review `backup/api/endpoints/groups.py`
- Review `backup/api/endpoints/group_posts.py`
- Review `backup/api/endpoints/admin_messages.py`

### Step 2: Extract Logic
- Copy repository logic from backup/repositories/
- Adapt service layer for new structure

### Step 3: Create New Modules
- Create modules/shared/ for shared functionality
- Follow existing module pattern

### Step 4: WebSocket Integration
- Add WebSocket support for chat
- Implement real-time messaging

### Step 5: Integration
- Register routes in main.py
- Add to module exports

### Step 6: Testing
- Test REST endpoints
- Test WebSocket connections
- Test real-time messaging

---

## Time Estimate

| Module | Development Time | Testing Time |
|--------|-----------------|--------------|
| Chat (with WebSocket) | 3-4 days | 1-2 days |
| Groups | 2-3 days | 1 day |
| Messages | 1 day | 0.5 day |
| **Total** | **6-8 days** | **2.5-3.5 days** |

---

## Files to Reference

### Source Files (from backup/)
- `backup/api/endpoints/chat.py`
- `backup/api/endpoints/groups.py`
- `backup/api/endpoints/group_posts.py`
- `backup/api/endpoints/admin_messages.py`
- `backup/repositories/chat_repository.py`
- `backup/repositories/group_repository.py`
- `backup/repositories/group_post_repository.py`
- `backup/repositories/message_repository.py`

### Reference Templates
- `modules/shared/` (for shared module structure)
- `modules/web_common/` (for web routes)

---

## WebSocket Requirements

For Chat module, need to implement:
1. WebSocket connection handling
2. Real-time message delivery
3. Online status tracking
4. Message read receipts

---

## Dependencies

- Chat requires authentication
- Groups require membership management
- Messages require admin privileges for analytics

---

*Plan created: 2026-03-26*