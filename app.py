import streamlit as st
from datetime import date

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Financial Safety Simulator",
    layout="centered"
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "events" not in st.session_state:
    st.session_state.events = []

# -----------------------------
# HEADER WITH LOGO
# -----------------------------
col1, col2 = st.columns([1, 6])

with col1:
    st.image("logo.jpg", width=60)

with col2:
    st.title("Financial Safety Simulator")
    st.caption(
        "Most financial stress comes from timing — not totals. "
        "This tool helps you see that before it happens."
    )

# -----------------------------
# SECTION 1 — CURRENT SITUATION
# -----------------------------
st.markdown("### Your current situation")

balance = st.number_input(
    "Current balance ($)",
    min_value=0.0,
    step=50.0
)

buffer = st.number_input(
    "Safety buffer ($)",
    min_value=0.0,
    step=50.0,
    help="This is the level where money usually starts to feel stressful."
)

st.divider()

# -----------------------------
# SECTION 2 — BILLS & INCOME
# -----------------------------
st.markdown("### What’s already coming")
st.caption("Bills and income you expect no matter what.")

# ---- Bills ----
st.markdown("**Bills**")

bill_name = st.text_input(
    "Bill name",
    placeholder="Rent, credit card, utilities"
)

bill_amount = st.number_input(
    "Bill amount ($)",
    min_value=0.0,
    step=25.0,
    key="bill_amount"
)

bill_date = st.date_input(
    "Bill due date",
    key="bill_date"
)

if st.button("Add bill"):
    if bill_amount > 0:
        st.session_state.events.append({
            "date": bill_date,
            "amount": -bill_amount,
            "label": bill_name or "Bill"
        })

# ---- Income ----
st.markdown("**Income**")

income_name = st.text_input(
    "Income source",
    placeholder="Paycheck"
)

income_amount = st.number_input(
    "Income amount ($)",
    min_value=0.0,
    step=50.0,
    key="income_amount"
)

income_date = st.date_input(
    "Income date",
    key="income_date"
)

if st.button("Add income"):
    if income_amount > 0:
        st.session_state.events.append({
            "date": income_date,
            "amount": income_amount,
            "label": income_name or "Income"
        })

st.divider()

# -----------------------------
# SECTION 3 — OPTIONAL PURCHASE
# -----------------------------
st.markdown("### Thinking about a purchase?")
st.caption("Optional — just to see the impact. Nothing is saved.")

consider_amount = st.number_input(
    "About how much would it be?",
    min_value=0.0,
    step=25.0
)

consider_date = st.date_input(
    "When would it happen?",
    value=date.today()
)

if consider_amount > 0:
    st.session_state.events.append({
        "date": consider_date,
        "amount": -consider_amount,
        "label": "Optional purchase"
    })

st.divider()

# -----------------------------
# EVENT PREVIEW
# -----------------------------
if st.session_state.events:
    st.markdown("### Upcoming items")
    for e in sorted(st.session_state.events, key=lambda x: x["date"]):
        sign = "+" if e["amount"] > 0 else "-"
        st.write(f"{e['date']} — {e['label']} ({sign}${abs(e['amount']):,.2f})")

st.divider()

# -----------------------------
# SIMULATION
# -----------------------------
if st.button("Simulate"):
    if not st.session_state.events:
        st.warning("Add at least one bill or income to simulate.")
    else:
        events = sorted(st.session_state.events, key=lambda x: x["date"])

        running_balance = balance
        lowest_balance = balance
        lowest_date = None

        for event in events:
            running_balance += event["amount"]
            if running_balance < lowest_balance:
                lowest_balance = running_balance
                lowest_date = event["date"]

        st.markdown("### Result")

        st.write(
            f"**Lowest balance before money arrives:** "
            f"${lowest_balance:,.2f}"
        )

        if lowest_date:
            st.write(f"**When it happens:** {lowest_date}")

        st.divider()

        # Status + explanation
        if lowest_balance >= buffer:
            st.success("You stay above your safety buffer. This looks manageable.")
            summary = f"You remain safe through {lowest_date}."

        elif lowest_balance > 0:
            st.warning("This gets tight before your next income.")
            summary = f"Things become tight around {lowest_date}."

        else:
            st.error("This would push your balance below zero before money arrives.")
            summary = f"You would run into trouble around {lowest_date}."

        st.markdown("### Summary")
        st.write(summary)

        st.caption(
            "This app doesn’t move money or track anything. "
            "It only shows what would happen based on timing."
        )

# -----------------------------
# LOCKED FEATURE (MONETIZATION SIGNAL)
# -----------------------------
st.divider()
st.markdown("### Coming soon")

if st.button("💾 Save this scenario"):
    st.info(
        "🔒 Saving scenarios will be available in a future version.\n\n"
        "This will let you compare decisions over time."
    )
