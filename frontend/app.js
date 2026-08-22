// Configuration: Point this to your FastAPI backend
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Global variables
let hazardMap = null;
let categoryChartInstance = null;
let severityChartInstance = null;

// Heatmap Variables
let markerLayerGroup = L.layerGroup();
let heatLayer = null;
let isHeatmapActive = false;
let allMapData = []; // Saved for CSV Download

// ==========================================
// 1. NAVIGATION & SPA LOGIC
// ==========================================
function showSection(sectionId) {
    document.querySelectorAll('.content-section').forEach(sec => sec.style.display = 'none');
    document.querySelectorAll('.nav-links a').forEach(link => link.classList.remove('active'));
    
    document.getElementById(sectionId).style.display = 'block';
    event.target.classList.add('active');

    if (sectionId === 'map-section') initMap();
    else if (sectionId === 'analytics-section') loadAnalytics();
}

// ==========================================
// 2. REPORT SUBMISSION (Connecting to ML + Voice Alert)
// ==========================================
document.getElementById('hazardForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.innerText = "Analyzing Report...";
    submitBtn.disabled = true;

    const payload = {
        description: document.getElementById('description').value,
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value),
        image_url: null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/reports/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Failed to submit report");
        const data = await response.json();

        // UI Updates
        document.getElementById('predictionResult').style.display = 'block';
        document.getElementById('res-category').innerText = data.prediction.predicted_category;
        const confPercent = (data.prediction.confidence * 100).toFixed(1);
        document.getElementById('res-confidence').innerText = `${confPercent}%`;
        document.getElementById('res-severity').innerText = data.prediction.severity;

        // 🔊 NEW FEATURE: AI VOICE ALERT
        if (data.prediction.severity === 'CRITICAL' || data.prediction.severity === 'HIGH') {
            const speech = new SpeechSynthesisUtterance(`Alert! ${data.prediction.severity} severity marine hazard detected.`);
            speech.volume = 1; 
            speech.rate = 1;
            window.speechSynthesis.speak(speech);
        }

        document.getElementById('hazardForm').reset();
        document.getElementById('weatherInfo').style.display = 'none'; // hide weather
    } catch (error) {
        alert("Error submitting report. Is the FastAPI backend running?");
    } finally {
        submitBtn.innerText = "Submit Report & Run AI";
        submitBtn.disabled = false;
    }
});

