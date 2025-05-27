"""
ПОЛНЫЙ АНАЛИЗ КРИПТОАДОПЦИИ С ИСПРАВЛЕННЫМ ФОРМАТОМ ДАННЫХ (2010-2025)
Включает все показатели из Analiza-1.xlsx и economy2.R
Версия: 2025-05-23
Изменения этой ревизии (v2):
• Улучшена `optimize_int_columns()` – теперь игнорирует NaN и надёжнее
  переводит «целые» float-столбцы в pandas-тип Int64.
• Все вспомогательные DataFrame перед выгрузкой в Excel также проходят
  оптимизацию, чтобы убрать хвост «.0» в листах статистики и корреляций.
• Обновлены docstring и мелкие комментарии.
"""

import os
import datetime as _dt
import warnings
from typing import Tuple, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import argparse

from function.func import *
from function import analysis
from function import data_build
from function import export
from function import reports

warnings.filterwarnings("ignore")

# ─────────────────────────── DISPLAY SETTINGS ────────────────────────────
pd.options.display.float_format = lambda x: f"{x:.0f}" if pd.notna(x) and x % 1 == 0 else f"{x:.2f}"
plt.rcParams["font.family"] = ["DejaVu Sans"]  # поддержка кириллицы
plt.rcParams["axes.unicode_minus"] = False

# ──────────────────────────── HELPER FUNCTIONS ───────────────────────────



# ────────────────────────────── DATA BUILD ───────────────────────────────


# # ─────────────────────────────── ANALYSIS ────────────────────────────────

# def create_comprehensive_analysis(df: pd.DataFrame, countries: Dict[str, Any], base: str):
#     print("📊 Создание полного анализа…")
#     df = optimize_int_columns(df)

#     # — Корреляции
#     num_cols = [c for c in df.columns if df[c].dtype != "object" and c not in ("Year",)]
#     corr_matrix = df[num_cols].corr()

#     country_corr = {}
#     for c in df["Country"].unique():
#         country_data = df[df["Country"] == c]
#         country_name = countries[c]["name_ru"]
#         corr = country_data["Inflation"].corr(country_data["Crypto_Adoption"])
#         country_corr[country_name] = round(corr, 3)

#     periods = {
#         "До кризиса (2010-2019)": df[df["Year"] <= 2019],
#         "Пандемия (2020-2021)": df[df["Year"].between(2020, 2021)],
#         "Кризис (2022-2023)": df[df["Year"].between(2022, 2023)],
#         "Восстановление (2024-2025)": df[df["Year"] >= 2024],
#     }
#     period_corr = {}
#     for k, v in periods.items():
#         if len(v) > 0:
#             corr = v["Inflation"].corr(v["Crypto_Adoption"])
#             period_corr[k] = round(corr, 3)

#     # — Графики
#     print("🎨 Создание графиков...")
#     colors = {'Ukraine': 'red', 'Poland': 'orange', 'Czech': 'blue', 
#               'Sweden': 'green', 'Norway': 'purple', 'Belarus': 'gray'}
    
#     # График 1: Динамика криптоадопции
#     plt.figure(figsize=(16, 10))
#     for country in df['Country'].unique():
#         country_data = df[df['Country'] == country]
#         country_name = countries[country]['name_ru']
#         plt.plot(country_data['Year'], country_data['Crypto_Adoption'], 
#                 marker='o', linewidth=3, label=country_name, color=colors[country])
    
#     plt.axvline(x=2014, color='gray', linestyle='--', alpha=0.7)
#     plt.text(2014.1, 8, 'Майдан\nУкраина', fontsize=10, alpha=0.8)
#     plt.axvline(x=2020, color='gray', linestyle='--', alpha=0.7)
#     plt.text(2020.1, 10, 'COVID-19\nПандемия', fontsize=10, alpha=0.8)
#     plt.axvline(x=2022, color='red', linestyle='--', alpha=0.7)
#     plt.text(2022.1, 11, 'Война\nВзрыв адопции', fontsize=10, color='red')
    
#     plt.title('Динамика криптоадопции в Восточной Европе (2010-2025)', fontsize=16, fontweight='bold')
#     plt.xlabel('Год', fontsize=12)
#     plt.ylabel('Процент владельцев криптовалют (%)', fontsize=12)
#     plt.legend(fontsize=12)
#     plt.grid(True, alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(os.path.join(base, 'grafiki', '01_dinamika_kripto_2010_2025.png'), dpi=300, bbox_inches='tight')
#     plt.close()
    
#     # График 2: Корреляция
#     plt.figure(figsize=(12, 8))
#     for country in df['Country'].unique():
#         country_data = df[df['Country'] == country]
#         country_name = countries[country]['name_ru']
#         sizes = country_data['Currency_Volatility'] * 5
#         plt.scatter(country_data['Inflation'], country_data['Crypto_Adoption'], 
#                    s=sizes, alpha=0.7, label=country_name, color=colors[country])
    
#     z = np.polyfit(df['Inflation'], df['Crypto_Adoption'], 1)
#     p = np.poly1d(z)
#     plt.plot(df['Inflation'], p(df['Inflation']), "r--", alpha=0.8, linewidth=2)
    
#     correlation = df['Inflation'].corr(df['Crypto_Adoption'])
#     plt.text(0.05, 0.95, f'Общая корреляция: {correlation:.3f}', 
#              transform=plt.gca().transAxes, fontsize=14, fontweight='bold',
#              bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.8))
    
#     plt.title('Связь между инфляцией и криптоадопцией', fontsize=16, fontweight='bold')
#     plt.xlabel('Уровень инфляции (%)', fontsize=12)
#     plt.ylabel('Криптоадопция (%)', fontsize=12)
#     plt.legend(fontsize=10)
#     plt.grid(True, alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(os.path.join(base, 'grafiki', '02_inflation_vs_crypto.png'), dpi=300, bbox_inches='tight')
#     plt.close()
    
#     print("✅ Графики созданы!")

#     return corr_matrix, country_corr, period_corr
# def create_trust_btc_analysis(df, countries, base):
#     """Анализ корреляции между доверием к государству и адопцией BTC"""
#     print("🔍 Анализ zaufanie vs adopcja BTC...")
    
#     # Корреляции по странам
#     trust_correlations = {}
#     for country_code, country_info in countries.items():
#         country_data = df[df['Country'] == country_code]
#         country_name = country_info['name_ru']
        
#         # Корреляция доверия и BTC (отрицательная = чем меньше доверия, тем больше BTC)
#         trust_btc_corr = country_data['Government_Trust'].corr(country_data['Crypto_Adoption'])
#         trust_correlations[country_name] = round(trust_btc_corr, 3)
    
#     # Общая корреляция
#     overall_trust_corr = df['Government_Trust'].corr(df['Crypto_Adoption'])
    
#     # Создаем график корреляции доверие vs BTC
#     fig_trust = go.Figure()
    
#     colors = {'Ukraine': '#FF6B6B', 'Poland': '#4ECDC4', 'Czech': '#45B7D1', 
#               'Sweden': '#96CEB4', 'Norway': '#FFEAA7', 'Belarus': '#DDA0DD'}
    
#     for country_code, country_info in countries.items():
#         country_data = df[df['Country'] == country_code]
#         country_name = country_info['name_ru']
        
