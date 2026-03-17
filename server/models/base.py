# filepath: server/models/base.py
from . import db

class BaseModel(db.Model):
    """Abstract base model providing shared validation helpers for all SQLAlchemy models."""

    __abstract__ = True
    
    @staticmethod
    def validate_string_length(field_name: str, value: str | None, min_length: int = 2, allow_none: bool = False) -> str | None:
        """Validate that a string field meets minimum length requirements.

        Args:
            field_name: The display name of the field, used in error messages.
            value: The value to validate.
            min_length: Minimum number of non-whitespace characters required.
            allow_none: If True, a None value is accepted and returned as-is.

        Returns:
            The original value if validation passes.

        Raises:
            ValueError: If the value is None (when allow_none is False), not a string,
                        or shorter than min_length after stripping whitespace.
        """
        if value is None:
            if allow_none:
                return value
            else:
                raise ValueError(f"{field_name} cannot be empty")
        
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
            
        if len(value.strip()) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
            
        return value