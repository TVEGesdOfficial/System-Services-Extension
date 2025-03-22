document.addEventListener('DOMContentLoaded', function() {
    const blockerToggle = document.getElementById('blockerToggle');
    const antivirusToggle = document.getElementById('antivirusToggle');
    const statusMessage = document.querySelector('.status');
    const body = document.body;
    const sitesList = document.getElementById('sitesList');
    const locationInfo = document.getElementById('locationInfo');

    // Check if elements exist before proceeding
    if (!blockerToggle || !antivirusToggle || !statusMessage || !sitesList || !locationInfo) {
        console.error('Required elements not found');
        return;
    }

    // Update border color based on feature states
    function updateBorderColor() {
        if (!blockerToggle.checked || !antivirusToggle.checked) {
            body.style.border = '2px solid #ff0000';
        } else {
            body.style.border = '2px solid #00ff00';
        }
    }

    // Get current states
    chrome.storage.local.get(['blockerEnabled', 'antivirusEnabled'], function(result) {
        blockerToggle.checked = result.blockerEnabled !== undefined ? result.blockerEnabled : true;
        antivirusToggle.checked = result.antivirusEnabled !== undefined ? result.antivirusEnabled : true;
        statusMessage.textContent = 'Ready';
        updateBorderColor();
    });

    // Load blocked sites
    function loadBlockedSites() {
        // Example blocked sites
        const blockedSites = ['example.com', 'testsite.com'];
        sitesList.innerHTML = '';
        blockedSites.forEach(site => {
            const li = document.createElement('li');
            li.textContent = site;
            sitesList.appendChild(li);
        });
    }

    // Load system information
    function loadSystemInfo() {
        // Example system information
        locationInfo.innerHTML = `
            <div>IP: 192.168.1.1</div>
            <div>Location: City, Country</div>
            <div>ISP: Example ISP</div>
        `;
    }

    // Blocker toggle
    blockerToggle.addEventListener('change', function() {
        chrome.runtime.sendMessage({ 
            action: 'toggleBlocker', 
            enabled: this.checked 
        });
        updateBorderColor();
    });

    // Antivirus toggle
    antivirusToggle.addEventListener('change', function() {
        chrome.runtime.sendMessage({
            action: 'toggleAntivirus',
            enabled: this.checked
        });
        updateBorderColor();
    });

    // Initial load
    loadBlockedSites();
    loadSystemInfo();
});