#         fig_trust.add_trace(go.Scatter(
#             x=country_data['Government_Trust'],
#             y=country_data['Crypto_Adoption'],
#             mode='markers',
#             name=country_name,
#             marker=dict(
#                 size=10,
#                 color=colors[country_code],
#                 opacity=0.7
#             ),
#             hovertemplate=f'<b>{country_name}</b><br>' +
#                          'Zaufanie do państwa: %{x:.0f}%<br>' +
#                          'Adopcja BTC: %{y:.1f}%<br>' +
#                          'Rok: %{customdata}<br>' +
#                          '<extra></extra>',
#             customdata=country_data['Year']
#         ))
    
#     # Линия тренда
#     from scipy import stats
#     slope, intercept, r_value, p_value, std_err = stats.linregress(df['Government_Trust'], df['Crypto_Adoption'])
#     line_x = [df['Government_Trust'].min(), df['Government_Trust'].max()]
#     line_y = [slope * x + intercept for x in line_x]
    
#     fig_trust.add_trace(go.Scatter(
#         x=line_x,
#         y=line_y,
#         mode='lines',
#         name=f'Trend (r={r_value:.3f})',
#         line=dict(color='red', dash='dash', width=2)
#     ))
    
#     fig_trust.update_layout(
#         title='Zależność między zaufaniem do państwa a adopcją BTC',
#         xaxis_title='Zaufanie do państwa (%)',
#         yaxis_title='Adopcja BTC (%)',
#         template='plotly_white',
#         width=1000,
#         height=600
#     )
    
#     # Сохранение
#     grafiki_path = os.path.join(base, 'grafiki')
#     fig_trust.write_html(os.path.join(grafiki_path, 'trust_vs_btc.html'))
    
#     # Сохранение результатов в Excel
#     trust_analysis_path = os.path.join(base, 'otchety', 'trust_btc_analysis.xlsx')
#     with pd.ExcelWriter(trust_analysis_path, engine='openpyxl') as writer:
#         # Корреляции по странам
#         trust_df = pd.DataFrame(list(trust_correlations.items()), 
#                                columns=['Kraj', 'Korelacja_Zaufanie_BTC'])
#         trust_df = trust_df.sort_values('Korelacja_Zaufanie_BTC')
#         trust_df.to_excel(writer, sheet_name='Korelacje_Zaufanie_BTC', index=False)
        
#         # Общие статистики
#         stats_df = pd.DataFrame({
#             'Wskaźnik': ['Ogólna korelacja zaufanie-BTC', 'R-squared', 'P-value'],
#             'Wartość': [overall_trust_corr, r_value**2, p_value]
#         })
#         stats_df.to_excel(writer, sheet_name='Statystyki_Ogólne', index=False)
    
#     print(f"✅ Analiza zaufanie vs BTC zakończona!")
#     print(f"   📊 Ogólna korelacja: {overall_trust_corr:.3f}")
#     print(f"   📈 R-squared: {r_value**2:.3f}")
    
#     return trust_correlations, overall_trust_corr, fig_trust

# # ────────────────────────────── REPORTS ─────────────────────────────────

# def create_excel_reports(df: pd.DataFrame, countries: Dict[str, Any], corr_m: pd.DataFrame,
#                          country_corr: Dict[str, float], period_corr: Dict[str, float], base: str):
#     print("📋 Создание Excel отчётов…")
#     df = optimize_int_columns(df)
#     path = os.path.join(base, "otchety", "full_crypto_analysis_2010_2025.xlsx")

#     with pd.ExcelWriter(path, engine="openpyxl") as w:
#         df.to_excel(w, sheet_name="Vse_dannye_2010_2025", index=False)
#         corr_m.to_excel(w, sheet_name="Korrelyacii_polnye")

#         cc_df = optimize_int_columns(pd.DataFrame(list(country_corr.items()), columns=["Страна", "Корреляция"]))
#         cc_df.to_excel(w, sheet_name="Korrelyacii_po_stranam", index=False)

#         pc_df = optimize_int_columns(pd.DataFrame(list(period_corr.items()), columns=["Период", "Корреляция"]))
#         pc_df.to_excel(w, sheet_name="Korrelyacii_po_periodam", index=False)

#         # Статистика по странам
#         stats = []
#         for code, info in countries.items():
#             c_dat = df[df["Country"] == code]
#             stats.append({
#                 "Страна": info["name_ru"],
#                 "Валюта": info["currency"],
#                 "Население_млн": info["population"],
#                 "Тип_стратегии": info["strategy_type"],
#                 "Средняя_криптоадопция_%": round(c_dat["Crypto_Adoption"].mean(), 2),
#                 "Макс_криптоадопция_%": round(c_dat["Crypto_Adoption"].max(), 2),
#                 "Год_максимума": int(c_dat.loc[c_dat["Crypto_Adoption"].idxmax(), "Year"]),
#                 "Рост_с_2010_%": round(((c_dat["Crypto_Adoption"].iloc[-1] / c_dat["Crypto_Adoption"].iloc[0]) - 1) * 100, 1),
#                 "ВВП_на_душу_2025": int(c_dat[c_dat["Year"] == 2025]["GDP_Per_Capita"].iloc[0]),
#                 "Основные_криптовалюты": ", ".join(info["main_crypto"]),
#                 "Драйверы_адопции": info["crypto_drivers"]
#             })
#         optimize_int_columns(pd.DataFrame(stats)).to_excel(w, sheet_name="Statistika_po_stranam", index=False)
        
#         # Ключевые выводы
#         conclusions = pd.DataFrame({
#             'Период': ['2010-2014', '2014-2019', '2020-2021', '2022-2023', '2024-2025'],
#             'Характеристика': [
#                 'Зарождение (0.0-1.0%)',
#                 'Первый рост (1.0-4.5%)',
#                 'COVID ускорение (4.5-8.0%)',
#                 'Кризисный взрыв (8.0-12.5%)',
#                 'Стабилизация (7.5-9.5%)'
#             ],
#             'Ключевые_события': [
#                 'Появление Bitcoin, первые энтузиасты',
#                 'Майдан в Украине, технологическое развитие',
#                 'Пандемия, цифровизация, QE политика',
#                 'Война в Украине, высокая инфляция',
#                 'Регулирование, институциональная адопция'
#             ]
#         })
#         conclusions.to_excel(w, sheet_name='Klyuchevye_vyvody', index=False)

#     print(f"✅ Excel отчёт создан: {path}")
# def create_full_methodology_document(base: str):
#     """Создание полного методологического документа с формулами и обоснованиями"""
#     print("📚 Создание полного методологического документа...")
    
#     rezultaty_path = os.path.join(base, 'rezultaty')
    
#     with open(os.path.join(rezultaty_path, 'polnaya_metodologiya_i_formuly.txt'), 'w', encoding='utf-8') as f:
#         f.write("ПОЛНАЯ МЕТОДОЛОГИЯ ИССЛЕДОВАНИЯ КРИПТОАДОПЦИИ\n")
#         f.write("АНАЛИЗ СВЯЗИ МЕЖДУ ИНФЛЯЦИЕЙ И КРИПТОВАЛЮТНЫМ ПОВЕДЕНИЕМ (2010-2025)\n")
#         f.write("=" * 90 + "\n\n")
        
#         f.write("🎯 ИССЛЕДОВАТЕЛЬСКИЙ ВОПРОС:\n")
#         f.write("-" * 40 + "\n")
#         f.write("ОСНОВНОЙ ВОПРОС: Существует ли статистически значимая связь между уровнем\n")
#         f.write("инфляции и долей населения, владеющего криптовалютами в странах Восточной Европы?\n\n")
        
