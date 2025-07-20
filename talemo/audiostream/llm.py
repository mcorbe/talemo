from django.conf import settings
from litellm import acompletion

# os.environ['LITELLM_LOG'] = 'DEBUG'
# litellm._turn_on_debug()

async def stream_tokens(prompt: str, model: str | None = None):
    # Use the model from settings if not specified
    if model is None:
        model = getattr(settings, 'LLM_MODEL_NAME', 'gpt-4o')

    # Configure LiteLLM with the same settings
    resp = await acompletion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_base=settings.LLM_API_BASE,
        api_key=settings.LLM_API_KEY,
        stream=True,
        max_tokens=100,
        timeout=60,
    )

    async for chunk in resp:
        if delta := chunk.choices[0].delta:
            if content := delta.content:
                yield content
