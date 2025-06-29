document.addEventListener('DOMContentLoaded', () => {
    const markButtons = document.querySelectorAll('.mark-button');
    const clearMarkerBtn = document.getElementById('clear-marker-btn');
    const goToMarkerBtn = document.getElementById('go-to-marker-btn');

    const MARKER_KEY = 'iknow_marked_item';

    // Function to save the marked item to local storage
    const saveMarker = (itemId, pageUrl) => {
        localStorage.setItem(MARKER_KEY, JSON.stringify({ itemId, pageUrl }));
        updateMarkerDisplay();
    };

    // Function to retrieve the marked item from local storage
    const getMarker = () => {
        const markerData = localStorage.getItem(MARKER_KEY);
        return markerData ? JSON.parse(markerData) : null;
    };

    // Function to clear the marker from local storage
    const clearMarker = () => {
        localStorage.removeItem(MARKER_KEY);
        updateMarkerDisplay();
    };

    // Function to update the display of the marked item
    const updateMarkerDisplay = () => {
        // Remove existing highlights
        document.querySelectorAll('.item-section.marked').forEach(el => {
            el.classList.remove('marked');
        });

        const marker = getMarker();
        if (marker && marker.pageUrl === window.location.pathname.split('/').pop()) {
            const markedItem = document.getElementById(marker.itemId);
            if (markedItem) {
                markedItem.classList.add('marked');
            }
        }
    };

    // Event listeners for "Mark as Learning" buttons
    markButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const itemId = event.target.dataset.itemId;
            const pageUrl = window.location.pathname.split('/').pop(); // Get current page filename
            saveMarker(itemId, pageUrl);
        });
    });

    // Event listener for "Clear Marker" button
    if (clearMarkerBtn) {
        clearMarkerBtn.addEventListener('click', () => {
            clearMarker();
            alert('Marker cleared!');
        });
    }

    // Event listener for "Go to Marked Item" button
    if (goToMarkerBtn) {
        goToMarkerBtn.addEventListener('click', () => {
            const marker = getMarker();
            if (marker) {
                const currentPageUrl = window.location.pathname.split('/').pop();
                if (marker.pageUrl === currentPageUrl) {
                    // If on the same page, scroll to the item
                    const markedItem = document.getElementById(marker.itemId);
                    if (markedItem) {
                        markedItem.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                } else {
                    // If on a different page, navigate to the page and then scroll
                    window.location.href = `${marker.pageUrl}#${marker.itemId}`;
                }
            } else {
                alert('No item is marked.');
            }
        });
    }

    // Initial display update when the page loads
    updateMarkerDisplay();

    // Handle direct navigation to a marked item via URL hash
    if (window.location.hash) {
        const targetId = window.location.hash.substring(1);
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
});
