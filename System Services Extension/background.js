import blockedSites from './rules.js';

let isBlockerEnabled = true;

// Initialize blocker state
chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({ blockerEnabled: true });
});

chrome.webNavigation.onBeforeNavigate.addListener(function(details) {
    if (details.url.includes(chrome.runtime.getURL('blocked.html'))) return;
    
    chrome.storage.local.get(['blockerEnabled'], function(result) {
        if (result.blockerEnabled) {
            const currentUrl = details.url.toLowerCase();
            const isBlocked = blockedSites.some(site => currentUrl.includes(site.toLowerCase()));
            
            if (isBlocked) {
                chrome.tabs.update(details.tabId, {
                    url: chrome.runtime.getURL('blocked.html')
                });
            }
        }
    });
}, {
    url: [{
        schemes: ['http', 'https']
    }]
});

// Handle toggle messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'toggleBlocker') {
        chrome.storage.local.set({ blockerEnabled: message.enabled });
        isBlockerEnabled = message.enabled;
    }
    
    if (message.action === 'toggleAntivirus') {
        // Implement your antivirus toggle logic here
        chrome.storage.local.set({ antivirusEnabled: message.enabled }, () => {
            if (chrome.runtime.lastError) {
                sendResponse({ success: false });
            } else {
                sendResponse({ success: true });
                // Add your antivirus enable/disable logic here
                if (message.enabled) {
                    console.log('Antivirus enabled');
                    // Enable antivirus functionality
                } else {
                    console.log('Antivirus disabled');
                    // Disable antivirus functionality
                }
            }
        });
        return true; // Keep the message channel open for async response
    }
});