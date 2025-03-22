import blockedSites from './rules.js';

document.addEventListener('DOMContentLoaded', async () => {
    const sitesList = document.getElementById('sitesList');
    const locationInfo = document.getElementById('locationInfo');
    const antivirusAlert = document.getElementById('antivirusAlert');
    const toggleButton = document.getElementById('antivirusToggle');
    const blockedSitesHeader = document.querySelector('.blocked-sites .section-header');
    const blockedSitesContent = document.querySelector('.blocked-sites-content');

    // Check if elements exist before proceeding
    if (!sitesList || !locationInfo || !antivirusAlert || !toggleButton || !blockedSitesHeader || !blockedSitesContent) {
        console.error('Required elements not found');
        return;
    }

    // Initialize audio
    const blockSound = new Audio(chrome.runtime.getURL('BlockSound.mp3'));
    blockSound.loop = true;
    blockSound.play().catch(error => console.log('Audio playback failed:', error));

    // Load blocked sites from rules.js
    function loadBlockedSites() {
        sitesList.innerHTML = '';
        blockedSites.forEach(site => {
            const li = document.createElement('li');
            li.textContent = site;
            li.addEventListener('click', () => {
                const siteInfo = li.querySelector('.site-info');
                if (siteInfo) {
                    siteInfo.classList.toggle('active');
                } else {
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'site-info';
                    infoDiv.innerHTML = `
                        <div>Threat detected: Remote Access Tool (RAT)</div>
                        <div>Risk Level: High</div>
                    `;
                    li.appendChild(infoDiv);
                }
            });
            sitesList.appendChild(li);
        });
    }

    // Load system information
    async function loadSystemInfo() {
        try {
            const response = await fetch('https://api.ipify.org?format=json');
            const ipData = await response.json();
            const locationResponse = await fetch(`https://ip-api.com/json/${ipData.ip}`);
            const locationData = await locationResponse.json();

            locationInfo.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 10px;">⚠️ Access Blocked</div>
                <div>
                    IP: ${ipData.ip}<br>
                    Location: ${locationData.city}, ${locationData.country}<br>
                    ISP: ${locationData.isp}<br>
                    Time: ${new Date().toLocaleString()}
                </div>
            `;
            locationInfo.classList.remove('loading');
        } catch (error) {
            locationInfo.innerHTML = `
                <div style="font-weight: bold; margin-bottom: 10px;">⚠️ Access Blocked</div>
                <div>Unable to load system information</div>
            `;
            locationInfo.classList.remove('loading');
        }
    }

    // Toggle antivirus
    toggleButton.addEventListener('click', () => {
        const antivirusEnabled = antivirusAlert.style.display === 'none';
        antivirusAlert.style.display = antivirusEnabled ? 'block' : 'none';
        toggleButton.textContent = antivirusEnabled ? 'Disable Antivirus' : 'Enable Antivirus';
        toggleButton.style.backgroundColor = antivirusEnabled ? '#ff0000' : '#00ff00';
    });

    // Toggle blocked sites dropdown
    blockedSitesHeader.addEventListener('click', () => {
        blockedSitesContent.classList.toggle('active');
    });

    // Initial load
    loadBlockedSites();
    loadSystemInfo();
});