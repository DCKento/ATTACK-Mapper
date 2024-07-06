document.addEventListener('DOMContentLoaded', () => {
    const attackFramework = document.getElementById('attack-framework');
    
    function renderFramework(data) {
        attackFramework.innerHTML = '';
        data.tactics.forEach(tactic => {
            const tacticElement = document.createElement('div');
            tacticElement.className = 'tactic';
            tacticElement.innerHTML = `
                <div class="tactic-header">
                    <h2>${tactic.name}</h2>
                </div>
            `;
            
            tactic.techniques.forEach(technique => {
                const techElement = document.createElement('div');
                techElement.className = 'technique';
                techElement.innerHTML = `
                    <h3>${technique.name}</h3>
                    <input type="text" class="control-input" placeholder="Enter control" data-id="${technique.id}">
                    <select class="color-select" data-id="${technique.id}">
                        <option value="">Select effectiveness</option>
                        <option value="red">Red</option>
                        <option value="orange">Orange</option>
                        <option value="green">Green</option>
                    </select>
                    <button class="upload-btn" data-id="${technique.id}">Upload Screenshot</button>
                    <div class="screenshot-preview" data-id="${technique.id}"></div>
                `;
                
                technique.subtechniques.forEach(subtech => {
                    const subtechElement = document.createElement('div');
                    subtechElement.className = 'subtechnique';
                    subtechElement.innerHTML = `
                        <h4>${subtech.name}</h4>
                        <input type="text" class="control-input" placeholder="Enter control" data-id="${subtech.id}">
                        <select class="color-select" data-id="${subtech.id}">
                            <option value="">Select effectiveness</option>
                            <option value="red">Red</option>
                            <option value="orange">Orange</option>
                            <option value="green">Green</option>
                        </select>
                        <button class="upload-btn" data-id="${subtech.id}">Upload Screenshot</button>
                        <div class="screenshot-preview" data-id="${subtech.id}"></div>
                    `;
                    techElement.appendChild(subtechElement);
                });
                
                tacticElement.appendChild(techElement);
            });
            
            attackFramework.appendChild(tacticElement);
        });
    }
    
    // Fetch and render initial data
    fetch('/api/framework')
        .then(response => response.json())
        .then(data => renderFramework(data));
    
    // Real-time updates
    attackFramework.addEventListener('change', (event) => {
        if (event.target.classList.contains('control-input') || event.target.classList.contains('color-select')) {
            const id = event.target.getAttribute('data-id');
            const control = document.querySelector(`.control-input[data-id="${id}"]`).value;
            const color = document.querySelector(`.color-select[data-id="${id}"]`).value;
            
            fetch('/api/update_technique', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id, control, color }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    event.target.closest('.technique, .subtechnique').className = 
                        event.target.closest('.technique, .subtechnique').className.replace(/red|orange|green/, '') + ' ' + color;
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });
    
    // Screenshot upload
    attackFramework.addEventListener('click', (event) => {
        if (event.target.classList.contains('upload-btn')) {
            const id = event.target.getAttribute('data-id');
            const fileInput = document.getElementById('screenshot-upload');
            fileInput.click();
            fileInput.onchange = () => {
                const file = fileInput.files[0];
                const formData = new FormData();
                formData.append('screenshot', file);
                formData.append('id', id);
                
                fetch('/api/upload_screenshot', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        const previewDiv = document.querySelector(`.screenshot-preview[data-id="${id}"]`);
                        previewDiv.innerHTML = `<img src="${data.url}" alt="Screenshot">`;
                    }
                })
                .catch(error => console.error('Error:', error));
            };
        }
    });
    
    // Export functionality
    document.getElementById('export-json-btn').addEventListener('click', () => {
        fetch('/api/export')
            .then(response => response.json())
            .then(data => {
                const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
                const downloadAnchorNode = document.createElement('a');
                downloadAnchorNode.setAttribute("href", dataStr);
                downloadAnchorNode.setAttribute("download", "attack_mapper_export.json");
                document.body.appendChild(downloadAnchorNode);
                downloadAnchorNode.click();
                downloadAnchorNode.remove();
            });
    });
    
    document.getElementById('export-csv-btn').addEventListener('click', () => {
        fetch('/api/export_csv')
            .then(response => response.blob())
            .then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = url;
                a.download = 'attack_mapper_export.csv';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            });
    });
});