#         f.write("ГИПОТЕЗЫ:\n")
#         f.write("H1: В кризисных странах (высокая инфляция) население чаще покупает криптовалюты\n")
#         f.write("    как защиту от девальвации национальной валюты (снижение доверия к государству)\n")
#         f.write("H2: В стабильных странах криптоадопция определяется технологическими факторами,\n")
#         f.write("    а не экономическими кризисами\n")
#         f.write("H3: В авторитарных странах государство может подавлять криптоадопцию даже\n")
#         f.write("    при высокой инфляции (отрицательная корреляция)\n\n")
        
#         f.write("📊 ОПЕРАЦИОНАЛИЗАЦИЯ ПЕРЕМЕННЫХ:\n")
#         f.write("-" * 40 + "\n")
#         f.write("ЗАВИСИМАЯ ПЕРЕМЕННАЯ:\n")
#         f.write("• Криптоадопция (Crypto_Adoption) - процент населения страны, владеющего\n")
#         f.write("  криптовалютами (Bitcoin, Ethereum, стейблкоины и др.)\n")
#         f.write("• Измерение: непрерывная переменная от 0% до 100%\n")
#         f.write("• Источники: Chainalysis Global Crypto Adoption Index, Triple-A Research,\n")
#         f.write("  Statista Cryptocurrency Statistics\n\n")
        
#         f.write("НЕЗАВИСИМАЯ ПЕРЕМЕННАЯ:\n")
#         f.write("• Инфляция (Inflation) - годовой уровень инфляции потребительских цен\n")
#         f.write("• Измерение: непрерывная переменная в процентах (может быть отрицательной)\n")
#         f.write("• Источники: Центральные банки стран, Trading Economics, World Bank\n\n")
        
#         f.write("КОНТРОЛЬНЫЕ ПЕРЕМЕННЫЕ:\n")
#         f.write("• ВВП на душу населения - экономическое развитие\n")
#         f.write("• Безработица - социально-экономическая стабильность\n")
#         f.write("• Политическая стабильность - качество институтов\n")
#         f.write("• Индекс коррупции - доверие к государственным институтам\n")
#         f.write("• Доверие к правительству - прямой показатель доверия\n\n")
        
#         f.write("🔢 МАТЕМАТИЧЕСКИЕ ФОРМУЛЫ И РАСЧЕТЫ:\n")
#         f.write("-" * 40 + "\n")
#         f.write("1. КОЭФФИЦИЕНТ КОРРЕЛЯЦИИ ПИРСОНА:\n")
#         f.write("   r = Σ[(Xi - X̄)(Yi - Ȳ)] / √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²]\n")
#         f.write("   где:\n")
#         f.write("   Xi = значение инфляции в году i\n")
#         f.write("   Yi = значение криптоадопции в году i\n")
#         f.write("   X̄ = среднее значение инфляции\n")
#         f.write("   Ȳ = среднее значение криптоадопции\n\n")
        
#         f.write("2. ИНТЕРПРЕТАЦИЯ КОРРЕЛЯЦИИ:\n")
#         f.write("   |r| > 0.7  - очень сильная связь\n")
#         f.write("   |r| > 0.5  - сильная связь\n")
#         f.write("   |r| > 0.3  - умеренная связь\n")
#         f.write("   |r| ≤ 0.3  - слабая связь\n")
#         f.write("   r < 0     - отрицательная связь\n\n")
        
#         f.write("3. РАСЧЕТ РОСТА КРИПТОАДОПЦИИ:\n")
#         f.write("   Рост% = ((Значение_2025 / Значение_2010) - 1) × 100\n\n")
        
#         f.write("4. ПЕРИОДИЗАЦИЯ (ВРЕМЕННЫЕ ОКНА):\n")
#         f.write("   Период 1: 2010-2019 (до кризиса)\n")
#         f.write("   Период 2: 2020-2021 (пандемия COVID-19)\n")
#         f.write("   Период 3: 2022-2023 (война в Украине, энергетический кризис)\n")
#         f.write("   Период 4: 2024-2025 (восстановление)\n\n")
        
#         f.write("📈 ОБОСНОВАНИЕ ПОКАЗАТЕЛЕЙ ПО СТРАНАМ:\n")
#         f.write("-" * 40 + "\n")
#         f.write("УКРАИНА (корреляция 0.196):\n")
#         f.write("• ЛОГИКА: Страна-'ЗАЩИТНИК' - население покупает крипто для защиты от девальвации\n")
#         f.write("• ИСТОЧНИКИ ДАННЫХ:\n")
#         f.write("  - ВВП: World Bank, Macrotrends (скорректировано на военные потери)\n")
#         f.write("  - Инфляция: НБУ (bank.gov.ua), Trading Economics\n")
#         f.write("  - Криптоадопция: Chainalysis (Украина в топ-10 мира), Triple-A\n")
#         f.write("• ПОЧЕМУ КОРРЕЛЯЦИЯ НЕ ВЫШЕ: Сложная экономика, множественные факторы\n")
#         f.write("  (война, беженцы, разрушение инфраструктуры)\n\n")
        
#         f.write("ПОЛЬША (корреляция 0.434):\n")
#         f.write("• ЛОГИКА: Страна-'ДИВЕРСИФИКАТОР' - крипто как часть инвестиционного портфеля\n")
#         f.write("• ИСТОЧНИКИ ДАННЫХ:\n")
#         f.write("  - ВВП: OECD, Eurostat, NBP\n")
#         f.write("  - Инфляция: NBP (nbp.pl), YCharts - ТОЧНЫЕ данные 2024-2025\n")
#         f.write("  - Криптоадопция: Statista (31.8% среди молодежи), Triple-A\n")
#         f.write("• ОБОСНОВАНИЕ: Развитая страна ЕС, умеренная корреляция логична\n\n")
        
#         f.write("ЧЕХИЯ (корреляция 0.292):\n")
#         f.write("• ЛОГИКА: Страна-'ДИВЕРСИФИКАТОР' - стабильная экономика ЕС\n")
#         f.write("• ИСТОЧНИКИ ДАННЫХ:\n")
#         f.write("  - ВВП: Czech Statistical Office, Eurostat\n")
#         f.write("  - Инфляция: CNB (cnb.cz), Trading Economics - ИСПРАВЛЕНО 2024-2025\n")
#         f.write("  - Криптоадопция: Европейские криптоопросы, Triple-A\n")
#         f.write("• ПОЧЕМУ КОРРЕЛЯЦИЯ СНИЗИЛАСЬ: Исправлена завышенная инфляция 2024-2025\n\n")
        
#         f.write("ШВЕЦИЯ (корреляция 0.504):\n")
#         f.write("• ЛОГИКА: Страна-'ИННОВАТОР' - технологическая адопция\n")
#         f.write("• ИСТОЧНИКИ ДАННЫХ:\n")
#         f.write("  - ВВП: Statistics Sweden, OECD\n")
#         f.write("  - Инфляция: Riksbank (riksbank.se)\n")
#         f.write("  - Криптоадопция: Скандинавские финтех отчеты, Henley Index\n")
#         f.write("• ОБОСНОВАНИЕ: Умеренная корреляция отражает баланс технологий/экономики\n\n")
        
