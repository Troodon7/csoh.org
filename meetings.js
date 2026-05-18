// meetings.html (index) - search + filter buttons across the meeting cards.
// Lives in an external file because the site's strict CSP
// (`script-src 'self'`) blocks any inline <script> block.
(function () {
    const input = document.getElementById('meetingSearch');
    const filters = document.getElementById('meetingFilters');
    const cards = Array.from(document.querySelectorAll('.meeting-card'));
    const countEl = document.getElementById('visibleMeetings');
    const noRes = document.getElementById('noMeetingResults');
    const clearBtn = document.getElementById('clearMeetingSearch');

    if (!cards.length) return;

    // Pull each card's filterable data once up front. `text` starts as
    // the card-only summary; once the full-text index loads, we swap each
    // entry's `text` for the full meeting recap so search hits speakers
    // and topics buried in the body, not just the card summary.
    const meta = cards.map(card => {
        const tags = Array.from(card.querySelectorAll('.meeting-tags .tag')).map(t => t.textContent);
        const yearMatch = card.id.match(/^meeting-(\d{4})/);
        return {
            el: card,
            id: card.id,
            year: yearMatch ? yearMatch[1] : null,
            tags,
            text: card.textContent.toLowerCase(),
        };
    });

    // Auto-generate year + topical-tag filter buttons. Month tags
    // (YYYY-MM) are searchable via the text input but not surfaced as
    // buttons to keep the row tidy.
    if (filters) {
        const tagSet = new Set();
        meta.forEach(m => m.tags.forEach(t => tagSet.add(t)));
        const topicalTags = Array.from(tagSet)
            .filter(t => !/^\d{4}-\d{2}$/.test(t))
            .sort();

        const years = Array.from(new Set(meta.map(m => m.year).filter(Boolean)))
            .sort()
            .reverse();

        const frag = document.createDocumentFragment();
        const makeBtn = (label, filterValue) => {
            const b = document.createElement('button');
            b.type = 'button';
            b.className = 'filter-btn';
            b.setAttribute('data-filter', filterValue);
            b.textContent = label;
            return b;
        };
        years.forEach(y => frag.appendChild(makeBtn(y, 'year:' + y)));
        topicalTags.forEach(t => frag.appendChild(makeBtn(t, 'tag:' + t)));
        filters.appendChild(frag);
    }

    let activeFilter = 'all';
    let searchTerm = '';

    function refresh() {
        let visible = 0;
        meta.forEach(m => {
            let show = true;
            if (activeFilter.startsWith('year:')) {
                if (m.year !== activeFilter.slice(5)) show = false;
            } else if (activeFilter.startsWith('tag:')) {
                if (!m.tags.includes(activeFilter.slice(4))) show = false;
            }
            if (show && searchTerm && !m.text.includes(searchTerm)) {
                show = false;
            }
            m.el.style.display = show ? '' : 'none';
            if (show) visible++;
        });
        if (countEl) countEl.textContent = String(visible);
        if (noRes) noRes.classList.toggle('is-hidden', visible !== 0);
    }

    // Lazy-load the full-text index on first interaction with the search
    // box. The index is built by tools/build_meetings_search_index.py and
    // contains the full body text of every per-meeting recap. Until it
    // arrives, search runs against the card-only summary text.
    let indexState = 'idle'; // 'idle' | 'loading' | 'loaded' | 'failed'
    function ensureIndex() {
        if (indexState !== 'idle') return;
        indexState = 'loading';
        fetch('/meetings-search-index.json', { credentials: 'omit' })
            .then(r => r.ok ? r.json() : Promise.reject(r.status))
            .then(entries => {
                const byId = new Map(entries.map(e => [e.id, e.text]));
                meta.forEach(m => {
                    const full = byId.get(m.id);
                    if (full) m.text = m.text + ' ' + full;
                });
                indexState = 'loaded';
                if (searchTerm) refresh();
            })
            .catch(() => { indexState = 'failed'; });
    }

    if (filters) {
        filters.addEventListener('click', (ev) => {
            const btn = ev.target.closest('button[data-filter]');
            if (!btn) return;
            Array.from(filters.querySelectorAll('button[data-filter]'))
                .forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            activeFilter = btn.getAttribute('data-filter');
            refresh();
        });
    }

    if (input) {
        let timer = null;
        input.addEventListener('input', () => {
            ensureIndex();
            clearTimeout(timer);
            timer = setTimeout(() => {
                searchTerm = input.value.trim().toLowerCase();
                refresh();
            }, 120);
        });
        // Also kick off the fetch on focus so by the time the user has
        // typed a query, the index is usually already loaded.
        input.addEventListener('focus', ensureIndex, { once: true });
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            if (input) input.value = '';
            searchTerm = '';
            activeFilter = 'all';
            if (filters) {
                Array.from(filters.querySelectorAll('button[data-filter]'))
                    .forEach(b => b.classList.remove('active'));
                const allBtn = filters.querySelector('button[data-filter="all"]');
                if (allBtn) allBtn.classList.add('active');
            }
            refresh();
        });
    }

    // Initial sync so the visible-count starts truthful.
    refresh();
})();
