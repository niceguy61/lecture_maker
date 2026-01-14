import sys
sys.path.insert(0, '.')

print("Starting import...")
try:
    from src.generators import korean_term_dictionary
    print(f"Import successful!")
    print(f"Has get_korean_term_dictionary: {hasattr(korean_term_dictionary, 'get_korean_term_dictionary')}")
    print(f"Module dict keys: {list(korean_term_dictionary.__dict__.keys())}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