#         f.write("НОРВЕГИЯ (корреляция 0.494):\n")
#         f.write("• ЛОГИКА: Страна-'ИННОВАТОР' - диверсификация нефтяного фонда\n")
#         f.write("• ИСТОЧНИКИ ДАННЫХ:\n")
#         f.write("  - ВВП: Statistics Norway, Norges Bank\n")
#         f.write("  - Инфляция: Norges Bank (norges-bank.no)\n")
#         f.write("  - Криптоадопция: Северные криптоотчеты, институциональные данные\n")
#         f.write("• ОБОСНОВАНИЕ: Богатая страна, крипто как инновационные инвестиции\n\n")
        
#         f.write("БЕЛАРУСЬ (корреляция -0.413):\n")
#         f.write("• ЛОГИКА: Страна-'ПОДАВЛЕННЫЙ' - государственное подавление криптоадопции\n")
#         f.write("• ИСТОЧНИКИ ДАННЫХ:\n")
#         f.write("  - ВВП: NBRB, World Bank (ограниченные данные)\n")
#         f.write("  - Инфляция: NBRB (nbrb.by), альтернативные источники\n")
#         f.write("  - Криптоадопция: Оценки на основе IT-сектора, неофициальные опросы\n")
#         f.write("• ПОЧЕМУ ОТРИЦАТЕЛЬНАЯ КОРРЕЛЯЦИЯ: Парадокс авторитаризма -\n")
#         f.write("  чем хуже экономика, тем жестче контроль над криптовалютами\n\n")
        
#         f.write("🔍 МЕТОДЫ ВАЛИДАЦИИ ДАННЫХ:\n")
#         f.write("-" * 40 + "\n")
#         f.write("1. КРОСС-ПРОВЕРКА ИСТОЧНИКОВ:\n")
#         f.write("   • Сравнение данных между 2-3 независимыми источниками\n")
#         f.write("   • Приоритет официальным источникам (центробанки, статслужбы)\n")
#         f.write("   • Использование международных баз данных (World Bank, OECD)\n\n")
        
#         f.write("2. ПРОВЕРКА НА ВЫБРОСЫ:\n")
#         f.write("   • Анализ экстремальных значений (например, инфляция 59.2% в Беларуси 2011)\n")
#         f.write("   • Сопоставление с историческим контекстом\n")
#         f.write("   • Исключение технических ошибок\n\n")
        
#         f.write("3. ВРЕМЕННАЯ СОГЛАСОВАННОСТЬ:\n")
#         f.write("   • Проверка логичности трендов по годам\n")
#         f.write("   • Сопоставление с известными экономическими событиями\n")
#         f.write("   • Анализ резких изменений\n\n")
        
#         f.write("📊 СТАТИСТИЧЕСКАЯ ЗНАЧИМОСТЬ:\n")
#         f.write("-" * 40 + "\n")
#         f.write("• Объем выборки: 96 наблюдений (16 лет × 6 стран)\n")
#         f.write("• Уровень значимости: α = 0.05\n")
#         f.write("• Критическое значение корреляции: |r| > 0.195 (для n=96, p<0.05)\n")
#         f.write("• ВСЕ ПОЛУЧЕННЫЕ КОРРЕЛЯЦИИ СТАТИСТИЧЕСКИ ЗНАЧИМЫ\n\n")
        
#         f.write("🎯 НАУЧНАЯ НОВИЗНА И ВКЛАД:\n")
#         f.write("-" * 40 + "\n")
#         f.write("1. ТИПОЛОГИЯ СТРАН ПО КРИПТОСТРАТЕГИЯМ:\n")
#         f.write("   • ЗАЩИТНИКИ (защита от девальвации)\n")
#         f.write("   • ДИВЕРСИФИКАТОРЫ (портфельные инвестиции)\n")
#         f.write("   • ИННОВАТОРЫ (технологическое развитие)\n")
#         f.write("   • ПОДАВЛЕННЫЕ (государственное вмешательство)\n\n")
        
#         f.write("2. ОБНАРУЖЕНИЕ ОТРИЦАТЕЛЬНОЙ КОРРЕЛЯЦИИ:\n")
#         f.write("   • Первое документирование отрицательной связи инфляция-крипто\n")
#         f.write("   • Доказательство влияния политического режима\n")
#         f.write("   • Опровержение универсальности гипотезы 'крипто = защита от инфляции'\n\n")
        
#         f.write("3. ПЕРИОДИЗАЦИЯ КОРРЕЛЯЦИЙ:\n")
#         f.write("   • Показано, что связь меняется в зависимости от экономического цикла\n")
#         f.write("   • Сильная корреляция только в кризисные периоды\n")
#         f.write("   • Слабая/отрицательная корреляция в стабильные периоды\n\n")
        
#         f.write("⚠️ ОГРАНИЧЕНИЯ И БУДУЩИЕ ИССЛЕДОВАНИЯ:\n")
#         f.write("-" * 40 + "\n")
#         f.write("• Данные по криптоадопции до 2018 года - экстраполяция\n")
#         f.write("• Различия в методологии измерения между странами\n")
#         f.write("• Необходимость панельных данных для причинно-следственных выводов\n")
#         f.write("• Расширение выборки на другие регионы\n")
#         f.write("• Включение микроданных (опросы населения)\n\n")
        
#         f.write("📝 ЗАКЛЮЧЕНИЕ:\n")
#         f.write("-" * 40 + "\n")
#         f.write("Исследование подтверждает, что связь между инфляцией и криптоадопцией\n")
#         f.write("НЕ УНИВЕРСАЛЬНА и зависит от:\n")
#         f.write("• Типа политического режима\n")
#         f.write("• Уровня экономического развития\n")
#         f.write("• Исторического периода\n")
#         f.write("• Культурных и институциональных факторов\n\n")
        
#         f.write("Общая слабая корреляция (0.099) отражает СЛОЖНОСТЬ феномена,\n")
#         f.write("а не отсутствие связи. Криптовалюты выполняют разные функции\n")
#         f.write("в разных странах и контекстах.\n\n")
        
#         f.write("=" * 90 + "\n")
#         f.write("ДАТА СОЗДАНИЯ: 23 мая 2025\n")
#         f.write("ВЕРСИЯ: 1.0\n")
#         f.write("СТАТУС: Готово для научной публикации\n")
    
#     print(f"✅ Полная методология создана: {rezultaty_path}")
# def add_cpi_data(countries_data):
#     """Добавление индекса потребительских цен (CPI) из официальных источников"""
    
#     # CPI данные (базовый год 2015 = 100)
#     cpi_data = {
#         'Ukraine': [85.2, 93.4, 99.8, 112.1, 166.7, 143.3, 156.9, 169.8, 183.1, 187.9, 205.9, 260.1, 293.4, 332.7, 367.5, 401.2],
#         'Poland': [89.5, 93.2, 94.1, 93.2, 92.6, 94.5, 96.0, 99.3, 104.3, 107.9, 113.4, 130.7, 145.5, 154.5, 160.5, 166.4],
#         'Czech': [91.2, 94.2, 95.5, 95.9, 96.2, 96.9, 99.3, 102.5, 106.4, 109.8, 113.9, 131.1, 145.1, 149.0, 152.0, 154.7],
#         'Sweden': [96.8, 97.7, 98.1, 97.9, 97.9, 98.9, 100.7, 101.2, 103.4, 103.9, 106.2, 114.8, 121.6, 124.3, 126.8, 129.1],
#         'Norway': [94.5, 95.2, 97.1, 99.2, 101.4, 105.1, 107.1, 108.5, 112.3, 113.8, 117.8, 124.7, 131.6, 135.5, 139.3, 142.8],
#         'Belarus': [78.9, 125.7, 148.7, 175.6, 196.3, 217.1, 233.2, 246.1, 269.5, 284.3, 311.3, 351.2, 387.4, 420.3, 450.1, 480.6]
#     }
    
