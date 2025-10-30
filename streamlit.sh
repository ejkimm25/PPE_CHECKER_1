pip install streamlit
#python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0

# 2. DNS 및 네트워크 안정화 대기
echo "⏳ Waiting for network to stabilize..."
sleep 20

# 3️⃣ 네트워크 확인 (디버깅용)
echo "🌐 Checking DNS..."
nslookup pro-ppe-checker-func.azurewebsites.net || echo "DNS not ready yet"

# 3. Streamlit 실행
echo "🚀 Starting Streamlit app..."
python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0