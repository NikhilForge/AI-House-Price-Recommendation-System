// ================================
// GLOBAL VARIABLES
// ================================

let featuresData = [];
let featureInfo = {};

// ================================
// INITIALIZATION
// ================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Application initialized');
    loadFeatures();
    setupEventListeners();
});

// ================================
// LOAD FEATURES FROM API
// ================================

async function loadFeatures() {
    try {
        const response = await fetch('/features');
        
        if (!response.ok) {
            throw new Error('Failed to load features');
        }
        
        const data = await response.json();
        featuresData = data.features;
        featureInfo = data.feature_info;
        
        console.log(`✅ Loaded ${featuresData.length} features`);
        
        // Update stats
        updateStats(data);
        
        // Generate form
        generateForm();
        
    } catch (error) {
        console.error('❌ Error loading features:', error);
        showError('Failed to load features. Please refresh the page.');
    }
}

// ================================
// GENERATE DYNAMIC FORM
// ================================

function generateForm() {
    const container = document.getElementById('featuresContainer');
    container.innerHTML = ''; // Clear loading message
    
    if (featuresData.length === 0) {
        container.innerHTML = '<p class="error">No features available</p>';
        return;
    }
    
    // Create form groups for each feature
    featuresData.forEach((feature, index) => {
        const formGroup = createFormGroup(feature, index);
        container.appendChild(formGroup);
    });
    
    console.log(`✅ Generated form with ${featuresData.length} fields`);
}

// ================================
// CREATE FORM GROUP (ENHANCED WITH DROPDOWN SUPPORT)
// ================================

function createFormGroup(featureName, index) {
    const formGroup = document.createElement('div');
    formGroup.className = 'form-group';
    formGroup.style.animationDelay = `${index * 0.03}s`;
    
    // Get feature metadata
    const metadata = featureInfo[featureName] || {
        type: 'number',
        min: 0,
        max: 100000,
        step: 1,
        default: 0,
        description: 'Numeric value'
    };
    
    // Create label
    const label = document.createElement('label');
    label.className = 'form-label';
    label.htmlFor = `feature_${featureName}`;
    
    // Add icon if available
    const icon = metadata.icon || '';
    const labelText = metadata.label || formatFeatureName(featureName);
    
    label.innerHTML = `
        <span>${icon} ${labelText}</span>
        <span style="font-size: 0.75rem; color: #a0aec0;">${metadata.description}</span>
    `;
    
    // Create input element (either select dropdown or number input)
    let inputElement;
    
    if (metadata.type === 'select' && metadata.options) {
        // CREATE DROPDOWN SELECT
        inputElement = document.createElement('select');
        inputElement.id = `feature_${featureName}`;
        inputElement.name = featureName;
        inputElement.className = 'form-input';
        inputElement.required = true;
        
        // Add options
        metadata.options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option.value;
            optionElement.textContent = option.label;
            
            // Set default selected
            if (option.value == metadata.default) {
                optionElement.selected = true;
            }
            
            inputElement.appendChild(optionElement);
        });
        
    } else {
        // CREATE NUMBER INPUT (DEFAULT)
        inputElement = document.createElement('input');
        inputElement.type = metadata.type || 'number';
        inputElement.id = `feature_${featureName}`;
        inputElement.name = featureName;
        inputElement.className = 'form-input';
        inputElement.required = true;
        inputElement.value = metadata.default;
        
        if (metadata.type === 'number' || !metadata.type) {
            inputElement.min = metadata.min;
            inputElement.max = metadata.max;
            inputElement.step = metadata.step;
            inputElement.placeholder = `Enter ${labelText.toLowerCase()}`;
        }
    }
    
    formGroup.appendChild(label);
    formGroup.appendChild(inputElement);
    
    return formGroup;
}

// ================================
// FORMAT FEATURE NAME
// ================================

