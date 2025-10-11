"""
Dependency checker for iOS Keyboard Prototype
Проверка установленных зависимостей
"""

import sys

def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("⚠ Рекомендуется Python 3.11+")
        return False
    return True

def check_kivy():
    """Проверка установки Kivy"""
    try:
        import kivy
        print(f"✓ Kivy {kivy.__version__}")
        return True
    except ImportError:
        print("✗ Kivy не установлен")
        print("\nУстановите командой:")
        print("  pip install kivy")
        print("или")
        print("  pip install -r requirements.txt")
        return False

def main():
    print("=" * 50)
    print("iOS Keyboard Prototype - Dependency Check")
    print("=" * 50)
    print()
    
    checks = [
        check_python_version(),
        check_kivy()
    ]
    
    print()
    print("=" * 50)
    
    if all(checks):
        print("✓ Все зависимости установлены!")
        print("\nЗапустите клавиатуру командой:")
        print("  python keyboard_widget.py")
    else:
        print("⚠ Некоторые зависимости отсутствуют")
        print("Установите их перед запуском")
    
    print("=" * 50)

if __name__ == '__main__':
    main()

