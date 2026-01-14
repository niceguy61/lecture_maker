import sys
sys.path.insert(0, '.')

try:
    import src.generators.korean_term_dictionary as ktd
    print(f"Module loaded successfully")
    print(f"Module attributes: {dir(ktd)}")
except Exception as e:
    print(f"Error loading module: {e}")
    import traceback
    traceback.print_exc()
