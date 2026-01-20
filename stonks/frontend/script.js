const data = __DATA__;

function init() {
    const tabsContainer = document.getElementById('tabs');
    const contentContainer = document.getElementById('content');

    let first = true;

    for (const key in data) {
        const item = data[key];
        const title = item.title;
        const rows = item.data;

        // Create Tab
        const btn = document.createElement('button');
        btn.className = `tab-btn ${first ? 'active' : ''}`;
        btn.innerText = title;
        btn.onclick = () => switchTab(key);
        tabsContainer.appendChild(btn);

        // Create Content Div
        const div = document.createElement('div');
        div.id = `content-${key}`;
        div.className = `tab-content ${first ? 'active' : ''}`;

        // Special handling for recommendations tab
        if (key === 'recommendations') {
            const gainers = item.gainers || [];
            const losers = item.losers || [];

            let html = `
                <div style="margin-bottom: 30px;">
                    <h2 style="color: #27ae60; margin-bottom: 15px;">🚀 Top 30 Gainers (Highest Price Increase)</h2>
                    <div class="table-container">
                        <table id="table-gainers" data-order="desc">
                            <thead>
                                <tr>
                                    <th onclick="sortRecommendationTable('gainers', 0)">Ticker ⬍</th>
                                    <th onclick="sortRecommendationTable('gainers', 1)">Company ⬍</th>
                                    <th onclick="sortRecommendationTable('gainers', 2)">Category ⬍</th>
                                    <th onclick="sortRecommendationTable('gainers', 3)">Price ⬍</th>
                                    <th onclick="sortRecommendationTable('gainers', 4)">Change % ⬍</th>
                                    <th>News</th>
                                </tr>
                            </thead>
                            <tbody>
            `;

            gainers.forEach(r => {
                html += `
                    <tr>
                        <td><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" style="text-decoration:none; color:#3498db; font-weight:bold;">${r.ticker}</a></td>
                        <td><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" style="text-decoration:none; color:inherit;">${r.name}</a></td>
                        <td>${r.category}</td>
                        <td>${r.price_str}</td>
                        <td class="positive" data-val="${r.change}">${r.change_str}</td>
                        <td class="news-links">
                            ${r.links.map(l => `<a href="${l.url}" target="_blank">${l.name}</a>`).join('')}
                        </td>
                    </tr>
                `;
            });

            html += `
                            </tbody>
                        </table>
                    </div>
                </div>
                
                <div>
                    <h2 style="color: #c0392b; margin-bottom: 15px;">📉 Top 30 Losers (Highest Price Decrease)</h2>
                    <div class="table-container">
                        <table id="table-losers" data-order="desc">
                            <thead>
                                <tr>
                                    <th onclick="sortRecommendationTable('losers', 0)">Ticker ⬍</th>
                                    <th onclick="sortRecommendationTable('losers', 1)">Company ⬍</th>
                                    <th onclick="sortRecommendationTable('losers', 2)">Category ⬍</th>
                                    <th onclick="sortRecommendationTable('losers', 3)">Price ⬍</th>
                                    <th onclick="sortRecommendationTable('losers', 4)">Change % ⬍</th>
                                    <th>News</th>
                                </tr>
                            </thead>
                            <tbody>
            `;

            losers.forEach(r => {
                html += `
                    <tr>
                        <td><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" style="text-decoration:none; color:#3498db; font-weight:bold;">${r.ticker}</a></td>
                        <td><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" style="text-decoration:none; color:inherit;">${r.name}</a></td>
                        <td>${r.category}</td>
                        <td>${r.price_str}</td>
                        <td class="negative" data-val="${r.change}">${r.change_str}</td>
                        <td class="news-links">
                            ${r.links.map(l => `<a href="${l.url}" target="_blank">${l.name}</a>`).join('')}
                        </td>
                    </tr>
                `;
            });

            html += `
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            div.innerHTML = html;
            contentContainer.appendChild(div);
            first = false;
            continue;
        }

        // Regular category handling
        // Calculate stats
        const gainersCount = rows.filter(r => r.change > 0).length;
        const losersCount = rows.filter(r => r.change < 0).length;

        // Determine Best and Worst
        let best = { name: 'N/A', ticker: '-', change_str: '-' };
        let worst = { name: 'N/A', ticker: '-', change_str: '-' };

        if (rows.length > 0) {
            best = rows[0];
            worst = rows[rows.length - 1];
        }

        let html = `
            <div class="stats">
                <div class="card card-total"><h3>Analyzed</h3><p>${rows.length}</p></div>
                <div class="card card-total"><h3>Gainers</h3><p style="color:#27ae60">${gainersCount}</p></div>
                <div class="card card-total"><h3>Losers</h3><p style="color:#c0392b">${losersCount}</p></div>
                <div class="card card-best"><h3>Best Performance</h3><p class="positive" title="${best.name}">${best.ticker} (${best.change_str})</p></div>
                <div class="card card-worst"><h3>Worst Performance</h3><p class="negative" title="${worst.name}">${worst.ticker} (${worst.change_str})</p></div>
            </div>
            <div class="table-container">
                <table id="table-${key}" data-order="asc">
                    <thead>
                        <tr>
                            <th onclick="sortTable('${key}', 0)">Ticker ⬍</th>
                            <th onclick="sortTable('${key}', 1)">Company ⬍</th>
                            <th onclick="sortTable('${key}', 2)">Price ⬍</th>
                            <th onclick="sortTable('${key}', 3)">Change % ⬍</th>
                            <th>News</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        rows.forEach(r => {
            const colorClass = r.change >= 0 ? 'positive' : 'negative';
            html += `
                <tr>
                    <td><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" style="text-decoration:none; color:#3498db; font-weight:bold;">${r.ticker}</a></td>
                    <td><a href="https://finance.yahoo.com/quote/${r.ticker}" target="_blank" style="text-decoration:none; color:inherit;">${r.name}</a></td>
                    <td>${r.price_str}</td>
                    <td class="${colorClass}" data-val="${r.change}">${r.change_str}</td>
                    <td class="news-links">
                        ${r.links.map(l => `<a href="${l.url}" target="_blank">${l.name}</a>`).join('')}
                    </td>
                </tr>
            `;
        });

        html += `</tbody></table></div>`;
        div.innerHTML = html;
        contentContainer.appendChild(div);

        first = false;
    }
}

function switchTab(key) {
    // Buttons
    document.querySelectorAll('.tab-btn').forEach(b => {
        if (b.innerText === data[key].title) b.classList.add('active');
        else b.classList.remove('active');
    });

    // Content
    document.querySelectorAll('.tab-content').forEach(d => d.classList.remove('active'));
    document.getElementById(`content-${key}`).classList.add('active');
}

function sortTable(key, colIndex) {
    const table = document.getElementById(`table-${key}`);
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const currentOrder = table.getAttribute('data-order') || 'asc';
    const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    table.setAttribute('data-order', newOrder);

    rows.sort((a, b) => {
        const cellA = a.children[colIndex].innerText;
        const cellB = b.children[colIndex].innerText;

        // Sort by change % (col 3)
        if (colIndex === 3) {
            const valA = parseFloat(a.children[colIndex].getAttribute('data-val'));
            const valB = parseFloat(b.children[colIndex].getAttribute('data-val'));
            return newOrder === 'asc' ? valA - valB : valB - valA;
        }

        // Sort by price (col 2) - extract number
        if (colIndex === 2) {
            const valA = parseFloat(cellA.replace(/,/g, ''));
            const valB = parseFloat(cellB.replace(/,/g, ''));
            return newOrder === 'asc' ? valA - valB : valB - valA;
        }

        return newOrder === 'asc' ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });

    rows.forEach(r => tbody.appendChild(r));
}

function sortRecommendationTable(tableType, colIndex) {
    const table = document.getElementById(`table-${tableType}`);
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const currentOrder = table.getAttribute('data-order') || 'asc';
    const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    table.setAttribute('data-order', newOrder);

    rows.sort((a, b) => {
        const cellA = a.children[colIndex].innerText;
        const cellB = b.children[colIndex].innerText;

        // Sort by change % (col 4)
        if (colIndex === 4) {
            const valA = parseFloat(a.children[colIndex].getAttribute('data-val'));
            const valB = parseFloat(b.children[colIndex].getAttribute('data-val'));
            return newOrder === 'asc' ? valA - valB : valB - valA;
        }

        // Sort by price (col 3) - extract number
        if (colIndex === 3) {
            const valA = parseFloat(cellA.replace(/,/g, ''));
            const valB = parseFloat(cellB.replace(/,/g, ''));
            return newOrder === 'asc' ? valA - valB : valB - valA;
        }

        return newOrder === 'asc' ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });

    rows.forEach(r => tbody.appendChild(r));
}

document.addEventListener('DOMContentLoaded', init);
