  const tabNav = document.querySelector('.incident-tabs');
  const tabs = Array.from(tabNav.querySelectorAll('.itab'));

  tabs.sort((a, b) => {
    return parseInt(a.dataset.year || 0) - parseInt(b.dataset.year || 0);
  });

  tabs.forEach(tab => tabNav.appendChild(tab));

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.itab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.incident-panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      const panel = document.getElementById(tab.dataset.panel);
      if (panel) panel.classList.add('active');
    });
  });