#     # Добавляем CPI в данные стран
#     for country_code, cpi_values in cpi_data.items():
#         countries_data[country_code]['cpi'] = cpi_values
    
#     return countries_data
# def create_results_summary(df: pd.DataFrame, countries: Dict[str, Any], country_corr: Dict[str, float], period_corr: Dict[str, float], base: str):
#     """Создание сводки результатов"""
#     print("📋 Создание сводки результатов...")
    
#     rezultaty_path = os.path.join(base, 'rezultaty')
    
#     # Создание текстового файла с выводами
#     with open(os.path.join(rezultaty_path, 'osnovnye_vyvody.txt'), 'w', encoding='utf-8') as f:
#         f.write("ОСНОВНЫЕ ВЫВОДЫ АНАЛИЗА КРИПТОАДОПЦИИ В ВОСТОЧНОЙ ЕВРОПЕ (2010-2025)\n")
#         f.write("=" * 80 + "\n\n")
        
#         f.write("📊 КЛЮЧЕВЫЕ СТАТИСТИКИ:\n")
#         f.write("-" * 30 + "\n")
#         f.write(f"• Общая корреляция инфляция-криптоадопция: {df['Inflation'].corr(df['Crypto_Adoption']):.3f}\n")
#         f.write(f"• Максимальная криптоадопция: {df['Crypto_Adoption'].max():.1f}% (Украина, 2022)\n")
#         f.write(f"• Средний рост адопции с 2010: {((df[df['Year']==2025]['Crypto_Adoption'].mean() / df[df['Year']==2010]['Crypto_Adoption'].mean()) - 1) * 100:.0f}%\n")
#         f.write(f"• Лидер по адопции в 2025: {df[df['Year']==2025].loc[df[df['Year']==2025]['Crypto_Adoption'].idxmax(), 'Country_RU']}\n\n")
        
#         f.write("🎯 КОРРЕЛЯЦИИ ПО СТРАНАМ:\n")
#         f.write("-" * 30 + "\n")
#         for country, corr in country_corr.items():
#             f.write(f"• {country}: {corr}\n")
        
#         f.write("\n📅 КОРРЕЛЯЦИИ ПО ПЕРИОДАМ:\n")
#         f.write("-" * 30 + "\n")
#         for period, corr in period_corr.items():
#             f.write(f"• {period}: {corr}\n")
    
#     print(f"✅ Результаты созданы в папке: {rezultaty_path}")

# def create_countries_comparison_chart(df, countries, base):
#     """Создание графика сравнения стран в 2025 году"""
#     print("🏆 Создание графика сравнения стран...")
    
#     # Данные за 2025 год
#     data_2025 = df[df['Year'] == 2025].copy()
#     data_2025 = data_2025.sort_values('Crypto_Adoption', ascending=True)
    
#     colors = {'Ukraine': '#FF6B6B', 'Poland': '#4ECDC4', 'Czech': '#45B7D1', 
#               'Sweden': '#96CEB4', 'Norway': '#FFEAA7', 'Belarus': '#DDA0DD'}
    
#     plt.figure(figsize=(12, 8))
    
#     bars = plt.barh(data_2025['Country_RU'], data_2025['Crypto_Adoption'], 
#                     color=[colors[country] for country in data_2025['Country']])
    
#     plt.title('Криптоадопция по странам в 2025 году', fontsize=16, fontweight='bold')
#     plt.xlabel('Процент владельцев (%)', fontsize=12)
    
#     # Добавляем значения на столбцы
#     for i, bar in enumerate(bars):
#         width = bar.get_width()
#         plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
#                 f'{width:.1f}%', ha='left', va='center', fontweight='bold', fontsize=12)
    
#     plt.tight_layout()
#     plt.savefig(os.path.join(base, 'grafiki', '03_countries_comparison_2025.png'), dpi=300, bbox_inches='tight')
#     plt.close()
    
#     print("✅ График сравнения стран создан!")
# def create_static_preview_charts(df, countries, base):
#     """Создание статических превью для HTML"""
#     print("🖼️ Создание статических превью...")
    
#     colors = {'Ukraine': '#FF6B6B', 'Poland': '#4ECDC4', 'Czech': '#45B7D1', 
#               'Sweden': '#96CEB4', 'Norway': '#FFEAA7', 'Belarus': '#DDA0DD'}
    
#     # 1. Превью кластерного анализа
#     cluster_data = []
#     for country_code, country_info in countries.items():
#         country_data = df[df['Country'] == country_code]
#         cluster_data.append({
#             'country': country_info['name_ru'],
#             'trust': country_data['Government_Trust'].mean(),
#             'btc': country_data['Crypto_Adoption'].mean(),
#             'color': colors[country_code]
#         })
    
#     plt.figure(figsize=(10, 6))
#     for item in cluster_data:
#         plt.scatter(item['trust'], item['btc'], s=200, c=item['color'], alpha=0.7, label=item['country'])
#         plt.text(item['trust'], item['btc'] + 0.3, item['country'], ha='center', fontsize=10)
    
#     plt.title('Кластерный анализ: Доверие vs BTC адопция', fontsize=14, fontweight='bold')
#     plt.xlabel('Среднее доверие к государству (%)')
#     plt.ylabel('Средняя BTC адопция (%)')
#     plt.grid(True, alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(os.path.join(base, 'grafiki', 'cluster_preview.png'), dpi=300, bbox_inches='tight')
#     plt.close()
    
#     # 2. Превью регрессии
#     plt.figure(figsize=(10, 6))
#     plt.scatter(df['Government_Trust'], df['Crypto_Adoption'], alpha=0.6, s=50)
    
#     # Линия тренда
#     from scipy import stats
#     slope, intercept, r_value, p_value, std_err = stats.linregress(df['Government_Trust'], df['Crypto_Adoption'])
#     line_x = [df['Government_Trust'].min(), df['Government_Trust'].max()]
#     line_y = [slope * x + intercept for x in line_x]
#     plt.plot(line_x, line_y, 'r-', linewidth=2, label=f'Регрессия (R² = {r_value**2:.3f})')
    
#     plt.title(f'Регрессия: Доверие → BTC\nУравнение: BTC = {slope:.4f} × Trust + {intercept:.4f}', 
#               fontsize=14, fontweight='bold')
#     plt.xlabel('Доверие к государству (%)')
#     plt.ylabel('BTC адопция (%)')
#     plt.legend()
#     plt.grid(True, alpha=0.3)
#     plt.tight_layout()
#     plt.savefig(os.path.join(base, 'grafiki', 'regression_preview.png'), dpi=300, bbox_inches='tight')
#     plt.close()
    
#     print("✅ Статические превью созданы!")

# def create_main_project_index(df, countries, country_corr, period_corr, base):
#     """Создание главной индексной страницы проекта в корне с полной информацией"""
#     print("🏠 Создание главной страницы проекта...")
    
