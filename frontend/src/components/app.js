// Main Application Logic
(function() {
    const api = new APIService();
    let stats = {
        totalAds:  0,
        totalTime: 0,
        successCount: 0,
        errorCount: 0,
    };

    // Initialize app
    document.addEventListener('DOMContentLoaded', async () => {
        await checkSystemStatus();
        setupEventListeners();
        startMetricsPolling();
    });

    // Check system status
    async function checkSystemStatus() {
        try {
            const health = await api.getHealth();
            updateStatusIndicator(true, health);
            showToast('System online and ready! ', 'success');
        } catch (error) {
            updateStatusIndicator(false);
            showToast('Unable to connect to API', 'error');
        }
    }

    // Update status indicator
    function updateStatusIndicator(online, health = null) {
        const dot = document.getElementById('status-dot');
        const text = document.getElementById('status-text');
        const details = document.getElementById('status-details');

        dot.className = 'status-dot ' + (online ? 'online' : 'offline');
        text.textContent = online ? 'System Online' : 'System Offline';

        if (online && health) {
            details. innerHTML = `
                <span>Model: ${health.model_name}</span>
                <span>Device: ${health.device}</span>
                <span>Uptime: ${formatUptime(health.uptime_seconds)}</span>
            `;
        }
    }

    // Setup event listeners
    function setupEventListeners() {
        // Form submission
        document.getElementById('ad-form').addEventListener('submit', handleGenerate);

        // Character count
        document.getElementById('description').addEventListener('input', updateCharCount);

        // Example button
        document.getElementById('example-btn').addEventListener('click', loadExample);

        // Copy button
        document.getElementById('copy-btn').addEventListener('click', copyToClipboard);

        // CSV upload
        document.getElementById('csv-upload').addEventListener('change', handleCSVUpload);

        // Download template
        document.getElementById('download-template').addEventListener('click', downloadTemplate);
    }

    // Handle ad generation
    async function handleGenerate(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const productData = {
            product_name: formData.get('product_name'),
            category: formData.get('category'),
            description: formData.get('description'),
            price: parseFloat(formData.get('price')),
        };

        showLoading(true);
        const btn = document.getElementById('generate-btn');
        btn.disabled = true;
        btn.innerHTML = `
            <svg class="btn-icon spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
            </svg>
            Generating...
        `;

        try {
            const result = await api.generateAd(productData);
            displayResult(result);
            updateStats(result);
            showToast('Ad generated successfully!', 'success');
        } catch (error) {
            showToast(error.message, 'error');
            stats.errorCount++;
        } finally {
            showLoading(false);
            btn.disabled = false;
            btn.innerHTML = `
                <svg class="btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                </svg>
                Generate Ad
            `;
        }
    }

    // Display result
    function displayResult(result) {
        const container = document.getElementById('output-container');
        const metrics = document.getElementById('output-metrics');
        const copyBtn = document.getElementById('copy-btn');

        container.innerHTML = `<p class="output-text">${result.generated_ad}</p>`;
        
        document.getElementById('gen-time').textContent = `${(result.generation_time_ms / 1000).toFixed(2)}s`;
        document.getElementById('ad-length').textContent = `${result.generated_ad.length} chars`;
        document.getElementById('word-count').textContent = `${result.generated_ad.split(' ').length} words`;

        metrics.style.display = 'grid';
        copyBtn.style.display = 'block';
        copyBtn.dataset.text = result.generated_ad;
    }

    // Update statistics
    function updateStats(result) {
        stats.totalAds++;
        stats.totalTime += result.generation_time_ms;
        stats.successCount++;

        document.getElementById('total-ads').textContent = stats.totalAds;
        document.getElementById('avg-time').textContent = `${(stats.totalTime / stats. totalAds / 1000).toFixed(2)}s`;
        
        const successRate = (stats.successCount / (stats.successCount + stats.errorCount) * 100).toFixed(1);
        document.getElementById('success-rate').textContent = `${successRate}%`;
    }

    // Character count
    function updateCharCount(e) {
        const count = e.target.value.length;
        const max = e.target.maxLength;
        document.getElementById('char-count').textContent = `${count} / ${max}`;
    }

    // Load example
    function loadExample() {
        document.getElementById('product-name').value = 'Wireless Noise-Cancelling Headphones Pro';
        document.getElementById('category').value = 'Electronics';
        document.getElementById('description').value = 'Premium wireless headphones with industry-leading noise cancellation, 30-hour battery life, and exceptional sound quality. Perfect for music lovers and professionals. ';
        document.getElementById('price').value = '299.99';
        updateCharCount({ target: document.getElementById('description') });
    }

    // Copy to clipboard
    async function copyToClipboard(e) {
        const text = e.currentTarget.dataset.text;
        try {
            await navigator.clipboard. writeText(text);
            showToast('Copied to clipboard!', 'success');
        } catch (error) {
            showToast('Failed to copy', 'error');
        }
    }

    // Handle CSV upload
    async function handleCSVUpload(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = async (event) => {
            try {
                const csv = event.target.result;
                const products = parseCSV(csv);
                
                showLoading(true);
                const result = await api.generateBatch(products);
                displayBatchResults(result);
                showToast(`Generated ${result.successful} ads! `, 'success');
            } catch (error) {
                showToast(error.message, 'error');
            } finally {
                showLoading(false);
            }
        };
        reader.readAsText(file);
    }

    // Parse CSV
    function parseCSV(csv) {
        const lines = csv.trim().split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        
        return lines.slice(1).map(line => {
            const values = line.split(',').map(v => v.trim());
            const product = {};
            headers.forEach((header, index) => {
                if (header === 'price') {
                    product[header] = parseFloat(values[index]);
                } else {
                    product[header] = values[index];
                }
            });
            return product;
        });
    }

    // Display batch results
    function displayBatchResults(result) {
        const container = document.getElementById('batch-results');
        container.style.display = 'block';
        
        container.innerHTML = `
            <h3>Batch Results</h3>
            <p>Total:  ${result.total_products} | Success: ${result.successful} | Failed: ${result.failed}</p>
            <div class="batch-ads">
                ${result.results.map((r, i) => `
                    <div class="batch-ad">
                        <strong>${i + 1}.  ${r.product_name}</strong>
                        <p>${r.generated_ad}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // Download template
    function downloadTemplate() {
        const csv = 'product_name,category,description,price\n' +
                    'Example Product,Electronics,This is a sample product description,99.99';
        
        const blob = new Blob([csv], { type: 'text/csv' });
        const url = URL. createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'batch_template.csv';
        a.click();
        URL.revokeObjectURL(url);
    }

    // Start metrics polling
    function startMetricsPolling() {
        setInterval(async () => {
            try {
                const metricsText = await api.getMetrics();
                parseAndDisplayMetrics(metricsText);
            } catch (error) {
                console.error('Failed to fetch metrics:', error);
            }
        }, 10000); // Every 10 seconds
    }

    // Parse and display Prometheus metrics
    function parseAndDisplayMetrics(metricsText) {
        const lines = metricsText.split('\n');
        
        // Parse metrics (simplified)
        lines.forEach(line => {
            if (line.includes('ad_generator_requests_total')) {
                // Extract request count
            } else if (line.includes('ad_generator_active_requests')) {
                const match = line.match(/(\d+\. ?\d*)/);
                if (match) {
                    document.getElementById('active-requests').textContent = match[1];
                }
            } else if (line.includes('ad_generator_uptime_seconds')) {
                const match = line.match(/(\d+\.?\d*)/);
                if (match) {
                    document.getElementById('uptime').textContent = formatUptime(parseFloat(match[1]));
                }
            }
        });
    }

    // Utility functions
    function showLoading(show) {
        document.getElementById('loading').style.display = show ? 'flex' : 'none';
    }

    function showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    function formatUptime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}m`;
    }
})();