import os
import yfinance as yf
import pandas as pd
from git import Repo  # Git 제어를 위한 라이브러리

# 1. 티커 리스트 정의
tickers = ['NVDA', 'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'AVGO', 'TSLA', 'META', 'MU', 'LLY', 'WMT', 'JPM']
stock_data = []

print("1. 야후 파이낸스에서 실시간 데이터를 가져오는 중...")
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        fast_info = stock.fast_info
        
        symbol = ticker
        name = info.get('longName', 'N/A')
        market_cap = info.get('marketCap', 0)
        price = fast_info.get('lastPrice') or info.get('regularMarketPrice', 0)
        prev_close = info.get('regularMarketPreviousClose')
        
        if price and prev_close:
            change_percent = ((price - prev_close) / prev_close) * 100
        else:
            change_percent = 0.0

        stock_data.append({
            'Symbol': symbol,
            'Name': name,
            'Market Cap (USD)': market_cap,
            'Price ($)': round(price, 2) if price else 0,
            'Change %': round(change_percent, 2)
        })
    except Exception as e:
        print(f"{ticker} 오류 발생: {e}")

# 2. DataFrame 생성 및 시가총액 기준 내림차순 정렬
df = pd.DataFrame(stock_data)
df_sorted = df.sort_values(by='Market Cap (USD)', ascending=False).reset_index(drop=True)

# 3. HTML 테이블 행(Row) 문자열 동적 생성
table_rows = ""
for _, row in df_sorted.iterrows():
    is_positive = row['Change %'] >= 0
    color = '#d21926' if is_positive else '#117a3a'  # 상승 빨강, 하락 초록
    sign = '+' if is_positive else ''
    
    formatted_market_cap = f"${row['Market Cap (USD)']:,.0f}"
    
    table_rows += f"""
    <tr>
        <td class="symbol">{row['Symbol']}</td>
        <td class="name">{row['Name']}</td>
        <td>${row['Price ($)']:.2f}</td>
        <td style="color: {color}; font-weight: 600;">{sign}{row['Change %']:.2f}%</td>
        <td>{formatted_market_cap}</td>
    </tr>
    """

# 4. 전체 index.html 파일 뼈대 작성
html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>미국 주식 시가총액 대시보드</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f6f8fa; margin: 0; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 24px; margin-bottom: 5px; color: #24292f; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; margin-top: 15px; }}
        th, td {{ padding: 12px 15px; border-bottom: 1px solid #d0d7de; }}
        th {{ background-color: #f6f8fa; color: #57606a; font-weight: 600; }}
        tr:hover {{ background-color: #f3f4f6; }}
        .symbol {{ font-weight: bold; color: #0969da; }}
        .name {{ color: #24292f; max-width: 250px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    </style>
</head>
<body>
<div class="container">
    <h1>미국 주식 시가총액 TOP 12 (실시간 정렬)</h1>
    <table>
        <thead>
            <tr>
                <th>Symbol</th>
                <th>Name</th>
                <th>Price</th>
                <th>Change %</th>
                <th>Market Cap</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</div>
</body>
</html>
"""

# 5. 로컬 저장소 폴더에 index.html 저장
html_filename = "index.html"
with open(html_filename, "w", encoding="utf-8") as f:
    f.write(html_template)
print("2. 로컬 index.html 파일 생성 완료.")

# 6. Git을 사용하여 GitHub 저장소로 자동 Push
try:
    print("3. GitHub 저장소로 자동 푸시 시작...")
    repo_path = os.getcwd()  # 현재 파이썬 코드가 실행 중인 폴더 위치
    repo = Repo(repo_path)
    
    # 변경된 index.html 스테이징 및 커밋
    repo.git.add(html_filename)
    repo.index.commit("클라우드 우회 - 파이썬 기반 주가 데이터 자동 업데이트")
    
    # 원격 저장소(GitHub)로 푸시
    origin = repo.remote(name='origin')
    origin.push()
    print("4. GitHub Pages 업데이트 최종 성공 완료!")
    
except Exception as git_error:
    print(f"Git 푸시 중 오류 발생 (로컬 커밋은 완료됨): {git_error}")