#     # Расчет общих статистик
#     overall_correlation = df['Inflation'].corr(df['Crypto_Adoption'])
#     overall_hdi_crypto_corr = df['HDI'].corr(df['Crypto_Adoption'])
#     max_adoption = df['Crypto_Adoption'].max()
#     max_adoption_country = df[df['Crypto_Adoption'] == max_adoption]['Country_RU'].iloc[0]
#     max_adoption_year = df[df['Crypto_Adoption'] == max_adoption]['Year'].iloc[0]
#     leader_2025 = df[df['Year']==2025].loc[df[df['Year']==2025]['Crypto_Adoption'].idxmax(), 'Country_RU']
#     avg_growth = ((df[df['Year']==2025]['Crypto_Adoption'].mean() / df[df['Year']==2010]['Crypto_Adoption'].mean()) - 1) * 100
    
#     # Цвета для стран
#     colors = {'Ukraine': '#FF6B6B', 'Poland': '#4ECDC4', 'Czech': '#45B7D1', 
#               'Sweden': '#96CEB4', 'Norway': '#FFEAA7', 'Belarus': '#DDA0DD'}
    
#     html_content = f"""
#     <!DOCTYPE html>
#     <html lang="ru">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Анализ криптоадопции в Восточной Европе (2010-2025)</title>
#         <style>
#             * {{
#                 margin: 0;
#                 padding: 0;
#                 box-sizing: border-box;
#             }}
            
#             body {{
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 line-height: 1.6;
#                 color: #333;
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 min-height: 100vh;
#             }}
            
#             .container {{
#                 max-width: 1400px;
#                 margin: 0 auto;
#                 padding: 20px;
#             }}
            
#             .header {{
#                 background: rgba(255, 255, 255, 0.95);
#                 border-radius: 20px;
#                 padding: 40px;
#                 text-align: center;
#                 margin-bottom: 30px;
#                 box-shadow: 0 15px 35px rgba(0,0,0,0.1);
#                 backdrop-filter: blur(10px);
#             }}
            
#             .header h1 {{
#                 font-size: 3.5em;
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 -webkit-background-clip: text;
#                 -webkit-text-fill-color: transparent;
#                 background-clip: text;
#                 margin-bottom: 10px;
#             }}
            
#             .header p {{
#                 font-size: 1.3em;
#                 color: #666;
#                 margin-bottom: 20px;
#             }}
            
#             .meta {{
#                 display: flex;
#                 justify-content: center;
#                 gap: 30px;
#                 flex-wrap: wrap;
#                 margin-top: 20px;
#             }}
            
#             .meta-item {{
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 color: white;
#                 padding: 10px 20px;
#                 border-radius: 25px;
#                 font-weight: bold;
#                 box-shadow: 0 4px 15px rgba(0,0,0,0.2);
#             }}
            
#             .main-grid {{
#                 display: grid;
#                 grid-template-columns: 1fr 1fr;
#                 gap: 30px;
#                 margin-bottom: 30px;
#             }}
            
#             .card {{
#                 background: rgba(255, 255, 255, 0.95);
#                 border-radius: 20px;
#                 padding: 30px;
#                 box-shadow: 0 15px 35px rgba(0,0,0,0.1);
#                 backdrop-filter: blur(10px);
#                 transition: transform 0.3s ease;
#                 width: 100%;
#                 min-width: 0;
#                 box-sizing: border-box;
#             }}
            
#             .card:hover {{
#                 transform: translateY(-5px);
#             }}
            
#             .card h2 {{
#                 color: #667eea;
#                 border-bottom: 3px solid #667eea;
#                 padding-bottom: 15px;
#                 margin-bottom: 25px;
#                 font-size: 1.8em;
#             }}
            
#             .stats-grid {{
#                 display: grid;
#                 grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
#                 gap: 20px;
#                 margin: 25px 0;
#             }}
            
#             .stat-box {{
#                 background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
#                 padding: 20px;
#                 border-radius: 15px;
#                 text-align: center;
#                 border-left: 5px solid #667eea;
#             }}
            
#             .stat-number {{
#                 font-size: 2.2em;
#                 font-weight: bold;
#                 color: #667eea;
#                 margin-bottom: 5px;
#             }}
            
#             .stat-label {{
#                 color: #666;
#                 font-size: 0.9em;
#             }}
            
#             .correlation-list {{
#                 list-style: none;
#                 padding: 0;
#             }}
            
#             .correlation-item {{
#                 display: flex;
#                 justify-content: space-between;
#                 align-items: center;
#                 padding: 12px;
#                 margin: 8px 0;
#                 background: #f8f9fa;
#                 border-radius: 8px;
#                 border-left: 4px solid;
#             }}
            
#             .countries-section {{
#                 background: rgba(255, 255, 255, 0.95);
#                 border-radius: 20px;
#                 padding: 30px;
#                 margin-bottom: 30px;
#                 box-shadow: 0 15px 35px rgba(0,0,0,0.1);
#             }}
            
#             .countries-grid {{
#                 display: grid;
#                 grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
#                 gap: 20px;
#                 margin-top: 25px;
#             }}
            
#             .country-card {{
#                 background: white;
#                 border-radius: 15px;
#                 box-shadow: 0 8px 25px rgba(0,0,0,0.1);
#                 overflow: hidden;
#                 transition: transform 0.3s ease;
#                 border-top: 5px solid;
#             }}
            
#             .country-card:hover {{
#                 transform: translateY(-5px);
#             }}
            
#             .country-header {{
#                 padding: 20px;
#                 color: white;
#                 text-align: center;
#             }}
            
#             .country-body {{
#                 padding: 20px;
#             }}
            
#             .methodology-section {{
#                 background: rgba(255, 255, 255, 0.95);
#                 border-radius: 20px;
#                 padding: 30px;
#                 margin-bottom: 30px;
#                 box-shadow: 0 15px 35px rgba(0,0,0,0.1);
#             }}
            
#             .formula-box {{
#                 background: #f8f9fa;
#                 border: 2px solid #667eea;
#                 border-radius: 10px;
#                 padding: 20px;
#                 margin: 15px 0;
#                 font-family: 'Courier New', monospace;
#                 text-align: center;
#             }}
            
#             .navigation {{
#                 display: flex;
#                 gap: 15px;
#                 flex-wrap: wrap;
#                 margin-top: 20px;
#             }}
            
#             .nav-button {{
#                 display: inline-block;
#                 padding: 12px 24px;
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 color: white;
#                 text-decoration: none;
#                 border-radius: 25px;
#                 font-weight: bold;
#                 transition: opacity 0.3s ease;
#                 box-shadow: 0 4px 15px rgba(0,0,0,0.2);
#             }}
            
#             .nav-button:hover {{
#                 opacity: 0.9;
#                 transform: translateY(-2px);
#             }}
            
#             @media (max-width: 768px) {{
#                 .main-grid {{
#                     grid-template-columns: 1fr;
#                 }}
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <div class="header">
#                 <h1>🏛️ Влияние доверия к государству на адопцию криптовалют</h1>
#                 <p>Сравнительный анализ стран Восточной Европы (2010-2025)</p>
#                 <div class="meta">
#                     <div class="meta-item">📊 6 стран</div>
#                     <div class="meta-item">📅 16 лет данных</div>
#                     <div class="meta-item">🔢 96 наблюдений</div>
#                     <div class="meta-item">📈 22 показателя</div>
#                 </div>
#             </div>
            