// ==========================================
// 3. LEAFLET MAP + HEATMAP + LIVE WEATHER
// ==========================================
async function initMap() {
    if (hazardMap !== null) {
        hazardMap.invalidateSize();
        return;
    }

    hazardMap = L.map('hazardMap').setView([17.5, 73.0], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(hazardMap);

    // Click on Map Logic
    hazardMap.on('click', async function(e) {
        let lat = e.latlng.lat.toFixed(4);
        let lng = e.latlng.lng.toFixed(4);
        
        document.getElementById('latitude').value = lat;
        document.getElementById('longitude').value = lng;
        
        L.popup()
            .setLatLng(e.latlng)
            .setContent(`<div style="text-align:center;"><b>📍 Location Picked!</b><br><small>Lat: ${lat}, Lng: ${lng}</small></div>`)
            .openOn(hazardMap);

        // 🌤️ NEW FEATURE: FETCH LIVE WEATHER (Open-Meteo Free API)
        try {
            document.getElementById('weatherInfo').style.display = 'block';
            document.getElementById('weatherText').innerText = "Fetching weather...";
            
            const weatherRes = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lng}&current_weather=true`);
            const weatherData = await weatherRes.json();
            const temp = weatherData.current_weather.temperature;
            const wind = weatherData.current_weather.windspeed;
            
            document.getElementById('weatherText').innerText = `${temp}°C, Wind Speed: ${wind} km/h`;
        } catch(err) {
            document.getElementById('weatherText').innerText = "Weather unavailable.";
        }
    });

    // Fetch and Plot Data
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/map`);
        const markersData = await response.json();
        allMapData = markersData; // Save for CSV

        const heatData = [];
        markerLayerGroup.clearLayers();

        markersData.forEach(item => {
            let color = 'blue';
            let heatIntensity = 0.4;
            if (item.severity === 'CRITICAL') { color = '#EF476F'; heatIntensity = 1.0; }
            else if (item.severity === 'HIGH') { color = '#F77F00'; heatIntensity = 0.8; }
            else if (item.severity === 'MEDIUM') { color = '#FFD166'; heatIntensity = 0.6; }

            // Add to heat data array
            heatData.push([item.latitude, item.longitude, heatIntensity]);

            // Create dot marker
            const marker = L.circleMarker([item.latitude, item.longitude], {
                radius: 8, fillColor: color, color: '#fff', weight: 1, opacity: 1, fillOpacity: 0.8
            });
            marker.bindPopup(`<strong>${item.category}</strong><br>Severity: <b>${item.severity}</b><br>Date: ${item.date}`);
            marker.addTo(markerLayerGroup);
        });

        // Initialize heat layer (but don't add to map yet)
        heatLayer = L.heatLayer(heatData, {radius: 25, blur: 15, maxZoom: 8});
        
        // Add default marker layer
        markerLayerGroup.addTo(hazardMap);
    } catch (error) {
        console.error("Error loading map data:", error);
    }
}

// 🔥 HEATMAP TOGGLE LOGIC
document.getElementById('toggleHeatmapBtn').addEventListener('click', function() {
    if (!hazardMap) return;
    
    if (isHeatmapActive) {
        hazardMap.removeLayer(heatLayer);
        hazardMap.addLayer(markerLayerGroup);
        this.innerText = "🔥 Toggle Heatmap";
        this.style.backgroundColor = "#EF476F";
        isHeatmapActive = false;
    } else {
        hazardMap.removeLayer(markerLayerGroup);
        hazardMap.addLayer(heatLayer);
        this.innerText = "📍 Show Pins";
        this.style.backgroundColor = "#118AB2";
        isHeatmapActive = true;
    }
});

// ==========================================
// 4. CHART.JS ANALYTICS DASHBOARD
// ==========================================
async function loadAnalytics() {
    try {
        const summaryRes = await fetch(`${API_BASE_URL}/analytics/summary`);
        const summaryData = await summaryRes.json();
        
        document.getElementById('totalReports').innerText = summaryData.total_reports;
        document.getElementById('highRiskReports').innerText = summaryData.high_risk_hazards;

        const catRes = await fetch(`${API_BASE_URL}/analytics/categories`);
        const catData = await catRes.json();
        drawCategoryChart(catData);

        const sevRes = await fetch(`${API_BASE_URL}/analytics/severity`);
        const sevData = await sevRes.json();
        drawSeverityChart(sevData);

    } catch (error) {
        console.error("Error loading analytics:", error);
    }
}

// Chart rendering functions...
function drawCategoryChart(data) {
    if (categoryChartInstance) categoryChartInstance.destroy(); 
    const ctx = document.getElementById('categoryChart').getContext('2d');
    categoryChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.category),
            datasets: [{ data: data.map(d => d.count), backgroundColor: ['#0A2540', '#118AB2', '#06D6A0', '#FFD166', '#EF476F'] }]
        },
        options: { responsive: true }
    });
}

function drawSeverityChart(data) {
    if (severityChartInstance) severityChartInstance.destroy();
    const ctx = document.getElementById('severityChart').getContext('2d');
    severityChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.severity),
            datasets: [{ label: 'Number of Incidents', data: data.map(d => d.count), backgroundColor: '#118AB2' }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}

// ==========================================
// 5. GPS LOCATION & CSV EXPORT
// ==========================================
document.getElementById('getLocationBtn').addEventListener('click', function() {
    const msg = document.getElementById('locationMessage');
    msg.innerText = "Locating..."; msg.style.color = "orange";
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                document.getElementById('latitude').value = position.coords.latitude.toFixed(4);
                document.getElementById('longitude').value = position.coords.longitude.toFixed(4);
                msg.innerText = "✅ Location captured!"; msg.style.color = "green";
            },
            () => { msg.innerText = "❌ Location access denied."; msg.style.color = "red"; }
        );
    } else {
        msg.innerText = "Geolocation not supported.";
    }
});

// 📊 NEW FEATURE: EXPORT DATA TO CSV
document.getElementById('exportCsvBtn').addEventListener('click', function() {
    if (allMapData.length === 0) {
        alert("No data available to download.");
        return;
    }
    
    // Create CSV Header
    let csvContent = "data:text/csv;charset=utf-8,Category,Severity,Latitude,Longitude,Date\n";
    
    // Add Rows
    allMapData.forEach(row => {
        csvContent += `${row.category},${row.severity},${row.latitude},${row.longitude},${row.date}\n`;
    });
    
    // Create hidden link and download
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "ocean_hazard_data.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
});