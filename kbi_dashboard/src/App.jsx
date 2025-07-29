import React, { useState } from 'react';
import { SWRConfig } from 'swr';
import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Components (we'll create these next)
// import Dashboard from './pages/Dashboard';
// import Companies from './pages/Companies';

// Styles
import './index.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 2,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

// SWR Configuration
const swrConfig = {
  revalidateOnFocus: false,
  shouldRetryOnError: true,
  errorRetryCount: 2,
  errorRetryInterval: 5000,
};

function App() {
  const [currentView, setCurrentView] = useState('dashboard');

  return (
    <QueryClientProvider client={queryClient}>
      <SWRConfig value={swrConfig}>
        <div className="min-h-screen bg-gray-50">
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#1f2937',
                color: '#fff',
              },
              success: {
                iconTheme: {
                  primary: '#10b981',
                  secondary: '#fff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#fff',
                },
              },
            }}
          />
          
          {/* Navigation */}
          <nav className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex">
                  <div className="flex-shrink-0 flex items-center">
                    <h1 className="text-xl font-bold text-primary-600">KBI Labs</h1>
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <button
                      onClick={() => setCurrentView('dashboard')}
                      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                        currentView === 'dashboard'
                          ? 'border-primary-500 text-gray-900'
                          : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                      }`}
                    >
                      Dashboard
                    </button>
                    <button
                      onClick={() => setCurrentView('companies')}
                      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                        currentView === 'companies'
                          ? 'border-primary-500 text-gray-900'
                          : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                      }`}
                    >
                      Companies
                    </button>
                    <button
                      onClick={() => setCurrentView('analytics')}
                      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                        currentView === 'analytics'
                          ? 'border-primary-500 text-gray-900'
                          : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                      }`}
                    >
                      Analytics
                    </button>
                    <button
                      onClick={() => setCurrentView('market')}
                      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                        currentView === 'market'
                          ? 'border-primary-500 text-gray-900'
                          : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                      }`}
                    >
                      Market Intelligence
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </nav>

          {/* Main Content */}
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            {currentView === 'dashboard' && (
              <div className="px-4 py-6 sm:px-0">
                <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
                {/* Dashboard component will go here */}
                <div className="bg-white rounded-lg shadow p-6">
                  <p>Dashboard content coming soon...</p>
                </div>
              </div>
            )}
            
            {currentView === 'companies' && (
              <div className="px-4 py-6 sm:px-0">
                <h2 className="text-2xl font-bold mb-4">Companies</h2>
                {/* Companies component will go here */}
                <div className="bg-white rounded-lg shadow p-6">
                  <p>Companies list coming soon...</p>
                </div>
              </div>
            )}
            
            {currentView === 'analytics' && (
              <div className="px-4 py-6 sm:px-0">
                <h2 className="text-2xl font-bold mb-4">Analytics</h2>
                {/* Analytics component will go here */}
                <div className="bg-white rounded-lg shadow p-6">
                  <p>Analytics coming soon...</p>
                </div>
              </div>
            )}
            
            {currentView === 'market' && (
              <div className="px-4 py-6 sm:px-0">
                <h2 className="text-2xl font-bold mb-4">Market Intelligence</h2>
                {/* Market Intelligence component will go here */}
                <div className="bg-white rounded-lg shadow p-6">
                  <p>Market Intelligence coming soon...</p>
                </div>
              </div>
            )}
          </main>
        </div>
      </SWRConfig>
    </QueryClientProvider>
  );
}

export default App;