function formatFeatureName(name) {
    // Convert camelCase or PascalCase to readable format
    return name
        .replace(/([A-Z])/g, ' $1')
        .replace(/([0-9]+)/g, ' $1')
        .trim()
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// ================================
// UPDATE STATS
// ================================

function updateStats(data) {
    document.getElementById('featuresCount').textContent = data.total_features;
}

async function loadModelInfo() {
    try {
        const response = await fetch('/model-info');
        const data = await response.json();
        document.getElementById('modelType').textContent = data.model_type;
    } catch (error) {
        document.getElementById('modelType').textContent = 'ML Model';
    }
}

// Load model info after features
setTimeout(loadModelInfo, 500);

// ================================
// EVENT LISTENERS
// ================================

function setupEventListeners() {
    const form = document.getElementById('predictionForm');
    const resetButton = document.getElementById('resetButton');
    const retryButton = document.getElementById('retryButton');
    
    form.addEventListener('submit', handleFormSubmit);
    resetButton.addEventListener('click', resetForm);
    retryButton.addEventListener('click', hideError);
}

// ================================
// FORM SUBMISSION
// ================================

async function handleFormSubmit(event) {
    event.preventDefault();
    
    console.log('📊 Form submitted');
    
    // Show loading overlay
    showLoading();
    
    // Hide previous results/errors
    hideResult();
    hideError();
    
    // Collect form data
    const formData = collectFormData();
    
    console.log('📋 Collected form data:', formData);
    
    try {
        // Make prediction request
        const prediction = await makePrediction(formData);
        
        // Hide loading
        hideLoading();
        
        // Show result
        showResult(prediction);
        
    } catch (error) {
        console.error('❌ Prediction error:', error);
        hideLoading();
        
        // Extract readable error message
        const errorMessage = extractErrorMessage(error);
        showError(errorMessage);
    }
}

// ================================
// EXTRACT ERROR MESSAGE (FIX FOR [object Object])
// ================================

function extractErrorMessage(error) {
    // If error is a string, return it
    if (typeof error === 'string') {
        return error;
    }
    
    // If error has a message property that's a string
    if (error && typeof error.message === 'string') {
        return error.message;
    }
    
    // If error is an object, try to stringify it nicely
    if (error && typeof error === 'object') {
        // Check for common error formats
        if (error.detail) {
            if (typeof error.detail === 'string') {
                return error.detail;
            }
            // If detail is an array (FastAPI validation errors)
            if (Array.isArray(error.detail)) {
                // Extract unique error messages
                const uniqueMessages = [...new Set(
                    error.detail.map(e => e.msg || JSON.stringify(e))
                )];
                return uniqueMessages.join('; ');
            }
        }
        
        // Try to extract any meaningful message
        if (error.msg) return error.msg;
        if (error.error) return error.error;
        
        // Last resort: stringify the error
        try {
            return JSON.stringify(error);
        } catch (e) {
            return 'An unknown error occurred';
        }
    }
    
    // Default fallback
    return 'Failed to make prediction. Please try again.';
}

// ================================
// COLLECT FORM DATA (FIXED!)
// ================================

function collectFormData() {
    const formData = {};
    
    featuresData.forEach(feature => {
        const input = document.getElementById(`feature_${feature}`);
        if (input) {
            const value = input.value;
            
            // Smart conversion: try to parse as number, keep as string if it fails
            const numValue = parseFloat(value);
            
            // If it's a valid number (including 0), use the number
            // Otherwise keep the string (for location_type, basement_finish, etc.)
            if (!isNaN(numValue) && value !== '') {
                formData[feature] = numValue;
            } else {
                formData[feature] = value;
            }
        }
    });
    
    console.log('📝 Form data collected:', Object.keys(formData).length, 'features');
    console.log('🔍 Sample data:', Object.entries(formData).slice(0, 3));
    
    return formData;
}

// ================================
// MAKE PREDICTION
// ================================

async function makePrediction(features) {
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            features: features
        })
    });
    
    // Parse response
    const data = await response.json();
    
    // Check if response was not OK
    if (!response.ok) {
        // Throw the parsed data (which might be an error object)
        throw data;
    }
    
    console.log('✅ Prediction received:', data);
    return data;
}

