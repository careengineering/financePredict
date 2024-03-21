import streamlit as st
import yfinance as yf
import datetime
from prophet import Prophet


def financePredict(type,day_before,day_after):
    date_before = datetime.timedelta(days=day_before)
    today = datetime.date.today()
    after_day = (day_after - today).days

    df = yf.download(type, today - date_before, today)
    if df.empty:
        st.write("No datas found...")
        st.stop()
    else: 
        df = df.reset_index()
        df = df[["Date", "Close"]]
        df.columns = ["ds", "y"]

        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(after_day)
        predict = model.predict(future)
        yhat = predict.iloc[-1]["yhat"]
        st.caption("Prediction for " + day_after.strftime("%d-%m-%Y") + " is " +  str(round(yhat,2))+" $")
        model.plot(predict);


def get_keys_by_value(d, value):
    reverse_dict = {v: k for k, v in d.items()}
    if value in reverse_dict:
        return reverse_dict[value]
    else:
        return None


tickers = {
    "AAPL": "Apple Inc.",
    "RDDT": "Reddit, Inc.",
    "MU": "Micron Technology, Inc.",
    "AVGO": "Broadcom Inc.",
    "ACN": "Accenture plc",
    "PARA": "Paramount Global",
    "KAVL": "Kaival Brands Innovations Group, Inc.",
    "FIVE": "Five Below, Inc.",
    "ATD.TO": "Alimentation Couche-Tard Inc.",
    "BAC": "Bank of America Corporation",
    "GC=F": "Gold Apr 24",
    "SOXL": "Direxion Daily Semiconductor Bull 3X Shares",
    "LU": "Lufax Holding Ltd",
    "^DJI": "Dow Jones Industrial Average",
    "YTEN": "Yield10 Bioscience, Inc.",
    "LRCX": "Lam Research Corporation",
    "ALAB": "Astera Labs, Inc.",
    "NA.TO": "National Bank of Canada",
    "WDC": "Western Digital Corporation",
    "HD": "The Home Depot, Inc.",
    "AMTX": "Aemetis, Inc.",
    "CNR.TO": "Canadian National Railway Company",
    "CURI": "CuriosityStream Inc.",
    "CHWY": "Chewy, Inc.",
    "ASO": "Academy Sports and Outdoors, Inc.",
    "PYPL": "PayPal Holdings, Inc.",
    "GS": "The Goldman Sachs Group, Inc.",
    "VRT": "Vertiv Holdings Co",
    "BROS": "Dutch Bros Inc.",
    "WOLF": "Wolfspeed, Inc.",
    "TRY=X" : "USD/TRY",
    "EURTRY=X" : "EUR/TRY",
    "OOOO" : "Other"
}

st.sidebar.header("Financial Prediction with AI")

type_name =st.sidebar.selectbox("Choose What to Predict",tickers.values())

type_symbol = ""
if type_name == "Other":
    type_symbol = st.sidebar.text_input("Submit YFinance Symbol")
    st.subheader(type_name+" - "+type_symbol)
else: 
    type_symbol = get_keys_by_value(tickers,type_name)
    st.subheader(type_name)

day_before = st.sidebar.number_input("How many days backward do you want to use for prediction?",value=10000)
day_after = st.sidebar.date_input("Prediction Date", format="DD/MM/YYYY")

if type_symbol != "":
    x = financePredict(type_symbol,day_before,day_after)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(x)

