import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from django.shortcuts import render
from openai import OpenAI
import os
# example in views.py

# then use openai.ChatCompletion.create(...) or new client syntax you use

# Initialize OpenAI
client = OpenAI(api_key="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")  # Use env variable in production

def predict_stock(request):
    prediction = None
    summary = None
    if request.method == 'POST':
        ticker = request.POST['ticker'].upper()
        data = yf.download(ticker, period='1y', interval='1d')

        data['Date'] = data.index
        data['Days'] = np.arange(len(data))
        X = data[['Days']]
        y = data['Close']

        model = LinearRegression()
        model.fit(X, y)

        future_days = 7
        future = np.arange(len(data), len(data) + future_days).reshape(-1, 1)
        future_pred = model.predict(future)

        future_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, future_days + 1)]
        prediction = zip(future_dates, future_pred)

        # Optional AI insight using OpenAI
        prompt = f"Analyze {ticker} stock trends and give short investment advice based on predicted upward or downward trend."
        ai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial market analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = ai_response.choices[0].message.content

    return render(request, 'index.html', {'prediction': prediction, 'summary': summary})
