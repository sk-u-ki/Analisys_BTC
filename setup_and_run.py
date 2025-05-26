"""
УСТАНОВКА БИБЛИОТЕК ДЛЯ АНАЛИЗА КРИПТОАДОПЦИИ
Запустите этот файл ПЕРВЫМ для установки всех зависимостей
"""

import subprocess
import sys
import os

def install_libraries():
    """Установка всех необходимых библиотек"""
    print("🔧 УСТАНОВКА БИБЛИОТЕК ДЛЯ АНАЛИЗА КРИПТОАДОПЦИИ")
    print("=" * 50)
    
    # ТОЧНЫЙ список библиотек из вашего проекта
    libraries = [
    'pandas>=2.0.0',
    'numpy>=1.24.0', 
    'matplotlib>=3.7.0',
    'openpyxl>=3.1.0',
    'plotly>=5.15.0',
    'pyyaml>=6.0' ,
    'jinja2>=3.1.0'  # ← ДОБАВИТЬ для работы с YAML
] # для Excel файлов

    
    print(f"📦 Будет установлено {len(libraries)} библиотек...")
    print("📋 Список библиотек:")
    for lib in libraries:
        print(f"   • {lib}")
    print()
    
    success = 0
    failed = []
    
    for lib in libraries:
        try:
            print(f"🔧 Установка {lib}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {lib} установлен")
            success += 1
        except Exception as e:
            print(f"❌ Ошибка установки {lib}")
            failed.append(lib)
    
    print(f"\n📊 РЕЗУЛЬТАТ: {success}/{len(libraries)} библиотек установлено")
    
    if success == len(libraries):
        print("🎉 Все библиотеки установлены успешно!")
        print("✅ Теперь можете запустить run.py")
    else:
        print("⚠️ Некоторые библиотеки не установились:")
        for lib in failed:
            print(f"   ❌ {lib}")
        print("\n💡 Попробуйте:")
        print("   1. Запустить от имени администратора")
        print("   2. Обновить pip: python -m pip install --upgrade pip")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    install_libraries()
