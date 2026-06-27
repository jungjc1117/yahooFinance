import yfinance as yf
import pandas as pd

# [테이블 1] 주요 지수/선물/환율 매핑 (새로 추가된 항목)
index_map = {
    "CL=F": {"name": "원유값"},
    "^SOX": {"name": "필라델피아지수"},
    "^VIX": {"name": "VIX"},
    "^DJI": {"name": "다우"},
    "^IXIC": {"name": "나스닥"},
    "^GSPC": {"name": "S&P500"},
    "EWY": {"name": "MSCI지수"},
    "KRW=X": {"name": "환율"},
    "^KS11": {"name": "KOSPI"},
    "^KQ11": {"name": "KOSDAQ"},
    "^KS200": {"name": "KOSPI200선물"},
    "^KQ150": {"name": "KOSDAQ150선물"}
}

# [테이블 2] 기존 테마 및 티커 매핑
theme_map = {
    "MU": {"theme": "메모리반도체/HBM/D램", "name": "Micron Technology"},
    "NVDA": {"theme": "시스템반도체", "name": "NVIDIA"},
    "RMBS": {"theme": "CXL", "name": "Rambus"},
    "AMAT": {"theme": "유리기판", "name": "Applied Materials"},
    "CBRS": {"theme": "퓨리오사AI", "name": "Cerebras"},
    "MSFT": {"theme": "ChatGPT(AI)", "name": "Microsoft"},
    "IONQ": {"theme": "양자컴퓨터", "name": "IonQ"},
    "SDGR": {"theme": "AI신약개발", "name": "Schrodinger"},
    "LLY": {"theme": "제약/비만치료제", "name": "Eli Lilly"},
    "PFE": {"theme": "바이오시밀러", "name": "Pfizer"},
    "TSLA": {"theme": "2차전지/ESS/전기차", "name": "Tesla"},
    "QS": {"theme": "전고체배터리", "name": "QuantumScape"},
    "ALB": {"theme": "리튬", "name": "Albemarle"},
    "GEV": {"theme": "전력설비", "name": "GE Vernova"},
    "ETN": {"theme": "변압기", "name": "Eaton Corporation"},
    "CEG": {"theme": "원전", "name": "Constellation Energy"},
    "SMR": {"theme": "SMR", "name": "NuScale Power"},
    "CHPT": {"theme": "전기차인프라", "name": "ChargePoint"},
    "GOOGL": {"theme": "자율주행", "name": "Alphabet"},
    "MRAY": {"theme": "MLCC", "name": "Murata Manufacturing"},
    "ISRG": {"theme": "지능형로봇", "name": "Intuitive Surgical"},
    "LMT": {"theme": "방산", "name": "Lockheed Martin"},
    "RTX": {"theme": "우주/항공", "name": "RTX Corporation"},
    "HII": {"theme": "조선", "name": "Huntington Ingalls"},
    "CAT": {"theme": "조선기자재", "name": "Caterpillar"},
    "AA": {"theme": "알루미늄", "name": "Alcoa"},
    "FCX": {"theme": "구리", "name": "Freeport-McMoRan"},
    "AMSC": {"theme": "초전도체", "name": "American Superconductor"},
    "CRWD": {"theme": "인터넷 보안", "name": "CrowdStrike"},
    "CSCO": {"theme": "통신장비", "name": "Cisco Systems"},
    "DLR": {"theme": "데이터센터", "name": "Digital Realty"},
    "VRT": {"theme": "액침냉각", "name": "Vertiv Holdings"},
    "COIN": {"theme": "스테이블코인", "name": "Coinbase"},
    "IONQ": {"theme": "양자컴퓨터", "name": "IONQ"},
    "GLW": {"theme": "유리기판", "name": "Corning"},
    "COHR": {"theme": "광통신", "name": "Coherent"},
}

# 1. 데이터 수집 통합 실행
index_tickers = list(index_map.keys())
stock_tickers = list(theme_map.keys())

index_data = []
stock_data = []

print("야후 파이낸스에서 실시간 데이터를 받아오는 중...")

# [처리 1] 주요 지수/선물/환율 파싱
for ticker in index_tickers:
    try:
        stock = yf.Ticker(ticker)
        fast_info = stock.fast_info
        info = stock.info
        
        price = fast_info.get('lastPrice') or info.get('regularMarketPrice', 0)
        prev_close = info.get('regularMarketPreviousClose')
        
        change_percent = ((price - prev_close) / prev_close) * 100 if price and prev_close else 0.0
        
        index_data.append({
            'Name': index_map[ticker]['name'],
            'Price': price,
            'Change_Percent': round(change_percent, 2)
        })
    except Exception as e:
        print(f"지수 {ticker} 에러 발생 (N/A 처리): {e}")

