from src.utils import safe_pct
def test_safe_pct(): assert safe_pct(25,100)==25 and safe_pct(1,0)==0
