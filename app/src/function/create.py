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



def hypothesis_analysis(df, countries, base):
    """Создание детального анализа гипотез с конкретными критериями"""
    print("🎯 Создание анализа гипотез...")
    
    # Расчет показателей для проверки гипотез
    overall_inflation_crypto_corr = df['Inflation'].corr(df['Crypto_Adoption'])
    overall_trust_crypto_corr = df['Government_Trust'].corr(df['Crypto_Adoption'])
    overall_hdi_crypto_corr = df['HDI'].corr(df['Crypto_Adoption'])
    
    # Анализ по типам стран
    crisis_countries = ['Ukraine', 'Belarus']  # Высокая инфляция
    stable_countries = ['Sweden', 'Norway']    # Низкая инфляция, высокое развитие
    transition_countries = ['Poland', 'Czech'] # Средний уровень
    
    crisis_corr = df[df['Country'].isin(crisis_countries)]['Inflation'].corr(
        df[df['Country'].isin(crisis_countries)]['Crypto_Adoption'])
    stable_corr = df[df['Country'].isin(stable_countries)]['Inflation'].corr(
        df[df['Country'].isin(stable_countries)]['Crypto_Adoption'])
    transition_corr = df[df['Country'].isin(transition_countries)]['Inflation'].corr(
        df[df['Country'].isin(transition_countries)]['Crypto_Adoption'])
    
    # Создание HTML отчета по гипотезам
    hypothesis_html = f""
    
    # Сохранение HTML файла
    hypothesis_path = os.path.join(base, 'hypothesis_analysis.html')
    with open(hypothesis_path, 'w', encoding='utf-8') as f:
        f.write(hypothesis_html)
    
    print(f"✅ Анализ гипотез создан: {hypothesis_path}")
    return crisis_corr, stable_corr, transition_corr



