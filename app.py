import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="BMI & Weight Management Calculator",
    page_icon="🩺",
    layout="centered"
)


# =========================================================
# GOOGLE SHEET CONNECTION
# =========================================================

@st.cache_resource
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

    spreadsheet = client.open(
        "BMI Calculator Visitor Log"
    )

    worksheet = spreadsheet.sheet1

    return worksheet


# =========================================================
# PDF REPORT
# =========================================================

def create_pdf(data):

    file_path = "/tmp/bmi_report.pdf"

    pdf = canvas.Canvas(
        file_path,
        pagesize=A4
    )

    width, height = A4

    y = height - 25 * mm

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        20 * mm,
        y,
        "BMI & Weight Management Report"
    )

    y -= 15 * mm

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica",
        11
    )

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

    # -----------------------------------------------------
    # MEASUREMENTS
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        20 * mm,
        y,
        "Measurements"
    )

    y -= 9 * mm

    pdf.setFont(
        "Helvetica",
        11
    )

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

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        20 * mm,
        y,
        "Results"
    )

    y -= 9 * mm

    pdf.setFont(
        "Helvetica",
        11
    )

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

    # -----------------------------------------------------
    # WEIGHT MANAGEMENT
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        20 * mm,
        y,
        "Weight Management"
    )

    y -= 9 * mm

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        20 * mm,
        y,
        f"Target Weight: "
        f"{data['target_weight_kg']:.1f} kg"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Weight Loss Plan: "
        f"{data['weight_loss_plan']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Daily Calorie Target: "
        f"{data['daily_calorie_target']:.0f} kcal/day"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Estimated Days: "
        f"{data['estimated_days']}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Estimated Weeks: "
        f"{data['estimated_weeks']:.1f}"
    )

    y -= 7 * mm

    pdf.drawString(
        20 * mm,
        y,
        f"Estimated Months: "
        f"{data['estimated_months']:.1f}"
    )

    y -= 12 * mm

    # -----------------------------------------------------
    # HEALTHY WEIGHT
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        20 * mm,
        y,
        "Healthy Weight Range"
    )

    y -= 9 * mm

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        20 * mm,
        y,
        f"{data['healthy_min']:.1f} - "
        f"{data['healthy_max']:.1f} kg"
    )

    y -= 18 * mm

    # -----------------------------------------------------
    # DISCLAIMER
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica",
        9
    )

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


# =========================================================
# ACTIVITY LEVELS
# =========================================================

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


activity_factors = {

    "Sedentary": 1.20,

    "Lightly active": 1.375,

    "Moderately active": 1.55,

    "Very active": 1.725,

    "Extra active": 1.90
}


# =========================================================
# WEIGHT LOSS PLANS
# =========================================================

calorie_deficits = {

    "Mild": 250,

    "Moderate": 500,

    "More aggressive": 750
}


# =========================================================
# TITLE
# =========================================================

st.title(
    "🩺 BMI & Weight Management Calculator"
)

st.caption(
    "Calculate BMI, BMR, TDEE and estimate your daily calorie requirement."
)


# =========================================================
# USER INPUTS
# =========================================================

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
    [
        "Male",
        "Female"
    ]
)


# =========================================================
# WEIGHT
# =========================================================

weight_unit = st.selectbox(
    "Select weight unit",
    [
        "kg",
        "lb"
    ]
)


weight = st.number_input(
    f"Enter weight ({weight_unit})",
    min_value=1.0,
    max_value=500.0,
    value=None,
    placeholder=f"Enter weight in {weight_unit}"
)


# =========================================================
# HEIGHT
# =========================================================

