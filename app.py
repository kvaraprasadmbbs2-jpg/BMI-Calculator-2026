```python
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="BMI + BMR + TDEE Calculator",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM MOBILE-FRIENDLY CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        max-width: 700px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Main title */
    h1 {
        text-align: center;
        font-size: 2rem !important;
        margin-bottom: 0.3rem;
    }

    /* Section headings */
    h2 {
        font-size: 1.35rem !important;
        margin-top: 1.5rem;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        min-height: 3rem;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 10px;
    }

    /* Input fields */
    div[data-baseweb="input"] input {
        font-size: 1rem;
    }

    /* Select boxes */
    div[data-baseweb="select"] {
        font-size: 1rem;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        padding: 0.5rem 0;
    }

    /* Success / warning / error boxes */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.title("🩺 BMI + BMR + TDEE Calculator")

st.markdown(
    "<p style='text-align:center;'>"
    "Calculate your BMI, BMR, TDEE and weight-loss targets"
    "</p>",
    unsafe_allow_html=True
)


# =========================================================
# GOOGLE SHEET CONNECTION
# =========================================================

def get_google_sheet():

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )

    client = gspread.authorize(credentials)

    spreadsheet = client.open("BMI Calculator Visitor Log")

    worksheet = spreadsheet.sheet1

    return worksheet


# =========================================================
# SESSION STATE
# =========================================================

if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "results" not in st.session_state:
    st.session_state.results = {}

if "saved" not in st.session_state:
    st.session_state.saved = False


# =========================================================
# PERSONAL INFORMATION
# =========================================================

st.subheader("👤 Personal Information")

name = st.text_input(
    "Name",
    placeholder="Enter your name"
)

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=None,
    placeholder="Enter your age"
)

sex = st.selectbox(
    "Sex",
    ["Male", "Female"]
)


# =========================================================
# WEIGHT
# =========================================================

st.subheader("⚖️ Weight")

weight_unit = st.selectbox(
    "Weight unit",
    ["kg", "lb"]
)

weight = st.number_input(
    f"Weight ({weight_unit})",
    min_value=1.0,
    max_value=700.0,
    value=None,
    placeholder=f"Enter weight in {weight_unit}"
)


# =========================================================
# HEIGHT
# =========================================================

st.subheader("📏 Height")

height_unit = st.selectbox(
    "Height unit",
    ["cm", "m", "inches"]
)

height = st.number_input(
    f"Height ({height_unit})",
    min_value=1.0,
    max_value=300.0,
    value=None,
    placeholder=f"Enter height in {height_unit}"
)


# =========================================================
# TARGET WEIGHT
# =========================================================

st.subheader("🎯 Weight Goal")

target_weight = st.number_input(
    "Target weight (kg)",
    min_value=1.0,
    max_value=700.0,
    value=None,
    placeholder="Enter target weight"
)

st.caption(
    "Target weight should be entered in kilograms (kg)."
)


# =========================================================
# ACTIVITY LEVEL
# =========================================================

st.subheader("🏃 Activity Level")

activity = st.selectbox(
    "Select your activity level",
    [
        "Sedentary",
        "Lightly active",
        "Moderately active",
        "Very active",
        "Extremely active"
    ]
)


# =========================================================
# ACTIVITY DESCRIPTIONS
# =========================================================

activity_description = {

    "Sedentary":
        "Desk job, little or no exercise.",

    "Lightly active":
        "Exercise 1–3 days/week or mostly light physical activity.",

    "Moderately active":
        "Exercise 3–5 days/week, such as regular gym or brisk walking.",

    "Very active":
        "Exercise 6–7 days/week or high daily physical activity.",

    "Extremely active":
        "Intense training, athlete, or heavy physical work."
}


# =========================================================
# ACTIVITY FACTORS
# =========================================================

activity_factors = {

    "Sedentary": 1.2,

    "Lightly active": 1.375,

    "Moderately active": 1.55,

    "Very active": 1.725,

    "Extremely active": 1.9
}


# =========================================================
# ACTIVITY DESCRIPTION
# =========================================================

st.caption(activity_description[activity])


# =========================================================
# CALCULATE BUTTON
# =========================================================

st.markdown("---")

if st.button(
    "🧮 Calculate My Results",
    type="primary"
):

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name.strip():

        st.error("Please enter your name.")
        st.session_state.calculated = False

    elif age is None:

        st.error("Please enter your age.")
        st.session_state.calculated = False

    elif weight is None:

        st.error("Please enter your weight.")
        st.session_state.calculated = False

    elif height is None:

        st.error("Please enter your height.")
        st.session_state.calculated = False

    elif target_weight is None:

        st.error("Please enter your target weight.")
        st.session_state.calculated = False

    else:

        # -------------------------------------------------
        # CONVERT WEIGHT TO KG
        # -------------------------------------------------

        if weight_unit == "lb":
            weight_kg = weight * 0.453592

        else:
            weight_kg = weight


        # -------------------------------------------------
        # CONVERT HEIGHT TO METERS
        # -------------------------------------------------

        if height_unit == "cm":

            height_m = height / 100

        elif height_unit == "inches":

            height_m = height * 0.0254

        else:

            height_m = height


        # -------------------------------------------------
        # HEIGHT IN CM
        # -------------------------------------------------

        height_cm = height_m * 100


        # -------------------------------------------------
        # BMI
        # -------------------------------------------------

        bmi = weight_kg / (height_m ** 2)


        # -------------------------------------------------
        # BMR
        # Mifflin-St Jeor Equation
        # -------------------------------------------------

        if sex == "Male":

            bmr = (
                (10 * weight_kg)
                + (6.25 * height_cm)
                - (5 * age)
                + 5
            )

        else:

            bmr = (
                (10 * weight_kg)
                + (6.25 * height_cm)
                - (5 * age)
                - 161
            )


        # -------------------------------------------------
        # TDEE
        # -------------------------------------------------

        activity_factor = activity_factors[activity]

        tdee = bmr * activity_factor


        # -------------------------------------------------
        # CALORIE TARGETS
        # -------------------------------------------------

        maintenance = tdee

        mild_weight_loss = tdee * 0.90

        moderate_weight_loss = tdee * 0.85

        aggressive_weight_loss = tdee * 0.80

        weight_gain = tdee * 1.10


        # -------------------------------------------------
        # STORE RESULTS
        # -------------------------------------------------

        st.session_state.results = {

            "name": name.strip(),

            "age": age,

            "sex": sex,

            "weight_kg": weight_kg,

            "height_m": height_m,

            "height_cm": height_cm,

            "target_weight": target_weight,

            "activity": activity,

            "activity_factor": activity_factor,

            "bmi": bmi,

            "bmr": bmr,

            "tdee": tdee,

            "maintenance": maintenance,

            "mild_weight_loss": mild_weight_loss,

            "moderate_weight_loss": moderate_weight_loss,

            "aggressive_weight_loss": aggressive_weight_loss,

            "weight_gain": weight_gain
        }


        st.session_state.calculated = True

        # New calculation must be saved again
        st.session_state.saved = False


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state.calculated:

    results = st.session_state.results


    # -----------------------------------------------------
    # RETRIEVE RESULTS
    # -----------------------------------------------------

    name = results["name"]

    age = results["age"]

    sex = results["sex"]

    weight_kg = results["weight_kg"]

    height_m = results["height_m"]

    height_cm = results["height_cm"]

    target_weight = results["target_weight"]

    activity = results["activity"]

    bmi = results["bmi"]

    bmr = results["bmr"]

    tdee = results["tdee"]

    maintenance = results["maintenance"]

    mild_weight_loss = results["mild_weight_loss"]

    moderate_weight_loss = results["moderate_weight_loss"]

    aggressive_weight_loss = results["aggressive_weight_loss"]

    weight_gain = results["weight_gain"]


    # =====================================================
    # PERSONAL SUMMARY
    # =====================================================

    st.markdown("---")

    st.subheader("📋 Your Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"**Name:** {name}")

        st.write(f"**Age:** {age}")

        st.write(f"**Sex:** {sex}")

        st.write(f"**Weight:** {weight_kg:.1f} kg")

    with col2:

        st.write(f"**Height:** {height_m:.2f} m")

        st.write(f"**Activity:** {activity}")

        st.write(
            f"**Target:** {target_weight:.1f} kg"
        )


    # =====================================================
    # BMI
    # =====================================================

    st.markdown("---")

    st.subheader("⚖️ BMI")

    st.metric(
        "Your BMI",
        f"{bmi:.2f}"
    )


    # -----------------------------------------------------
    # BMI CATEGORY
    # -----------------------------------------------------

    if bmi < 18.5:

        st.warning(
            "BMI Category: Underweight"
        )

    elif bmi < 25:

        st.success(
            "BMI Category: Normal"
        )

    elif bmi < 30:

        st.warning(
            "BMI Category: Overweight"
        )

    else:

        st.error(
            "BMI Category: Obesity"
        )


    # =====================================================
    # BMR
    # =====================================================

    st.markdown("---")

    st.subheader("🔥 BMR")

    st.metric(
        "Basal Metabolic Rate",
        f"{bmr:.0f} kcal/day"
    )

    st.caption(
        "Estimated calories required at complete rest "
        "to maintain basic body functions."
    )


    # =====================================================
    # TDEE
    # =====================================================

    st.markdown("---")

    st.subheader("🔥 TDEE")

    st.metric(
        "Estimated Daily Energy Requirement",
        f"{tdee:.0f} kcal/day"
    )

    st.caption(
        "Estimated calories required each day to maintain "
        "your current body weight at your selected activity level."
    )


    # =====================================================
    # CALORIE TARGETS
    # =====================================================

    st.markdown("---")

    st.subheader("🎯 Daily Calorie Targets")


    st.metric(
        "⚖️ Maintain Weight",
        f"{maintenance:.0f} kcal/day"
    )


    st.metric(
        "🟢 Mild Weight Loss",
        f"{mild_weight_loss:.0f} kcal/day"
    )


    st.metric(
        "🟠 Moderate Weight Loss",
        f"{moderate_weight_loss:.0f} kcal/day"
    )


    st.metric(
        "🔴 More Aggressive Weight Loss",
        f"{aggressive_weight_loss:.0f} kcal/day"
    )


    st.metric(
        "🔵 Weight Gain",
        f"{weight_gain:.0f} kcal/day"
    )


    # =====================================================
    # WEIGHT GOAL
    # =====================================================

    st.markdown("---")

    st.subheader("🎯 Weight Goal")

    weight_difference = weight_kg - target_weight


    # =====================================================
    # WEIGHT LOSS
    # =====================================================

    if weight_difference > 0:

        st.info(
            f"Weight to lose: **{weight_difference:.1f} kg**"
        )


        # -------------------------------------------------
        # WEIGHT LOSS PLAN
        # -------------------------------------------------

        weight_loss_plan = st.selectbox(
            "Select your weight-loss plan",
            [
                "Mild (10% calorie deficit)",
                "Moderate (15% calorie deficit)",
                "More aggressive (20% calorie deficit)"
            ],
            key="weight_loss_plan"
        )


        # -------------------------------------------------
        # DEFICIT
        # -------------------------------------------------

        deficit_factors = {

            "Mild (10% calorie deficit)": 0.10,

            "Moderate (15% calorie deficit)": 0.15,

            "More aggressive (20% calorie deficit)": 0.20
        }


        deficit_percentage = deficit_factors[
            weight_loss_plan
        ]


        # -------------------------------------------------
        # DAILY DEFICIT
        # -------------------------------------------------

        daily_deficit = (
            tdee * deficit_percentage
        )


        # -------------------------------------------------
        # CALORIE TARGET
        # -------------------------------------------------

        weight_loss_calories = (
            tdee - daily_deficit
        )


        st.metric(
            "🔥 Your Daily Calorie Target",
            f"{weight_loss_calories:.0f} kcal/day"
        )


        # -------------------------------------------------
        # CALCULATION OF TIME
        # -------------------------------------------------

        calories_to_lose = (
            weight_difference * 7700
        )


        days_required = (
            calories_to_lose / daily_deficit
        )


        weeks_required = (
            days_required / 7
        )


        months_required = (
            weeks_required / 4.345
        )


        # -------------------------------------------------
        # ESTIMATED TIME
        # -------------------------------------------------

        st.write("### ⏳ Estimated Time to Reach Target")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Days",
                f"{days_required:.0f}"
            )


        with col2:

            st.metric(
                "Weeks",
                f"{weeks_required:.1f}"
            )


        with col3:

            st.metric(
                "Months",
                f"{months_required:.1f}"
            )


        st.caption(
            "This is a mathematical estimate. Actual weight "
            "change can vary because of water, glycogen, "
            "muscle mass, appetite and changes in energy expenditure."
        )


    # =====================================================
    # SAME WEIGHT
    # =====================================================

    elif weight_difference == 0:

        weight_loss_plan = "No weight loss required"

        weight_loss_calories = maintenance

        days_required = 0

        weeks_required = 0

        months_required = 0


        st.success(
            "🎯 Your target weight is the same as your current weight."
        )


    # =====================================================
    # WEIGHT GAIN
    # =====================================================

    else:

        weight_to_gain = abs(weight_difference)

        weight_loss_plan = "Weight gain"

        weight_loss_calories = weight_gain

        days_required = 0

        weeks_required = 0

        months_required = 0


        st.info(
            f"Weight to gain: **{weight_to_gain:.1f} kg**"
        )


        st.caption(
            "Your target weight is higher than your current weight."
        )


    # =====================================================
    # SAVE RESULTS
    # =====================================================

    st.markdown("---")

    st.subheader("💾 Save Results")

    if st.session_state.saved:

        st.success(
            "✅ This calculation has already been saved."
        )

    else:

        st.write(
            "Review your results and press the button below "
            "to save them."
        )


        if st.button(
            "✅ Confirm & Save Results",
            type="primary",
            key="confirm_save"
        ):

            try:

                # -----------------------------------------
                # CONNECT TO GOOGLE SHEET
                # -----------------------------------------

                worksheet = get_google_sheet()


                # -----------------------------------------
                # DATE & TIME
                # -----------------------------------------

                now = datetime.now()

                date = now.strftime("%Y-%m-%d")

                time = now.strftime("%H:%M:%S")


                # -----------------------------------------
                # ROW
                # -----------------------------------------

                row = [

                    name,

                    date,

                    time,

                    age,

                    sex,

                    round(weight_kg, 2),

                    round(height_cm, 2),

                    round(target_weight, 2),

                    activity,

                    round(bmi, 2),

                    round(bmr, 0),

                    round(tdee, 0),

                    weight_loss_plan,

                    round(weight_loss_calories, 0),

                    round(days_required, 0),

                    round(weeks_required, 1),

                    round(months_required, 1)
                ]


                # -----------------------------------------
                # SAVE
                # -----------------------------------------

                worksheet.append_row(
                    row,
                    value_input_option="USER_ENTERED"
                )


                # -----------------------------------------
                # MARK SAVED
                # -----------------------------------------

                st.session_state.saved = True


                st.success(
                    "🎉 Results successfully saved to Google Sheet!"
                )


            except Exception as e:

                st.error(
                    "❌ Unable to save results to Google Sheet."
                )

                st.exception(e)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer-text">
    ⚠️ This calculator provides estimates for educational
    purposes and should not replace individualized medical advice.
    </div>
    """,
    unsafe_allow_html=True
)
```