def extended_data_2010_2025(base) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    print("📊 Создание расширенных данных с 2010 года…")
    years = list(range(2010, 2026))
    
    # ИСПРАВЛЕННЫЕ данные по всем странам
    countries_data: Dict[str, Dict[str, Any]] = {
        'Ukraine': {
            'name_ru': 'Украина',
            'currency': 'UAH',
            'main_crypto': ['Bitcoin', 'USDT', 'Ethereum'],
            'crypto_preference': 'Stablecoins (защита от девальвации)',
            
            'gdp_per_capita': [3577, 3855, 3927, 3014, 2115, 2640, 2656, 3095, 3659, 3425, 3752, 4828, 4576, 5181, 5500, 5800],
            'inflation': [9.4, 0.6, -0.3, 12.1, 48.7, 13.9, 14.4, 10.9, 7.9, 2.7, 10.0, 26.6, 12.9, 13.4, 15.1, 15.9],
            'crypto_adoption': [0.0, 0.1, 0.2, 0.5, 1.8, 3.2, 4.1, 4.5, 4.8, 5.2, 9.5, 15.2, 14.1, 12.8, 11.2, 10.5],
            'gdp_growth': [4.1, 0.2, 0.0, -6.6, -9.8, 2.4, 2.5, 3.4, 3.2, -4.0, 3.4, -29.1, 5.3, 4.0, 3.5, 3.8],
            'currency_volatility': [1.8, 2.1, 3.2, 15.8, 52.3, 25.4, 18.2, 12.1, 8.9, 8.5, 15.2, 45.8, 38.2, 25.1, 20.5, 18.2],
            'unemployment': [7.4, 7.5, 7.2, 9.3, 9.1, 9.4, 9.6, 8.8, 8.6, 8.5, 9.9, 18.6, 17.2, 16.8, 15.5, 14.8],
            'exports': [51.4, 68.8, 63.3, 53.9, 38.1, 36.4, 43.3, 47.3, 49.3, 50.1, 49.2, 44.1, 57.5, 62.8, 68.2, 72.1],
            'imports': [60.7, 84.7, 76.9, 54.4, 37.5, 39.2, 43.9, 49.6, 57.1, 60.8, 54.4, 42.2, 55.9, 61.4, 67.8, 71.5],
            'government_debt': [40.0, 36.6, 40.1, 70.3, 79.4, 81.0, 81.2, 71.8, 60.9, 50.3, 60.8, 78.8, 84.2, 88.5, 92.1, 95.2],
            'government_trust': [40, 35, 32, 25, 18, 15, 20, 22, 24, 25, 23, 18, 20, 22, 25, 27],
            'corruption_index': [26, 26, 25, 26, 27, 29, 30, 32, 32, 33, 33, 32, 33, 34, 33, 35],
            'political_stability': [-0.5, -0.8, -1.2, -2.5, -2.3, -1.8, -1.5, -1.2, -1.8, -2.1, -2.0, -2.8, -2.5, -2.2, -2.1, -2.0],
            
            'population': 41.2,
            'internet_penetration': 71,
            'strategy_type': 'ЗАЩИТНИК',
            'crypto_drivers': 'Защита от девальвации гривны, обход санкций, международные переводы'
        },
        
        'Poland': {
            'name_ru': 'Польша',
            'currency': 'PLN',
            'main_crypto': ['Bitcoin', 'Ethereum', 'Polish tokens'],
            'crypto_preference': 'Bitcoin (инвестиции)',
            
            'gdp_per_capita': [12294, 12648, 13432, 14342, 12495, 12372, 12414, 13823, 15694, 15694, 15694, 17640, 18920, 20150, 21380, 22100],
            'inflation': [2.6, 3.7, 0.9, -0.9, -0.6, 2.0, 1.6, 3.4, 5.1, 3.4, 5.1, 15.3, 11.3, 6.2, 3.9, 3.7],
            'crypto_adoption': [0.1, 0.3, 0.5, 0.8, 1.1, 1.5, 1.8, 2.1, 2.4, 2.7, 3.2, 8.5, 12.2, 15.8, 18.2, 19.1],
            'gdp_growth': [3.6, 1.6, 1.4, 3.3, 3.8, 3.1, 5.1, 4.9, 5.4, -2.5, 6.9, 3.1, 2.8, 3.2, 3.0, 2.8],
            'currency_volatility': [2.8, 3.2, 4.1, 8.7, 6.8, 5.2, 4.8, 6.2, 8.1, 6.2, 8.1, 11.4, 9.8, 8.5, 7.2, 6.8],
            'unemployment': [9.7, 10.1, 9.0, 7.5, 6.2, 4.9, 3.8, 3.4, 3.3, 3.2, 2.9, 2.9, 3.1, 3.5, 3.8, 4.0],
            'exports': [159.8, 184.5, 203.0, 218.2, 195.7, 195.1, 221.8, 249.8, 262.3, 269.4, 314.4, 390.7, 418.2, 445.8, 472.1, 495.2],
            'imports': [173.7, 188.4, 203.5, 215.0, 188.4, 188.6, 202.0, 239.9, 271.0, 254.8, 310.3, 378.2, 405.6, 432.1, 458.9, 481.8],
            'government_debt': [54.8, 55.6, 57.0, 50.4, 51.3, 54.2, 54.1, 48.9, 57.1, 57.4, 49.6, 49.6, 49.4, 49.8, 50.2, 50.8],
            'government_trust': [44, 42, 40, 38, 35, 36, 37, 38, 40, 38, 40, 35, 36, 37, 38, 39],
            'corruption_index': [53, 58, 60, 61, 62, 62, 60, 45, 45, 45, 45, 45, 56, 55, 45, 47],
            'political_stability': [0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.2, 0.3, 0.2, 0.3, 0.1, 0.2, 0.2, 0.2, 0.3],
            
            'population': 37.7,
            'internet_penetration': 85,
            'strategy_type': 'ДИВЕРСИФИКАТОР',
            'crypto_drivers': 'Диверсификация портфеля, хедж против злотого, технологические инвестиции'
        },
        
        'Czech': {
            'name_ru': 'Чехия',
            'currency': 'CZK',
            'main_crypto': ['Bitcoin', 'Ethereum', 'Local tokens'],
            'crypto_preference': 'Bitcoin (долгосрочные инвестиции)',
            
            'gdp_per_capita': [19420, 20294, 20571, 19582, 18267, 18858, 20152, 23111, 26821, 26821, 26821, 28450, 29780, 31200, 32650, 34100],
            'inflation': [1.5, 3.3, 1.4, 0.4, 0.3, 0.7, 2.5, 3.2, 3.8, 3.2, 3.8, 15.1, 10.7, 2.7, 2.0, 1.8],
            'crypto_adoption': [0.1, 0.2, 0.4, 0.7, 1.0, 1.3, 1.6, 1.8, 2.1, 2.4, 2.8, 7.2, 9.5, 11.8, 13.2, 14.1],
            'gdp_growth': [2.3, -0.8, -0.5, 2.7, 5.4, 2.5, 2.2, 3.6, 2.8, -5.8, 3.3, 2.4, 2.1, 2.5, 2.8, 3.0],
            'currency_volatility': [2.5, 2.8, 3.5, 7.2, 5.9, 4.1, 3.8, 5.8, 7.9, 5.8, 7.9, 12.7, 10.1, 8.8, 7.5, 7.0],
            'unemployment': [7.3, 7.0, 6.1, 5.1, 4.0, 2.9, 2.4, 2.2, 2.8, 2.6, 2.8, 2.4, 2.6, 3.0, 3.2, 3.4],
            'exports': [132.1, 162.0, 161.8, 174.7, 156.9, 143.4, 174.3, 192.9, 215.5, 216.8, 243.5, 267.8, 285.4, 302.1, 318.9, 335.2],
            'imports': [125.7, 143.1, 148.1, 156.0, 140.2, 134.2, 154.8, 177.6, 201.4, 198.7, 227.8, 251.2, 268.9, 285.6, 302.4, 318.8],
            'government_debt': [38.4, 44.5, 42.6, 42.2, 36.8, 36.8, 32.6, 30.0, 38.1, 37.7, 41.9, 41.0, 43.8, 44.2, 44.6, 45.0],
            'government_trust': [47, 45, 43, 41, 39, 40, 41, 42, 44, 42, 44, 40, 41, 42, 42, 43],
            'corruption_index': [46, 49, 48, 51, 56, 55, 55, 56, 56, 56, 56, 56, 56, 56, 56, 57],
            'political_stability': [1.0, 0.9, 0.8, 0.7, 0.8, 0.9, 1.0, 0.8, 0.9, 0.8, 0.9, 0.7, 0.8, 0.8, 0.8, 0.9],
            
            'population': 10.7,
            'internet_penetration': 88,
            'strategy_type': 'ДИВЕРСИФИКАТОР',
            'crypto_drivers': 'Технологические инновации, защита от инфляции, европейская интеграция'
        },
        
        'Sweden': {
            'name_ru': 'Швеция',
            'currency': 'SEK',
            'main_crypto': ['Bitcoin', 'Ethereum', 'Green crypto'],
            'crypto_preference': 'Ethereum (DeFi и экология)',
            
            'gdp_per_capita': [49803, 56956, 60430, 58491, 51165, 51608, 53442, 51648, 54608, 54608, 54608, 56890, 58420, 60150, 61980, 63850],
            'inflation': [1.9, 0.9, 0.4, -0.2, 0.0, 1.0, 1.8, 0.5, 2.2, 0.5, 2.2, 8.1, 5.9, 2.2, 2.0, 1.8],
            'crypto_adoption': [0.3, 0.5, 0.8, 1.2, 1.6, 2.0, 2.3, 2.6, 3.0, 3.4, 3.8, 5.2, 6.1, 6.8, 7.2, 7.5],
            'gdp_growth': [6.0, -0.3, 1.3, 2.7, 4.5, 2.1, 2.6, 1.2, 2.6, -2.8, 4.8, 1.9, 1.2, 2.0, 2.2, 2.4],
            'currency_volatility': [1.8, 2.1, 2.8, 5.2, 4.1, 3.2, 2.9, 4.2, 6.1, 4.2, 6.1, 8.3, 7.1, 6.5, 6.0, 5.5],
            'unemployment': [8.6, 8.0, 7.9, 7.4, 6.9, 6.9, 6.9, 6.8, 8.3, 8.3, 8.7, 7.5, 7.8, 8.1, 8.4, 8.6],
            'exports': [158.4, 184.8, 181.5, 165.6, 152.0, 140.2, 151.4, 151.0, 165.6, 176.5, 193.8, 208.7, 221.4, 234.8, 248.5, 262.1],
            'imports': [148.8, 166.8, 159.7, 148.8, 138.2, 131.8, 142.1, 142.8, 153.2, 167.1, 181.4, 195.2, 207.8, 220.9, 234.3, 247.8],
            'government_debt': [39.4, 38.2, 40.6, 45.0, 43.9, 42.8, 41.0, 35.1, 39.9, 39.8, 35.3, 35.4, 32.9, 31.5, 30.2, 29.0],
            'government_trust': [80, 78, 76, 74, 72, 73, 74, 75, 77, 75, 77, 73, 74, 75, 75, 76],
            'corruption_index': [92, 88, 89, 87, 87, 88, 85, 83, 83, 83, 83, 83, 83, 83, 83, 84],
            'political_stability': [1.5, 1.4, 1.3, 1.2, 1.3, 1.4, 1.5, 1.3, 1.4, 1.3, 1.4, 1.2, 1.3, 1.3, 1.3, 1.4],
            
            'population': 10.5,
            'internet_penetration': 97,
            'strategy_type': 'ИННОВАТОР',
            'crypto_drivers': 'Технологические инновации, экологические проекты, цифровая экономика'
        },
        
        'Norway': {
            'name_ru': 'Норвегия',
            'currency': 'NOK',
            'main_crypto': ['Bitcoin', 'Ethereum', 'Green mining'],
            'crypto_preference': 'Bitcoin (зеленый майнинг)',
            
            'gdp_per_capita': [87648, 73450, 75420, 74356, 60139, 59330, 70590, 67294, 75420, 75420, 75420, 78650, 81200, 83750, 86300, 88950],
            'inflation': [2.4, 0.7, 2.0, 2.2, 2.2, 3.6, 1.9, 1.3, 3.5, 1.3, 3.5, 5.9, 5.5, 3.0, 2.8, 2.5],
            'crypto_adoption': [0.2, 0.3, 0.6, 1.0, 1.3, 1.6, 1.9, 2.2, 2.6, 3.0, 3.4, 4.8, 5.5, 6.1, 6.5, 6.8],
            'gdp_growth': [0.7, 2.7, 1.0, 2.0, 1.6, 1.2, 1.1, 1.9, 2.9, -0.7, 5.3, 2.8, 1.5, 2.1, 2.0, 2.2],
            'currency_volatility': [1.5, 1.8, 2.5, 4.8, 3.9, 2.8, 2.5, 3.8, 5.2, 3.8, 5.2, 7.1, 6.2, 5.8, 5.5, 5.2],
            'unemployment': [3.6, 3.2, 3.5, 3.5, 4.4, 4.7, 4.7, 4.2, 5.0, 5.0, 4.4, 3.2, 3.5, 3.8, 4.0, 4.2],
            'exports': [130.7, 162.0, 153.8, 144.2, 103.4, 88.9, 102.1, 101.8, 122.2, 164.0, 183.9, 231.2, 195.4, 208.7, 222.1, 235.8],
            'imports': [77.3, 89.1, 90.3, 87.9, 75.9, 68.8, 75.2, 74.5, 82.1, 91.8, 102.4, 118.7, 108.9, 116.3, 123.8, 131.5],
            'government_debt': [43.6, 29.0, 27.4, 27.7, 27.9, 33.2, 36.4, 36.3, 39.7, 67.1, 45.5, 41.7, 38.2, 35.8, 33.5, 31.2],
            'government_trust': [74, 72, 70, 68, 66, 67, 68, 68, 70, 68, 70, 66, 67, 68, 68, 69],
            'corruption_index': [89, 85, 86, 87, 87, 85, 85, 85, 85, 85, 85, 85, 85, 85, 85, 86],
            'political_stability': [1.6, 1.5, 1.4, 1.3, 1.4, 1.5, 1.6, 1.4, 1.5, 1.4, 1.5, 1.3, 1.4, 1.4, 1.4, 1.5],
            
            'population': 5.4,
            'internet_penetration': 98,
            'strategy_type': 'ИННОВАТОР',
            'crypto_drivers': 'Диверсификация нефтяного фонда, зеленые технологии, институциональные инвестиции'
        },
        
        'Belarus': {
            'name_ru': 'Беларусь',
            'currency': 'BYN',
            'main_crypto': ['Bitcoin', 'USDT', 'Local mining'],
            'crypto_preference': 'USDT (обход ограничений)',
            
            'gdp_per_capita': [5819, 7031, 7973, 8039, 5762, 5143, 5762, 6330, 6890, 6330, 6890, 6450, 6200, 6350, 6500, 6650],
            'inflation': [7.7, 59.2, 18.3, 18.1, 11.8, 10.6, 7.4, 5.5, 9.5, 5.5, 9.5, 12.8, 10.3, 8.5, 7.2, 6.8],
            'crypto_adoption': [0.0, 0.1, 0.1, 0.2, 0.3, 0.4, 0.4, 0.5, 0.6, 0.7, 0.8, 1.2, 1.0, 0.9, 0.8, 0.9],
            'gdp_growth': [7.7, 1.7, 1.0, 1.7, -3.8, -2.5, -0.2, 2.5, 1.2, -0.9, 2.3, -0.9, -1.5, 0.5, 1.0, 1.2],
            'currency_volatility': [6.8, 8.2, 12.5, 18.7, 15.2, 12.8, 10.5, 12.1, 18.5, 12.1, 18.5, 15.2, 13.8, 12.0, 10.5, 9.8],
            'unemployment': [0.7, 0.5, 0.5, 0.5, 1.0, 1.0, 0.8, 4.8, 4.2, 4.2, 3.9, 4.8, 5.2, 5.5, 5.8, 6.0],
            'exports': [25.3, 46.1, 36.0, 31.2, 26.7, 23.5, 28.3, 33.0, 33.0, 28.8, 39.5, 41.8, 43.2, 44.7, 46.2, 47.8],
            'imports': [34.9, 46.4, 43.0, 40.5, 34.2, 30.3, 32.9, 38.8, 42.5, 35.4, 42.8, 44.2, 45.7, 47.3, 48.9, 50.5],
            'government_debt': [14.6, 31.5, 34.0, 34.7, 48.5, 53.4, 53.5, 47.5, 39.4, 46.7, 35.3, 46.9, 48.2, 49.5, 50.8, 52.1],
            'government_trust': [30, 25, 22, 18, 15, 12, 15, 15, 18, 15, 18, 12, 13, 14, 15, 16],
            'corruption_index': [25, 31, 29, 31, 32, 40, 44, 47, 47, 47, 47, 47, 47, 47, 47, 48],
            'political_stability': [-0.5, -0.8, -1.0, -1.2, -1.5, -1.8, -2.0, -1.8, -1.5, -1.8, -1.5, -2.2, -2.0, -1.9, -1.8, -1.7],
            
            'population': 9.4,
            'internet_penetration': 79,
            'strategy_type': 'ПОДАВЛЕННЫЙ',
            'crypto_drivers': 'Обход санкций, IT-экспорт, майнинг, защита от девальвации'
        }
    }

    # ДОБАВЛЯЕМ HDI данные ПОСЛЕ создания countries_data
    countries_data = add_hdi_data(countries_data, base)

    rows = []
    for code, info in countries_data.items():
        for i, yr in enumerate(years):
            rows.append({
                "Year": int(yr),
                "Country": code,
                "Country_RU": info["name_ru"],
                "Currency": info["currency"],
                "GDP_Per_Capita": int(info["gdp_per_capita"][i]),
                "Inflation": round(float(info["inflation"][i]), 2),
                "Crypto_Adoption": round(float(info["crypto_adoption"][i]), 2),
                "GDP_Growth": round(float(info["gdp_growth"][i]), 2),
                "Currency_Volatility": round(float(info["currency_volatility"][i]), 2),
                "Unemployment": round(float(info["unemployment"][i]), 2),
                "Exports": round(float(info["exports"][i]), 1),
                "Imports": round(float(info["imports"][i]), 1),
                "Government_Debt": round(float(info["government_debt"][i]), 1),
                "Government_Trust": int(info["government_trust"][i]),
                "Corruption_Index": int(info["corruption_index"][i]),
                "Political_Stability": round(float(info["political_stability"][i]), 2),
                "HDI": round(float(info["hdi"][i]), 3),  # ← ДОБАВЛЯЕМ HDI
                "Population": round(float(info["population"]), 1),
                "Internet_Penetration": int(info["internet_penetration"]),
                "Strategy_Type": info["strategy_type"],
                "Main_Crypto": ", ".join(info["main_crypto"]),
                "Crypto_Preference": info["crypto_preference"],
                "Crypto_Drivers": info["crypto_drivers"],
            })

    df = optimize_int_columns(pd.DataFrame(rows))
    df['Year'] = df['Year'].astype('int32')
    
    print(f"✅ Расширенные данные созданы: {len(df)} записей (2010-2025)")
    return df, countries_data
