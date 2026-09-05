import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm


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
# MOBILE-FRIENDLY CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 700px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1 {
        text-align: center;
        font-size: 2rem !important;
        margin-bottom: 0.3rem;
    }

    h2 {
        font-size: 1.35rem !important;
        margin-top: 1.5rem;
    }

    h3 {
        font-size: 1.15rem !important;
    }

    div.stButton > button {
        width: 100%;
        min-height: 3rem;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 10px;
    }

    div[data-baseweb="input"] input {
        font-size: 1rem;
    }

    div[data-baseweb="select"] {
        font-size: 1rem;
    }

    div[data-testid="stMetric"] {
        padding: 0.5rem 0;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

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
# PDF GENERATOR
# =========================================================

def create_pdf(results, weight_loss_plan,
               weight_loss_calories,
               days_required,
               weeks_required,
               months_required):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=16,
        spaceBefore=10,
        spaceAfter=7
    )

    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=13
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        fontSize=8,
        leading=11
    )

    story = []

    # -----------------------------------------------------
    # DATE AND TIME
    # -----------------------------------------------------

    now = datetime.now()

    report_date = now.strftime("%d-%m-%Y")

    report_time = now.strftime("%H:%M:%S")


    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "BMI + BMR + TDEE HEALTH REPORT",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Personalized Energy & Weight Management Report",
            subtitle_style
        )
    )


    # -----------------------------------------------------
    # PATIENT INFORMATION
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Patient Information",
            heading_style
        )
    )

    patient_data = [
        ["Name", results["name"]],
        ["Age", str(results["age"])],
        ["Sex", results["sex"]],
        ["Weight", f'{results["weight_kg"]:.1f} kg'],
        ["Height", f'{results["height_cm"]:.1f} cm'],
        ["Activity Level", results["activity"]],
        ["Target Weight", f'{results["target_weight"]:.1f} kg']
    ]

    patient_table = Table(
        patient_data,
        colWidths=[55 * mm, 105 * mm]
    )

    patient_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(patient_table)

    story.append(Spacer(1, 8))


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "BMI Assessment",
            heading_style
        )
    )

    bmi = results["bmi"]

    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obesity"

    bmi_data = [
        ["BMI", f"{bmi:.2f}"],
        ["Category", bmi_category]
    ]

    bmi_table = Table(
        bmi_data,
        colWidths=[55 * mm, 105 * mm]
    )

    bmi_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(bmi_table)


    # -----------------------------------------------------
    # BMR AND TDEE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Energy Requirements",
            heading_style
        )
    )

    energy_data = [
        ["BMR", f'{results["bmr"]:.0f} kcal/day'],
        ["TDEE", f'{results["tdee"]:.0f} kcal/day'],
        ["Activity Factor", f'{results["activity_factor"]:.3f}']
    ]

    energy_table = Table(
        energy_data,
        colWidths=[55 * mm, 105 * mm]
    )

    energy_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(energy_table)


    # -----------------------------------------------------
    # CALORIE TARGETS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Daily Calorie Targets",
            heading_style
        )
    )

    calorie_data = [
        ["Goal", "Estimated Calories"],
        [
            "Maintain Weight",
            f'{results["maintenance"]:.0f} kcal/day'
        ],
        [
            "Mild Weight Loss",
            f'{results["mild_weight_loss"]:.0f} kcal/day'
        ],
        [
            "Moderate Weight Loss",
            f'{results["moderate_weight_loss"]:.0f} kcal/day'
        ],
        [
            "More Aggressive Weight Loss",
            f'{results["aggressive_weight_loss"]:.0f} kcal/day'
        ],
        [
            "Weight Gain",
            f'{results["weight_gain"]:.0f} kcal/day'
        ]
    ]

    calorie_table = Table(
        calorie_data,
        colWidths=[95 * mm, 65 * mm]
    )

    calorie_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(calorie_table)


    # -----------------------------------------------------
    # WEIGHT LOSS PLAN
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Weight Goal",
            heading_style
        )
    )

    weight_difference = (
        results["weight_kg"]
        - results["target_weight"]
    )

    if weight_difference > 0:

        goal_data = [
            ["Current Weight", f'{results["weight_kg"]:.1f} kg'],
            ["Target Weight", f'{results["target_weight"]:.1f} kg'],
            ["Weight to Lose", f'{weight_difference:.1f} kg'],
            ["Selected Plan", weight_loss_plan],
            [
                "Daily Calorie Target",
                f"{weight_loss_calories:.0f} kcal/day"
            ],
            ["Estimated Days", f"{days_required:.0f}"],
            ["Estimated Weeks", f"{weeks_required:.1f}"],
            ["Estimated Months", f"{months_required:.1f}"]
        ]

    elif weight_difference == 0:

        goal_data = [
            ["Current Weight", f'{results["weight_kg"]:.1f} kg'],
            ["Target Weight", f'{results["target_weight"]:.1f} kg'],
            ["Goal", "Maintain current weight"],
            [
                "Daily Calorie Target",
                f"{weight_loss_calories:.0f} kcal/day"
            ]
        ]

    else:

        weight_to_gain = abs(weight_difference)

        goal_data = [
            ["Current Weight", f'{results["weight_kg"]:.1f} kg'],
            ["Target Weight", f'{results["target_weight"]:.1f} kg'],
            ["Weight to Gain", f"{weight_to_gain:.1f} kg"],
            ["Goal", "Weight gain"],
            [
                "Suggested Daily Calories",
                f"{weight_loss_calories:.0f} kcal/day"
            ]
        ]


    goal_table = Table(
        goal_data,
        colWidths=[65 * mm, 95 * mm]
    )

    goal_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(goal_table)


    # -----------------------------------------------------
    # EXPLANATION
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Important Information",
            heading_style
        )
    )

    explanation = (
        "BMR is the estimated energy required to maintain "
        "basic physiological functions at rest. TDEE is an "
        "estimate of daily energy expenditure based on the "
        "selected activity level. Calorie targets are estimates "
        "and actual requirements may vary between individuals."
    )

    story.append(
        Paragraph(
            explanation,
            normal_style
        )
    )

    story.append(Spacer(1, 8))


    # -----------------------------------------------------
    # WEIGHT LOSS DISCLAIMER
    # -----------------------------------------------------

    disclaimer = (
        "Estimated weight-loss time is a mathematical projection "
        "based on an approximate energy value of 7,700 kcal per "
        "kg of body weight. Actual weight change can differ due "
        "to changes in water, glycogen, muscle mass, appetite, "
        "metabolic adaptation and other factors."
    )

    story.append(
        Paragraph(
            disclaimer,
            small_style
        )
    )

    story.append(Spacer(1, 10))


    # -----------------------------------------------------
    # DATE / TIME
    # -----------------------------------------------------

    story.append(
        Paragraph(
            f"Report generated: {report_date} at {report_time}",
            small_style
        )
    )

    story.append(Spacer(1, 12))


    # -----------------------------------------------------
    # MEDICAL DISCLAIMER
    # -----------------------------------------------------

    medical_disclaimer = (
        "<b>Medical Disclaimer:</b> This calculator provides "
        "estimates for educational and informational purposes "
        "only. It is not a substitute for individualized "
        "medical assessment, diagnosis or treatment. Calorie "
        "requirements and weight-management recommendations "
        "should be interpreted in the context of the individual's "
        "overall health and clinical circumstances."
    )

    story.append(
        Paragraph(
            medical_disclaimer,
            small_style
        )
    )


    # -----------------------------------------------------
    # BUILD PDF
    # -----------------------------------------------------

    document.build(story)

    buffer.seek(0)

    return buffer


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
        # WEIGHT TO KG
        # -------------------------------------------------

        if weight_unit == "lb":

            weight_kg = weight * 0.453592

        else:

            weight_kg = weight


        # -------------------------------------------------
        # HEIGHT TO METERS
        # -------------------------------------------------

        if height_unit == "cm":

            height_m = height / 100

        elif height_unit == "inches":

            height_m = height * 0.0254

        else:

            height_m = height


        # -------------------------------------------------
        # HEIGHT CM
        # -------------------------------------------------

        height_cm = height_m * 100


        # -------------------------------------------------
        # BMI
        # -------------------------------------------------

        bmi = weight_kg / (height_m ** 2)


        # -------------------------------------------------
        # BMR
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

        st.session_state.saved = False


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state.calculated:

    results = st.session_state.results


    # -----------------------------------------------------
    # VALUES
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

        st.write(f"**Target:** {target_weight:.1f} kg")


    # =====================================================
    # BMI
    # =====================================================

    st.markdown("---")

    st.subheader("⚖️ BMI")

    st.metric(
        "Your BMI",
        f"{bmi:.2f}"
    )


    if bmi < 18.5:

        st.warning("BMI Category: Underweight")

    elif bmi < 25:

        st.success("BMI Category: Normal")

    elif bmi < 30:

        st.warning("BMI Category: Overweight")

    else:

        st.error("BMI Category: Obesity")


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


        weight_loss_plan = st.selectbox(
            "Select your weight-loss plan",
            [
                "Mild (10% calorie deficit)",
                "Moderate (15% calorie deficit)",
                "More aggressive (20% calorie deficit)"
            ],
            key="weight_loss_plan"
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
            "🔥 Your Daily Calorie Target",
            f"{weight_loss_calories:.0f} kcal/day"
        )


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
    # GOOGLE SHEET SAVE
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

                worksheet = get_google_sheet()


                # -------------------------------------------------
                # USE CURRENT DATE AND TIME
                # -------------------------------------------------

                now = datetime.now()

                date = now.strftime("%Y-%m-%d")

                time = now.strftime("%H:%M:%S")


                # -------------------------------------------------
                # CREATE ROW
                # -------------------------------------------------

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


                worksheet.append_row(
                    row,
                    value_input_option="USER_ENTERED"
                )


                st.session_state.saved = True


                st.success(
                    "🎉 Results successfully saved to Google Sheet!"
                )


            except Exception as e:

                st.error(
                    "❌ Unable to save results to Google Sheet."
                )

                st.exception(e)


    # =====================================================
    # PDF REPORT
    # =====================================================

    st.markdown("---")

    st.subheader("📄 Patient Report")

    st.write(
        "Generate a professional PDF containing the "
        "calculation results."
    )


    try:

        pdf_file = create_pdf(
            results,
            weight_loss_plan,
            weight_loss_calories,
            days_required,
            weeks_required,
            months_required
        )


        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_file,
            file_name=(
                f"BMI_Report_{name.replace(' ', '_')}.pdf"
            ),
            mime="application/pdf",
            type="primary"
        )


    except Exception as e:

        st.error(
            "❌ Unable to generate PDF report."
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
