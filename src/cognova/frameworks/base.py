"""
Base framework interface for test generation.

This module provides the base interface that all framework adapters should implement.
Currently, the framework system uses a data-driven approach with FrameworkInfo,
but this module is reserved for future extensions.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class FrameworkAdapter(ABC):
    """
    Base adapter interface for framework-specific behavior.

    This is currently not used but reserved for future extensions where
    frameworks may need custom validation, parsing, or post-processing logic.
    """

    @abstractmethod
    def validate_output(self, code: str) -> list[str]:
        """
        Validate generated code for framework-specific requirements.

        Args:
            code: The generated test code

        Returns:
            List of validation issues (empty if valid)
        """
        pass

    @abstractmethod
    def get_suggested_filename(self, scenario: str) -> str:
        """
        Get suggested filename for the test based on the scenario.

        Args:
            scenario: The test scenario description

        Returns:
            Suggested filename
        """
        pass

    @abstractmethod
    def post_process(self, code: str) -> str:
        """
        Post-process generated code (formatting, imports, etc.).

        Args:
            code: The generated test code

        Returns:
            Post-processed code
        """
        pass
