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
from function.create import analysis, data_build, reports
from function.export import save

warnings.filterwarnings("ignore")

# ─────────────────────────── DISPLAY SETTINGS ────────────────────────────
pd.options.display.float_format = lambda x: f"{x:.0f}" if pd.notna(x) and x % 1 == 0 else f"{x:.2f}"
plt.rcParams["font.family"] = ["DejaVu Sans"]  # поддержка кириллицы
plt.rcParams["axes.unicode_minus"] = False



# ─────────────────────────────── MAIN ────────────────────────────────

def main():
    print("🚀 АНАЛИЗ: Влияние доверия к государству на адопцию криптовалют")
    print("=" * 70)
    
    base = create_project_structure()
    df, countries = data_build.extended_data_2010_2025(base)
    save.clean_excel(df, base)
    corr_m, c_corr, p_corr = analysis.comprehensive_analysis(df, countries, base)
    reports.countries_comparison_chart(df, countries, base)
    
    # НОВЫЕ АНАЛИЗЫ
    data_build.interactive_dynamics_chart(df, countries, base)
    trust_corr, overall_trust, fig_trust = analysis.trust_btc_analysis(df, countries, base)
    extended_corr, clusters, regression = data_build.extended_correlation_analysis(df, countries, base)
    crisis_corr, stable_corr, transition_corr = data_build.hypothesis_analysis(df, countries, base)
    
    reports.excel_reports(df, countries, corr_m, c_corr, p_corr, base)
    data_build.country_analysis_pages(df, countries, base)
    reports.results_summary(df, countries, c_corr, p_corr, base)
    data_build.methodology_and_sources(base)
    reports.full_methodology_document(base)
    reports.static_preview_charts(df, countries, base)
    reports.main_project_index(df, countries, c_corr, p_corr, base)
    
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
