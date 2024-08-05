import random
import string
from datetime import datetime


def generate_matricule(prefix='EL', length=10):
    """
    Generate a unique matricule with the specified prefix and length.

    Args:
        prefix (str): The prefix to include in the matricule (e.g., 'EL').
        length (int): The total length of the matricule, including the prefix.

    Returns:
        str: The generated matricule.
    """
    year = datetime.now().strftime('%y')  # Current year (last two digits)
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length - len(prefix) - len(year)))
    matricule = f"{prefix}{year}{random_suffix}"
    return matricule
