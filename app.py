import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


# ==========================================
# GOOGLE SHEETS CONNECTION
# ==========================================

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


# ==========================================
# PAGE TITLE
# ==========================================

st.title("🩺 BMI + BMR + TDEE Calculator")

st.write(
    "Calculate your BMI, BMR, estimated TDEE, "
    "daily calorie targets and weight-loss goal."
)


# ==========================================
# SESSION STATE
# ==========================================

if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "results" not in st.session_state:
    st.session_state.results = {}

if "saved" not in st.session_state:
    st.session_state.saved = False


# ==========================================
# PERSONAL INFORMATION
# ==========================================

st.write("## 👤 Personal Information")

name = st.text_input("Enter your name")

age = st.number_input(
    "Enter your age",
    min_value=1,
    max_value=120,
    value=None,
    placeholder="Enter age"
)

sex = st.selectbox(
    "Select sex",
    ["Male", "Female"]
)


# ==========================================
# WEIGHT
# ==========================================

st.write("## ⚖️ Weight")

weight_unit = st.selectbox(
    "Select weight unit",
    ["kg", "lb"]
)

weight = st.number_input(
    f"Enter your weight in {weight_unit}",
    min_value=1.0,
    max_value=700.0,
    value=None,
    placeholder="Enter weight"
)


# ==========================================
# HEIGHT
# ==========================================

st.write("## 📏 Height")

height_unit = st.selectbox(
    "Select height unit",
    ["cm", "m", "inches"]
)

height = st.number_input(
    f"Enter your height in {height_unit}",
    min_value=1.0,
    max_value=300.0,
    value=None,
    placeholder="Enter height"
)


# ==========================================
# TARGET WEIGHT
# ==========================================

st.write("## 🎯 Weight Goal")

target_weight = st.number_input(
    "Enter your target weight (kg)",
    min_value=1.0,
    max_value=700.0,
    value=None,
    placeholder="Enter target weight"
)

st.caption(
    "Target weight should be entered in kilograms (kg)."
)


# ==========================================
# ACTIVITY LEVEL
# ==========================================

st.write("## 🏃 Activity Level")

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


# ==========================================
# ACTIVITY DESCRIPTIONS
# ==========================================

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


# ==========================================
# ACTIVITY FACTORS
# ==========================================

activity_factors = {

    "Sedentary": 1.2,

    "Lightly active": 1.375,

    "Moderately active": 1.55,

    "Very active": 1.725,

    "Extremely active": 1.9
}


st.caption(activity_description[activity])


# ==========================================
# CALCULATE BUTTON
# ==========================================