# [처리 2] 기존 주식 테마 파싱
for ticker in stock_tickers:
    try:
        stock = yf.Ticker(ticker)
        fast_info = stock.fast_info
        info = stock.info
        
        price = fast_info.get('lastPrice') or info.get('regularMarketPrice', 0)
        prev_close = info.get('regularMarketPreviousClose')
        
        change_percent = ((price - prev_close) / prev_close) * 100 if price and prev_close else 0.0
        
        stock_data.append({
            'Symbol': ticker,
            'Name': theme_map[ticker]['name'],
            'Theme': theme_map[ticker]['theme'],
            'Price': price,
            'Change_Percent': round(change_percent, 2)
        })
    except Exception as e:
        print(f"종목 {ticker} 에러 무시: {e}")

# 2. 데이터프레임 생성 및 각각 상승률 기준 내림차순 정렬
df_index = pd.DataFrame(index_data).reset_index(drop=True)
df_stock = pd.DataFrame(stock_data).sort_values(by='Change_Percent', ascending=False).reset_index(drop=True)

# 3. HTML 테이블 생성 1 - 주요 지수 테이블
index_rows = ""
for _, row in df_index.iterrows():
    is_positive = row['Change_Percent'] >= 0
    color = '#d21926' if is_positive else '#117a3a'
    sign = '+' if is_positive else ''
    
    # 환율이나 원유값 등에 맞게 소수점 포맷 조절
    formatted_price = f"{row['Price']:,.0f}"
    
    index_rows += f"""
    <tr>
        <td class="name" style="font-weight: 600;">{row['Name']}</td>
        <td style="color: {color}; font-weight: bold;">{sign}{row['Change_Percent']:.2f}%</td>
        <td class="price">{formatted_price}</td>
    </tr>
    """

# 4. HTML 테이블 생성 2 - 테마 주식 테이블
stock_rows = ""
for _, row in df_stock.iterrows():
    is_positive = row['Change_Percent'] >= 0
    color = '#d21926' if is_positive else '#117a3a'
    sign = '+' if is_positive else ''
    
    stock_rows += f"""
    <tr>
        <td class="theme">{row['Theme']} <span class="theme-change" style="color: {color};">({sign}{row['Change_Percent']:.2f}%)</span></td>
        <!--
        <td class="symbol">{row['Symbol']}</td>
        <td class="name">{row['Name']}</td>
        <td class="price">${row['Price']:.0f}</td>
        -->
    </tr>
    """

# 5. 복합 대시보드 웹 디자인 뼈대 생성
html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>종합 시장 동향 & 테마 대시보드</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f6f8fa; margin: 0; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 24px; margin-bottom: 20px; color: #24292f; text-align: center; font-weight: 700; }}
        h2 {{ font-size: 18px; margin-top: 30px; margin-bottom: 10px; color: #0969da; border-left: 4px solid #0969da; padding-left: 10px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; margin-bottom: 20px; }}
        th, td {{ padding: 12px 15px; border-bottom: 1px solid #d0d7de; }}
        th {{ background-color: #f6f8fa; color: #57606a; font-weight: 600; }}
        tr:hover {{ background-color: #f3f4f6; }}
        .theme {{ font-weight: 600; color: #24292f; }}
        .theme-change {{ font-size: 13px; font-weight: bold; margin-left: 5px; }}
        .symbol {{ font-weight: bold; color: #0969da; }}
        .name {{ color: #24292f; max-width: 220px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .price {{ font-weight: 500; text-align: right; }}
    </style>
</head>
<body>
<div class="container">
    <h1>글로벌 금융 시장 종합 대시보드</h1>
    
    <h2>📊 주요 시장 지수 및 지표 (상승률순)</h2>
    <table>
        <thead>
            <tr>
                <th>구분</th>
                <th>등락률</th>
                <th style="text-align: right;">현재가</th>
            </tr>
        </thead>
        <tbody>
            {index_rows}
        </tbody>
    </table>

    <h2>대표 종목 (상승률순)</h2>
    <table>
        <thead>
            <tr>
                <th>테마명 (상승률)</th>
                <!--
                <th>티커 (Symbol)</th>
                <th>종목명</th>
                <th style="text-align: right;">현재가</th>
                -->
            </tr>
        </thead>
        <tbody>
            {stock_rows}
        </tbody>
    </table>
</div>
</body>
</html>
"""

# 6. index.html로 최종 내보내기
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)
print("지표 및 주가 통합 대시보드 index.html 업데이트 완료.")