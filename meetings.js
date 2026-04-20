// meetings.html filter — search + topical tags.
// Lives in an external file because the site's strict CSP
// (`script-src 'self'`) blocks any inline <script> block.
(function () {
    const articles = Array.from(document.querySelectorAll('article[id^="meeting-"]'));
    const tocItems = Array.from(document.querySelectorAll('#table-of-contents li'));
    const search = document.getElementById('meetingSearch');
    const filters = document.getElementById('meetingFilters');
    const countEl = document.getElementById('visibleMeetings');
    const noResults = document.getElementById('noMeetingResults');
    const clearBtn = document.getElementById('clearMeetingSearch');

    if (!articles.length || !filters) return;

    // Build a map of each meeting's filter-relevant data.
    const meta = articles.map((art, i) => ({
        el: art,
        id: art.id,
        tags: Array.from(art.querySelectorAll('.meeting-tags .tag')).map(t => t.textContent),
        text: art.textContent.toLowerCase(),
        toc: tocItems[i] || null,
    }));

    // Auto-generate topical-tag filter buttons. Month tags (YYYY-MM)
    // are deliberately omitted to keep the button row tidy; they remain
    // searchable via the text input.
    const tagSet = new Set();
    meta.forEach(m => m.tags.forEach(t => tagSet.add(t)));
    const topicalTags = Array.from(tagSet).filter(t => !/^\d{4}-\d{2}$/.test(t)).sort();

    const frag = document.createDocumentFragment();
    const makeBtn = (label, value) => {
        const b = document.createElement('button');
        b.className = 'filter-btn';
        b.setAttribute('data-filter', 'tag:' + value);
        b.textContent = label;
        return b;
    };
    topicalTags.forEach(t => frag.appendChild(makeBtn(t, t)));
    filters.appendChild(frag);

    let activeFilter = 'all';
    let searchTerm = '';

    function refresh() {
        let visible = 0;
        meta.forEach(m => {
            let show = true;
            if (activeFilter !== 'all') {
                const value = activeFilter.slice(4); // strip "tag:"
                if (!m.tags.includes(value)) show = false;
            }
            if (show && searchTerm) {
                if (!m.text.includes(searchTerm)) show = false;
            }
            m.el.classList.toggle('is-hidden', !show);
            if (m.toc) m.toc.classList.toggle('is-hidden', !show);
            // Auto-expand topic <details> when a search term matches
            // content inside it; collapse back to default when cleared.
            const det = m.el.querySelector('details.meeting-topics');
            if (det) det.open = show && !!searchTerm;
            if (show) visible++;
        });
        if (countEl) countEl.textContent = String(visible);
        if (noResults) noResults.classList.toggle('is-hidden', visible !== 0);
    }

    filters.addEventListener('click', (ev) => {
        const btn = ev.target.closest('button[data-filter]');
        if (!btn) return;
        Array.from(filters.querySelectorAll('button[data-filter]')).forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = btn.getAttribute('data-filter');
        refresh();
    });

    if (search) {
        let timer = null;
        search.addEventListener('input', () => {
            clearTimeout(timer);
            timer = setTimeout(() => {
                searchTerm = search.value.trim().toLowerCase();
                refresh();
            }, 120);
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            if (search) search.value = '';
            searchTerm = '';
            activeFilter = 'all';
            Array.from(filters.querySelectorAll('button[data-filter]')).forEach(b => b.classList.remove('active'));
            const allBtn = filters.querySelector('button[data-filter="all"]');
            if (allBtn) allBtn.classList.add('active');
            refresh();
        });
    }

    // Initial sync so the "All (N)" counter and no-results state reflect reality.
    refresh();
})();
