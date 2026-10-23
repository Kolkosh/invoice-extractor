import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from schema import Invoice
from dataset import DATASET

for case in DATASET:
    inv = Invoice(**case["expected"])
    items_sum = sum(i.quantity * i.unit_price for i in inv.items)
    flag = "" if abs(items_sum - inv.total) < 0.01 else "   <-- ловушка: сумма позиций не равна итогу"
    print(f"{case['id']:<28} позиций: {len(inv.items)}  по строкам: {items_sum:>9.2f}  итого: {inv.total:>9.2f}{flag}")