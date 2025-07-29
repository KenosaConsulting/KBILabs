import React from 'react';
import { useCompanies } from '../hooks/useCompanies';
import { Activity, TrendingUp, Users, DollarSign, Brain, AlertCircle } from 'lucide-react';

const MetricCard = ({ title, value, change, icon: Icon, color }) => (
  <div className="bg-white rounded-lg shadow p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-semibold text-gray-900">{value}</p>
        {change && (
          <p className={`text-sm ${change > 0 ? 'text-green-600' : 'text-red-600'}`}>
            {change > 0 ? '+' : ''}{change}%
          </p>
        )}
      </div>
      <div className={`p-3 rounded-lg ${color}`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const { companies, totalCount, isLoading } = useCompanies({ limit: 5 });

  const metrics = [
    {
      title: 'Total Companies',
      value: totalCount || 0,
      icon: Users,
      color: 'bg-primary-500'
    },
    {
      title: 'Active KPIs',
      value: '2,847',
      change: 12.5,
      icon: Activity,
      color: 'bg-secondary-500'
    },
    {
      title: 'AI Insights',
      value: '156',
      change: 8.2,
      icon: Brain,
      color: 'bg-ai-500'
    },
    {
      title: 'Portfolio Value',
      value: '$45.2M',
      change: -2.4,
      icon: DollarSign,
      color: 'bg-green-500'
    }
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to KBI Labs Intelligence Platform</p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric, index) => (
          <MetricCard key={index} {...metric} />
        ))}
      </div>

      {/* Recent Companies */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Recent Companies</h2>
        </div>
        <div className="p-6">
          {companies.length > 0 ? (
            <div className="space-y-4">
              {companies.map((company) => (
                <div key={company.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors">
                  <div>
                    <h3 className="font-medium text-gray-900">{company.name}</h3>
                    <p className="text-sm text-gray-600">{company.industry}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">${company.revenue || 'N/A'}</p>
                    <p className="text-xs text-gray-600">Revenue</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <AlertCircle className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2 text-gray-600">No companies found</p>
              <button className="mt-4 btn-primary">
                Add Your First Company
              </button>
            </div>
          )}
        </div>
      </div>

      {/* AI Insights Preview */}
      <div className="bg-gradient-to-r from-ai-500 to-secondary-500 rounded-lg shadow p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">AI-Powered Insights</h2>
            <p className="mt-1 text-white/80">
              Get intelligent recommendations and predictions powered by advanced AI
            </p>
          </div>
          <Brain className="h-12 w-12 text-white/50" />
        </div>
        <button className="mt-4 bg-white text-ai-600 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors">
          Explore AI Features
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
