document.getElementById('downloadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const links = document.getElementById('links').value.split('\n').filter(l => l.trim());
    if (links.length > 5) {
        alert("Maximum 5 links allowed");
        return;
    }
    
    const response = await fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ links })
    });
    
    const data = await response.json();
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';
    
    data.urls.forEach((url, index) => {
        const a = document.createElement('a');
        a.href = url;
        a.target = '_blank';
        a.innerText = `Download Video ${index + 1}`;
        a.className = 'd-block mb-2';
        resultsDiv.appendChild(a);
    });
});
