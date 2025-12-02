class ChatClient {
    constructor(token) {
        this.token = token;
        this.ws = null;
        this.currentReceiverId = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/chat?token=${this.token}`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
            this.reconnectAttempts = 0;
            this.updateConnectionStatus(true);
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus(false);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            this.updateConnectionStatus(false);
            this.reconnect();
        };
    }

    reconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
            console.log(`Reconnecting in ${delay}ms...`);
            setTimeout(() => this.connect(), delay);
        }
    }

    sendMessage(receiverId, content) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'message',
                receiver_id: receiverId,
                content: content
            }));
        }
    }

    sendTyping(receiverId) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'typing',
                receiver_id: receiverId
            }));
        }
    }

    markAsRead(messageIds) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'mark_read',
                message_ids: messageIds
            }));
        }
    }

    handleMessage(data) {
        switch (data.type) {
            case 'message':
                this.displayMessage(data);
                break;
            case 'message_sent':
                this.onMessageSent(data);
                break;
            case 'user_status':
                this.updateUserStatus(data.user_id, data.status);
                break;
            case 'typing':
                this.showTypingIndicator(data.user_id, data.user_name);
                break;
        }
    }

    displayMessage(data) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message received';
        messageDiv.innerHTML = `
            <div class="message-content">
                <strong>${data.sender_name}</strong>
                <p>${this.escapeHtml(data.content)}</p>
                <span class="message-time">${this.formatTime(data.created_at)}</span>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Mark as read if chat is open
        if (this.currentReceiverId === data.sender_id) {
            this.markAsRead([data.id]);
        }
    }

    onMessageSent(data) {
        // Update UI to show message was sent
        console.log('Message sent:', data);
    }

    updateUserStatus(userId, status) {
        const statusIndicator = document.querySelector(`[data-user-id="${userId}"] .status-indicator`);
        if (statusIndicator) {
            statusIndicator.className = `status-indicator ${status}`;
        }
    }

    showTypingIndicator(userId, userName) {
        if (this.currentReceiverId !== userId) return;

        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.textContent = `${userName} is typing...`;
            indicator.style.display = 'block';

            // Hide after 3 seconds
            setTimeout(() => {
                indicator.style.display = 'none';
            }, 3000);
        }
    }

    updateConnectionStatus(connected) {
        const statusEl = document.getElementById('connectionStatus');
        if (statusEl) {
            statusEl.className = connected ? 'connected' : 'disconnected';
            statusEl.textContent = connected ? 'Connected' : 'Disconnected';
        }
    }

    formatTime(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
        }
    }
}

// Initialize chat when document is ready
let chatClient = null;

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        chatClient = new ChatClient(token);
        chatClient.connect();
    }

    // Send message on form submit
    const messageForm = document.getElementById('messageForm');
    if (messageForm) {
        messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input = document.getElementById('messageInput');
            const receiverId = document.getElementById('currentReceiverId').value;
            
            if (input.value.trim() && receiverId) {
                chatClient.sendMessage(parseInt(receiverId), input.value.trim());
                
                // Display sent message
                const chatMessages = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message sent';
                messageDiv.innerHTML = `
                    <div class="message-content">
                        <p>${chatClient.escapeHtml(input.value.trim())}</p>
                        <span class="message-time">${chatClient.formatTime(new Date())}</span>
                    </div>
                `;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                input.value = '';
            }
        });
    }

    // Typing indicator
    const messageInput = document.getElementById('messageInput');
    if (messageInput) {
        let typingTimer;
        messageInput.addEventListener('input', () => {
            clearTimeout(typingTimer);
            const receiverId = document.getElementById('currentReceiverId').value;
            if (receiverId) {
                chatClient.sendTyping(parseInt(receiverId));
            }
        });
    }
});