from enum import Enum


# --- Enum classes ---
class Tags(str, Enum):
    """Enum for Invoice Generator tags."""

    TEST = "Test connection with the database, Redis and other services."
    INFO = "Info about the API"
    PET = "Profile evaluation"
    DATA = "Data from the API (SIPX and Imbalance data)"
