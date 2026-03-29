// API Service for Backend Communication
class APIService {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data. detail || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Health check
    async getHealth() {
        return this.request('/health');
    }

    // Generate single ad
    async generateAd(productData) {
        return this.request('/generate', {
            method: 'POST',
            body: JSON.stringify(productData),
        });
    }

    // Generate batch ads
    async generateBatch(products) {
        return this.request('/generate/batch', {
            method: 'POST',
            body: JSON.stringify({ products }),
        });
    }

    // Get metrics
    async getMetrics() {
        const response = await fetch(`${this.baseURL}/metrics`);
        return response.text();
    }
}

// Export for use in app.js
window.APIService = APIService;