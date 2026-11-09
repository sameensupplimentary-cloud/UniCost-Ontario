import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="UniCost Ontario",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 UniCost Ontario")

st.subheader("Plan Your University Finances")
st.write("Estimate university expenses, explore scholarship funding, and discover how much your degree could cost in Ontario.")
st.info("Get started by selecting your university and program, then enter your estimated expenses and available funding.")
st.caption("UniCost Ontario is a financial planning tool for current and future Ontario university students.")

st.sidebar.header("Quick Start Guide")
st.sidebar.write("Step 1: Select your university and program.")
st.sidebar.write("Step 2: Enter your estimated expenses and available funding.")
st.sidebar.write("Step 3: Review your financial summary, yearly breakdown, and charts.")
st.divider()
st.header("Student Information")

name = st.text_input("What is your name?")
if name:
    st.write("Welcome,", name)

university = st.selectbox(
    "What University are you interested in?",
    ["Select a University", "University of Waterloo", "McMaster University", "Queen's University", "Western University", "Wilfrid Laurier University", "Toronto Metropolitan University", "University of Toronto", "York University", "Carleton University"]    
)
if university != "Select a University":
    st.write("You selected:", university)


program = st.selectbox(
    "What program are you interested in?",
    ["Select a program",
     "Accounting",
    "Arts",
    "Business",
    "Computer Science",
    "Commerce",
     "Engineering",
    "Geological Science",
    "Life science",
    "Mathematics",
    "Other"]
)
if program != "Select a program":
    st.write("You selected:", program)
tuition_estimates = {
    "University of Waterloo Mathematics": 9000,
    "University of Waterloo Engineering": 19000,
    "University of Waterloo Computer Science": 16000,
    "Carleton University Engineering": 12290.12,
    "Carleton University Computer Science": 10772.94,
    "Carleton University Mathematics": 7637.46
}

selection_key = university + " " + program
if "previous_selection" not in st.session_state:
    st.session_state["previous_selection"] = selection_key

suggested_tuition = 0.0
if selection_key in tuition_estimates:
    suggested_tuition= float(tuition_estimates[selection_key])
    st.write(f"Estimated annual tuition: ${suggested_tuition:,.2f}")
    st.caption("2026–27 first-year Ontario domestic tuition and fees. Fall 2027 rates may differ.")

    if university =="University of Waterloo":
        st.markdown("[Source: Waterloo Official Tuition Estimates](https://uwaterloo.ca/future-students/financing/tuition)")
    elif university == "Carleton University":
        st.markdown("[Source: Carleton Official Tuition Fees](https://carleton.ca/studentaccounts/tuition-fees/fw-ug/f26w27-ug-ontario/)")

elif university != "Select a University" and program != "Select a program":
    st.info("No tuition estimate available yet. Please enter your tuition manually below.")
if "tuition_input" not in st.session_state:
    st.session_state["tuition_input"] = suggested_tuition
if selection_key != st.session_state["previous_selection"]:
    st.session_state["tuition_input"] = suggested_tuition
    st.session_state["previous_selection"] = selection_key
st.divider()
st.header("Degree Information")
years = st.slider("How many years is your degree?", min_value=1, max_value=6, value=4)
st.write("Your degree is:", years, "years")

