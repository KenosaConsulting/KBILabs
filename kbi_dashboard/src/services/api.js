const API_BASE_URL = 'http://3.143.232.123:9999/api/v1';

class APIService {
  async getCompanies(page = 1, limit = 20, search = '') {
    try {
      const skip = (page - 1) * limit;
      const url = `${API_BASE_URL}/companies?skip=${skip}&limit=${limit}${search ? `&search=${search}` : ''}`;
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors'
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching companies:', error);
      throw error;
    }
  }

  async getCompanyDetails(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/companies/${id}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching company details:', error);
      throw error;
    }
  }

  async getAnalytics() {
    try {
      const response = await fetch(`${API_BASE_URL}/analytics`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching analytics:', error);
      throw error;
    }
  }

  async getKPIs() {
    try {
      const response = await fetch(`${API_BASE_URL}/kpis`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching KPIs:', error);
      return {
        totalCompanies: 0,
        totalRevenue: 0,
        avgKBIScore: 0,
        activeDeals: 0
      };
    }
  }

  async getMarketIntelligence() {
    try {
      const response = await fetch(`${API_BASE_URL}/market-intelligence`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Error fetching market intelligence:', error);
      // Return null to trigger mock data
      return null;
    }
  }
}

export default new APIService();
