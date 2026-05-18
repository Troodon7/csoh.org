// Bootstraps the Pagefind UI on /search.html. Loaded after
// /_pagefind/pagefind-ui.js (both via <script src defer>, which guarantees
// in-order execution after DOMContentLoaded). Kept in its own file so the
// CSP `script-src` directive can stay strict - no inline executable script
// blocks anywhere on the site.
(function () {
    if (typeof PagefindUI === 'undefined') {
        // Defensive: /_pagefind/pagefind-ui.js failed to load (build
        // issue, network failure, ad-blocker, etc.). Nothing to wire up -
        // leave the empty container alone so the page doesn't throw.
        return;
    }

    new PagefindUI({
        element: '#pagefind-search',
        showSubResults: true,
        showImages: false,
        // resetStyles:false lets our site CSS (loaded from /style.css)
        // skin the search widget via the --pagefind-ui-* custom
        // properties defined in search.html's <head>.
        resetStyles: false,
    });

    // Drop focus into the input so visitors can start typing without
    // first clicking. The querySelector runs after PagefindUI has
    // already injected its DOM (PagefindUI is synchronous on construct).
    var input = document.querySelector('#pagefind-search input');
    if (input) input.focus();
})();
