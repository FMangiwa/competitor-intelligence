import json
from openai import OpenAI
import config
from scraper import fetch_website_links, fetch_website_contents  # Utility functions

def get_llm_client(provider="OpenAI"):
    """
    Returns an OpenAI client configured for OpenAI, Google Gemini, or Ollama.
    """
    if provider == "Gemini":
        return OpenAI(base_url=config.GEMINI_BASE_URL, api_key=config.GOOGLE_API_KEY)
    elif provider == "Ollama":
        return OpenAI(base_url=config.OLLAMA_BASE_URL, api_key="ollama")
    else:
        return OpenAI(api_key=config.OPENAI_API_KEY)

def select_relevant_links(url, client, model=config.DEFAULT_OPENAI_MODEL):
    """
    Fetches links from a target site and uses an LLM with JSON output formatting 
    to filter out unwanted links (ToS, privacy, emails).
    """
    raw_links = fetch_website_links(url)
    user_prompt = f"Links found on {url}:\n" + "\n".join(raw_links)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": config.LINK_SELECTION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    return result.get("links", [])

def assemble_website_context(url, client, model=config.DEFAULT_OPENAI_MODEL):
    landing_content = fetch_website_contents(url)
    relevant_links = select_relevant_links(url, client, model)
    
    context = f"## Landing Page:\n{landing_content}\n\n## Relevant Sub-pages:\n"
    for link in relevant_links:
        # Safely extract 'url', defaulting to empty string if missing or None
        link_url = link.get("url") if isinstance(link, dict) and link.get("url") else ""
        
        # Verify link_url is a string and starts with http:// or https://
        if isinstance(link_url, str) and (link_url.startswith("http://") or link_url.startswith("https://")):
            content = fetch_website_contents(link_url)
            if content:
                context += f"\n### Link ({link.get('type', 'sub-page')}): {link_url}\n"
                context += content
        
    return context[:config.MAX_CONTENT_CHARS]

def stream_prospectus(company_name, url, tone="Professional", provider="OpenAI", model=config.DEFAULT_OPENAI_MODEL):
    """
    Generates a streamed summary/prospectus report chunk by chunk.
    """
    client = get_llm_client(provider)
    site_context = assemble_website_context(url, client, model)
    
    system_prompt = config.BROCHURE_SYSTEM_PROMPTS.get(tone, config.BROCHURE_SYSTEM_PROMPTS["Professional"])
    user_prompt = f"Company: {company_name}\nWebsite Content:\n{site_context}"

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=True
    )
    
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        yield content