// ================================
// CALCULATE PRICE CATEGORY
// ================================

function getPriceCategory(price) {
    if (price < 150000) {
        return {
            category: 'Low',
            className: 'category-low',
            icon: '🔵'
        };
    } else if (price <= 300000) {
        return {
            category: 'Medium',
            className: 'category-medium',
            icon: '🟡'
        };
    } else {
        return {
            category: 'High',
            className: 'category-high',
            icon: '🟢'
        };
    }
}

// ================================
// SHOW/HIDE LOADING
// ================================

function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('hidden');
    
    // Disable submit button
    const button = document.getElementById('predictButton');
    button.disabled = true;
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.add('hidden');
    
    // Enable submit button
    const button = document.getElementById('predictButton');
    button.disabled = false;
}

// ================================
// SHOW/HIDE RESULT
// ================================

function showResult(prediction) {
    const container = document.getElementById('resultContainer');
    const priceElement = document.getElementById('predictedPrice');
    const modelElement = document.getElementById('modelName');
    const confidenceElement = document.getElementById('confidence');
    
    // ---------- Original: price + model + confidence ----------
    priceElement.textContent = prediction.formatted_price;
    modelElement.textContent = prediction.model_name;
    confidenceElement.textContent = prediction.confidence;
    
    // ---------- Original: price category badge ----------
    const priceValue = prediction.predicted_price;
    const categoryInfo = getPriceCategory(priceValue);
    
    let categoryElement = document.getElementById('priceCategory');
    if (!categoryElement) {
        categoryElement = document.createElement('div');
        categoryElement.id = 'priceCategory';
        categoryElement.className = 'price-category';
        const priceDisplay = document.getElementById('predictedPrice');
        priceDisplay.parentNode.insertBefore(categoryElement, priceDisplay.nextSibling);
    }
    categoryElement.innerHTML = `
        <span class="category-badge ${categoryInfo.className}">
            ${categoryInfo.icon} ${categoryInfo.category} Range
        </span>
    `;
    categoryElement.style.display = 'block';
    
    // ---------- Original: location impact ----------
    if (prediction.location_impact) {
        const locationImpactItem = document.getElementById('locationImpactItem');
        const locationElement = document.getElementById('locationImpact');
        if (locationImpactItem && locationElement) {
            locationElement.textContent = prediction.location_impact;
            locationImpactItem.style.display = 'flex';
        }
    }
    
    // ======================================================
    // NEW: POPULATE RECOMMENDATION PANEL
    // ======================================================

    // --- Price Range ---
    document.getElementById('rangeLower').textContent    = prediction.range_lower_fmt;
    document.getElementById('rangeUpper').textContent    = prediction.range_upper_fmt;
    document.getElementById('rangeBarMin').textContent   = prediction.range_lower_fmt;
    document.getElementById('rangeBarMax').textContent   = prediction.range_upper_fmt;

    // Animate range bar dot: position predicted price between lower & upper
    const displayMin = prediction.range_lower * 0.95;
    const displayMax = prediction.range_upper * 1.05;
    const pct = Math.min(100, Math.max(0,
        ((prediction.predicted_price - displayMin) / (displayMax - displayMin)) * 100
    ));
    document.getElementById('rangeBarDot').style.left = `${pct}%`;

    // --- Market Insight ---
    const insightBadge = document.getElementById('insightBadge');
    insightBadge.className = `insight-badge insight-${prediction.market_color}`;
    document.getElementById('insightIcon').textContent = prediction.market_icon;
    document.getElementById('insightText').textContent = prediction.market_insight;

    const insightDescriptions = {
        budget:  'This property falls in the affordable / budget segment of the market.',
        fair:    'This property is competitively priced within the mid-range market.',
        premium: 'This property sits in the premium / luxury segment of the market.'
    };
    document.getElementById('insightDesc').textContent =
        insightDescriptions[prediction.market_color] || '';

    // --- Suggestion ---
    const suggBox = document.getElementById('suggestionHighlight');
    suggBox.className = `suggestion-highlight suggestion-${prediction.suggestion_type}`;
    document.getElementById('suggestionIcon').textContent = prediction.suggestion_icon;
    document.getElementById('suggestionText').textContent = prediction.suggestion;

    // --- Tips list ---
    const tipsList = document.getElementById('tipsList');
    tipsList.innerHTML = '';
    prediction.tips.forEach((tip, i) => {
        const li = document.createElement('li');
        li.className = 'tip-item';
        li.style.animationDelay = `${0.1 + i * 0.1}s`;
        li.textContent = tip;
        tipsList.appendChild(li);
    });

    // ======================================================

    // Show container with animation
    container.classList.remove('hidden');
    
    // Scroll to result
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
    
    console.log(`✅ Result displayed - Category: ${categoryInfo.category}`);
}

