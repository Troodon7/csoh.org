// meetings.html (index) — client-side search across the meeting cards.
// Lives in an external file because the site's strict CSP
// (`script-src 'self'`) blocks any inline <script> block.
(function () {
    const input = document.getElementById('meetingSearch');
    const cards = Array.from(document.querySelectorAll('.meeting-card'));
    const noRes = document.getElementById('noMeetingResults');
    if (!input || !cards.length) return;

    input.addEventListener('input', () => {
        const q = input.value.toLowerCase().trim();
        let visible = 0;
        cards.forEach(card => {
            const txt = card.textContent.toLowerCase();
            const match = !q || txt.includes(q);
            card.style.display = match ? '' : 'none';
            if (match) visible++;
        });
        if (noRes) noRes.classList.toggle('is-hidden', visible !== 0);
    });
})();
