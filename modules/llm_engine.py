import os
import requests
import json
import google.generativeai as genai
from groq import Groq
import cohere

def generate_text(provider, model, prompt, api_key, temperature=0.7):
    if not api_key:
        return f"Error: API key for {provider} is missing."
        
    try:
        if provider == "Google_Gemini":
            genai.configure(api_key=api_key)
            # Use GenerativeModel directly
            gemini_model = genai.GenerativeModel(model)
            response = gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                )
            )
            # Gemini might not have simple token counts in this API version, default 0
            return response.text, 0, 0
            
        elif provider == "Groq":
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            usage = completion.usage
            in_tokens = usage.prompt_tokens if usage else 0
            out_tokens = usage.completion_tokens if usage else 0
            return completion.choices[0].message.content, in_tokens, out_tokens
            
        elif provider == "Cohere":
            co = cohere.Client(api_key=api_key)
            response = co.generate(
                prompt=prompt,
                model=model,
                temperature=temperature
            )
            # Cohere meta for billing contains token counts depending on API version
            return response.generations[0].text, 0, 0
            
        elif provider == "GitHub_Models":
            # Using OpenAI compatible endpoint
            from openai import OpenAI
            client = OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=api_key
            )
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            usage = completion.usage
            in_tokens = usage.prompt_tokens if usage else 0
            out_tokens = usage.completion_tokens if usage else 0
            return completion.choices[0].message.content, in_tokens, out_tokens
            
        elif provider == "NVIDIA_NIM":
            from openai import OpenAI
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key
            )
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            usage = completion.usage
            in_tokens = usage.prompt_tokens if usage else 0
            out_tokens = usage.completion_tokens if usage else 0
            return completion.choices[0].message.content, in_tokens, out_tokens
            
        elif provider == "OpenRouter":
            headers = {
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://github.com/your-repo/job-app-assistant",
                "X-Title": "Job App Assistant"
            }
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            }
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            res_json = response.json()
            usage = res_json.get("usage", {})
            return res_json["choices"][0]["message"]["content"], usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
            
        elif provider == "Azure_OpenAI":
            from openai import AzureOpenAI
            import httpx
            endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/")
            api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
            
            # Use httpx client with verify=False to bypass corporate proxy self-signed cert issues
            http_client = httpx.Client(verify=False)
            
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version,
                http_client=http_client
            )
            # For Azure, model maps to the deployment name
            completion = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            usage = completion.usage
            in_tokens = usage.prompt_tokens if usage else 0
            out_tokens = usage.completion_tokens if usage else 0
            return completion.choices[0].message.content, in_tokens, out_tokens
            
        else:
            return f"Provider {provider} not supported or implemented.", 0, 0
            
    except Exception as e:
        return f"Error with {provider}: {str(e)}", 0, 0

def test_connection(provider, model, api_key):
    """Simple connection test sending a 'Hello' prompt."""
    try:
        response, _, _ = generate_text(provider, model, "Hello, are you there? Reply with exactly 'Yes'.", api_key, temperature=0.1)
        if response.startswith("Error"):
            return False, response
        return True, "Connection successful! " + response
    except Exception as e:
        return False, str(e)

