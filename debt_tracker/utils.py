import uuid

def generate_transaction_id():
    """
    Generate a unique transaction ID.
    """
    # Use UUID (Universally Unique Identifier) to generate a random ID
    transaction_id = uuid.uuid4().hex[:10]  # Extract first 10 characters of the UUID
    return transaction_id
