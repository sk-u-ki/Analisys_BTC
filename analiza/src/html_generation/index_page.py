def generate_html_content(overall_correlation, max_adoption, max_adoption_country, max_adoption_year, leader_2025, avg_growth, country_corr, period_corr, countries):
    colors = {
        'Ukraine': '#FF6B6B',
        'Poland': '#4ECDC4',
        'Czech': '#45B7D1',
        'Sweden': '#96CEB4',
        'Norway': '#FFEAA7',
        'Belarus': '#DDA0DD'
    }

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Анализ криптоадопции в Восточной Европе (2010-2025)</title>
        <link rel="stylesheet" href="../styles/main.css">
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏛️ Влияние доверия к государству на адопцию криптовалют</h1>
                <p>Сравнительный анализ стран Восточной Европы (2010-2025)</p>
                <div class="meta">
                    <div class="meta-item">📊 6 стран</div>
                    <div class="meta-item">📅 16 лет данных</div>
                    <div class="meta-item">🔢 96 наблюдений</div>
                    <div class="meta-item">📈 22 показателя</div>
                </div>
            </div>
            
            <div class="main-grid">
                <div class="card">
                    <h2>📊 Ключевые результаты</h2>
                    <div class="stats-grid">
                        <div class="stat-box">
                            <div class="stat-number">{overall_correlation:.3f}</div>
                            <div class="stat-label">Общая корреляция</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{max_adoption:.1f}%</div>
                            <div class="stat-label">Макс. адопция ({max_adoption_country}, {int(max_adoption_year)})</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{leader_2025}</div>
                            <div class="stat-label">Лидер 2025</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{avg_growth:.0f}%</div>
                            <div class="stat-label">Рост с 2010</div>
                        </div>
                    </div>
                    <div class="info-box">
                        <p><strong>💡 Что означает общая корреляция {overall_correlation:.3f}?</strong></p>
                        <p>Это средняя связь между инфляцией и криптоадопцией по всем странам и годам. 
                        Слабая корреляция показывает, что связь <strong>НЕ универсальна</strong> и зависит от страны, 
                        периода и политического режима. Это научно обоснованный результат!</p>
                    </div>
                </div>
                <div class="card">
                    <h2>📈 Интерактивные анализы</h2>
                    <div class="analysis-section">
                        <h4>🎯 Кластерный анализ стран</h4>
                        <img src="grafiki/cluster_preview.png" alt="Кластерный анализ">
                        <a href="grafiki/cluster_analysis.html" class="nav-button">🎯 Открыть интерактивную версию</a>
                    </div>
                    <div class="analysis-section">
                        <h4>📈 Регрессионный анализ</h4>
                        <img src="grafiki/regression_preview.png" alt="Регрессионный анализ">
                        <a href="grafiki/regression_trust_btc.html" class="nav-button">📈 Открыть интерактивную версию</a>
                    </div>
                </div>
            </div>
            <div class="countries-section">
                <h2>🎯 Корреляции по странам</h2>
                <ul class="correlation-list">
    """
    
    for country, corr in country_corr.items():
        color = colors.get(country, '#667eea')
        html_content += f"""
                    <li class="correlation-item" style="border-left-color: {color};">
                        <span><strong>{country}</strong></span>
                        <span style="color: {color}; font-weight: bold;">{corr}</span>
                    </li>
        """
    
    html_content += """
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def save_html_file(content, base_path):
    main_index_path = os.path.join(base_path, 'index.html')
    with open(main_index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Главная страница проекта создана: {main_index_path}")
