"""
Cognova Error Definitions.

This module defines the exception hierarchy used throughout Cognova.
All exceptions inherit from CognovaError and include exit codes for CLI usage.

Error Categories (see MASTER_SPEC.md Section 6):
- CognovaError (base, exit_code=1)
- UserInputError (exit_code=2)
  - ScenarioValidationError
  - ScenarioNotFoundError
  - InvalidYAMLError
  - SchemaVersionError
- APIError (exit_code=3)
  - APIAuthError
  - APIRateLimitError
  - APITimeoutError
  - APIConnectionError
- GenerationError (exit_code=4)
  - EmptyResponseError
  - OutputParseError
  - PromptTemplateError
- StorageError (exit_code=5)
  - MemvidError
  - FeedbackStorageError
  - HistoryStorageError
- ConfigurationError (exit_code=6)
  - ProjectNotInitializedError
  - ProjectConfigError

TODO: Implement error classes
"""

# Placeholder - implementation to follow