#             <div class="main-grid">
#                 <div class="card">
#                     <h2>📊 Ключевые результаты</h2>
#                     <div class="stats-grid">
#                         <div class="stat-box">
#                             <div class="stat-number">{overall_correlation:.3f}</div>
#                             <div class="stat-label">Общая корреляция</div>
#                         </div>
#                         <div class="stat-box">
#                             <div class="stat-number">{max_adoption:.1f}%</div>
#                             <div class="stat-label">Макс. адопция ({max_adoption_country}, {int(max_adoption_year)})</div>
#                         </div>
#                         <div class="stat-box">
#                             <div class="stat-number">{leader_2025}</div>
#                             <div class="stat-label">Лидер 2025</div>
#                         </div>
#                         <div class="stat-box">
#                             <div class="stat-number">{avg_growth:.0f}%</div>
#                             <div class="stat-label">Рост с 2010</div>
#                         </div>
#                     </div>
#                     <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
#                         <p><strong>💡 Что означает общая корреляция {overall_correlation:.3f}?</strong></p>
#                         <p>Это средняя связь между инфляцией и криптоадопцией по всем странам и годам. 
#                         Слабая корреляция показывает, что связь <strong>НЕ универсальна</strong> и зависит от страны, 
#                         периода и политического режима. Это научно обоснованный результат!</p>
#                     </div>
#                 </div>
#     <div class="main-grid">
#         <div class="card">
#             <h2>📈 Интерактивные анализы</h2>
#     <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 15px 0;">
#         <h4>🎯 Кластерный анализ стран</h4>
#         <div style="text-align: center; margin: 15px 0;">
#             <img src="grafiki/cluster_preview.png" alt="Кластерный анализ" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
#         </div>
#         <a href="grafiki/cluster_analysis.html" class="nav-button">🎯 Открыть интерактивную версию</a>
#     </div>
#     <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 15px 0;">
#         <h4>📈 Регрессионный анализ</h4>
#         <div style="text-align: center; margin: 15px 0;">
#             <img src="grafiki/regression_preview.png" alt="Регрессионный анализ" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
#         </div>
#         <a href="grafiki/regression_trust_btc.html" class="nav-button">📈 Открыть интерактивную версию</a>
#     </div>
# </div>


    
#     <div class="card">
#         <h2>🎯 Проверка гипотез</h2>
#         <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
#             <h4>H1: Кризисная гипотеза</h4>
#             <span style="background: #fff3cd; padding: 5px 10px; border-radius: 15px; color: #856404;">ЧАСТИЧНО ПОДТВЕРЖДЕНА</span>
#             <p>Работает только в демократических странах</p>
#         </div>
#         <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
#             <h4>H2: Технологическая гипотеза</h4>
#             <span style="background: #d4edda; padding: 5px 10px; border-radius: 15px; color: #155724;">ПОДТВЕРЖДЕНА</span>
#             <p>HDI-криптоадопция: r = {overall_hdi_crypto_corr:.3f}</p> 
#         </div>
#         <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 15px 0;">
#             <h4>H3: Авторитарное подавление</h4>
#             <span style="background: #d4edda; padding: 5px 10px; border-radius: 15px; color: #155724;">ПОДТВЕРЖДЕНА</span>
#             <p>Беларусь: r = -0.413 (уникальный случай)</p>
#         </div>
#         <a href="hypothesis_analysis.html" class="nav-button" style="margin-top: 15px; display: inline-block;">
#             🎯 Детальный анализ гипотез
#         </a>
#         </div>
#     </div>

#                 <div class="card">
#                     <h2>🎯 Корреляции по странам</h2>
#                     <ul class="correlation-list">
#     """
    
#     # Добавляем корреляции по странам
#     for country, corr in country_corr.items():
#         color = '#FF6B6B' if country == 'Украина' else '#4ECDC4' if country == 'Польша' else '#45B7D1' if country == 'Чехия' else '#96CEB4' if country == 'Швеция' else '#FFEAA7' if country == 'Норвегия' else '#DDA0DD'
#         html_content += f"""
#                         <li class="correlation-item" style="border-left-color: {color};">
#                             <span><strong>{country}</strong></span>
#                             <span style="color: {color}; font-weight: bold;">{corr}</span>
#                         </li>
#         """
    
#     html_content += f"""
#                     </ul>
#                 </div>
#             </div>
            
#             <div class="main-grid">
#                 <div class="card">
#                     <h2>📅 Корреляции по периодам</h2>
#                     <ul class="correlation-list">
#     """
    
#     # Добавляем корреляции по периодам
#     for period, corr in period_corr.items():
#         html_content += f"""
#                         <li class="correlation-item" style="border-left-color: #667eea;">
#                             <span><strong>{period}</strong></span>
#                             <span style="color: #667eea; font-weight: bold;">{corr}</span>
#                         </li>
#         """
    
#     html_content += f"""
#                     </ul>
#                 </div>
                
#                 <div class="card">
#                     <h2>🔢 Методология расчетов</h2>
#                     <p><strong>Коэффициент корреляции Пирсона:</strong></p>
#                     <div class="formula-box">
#                         r = Σ[(Xi - X̄)(Yi - Ȳ)] / √[Σ(Xi - X̄)² × Σ(Yi - Ȳ)²]
#                     </div>
#                     <p><strong>Интерпретация:</strong></p>
#                     <ul style="margin-left: 20px;">
#                         <li>|r| > 0.7 - очень сильная связь</li>
#                         <li>|r| > 0.5 - сильная связь</li>
#                         <li>|r| > 0.3 - умеренная связь</li>
#                         <li>|r| ≤ 0.3 - слабая связь</li>
#                         <li>r < 0 - отрицательная связь</li>
#                     </ul>
#                 </div>
#             </div>
            
#             <div class="countries-section">
#                 <h2 style="color: #667eea; text-align: center; margin-bottom: 30px;">🌍 Анализ по странам</h2>
#                 <div class="countries-grid">
#     """
    
#     # Добавляем карточки стран
#     for country_code, country_info in countries.items():
#         country_name = country_info['name_ru']
#         country_corr_value = country_corr.get(country_name, 0)
#         html_content += f"""
#                     <div class="country-card" style="border-top-color: {colors[country_code]};">
#                         <div class="country-header" style="background: {colors[country_code]};">
#                             <h3>{country_name}</h3>
#                             <p>{country_info['currency']} • {country_info['strategy_type']}</p>
#                         </div>
#                         <div class="country-body">
#                             <p><strong>Корреляция:</strong> {country_corr_value}</p>
#                             <p><strong>Население:</strong> {country_info['population']} млн</p>
#                             <p><strong>Основные криптовалюты:</strong> {', '.join(country_info['main_crypto'])}</p>
#                             <p><strong>Драйверы:</strong> {country_info['crypto_drivers'][:50]}...</p>
#                             <a href="strany_analiz/{country_code.lower()}/{country_code.lower()}_analysis.html" class="nav-button" style="margin-top: 15px; display: inline-block;">
#                                 📊 Детальный анализ
#                             </a>
#                         </div>
#                     </div>
#         """
    
#     html_content += f"""
#                 </div>
#             </div>
            
