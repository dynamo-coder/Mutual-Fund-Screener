from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Read the data from CSV file
data = pd.read_csv('mf.csv')

def filter_funds(category):
    filtered_funds = data[
        (data['Sub Category'] == category) &
        (data['CAGR 3Y'] > 0) &
        (data['CAGR 5Y'] > 0) &
        (data['Sharpe Ratio'] > 0) &
        (data['Alpha'] > 0) &
        (data['Plan'] == 'Growth') &
        (data['Expense Ratio'] <= 1.5) &
        (data['Minimum Lumpsum'] > 0) &  
        (data['Minimum Lumpsum'] <= 100)
    ]
    return filtered_funds.nlargest(10, 'CAGR 3Y')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form['category']
        filtered_funds = filter_funds(category)
        funds_list = filtered_funds.to_dict('records')  # Convert DataFrame to list of dictionaries
        return render_template('result.html', funds=funds_list)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
