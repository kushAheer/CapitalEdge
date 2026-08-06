import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import './ChatInterface.css';

const ChatInterface = ({ embedded = false }) => {
  const [messages, setMessages] = useState([
    { id: '1', role: 'assistant', content: 'Hello! Upload a document , and I can answer any questions you have about it.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const { user } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!input.trim() || !user || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    const newUserMsg = { id: Date.now().toString(), role: 'user', content: userMessage };
    setMessages(prev => [...prev, newUserMsg]);
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user.user_id,
          query: userMessage,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get response');
      }

      const data = await response.json();
      
      setMessages(prev => [
        ...prev, 
        { id: (Date.now() + 1).toString(), role: 'assistant', content: data.answer }
      ]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [
        ...prev, 
        { 
          id: (Date.now() + 1).toString(), 
          role: 'assistant', 
          content: error.message || 'Sorry, I encountered an error. Have you uploaded a document yet? Please try again.',
          isError: true
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className={`chat-container ${embedded ? 'chat-container--embedded' : 'surface-panel'}`}>
      {!embedded && (
        <div className="chat-header">
          <div className="chat-icon">
            <Bot size={20} />
          </div>
          <h2>AI Assistant</h2>
        </div>
      )}

      <div className="chat-messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-wrapper ${msg.role}`}>
            <div className={`message-avatar ${msg.role}`}>
              {msg.role === 'assistant' ? <Bot size={18} /> : <User size={18} />}
            </div>
            <div className={`message-bubble ${msg.role} ${msg.isError ? 'error' : ''}`}>
              <div className="message-content">{msg.content}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper assistant">
            <div className="message-avatar assistant">
              <Bot size={18} />
            </div>
            <div className="message-bubble assistant loading">
              <Loader2 className="animate-spin" size={18} />
              <span>Thinking...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form onSubmit={handleSubmit} className="chat-form">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your document..."
            rows={1}
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="chat-submit-btn"
            disabled={!input.trim() || isLoading}
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
