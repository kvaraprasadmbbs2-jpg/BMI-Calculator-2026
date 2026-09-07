import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="BMI & Weight Management Calculator",
    page_icon="🩺",
    layout="centered"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .result-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        text-align: center;
        margin-bottom: 10px;
    }

    .result-value {
        font-size: 28px;
        font-weight: 700;
    }

    .result-label {
        font-size: 14px;
        opacity: 0.75;
    }

    .result-sub {
        font-size: 13px;
        margin-top: 4px;
    }

    .info-card {
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-top: 10px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# GOOGLE SHEET CONNECTION
# =====================================================

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


# =====================================================
# PDF CREATION
# =====================================================

def create_pdf(data):

    file_path = "/tmp/bmi_report.pdf"

    pdf = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4

    y = height - 25 * mm

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        20 * mm,
        y,
        "BMI & Weight Management Report"
    )

    y -= 15 * mm

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        20 * mm,
        y,
        f"Name: {data['name']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Date: {data['date']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Time: {data['time']}"
    )

    y -= 12 * mm

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(
        20 * mm,
        y,
        "Measurements"
    )

    y -= 9 * mm

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        20 * mm,
        y,
        f"Age: {data['age']} years"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Sex: {data['sex']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Weight: {data['weight_kg']:.1f} kg"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Height: {data['height_cm']:.1f} cm"
    )

    y -= 12 * mm

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(
        20 * mm,
        y,
        "Results"
    )

    y -= 9 * mm

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        20 * mm,
        y,
        f"BMI: {data['bmi']:.1f}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"BMI Category: {data['bmi_category']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"BMR: {data['bmr']:.0f} kcal/day"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"TDEE: {data['tdee']:.0f} kcal/day"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Activity Level: {data['activity']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Description: {data['activity_description']}"
    )

    y -= 12 * mm

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(
        20 * mm,
        y,
        "Weight Management"
    )

    y -= 9 * mm

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        20 * mm,
        y,
        f"Target Weight: {data['target_weight_kg']:.1f} kg"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Weight Loss Plan: {data['weight_loss_plan']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Daily Calorie Target: {data['daily_calorie_target']:.0f} kcal/day"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Estimated Days: {data['estimated_days']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Estimated Weeks: {data['estimated_weeks']:.1f}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Estimated Months: {data['estimated_months']:.1f}"
    )

    y -= 12 * mm

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(
        20 * mm,
        y,
        "Healthy Weight Range"
    )

    y -= 9 * mm

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        20 * mm,
        y,
        f"{data['healthy_min']:.1f} - {data['healthy_max']:.1f} kg"
    )

    y -= 18 * mm

    pdf.setFont("Helvetica", 9)

    pdf.drawString(
        20 * mm,
        y,
        "This calculator provides an estimate for educational purposes."
    )

    pdf.drawString(
        20 * mm,
        y - 5 * mm,
        "Individual calorie and weight-management needs may vary."
    )

    pdf.save()

    return file_path


# =====================================================
# ACTIVITY LEVEL DESCRIPTIONS
# =====================================================

activity_descriptions = {

    "Sedentary":
        "Little or no exercise; mostly sitting or desk-based activity.",

    "Lightly active":
        "Light exercise or walking 1–3 days per week.",

    "Moderately active":
        "Moderate exercise or physical activity 3–5 days per week.",

    "Very active":
        "Hard exercise or physical activity 6–7 days per week.",

    "Extra active":
        "Very hard daily exercise, physical job, or intensive training."
}


# =====================================================
# TITLE
# =====================================================

st.title("🩺 BMI & Weight Management Calculator")

st.caption(
    "Calculate BMI, BMR, TDEE and estimate your daily calorie requirement."
)


# =====================================================
# USER INPUTS
# =====================================================

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


# =====================================================
# WEIGHT
# =====================================================

weight_unit = st.selectbox(
    "Select weight unit",
    ["kg", "lb"]
)

weight = st.number_input(
    f"Enter weight ({weight_unit})",
    min_value=1.0,
    max_value=500.0,
    value=None,
    placeholder=f"Enter weight in {weight_unit}"
)


# =====================================================
# HEIGHT
# =====================================================

height_unit = st.selectbox(
    "Select height unit",
    ["cm", "ft/in"]
)


if height_unit == "cm":

    height_cm_input = st.number_input(
        "Enter height (cm)",
        min_value=50.0,
        max_value=250.0,
        value=None,
        placeholder="Enter height in cm"
    )

    height_ft = None
    height_in = None

else:

    height_ft = st.number_input(
        "Enter height (feet)",
        min_value=1,
        max_value=8,
        value=None,
        placeholder="Feet"
    )

    height_in = st.number_input(
        "Enter height (inches)",
        min_value=0.0,
        max_value=11.99,
        value=None,
        placeholder="Inches"
    )

    height_cm_input = None


# =====================================================
# TARGET WEIGHT
# =====================================================

target_weight_unit = st.selectbox(
    "Select target weight unit",
    ["kg", "lb"]
)

target_weight = st.number_input(
    f"Enter target weight ({target_weight_unit})",
    min_value=1.0,
    max_value=500.0,
    value=None,
    placeholder=f"Enter target weight in {target_weight_unit}"
)


# =====================================================
# ACTIVITY LEVEL
# =====================================================

activity = st.selectbox(
    "Select activity level",
    [
        "Sedentary",
        "Lightly active",
        "Moderately active",
        "Very active",
        "Extra active"
    ],
    label_visibility="collapsed"
)


# Dynamic activity description
st.markdown(
    f"**Select activity level:** {activity} "
    f"*({activity_descriptions[activity]})*"
)


# =====================================================
# SESSION STATE
# =====================================================

if "calculation" not in st.session_state:
    st.session_state.calculation = None

if "last_plan" not in st.session_state:
    st.session_state.last_plan = None

if "sheet_row" not in st.session_state:
    st.session_state.sheet_row = None


# =====================================================
# CALCULATE BUTTON
# =====================================================

calculate = st.button(
    "🧮 Calculate",
    use_container_width=True
)


