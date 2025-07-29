import axios from 'axios';
import config from '../config';

class APIService {
  constructor() {
    this.client = axios.create({
      baseURL: config.api.baseURL,
      timeout: config.api.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (request) => {
        const token = localStorage.getItem('kbi_auth_token');
        if (token) {
          request.headers.Authorization = `Bearer ${token}`;
        }
        return request;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor with retry logic
    this.client.interceptors.response.use(
      (response) => response.data,
      async (error) => {
        const originalRequest = error.config;

        // Retry logic
        if (error.response?.status >= 500 && !originalRequest._retry) {
          originalRequest._retry = true;
          originalRequest._retryCount = (originalRequest._retryCount || 0) + 1;

          if (originalRequest._retryCount <= config.api.retryAttempts) {
            await new Promise(resolve => 
              setTimeout(resolve, config.api.retryDelay * originalRequest._retryCount)
            );
            return this.client(originalRequest);
          }
        }

        // Handle 401 - Unauthorized
        if (error.response?.status === 401) {
          localStorage.removeItem('kbi_auth_token');
          window.location.href = '/login';
        }

        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async login(credentials) {
    const response = await this.client.post('/auth/login', credentials);
    if (response.token) {
      localStorage.setItem('kbi_auth_token', response.token);
    }
    return response;
  }

  async logout() {
    localStorage.removeItem('kbi_auth_token');
    return this.client.post('/auth/logout');
  }

  // Companies
  async getCompanies(params = {}) {
    return this.client.get('/companies', { params });
  }

  async getCompany(id) {
    return this.client.get(`/companies/${id}`);
  }

  async createCompany(data) {
    return this.client.post('/companies', data);
  }

  async updateCompany(id, data) {
    return this.client.put(`/companies/${id}`, data);
  }

  async deleteCompany(id) {
    return this.client.delete(`/companies/${id}`);
  }

  async enrichCompany(id) {
    return this.client.post(`/companies/${id}/enrich`);
  }

  // KPIs and Metrics
  async getKPIs(companyId, params = {}) {
    return this.client.get(`/companies/${companyId}/kpis`, { params });
  }

  async updateKPI(companyId, kpiId, data) {
    return this.client.put(`/companies/${companyId}/kpis/${kpiId}`, data);
  }

  async getFinancialData(companyId, params = {}) {
    return this.client.get(`/companies/${companyId}/financials`, { params });
  }

  // AI Insights
  async getAIInsights(companyId) {
    return this.client.get(`/ai/insights/${companyId}`);
  }

  async generateInsight(companyId, type) {
    return this.client.post(`/ai/insights/${companyId}/generate`, { type });
  }

  async queryAI(query) {
    return this.client.post('/ai/query', { query });
  }

  // Market Intelligence
  async getCompetitors(companyId) {
    return this.client.get(`/market-intelligence/competitors/${companyId}`);
  }

  async getMarketTrends(industry) {
    return this.client.get('/market-intelligence/trends', { 
      params: { industry } 
    });
  }

  async getIndustryBenchmarks(industry, metrics) {
    return this.client.get('/market-intelligence/benchmarks', {
      params: { industry, metrics }
    });
  }

  // Bulk Operations
  async bulkImport(file, type = 'companies') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    return this.client.post('/bulk/import', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }

  async bulkExport(params) {
    return this.client.post('/bulk/export', params, {
      responseType: 'blob'
    });
  }

  // Scenario Planning
  async createScenario(companyId, scenario) {
    return this.client.post(`/companies/${companyId}/scenarios`, scenario);
  }

  async getScenarios(companyId) {
    return this.client.get(`/companies/${companyId}/scenarios`);
  }

  async runScenario(companyId, scenarioId) {
    return this.client.post(`/companies/${companyId}/scenarios/${scenarioId}/run`);
  }

  // Search
  async search(query, filters = {}) {
    return this.client.get('/search', {
      params: { q: query, ...filters }
    });
  }

  // Analytics
  async getAnalytics(params) {
    return this.client.get('/analytics', { params });
  }

  async getPortfolioAnalytics(portfolioId) {
    return this.client.get(`/analytics/portfolio/${portfolioId}`);
  }

  // Cost Monitoring
  async getAPICosts(period = 'daily') {
    return this.client.get('/admin/api-costs', { params: { period } });
  }
}

export default new APIService();
