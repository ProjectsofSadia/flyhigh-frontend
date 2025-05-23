import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from fpdf import FPDF
from datetime import datetime


df = pd.read_csv("FlyHigh_Airline_NoShow_Data.csv")
st.set_page_config(page_title="FlyHigh.AI", layout="wide")
st.title("✈️ FlyHigh.AI - Airline Overbooking Optimizer")
st.subheader("Predict no-shows & supercharge airline revenue")
st.sidebar.header("🔍 Explore the Data")
if st.sidebar.checkbox("Show raw data"):
    st.write(df.head())

st.header("📊 Exploratory Data Analysis")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(df, x='TicketPrice', color='NoShow', nbins=30,
                        title="Ticket Price Distribution by No-Show Status")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.box(df, x='SeatClass', y='TicketPrice', color='NoShow',
                  title="Seat Class vs Ticket Price")
    st.plotly_chart(fig2, use_container_width=True)

df_encoded = pd.get_dummies(df.drop(['BookingID', 'PassengerName', 'FlightDate'], axis=1), drop_first=True)
X = df_encoded.drop('NoShow', axis=1)
y = df_encoded['NoShow']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
y_pred = model.predict(X_test)

st.header("🧠 Model Performance")
st.markdown(f"**Random Forest Accuracy:** `{accuracy * 100:.2f}%`")

st.markdown("**Confusion Matrix:**")
cm = confusion_matrix(y_test, y_pred)
st.write(pd.DataFrame(cm, columns=["Predicted No", "Predicted Yes"], index=["Actual No", "Actual Yes"]))

st.markdown("**Classification Report:**")
st.text(classification_report(y_test, y_pred))
st.header("🧾 Try It Yourself: Predict & Book a Flight")

with st.form(key='predict_form'):
    col1, col2 = st.columns(2)
    with col1:
        departure = st.selectbox("Departure City", df["DepartureCity"].unique())
        arrival = st.selectbox("Arrival City", df["ArrivalCity"].unique())
        price = st.slider("Ticket Price", 100, 1000, 300)
        seat_class = st.selectbox("Seat Class", df["SeatClass"].unique())
        reschedule_date = st.date_input("Select Flight Date", value=pd.to_datetime("2025-06-01"))
        reschedule_time = st.time_input("Select Flight Time", value=datetime.now().time())
    with col2:
        flyer = st.selectbox("Frequent Flyer", [1, 0])
        days_before = st.slider("Booking Advance Days", 1, 60, 20)
        checked_in = st.selectbox("Checked In?", [1, 0])
        passenger_name = st.text_input("Passenger Name")

    submit = st.form_submit_button("Predict & Generate Ticket")

if submit:
    input_data = {
        'TicketPrice': price,
        'FrequentFlyer': flyer,
        'BookingAdvanceDays': days_before,
        'CheckedIn': checked_in,
        f"DepartureCity_{departure}": 1,
        f"ArrivalCity_{arrival}": 1,
        f"SeatClass_{seat_class}": 1
    }

    input_df = pd.DataFrame([input_data])
    for col in X.columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[X.columns]

    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    st.success(f"Prediction: {'❌ Will No-Show' if prediction else '✅ Will Show Up'} ({prob*100:.1f}% chance)")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="FlyHigh.AI Ticket Confirmation", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Passenger: {passenger_name}", ln=True)
    pdf.cell(200, 10, txt=f"From: {departure}  ➜  To: {arrival}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {reschedule_date}  Time: {reschedule_time}", ln=True)
    pdf.cell(200, 10, txt=f"Seat Class: {seat_class} | Price: ${price}", ln=True)
    pdf.cell(200, 10, txt=f"Prediction: {'No-Show ❌' if prediction else 'Will Show ✅'}", ln=True)
    pdf.cell(200, 10, txt=f"Probability: {prob:.2%}", ln=True)

    pdf_output = "FlyHigh_Ticket.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as file:
        st.download_button(label="📄 Download Ticket (PDF)", data=file, file_name="FlyHigh_Ticket.pdf")

st.header("💬 Feedback")
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    comments = st.text_area("What do you think of FlyHigh?")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("Thank you! Feedback received 💙")
    with open("feedback_log.txt", "a") as f:
        f.write(f"\n{name}: {comments}")
