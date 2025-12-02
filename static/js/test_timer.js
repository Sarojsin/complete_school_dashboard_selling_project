class TestTimer {
    constructor(durationSeconds, onTimeUp) {
        this.remainingSeconds = durationSeconds;
        this.onTimeUp = onTimeUp;
        this.timerInterval = null;
        this.isPaused = false;
    }

    start() {
        this.updateDisplay();
        this.timerInterval = setInterval(() => {
            if (!this.isPaused && this.remainingSeconds > 0) {
                this.remainingSeconds--;
                this.updateDisplay();
                
                // Save progress every 30 seconds
                if (this.remainingSeconds % 30 === 0) {
                    this.autoSave();
                }
                
                // Warning at 5 minutes
                if (this.remainingSeconds === 300) {
                    this.showWarning('5 minutes remaining!');
                }
                
                // Warning at 1 minute
                if (this.remainingSeconds === 60) {
                    this.showWarning('1 minute remaining!');
                }
                
                if (this.remainingSeconds === 0) {
                    this.stop();
                    if (this.onTimeUp) {
                        this.onTimeUp();
                    }
                }
            }
        }, 1000);
    }

    stop() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    pause() {
        this.isPaused = true;
    }

    resume() {
        this.isPaused = false;
    }

    updateDisplay() {
        const hours = Math.floor(this.remainingSeconds / 3600);
        const minutes = Math.floor((this.remainingSeconds % 3600) / 60);
        const seconds = this.remainingSeconds % 60;
        
        const display = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        const timerElement = document.getElementById('timer');
        if (timerElement) {
            timerElement.textContent = display;
            
            // Change color when time is running out
            if (this.remainingSeconds <= 60) {
                timerElement.style.color = 'red';
                timerElement.style.fontWeight = 'bold';
            } else if (this.remainingSeconds <= 300) {
                timerElement.style.color = 'orange';
            }
        }
    }

    showWarning(message) {
        const warningDiv = document.createElement('div');
        warningDiv.className = 'timer-warning';
        warningDiv.textContent = message;
        warningDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff9800;
            color: white;
            padding: 15px 25px;
            border-radius: 5px;
            font-weight: bold;
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
        `;
        
        document.body.appendChild(warningDiv);
        
        setTimeout(() => {
            warningDiv.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => warningDiv.remove(), 300);
        }, 3000);
    }

    autoSave() {
        // Save current answers
        const answers = {};
        document.querySelectorAll('.question').forEach(question => {
            const questionId = question.dataset.questionId;
            const questionType = question.dataset.questionType;
            
            let answer = null;
            
            if (questionType === 'mcq' || questionType === 'true_false') {
                const selected = question.querySelector('input[type="radio"]:checked');
                if (selected) answer = selected.value;
            } else {
                const textarea = question.querySelector('textarea');
                if (textarea) answer = textarea.value;
            }
            
            if (answer) {
                answers[questionId] = answer;
            }
        });
        
        // Save to localStorage as backup
        const testId = document.getElementById('testId').value;
        localStorage.setItem(`test_${testId}_answers`, JSON.stringify(answers));
        
        console.log('Answers auto-saved');
    }
}

// Initialize test timer when page loads
document.addEventListener('DOMContentLoaded', () => {
    const timerElement = document.getElementById('timer');
    if (timerElement && timerElement.dataset.duration) {
        const duration = parseInt(timerElement.dataset.duration);
        
        const timer = new TestTimer(duration, () => {
            // Auto-submit when time is up
            alert('Time is up! Submitting your test...');
            document.getElementById('testForm').submit();
        });
        
        timer.start();
        
        // Handle page visibility change
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                timer.pause();
            } else {
                timer.resume();
            }
        });
        
        // Warn before leaving page
        window.addEventListener('beforeunload', (e) => {
            e.preventDefault();
            e.returnValue = 'Are you sure you want to leave? Your progress may not be saved.';
        });
        
        // Store timer reference globally
        window.testTimer = timer;
    }
    
    // Load saved answers from localStorage
    const testId = document.getElementById('testId')?.value;
    if (testId) {
        const savedAnswers = localStorage.getItem(`test_${testId}_answers`);
        if (savedAnswers) {
            const answers = JSON.parse(savedAnswers);
            Object.entries(answers).forEach(([questionId, answer]) => {
                const question = document.querySelector(`.question[data-question-id="${questionId}"]`);
                if (question) {
                    const questionType = question.dataset.questionType;
                    
                    if (questionType === 'mcq' || questionType === 'true_false') {
                        const radio = question.querySelector(`input[value="${answer}"]`);
                        if (radio) radio.checked = true;
                    } else {
                        const textarea = question.querySelector('textarea');
                        if (textarea) textarea.value = answer;
                    }
                }
            });
        }
    }
    
    // Submit test form
    const testForm = document.getElementById('testForm');
    if (testForm) {
        testForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Stop timer
            if (window.testTimer) {
                window.testTimer.stop();
            }
            
            // Collect answers
            const answers = {};
            document.querySelectorAll('.question').forEach(question => {
                const questionId = question.dataset.questionId;
                const questionType = question.dataset.questionType;
                
                let answer = null;
                
                if (questionType === 'mcq' || questionType === 'true_false') {
                    const selected = question.querySelector('input[type="radio"]:checked');
                    if (selected) answer = selected.value;
                } else {
                    const textarea = question.querySelector('textarea');
                    if (textarea) answer = textarea.value;
                }
                
                answers[questionId] = answer || '';
            });
            
            // Submit via AJAX
            const testId = document.getElementById('testId').value;
            const submitButton = testForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';
            
            fetch(`/api/tests/${testId}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({ answers })
            })
            .then(response => response.json())
            .then(data => {
                // Clear saved answers
                localStorage.removeItem(`test_${testId}_answers`);
                
                // Redirect to results
                window.location.href = `/student/test-result/${testId}`;
            })
            .catch(error => {
                console.error('Error submitting test:', error);
                alert('Error submitting test. Please try again.');
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Test';
            });
        });
    }
});