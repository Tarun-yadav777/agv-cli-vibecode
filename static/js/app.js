document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const btnRefresh = document.getElementById('btn-refresh');
    const finishedMatchesContainer = document.getElementById('finished-matches-list');
    const upcomingMatchesContainer = document.getElementById('upcoming-matches-list');
    const finishedSection = document.getElementById('finished-section');
    const upcomingSection = document.getElementById('upcoming-section');

    // Create Toast Container
    const toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.style.position = 'fixed';
    toastContainer.style.bottom = '20px';
    toastContainer.style.right = '20px';
    toastContainer.style.zIndex = '9999';
    toastContainer.style.display = 'flex';
    toastContainer.style.flexDirection = 'column';
    toastContainer.style.gap = '10px';
    document.body.appendChild(toastContainer);

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.style.background = 'rgba(18, 22, 47, 0.95)';
        toast.style.color = '#fff';
        toast.style.padding = '12px 24px';
        toast.style.borderRadius = '12px';
        toast.style.border = '1px solid rgba(255,255,255,0.15)';
        toast.style.boxShadow = '0 10px 25px rgba(0,0,0,0.3)';
        toast.style.fontFamily = "'Outfit', sans-serif";
        toast.style.fontWeight = '600';
        toast.style.fontSize = '0.95rem';
        toast.style.backdropFilter = 'blur(10px)';
        toast.style.display = 'flex';
        toast.style.alignItems = 'center';
        toast.style.gap = '10px';
        toast.style.transform = 'translateY(50px)';
        toast.style.opacity = '0';
        toast.style.transition = 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)';

        let icon = '⚽';
        if (type === 'info') icon = 'ℹ️';
        if (type === 'check') icon = '✅';

        toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
        toastContainer.appendChild(toast);

        // Trigger transition
        setTimeout(() => {
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
        }, 10);

        // Remove toast
        setTimeout(() => {
            toast.style.transform = 'translateY(-20px)';
            toast.style.opacity = '0';
            setTimeout(() => {
                toast.remove();
            }, 400);
        }, 4000);
    }

    // Refresh Action
    btnRefresh.addEventListener('click', async () => {
        btnRefresh.disabled = true;
        const icon = btnRefresh.querySelector('i');
        if (icon) icon.className = 'fas fa-sync-alt fa-spin';

        try {
            const response = await fetch('/api/refresh', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                updateUI(data);
                showToast(data.message || 'Match day scores synced.', 'check');
            } else {
                showToast('Failed to sync data.', 'info');
            }
        } catch (error) {
            console.error('Error refreshing matches:', error);
            showToast('Network error during sync.', 'info');
        } finally {
            btnRefresh.disabled = false;
            if (icon) icon.className = 'fas fa-sync-alt';
        }
    });

    // Group Tab Switching
    const setupTabListeners = () => {
        const tabs = document.querySelectorAll('.group-tab-btn');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                const groupName = tab.dataset.group;
                document.querySelectorAll('.standings-group-tab-content').forEach(content => {
                    content.classList.add('hidden');
                });
                
                const activeContent = document.getElementById(`group-content-${groupName}`);
                if (activeContent) {
                    activeContent.classList.remove('hidden');
                }
            });
        });
    };

    setupTabListeners();

    // Update UI from data
    function updateUI(data) {
        const matches = data.matches;
        const standings = data.standings;

        // Group matches by status
        const finished = matches.filter(m => m.status === 'finished');
        const upcoming = matches.filter(m => m.status === 'upcoming');

        // 1. Process Finished Section Visibility
        if (finished.length > 0) {
            finishedSection.classList.remove('hidden');
            syncMatches(finished, finishedMatchesContainer);
        } else {
            finishedSection.classList.add('hidden');
            finishedMatchesContainer.innerHTML = '';
        }

        // 2. Process Upcoming Section Visibility
        if (upcoming.length > 0) {
            upcomingSection.classList.remove('hidden');
            syncMatches(upcoming, upcomingMatchesContainer);
        } else {
            upcomingSection.classList.add('hidden');
            upcomingMatchesContainer.innerHTML = '';
        }

        // 3. Update Standings Tables
        updateStandingsUI(standings);
    }

    // Smart sync matches to avoid full page rebuilds and trigger animations
    function syncMatches(matchesList, container) {
        const existingCards = container.querySelectorAll('.match-card');
        const existingIds = Array.from(existingCards).map(c => parseInt(c.dataset.id));
        const newIds = matchesList.map(m => m.id);

        const mismatch = existingIds.length !== newIds.length || !newIds.every(id => existingIds.includes(id));
        
        if (mismatch) {
            container.innerHTML = '';
            matchesList.forEach(m => {
                container.appendChild(createMatchCard(m));
            });
            return;
        }

        matchesList.forEach(m => {
            const card = container.querySelector(`.match-card[data-id="${m.id}"]`);
            if (!card) return;

            const homeScoreSpan = card.querySelector('.score-home');
            const awayScoreSpan = card.querySelector('.score-away');
            
            if (homeScoreSpan) homeScoreSpan.textContent = m.home_score;
            if (awayScoreSpan) awayScoreSpan.textContent = m.away_score;

            card.dataset.homeScore = m.home_score;
            card.dataset.awayScore = m.away_score;

            const badge = card.querySelector('.match-time-badge');
            if (badge) {
                if (m.status === 'finished') {
                    badge.textContent = 'FT';
                } else {
                    badge.textContent = m.time;
                }
            }

            const eventsContainer = card.querySelector('.match-events-timeline');
            if (eventsContainer) {
                eventsContainer.innerHTML = renderEvents(m.events);
            }
        });
    }

    // Helper to generate a single match card DOM element
    function createMatchCard(m) {
        const card = document.createElement('div');
        card.className = 'match-card';
        card.dataset.id = m.id;
        card.dataset.homeScore = m.home_score;
        card.dataset.awayScore = m.away_score;

        let badgeContent = '';
        if (m.status === 'finished') {
            badgeContent = `<div class="match-time-badge">FT</div>`;
        } else {
            badgeContent = `<div class="match-time-badge">${m.time}</div>`;
        }

        const eventsHtml = m.events && m.events.length > 0 ? `
            <div class="match-events-timeline">
                ${renderEvents(m.events)}
            </div>
        ` : '';

        const homeFlag = m.home_flag || m.home_code.toLowerCase();
        const awayFlag = m.away_flag || m.away_code.toLowerCase();

        card.innerHTML = `
            <div class="match-meta">
                <span class="match-group-info">${m.group}</span>
                <span class="match-stadium">${m.stadium}</span>
                <span>${m.date}</span>
            </div>
            
            <div class="match-content-grid">
                <div class="team-display home">
                    <span class="team-name">${m.home_team}</span>
                    <img src="https://flagcdn.com/w80/${homeFlag}.png" alt="${m.home_team} Flag" class="flag-logo">
                </div>

                <div class="score-center">
                    <div class="score-display">
                        <span class="score-home">${m.home_score}</span>
                        <span class="score-divider">:</span>
                        <span class="score-away">${m.away_score}</span>
                    </div>
                    ${badgeContent}
                </div>

                <div class="team-display away">
                    <img src="https://flagcdn.com/w80/${awayFlag}.png" alt="${m.away_team} Flag" class="flag-logo">
                    <span class="team-name">${m.away_team}</span>
                </div>
            </div>

            ${eventsHtml}
        `;
        return card;
    }

    // Helper to render event list html
    function renderEvents(events) {
        if (!events) return '';
        return events.map(e => {
            let iconClass = 'goal';
            let iconHtml = '⚽';
            
            if (e.type === 'yellow_card') { iconClass = 'yellow'; iconHtml = '🟨'; }
            else if (e.type === 'red_card') { iconClass = 'red'; iconHtml = '🟥'; }
            else if (e.type === 'substitution') { iconClass = 'sub'; iconHtml = '🔄'; }
            else if (e.type === 'whistle') { iconClass = 'whistle'; iconHtml = '🏁'; }

            return `
                <div class="timeline-event">
                    <span class="event-icon-circle ${iconClass}">${iconHtml}</span>
                    <span class="event-time">${e.minute > 0 ? e.minute + "'" : '-'}</span>
                    <span class="event-text">${e.detail}</span>
                </div>
            `;
        }).join('');
    }

    // Rebuild Standings Tables in UI
    function updateStandingsUI(standings) {
        Object.keys(standings).forEach(groupName => {
            const tableBody = document.getElementById(`standings-body-${groupName.replace(' ', '-')}`);
            if (!tableBody) return;

            tableBody.innerHTML = '';
            
            standings[groupName].forEach((team, index) => {
                const tr = document.createElement('tr');
                if (index < 2) {
                    tr.className = 'qualify-zone';
                }
                
                tr.innerHTML = `
                    <td class="team-cell">
                        <img src="https://flagcdn.com/w80/${team.flag_code}.png" alt="${team.name} Flag" class="flag-logo-mini">
                        <strong>${team.name}</strong>
                    </td>
                    <td>${team.P}</td>
                    <td>${team.W}</td>
                    <td>${team.D}</td>
                    <td>${team.L}</td>
                    <td>${team.GD >= 0 ? '+' + team.GD : team.GD}</td>
                    <td class="pts-cell">${team.PTS}</td>
                `;
                tableBody.appendChild(tr);
            });
        });
    }
});
