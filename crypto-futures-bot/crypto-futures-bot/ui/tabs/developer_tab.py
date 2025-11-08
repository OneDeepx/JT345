"""
Developer Tab - Claude AI Assistant for Debugging
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from utils.logger import setup_logger
from config.settings import settings

logger = setup_logger('developer_tab')


class ClaudeAssistantThread(QThread):
    """Thread for Claude API calls to prevent UI blocking"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, message: str, conversation_history: list):
        super().__init__()
        self.message = message
        self.conversation_history = conversation_history
    
    def run(self):
        """Run Claude API call in background thread"""
        try:
            from anthropic import Anthropic
            
            # Get API key
            api_key = settings.get_api_key('claude').get('key')
            if not api_key:
                self.error_occurred.emit("Claude API key not configured. Please add it in Settings.")
                return
            
            # Initialize client
            client = Anthropic(api_key=api_key)
            
            # Prepare messages
            messages = self.conversation_history + [
                {"role": "user", "content": self.message}
            ]
            
            # Call Claude API
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=messages
            )
            
            # Extract response text
            response_text = response.content[0].text
            self.response_ready.emit(response_text)
            
        except Exception as e:
            error_msg = f"Error communicating with Claude: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)


class DeveloperTab(QWidget):
    """Developer console with Claude AI assistant"""
    
    def __init__(self):
        super().__init__()
        self.conversation_history = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the developer tab UI"""
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Claude AI Developer Assistant")
        header.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(header)
        
        # Description
        desc = QLabel(
            "Ask Claude to help debug code, explain errors, suggest improvements, "
            "or answer questions about the trading bot in plain English."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("padding: 5px; color: #aaaaaa;")
        layout.addWidget(desc)
        
        # Create splitter for chat and code sections
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Chat section
        chat_group = QGroupBox("Conversation")
        chat_layout = QVBoxLayout()
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("Conversation with Claude will appear here...")
        chat_layout.addWidget(self.chat_display)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(100)
        self.input_field.setPlaceholderText(
            "Type your question or paste error messages here...\n"
            "Press Ctrl+Enter to send"
        )
        self.input_field.installEventFilter(self)
        input_layout.addWidget(self.input_field)
        
        # Send button
        send_btn = QPushButton("Send")
        send_btn.setMinimumWidth(100)
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        
        chat_layout.addLayout(input_layout)
        chat_group.setLayout(chat_layout)
        splitter.addWidget(chat_group)
        
        # Code context section
        code_group = QGroupBox("Code Context (Optional)")
        code_layout = QVBoxLayout()
        
        code_desc = QLabel("Paste relevant code here to give Claude context:")
        code_desc.setStyleSheet("color: #aaaaaa;")
        code_layout.addWidget(code_desc)
        
        self.code_context = QTextEdit()
        self.code_context.setPlaceholderText(
            "# Paste your code here\n"
            "# Claude will use this as context when answering questions\n\n"
            "def example_function():\n"
            "    pass"
        )
        code_layout.addWidget(self.code_context)
        
        code_group.setLayout(code_layout)
        splitter.addWidget(code_group)
        
        # Set initial splitter sizes
        splitter.setSizes([400, 200])
        layout.addWidget(splitter)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear Conversation")
        clear_btn.clicked.connect(self.clear_conversation)
        button_layout.addWidget(clear_btn)
        
        clear_code_btn = QPushButton("Clear Code Context")
        clear_code_btn.clicked.connect(self.clear_code_context)
        button_layout.addWidget(clear_code_btn)
        
        button_layout.addStretch()
        
        export_btn = QPushButton("Export Conversation")
        export_btn.clicked.connect(self.export_conversation)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Add welcome message
        self.add_system_message(
            "Welcome to the Developer Console!\n\n"
            "I'm Claude, your AI debugging assistant. I can help you:\n"
            "• Debug errors and exceptions\n"
            "• Explain how parts of the code work\n"
            "• Suggest improvements and optimizations\n"
            "• Answer questions about trading strategies\n"
            "• Help with API integration issues\n\n"
            "Just type your question and I'll do my best to help!"
        )
    
    def eventFilter(self, obj, event):
        """Handle keyboard shortcuts"""
        if obj == self.input_field:
            if event.type() == event.Type.KeyPress:
                # Ctrl+Enter to send
                if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
                    self.send_message()
                    return True
        return super().eventFilter(obj, event)
    
    def send_message(self):
        """Send message to Claude"""
        message = self.input_field.toPlainText().strip()
        if not message:
            return
        
        # Add user message to display
        self.add_user_message(message)
        
        # Get code context if provided
        code_context = self.code_context.toPlainText().strip()
        
        # Build full message with context
        full_message = message
        if code_context:
            full_message = f"Here's some code for context:\n\n```python\n{code_context}\n```\n\n{message}"
        
        # Clear input
        self.input_field.clear()
        
        # Show thinking indicator
        self.add_system_message("Claude is thinking...")
        
        # Call Claude API in background thread
        self.claude_thread = ClaudeAssistantThread(full_message, self.conversation_history)
        self.claude_thread.response_ready.connect(self.on_response_ready)
        self.claude_thread.error_occurred.connect(self.on_error)
        self.claude_thread.start()
    
    def on_response_ready(self, response: str):
        """Handle Claude's response"""
        # Remove thinking indicator
        self.remove_last_message()
        
        # Add Claude's response
        self.add_assistant_message(response)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": self.input_field.toPlainText()})
        self.conversation_history.append({"role": "assistant", "content": response})
    
    def on_error(self, error: str):
        """Handle error from Claude API"""
        # Remove thinking indicator
        self.remove_last_message()
        
        # Add error message
        self.add_system_message(f"Error: {error}")
    
    def add_user_message(self, message: str):
        """Add user message to chat display"""
        self.chat_display.append(
            f'<div style="background-color: #2d4a5e; padding: 10px; margin: 5px; border-radius: 5px;">'
            f'<b style="color: #4caf50;">You:</b><br>{self._format_message(message)}'
            f'</div>'
        )
    
    def add_assistant_message(self, message: str):
        """Add assistant message to chat display"""
        self.chat_display.append(
            f'<div style="background-color: #3d2d4a; padding: 10px; margin: 5px; border-radius: 5px;">'
            f'<b style="color: #9c27b0;">Claude:</b><br>{self._format_message(message)}'
            f'</div>'
        )
    
    def add_system_message(self, message: str):
        """Add system message to chat display"""
        self.chat_display.append(
            f'<div style="background-color: #3d3d3d; padding: 10px; margin: 5px; border-radius: 5px;">'
            f'<i style="color: #aaaaaa;">{self._format_message(message)}</i>'
            f'</div>'
        )
    
    def remove_last_message(self):
        """Remove the last message from display"""
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.select(cursor.SelectionType.BlockUnderCursor)
        cursor.removeSelectedText()
        cursor.deletePreviousChar()
    
    def _format_message(self, message: str) -> str:
        """Format message for HTML display"""
        # Convert markdown-style code blocks to HTML
        import re
        
        # Replace code blocks
        message = re.sub(
            r'```(\w+)?\n(.*?)```',
            r'<pre style="background-color: #1e1e1e; padding: 10px; border-radius: 3px;"><code>\2</code></pre>',
            message,
            flags=re.DOTALL
        )
        
        # Replace inline code
        message = re.sub(
            r'`([^`]+)`',
            r'<code style="background-color: #1e1e1e; padding: 2px 4px; border-radius: 3px;">\1</code>',
            message
        )
        
        # Convert newlines to br tags
        message = message.replace('\n', '<br>')
        
        return message
    
    def clear_conversation(self):
        """Clear the conversation history"""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self,
            'Clear Conversation',
            'Are you sure you want to clear the conversation history?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_display.clear()
            self.conversation_history.clear()
            self.add_system_message("Conversation cleared. How can I help you?")
    
    def clear_code_context(self):
        """Clear the code context area"""
        self.code_context.clear()
    
    def export_conversation(self):
        """Export conversation to a file"""
        from PyQt6.QtWidgets import QFileDialog
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Conversation",
            "conversation.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    # Write conversation history
                    for msg in self.conversation_history:
                        role = "You" if msg['role'] == 'user' else "Claude"
                        f.write(f"{role}:\n{msg['content']}\n\n")
                
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"Conversation exported to {filename}"
                )
            except Exception as e:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export conversation: {str(e)}"
                )
    
    def update_display(self):
        """Update display (called by main window timer)"""
        # Nothing to update periodically for this tab
        pass
