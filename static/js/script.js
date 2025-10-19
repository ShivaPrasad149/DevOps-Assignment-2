// Common JavaScript functions used across all pages
// Add any shared JavaScript functionality here

console.log('BusBooker Pro - JavaScript loaded successfully');

// Common utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function showNotification(message, type = 'info') {
    // Implementation for showing notifications
    console.log(`${type.toUpperCase()}: ${message}`);
}

// API integration functions
async function makeAPIRequest(endpoint, data = {}) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        return { success: false, message: 'Network error occurred' };
    }
}