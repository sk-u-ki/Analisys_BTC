
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


# ──────────────────────────── CSV EXPORT ────────────────────────────────

def clean_excel(df: pd.DataFrame, base: str):
    """Сохранение Excel файла с правильным форматом чисел"""
    print("💾 Сохранение Excel...")
    excel_df = optimize_int_columns(df.copy())
    excel_df['Year'] = excel_df['Year'].astype(int)
    
    # ПОЛНОЕ переименование колонок
    excel_df = excel_df.rename(columns={
        "Year": "Год",
        "Country": "Код_страны",
        "Country_RU": "Страна",
        "Currency": "Валюта",
        "GDP_Per_Capita": "ВВП_на_душу_USD",
        "Inflation": "Инфляция_%",
        "Crypto_Adoption": "Криптоадопция_%",
        "GDP_Growth": "Рост_ВВП_%",
        "Currency_Volatility": "Валютная_волатильность_%",
        "Unemployment": "Безработица_%",
        "Exports": "Экспорт_млрд_USD",
        "Imports": "Импорт_млрд_USD",
        "Government_Debt": "Гос_долг_%_ВВП",
        "Government_Trust": "Доверие_к_правительству_%",
        "Corruption_Index": "Индекс_коррупции_0_100",
        "Political_Stability": "Политическая_стабильность",
        "HDI": "Индекс_человеческого_развития",
        "Population": "Население_млн",
        "Internet_Penetration": "Интернет_проникновение_%",
        "Strategy_Type": "Тип_стратегии",
        "Main_Crypto": "Основные_криптовалюты",
        "Crypto_Preference": "Криптопредпочтения",
        "Crypto_Drivers": "Драйверы_адопции"
    })
    
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = os.path.join(base, "dannye", f"clean_dataset_{ts}.xlsx")
    
    try:
        excel_df.to_excel(fn, index=False, engine='openpyxl')
        print(f"✅ Excel сохранён: {fn}")
    except PermissionError:
        backup_fn = os.path.join(base, f"dataset_backup_{ts}.xlsx")
        excel_df.to_excel(backup_fn, index=False, engine='openpyxl')
        print(f"✅ Excel создан в корневой папке: {backup_fn}")