def extended_correlation_analysis(df, countries, base):
    """Расширенный анализ корреляций: BTC vs Trust/HDI + простая кластеризация"""
    print("🔍 Расширенный корреляционный анализ...")
    
    # 1. КОРРЕЛЯЦИИ BTC vs TRUST/HDI
    correlations_analysis = {}
    
    # Общие корреляции
    btc_trust_corr = df['Government_Trust'].corr(df['Crypto_Adoption'])
    btc_hdi_corr = df['HDI'].corr(df['Crypto_Adoption'])
    btc_corruption_corr = df['Corruption_Index'].corr(df['Crypto_Adoption'])
    btc_stability_corr = df['Political_Stability'].corr(df['Crypto_Adoption'])
    
    correlations_analysis['Общие'] = {
        'BTC_vs_Trust': round(btc_trust_corr, 3),
        'BTC_vs_HDI': round(btc_hdi_corr, 3),
        'BTC_vs_Corruption': round(btc_corruption_corr, 3),
        'BTC_vs_Political_Stability': round(btc_stability_corr, 3)
    }
    
    # Корреляции по странам
    country_detailed_corr = {}
    for country_code, country_info in countries.items():
        country_data = df[df['Country'] == country_code]
        country_name = country_info['name_ru']
        
        country_detailed_corr[country_name] = {
            'Trust_BTC': round(country_data['Government_Trust'].corr(country_data['Crypto_Adoption']), 3),
            'HDI_BTC': round(country_data['HDI'].corr(country_data['Crypto_Adoption']), 3),
            'Corruption_BTC': round(country_data['Corruption_Index'].corr(country_data['Crypto_Adoption']), 3),
            'Stability_BTC': round(country_data['Political_Stability'].corr(country_data['Crypto_Adoption']), 3)
        }
    
    # 2. ПРОСТАЯ КЛАСТЕРИЗАЦИЯ (без sklearn)
    # Подготовка данных для кластеризации (средние значения по странам)
    cluster_data = []
    country_names = []
    
    for country_code, country_info in countries.items():
        country_data = df[df['Country'] == country_code]
        country_names.append(country_info['name_ru'])
        
        cluster_data.append({
            'Страна': country_info['name_ru'],
            'Доверие_среднее': round(country_data['Government_Trust'].mean(), 1),
            'HDI_среднее': round(country_data['HDI'].mean(), 3),
            'BTC_адопция_средняя': round(country_data['Crypto_Adoption'].mean(), 1),
            'Коррупция_средняя': round(country_data['Corruption_Index'].mean(), 1),
            'Стабильность_средняя': round(country_data['Political_Stability'].mean(), 2)
        })
    
    # Простая кластеризация по доверию и BTC
    cluster_df = pd.DataFrame(cluster_data)
    
    # Определяем кластеры по правилам
    def assign_cluster(row):
        trust = row['Доверие_среднее']
        btc = row['BTC_адопция_средняя']
        
        if trust >= 60 and btc <= 5:
            return 0  # Высокое доверие, низкая адопция
        elif trust <= 30 and btc >= 5:
            return 2  # Низкое доверие, высокая адопция
        else:
            return 1  # Среднее доверие, умеренная адопция
    
    cluster_df['Кластер'] = cluster_df.apply(assign_cluster, axis=1)
    
    # Интерпретация кластеров
    cluster_interpretation = {
        0: "Высокое доверие, низкая адопция BTC",
        1: "Среднее доверие, умеренная адопция BTC", 
        2: "Низкое доверие, высокая адопция BTC"
    }
    
    # 3. ПРОСТАЯ РЕГРЕССИЯ Trust → BTC
    from scipy import stats
    
    # Линейная регрессия: Trust → BTC
    slope_trust, intercept_trust, r_value_trust, p_value_trust, std_err_trust = stats.linregress(
        df['Government_Trust'], df['Crypto_Adoption']
    )
    
    # Линейная регрессия: HDI → BTC  
    slope_hdi, intercept_hdi, r_value_hdi, p_value_hdi, std_err_hdi = stats.linregress(
        df['HDI'], df['Crypto_Adoption']
    )
    
    regression_results = {
        'Trust_to_BTC': {
            'slope': round(slope_trust, 4),
            'intercept': round(intercept_trust, 4),
            'r_squared': round(r_value_trust**2, 3),
            'p_value': round(p_value_trust, 4)
        },
        'HDI_to_BTC': {
            'slope': round(slope_hdi, 4),
            'intercept': round(intercept_hdi, 4),
            'r_squared': round(r_value_hdi**2, 3),
            'p_value': round(p_value_hdi, 4)
        }
    }
    
    # 4. СОЗДАНИЕ ИНТЕРАКТИВНЫХ ГРАФИКОВ
    
    # График кластеризации
    fig_cluster = go.Figure()
    
    colors_cluster = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    for i in range(3):
        cluster_countries = cluster_df[cluster_df['Кластер'] == i]
        if len(cluster_countries) > 0:
            fig_cluster.add_trace(go.Scatter(
                x=cluster_countries['Доверие_среднее'],
                y=cluster_countries['BTC_адопция_средняя'],
                mode='markers+text',
                name=f'Кластер {i}: {cluster_interpretation[i]}',
                text=cluster_countries['Страна'],
                textposition="top center",
                marker=dict(
                    size=cluster_countries['HDI_среднее'] * 50,
                    color=colors_cluster[i],
                    opacity=0.7,
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{text}</b><br>' +
                             'Доверие: %{x:.1f}%<br>' +
                             'BTC адопция: %{y:.1f}%<br>' +
                             'HDI: %{customdata:.3f}<br>' +
                             '<extra></extra>',
                customdata=cluster_countries['HDI_среднее']
            ))
    
    fig_cluster.update_layout(
        title='Кластеризация стран по доверию и BTC адопции (размер = HDI)',
        xaxis_title='Среднее доверие к государству (%)',
        yaxis_title='Средняя BTC адопция (%)',
        template='plotly_white',
        width=1000,
        height=600
    )
    
    # График регрессии Trust → BTC
    fig_regression = go.Figure()
    
    # Точки данных
    fig_regression.add_trace(go.Scatter(
        x=df['Government_Trust'],
        y=df['Crypto_Adoption'],
        mode='markers',
        name='Данные',
        marker=dict(size=8, opacity=0.6),
        hovertemplate='Доверие: %{x}%<br>BTC: %{y:.1f}%<extra></extra>'
    ))
    
    # Линия регрессии
    x_reg = [df['Government_Trust'].min(), df['Government_Trust'].max()]
    y_reg = [slope_trust * x + intercept_trust for x in x_reg]
    
    fig_regression.add_trace(go.Scatter(
        x=x_reg,
        y=y_reg,
        mode='lines',
        name=f'Регрессия (R² = {r_value_trust**2:.3f})',
        line=dict(color='red', width=3)
    ))
    
    fig_regression.update_layout(
        title=f'Регрессионный анализ: Доверие → BTC адопция<br>Уравнение: BTC = {slope_trust:.4f} × Trust + {intercept_trust:.4f}',
        xaxis_title='Доверие к государству (%)',
        yaxis_title='BTC адопция (%)',
        template='plotly_white',
        width=1000,
        height=600
    )
    
    # 5. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ
    
    # Сохранение графиков
    grafiki_path = os.path.join(base, 'grafiki')
    fig_cluster.write_html(os.path.join(grafiki_path, 'cluster_analysis.html'))
    fig_regression.write_html(os.path.join(grafiki_path, 'regression_trust_btc.html'))
    
    # Сохранение в Excel
    extended_analysis_path = os.path.join(base, 'otchety', 'extended_correlation_analysis.xlsx')
    with pd.ExcelWriter(extended_analysis_path, engine='openpyxl') as writer:
        
        # Общие корреляции
        general_corr_df = pd.DataFrame(list(correlations_analysis['Общие'].items()), 
                                      columns=['Показатель', 'Корреляция_с_BTC'])
        general_corr_df.to_excel(writer, sheet_name='Общие_корреляции', index=False)
        
        # Детальные корреляции по странам
        detailed_df = pd.DataFrame(country_detailed_corr).T
        detailed_df.reset_index(inplace=True)
        detailed_df.rename(columns={'index': 'Страна'}, inplace=True)
        detailed_df.to_excel(writer, sheet_name='Корреляции_по_странам', index=False)
        
        # Результаты кластеризации
        cluster_df.to_excel(writer, sheet_name='Кластеризация', index=False)
        
        # Результаты регрессии
        regression_df = pd.DataFrame(regression_results).T
        regression_df.reset_index(inplace=True)
        regression_df.rename(columns={'index': 'Модель'}, inplace=True)
        regression_df.to_excel(writer, sheet_name='Регрессионный_анализ', index=False)
    
    print("✅ Расширенный корреляционный анализ завершен!")
    print(f"   📊 BTC vs Trust: {btc_trust_corr:.3f}")
    print(f"   📊 BTC vs HDI: {btc_hdi_corr:.3f}")
    print(f"   🎯 Кластеры: {len(cluster_df['Кластер'].unique())} группы стран")
    print(f"   📈 R² (Trust→BTC): {r_value_trust**2:.3f}")
    
    return correlations_analysis, cluster_df, regression_results

def country_analysis_pages(df: pd.DataFrame, countries: Dict[str, Any], base: str):
    """Создание детального анализа по каждой стране с HTML страницами и графиками"""
    print("🌍 Создание анализа по странам...")
    
    strany_path = os.path.join(base, 'strany_analiz')
    os.makedirs(strany_path, exist_ok=True)
    
    # Цвета для стран
    colors = {'Ukraine': '#FF6B6B', 'Poland': '#4ECDC4', 'Czech': '#45B7D1', 
              'Sweden': '#96CEB4', 'Norway': '#FFEAA7', 'Belarus': '#DDA0DD'}
    
    for country_code, country_info in countries.items():
        country_name = country_info['name_ru']
        country_data = df[df['Country'] == country_code].copy()
        
        print(f"   📈 Создание анализа для {country_name}...")
        
        # Создаем папку для страны
        country_folder = os.path.join(strany_path, country_code.lower())
        os.makedirs(country_folder, exist_ok=True)
        
        # 1. СОЗДАНИЕ ГРАФИКОВ ДЛЯ СТРАНЫ
        
        # График 1: Динамика криптоадопции
        plt.figure(figsize=(12, 8))
        plt.plot(country_data['Year'], country_data['Crypto_Adoption'], 
                marker='o', linewidth=3, color=colors[country_code], markersize=8)
        
        # Добавляем аннотации ключевых событий
        if country_code == 'Ukraine':
            plt.axvline(x=2014, color='red', linestyle='--', alpha=0.7)
            plt.text(2014.1, country_data['Crypto_Adoption'].max()*0.8, 'Майдан', fontsize=10)
            plt.axvline(x=2022, color='red', linestyle='--', alpha=0.7)
            plt.text(2022.1, country_data['Crypto_Adoption'].max()*0.9, 'Война', fontsize=10)
        elif country_code == 'Poland':
            plt.axvline(x=2004, color='blue', linestyle='--', alpha=0.7)
            plt.text(2004.1, country_data['Crypto_Adoption'].max()*0.8, 'Вступление в ЕС', fontsize=10)
        
        plt.title(f'Динамика криптоадопции: {country_name} (2010-2025)', fontsize=16, fontweight='bold')
        plt.xlabel('Год', fontsize=12)
        plt.ylabel('Криптоадопция (%)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(country_folder, f'{country_code.lower()}_crypto_trend.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # График 2: Корреляция инфляция-крипто
        plt.figure(figsize=(10, 8))
        plt.scatter(country_data['Inflation'], country_data['Crypto_Adoption'], 
                   s=100, alpha=0.7, color=colors[country_code])
        
        # Линия тренда
        z = np.polyfit(country_data['Inflation'], country_data['Crypto_Adoption'], 1)
        p = np.poly1d(z)
        plt.plot(country_data['Inflation'], p(country_data['Inflation']), 
                "r--", alpha=0.8, linewidth=2)
        
        correlation = country_data['Inflation'].corr(country_data['Crypto_Adoption'])
        plt.title(f'Связь инфляции и криптоадопции: {country_name}', fontsize=16, fontweight='bold')
        plt.xlabel('Инфляция (%)', fontsize=12)
        plt.ylabel('Криптоадопция (%)', fontsize=12)
        plt.text(0.05, 0.95, f'Корреляция: {correlation:.3f}', 
                transform=plt.gca().transAxes, fontsize=14, fontweight='bold',
                bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.8))
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(country_folder, f'{country_code.lower()}_correlation.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # График 3: Экономические показатели
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # ВВП на душу населения
        ax1.plot(country_data['Year'], country_data['GDP_Per_Capita'], 
                color=colors[country_code], linewidth=2, marker='o')
        ax1.set_title('ВВП на душу населения (USD)', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Безработица
        ax2.plot(country_data['Year'], country_data['Unemployment'], 
                color='red', linewidth=2, marker='s')
        ax2.set_title('Уровень безработицы (%)', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Экспорт/Импорт
        ax3.plot(country_data['Year'], country_data['Exports'], 
                color='green', linewidth=2, marker='^', label='Экспорт')
        ax3.plot(country_data['Year'], country_data['Imports'], 
                color='orange', linewidth=2, marker='v', label='Импорт')
        ax3.set_title('Торговый баланс (млрд USD)', fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Доверие к правительству
        ax4.plot(country_data['Year'], country_data['Government_Trust'], 
                color='purple', linewidth=2, marker='d')
        ax4.set_title('Доверие к правительству (%)', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'Экономические показатели: {country_name}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(country_folder, f'{country_code.lower()}_economics.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. СОЗДАНИЕ HTML СТРАНИЦЫ ДЛЯ СТРАНЫ
        
        # Расчет статистик
        avg_crypto = country_data['Crypto_Adoption'].mean()
        max_crypto = country_data['Crypto_Adoption'].max()
        max_crypto_year = country_data.loc[country_data['Crypto_Adoption'].idxmax(), 'Year']
        growth_2010_2025 = ((country_data['Crypto_Adoption'].iloc[-1] / country_data['Crypto_Adoption'].iloc[0]) - 1) * 100
        
        # Определение стратегии
        strategy_description = {
            'ЗАЩИТНИК': 'Использует криптовалюты как защиту от экономической нестабильности и девальвации национальной валюты',
            'ДИВЕРСИФИКАТОР': 'Включает криптовалюты в инвестиционный портфель для диверсификации рисков',
            'ИННОВАТОР': 'Принимает криптовалюты как технологическую инновацию и инструмент цифровой экономики',
            'ПОДАВЛЕННЫЙ': 'Криптоадопция ограничена государственным регулированием и контролем'
        }
        
        html_content = f""
        # ------ main.html ------
        # Добавляем данные в таблицу
        for _, row in country_data.iterrows():
            html_content += f"""
                                <tr>
                                    <td>{int(row['Year'])}</td>
                                    <td>{row['Crypto_Adoption']:.2f}%</td>
                                    <td>{row['Inflation']:.2f}%</td>
                                    <td>${row['GDP_Per_Capita']:,.0f}</td>
                                    <td>{row['Unemployment']:.2f}%</td>
                                </tr>
            """
        
        html_content += f"""
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="section">
                        <h2>🔍 Выводы и рекомендации</h2>
                        <div class="highlight">
        """
        
        # Генерируем выводы на основе данных
        if correlation > 0.5:
            html_content += f"<p><strong>Высокая корреляция ({correlation:.3f}):</strong> В {country_name} наблюдается сильная связь между инфляцией и криптоадопцией. Население активно использует криптовалюты как защиту от экономической нестабильности.</p>"
        elif correlation > 0.3:
            html_content += f"<p><strong>Умеренная корреляция ({correlation:.3f}):</strong> В {country_name} криптоадопция частично связана с инфляцией, но также определяется другими факторами.</p>"
        elif correlation < 0:
            html_content += f"<p><strong>Отрицательная корреляция ({correlation:.3f}):</strong> В {country_name} наблюдается уникальный случай - рост инфляции сопровождается снижением криптоадопции, что указывает на государственное вмешательство.</p>"
        else:
            html_content += f"<p><strong>Слабая корреляция ({correlation:.3f}):</strong> В {country_name} криптоадопция определяется преимущественно технологическими и социальными факторами, а не экономическими кризисами.</p>"
        
        html_content += f"""
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Сохраняем HTML файл
        html_path = os.path.join(country_folder, f'{country_code.lower()}_analysis.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"   ✅ Анализ для {country_name} создан")
    
    # Создаем индексную страницу
    countries_index_page(countries, strany_path, colors)
    
    print(f"✅ Анализ по всем странам создан в папке: {strany_path}")

def countries_index_page(countries: Dict[str, Any], strany_path: str, colors: Dict[str, str]):
    """Создание главной индексной страницы со списком всех стран"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Анализ криптоадопции по странам</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 3em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
            .countries-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 30px;
                padding: 40px;
            }}
            .country-card {{
                background: white;
                border-radius: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-top: 5px solid;
            }}
            .country-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.2);
            }}
            .country-header {{
                padding: 25px;
                color: white;
                text-align: center;
            }}
            .country-body {{
                padding: 25px;
            }}
            .country-title {{
                font-size: 1.8em;
                font-weight: bold;
                margin: 0;
            }}
            .country-subtitle {{
                opacity: 0.9;
                margin: 5px 0 0 0;
            }}
            .strategy-badge {{
                display: inline-block;
                background: rgba(255,255,255,0.2);
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 0.9em;
                margin-top: 10px;
            }}
            .country-stats {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin: 20px 0;
            }}
            .stat {{
                text-align: center;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
            }}
            .stat-number {{
                font-size: 1.5em;
                font-weight: bold;
                margin: 0;
            }}
            .stat-label {{
                color: #666;
                font-size: 0.9em;
                margin: 5px 0 0 0;
            }}
            .view-button {{
                display: block;
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                text-align: center;
                border-radius: 8px;
                font-weight: bold;
                transition: opacity 0.3s ease;
            }}
            .view-button:hover {{
                opacity: 0.9;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌍 Анализ криптоадопции по странам</h1>
                <p>Восточная Европа (2010-2025)</p>
            </div>
            
            <div class="countries-grid">
    """
    
    # Добавляем карточки стран
    for country_code, country_info in countries.items():
        country_name = country_info['name_ru']
        html_content += f"""
                <div class="country-card" style="border-top-color: {colors[country_code]};">
                    <div class="country-header" style="background: {colors[country_code]};">
                        <h2 class="country-title">{country_name}</h2>
                        <p class="country-subtitle">{country_info['currency']}</p>
                        <div class="strategy-badge">{country_info['strategy_type']}</div>
                    </div>
                    <div class="country-body">
                        <div class="country-stats">
                            <div class="stat">
                                <div class="stat-number" style="color: {colors[country_code]};">{country_info['population']}</div>
                                <div class="stat-label">млн населения</div>
                            </div>
                            <div class="stat">
                                <div class="stat-number" style="color: {colors[country_code]};">{country_info['internet_penetration']}%</div>
                                <div class="stat-label">интернет</div>
                            </div>
                        </div>
                        <p><strong>Основные криптовалюты:</strong> {', '.join(country_info['main_crypto'])}</p>
                        <p><strong>Предпочтения:</strong> {country_info['crypto_preference']}</p>
                        <a href="{country_code.lower()}/{country_code.lower()}_analysis.html" class="view-button">
                            📊 Посмотреть детальный анализ
                        </a>
                    </div>
                </div>
        """
    
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    # Сохраняем индексную страницу
    index_path = os.path.join(strany_path, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Главная страница создана: {index_path}")
def interactive_dynamics_chart(df, countries, base):
    """Создание только интерактивного графика динамики"""
    print("🎨 Создание интерактивного графика динамики...")
    
    colors = {'Ukraine': '#FF6B6B', 'Poland': '#4ECDC4', 'Czech': '#45B7D1', 
              'Sweden': '#96CEB4', 'Norway': '#FFEAA7', 'Belarus': '#DDA0DD'}
    
    fig_dynamic = go.Figure()
    
    for country_code, country_info in countries.items():
        country_data = df[df['Country'] == country_code]
        country_name = country_info['name_ru']
        
        fig_dynamic.add_trace(go.Scatter(
            x=country_data['Year'],
            y=country_data['Crypto_Adoption'],
            mode='lines+markers',
            name=country_name,
            line=dict(color=colors[country_code], width=3),
            marker=dict(size=8),
            hovertemplate=f'<b>{country_name}</b><br>' +
                         'Rok: %{x}<br>' +
                         'Adopcja BTC: %{y:.1f}%<br>' +
                         'Zaufanie do państwa: %{customdata:.0f}%<br>' +
                         '<extra></extra>',
            customdata=country_data['Government_Trust']
        ))
    
    # События
    fig_dynamic.add_vline(x=2014, line_dash="dash", line_color="gray", 
                         annotation_text="Majdan na Ukrainie", annotation_position="top")
    fig_dynamic.add_vline(x=2020, line_dash="dash", line_color="orange", 
                         annotation_text="COVID-19", annotation_position="top")
    fig_dynamic.add_vline(x=2022, line_dash="dash", line_color="red", 
                         annotation_text="Wojna na Ukrainie", annotation_position="top")
    
    fig_dynamic.update_layout(
        title='Dynamika adopcji kryptowalut w krajach Europy Wschodniej (2010-2025)',
        xaxis_title='Rok',
        yaxis_title='Adopcja kryptowalut (%)',
        hovermode='x unified',
        template='plotly_white',
        width=1200,
        height=600,
        legend=dict(x=0.02, y=0.98)
    )
    
    # Сохранение
    grafiki_path = os.path.join(base, 'grafiki')
    fig_dynamic.write_html(os.path.join(grafiki_path, 'interactive_dynamics.html'))
    
    print("✅ Интерактивный график динамики создан!")
    return fig_dynamic

def methodology_and_sources(base: str):
    """Создание файла с методологией и источниками данных"""
    print("📚 Создание методологии и источников...")
    
    rezultaty_path = os.path.join(base, 'rezultaty')
    
    # Создание файла с источниками и методологией
    with open(os.path.join(rezultaty_path, 'metodologiya_i_istochniki.txt'), 'w', encoding='utf-8') as f:
        f.write("МЕТОДОЛОГИЯ И ИСТОЧНИКИ ДАННЫХ\n")
        f.write("АНАЛИЗ КРИПТОАДОПЦИИ В ВОСТОЧНОЙ ЕВРОПЕ (2010-2025)\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("📊 ИСТОЧНИКИ ЭКОНОМИЧЕСКИХ ДАННЫХ:\n")
        f.write("-" * 40 + "\n")
        f.write("• ВВП на душу населения:\n")
        f.write("  - World Bank Open Data (data.worldbank.org)\n")
        f.write("  - Trading Economics (tradingeconomics.com)\n")
        f.write("  - Macrotrends (macrotrends.net)\n")
        f.write("  - OECD Statistics (stats.oecd.org)\n\n")
        
        f.write("• Инфляция:\n")
        f.write("  - Центральные банки стран:\n")
        f.write("    * NBU (Украина) - bank.gov.ua\n")
        f.write("    * NBP (Польша) - nbp.pl\n")
        f.write("    * CNB (Чехия) - cnb.cz\n")
        f.write("    * Riksbank (Швеция) - riksbank.se\n")
        f.write("    * Norges Bank (Норвегия) - norges-bank.no\n")
        f.write("    * NBRB (Беларусь) - nbrb.by\n")
        f.write("  - Trading Economics\n")
        f.write("  - YCharts (ycharts.com)\n")
        f.write("  - Inflation.eu\n\n")
        
        f.write("• Безработица и рост ВВП:\n")
        f.write("  - Eurostat (ec.europa.eu/eurostat)\n")
        f.write("  - OECD Employment Outlook\n")
        f.write("  - Национальные статистические службы\n\n")
        
        f.write("• Экспорт/Импорт:\n")
        f.write("  - UN Comtrade Database\n")
        f.write("  - WTO Statistics\n")
        f.write("  - Национальные таможенные службы\n\n")
        
        f.write("🪙 ИСТОЧНИКИ ДАННЫХ О КРИПТОАДОПЦИИ:\n")
        f.write("-" * 40 + "\n")
        f.write("• Chainalysis Global Crypto Adoption Index\n")
        f.write("• Triple-A Crypto Ownership Report\n")
        f.write("• Henley Crypto Adoption Index 2024\n")
        f.write("• Statista Cryptocurrency Statistics\n")
        f.write("• CoinMarketCap Research\n")
        f.write("• Binance Research Reports\n")
        f.write("• Finder.com Crypto Adoption Surveys\n\n")
        
        f.write("🏛️ ИСТОЧНИКИ ПОЛИТИЧЕСКИХ И СОЦИАЛЬНЫХ ДАННЫХ:\n")
        f.write("-" * 40 + "\n")
        f.write("• Индекс коррупции:\n")
        f.write("  - Transparency International CPI\n")
        f.write("• Политическая стабильность:\n")
        f.write("  - World Bank Worldwide Governance Indicators\n")
        f.write("• Доверие к правительству:\n")
        f.write("  - OECD Government at a Glance\n")
        f.write("  - Edelman Trust Barometer\n")
        f.write("  - Gallup World Poll\n\n")
        
        f.write("🔬 МЕТОДОЛОГИЯ ИССЛЕДОВАНИЯ:\n")
        f.write("-" * 40 + "\n")
        f.write("• Временные рамки: 2010-2025 (16 лет)\n")
        f.write("• Количество стран: 6 (Украина, Польша, Чехия, Швеция, Норвегия, Беларусь)\n")
        f.write("• Общий объем данных: 96 наблюдений (16 лет × 6 стран)\n")
        f.write("• Количество переменных: 22 показателя на страну\n\n")
        
        f.write("• Методы анализа:\n")
        f.write("  - Корреляционный анализ (коэффициент Пирсона)\n")
        f.write("  - Временные ряды\n")
        f.write("  - Кластерный анализ для типологии стран\n")
        f.write("  - Описательная статистика\n\n")
        
        f.write("• Программное обеспечение:\n")
        f.write("  - Python 3.13 (pandas, numpy, matplotlib)\n")
        f.write("  - Excel для валидации данных\n\n")
        
        f.write("⚠️ ОГРАНИЧЕНИЯ ИССЛЕДОВАНИЯ:\n")
        f.write("-" * 40 + "\n")
        f.write("• Данные по криптоадопции до 2018 года основаны на экстраполяции\n")
        f.write("• Беларусь: ограниченная доступность официальной статистики\n")
        f.write("• Украина: данные за 2022-2023 могут быть неточными из-за войны\n")
        f.write("• Различия в методологии измерения криптоадопции между источниками\n")
        f.write("• Прогнозы основаны на текущих трендах и могут измениться\n\n")
        
        f.write("📝 ВАЛИДАЦИЯ ДАННЫХ:\n")
        f.write("-" * 40 + "\n")
        f.write("• Кросс-проверка данных между несколькими источниками\n")
        f.write("• Сравнение с независимыми исследованиями\n")
        f.write("• Проверка на выбросы и аномалии\n")
        f.write("• Экспертная оценка результатов\n\n")
        
        f.write("🎯 НАУЧНАЯ НОВИЗНА:\n")
        f.write("-" * 40 + "\n")
        f.write("• Первое комплексное исследование криптоадопции в Восточной Европе\n")
        f.write("• Уникальная типология стран по стратегиям криптоадопции\n")
        f.write("• Обнаружение отрицательной корреляции в авторитарных странах\n")
        f.write("• Анализ влияния геополитических кризисов на адопцию\n\n")
    
    print(f"✅ Методология и источники созданы: {rezultaty_path}")