increase = st.slider("Expected annual cost increase (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.5)
st.write(f"Your expected annual cost increase is: {increase}%")

st.divider()
st.header("Annual University Expenses")

tuition = st.number_input("Enter your annual tuition: $", min_value =0.0, key="tuition_input")
st.caption("Enter your estimated tuition for one academic year, not the entire degree.")
if tuition:
    st.write("Your annual tuition is: $", tuition)
housing = st.number_input("Enter your annual housing costs: $", min_value = 0.0)
if housing:
    st.write("Your annual housing price is: $", housing)
food = st.number_input("Enter annual food expenses: $", min_value = 0.0)
if food:
    st.write("Your annual food price is $:", food)
transportation = st.number_input("Enter annual transportation expenses: $", min_value = 0.0)
if transportation:
    st.write("Your annual transportation price is $:", transportation)
textbooks = st.number_input("Enter annual textbooks expenses: $", min_value = 0.0)
if textbooks:
    st.write("Your annual textbooks price is $:", textbooks)

st.divider()
st.header("Available Funding")
scholarships = st.number_input("Enter your annual scholarship amount: $", min_value=0.0)
scholarship_renews = False 
if scholarships:
    st.write("Your available scholarship amount is $:", scholarships)
    scholarship_renews = st.checkbox("Will your scholarship renew every year?")
    if scholarship_renews:
        st.write("Your scholarship is renewable each year")
    else:
        st.write("Your scholarship is a one time award.")
income = st.number_input("Enter your annual available income amount: $", min_value=0.0)
st.caption("Enter the amount of income you expect to have available for university expenses each year.")
if income:
    st.write("Your available income is $:", income)
available_funding = scholarships + income   

totalcost = tuition + housing + food + transportation + textbooks

funding_gap = max(0, totalcost - available_funding)

st.divider()
st.header("Financial Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Annual Expenses", f"${totalcost:,.2f}")
with col2:    
    st.metric("Available Funding", f"${available_funding:,.2f}")
with col3:
    st.metric("Remaining Funding Gap", f"${funding_gap:,.2f}")

if totalcost ==0:
    st.info("Enter your estimated university expenses to get a meaningful financial summary.")
elif totalcost > available_funding:
    st.warning(f"You still need ${funding_gap:,.2f} to cover your expenses!")

elif available_funding > totalcost:
    surplus = available_funding - totalcost
    st.success(f"You have ${surplus:,.2f} extra left over! Good job.")

else:
    st.success("Your expenses and available funding are equal.")

st.divider()
st.header("Multi-Year cost Projection")
annual_cost = totalcost
degree_total = 0.0
chart_years =[]
chart_expenses = []
chart_funding = []
chart_gaps = []

for year in range(1, years + 1):
    if scholarship_renews or year ==1:
        yearly_scholarship = scholarships
    else: 
        yearly_scholarship = 0.0
    yearly_funding = yearly_scholarship + income
    yearly_gap = max(0, annual_cost - yearly_funding)
    chart_years.append(year)
    chart_expenses.append(annual_cost)
    chart_funding.append(yearly_funding)
    chart_gaps.append(yearly_gap)
    st.subheader(f"Year {year}")
    st.write(f"Year {year} scholarship: ${yearly_scholarship:,.2f}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Expenses", f"${annual_cost:,.2f}")
    with col2:
        st.metric("Available Funding", f"${yearly_funding:,.2f}")
    with col3:
        st.metric("Funding gap", f"${yearly_gap:,.2f}")


    degree_total += annual_cost
    annual_cost *= (1+ increase / 100)

st.metric("Total Degree Price", f"${degree_total:,.2f}")
st.divider()
st.header("Multi-Year Funding Projection")
if scholarship_renews:
    total_scholarships = scholarships * years
else: 
    total_scholarships = scholarships

total_income = income * years

total_funding = total_scholarships + total_income
st.metric("Total Funding", f"${total_funding:,.2f}")

degree_funding_gap = max(0, degree_total - total_funding)
st.metric("Total Funding Gap", f"${degree_funding_gap:,.2f}")
st.divider()
st.header("University Expenses vs. Available Funding")

chart_data = pd.DataFrame({
    "Year": chart_years,
    "Expenses": chart_expenses,
    "Available Funding": chart_funding,
    "Funding Gap": chart_gaps,
})
st.line_chart(chart_data, x="Year", y=["Expenses", "Available Funding"])
st.caption("This chart shows how estimated university expenses and available funding change each year")
st.caption("The expenses increase based on the student's selected annual percentage")
st.caption("Scholarships could be one time, or renewable")
st.caption("This assumes annual employment income stays the same.")
st.divider()
st.subheader("Yearly Funding Gap")
st.bar_chart(chart_data, x="Year", y=["Funding Gap"])
highest_gap = max(chart_gaps)
highest_gap_year = chart_gaps.index(highest_gap) + 1
st.caption("This Bar chart shows how much additional funding students may need each year")

st.metric("Highest Yearly Funding Gap", f"${highest_gap:,.2f}")

if highest_gap>0:
    st.info(f"Year {highest_gap_year} has the highest estimated funding gap.")
else:
    st.success("Your estimated funding covers your expenses in every year of your degree!")
st.divider()
st.header("Your Financial Outlook")

if degree_funding_gap >0:
    st.warning(f"Based on your estimates, you may need an additional ${degree_funding_gap:,.2f} to cover your entire {years}-year degree.")
else:
    st.success("Your estimated total funding covers your projected degree expenses! Check your yearly breakdown to make sure you have enough funding each year.")
st.divider()
st.header("Important Financial Assumptions")

st.write("These calculations are estimates intended to help students plan their university finances.")
st.caption("Actual university expenses and financial aid may differ from these estimates.")
st.caption("This program applies the selected percentage increase to all university expenses each year.")
st.caption("Renewable scholarships are assumed to continue every year, and available annual income is assumed to remain constant.")