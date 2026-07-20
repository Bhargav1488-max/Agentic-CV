import streamlit as st
from modules import config_loader

def render_sidebar():
    st.sidebar.header("⚙️ Configuration")
    
    providers = config_loader.get_providers()
    provider_names = list(providers.keys()) + ["Custom / Manual"]
    
    selected_provider = st.sidebar.selectbox("🤖 Provider", provider_names)
    
    if selected_provider == "Custom / Manual":
        custom_provider_name = st.sidebar.text_input("Custom Provider Name", "My_Provider")
        selected_model = st.sidebar.text_input("🧠 Model", "my-custom-model")
        api_key = st.sidebar.text_input("🔑 API Key", type="password")
        
        st.session_state["selected_provider"] = custom_provider_name
        st.session_state["selected_model"] = selected_model
        st.session_state["api_key"] = api_key
    else:
        provider_info = providers[selected_provider]
        models = provider_info.get("models", [])
        default_model = provider_info.get("default_model", "")
        
        default_idx = 0
        if default_model in models:
            default_idx = models.index(default_model)
            
        use_manual_model = st.sidebar.checkbox("Manually Enter Model")
        
        if use_manual_model:
            selected_model = st.sidebar.text_input("🧠 Model (Manual Entry)", default_model)
        else:
            selected_model = st.sidebar.selectbox("🧠 Model", models, index=default_idx)
            
        st.session_state["selected_provider"] = selected_provider
        st.session_state["selected_model"] = selected_model
        
        # API Key input
        env_key = provider_info.get("api_key_env", "")
        import os
        default_api_key = os.environ.get(env_key, "")
        
        api_key = st.sidebar.text_input("🔑 API Key", value=default_api_key, type="password")
        
        # For Azure OpenAI, we also need an endpoint and api_version
        if selected_provider == "Azure_OpenAI":
            endpoint = st.sidebar.text_input("🌐 Azure Endpoint URL", value=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://your-resource.openai.azure.com/"))
            api_version = st.sidebar.text_input("📅 API Version", value=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"))
            os.environ["AZURE_OPENAI_ENDPOINT"] = endpoint
            os.environ["AZURE_OPENAI_API_VERSION"] = api_version
            
        st.session_state["api_key"] = api_key
        
        if st.sidebar.button("🔌 Test Connection"):
            with st.spinner(f"Testing {selected_provider}..."):
                from modules.llm_engine import test_connection
                success, msg = test_connection(selected_provider, selected_model, api_key)
                if success:
                    st.sidebar.success(msg)
                else:
                    st.sidebar.error(f"Failed: {msg}")
        
    st.sidebar.divider()
    
    temperature = st.sidebar.slider("🌡️ Temperature", 0.0, 1.0, 0.7, 0.1)
    st.session_state["temperature"] = temperature
    
    languages = config_loader.get_languages()
    selected_lang = st.sidebar.radio("🌍 Language", languages)
    st.session_state["language"] = selected_lang
    
    templates = config_loader.get_templates()
    selected_template = st.sidebar.selectbox("🎨 CV Template", templates)
    st.session_state["template"] = selected_template
