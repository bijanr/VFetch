document.addEventListener('DOMContentLoaded', () => {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');
    const resultsContainer = document.getElementById('results-container');
    let isSearching = false;

    searchButton.addEventListener('click', async () => {
        if (isSearching) return; // Prevent multiple searches

        const query = searchInput.value;
        if (!query) {
            alert('Please enter a search query.');
            return;
        }

        isSearching = true;
        searchButton.disabled = true;
        searchButton.textContent = 'Searching...';
        resultsContainer.innerHTML = '<p>Searching...</p>';

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const results = await response.json();

            resultsContainer.innerHTML = '';

            if (results.length === 0) {
                resultsContainer.innerHTML = '<p>No results found.</p>';
                return;
            }

            results.forEach(video => {
                const videoElement = document.createElement('div');
                videoElement.classList.add('video-result');

                videoElement.innerHTML = `
                    <p class="video-title">${video.title}</p>
                    <div class="download-options">
                        <select class="quality-select">
                            <option value="720p">720p</option>
                            <option value="480p">480p</option>
                            <option value="360p">360p</option>
                        </select>
                        <button class="download-button" data-url="${video.url}">Download</button>
                    </div>
                `;

                resultsContainer.appendChild(videoElement);
            });

            addDownloadButtonListeners();
        } catch (error) {
            console.error('Error fetching search results:', error);
            resultsContainer.innerHTML = '<p>Error fetching results. Please try again.</p>';
        } finally {
            isSearching = false;
            searchButton.disabled = false;
            searchButton.textContent = 'Search';
        }
    });

    function addDownloadButtonListeners() {
        const downloadButtons = document.querySelectorAll('.download-button');
        downloadButtons.forEach(button => {
            button.addEventListener('click', async () => {
                const videoUrl = button.dataset.url;
                const quality = button.closest('.download-options').querySelector('.quality-select').value;
                const buttonText = button.textContent;
                button.textContent = 'Processing...';
                button.disabled = true;

                try {
                    // Always use full YouTube URL
                    const fullVideoUrl = videoUrl.startsWith('http') ? videoUrl : `https://www.youtube.com${videoUrl}`;
                    // Open download in a new tab/window
                    window.open(`/api/download?url=${encodeURIComponent(fullVideoUrl)}&quality=${quality}`, '_blank');
                    button.textContent = buttonText;
                    button.disabled = false;
                } catch (error) {
                    console.error('Error fetching download link:', error);
                    alert('Error fetching download link. Please try again.');
                    button.textContent = buttonText;
                    button.disabled = false;
                }
            });
        });
    }
});