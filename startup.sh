#!/bin/bash

# 1. 함수 실행
cd PPE_Function
python3.11 -m venv .venv
source .venv/bin/activate
func start &

# 2. Streamlit 실행
cd ..
python3.11 -m venv .venv
source .venv/bin/activated
streamlit run app.py --server.port=8000 --server.address=0.0.0.0