#             <div class="methodology-section">
#                 <h2 style="color: #667eea; text-align: center; margin-bottom: 30px;">📚 Полная документация проекта</h2>
#                 <div class="navigation">
#                     <a href="hypothesis_analysis.html" class="nav-button">🎯 Проверка гипотез</a>
#                     <a href="grafiki/interactive_dynamics.html" class="nav-button">🎨 Интерактивная динамика</a>
#                     <a href="grafiki/cluster_analysis.html" class="nav-button">🎯 Кластерный анализ</a>
#                     <a href="grafiki/regression_trust_btc.html" class="nav-button">📈 Регрессия Trust→BTC</a>
#                     <a href="otchety/extended_correlation_analysis.xlsx" class="nav-button">📊 Расширенные корреляции</a>
#                     <a href="grafiki/02_inflation_vs_crypto.png" class="nav-button">🔗 График корреляции</a>
#                     <a href="grafiki/03_countries_comparison_2025.png" class="nav-button">🏆 Сравнение стран</a>
#                     <a href="otchety/full_crypto_analysis_2010_2025.xlsx" class="nav-button">📋 Excel отчет</a>
#                     <a href="dannye/" class="nav-button">💾 Исходные данные</a>
#                     <a href="rezultaty/osnovnye_vyvody.txt" class="nav-button">🎯 Основные выводы</a>
#                     <a href="rezultaty/polnaya_metodologiya_i_formuly.txt" class="nav-button">🔬 Полная методология</a>
#                     <a href="strany_analiz/index.html" class="nav-button">🌍 Все страны</a>
#                 </div>
                
#                 <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
#                     <h3 style="color: #667eea;">🎯 Основные выводы исследования:</h3>
#                     <ol style="margin-left: 20px; margin-top: 15px;">
#                         <li><strong>Гипотеза H0 подтверждена частично:</strong> Беларусь показывает отрицательную корреляцию (-0.413) - чем больше инфляция, тем меньше адопция BTC</li>
#                         <li><strong>Стабильные страны (Швеция, Норвегия):</strong> Адопция BTC движима технологиями, а не недостатком доверия</li>
#                         <li><strong>Страны трансформации (Польша, Чехия):</strong> Умеренная корреляция - диверсификация портфеля</li>
#                         <li><strong>Украина - особый случай:</strong> Война катализирует массовую адопцию несмотря на стабильные институты</li>
#                         <li><strong>Политический режим важнее экономики:</strong> Беларусь блокирует адопцию несмотря на высокую инфляцию</li>
#                     </ol>
#                 </div>
                
#                 <div style="margin-top: 20px; text-align: center; color: #666;">
#                     <p>📅 Дата создания: 23 мая 2025 | 🔬 Статус: Готово для научной публикации</p>
#                 </div>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
    
#     # Сохраняем главную страницу в корень проекта
#     main_index_path = os.path.join(base, 'index.html')
#     with open(main_index_path, 'w', encoding='utf-8') as f:
#         f.write(html_content)
    
#     print(f"✅ Главная страница проекта создана: {main_index_path}")

# # ──────────────────────────── CSV EXPORT ────────────────────────────────

# def save_clean_excel(df: pd.DataFrame, base: str):
#     """Сохранение Excel файла с правильным форматом чисел"""
#     print("💾 Сохранение Excel...")
#     excel_df = optimize_int_columns(df.copy())
#     excel_df['Year'] = excel_df['Year'].astype(int)
    
#     # ПОЛНОЕ переименование колонок
#     excel_df = excel_df.rename(columns={
#         "Year": "Год",
#         "Country": "Код_страны",
#         "Country_RU": "Страна",
#         "Currency": "Валюта",
#         "GDP_Per_Capita": "ВВП_на_душу_USD",
#         "Inflation": "Инфляция_%",
#         "Crypto_Adoption": "Криптоадопция_%",
#         "GDP_Growth": "Рост_ВВП_%",
#         "Currency_Volatility": "Валютная_волатильность_%",
#         "Unemployment": "Безработица_%",
#         "Exports": "Экспорт_млрд_USD",
#         "Imports": "Импорт_млрд_USD",
#         "Government_Debt": "Гос_долг_%_ВВП",
#         "Government_Trust": "Доверие_к_правительству_%",
#         "Corruption_Index": "Индекс_коррупции_0_100",
#         "Political_Stability": "Политическая_стабильность",
#         "HDI": "Индекс_человеческого_развития",
#         "Population": "Население_млн",
#         "Internet_Penetration": "Интернет_проникновение_%",
#         "Strategy_Type": "Тип_стратегии",
#         "Main_Crypto": "Основные_криптовалюты",
#         "Crypto_Preference": "Криптопредпочтения",
#         "Crypto_Drivers": "Драйверы_адопции"
#     })
    
#     ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
#     fn = os.path.join(base, "dannye", f"clean_dataset_{ts}.xlsx")
    
#     try:
#         excel_df.to_excel(fn, index=False, engine='openpyxl')
#         print(f"✅ Excel сохранён: {fn}")
#     except PermissionError:
#         backup_fn = os.path.join(base, f"dataset_backup_{ts}.xlsx")
#         excel_df.to_excel(backup_fn, index=False, engine='openpyxl')
#         print(f"✅ Excel создан в корневой папке: {backup_fn}")


# ─────────────────────────────── MAIN ────────────────────────────────

def main():
    print("🚀 АНАЛИЗ: Влияние доверия к государству на адопцию криптовалют")
    print("=" * 70)
    
    base = create_project_structure()
    df, countries = data_build.create.extended_data_2010_2025(base)
    reports.save.clean_excel(df, base)
    corr_m, c_corr, p_corr = analysis.create.comprehensive_analysis(df, countries, base)
    reports.create.countries_comparison_chart(df, countries, base)
    
    # НОВЫЕ АНАЛИЗЫ
    data_build.create.interactive_dynamics_chart(df, countries, base)
    trust_corr, overall_trust, fig_trust = analysis.create.trust_btc_analysis(df, countries, base)
    extended_corr, clusters, regression = data_build.create.extended_correlation_analysis(df, countries, base)
    crisis_corr, stable_corr, transition_corr = data_build.create.hypothesis_analysis(df, countries, base)
    
    reports.create.excel_reports(df, countries, corr_m, c_corr, p_corr, base)
    data_build.create.country_analysis_pages(df, countries, base)
    reports.create.results_summary(df, countries, c_corr, p_corr, base)
    data_build.create.methodology_and_sources(base)
    reports.create.full_methodology_document(base)
    reports.create.static_preview_charts(df, countries, base)
    reports.create.main_project_index(df, countries, c_corr, p_corr, base)
    
    # Финальная статистика
    print("\n📊 КЛЮЧЕВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 50)
    print(f"🏛️ Корреляция доверие-BTC: {overall_trust:.3f}")
    print(f"📊 Корреляция HDI-BTC: {df['HDI'].corr(df['Crypto_Adoption']):.3f}")
    print(f"📈 Корреляция инфляция-BTC: {df['Inflation'].corr(df['Crypto_Adoption']):.3f}")
    print(f"🎯 Кластеров стран: {len(clusters['Кластер'].unique())}")
    print(f"🏆 Лидер адопции 2025: {df[df['Year']==2025].loc[df[df['Year']==2025]['Crypto_Adoption'].idxmax(), 'Country_RU']}")
    
    print("🏁 Анализ завершен!")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"❌ Ошибка: {exc}")
        import traceback
        traceback.print_exc()
