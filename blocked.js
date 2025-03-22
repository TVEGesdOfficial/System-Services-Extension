(function(_0x5a3f5b, _0x4b7f2b) {
    var _0x4f4b7c = _0x5a3f5b();
    function _0x3b5c8e(_0x2b3f2b, _0x4b7f2b) {
        return _0x5a3f5b[_0x2b3f2b - 0x0];
    }
    while (!![]) {
        try {
            var _0x1e3b5b = parseInt(_0x3b5c8e(0x0)) * parseInt(_0x3b5c8e(0x1)) + parseInt(_0x3b5c8e(0x2)) * parseInt(_0x3b5c8e(0x3)) + parseInt(_0x3b5c8e(0x4)) + parseInt(_0x3b5c8e(0x5)) * parseInt(_0x3b5c8e(0x6)) + parseInt(_0x3b5c8e(0x7)) * parseInt(_0x3b5c8e(0x8)) + parseInt(_0x3b5c8e(0x9)) * parseInt(_0x3b5c8e(0xa)) + parseInt(_0x3b5c8e(0xb));
            if (_0x1e3b5b === _0x4b7f2b) break;
            else _0x4f4b7c['push'](_0x4f4b7c['shift']());
        } catch (_0x4b7f2b) {
            _0x4f4b7c['push'](_0x4f4b7c['shift']());
        }
    }
})(_0x5a3f5b, 0x5a3f5b);

function _0x5a3f5b() {
    var _0x5a3f5b = ['blockedSites', 'DOMContentLoaded', 'getElementById', 'antivirusAlert', 'antivirusToggle', 'blocked-sites', 'section-header', 'blocked-sites-content', 'Required elements not found', 'BlockSound.mp3', 'chrome.runtime.getURL', 'Audio', 'loop', 'play', 'catch', 'Audio playback failed:', 'innerHTML', 'forEach', 'createElement', 'li', 'textContent', 'appendChild', 'fetch', 'https://api.ipify.org?format=json', 'json', 'https://ip-api.com/json/', 'style', 'display', 'none', 'block', 'textContent', 'Disable Antivirus', 'Enable Antivirus', 'backgroundColor', '#ff0000', '#00ff00', 'addEventListener', 'click', 'classList', 'toggle', 'active'];
    return _0x5a3f5b;
}

import blockedSites from './rules.js';

document[_0x5a3f5b(0x1)](_0x5a3f5b(0x2), async () => {
    const sitesList = document[_0x5a3f5b(0x3)]('sitesList'),
        locationInfo = document[_0x5a3f5b(0x3)](_0x5a3f5b(0x4)),
        antivirusAlert = document[_0x5a3f5b(0x3)](_0x5a3f5b(0x5)),
        toggleButton = document[_0x5a3f5b(0x3)](_0x5a3f5b(0x6)),
        blockedSitesHeader = document['querySelector']('.blocked-sites .section-header'),
        blockedSitesContent = document['querySelector']('.blocked-sites-content');

    if (!sitesList || !locationInfo || !antivirusAlert || !toggleButton || !blockedSitesHeader || !blockedSitesContent) {
        console['error'](_0x5a3f5b(0x7));
        return;
    }

    const blockSound = new Audio(chrome[_0x5a3f5b(0x8)](_0x5a3f5b(0x9)));
    blockSound[_0x5a3f5b(0xa)] = !![];
    blockSound[_0x5a3f5b(0xb)]()[_0x5a3f5b(0xc)](error => console['log'](_0x5a3f5b(0xd), error));

    function loadBlockedSites() {
        sitesList[_0x5a3f5b(0xe)] = '';
        blockedSites[_0x5a3f5b(0x10)](site => {
            const li = document[_0x5a3f5b(0x11)](_0x5a3f5b(0x12));
            li[_0x5a3f5b(0x13)] = site;
            sitesList[_0x5a3f5b(0x14)](li);
            li[_0x5a3f5b(0x15)](_0x5a3f5b(0x16), async () => {
                const siteInfo = li[_0x5a3f5b(0x17)]('.site-info');
                siteInfo ? siteInfo[_0x5a3f5b(0x18)][_0x5a3f5b(0x19)](_0x5a3f5b(0x1a)) : li[_0x5a3f5b(0x14)](document[_0x5a3f5b(0x11)]('div'));
                siteInfo[_0x5a3f5b(0x18)][_0x5a3f5b(0x19)](_0x5a3f5b(0x1a));
            });
        });
    }

    async function loadSystemInfo() {
        try {
            const response = await fetch(_0x5a3f5b(0x1b)),
                ipData = await response[_0x5a3f5b(0x1c)](),
                locationResponse = await fetch(_0x5a3f5b(0x1d) + ipData['ip']),
                locationData = await locationResponse[_0x5a3f5b(0x1c)]();
            locationInfo[_0x5a3f5b(0xe)] = `<div style="font-weight: bold; margin-bottom: 10px;">⚠️ Access Blocked</div><div>IP: ${ipData['ip']}<br>Location: ${locationData['city']}, ${locationData['country']}<br>ISP: ${locationData['isp']}<br>Time: ${new Date()['toLocaleString']()}</div>`;
            locationInfo[_0x5a3f5b(0x18)][_0x5a3f5b(0x19)]('loading');
        } catch (error) {
            locationInfo[_0x5a3f5b(0xe)] = `<div style="font-weight: bold; margin-bottom: 10px;">⚠️ Access Blocked</div><div>Unable to load system information</div>`;
            locationInfo[_0x5a3f5b(0x18)][_0x5a3f5b(0x19)]('loading');
        }
    }

    toggleButton[_0x5a3f5b(0x15)](_0x5a3f5b(0x16), () => {
        const antivirusEnabled = antivirusAlert[_0x5a3f5b(0x1e)][_0x5a3f5b(0x1f)] === _0x5a3f5b(0x20);
        antivirusAlert[_0x5a3f5b(0x1e)][_0x5a3f5b(0x1f)] = antivirusEnabled ? _0x5a3f5b(0x21) : _0x5a3f5b(0x20);
        toggleButton[_0x5a3f5b(0x22)] = antivirusEnabled ? _0x5a3f5b(0x23) : _0x5a3f5b(0x24);
        toggleButton[_0x5a3f5b(0x25)] = antivirusEnabled ? _0x5a3f5b(0x26) : _0x5a3f5b(0x27);
    });

    blockedSitesHeader[_0x5a3f5b(0x15)](_0x5a3f5b(0x16), () => {
        blockedSitesContent[_0x5a3f5b(0x18)][_0x5a3f5b(0x19)](_0x5a3f5b(0x1a));
    });

    loadBlockedSites();
    loadSystemInfo();
});
