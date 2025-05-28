"""
ПОЛНЫЙ АНАЛИЗ КРИПТОАДОПЦИИ С API ИНТЕГРАЦИЕЙ (2010-2025)
Автономная версия без внешних зависимостей
Версия: 2025.1 (Standalone)
"""

import os
import datetime as dt
import warnings
from typing import Tuple, Dict, Any, List
import sys
import numpy as np
import pandas as pd
from scipy import stats
import requests
from functools import lru_cache
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

warnings.filterwarnings("ignore")

# ─────────────────────────── НАСТРОЙКИ ────────────────────────────
pd.options.display.float_format = lambda x: f"{x:.0f}" if pd.notna(x) and x % 1 == 0 else f"{x:.2f}"
plt.rcParams["font.family"] = ["DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ─────────────────────────── API МОДУЛЬ ────────────────────────────
BASE_URL = "https://api.worldbank.org/v2/country/{iso}/indicator/{ind}?format=json&per_page=100"

INDICATORS = {
    "gdp_per_capita": "NY.GDP.PCAP.KD",       # ВВП на душу (пост. USD-2015)
    "inflation":      "FP.CPI.TOTL.ZG",       # Инфляция, % г/г
    "unemployment":   "SL.UEM.TOTL.ZS",       # Безработица, % labor force
}

@lru_cache(maxsize=None)
def fetch_indicator(iso: str, ind_code: str) -> pd.DataFrame:
    """Загружает один индикатор через World Bank API"""
    try:
        url = BASE_URL.format(iso=iso.lower(), ind=ind_code)
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1]:
                payload = data[1]
                df = (pd.DataFrame(payload)[["date", "value"]]
                      .dropna()
                      .rename(columns={"date": "Year", "value": ind_code})
                      .astype({"Year": "int32", ind_code: "float64"}))
                return df
        
        return pd.DataFrame(columns=["Year", ind_code])
        
    except Exception as e:
        print(f"   ⚠️ Ошибка загрузки {ind_code} для {iso}: {e}")
        return pd.DataFrame(columns=["Year", ind_code])

def build_country_frame(iso: str, years: List[int]) -> pd.DataFrame:
    """Собирает все экономические индикаторы для страны"""
    dfs = []
    
    for human_key, wb_code in INDICATORS.items():
        part = fetch_indicator(iso, wb_code).rename(columns={wb_code: human_key})
        dfs.append(part)
    
    if not dfs:
        return pd.DataFrame(columns=["Year"])
    
    # Объединяем по Year
    df = dfs[0]
    for part in dfs[1:]:
        df = df.merge(part, on="Year", how="outer")
    
    # Фильтруем по нужным годам и заполняем пропуски
    if not df.empty and "Year" in df.columns:
        df = df[df["Year"].isin(years)].sort_values("Year").reset_index(drop=True)
        
        # Интерполяция пропусков
        for col in df.columns:
            if col != "Year":
                df[col] = df[col].interpolate(method='linear').fillna(method='bfill').fillna(method='ffill')
    
    return df

# ─────────────────────────── МОДУЛЬ ДАННЫХ ────────────────────────────
def model_hdi(country: str, year: int) -> float:
    """Моделирование HDI"""
    base_hdi_2020 = {
        'UKR': 0.773, 'POL': 0.880, 'CZE': 0.900,
        'SWE': 0.947, 'NOR': 0.961, 'BLR': 0.823
    }
    
    base_value = base_hdi_2020.get(country, 0.800)
    
    if year <= 2010:
        adjustment = -0.05 if country in ['UKR', 'BLR'] else -0.03
    elif year <= 2020:
        adjustment = 0.0
    elif year <= 2022:
        if country == 'UKR': adjustment = -0.04  # Война
        elif country == 'BLR': adjustment = -0.02  # Политический кризис
        else: adjustment = 0.0
    else:
        adjustment = -0.04 if country == 'UKR' else 0.0
    
    return round(max(0.5, min(1.0, base_value + adjustment)), 3)

