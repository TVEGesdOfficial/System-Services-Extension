// ... existing code ...

function blockPage() {
    // Clear the page content
    document.body.innerHTML = '';
    
    // Create a simple blocked message
    const message = document.createElement('div');
    message.style.position = 'fixed';
    message.style.top = '50%';
    message.style.left = '50%';
    message.style.transform = 'translate(-50%, -50%)';
    message.style.textAlign = 'center';
    message.style.color = '#fff';
    message.style.fontFamily = 'Arial, sans-serif';
    
    message.innerHTML = `
        <h2>Access Blocked</h2>
        <p>This site has been restricted by your administrator.</p>
    `;
    
    document.body.style.backgroundColor = '#000';
    document.body.appendChild(message);
}

// ... existing code ...