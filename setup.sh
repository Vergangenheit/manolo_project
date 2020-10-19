mkdir -p ~/.streamlit/
echo "[general]
email = \"m_macchetta@yahoo.com\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml