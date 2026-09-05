import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
import io


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="BMI & Weight Management Calculator",
    page_icon="🩺",
    layout="centered"
)


# =========================================================
# MOBILE FRIENDLY CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        max-width: 700px;
        margin: auto;
    }

    .stButton > button {
        width: 100%;
        height: 48px;
        font-size: 17px;
    }

    .stDownloadButton > button {
        width: 100%;
        height: 48px;
        font-size: 17px;
    }

    h1 {
        text-align: center;
    }

    </style>
    """,
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

def create_pdf(
    name,
    age,
    sex,
    weight_kg,
    height_cm,
    target_weight,
    activity,
    bmi,
    bmr,
    tdee,
    weight_loss_plan,
    daily_calorie_target,
    estimated_days,
    estimated_weeks,
    estimated_months
):

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )

    elements = []

    # =====================================================
    # INDIA / IST DATE AND TIME
    # =====================================================

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    report_date = now.strftime("%d-%m-%Y")
    report_time = now.strftime("%I:%M:%S %p")


    # =====================================================
    # TITLE
    # =====================================================

    elements.append(
        Paragraph(
            "BMI & WEIGHT MANAGEMENT REPORT",
            title_style
        )
    )

    elements.append(
        Paragraph(
            f"Generated on {report_date} at {report_time}",
            normal_style
        )
    )

    elements.append(Spacer(1, 12))


    # =====================================================
    # PERSONAL INFORMATION
    # =====================================================

    elements.append(
        Paragraph(
            "Personal Information",
            heading_style
        )
    )

    personal_data = [
        ["Name", name],
        ["Age", f"{age} years"],
        ["Sex", sex],
        ["Weight", f"{weight_kg:.1f} kg"],
        ["Height", f"{height_cm:.1f} cm"],
        ["Target Weight", f"{target_weight:.1f} kg"],
        ["Activity Level", activity]
    ]

    personal_table = Table(
        personal_data,
        colWidths=[5 * cm, 11 * cm]
    )

    personal_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elements.append(personal_table)


    # =====================================================
    # BMI ASSESSMENT
    # =====================================================

    elements.append(
        Paragraph(
            "BMI Assessment",
            heading_style
        )
    )

    if bmi < 18.5:
        bmi_category = "Underweight"

    elif bmi < 25:
        bmi_category = "Normal weight"

    elif bmi < 30:
        bmi_category = "Overweight"

    else:
        bmi_category = "Obesity"


    bmi_data = [
        ["BMI", f"{bmi:.1f}"],
        ["Category", bmi_category]
    ]

    bmi_table = Table(
        bmi_data,
        colWidths=[5 * cm, 11 * cm]
    )

    bmi_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elements.append(bmi_table)


    # =====================================================
    # ENERGY REQUIREMENTS
    # =====================================================

    elements.append(
        Paragraph(
            "Energy Requirements",
            heading_style
        )
    )

    energy_data = [
        ["BMR", f"{bmr:.0f} kcal/day"],
        ["TDEE / Maintenance", f"{tdee:.0f} kcal/day"],
        ["Selected Plan", weight_loss_plan],
        ["Daily Calorie Target", f"{daily_calorie_target:.0f} kcal/day"]
    ]

    energy_table = Table(
        energy_data,
        colWidths=[7 * cm, 9 * cm]
    )

    energy_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elements.append(energy_table)


    # =====================================================
    # WEIGHT LOSS ESTIMATE
    # =====================================================

    elements.append(
        Paragraph(
            "Estimated Weight-Loss Timeline",
            heading_style
        )
    )

    weight_difference = weight_kg - target_weight

    if weight_difference > 0:

        timeline_data = [
            ["Current Weight", f"{weight_kg:.1f} kg"],
            ["Target Weight", f"{target_weight:.1f} kg"],
            ["Weight to Lose", f"{weight_difference:.1f} kg"],
            ["Estimated Time", f"{estimated_days:.0f} days"],
            ["Estimated Weeks", f"{estimated_weeks:.1f} weeks"],
            ["Estimated Months", f"{estimated_months:.1f} months"]
        ]

    else:

        timeline_data = [
            ["Current Weight", f"{weight_kg:.1f} kg"],
            ["Target Weight", f"{target_weight:.1f} kg"],
            ["Status", "Target weight is not below current weight"]
        ]

    timeline_table = Table(
        timeline_data,
        colWidths=[7 * cm, 9 * cm]
    )

    timeline_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elements.append(timeline_table)


    # =====================================================
    # EXPLANATION
    # =====================================================

    elements.append(
        Paragraph(
            "About the Calculations",
            heading_style
        )
    )

    explanation = """
    BMI is calculated from body weight and height. BMR represents the
    approximate amount of energy required by the body at rest. TDEE
    estimates daily energy expenditure after considering activity level.
    The calorie target is calculated from the selected weight-management
    plan.
    """

    elements.append(
        Paragraph(
            explanation,
            normal_style
        )
    )

    elements.append(Spacer(1, 10))


    # =====================================================
    # DISCLAIMER
    # =====================================================

    elements.append(
        Paragraph(
            "Medical Disclaimer",
            heading_style
        )
    )

    disclaimer = """
    This report is intended for general educational and informational
    purposes. BMI, BMR, TDEE and estimated weight-loss timelines are
    approximate calculations and should not be considered a substitute
    for individualized medical advice, diagnosis or treatment.
    """

    elements.append(
        Paragraph(
            disclaimer,
            normal_style
        )
    )


    # =====================================================
    # BUILD PDF
    # =====================================================

    document.build(elements)

    buffer.seek(0)

    return buffer


# =========================================================
# TITLE
# =========================================================

st.title(
    "🩺 BMI & Weight Management Calculator"
)

st.write(
    "Enter your details below to calculate BMI, BMR, TDEE "
    "and a personalized calorie target."
)


# =========================================================
# PERSONAL INFORMATION
# =========================================================

st.subheader("👤 Personal Information")

name = st.text_input(
    "Enter your name"
)

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


# =========================================================
# WEIGHT
# =========================================================

st.subheader("⚖️ Weight")

weight_unit = st.selectbox(
    "Select weight unit",
    ["kg", "lb"]
)

weight = st.number_input(
    f"Enter weight ({weight_unit})",
    min_value=1.0,
    max_value=500.0,
    value=None,
    placeholder="Enter weight"
)


# =========================================================
# HEIGHT
# =========================================================

st.subheader("📏 Height")

height_unit = st.selectbox(
    "Select height unit",
    ["cm", "m", "inches"]
)

height = st.number_input(
    f"Enter height ({height_unit})",
    min_value=1.0,
    max_value=300.0,
    value=None,
    placeholder="Enter height"
)


# =========================================================
# TARGET WEIGHT
# =========================================================

target_weight = st.number_input(
    "Enter target weight (kg)",
    min_value=1.0,
    max_value=500.0,
    value=None,
    placeholder="Enter target weight"
)


# =========================================================
# ACTIVITY LEVEL
# =========================================================

st.subheader("🏃 Activity Level")

activity_options = {
    "Sedentary": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Very active": 1.725,
    "Extremely active": 1.9
}

activity_descriptions = {
    "Sedentary":
        "Little or no exercise",

    "Lightly active":
        "Light exercise or sports 1–3 days/week",

    "Moderately active":
        "Moderate exercise or sports 3–5 days/week",

    "Very active":
        "Hard exercise or sports 6–7 days/week",

    "Extremely active":
        "Very hard exercise, physical job or intense training"
}

activity = st.selectbox(
    "Select your activity level",
    list(activity_options.keys())
)

st.info(
    activity_descriptions[activity]
)


# =========================================================
# CALCULATE BUTTON
# =========================================================

calculate = st.button(
    "🧮 Calculate"
)


# =========================================================
# CALCULATION
# =========================================================

if calculate:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name.strip():

        st.error("Please enter your name.")
        st.stop()

    if age is None:

        st.error("Please enter your age.")
        st.stop()

    if weight is None:

        st.error("Please enter your weight.")
        st.stop()

    if height is None:

        st.error("Please enter your height.")
        st.stop()

    if target_weight is None:

        st.error("Please enter your target weight.")
        st.stop()


    # -----------------------------------------------------
    # CONVERT WEIGHT TO KG
    # -----------------------------------------------------

    if weight_unit == "kg":

        weight_kg = weight

    else:

        weight_kg = weight * 0.453592


    # -----------------------------------------------------
    # CONVERT HEIGHT TO CM
    # -----------------------------------------------------

    if height_unit == "cm":

        height_cm = height

    elif height_unit == "m":

        height_cm = height * 100

    else:

        height_cm = height * 2.54


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)


    # -----------------------------------------------------
    # BMR - MIFFLIN ST JEOR
    # -----------------------------------------------------

    if sex == "Male":

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight_kg
            + 6.25 * height_cm
            - 5 * age
            - 161
        )


    # -----------------------------------------------------
    # TDEE
    # -----------------------------------------------------

    activity_factor = activity_options[activity]

    tdee = bmr * activity_factor


    # -----------------------------------------------------
    # BMI CATEGORY
    # -----------------------------------------------------

    if bmi < 18.5:

        bmi_category = "Underweight"

    elif bmi < 25:

        bmi_category = "Normal weight"

    elif bmi < 30:

        bmi_category = "Overweight"

    else:

        bmi_category = "Obesity"


    # =====================================================
    # RESULTS
    # =====================================================

    st.subheader("📊 Your Results")


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    st.metric(
        "BMI",
        f"{bmi:.1f}"
    )


    # -----------------------------------------------------
    # BMI VISUAL STATUS
    # -----------------------------------------------------

    if bmi < 18.5:

        st.info("🔵 Underweight")

    elif bmi < 25:

        st.success("🟢 Normal weight")

    elif bmi < 30:

        st.warning("🟠 Overweight")

    else:

        st.error("🔴 Obesity")


    st.write(
        f"**BMI Category:** {bmi_category}"
    )


    # -----------------------------------------------------
    # BMR
    # -----------------------------------------------------

    st.metric(
        "BMR",
        f"{bmr:.0f} kcal/day"
    )


    # -----------------------------------------------------
    # TDEE
    # -----------------------------------------------------

    st.metric(
        "TDEE / Maintenance Calories",
        f"{tdee:.0f} kcal/day"
    )


    # =====================================================
    # WEIGHT MANAGEMENT PLAN
    # =====================================================

    st.subheader(
        "🎯 Select Your Weight Management Plan"
    )

    plan = st.selectbox(
        "Select your plan",
        [
            "Mild",
            "Moderate",
            "More aggressive"
        ],
        key="plan_selection"
    )


    # -----------------------------------------------------
    # CALORIE DEFICIT
    # -----------------------------------------------------

    if plan == "Mild":

        calorie_deficit = 0.10

    elif plan == "Moderate":

        calorie_deficit = 0.15

    else:

        calorie_deficit = 0.20


    daily_calorie_target = (
        tdee * (1 - calorie_deficit)
    )


    st.metric(
        "Daily Calorie Target",
        f"{daily_calorie_target:.0f} kcal/day"
    )


    # =====================================================
    # WEIGHT LOSS CALCULATION
    # =====================================================

    weight_to_lose = weight_kg - target_weight


    if weight_to_lose > 0:

        total_calorie_deficit = (
            weight_to_lose * 7700
        )

        daily_deficit = (
            tdee - daily_calorie_target
        )


        if daily_deficit > 0:

            estimated_days = (
                total_calorie_deficit
                / daily_deficit
            )

            estimated_weeks = (
                estimated_days / 7
            )

            estimated_months = (
                estimated_days / 30.44
            )

        else:

            estimated_days = 0
            estimated_weeks = 0
            estimated_months = 0


        st.write(
            f"**Weight to lose:** "
            f"{weight_to_lose:.1f} kg"
        )

        st.write(
            f"**Estimated time:** "
            f"{estimated_days:.0f} days "
            f"({estimated_weeks:.1f} weeks / "
            f"{estimated_months:.1f} months)"
        )

    else:

        estimated_days = 0
        estimated_weeks = 0
        estimated_months = 0

        st.info(
            "Your target weight is not below your current weight."
        )


    # =====================================================
    # CREATE CALCULATION DATA
    # =====================================================

    calculation = {

        "name": name,
        "age": age,
        "sex": sex,
        "weight_kg": weight_kg,
        "height_cm": height_cm,
        "target_weight": target_weight,
        "activity": activity,
        "bmi": bmi,
        "bmr": bmr,
        "tdee": tdee,
        "plan": plan,
        "daily_calorie_target": daily_calorie_target,
        "estimated_days": estimated_days,
        "estimated_weeks": estimated_weeks,
        "estimated_months": estimated_months
    }


    # =====================================================
    # AUTOMATIC GOOGLE SHEET SAVE
    # =====================================================

    # Create a unique ID for this calculation.
    # This prevents the same calculation from being
    # automatically saved multiple times during reruns.

    calculation_id = (
        f"{name.strip().lower()}|"
        f"{age}|"
        f"{sex}|"
        f"{weight_kg:.4f}|"
        f"{height_cm:.4f}|"
        f"{target_weight:.4f}|"
        f"{activity}|"
        f"{plan}"
    )


    if st.session_state.get(
        "last_saved_calculation_id"
    ) != calculation_id:

        try:

            worksheet = get_google_sheet()


            # -------------------------------------------------
            # INDIA / IST DATE AND TIME
            # -------------------------------------------------

            now = datetime.now(
                ZoneInfo("Asia/Kolkata")
            )

            date = now.strftime(
                "%Y-%m-%d"
            )

            time = now.strftime(
                "%I:%M:%S %p"
            )


            # -------------------------------------------------
            # GOOGLE SHEET ROW
            # -------------------------------------------------

            row = [

                calculation["name"],
                date,
                time,
                calculation["age"],
                calculation["sex"],
                round(
                    calculation["weight_kg"],
                    2
                ),
                round(
                    calculation["height_cm"],
                    2
                ),
                round(
                    calculation["target_weight"],
                    2
                ),
                calculation["activity"],
                round(
                    calculation["bmi"],
                    2
                ),
                round(
                    calculation["bmr"],
                    0
                ),
                round(
                    calculation["tdee"],
                    0
                ),
                calculation["plan"],
                round(
                    calculation["daily_calorie_target"],
                    0
                ),
                round(
                    calculation["estimated_days"],
                    0
                ),
                round(
                    calculation["estimated_weeks"],
                    1
                ),
                round(
                    calculation["estimated_months"],
                    1
                )
            ]


            # -------------------------------------------------
            # AUTOMATICALLY APPEND ROW
            # -------------------------------------------------

            worksheet.append_row(
                row,
                value_input_option="USER_ENTERED"
            )


            # Remember that this calculation has been saved.

            st.session_state[
                "last_saved_calculation_id"
            ] = calculation_id


            st.success(
                "✅ Results automatically saved "
                "to Google Sheet."
            )


        except Exception as e:

            st.error(
                f"❌ Could not save results to "
                f"Google Sheet: {e}"
            )


    # =====================================================
    # STORE CALCULATION FOR PDF
    # =====================================================

    st.session_state[
        "calculation"
    ] = calculation


# =========================================================
# PDF SECTION
# =========================================================

if "calculation" in st.session_state:

    data = st.session_state["calculation"]


    st.subheader(
        "📄 Download Report"
    )


    # -----------------------------------------------------
    # CREATE PDF
    # -----------------------------------------------------

    pdf_file = create_pdf(

        data["name"],
        data["age"],
        data["sex"],
        data["weight_kg"],
        data["height_cm"],
        data["target_weight"],
        data["activity"],
        data["bmi"],
        data["bmr"],
        data["tdee"],
        data["plan"],
        data["daily_calorie_target"],
        data["estimated_days"],
        data["estimated_weeks"],
        data["estimated_months"]
    )


    # -----------------------------------------------------
    # DOWNLOAD BUTTON
    # -----------------------------------------------------

    st.download_button(

        label="📥 Download PDF Report",

        data=pdf_file,

        file_name=(
            f"BMI_Report_"
            f"{data['name'].replace(' ', '_')}.pdf"
        ),

        mime="application/pdf"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "For educational and informational purposes. "
    "Calculations are estimates and should not replace "
    "individual medical assessment."
)
