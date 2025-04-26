_receipts_store = {}

def store_points(receipt_id, points):
    _receipts_store[receipt_id] = points

def get_points(receipt_id):
    return _receipts_store.get(receipt_id)