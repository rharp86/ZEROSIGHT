### utils/target_validator.py
import re

def validate_target(target: str) -> bool:
    """Validate that input is a proper domain or IP address."""
    target = target.strip()

    # Remove control characters like ^M (Carriage Return)
    target = re.sub(r'[\x00-\x1F\x7F]', '', target)

    # Simple heuristic for domain or IP validation
    return "." in target or ":" in target
