def log_message(message: str) -> None:
    """Logs a message to the console."""
    print(f"[LOG] {message}")

def format_percentage(value: float) -> str:
    """Formats a float as a percentage string."""
    return f"{value:.2f}%"

def clean_data(data: list) -> list:
    """Cleans the input data by removing any empty entries."""
    return [entry for entry in data if entry]