height_unit = st.selectbox(
    "Select height unit",
    [
        "cm",
        "ft/in"
    ]
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


# =========================================================
# TARGET WEIGHT
# =========================================================

target_weight_unit = st.selectbox(
    "Select target weight unit",
    [
        "kg",
        "lb"
    ]
)


target_weight = st.number_input(
    f"Enter target weight ({target_weight_unit})",
    min_value=1.0,
    max_value=500.0,
    value=None,
    placeholder=f"Enter target weight in {target_weight_unit}"
)


# =========================================================
# ACTIVITY LEVEL
# =========================================================

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


# Dynamic single-line activity description

st.markdown(
    f"**Select activity level:** {activity} "
    f"*({activity_descriptions[activity]})*"
)


# =========================================================
# SESSION STATE
# =========================================================

if "calculation" not in st.session_state:

    st.session_state.calculation = None


if "last_plan" not in st.session_state:

    st.session_state.last_plan = None


if "sheet_row" not in st.session_state:

    st.session_state.sheet_row = None


# =========================================================
# CALCULATE BUTTON
# =========================================================

calculate = st.button(
    "🧮 Calculate",
    use_container_width=True
)


# =========================================================
# CALCULATION
# =========================================================

if calculate:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not name.strip():

        st.error(
            "Please enter your name."
        )

        st.stop()


    if age is None:

        st.error(
            "Please enter your age."
        )

        st.stop()


    if weight is None:

        st.error(
            "Please enter your weight."
        )

        st.stop()


    if target_weight is None:

        st.error(
            "Please enter your target weight."
        )

        st.stop()


    # -----------------------------------------------------
    # CONVERT WEIGHT TO KG
    # -----------------------------------------------------

    if weight_unit == "kg":

        weight_kg = float(weight)

    else:

        weight_kg = (
            float(weight)
            *
            0.45359237
        )


    # -----------------------------------------------------
    # CONVERT HEIGHT TO CM
    # -----------------------------------------------------

    if height_unit == "cm":

        if height_cm_input is None:

            st.error(
                "Please enter your height."
            )

            st.stop()

        height_cm = float(
            height_cm_input
        )

    else:

        if (
            height_ft is None
            or
            height_in is None
        ):

            st.error(
                "Please enter both feet and inches."
            )

            st.stop()

        height_cm = (
            float(height_ft) * 30.48
            +
            float(height_in) * 2.54
        )


    # -----------------------------------------------------
    # CONVERT TARGET WEIGHT TO KG
    # -----------------------------------------------------

    if target_weight_unit == "kg":

        target_weight_kg = float(
            target_weight
        )

    else:

        target_weight_kg = (
            float(target_weight)
            *
            0.45359237
        )


    # -----------------------------------------------------
    # HEIGHT IN METERS
    # -----------------------------------------------------

    height_m = (
        height_cm / 100
    )


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    bmi = (
        weight_kg
        /
        (height_m ** 2)
    )


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


    # -----------------------------------------------------
    # BMR — MIFFLIN-ST JEOR
    # -----------------------------------------------------

    if sex == "Male":

        bmr = (
            10 * weight_kg
            +
            6.25 * height_cm
            -
            5 * int(age)
            +
            5
        )

    else:

        bmr = (
            10 * weight_kg
            +
            6.25 * height_cm
            -
            5 * int(age)
            -
            161
        )


    # -----------------------------------------------------
    # TDEE
    # -----------------------------------------------------

    activity_factor = (
        activity_factors[activity]
    )

    tdee = (
        bmr
        *
        activity_factor
    )


    # -----------------------------------------------------
    # HEALTHY WEIGHT RANGE
    # -----------------------------------------------------

    healthy_min = (
        18.5
        *
        (height_m ** 2)
    )

    healthy_max = (
        24.9
        *
        (height_m ** 2)
    )


    # -----------------------------------------------------
    # IST DATE AND TIME
    # -----------------------------------------------------

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    date = now.strftime(
        "%d-%m-%Y"
    )

    time = now.strftime(
        "%I:%M:%S %p"
    )


    # -----------------------------------------------------
    # STORE CALCULATION
    # -----------------------------------------------------

    st.session_state.calculation = {

        "name": name.strip(),

        "age": int(age),

        "sex": sex,

        "weight_kg": weight_kg,

        "height_cm": height_cm,

        "target_weight_kg":
            target_weight_kg,

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


    # Reset Google Sheet row for new calculation

    st.session_state.last_plan = None

    st.session_state.sheet_row = None


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state.calculation is not None:

    data = st.session_state.calculation

    st.divider()

    st.subheader(
        "📊 Your Results"
    )


    # =====================================================
    # DASHBOARD
    # Native Streamlit components
    # =====================================================

    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            label="BMI",
            value=f"{data['bmi']:.1f}",
            delta=data["bmi_category"],
            delta_color="off"
        )


    with col2:

        st.metric(
            label="BMR",
            value=f"{data['bmr']:.0f} kcal/day"
        )


    col3, col4 = st.columns(2)


    with col3:

        st.metric(
            label="TDEE",
            value=f"{data['tdee']:.0f} kcal/day"
        )


    with col4:

        st.metric(
            label="Healthy Weight",
            value=(
                f"{data['healthy_min']:.1f}–"
                f"{data['healthy_max']:.1f} kg"
            )
        )


    # =====================================================
    # HEALTHY WEIGHT
    # =====================================================

    st.info(
        f"🎯 **Healthy weight range:** "
        f"{data['healthy_min']:.1f} – "
        f"{data['healthy_max']:.1f} kg"
    )


    # =====================================================
    # ACTIVITY
    # =====================================================

    st.markdown(
        f"**Select activity level:** "
        f"{data['activity']} "
        f"*({data['activity_description']})*"
    )


    # =====================================================
    # WEIGHT LOSS PLAN
    # =====================================================

    st.subheader(
        "⚖️ Select your weight loss plan"
    )


    weight_loss_plan = st.selectbox(

        "Choose your plan",

        [
            "Mild",
            "Moderate",
            "More aggressive"
        ],

        label_visibility="collapsed"
    )


    # =====================================================
    # CALORIE DEFICIT
    # =====================================================

    deficit = (
        calorie_deficits[
            weight_loss_plan
        ]
    )


    daily_calorie_target = max(
        data["tdee"] - deficit,
        1200
    )


    # =====================================================
    # WEIGHT DIFFERENCE
    # =====================================================

    weight_to_lose = (
        data["weight_kg"]
        -
        data["target_weight_kg"]
    )


    # =====================================================
    # ESTIMATED TIME
    # =====================================================

    if weight_to_lose > 0:

        total_calorie_deficit = (
            weight_to_lose
            *
            7700
        )

        estimated_days = (
            total_calorie_deficit
            /
            deficit
        )

        estimated_weeks = (
            estimated_days
            /
            7
        )

        estimated_months = (
            estimated_days
            /
            30.44
        )

    else:

        estimated_days = 0

        estimated_weeks = 0

        estimated_months = 0


    # =====================================================
    # WEIGHT GOAL
    # =====================================================

    if weight_to_lose > 0:

        st.subheader(
            "📉 Weight-loss goal"
        )

        st.write(
            f"**Current weight:** "
            f"{data['weight_kg']:.1f} kg"
        )

        st.write(
            f"**Target weight:** "
            f"{data['target_weight_kg']:.1f} kg"
        )

        st.write(
            f"**Weight to lose:** "
            f"{weight_to_lose:.1f} kg"
        )


        # -------------------------------------------------
        # GOAL BAR
        # -------------------------------------------------
        #
        # At the initial calculation, progress is 0%.
        # The bar represents actual progress only when
        # a future weight-tracking feature is added.
        #
        # For now, show the size of the goal separately.

        goal_size_percent = (
            weight_to_lose
            /
            data["weight_kg"]
            *
            100
        )

        goal_size_percent = min(
            max(goal_size_percent, 0),
            100
        )


        st.progress(
            int(goal_size_percent)
        )


        st.caption(
            f"Your weight-loss goal is "
            f"{goal_size_percent:.1f}% "
            f"of your current body weight."
        )


    elif weight_to_lose == 0:

        st.success(
            "🎯 You are already at your target weight."
        )


    else:

        weight_to_gain = abs(
            weight_to_lose
        )

        st.info(
            f"🎯 Your target weight is "
            f"{weight_to_gain:.1f} kg above your "
            f"current weight."
        )


    # =====================================================
    # DAILY CALORIE TARGET
    # =====================================================

    st.subheader(
        "🔥 Daily calorie target"
    )

    st.metric(
        label="Recommended daily calorie target",
        value=f"{daily_calorie_target:.0f} kcal/day"
    )


    # =====================================================
    # ESTIMATED WEIGHT LOSS
    # =====================================================

    if weight_to_lose > 0:

        st.subheader(
            "⏱️ Estimated weight-loss time"
        )

        col5, col6, col7 = st.columns(3)


        with col5:

            st.metric(
                "Days",
                f"{estimated_days:.0f}"
            )


        with col6:

            st.metric(
                "Weeks",
                f"{estimated_weeks:.1f}"
            )


        with col7:

            st.metric(
                "Months",
                f"{estimated_months:.1f}"
            )


        st.caption(
            "This is an estimate based on an assumed "
            "7,700 kcal energy deficit per kg of weight loss."
        )


    elif weight_to_lose == 0:

        st.success(
            "Target weight already reached."
        )


    # =====================================================
    # SAVE WEIGHT MANAGEMENT DATA
    # =====================================================

    data["weight_loss_plan"] = (
        weight_loss_plan
    )

    data["daily_calorie_target"] = (
        daily_calorie_target
    )

    data["estimated_days"] = round(
        estimated_days
    )

    data["estimated_weeks"] = round(
        estimated_weeks,
        1
    )

    data["estimated_months"] = round(
        estimated_months,
        1
    )


    # =====================================================
    # GOOGLE SHEET
    # =====================================================

    try:

        worksheet = get_google_sheet()


        # -------------------------------------------------
        # FIRST SAVE
        # -------------------------------------------------

        if st.session_state.sheet_row is None:

            row = [

                data["name"],

                data["date"],

                data["time"],

                data["age"],

                data["sex"],

                round(
                    data["weight_kg"],
                    2
                ),

                round(
                    data["height_cm"],
                    2
                ),

                round(
                    data["target_weight_kg"],
                    2
                ),

                data["activity"],

                round(
                    data["bmi"],
                    2
                ),

                round(
                    data["bmr"],
                    0
                ),

                round(
                    data["tdee"],
                    0
                ),

                data["weight_loss_plan"],

                round(
                    data["daily_calorie_target"],
                    0
                ),

                data["estimated_days"],

                data["estimated_weeks"],

                data["estimated_months"]
            ]


            result = worksheet.append_row(

                row,

                value_input_option="USER_ENTERED",

                include_values_in_response=True
            )


            # -------------------------------------------------
            # FIND ACTUAL SAVED ROW
            # -------------------------------------------------

            if (
                result
                and result.get("updates")
                and result["updates"].get("updatedRange")
            ):

                updated_range = (
                    result["updates"]["updatedRange"]
                )

                range_part = (
                    updated_range.split("!")[-1]
                )

                start_cell = (
                    range_part.split(":")[0]
                )

                row_number = int(
                    "".join(
                        char
                        for char in start_cell
                        if char.isdigit()
                    )
                )

                st.session_state.sheet_row = (
                    row_number
                )

            else:

                st.session_state.sheet_row = len(
                    worksheet.get_all_values()
                )


            st.session_state.last_plan = (
                weight_loss_plan
            )


        # -------------------------------------------------
        # CHANGE PLAN
        # -------------------------------------------------

        elif (
            st.session_state.last_plan
            !=
            weight_loss_plan
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

                ]],

                value_input_option="USER_ENTERED"
            )


            st.session_state.last_plan = (
                weight_loss_plan
            )


    except Exception as e:

        # Keep technical Google Sheet errors
        # hidden from the visitor.

        print(
            "Google Sheet error:",
            repr(e)
        )


    # =====================================================
    # PDF REPORT
    # =====================================================

    pdf_file = create_pdf(
        data
    )


    with open(
        pdf_file,
        "rb"
    ) as pdf:

        st.download_button(

            label="📄 Download PDF Report",

            data=pdf.read(),

            file_name=(
                "BMI_Weight_Management_Report.pdf"
            ),

            mime="application/pdf",

            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "BMI & Weight Management Calculator"
)

st.caption(
    "For educational and informational purposes."
)