def model_crypto_adoption(country: str, year: int) -> float:
    """Моделирование криптоадопции"""
    params = {
        'UKR': {'base': 0.1, 'acceleration_year': 2022, 'max_adoption': 15.0},
        'POL': {'base': 0.2, 'acceleration_year': 2020, 'max_adoption': 20.0},
        'CZE': {'base': 0.15, 'acceleration_year': 2021, 'max_adoption': 14.0},
        'SWE': {'base': 0.3, 'acceleration_year': 2019, 'max_adoption': 8.0},
        'NOR': {'base': 0.25, 'acceleration_year': 2019, 'max_adoption': 7.0},
        'BLR': {'base': 0.05, 'acceleration_year': 2020, 'max_adoption': 1.0}
    }
    
    param = params.get(country, params['POL'])
    
    if year <= 2010:
        return 0.0
    elif year <= 2015:
        return param['base'] * (year - 2010) / 5
    elif year <= param['acceleration_year']:
        base_2015 = param['base']
        years_since_2015 = year - 2015
        return base_2015 + (2.0 * years_since_2015 / (param['acceleration_year'] - 2015))
    else:
        years_since_acceleration = year - param['acceleration_year']
        base_at_acceleration = param['base'] + 2.0
        growth_rate = 0.3
        max_adoption = param['max_adoption']
        return max_adoption / (1 + np.exp(-growth_rate * years_since_acceleration)) * (base_at_acceleration / max_adoption)

def model_government_trust(country: str, year: int) -> int:
    """Моделирование доверия к правительству"""
    base_trust = {'UKR': 22, 'POL': 37, 'CZE': 42, 'SWE': 75, 'NOR': 68, 'BLR': 14}
    trust = base_trust.get(country, 40)
    
    if country == 'UKR':
        if year <= 2013: return 40
        elif year <= 2019: return 25
        elif year <= 2021: return 23
        else: return 22
    elif country == 'BLR':
        if year <= 2019: return 15
        else: return 12
    else:
        variation = np.sin((year - 2010) * 0.5) * 3
        return max(5, min(95, int(trust + variation)))

def model_corruption_index(country: str, year: int) -> int:
    """Моделирование индекса коррупции"""
    corruption_2023 = {'UKR': 33, 'POL': 45, 'CZE': 56, 'SWE': 83, 'NOR': 85, 'BLR': 47}
    
    if year <= 2015:
        base_values = {'UKR': 26, 'POL': 53, 'CZE': 46, 'SWE': 92, 'NOR': 89, 'BLR': 25}
        return base_values.get(country, 50)
    else:
        base = {'UKR': 26, 'POL': 53, 'CZE': 46, 'SWE': 92, 'NOR': 89, 'BLR': 25}.get(country, 50)
        target = corruption_2023.get(country, 50)
        progress = min(1.0, (year - 2015) / (2023 - 2015))
        return int(base + (target - base) * progress)

def optimize_int_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Оптимизация типов данных"""
    for col in df.columns:
        if df[col].dtype == 'float64':
            if df[col].notna().all() and (df[col] % 1 == 0).all():
                df[col] = df[col].astype('Int64')
    return df

def extended_data_2010_2025(base_path: str = ".") -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Создание полного набора данных через API"""
    print("📊 Загрузка данных через World Bank API...")
    
    YEARS = list(range(2010, 2026))
    
    COUNTRY_META = {
        "ukr": {
            "name_ru": "Украина", "currency": "UAH", "population": 41.2, "internet_penetration": 71,
            "main_crypto": ['Bitcoin', 'USDT', 'Ethereum'], "strategy_type": "ЗАЩИТНИК",
            "crypto_preference": "Stablecoins (защита от девальвации)",
            "crypto_drivers": "Защита от девальвации гривны, обход санкций, международные переводы"
        },
        "pol": {
            "name_ru": "Польша", "currency": "PLN", "population": 37.7, "internet_penetration": 85,
            "main_crypto": ['Bitcoin', 'Ethereum', 'Polish tokens'], "strategy_type": "ДИВЕРСИФИКАТОР",
            "crypto_preference": "Bitcoin (инвестиции)",
            "crypto_drivers": "Диверсификация портфеля, хедж против злотого, технологические инвестиции"
        },
        "cze": {
            "name_ru": "Чехия", "currency": "CZK", "population": 10.7, "internet_penetration": 88,
            "main_crypto": ['Bitcoin', 'Ethereum', 'Local tokens'], "strategy_type": "ДИВЕРСИФИКАТОР",
            "crypto_preference": "Bitcoin (долгосрочные инвестиции)",
            "crypto_drivers": "Технологические инновации, защита от инфляции, европейская интеграция"
        },
        "swe": {
            "name_ru": "Швеция", "currency": "SEK", "population": 10.5, "internet_penetration": 97,
            "main_crypto": ['Bitcoin', 'Ethereum', 'Green crypto'], "strategy_type": "ИННОВАТОР",
            "crypto_preference": "Ethereum (DeFi и экология)",
            "crypto_drivers": "Технологические инновации, экологические проекты, цифровая экономика"
        },
        "nor": {
            "name_ru": "Норвегия", "currency": "NOK", "population": 5.4, "internet_penetration": 98,
            "main_crypto": ['Bitcoin', 'Ethereum', 'Green mining'], "strategy_type": "ИННОВАТОР",
            "crypto_preference": "Bitcoin (зеленый майнинг)",
            "crypto_drivers": "Диверсификация нефтяного фонда, зеленые технологии, институциональные инвестиции"
        },
        "blr": {
            "name_ru": "Беларусь", "currency": "BYN", "population": 9.4, "internet_penetration": 79,
            "main_crypto": ['Bitcoin', 'USDT', 'Local mining'], "strategy_type": "ПОДАВЛЕННЫЙ",
            "crypto_preference": "USDT (обход ограничений)",
            "crypto_drivers": "Обход санкций, IT-экспорт, майнинг, защита от девальвации"
        }
    }
    
    rows = []
    countries_data = {}
    
    for iso, meta in COUNTRY_META.items():
        try:
            print(f"   🌐 Загрузка данных для {meta['name_ru']}...")
            econ = build_country_frame(iso, YEARS)
            
            if len(econ) == 0:
                print(f"   ⚠️ Нет API данных для {meta['name_ru']}, пропускаем...")
                continue
            
            for _, rec in econ.iterrows():
                year = int(rec["Year"])
                
                # Рассчитываем производные показатели
                gdp_growth = 2.0  # Базовое значение
                if len(econ[econ['Year'] < year]) > 0:
                    prev_gdp = econ[econ['Year'] == year - 1]['gdp_per_capita']
                    if len(prev_gdp) > 0 and prev_gdp.iloc[0] > 0:
                        gdp_growth = ((rec['gdp_per_capita'] / prev_gdp.iloc[0]) - 1) * 100
                
                # Моделируем дополнительные показатели
                crypto_adoption = model_crypto_adoption(iso.upper(), year)
                government_trust = model_government_trust(iso.upper(), year)
                corruption_index = model_corruption_index(iso.upper(), year)
                hdi = model_hdi(iso.upper(), year)
                
                # Рассчитываем производные
                currency_volatility = abs(rec["inflation"]) * 0.8
                political_stability = (government_trust - 50) / 50
                
                # Торговые данные (моделирование)
                base_trade = rec["gdp_per_capita"] * meta["population"] * 0.3
                exports = base_trade * (1 + (year - 2010) * 0.02) / 1e9
                imports = exports * 0.9
                
                # Госдолг (моделирование)
                base_debt = 30.0 if iso == 'nor' else 40.0
                government_debt = base_debt + (year - 2010) * 0.5
                
                row = {
                    "Year": year,
                    "Country": iso.upper(),
                    "Country_RU": meta["name_ru"],
                    "Currency": meta["currency"],
                    "GDP_Per_Capita": int(rec["gdp_per_capita"]) if pd.notna(rec["gdp_per_capita"]) else 0,
                    "Inflation": round(float(rec["inflation"]), 2) if pd.notna(rec["inflation"]) else 0.0,
                    "Unemployment": round(float(rec["unemployment"]), 2) if pd.notna(rec["unemployment"]) else 0.0,
                    "Crypto_Adoption": round(crypto_adoption, 2),
                    "GDP_Growth": round(gdp_growth, 2),
                    "Currency_Volatility": round(currency_volatility, 2),
                    "Exports": round(exports, 1),
                    "Imports": round(imports, 1),
                    "Government_Debt": round(government_debt, 1),
                    "Government_Trust": government_trust,
                    "Corruption_Index": corruption_index,
                    "Political_Stability": round(political_stability, 2),
                    "HDI": hdi,
                    "Population": round(meta["population"], 1),
                    "Internet_Penetration": int(meta["internet_penetration"]),
                    "Strategy_Type": meta["strategy_type"],
                    "Main_Crypto": ", ".join(meta["main_crypto"]),
                    "Crypto_Preference": meta["crypto_preference"],
                    "Crypto_Drivers": meta["crypto_drivers"],
                }
                rows.append(row)
            
            # Создаем countries_data для совместимости
            countries_data[iso.upper()] = meta
            print(f"   ✅ {meta['name_ru']}: {len(econ)} записей загружено")
            
        except Exception as e:
            print(f"   ❌ Ошибка для {meta['name_ru']}: {e}")
            continue
    
    df = optimize_int_columns(pd.DataFrame(rows))
    df["Year"] = df["Year"].astype("int32")
    
    print(f"✅ Данных получено: {len(df)} записей через API")
    return df, countries_data

