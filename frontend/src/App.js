import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [inbox, setInbox] = useState(null);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [customName, setCustomName] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [copySuccess, setCopySuccess] = useState(false);
  const [selectedMessage, setSelectedMessage] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    let interval;
    if (autoRefresh && inbox) {
      interval = setInterval(() => {
        fetchMessages();
      }, 5000); // Refresh every 5 seconds
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh, inbox]);

  const createInbox = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/inbox/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          custom_name: customName || null
        })
      });

      if (!response.ok) {
        throw new Error('Failed to create inbox');
      }

      const data = await response.json();
      setInbox(data.inbox);
      setMessages([]);
      setCustomName('');
    } catch (error) {
      console.error('Error creating inbox:', error);
      alert('Ошибка при создании email адреса. Попробуйте еще раз.');
    } finally {
      setLoading(false);
    }
  };

  const fetchMessages = async () => {
    if (!inbox || !inbox.token) return;

    try {
      const response = await fetch(
        `${backendUrl}/api/inbox/${inbox.id}/messages?token=${inbox.token}`
      );

      if (!response.ok) {
        throw new Error('Failed to fetch messages');
      }

      const data = await response.json();
      setMessages(data);
    } catch (error) {
      console.error('Error fetching messages:', error);
    }
  };

  const copyToClipboard = () => {
    if (inbox?.email) {
      navigator.clipboard.writeText(inbox.email);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const openMessage = (message) => {
    setSelectedMessage(message);
  };

  const closeMessage = () => {
    setSelectedMessage(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-4">
            📧 Временные Email
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Создавайте одноразовые email адреса для регистрации на сайтах, тестирования и защиты вашей конфиденциальности
          </p>
        </div>

        {!inbox ? (
          /* Create Inbox Form */
          <div className="max-w-md mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
              <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
                Создать временный email
              </h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Имя пользователя (необязательно)
                  </label>
                  <input
                    type="text"
                    value={customName}
                    onChange={(e) => setCustomName(e.target.value)}
                    placeholder="my-temp-email"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Если не указано, будет сгенерировано автоматически
                  </p>
                </div>

                <button
                  onClick={createInbox}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 transform hover:scale-105"
                >
                  {loading ? (
                    <span className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Создаем...
                    </span>
                  ) : (
                    '✨ Создать Email'
                  )}
                </button>
              </div>
            </div>
          </div>
        ) : (
          /* Inbox Dashboard */
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Email Info Card */}
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-100">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-semibold text-gray-800">Ваш временный email</h2>
                <button
                  onClick={() => {
                    setInbox(null);
                    setMessages([]);
                    setAutoRefresh(false);
                  }}
                  className="text-gray-500 hover:text-red-500 transition duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div className="flex items-center space-x-4 bg-gray-50 rounded-lg p-4">
                <div className="flex-1">
                  <p className="text-2xl font-mono font-bold text-blue-600 break-all">
                    {inbox.email}
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    Создан: {formatDate(inbox.created_at)}
                  </p>
                </div>
                
                <button
                  onClick={copyToClipboard}
                  className={`px-4 py-2 rounded-lg font-semibold transition duration-200 ${
                    copySuccess
                      ? 'bg-green-500 text-white'
                      : 'bg-blue-100 text-blue-600 hover:bg-blue-200'
                  }`}
                >
                  {copySuccess ? '✓ Скопировано!' : '📋 Копировать'}
                </button>
              </div>

              <div className="flex items-center justify-between mt-6">
                <div className="flex items-center space-x-4">
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={autoRefresh}
                      onChange={(e) => setAutoRefresh(e.target.checked)}
                      className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">Автообновление</span>
                  </label>
                </div>

                <button
                  onClick={fetchMessages}
                  className="bg-indigo-100 text-indigo-600 px-4 py-2 rounded-lg hover:bg-indigo-200 font-semibold transition duration-200"
                >
                  🔄 Обновить
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100">
              <div className="p-6 border-b border-gray-100">
                <h3 className="text-xl font-semibold text-gray-800">
                  Входящие сообщения ({messages.length})
                </h3>
              </div>

              {messages.length === 0 ? (
                <div className="p-12 text-center">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2 2v-5m16 0h-2M4 13h2m8-6v.01M8 15h8" />
                    </svg>
                  </div>
                  <p className="text-gray-500 text-lg mb-2">Сообщений пока нет</p>
                  <p className="text-gray-400">Отправьте письмо на ваш временный адрес, и оно появится здесь</p>
                </div>
              ) : (
                <div className="divide-y divide-gray-100">
                  {messages.map((message, index) => (
                    <div
                      key={message.id}
                      onClick={() => openMessage(message)}
                      className="p-6 hover:bg-gray-50 cursor-pointer transition duration-200"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                              #{index + 1}
                            </span>
                            <p className="text-sm text-gray-600 truncate">
                              От: {message.from_address}
                            </p>
                          </div>
                          <h4 className="text-lg font-semibold text-gray-900 mb-2 truncate">
                            {message.subject || 'Без темы'}
                          </h4>
                          <p className="text-gray-600 line-clamp-2">
                            {message.body.substring(0, 150)}...
                          </p>
                        </div>
                        <div className="ml-4 text-right">
                          <p className="text-sm text-gray-500">
                            {formatDate(message.received_at)}
                          </p>
                          <div className="mt-2">
                            <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                            </svg>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Message Modal */}
        {selectedMessage && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
              <div className="p-6 border-b border-gray-100 flex items-center justify-between">
                <h3 className="text-xl font-semibold text-gray-800">
                  {selectedMessage.subject || 'Без темы'}
                </h3>
                <button
                  onClick={closeMessage}
                  className="text-gray-500 hover:text-red-500 transition duration-200"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="p-6 border-b border-gray-100">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-semibold text-gray-700">От:</span>
                    <span className="ml-2 text-gray-600">{selectedMessage.from_address}</span>
                  </div>
                  <div>
                    <span className="font-semibold text-gray-700">Кому:</span>
                    <span className="ml-2 text-gray-600">{selectedMessage.to_address}</span>
                  </div>
                  <div className="md:col-span-2">
                    <span className="font-semibold text-gray-700">Дата:</span>
                    <span className="ml-2 text-gray-600">{formatDate(selectedMessage.received_at)}</span>
                  </div>
                </div>
              </div>

              <div className="p-6 overflow-y-auto max-h-[60vh]">
                <div className="prose prose-sm max-w-none">
                  {selectedMessage.html_body && selectedMessage.html_body.length > 0 ? (
                    <div dangerouslySetInnerHTML={{ __html: selectedMessage.html_body[0] }} />
                  ) : (
                    <pre className="whitespace-pre-wrap font-sans text-gray-700 leading-relaxed">
                      {selectedMessage.body}
                    </pre>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500">
          <p>🔒 Ваши данные в безопасности. Временные email адреса автоматически удаляются.</p>
        </div>
      </div>
    </div>
  );
}

export default App;