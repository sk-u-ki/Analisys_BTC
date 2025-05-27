
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

warnings.filterwarnings("ignore")




# ─────────────────────────────── ANALYSIS ────────────────────────────────

def comprehensive_analysis(df: pd.DataFrame, countries: Dict[str, Any], base: str):
    print("📊 Создание полного анализа…")
    df = optimize_int_columns(df)

    # — Корреляции
    num_cols = [c for c in df.columns if df[c].dtype != "object" and c not in ("Year",)]
    corr_matrix = df[num_cols].corr()

    country_corr = {}
    for c in df["Country"].unique():
        country_data = df[df["Country"] == c]
        country_name = countries[c]["name_ru"]
        corr = country_data["Inflation"].corr(country_data["Crypto_Adoption"])
        country_corr[country_name] = round(corr, 3)

    periods = {
        "До кризиса (2010-2019)": df[df["Year"] <= 2019],
        "Пандемия (2020-2021)": df[df["Year"].between(2020, 2021)],
        "Кризис (2022-2023)": df[df["Year"].between(2022, 2023)],
        "Восстановление (2024-2025)": df[df["Year"] >= 2024],
    }
    period_corr = {}
    for k, v in periods.items():
        if len(v) > 0:
            corr = v["Inflation"].corr(v["Crypto_Adoption"])
            period_corr[k] = round(corr, 3)

    # — Графики
    print("🎨 Создание графиков...")
    colors = {'Ukraine': 'red', 'Poland': 'orange', 'Czech': 'blue', 
              'Sweden': 'green', 'Norway': 'purple', 'Belarus': 'gray'}
    
    # График 1: Динамика криптоадопции
    plt.figure(figsize=(16, 10))
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        country_name = countries[country]['name_ru']
        plt.plot(country_data['Year'], country_data['Crypto_Adoption'], 
                marker='o', linewidth=3, label=country_name, color=colors[country])
    
    plt.axvline(x=2014, color='gray', linestyle='--', alpha=0.7)
    plt.text(2014.1, 8, 'Майдан\nУкраина', fontsize=10, alpha=0.8)
    plt.axvline(x=2020, color='gray', linestyle='--', alpha=0.7)
    plt.text(2020.1, 10, 'COVID-19\nПандемия', fontsize=10, alpha=0.8)
    plt.axvline(x=2022, color='red', linestyle='--', alpha=0.7)
    plt.text(2022.1, 11, 'Война\nВзрыв адопции', fontsize=10, color='red')
    
    plt.title('Динамика криптоадопции в Восточной Европе (2010-2025)', fontsize=16, fontweight='bold')
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Процент владельцев криптовалют (%)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(base, 'grafiki', '01_dinamika_kripto_2010_2025.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # График 2: Корреляция
    plt.figure(figsize=(12, 8))
    for country in df['Country'].unique():
        country_data = df[df['Country'] == country]
        country_name = countries[country]['name_ru']
        sizes = country_data['Currency_Volatility'] * 5
        plt.scatter(country_data['Inflation'], country_data['Crypto_Adoption'], 
                   s=sizes, alpha=0.7, label=country_name, color=colors[country])
    
    z = np.polyfit(df['Inflation'], df['Crypto_Adoption'], 1)
    p = np.poly1d(z)
    plt.plot(df['Inflation'], p(df['Inflation']), "r--", alpha=0.8, linewidth=2)
    
    correlation = df['Inflation'].corr(df['Crypto_Adoption'])
    plt.text(0.05, 0.95, f'Общая корреляция: {correlation:.3f}', 
             transform=plt.gca().transAxes, fontsize=14, fontweight='bold',
             bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.8))
    
    plt.title('Связь между инфляцией и криптоадопцией', fontsize=16, fontweight='bold')
    plt.xlabel('Уровень инфляции (%)', fontsize=12)
    plt.ylabel('Криптоадопция (%)', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(base, 'grafiki', '02_inflation_vs_crypto.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Графики созданы!")

    return corr_matrix, country_corr, period_corr
def trust_btc_analysis(df, countries, base):
    """Анализ корреляции между доверием к государству и адопцией BTC"""
    print("🔍 Анализ zaufanie vs adopcja BTC...")
    
    # Корреляции по странам
    trust_correlations = {}
    for country_code, country_info in countries.items():
        country_data = df[df['Country'] == country_code]
        country_name = country_info['name_ru']
        
        # Корреляция доверия и BTC (отрицательная = чем меньше доверия, тем больше BTC)
        trust_btc_corr = country_data['Government_Trust'].corr(country_data['Crypto_Adoption'])
        trust_correlations[country_name] = round(trust_btc_corr, 3)
    
    # Общая корреляция
    overall_trust_corr = df['Government_Trust'].corr(df['Crypto_Adoption'])
    
    # Создаем график корреляции доверие vs BTC
    fig_trust = go.Figure()
    
    colors = {'Ukraine': '#FF6B6B', 'Poland': '#4ECDC4', 'Czech': '#45B7D1', 
              'Sweden': '#96CEB4', 'Norway': '#FFEAA7', 'Belarus': '#DDA0DD'}
    
    for country_code, country_info in countries.items():
        country_data = df[df['Country'] == country_code]
        country_name = country_info['name_ru']
        
        fig_trust.add_trace(go.Scatter(
            x=country_data['Government_Trust'],
            y=country_data['Crypto_Adoption'],
            mode='markers',
            name=country_name,
            marker=dict(
                size=10,
                color=colors[country_code],
                opacity=0.7
            ),
            hovertemplate=f'<b>{country_name}</b><br>' +
                         'Zaufanie do państwa: %{x:.0f}%<br>' +
                         'Adopcja BTC: %{y:.1f}%<br>' +
                         'Rok: %{customdata}<br>' +
                         '<extra></extra>',
            customdata=country_data['Year']
        ))
    
    # Линия тренда
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(df['Government_Trust'], df['Crypto_Adoption'])
    line_x = [df['Government_Trust'].min(), df['Government_Trust'].max()]
    line_y = [slope * x + intercept for x in line_x]
    
    fig_trust.add_trace(go.Scatter(
        x=line_x,
        y=line_y,
        mode='lines',
        name=f'Trend (r={r_value:.3f})',
        line=dict(color='red', dash='dash', width=2)
    ))
    
    fig_trust.update_layout(
        title='Zależność między zaufaniem do państwa a adopcją BTC',
        xaxis_title='Zaufanie do państwa (%)',
        yaxis_title='Adopcja BTC (%)',
        template='plotly_white',
        width=1000,
        height=600
    )
    
    # Сохранение
    grafiki_path = os.path.join(base, 'grafiki')
    fig_trust.write_html(os.path.join(grafiki_path, 'trust_vs_btc.html'))
    
    # Сохранение результатов в Excel
    trust_analysis_path = os.path.join(base, 'otchety', 'trust_btc_analysis.xlsx')
    with pd.ExcelWriter(trust_analysis_path, engine='openpyxl') as writer:
        # Корреляции по странам
        trust_df = pd.DataFrame(list(trust_correlations.items()), 
                               columns=['Kraj', 'Korelacja_Zaufanie_BTC'])
        trust_df = trust_df.sort_values('Korelacja_Zaufanie_BTC')
        trust_df.to_excel(writer, sheet_name='Korelacje_Zaufanie_BTC', index=False)
        
        # Общие статистики
        stats_df = pd.DataFrame({
            'Wskaźnik': ['Ogólna korelacja zaufanie-BTC', 'R-squared', 'P-value'],
            'Wartość': [overall_trust_corr, r_value**2, p_value]
        })
        stats_df.to_excel(writer, sheet_name='Statystyki_Ogólne', index=False)
    
    print(f"✅ Analiza zaufanie vs BTC zakończona!")
    print(f"   📊 Ogólna korelacja: {overall_trust_corr:.3f}")
    print(f"   📈 R-squared: {r_value**2:.3f}")
    
    return trust_correlations, overall_trust_corr, fig_trust