function hideResult() {
    const container = document.getElementById('resultContainer');
    container.classList.add('hidden');
    
    // Hide category if it exists
    const categoryElement = document.getElementById('priceCategory');
    if (categoryElement) {
        categoryElement.style.display = 'none';
    }

    // Hide location impact
    const locationImpactItem = document.getElementById('locationImpactItem');
    if (locationImpactItem) {
        locationImpactItem.style.display = 'none';
    }
}

// ================================
// SHOW/HIDE ERROR
// ================================

function showError(message) {
    const container = document.getElementById('errorContainer');
    const messageElement = document.getElementById('errorMessage');
    
    // Ensure message is a string
    const displayMessage = typeof message === 'string' ? message : 'An error occurred. Please try again.';
    
    messageElement.textContent = displayMessage;
    container.classList.remove('hidden');
    
    // Scroll to error
    setTimeout(() => {
        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
    
    console.log('⚠️ Error displayed:', displayMessage);
}

function hideError() {
    const container = document.getElementById('errorContainer');
    container.classList.add('hidden');
}

// ================================
// RESET FORM
// ================================

function resetForm() {
    console.log('🔄 Resetting form');
    
    // Hide result and error
    hideResult();
    hideError();
    
    // Reset form fields to defaults
    featuresData.forEach(feature => {
        const input = document.getElementById(`feature_${feature}`);
        if (input) {
            const metadata = featureInfo[feature] || { default: 0 };
            input.value = metadata.default;
        }
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ================================
// UTILITY FUNCTIONS
// ================================

// Format number as currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Debounce function for input validation
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ================================
// INPUT VALIDATION
// ================================

// Add real-time validation to inputs
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => {
            if (input.type === 'number') {
                input.addEventListener('input', debounce(validateInput, 300));
            }
        });
    }, 1000);
});

function validateInput(event) {
    const input = event.target;
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    
    // Check if value is within range
    if (value < min || value > max) {
        input.style.borderColor = '#f5576c';
    } else {
        input.style.borderColor = '#e2e8f0';
    }
}

// ================================
// KEYBOARD SHORTCUTS
// ================================

document.addEventListener('keydown', (event) => {
    // Ctrl/Cmd + Enter to submit
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        const form = document.getElementById('predictionForm');
        form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }
    
    // Escape to reset
    if (event.key === 'Escape') {
        const resultContainer = document.getElementById('resultContainer');
        if (!resultContainer.classList.contains('hidden')) {
            resetForm();
        }
    }
});

// ================================
// CONSOLE GREETING
// ================================

console.log(`
%c🏠 House Price Predictor 
%cPowered by Machine Learning
%c
Built with FastAPI & Modern Web Tech
✅ High-Impact Features
✅ Price Category Display
✅ Price Range & Market Insight
✅ Smart Suggestions
✅ Smart Error Handling
✅ Proper Data Parsing
`, 
'font-size: 20px; font-weight: bold; color: #667eea;',
'font-size: 14px; color: #764ba2;',
'font-size: 12px; color: #718096;'
);