if calculate:

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------

    if not name.strip():

        st.error("Please enter your name.")

        st.stop()


    if age is None:

        st.error("Please enter your age.")

        st.stop()


    if weight is None:

        st.error("Please enter your weight.")

        st.stop()


    if target_weight is None:

        st.error("Please enter your target weight.")

        st.stop()


    # -------------------------------------------------
    # WEIGHT CONVERSION
    # -------------------------------------------------

    if weight_unit == "kg":

        weight_kg = float(weight)

    else:

        weight_kg = float(weight) * 0.45359237


    # -------------------------------------------------
    # HEIGHT CONVERSION
    # -------------------------------------------------

    if height_unit == "cm":

        if height_cm_input is None:

            st.error("Please enter your height.")

            st.stop()

        height_cm = float(height_cm_input)

    else:

        if height_ft is None or height_in is None:

            st.error("Please enter both feet and inches.")

            st.stop()

        height_cm = (
            float(height_ft) * 30.48
            + float(height_in) * 2.54
        )


    # -------------------------------------------------
    # TARGET WEIGHT CONVERSION
    # -------------------------------------------------

    if target_weight_unit == "kg":

        target_weight_kg = float(target_weight)

    else:

        target_weight_kg = float(target_weight) * 0.45359237


    # -------------------------------------------------
    # HEIGHT IN METERS
    # -------------------------------------------------

    height_m = height_cm / 100


    # -------------------------------------------------
    # BMI
    # -------------------------------------------------

    bmi = weight_kg / (height_m ** 2)


    if bmi < 18.5:

        bmi_category = "Underweight"

    elif bmi < 25:

        bmi_category = "Normal weight"

    elif bmi < 30:

        bmi_category = "Overweight"

    else:

        bmi_category = "Obesity"


    # -------------------------------------------------
    # BMR
    # Mifflin-St Jeor equation
    # -------------------------------------------------

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


    # -------------------------------------------------
    # ACTIVITY FACTOR
    # -------------------------------------------------

    activity_factors = {

        "Sedentary": 1.20,

        "Lightly active": 1.375,

        "Moderately active": 1.55,

        "Very active": 1.725,

        "Extra active": 1.90
    }


    activity_factor = activity_factors[activity]


    # -------------------------------------------------
    # TDEE
    # -------------------------------------------------

    tdee = bmr * activity_factor


    # -------------------------------------------------
    # HEALTHY WEIGHT RANGE
    # BMI 18.5 – 24.9
    # -------------------------------------------------

    healthy_min = 18.5 * (height_m ** 2)

    healthy_max = 24.9 * (height_m ** 2)


    # -------------------------------------------------
    # IST DATE & TIME
    # -------------------------------------------------

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    date = now.strftime("%d-%m-%Y")

    time = now.strftime("%I:%M:%S %p")


    # -------------------------------------------------
    # STORE CALCULATION
    # -------------------------------------------------

    st.session_state.calculation = {

        "name": name.strip(),

        "age": int(age),

        "sex": sex,

        "weight_kg": weight_kg,

        "height_cm": height_cm,

        "target_weight_kg": target_weight_kg,

        "activity": activity,

        "activity_description":
            activity_descriptions[activity],

        "bmi": bmi,

        "bmi_category":
            bmi_category,

        "bmr": bmr,

        "tdee": tdee,

        "healthy_min":
            healthy_min,

        "healthy_max":
            healthy_max,

        "date": date,

        "time": time
    }


    # Reset plan selection tracking
    st.session_state.last_plan = None

    st.session_state.sheet_row = None


# =====================================================
# DISPLAY RESULTS
# =====================================================

