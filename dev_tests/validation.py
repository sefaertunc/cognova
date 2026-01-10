from aitestkit.config import get_settings

settings = get_settings()
print(f"API Key loaded: {settings.anthropic_api_key[:10]}...")
print(f"Code Gen Model: {settings.model_code_gen}")
print(f"Analysis Model: {settings.model_analysis}")
print(f"Regression Model: {settings.model_regression}")
print(f"\nTesting get_model_id method:")
print(f"  Opus: {settings.get_model_id('opus')}")
print(f"  Sonnet: {settings.get_model_id('sonnet')}")
print(f"  Haiku: {settings.get_model_id('haiku')}")
