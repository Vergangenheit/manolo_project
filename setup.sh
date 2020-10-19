mkdir -p ~/.streamlit/
echo "
[general]\n
email = \"m_macchetta@yahoo.com\"\n
" > ~/.streamlit/credentials.toml
echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n