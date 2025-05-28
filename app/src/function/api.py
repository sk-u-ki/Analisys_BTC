"""
api.py – компактный клиент Всемирного банка
------------------------------------------
Получает экономические показатели по ISO-коду страны и индикатору.
Использует кэш в памяти, чтобы не дёргать API лишний раз.
"""

from functools import lru_cache
import requests
import pandas as pd

BASE = "https://api.worldbank.org/v2/country/{iso}/indicator/{ind}?format=json&per_page=100"

INDICATORS = {
    "gdp_per_capita": "NY.GDP.PCAP.KD",       # ВВП на душу (пост. USD-2015)
    "inflation":      "FP.CPI.TOTL.ZG",       # Инфляция, % г/г
    "unemployment":   "SL.UEM.TOTL.ZS",       # Безработица, % labor force
    # Убираем HDI - его нет в World Bank
}

def _wb_request(url: str, page: int = 1) -> list[dict]:
    """Запрос к World Bank API с обработкой ошибок"""
    r = requests.get(f"{url}&page={page}", timeout=10)
    if r.status_code != 200:
        raise ConnectionError(f"WB {r.status_code}: {r.text[:120]}")
    data = r.json()
    if not isinstance(data, list) or len(data) < 2:
        return []
    return data

@lru_cache(maxsize=None)
def fetch_indicator(iso: str, ind_code: str) -> pd.DataFrame:
    """Загружает один индикатор для страны"""
    try:
        url = BASE.format(iso=iso.lower(), ind=ind_code)
        meta = _wb_request(url)[0]            # метаданные
        pages = int(meta.get("pages", 1))
        
        payload = []
        for p in range(1, pages + 1):
            payload.extend(_wb_request(url, page=p)[1])
        
        if not payload:
            return pd.DataFrame(columns=["Year", ind_code])
        
        df = (pd.DataFrame(payload)[["date", "value"]]
                .dropna()
                .rename(columns={"date": "Year", "value": ind_code})
                .astype({"Year": "int32", ind_code: "float64"}))
        return df
        
    except Exception as e:
        print(f"   ⚠️ Ошибка загрузки {ind_code} для {iso}: {e}")
        return pd.DataFrame(columns=["Year", ind_code])

def build_country_frame(iso: str, years: list[int]) -> pd.DataFrame:
    """Собирает все индикаторы для страны"""
    dfs = []
    for human_key, wb_code in INDICATORS.items():
        part = fetch_indicator(iso, wb_code).rename(columns={wb_code: human_key})
        dfs.append(part)
    
    # Объединяем по Year
    if not dfs:
        return pd.DataFrame(columns=["Year"])
    
    df = dfs[0]
    for part in dfs[1:]:
        df = df.merge(part, on="Year", how="outer")
    
    # Фильтруем по нужным годам
    if not df.empty and "Year" in df.columns:
        df = df[df["Year"].isin(years)].sort_values("Year").reset_index(drop=True)
    
    return df
