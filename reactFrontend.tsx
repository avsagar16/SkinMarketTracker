import React, { useState } from 'react';

const InputInterface = () => {
  const [input, setInput] = useState('');
  const [status, setStatus] = useState({ message: '', type: '', show: false });
  const [isSubmitting, setIsSubmitting] = useState(false);

  const showStatus = (message, type) => {
    setStatus({ message, type, show: true });
    setTimeout(() => {
      setStatus(prev => ({ ...prev, show: false }));
    }, 3000);
  };

  const sendToBackend = async (inputText) => {
    console.log('Sending to backend:', inputText);
    setIsSubmitting(true);

    const payload = {
      input: inputText,
      timestamp: new Date().toISOString()
    };

    console.log('Payload being sent:', JSON.stringify(payload, null, 2));

    try {
      // For development: http://localhost:8000
      // For production: your deployed backend URL
      const API_BASE = process.env.NODE_ENV === 'production' 
        ? 'https://your-backend.herokuapp.com' 
        : 'http://localhost:8000';

      console.log(`Making request to: ${API_BASE}/api/process`);

      const response = await fetch(`${API_BASE}/api/process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      console.log('Response status:', response.status);

      if (response.ok) {
        const result = await response.json();
        console.log('Backend response:', result);
        showStatus('Success!', 'success');
        
        // Clear input after successful submission
        setInput('');
      } else {
        const errorData = await response.json();
        console.error('Backend error:', errorData);
        throw new Error(`HTTP error! status: ${response.status} - ${JSON.stringify(errorData)}`);
      }
    } catch (error) {
      console.error('Error sending to backend:', error);
      showStatus('Connection failed. Check console for details.', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSubmit = () => {
    const userInput = input.trim();
    if (!userInput) return;

    showStatus('Processing...', 'info');
    sendToBackend(userInput);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center overflow-hidden">
      {/* Status notification */}
      <div className={`fixed top-5 right-5 px-4 py-2 rounded-full backdrop-blur-md text-sm transition-all duration-300 transform ${
        status.show ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-5'
      } ${
        status.type === 'success' ? 'bg-green-500/90 text-white' :
        status.type === 'error' ? 'bg-red-500/90 text-white' :
        'bg-white/90 text-gray-800'
      }`}>
        {status.message}
      </div>

      {/* Input container */}
      <div className="w-full max-w-2xl px-5 animate-fadeInUp">
        <div className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type something..."
            maxLength={500}
            disabled={isSubmitting}
            className={`w-full px-6 py-5 text-lg border-none rounded-full bg-white/95 backdrop-blur-md shadow-2xl outline-none transition-all duration-300 text-gray-700 placeholder-gray-500 ${
              isSubmitting ? 'opacity-75 cursor-not-allowed' : 'hover:bg-white focus:bg-white focus:shadow-3xl focus:-translate-y-1'
            }`}
            autoFocus
          />
          
          {/* Submit button */}
          <button
            onClick={handleSubmit}
            disabled={!input.trim() || isSubmitting}
            className={`absolute right-2 top-1/2 -translate-y-1/2 w-11 h-11 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 border-none cursor-pointer transition-all duration-300 flex items-center justify-center ${
              input.trim() && !isSubmitting 
                ? 'opacity-100 hover:scale-110 hover:shadow-lg' 
                : 'opacity-0 pointer-events-none'
            }`}
          >
            {isSubmitting ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
            ) : (
              <svg className="w-5 h-5 fill-white" viewBox="0 0 24 24">
                <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
              </svg>
            )}
          </button>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(50px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fadeInUp {
          animation: fadeInUp 0.8s ease;
        }
        
        .shadow-3xl {
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
      `}</style>
    </div>
  );
};

export default InputInterface;