if st.button("Calculate"):

    if not name:

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

        # ==================================
        # WEIGHT TO KG
        # ==================================

        if weight_unit == "lb":
            weight_kg = weight * 0.453592
        else:
            weight_kg = weight


        # ==================================
        # HEIGHT TO METERS
        # ==================================

        if height_unit == "cm":

            height_m = height / 100

        elif height_unit == "inches":

            height_m = height * 0.0254

        else:

            height_m = height


        height_cm = height_m * 100


        # ==================================
        # BMI
        # ==================================

        bmi = weight_kg / (height_m ** 2)


        # ==================================
        # BMR
        # ==================================

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


        # ==================================
        # TDEE
        # ==================================

        activity_factor = activity_factors[activity]

        tdee = bmr * activity_factor


        # ==================================
        # CALORIE TARGETS
        # ==================================

        maintenance = tdee

        mild_weight_loss = tdee * 0.90

        moderate_weight_loss = tdee * 0.85

        aggressive_weight_loss = tdee * 0.80

        weight_gain = tdee * 1.10


        # ==================================
        # SAVE RESULTS
        # ==================================

        st.session_state.results = {

            "name": name,
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

        # Allow saving again for a new calculation
        st.session_state.saved = False


# ==========================================
# DISPLAY RESULTS
# ==========================================

if st.session_state.calculated:

    results = st.session_state.results

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


    # ======================================
    # PERSONAL INFORMATION
    # ======================================

    st.success(f"Hello {name}! 👋")

    st.write("## 📋 Your Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"**Age:** {age}")

        st.write(f"**Sex:** {sex}")

        st.write(
            f"**Weight:** {weight_kg:.2f} kg"
        )

    with col2:

        st.write(
            f"**Height:** {height_m:.2f} m"
        )

        st.write(
            f"**Activity:** {activity}"
        )

        st.write(
            f"**Target weight:** {target_weight:.1f} kg"
        )


    # ======================================
    # BMI
    # ======================================

    st.write("## ⚖️ BMI")

    st.metric(
        "Your BMI",
        f"{bmi:.2f}"
    )


    if bmi < 18.5:

        st.warning("BMI Category: Underweight")

        st.write(
            "Consider maintaining adequate "
            "calorie and nutrient intake."
        )

    elif bmi < 25:

        st.success("BMI Category: Normal")

        st.write(
            "Your BMI is within the normal range. "
            "Regular exercise and a balanced diet "
            "will help maintain your health."
        )

    elif bmi < 30:

        st.warning("BMI Category: Overweight")

        st.write(
            "Regular exercise and a balanced diet "
            "may be helpful."
        )

    else:

        st.error("BMI Category: Obesity")

        st.write(
            "Consider discussing weight management "
            "with a healthcare professional."
        )


    # ======================================
    # BMR
    # ======================================

    st.write("## 🔥 BMR")

    st.metric(
        "Basal Metabolic Rate",
        f"{bmr:.0f} kcal/day"
    )

    st.caption(
        "BMR is the estimated energy your body "
        "needs at complete rest to maintain basic "
        "physiological functions."
    )


    # ======================================
    # ACTIVITY
    # ======================================

    st.write("## 🏃 Activity Level")

    st.write(f"**{activity}**")

    st.caption(activity_description[activity])


    # ======================================
    # TDEE
    # ======================================

    st.write("## 🔥 TDEE")

    st.metric(
        "Estimated Daily Energy Requirement",
        f"{tdee:.0f} kcal/day"
    )

    st.info(
        "TDEE is the estimated number of calories "
        "you need each day to maintain your current weight."
    )


    # ======================================
    # CALORIE TARGETS
    # ======================================

    st.write("## 🎯 Daily Calorie Targets")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "⚖️ Maintain Weight",
            f"{maintenance:.0f} kcal/day"
        )

        st.metric(
            "🟢 Mild Weight Loss",
            f"{mild_weight_loss:.0f} kcal/day",
            "-10%"
        )

        st.metric(
            "🟠 Moderate Weight Loss",
            f"{moderate_weight_loss:.0f} kcal/day",
            "-15%"
        )

    with col2:

        st.metric(
            "🔴 More Aggressive Weight Loss",
            f"{aggressive_weight_loss:.0f} kcal/day",
            "-20%"
        )

        st.metric(
            "🔵 Weight Gain",
            f"{weight_gain:.0f} kcal/day",
            "+10%"
        )


    # ======================================
    # WEIGHT GOAL
    # ======================================

    st.write("## 🎯 Weight Goal")

    weight_difference = weight_kg - target_weight


    # ======================================
    # WEIGHT LOSS
    # ======================================

    if weight_difference > 0:

        st.write(
            f"**Weight to lose: "
            f"{weight_difference:.1f} kg**"
        )

        weight_loss_plan = st.selectbox(
            "Select your weight-loss plan",
            [
                "Mild (10% calorie deficit)",
                "Moderate (15% calorie deficit)",
                "More aggressive (20% calorie deficit)"
            ]
        )


        deficit_factors = {

            "Mild (10% calorie deficit)": 0.10,

            "Moderate (15% calorie deficit)": 0.15,

            "More aggressive (20% calorie deficit)": 0.20
        }


        deficit_percentage = deficit_factors[
            weight_loss_plan
        ]


        daily_deficit = (
            tdee * deficit_percentage
        )


        weight_loss_calories = (
            tdee - daily_deficit
        )


        st.metric(
            "🔥 Daily Calorie Target",
            f"{weight_loss_calories:.0f} kcal/day"
        )


        st.caption(
            f"Selected plan: **{weight_loss_plan}**"
        )


        # ==================================
        # ESTIMATED TIME
        # ==================================

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


        st.write("### ⏳ Estimated Time")

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


        st.info(
            "This is an approximate mathematical estimate. "
            "Actual weight loss may differ because of changes "
            "in water, glycogen, muscle mass, appetite and "
            "energy expenditure."
        )


    # ======================================
    # SAME WEIGHT
    # ======================================

    elif weight_difference == 0:

        weight_loss_plan = "No weight loss required"
        weight_loss_calories = maintenance

        days_required = 0
        weeks_required = 0
        months_required = 0

        st.success(
            "🎯 Your target weight is the same "
            "as your current weight."
        )


    # ======================================
    # WEIGHT GAIN
    # ======================================

    else:

        weight_to_gain = abs(weight_difference)

        weight_loss_plan = "Weight gain"
        weight_loss_calories = weight_gain

        days_required = 0
        weeks_required = 0
        months_required = 0

        st.write(
            f"**Weight to gain: "
            f"{weight_to_gain:.1f} kg**"
        )

        st.info(
            "Your target weight is higher than your current "
            "weight. A dedicated weight-gain calorie plan "
            "can be added separately."
        )


    # ======================================
    # SAVE TO GOOGLE SHEET
    # ======================================

    st.write("## 📊 Save Your Results")

    if not st.session_state.saved:

        if st.button("💾 Save Results to Google Sheet"):

            try:

                worksheet = get_google_sheet()

                now = datetime.now()

                date_value = now.strftime("%Y-%m-%d")

                time_value = now.strftime("%H:%M:%S")


                row = [

                    name,
                    date_value,
                    time_value,

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


                worksheet.append_row(
                    row,
                    value_input_option="USER_ENTERED"
                )


                st.session_state.saved = True

                st.success(
                    "✅ Your results have been successfully "
                    "saved to the Google Sheet."
                )


            except Exception as e:

                st.error(
                    "❌ Unable to save to Google Sheet."
                )

                st.exception(e)

    else:

        st.success(
            "✅ These results have already been saved."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "⚠️ This calculator provides estimates for educational "
    "purposes and should not replace individualized medical advice."
)