# ─────────────────────────── УТИЛИТЫ ────────────────────────────
def create_project_structure(base_dir: str = ".") -> str:
    """Создание структуры папок проекта"""
    folders = ["dannye", "grafiki", "otchety", "rezultaty", "strany_analiz"]
    
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        os.makedirs(folder_path, exist_ok=True)
    
    print(f"📁 Структура проекта создана в: {base_dir}")
    return base_dir

def save_excel_report(df: pd.DataFrame, base_dir: str):
    """Сохранение Excel отчета"""
    excel_path = os.path.join(base_dir, "otchety", "crypto_analysis_api.xlsx")
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # Основные данные
        df.to_excel(writer, sheet_name='Основные данные', index=False)
        
        # Статистика по странам
        if 'Country_RU' in df.columns:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            numeric_cols = [col for col in numeric_cols if col not in ['Year']]
            
            if len(numeric_cols) > 0:
                country_stats = df.groupby('Country_RU')[numeric_cols].agg(['mean', 'std', 'min', 'max']).round(2)
                country_stats.to_excel(writer, sheet_name='Статистика по странам')
        
        # Корреляционная матрица
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr().round(3)
            corr_matrix.to_excel(writer, sheet_name='Корреляции')
    
    print(f"💾 Excel отчет сохранен: {excel_path}")

def create_basic_charts(df: pd.DataFrame, base_dir: str):
    """Создание базовых графиков"""
    grafiki_dir = os.path.join(base_dir, "grafiki")
    os.makedirs(grafiki_dir, exist_ok=True)
    
    # График динамики ВВП
    if 'GDP_Per_Capita' in df.columns and 'Country_RU' in df.columns:
        plt.figure(figsize=(12, 8))
        
        for country in df['Country_RU'].unique():
            country_data = df[df['Country_RU'] == country]
            plt.plot(country_data['Year'], country_data['GDP_Per_Capita'], 
                    marker='o', label=country, linewidth=2)
        
        plt.title('Динамика ВВП на душу населения (2010-2025)', fontsize=14, fontweight='bold')
        plt.xlabel('Год')
        plt.ylabel('ВВП на душу (USD)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        chart_path = os.path.join(grafiki_dir, 'gdp_dynamics.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"📊 График ВВП сохранен: {chart_path}")
    
    # График инфляции
    if 'Inflation' in df.columns and 'Country_RU' in df.columns:
        plt.figure(figsize=(12, 8))
        
        for country in df['Country_RU'].unique():
            country_data = df[df['Country_RU'] == country]
            plt.plot(country_data['Year'], country_data['Inflation'], 
                    marker='s', label=country, linewidth=2)
        
        plt.title('Динамика инфляции (2010-2025)', fontsize=14, fontweight='bold')
        plt.xlabel('Год')
        plt.ylabel('Инфляция (%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        chart_path = os.path.join(grafiki_dir, 'inflation_dynamics.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"📊 График инфляции сохранен: {chart_path}")