if st.session_state.calculation is not None:

    data = st.session_state.calculation


    st.divider()

    st.subheader("📊 Your Results")


    # =================================================
    # PROFESSIONAL RESULT DASHBOARD
    # =================================================

    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    BMI
                </div>

                <div class="result-value">
                    {data['bmi']:.1f}
                </div>

                <div class="result-sub">
                    {data['bmi_category']}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    BMR
                </div>

                <div class="result-value">
                    {data['bmr']:.0f}
                </div>

                <div class="result-sub">
                    kcal/day
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    col3, col4 = st.columns(2)


    with col3:

        st.markdown(
            f"""
            <div class="result-card">

                <div class="result-label">
                    TDEE
                </div>

                <div class="result-value">
                    {data['tdee']:.0f}
                </div>

                <div class="result-sub">
                    kcal/day
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            """
            <div class="result-card">

                <div class="result-label">
                    BMI Status
                </div>

                <div class="result-value">
                    ✓
                </div>

                <div class="result-sub">
                    Assessment complete
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =================================================
    # HEALTHY WEIGHT RANGE
    # =================================================

    st.markdown(
        f"""
        <div class="info-card">

        <b>🎯 Healthy weight range</b><br><br>

        {data['healthy_min']:.1f} – {data['healthy_max']:.1f} kg

        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # ACTIVITY LEVEL
    # =================================================

    st.markdown(
        f"**Select activity level:** "
        f"{data['activity']} "
        f"*({data['activity_description']})*"
    )


    # =================================================
    # WEIGHT LOSS PLAN
    # =================================================

    st.subheader("⚖️ Select your weight loss plan")


    weight_loss_plan = st.selectbox(

        "Choose your plan",

        [
            "Mild",
            "Moderate",
            "More aggressive"
        ],

        label_visibility="collapsed"
    )


    # =================================================
    # CALORIE DEFICIT
    # =================================================

    calorie_deficits = {

        "Mild": 250,

        "Moderate": 500,

        "More aggressive": 750
    }


    deficit = calorie_deficits[
        weight_loss_plan
    ]


    # =================================================
    # DAILY CALORIE TARGET
    # =================================================

    daily_calorie_target = max(
        data["tdee"] - deficit,
        1200
    )


    # =================================================
    # WEIGHT DIFFERENCE
    # =================================================

    weight_to_lose = (
        data["weight_kg"]
        - data["target_weight_kg"]
    )


    # =================================================
    # ESTIMATED WEIGHT LOSS TIME
    # =================================================

    if weight_to_lose > 0:

        total_calorie_deficit = (
            weight_to_lose * 7700
        )

        estimated_days = (
            total_calorie_deficit / deficit
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


    # =================================================
    # WEIGHT LOSS RESULTS
    # =================================================

    st.markdown(
        f"""
        <div class="info-card">

        <b>🔥 Daily calorie target</b><br>

        {daily_calorie_target:.0f} kcal/day

        <br><br>

        <b>📉 Estimated weight loss</b><br>

        {weight_to_lose:.1f} kg

        <br><br>

        <b>⏱️ Estimated time</b><br>

        {estimated_days:.0f} days
        ({estimated_weeks:.1f} weeks /
        {estimated_months:.1f} months)

        </div>
        """,
        unsafe_allow_html=True
    )


    # =================================================
    # UPDATE DATA DICTIONARY
    # =================================================

    data["weight_loss_plan"] = weight_loss_plan

    data["daily_calorie_target"] = (
        daily_calorie_target
    )

    data["estimated_days"] = (
        round(estimated_days)
    )

    data["estimated_weeks"] = (
        round(estimated_weeks, 1)
    )

    data["estimated_months"] = (
        round(estimated_months, 1)
    )


    # =================================================
    # GOOGLE SHEET AUTOMATIC SAVE / UPDATE
    # =================================================

    try:

        worksheet = get_google_sheet()


        # ------------------------------------------------
        # FIRST SAVE
        # ------------------------------------------------

        if st.session_state.sheet_row is None:

            row = [

                data["name"],

                data["date"],

                data["time"],

                data["age"],

                data["sex"],

                round(data["weight_kg"], 2),

                round(data["height_cm"], 2),

                round(data["target_weight_kg"], 2),

                data["activity"],

                round(data["bmi"], 2),

                round(data["bmr"], 0),

                round(data["tdee"], 0),

                data["weight_loss_plan"],

                round(data["daily_calorie_target"], 0),

                data["estimated_days"],

                data["estimated_weeks"],

                data["estimated_months"]
            ]


            worksheet.append_row(
                row,
                value_input_option="USER_ENTERED"
            )


            # Get the last row number
            st.session_state.sheet_row = (
                len(worksheet.get_all_values())
            )


            st.session_state.last_plan = (
                weight_loss_plan
            )


        # ------------------------------------------------
        # UPDATE EXISTING ROW
        # ------------------------------------------------

        elif (
            st.session_state.last_plan
            != weight_loss_plan
        ):

            row_number = (
                st.session_state.sheet_row
            )


            worksheet.update(
                f"M{row_number}:Q{row_number}",
                [[
                    data["weight_loss_plan"],

                    round(
                        data["daily_calorie_target"],
                        0
                    ),

                    data["estimated_days"],

                    data["estimated_weeks"],

                    data["estimated_months"]
                ]]
            )


            st.session_state.last_plan = (
                weight_loss_plan
            )


    except Exception as e:

        print(
            "Google Sheet error:",
            e
        )


    # =================================================
    # PDF REPORT
    # =================================================

    pdf_file = create_pdf(data)


    st.download_button(

        label="📄 Download PDF Report",

        data=open(pdf_file, "rb").read(),

        file_name="BMI_Weight_Management_Report.pdf",

        mime="application/pdf",

        use_container_width=True
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "BMI & Weight Management Calculator"
)

st.caption(
    "For educational and informational purposes."
)