# ─────────────────────────── ГЛАВНАЯ ФУНКЦИЯ ────────────────────────────
def main():
    print("🚀 АНАЛИЗ: Влияние доверия к государству на адопцию криптовалют")
    print("🌐 ВЕРСИЯ: API Integration (Standalone)")
    print("=" * 70)
    
    try:
        # Создание структуры проекта
        base = create_project_structure()
        
        # Загрузка данных через API
        print("\n📊 Загрузка данных...")
        df, countries = extended_data_2010_2025(base)
        
        if len(df) == 0:
            print("❌ Не удалось загрузить данные через API")
            return
        
        print(f"✅ Данные загружены: {len(df)} записей")
        print(f"📊 Страны: {list(countries.keys())}")
        
        # Базовая статистика
        print("\n📊 БАЗОВАЯ СТАТИСТИКА:")
        print("=" * 40)
        
        available_cols = df.columns.tolist()
        print(f"📋 Доступные колонки: {len(available_cols)}")
        
        if 'GDP_Per_Capita' in df.columns:
            print(f"💰 ВВП на душу: ${df['GDP_Per_Capita'].min():,.0f} - ${df['GDP_Per_Capita'].max():,.0f} (среднее: ${df['GDP_Per_Capita'].mean():,.0f})")
        
        if 'Inflation' in df.columns:
            print(f"📈 Инфляция: {df['Inflation'].min():.2f}% - {df['Inflation'].max():.2f}% (среднее: {df['Inflation'].mean():.2f}%)")
        
        if 'Crypto_Adoption' in df.columns:
            print(f"🪙 Криптоадопция: {df['Crypto_Adoption'].min():.2f}% - {df['Crypto_Adoption'].max():.2f}% (среднее: {df['Crypto_Adoption'].mean():.2f}%)")
        
        # Статистика по странам
        print(f"\n🌍 СТАТИСТИКА ПО СТРАНАМ:")
        for country_code, meta in countries.items():
            country_data = df[df['Country'] == country_code]
            if len(country_data) > 0:
                avg_gdp = country_data['GDP_Per_Capita'].mean() if 'GDP_Per_Capita' in country_data.columns else 0
                avg_crypto = country_data['Crypto_Adoption'].mean() if 'Crypto_Adoption' in country_data.columns else 0
                print(f"   {meta['name_ru']}: {len(country_data)} записей, ВВП: ${avg_gdp:,.0f}, крипто: {avg_crypto:.2f}%")
        
        # Корреляционный анализ
        print(f"\n🔍 КОРРЕЛЯЦИОННЫЙ АНАЛИЗ:")
        print("-" * 30)
        
        if 'Inflation' in df.columns and 'Crypto_Adoption' in df.columns:
            corr1 = df['Inflation'].corr(df['Crypto_Adoption'])
            print(f"📊 Инфляция ↔ Криптоадопция: {corr1:.3f}")
        
        if 'Government_Trust' in df.columns and 'Crypto_Adoption' in df.columns:
            corr2 = df['Government_Trust'].corr(df['Crypto_Adoption'])
            print(f"🏛️ Доверие ↔ Криптоадопция: {corr2:.3f}")
        
        if 'HDI' in df.columns and 'Crypto_Adoption' in df.columns:
            corr3 = df['HDI'].corr(df['Crypto_Adoption'])
            print(f"🌟 HDI ↔ Криптоадопция: {corr3:.3f}")
        
        # Сохранение результатов
        print(f"\n💾 СОХРАНЕНИЕ РЕЗУЛЬТАТОВ:")
        print("-" * 30)
        
        # Excel отчет
        save_excel_report(df, base)
        
        # Базовые графики
        create_basic_charts(df, base)
        
        # Сводная таблица по странам
        if 'Country_RU' in df.columns:
            numeric_cols = ['GDP_Per_Capita', 'Inflation', 'Unemployment', 'Crypto_Adoption', 'HDI']
            available_numeric = [col for col in numeric_cols if col in df.columns]
            
            if available_numeric:
                country_summary = df.groupby('Country_RU')[available_numeric].mean().round(2)
                print(f"\n📋 СВОДКА ПО СТРАНАМ:")
                print(country_summary)
                
                # Сохранение сводки
                summary_path = os.path.join(base, "otchety", "country_summary.csv")
                country_summary.to_csv(summary_path, encoding='utf-8')
                print(f"💾 Сводка сохранена: {summary_path}")
        
        print(f"\n🏁 АНАЛИЗ ЗАВЕРШЕН!")
        print(f"📁 Результаты в папке: {base}")
        print(f"📊 Excel отчет: {os.path.join(base, 'otchety', 'crypto_analysis_api.xlsx')}")
        print(f"📈 Графики: {os.path.join(base, 'grafiki')}")
        
    except Exception as exc:
        print(f"❌ Критическая ошибка: {exc}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Анализ прерван пользователем")
    except Exception as exc:
        print(f"❌ Ошибка запуска: {exc}")
        import traceback
        traceback.print_exc()
