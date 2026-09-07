import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from zoneinfo import ZoneInfo
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
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 700px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1 {
        text-align: center;
    }

    .stButton > button {
        width: 100%;
        height: 3em;
        font-size: 18px;
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

    spreadsheet = client.open(
        "BMI Calculator Visitor Log"
    )

    worksheet = spreadsheet.sheet1

    return worksheet


# =========================================================
# PDF CREATION
# =========================================================

def create_pdf(data):

    buffer = io.BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    width, height = A4

    y = height - 50

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        18
    )

    pdf.drawString(
        50,
        y,
        "BMI & Weight Management Report"
    )

    y -= 40

    # -----------------------------------------------------
    # BASIC INFORMATION
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        f"Name: {data['name']}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Date: {data['date']}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Time: {data['time']}"
    )

    y -= 30

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        50,
        y,
        "Basic Information"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        f"Age: {data['age']} years"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Sex: {data['sex']}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Weight: {data['weight_kg']:.1f} kg"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Height: {data['height_cm']:.1f} cm"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Target Weight: "
        f"{data['target_weight_kg']:.1f} kg"
    )

    y -= 35

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        50,
        y,
        "Results"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        f"BMI: {data['bmi']:.1f}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"BMI Category: "
        f"{data['bmi_category']}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"BMR: {data['bmr']:.0f} kcal/day"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"TDEE: {data['tdee']:.0f} kcal/day"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Activity Level: "
        f"{data['activity']}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Description: "
        f"{data['activity_description']}"
    )

    y -= 30

    # -----------------------------------------------------
    # WEIGHT LOSS PLAN
    # -----------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        50,
        y,
        "Weight Loss Plan"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        f"Plan: {data['plan']}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Daily Calorie Target: "
        f"{data['daily_calorie_target']:.0f} kcal"
    )

    y -= 20

    if data["weight_to_lose"] > 0:

        pdf.drawString(
            50,
            y,
            f"Weight to Lose: "
            f"{data['weight_to_lose']:.1f} kg"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Estimated Days: "
            f"{data['estimated_days']:.0f}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Estimated Weeks: "
            f"{data['estimated_weeks']:.1f}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"Estimated Months: "
            f"{data['estimated_months']:.1f}"
        )

    else:

        pdf.drawString(
            50,
            y,
            "Estimated weight loss: Not required"
        )

    y -= 35

    pdf.setFont(
        "Helvetica-Oblique",
        9
    )

    pdf.drawString(
        50,
        y,
        "This calculator provides an estimate "
        "and is not a substitute for medical advice."
    )

    pdf.save()

    buffer.seek(0)

    return buffer


# =========================================================
# ACTIVITY DESCRIPTIONS
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


# =========================================================
# TITLE
# =========================================================

st.title(
    "🩺 BMI & Weight Management Calculator"
)


# =========================================================
# NAME
# =========================================================

name = st.text_input(
    "Enter your name"
)


# =========================================================
# AGE
# =========================================================

age = st.number_input(
    "Enter your age",
    min_value=1,
    max_value=120,
    value=None,
    placeholder="Enter age"
)


# =========================================================
# SEX
# =========================================================

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
    min_value=0.1,
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
        "feet/inches"
    ]
)


if height_unit == "cm":

    height_cm_input = st.number_input(
        "Enter height (cm)",
        min_value=1.0,
        value=None,
        placeholder="Enter height in cm"
    )

    height_feet = None
    height_inches = None

else:

    height_feet = st.number_input(
        "Enter height (feet)",
        min_value=1,
        max_value=8,
        value=None,
        placeholder="Feet"
    )

    height_inches = st.number_input(
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
    min_value=0.1,
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


# =========================================================
# ACTIVITY LEVEL DISPLAY WHILE FILLING
# =========================================================

st.markdown(
    f"**Select activity level:** {activity} "
    f"*({activity_descriptions[activity]})*"
)


# =========================================================
# SESSION STATE
# =========================================================

if "calculation" not in st.session_state:

    st.session_state["calculation"] = None


if "sheet_row" not in st.session_state:

    st.session_state["sheet_row"] = None


if "base_id" not in st.session_state:

    st.session_state["base_id"] = None


if "last_saved_plan" not in st.session_state:

    st.session_state["last_saved_plan"] = None


if "selected_plan" not in st.session_state:

    st.session_state["selected_plan"] = "Select a plan"


# =========================================================
# CALCULATE BUTTON
# =========================================================

calculate_button = st.button(
    "🧮 Calculate"
)


if calculate_button:

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
            height_feet is None
            or height_inches is None
        ):

            st.error(
                "Please enter your complete height."
            )

            st.stop()

        height_cm = (
            float(height_feet) * 30.48
            + float(height_inches) * 2.54
        )


    if target_weight is None:

        st.error(
            "Please enter your target weight."
        )

        st.stop()


    # -----------------------------------------------------
    # WEIGHT TO KG
    # -----------------------------------------------------

    if weight_unit == "kg":

        weight_kg = float(weight)

    else:

        weight_kg = (
            float(weight) * 0.453592
        )


    # -----------------------------------------------------
    # TARGET WEIGHT TO KG
    # -----------------------------------------------------

    if target_weight_unit == "kg":

        target_weight_kg = float(
            target_weight
        )

    else:

        target_weight_kg = (
            float(target_weight)
            * 0.453592
        )


    # -----------------------------------------------------
    # HEIGHT TO METERS
    # -----------------------------------------------------

    height_m = height_cm / 100


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    bmi = (
        weight_kg
        / (height_m ** 2)
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
    # ACTIVITY FACTORS
    # -----------------------------------------------------

    activity_factors = {

        "Sedentary": 1.20,

        "Lightly active": 1.375,

        "Moderately active": 1.55,

        "Very active": 1.725,

        "Extra active": 1.90
    }


    activity_factor = (
        activity_factors[activity]
    )


    # -----------------------------------------------------
    # TDEE
    # -----------------------------------------------------

    tdee = (
        bmr * activity_factor
    )


    # -----------------------------------------------------
    # INDIA TIME
    # -----------------------------------------------------

    now = datetime.now(
        ZoneInfo("Asia/Kolkata")
    )

    calculation_date = now.strftime(
        "%d-%m-%Y"
    )

    calculation_time = now.strftime(
        "%I:%M:%S %p"
    )


    # -----------------------------------------------------
    # BASE ID
    # -----------------------------------------------------

    base_id = (
        f"{name.strip().lower()}|"
        f"{age}|"
        f"{sex}|"
        f"{weight_kg:.2f}|"
        f"{height_cm:.2f}|"
        f"{target_weight_kg:.2f}|"
        f"{activity}"
    )


    # -----------------------------------------------------
    # STORE CALCULATION
    # -----------------------------------------------------

    st.session_state["calculation"] = {

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

        "date": calculation_date,

        "time": calculation_time
    }


    # -----------------------------------------------------
    # RESET PLAN TRACKING
    # -----------------------------------------------------

    st.session_state["selected_plan"] = (
        "Select a plan"
    )

    st.session_state["sheet_row"] = None

    st.session_state["base_id"] = base_id

    st.session_state["last_saved_plan"] = None


# =========================================================
# RESULTS
# =========================================================

if st.session_state["calculation"] is not None:

    data = st.session_state["calculation"]


    st.divider()

    st.subheader(
        "📊 Results"
    )


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    st.metric(
        "BMI",
        f"{data['bmi']:.1f}"
    )


    st.write(
        f"**BMI Category: "
        f"{data['bmi_category']}**"
    )


    # -----------------------------------------------------
    # BMR
    # -----------------------------------------------------

    st.write(
        f"**BMR:** "
        f"{data['bmr']:.0f} kcal/day"
    )


    # -----------------------------------------------------
    # TDEE
    # -----------------------------------------------------

    st.write(
        f"**TDEE:** "
        f"{data['tdee']:.0f} kcal/day"
    )


    # =====================================================
    # ACTIVITY LEVEL AFTER CALCULATE
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
        "🎯 Select your weight loss plan"
    )


    plan = st.selectbox(

        "Weight loss plan",

        [
            "Select a plan",
            "Mild",
            "Moderate",
            "More aggressive"
        ],

        key="selected_plan"
    )


    # =====================================================
    # PLAN CALCULATION
    # =====================================================

    if plan != "Select a plan":

        plan_deficits = {

            "Mild": 250,

            "Moderate": 500,

            "More aggressive": 750
        }


        calorie_deficit = (
            plan_deficits[plan]
        )


        daily_calorie_target = max(
            data["tdee"]
            - calorie_deficit,
            1200
        )


        # -------------------------------------------------
        # WEIGHT TO LOSE
        # -------------------------------------------------

        weight_to_lose = (
            data["weight_kg"]
            - data["target_weight_kg"]
        )


        # -------------------------------------------------
        # ESTIMATED TIME
        # -------------------------------------------------

        if weight_to_lose > 0:

            total_calorie_deficit = (
                weight_to_lose * 7700
            )

            estimated_days = (
                total_calorie_deficit
                / calorie_deficit
            )

            estimated_weeks = (
                estimated_days / 7
            )

            estimated_months = (
                estimated_days / 30.44
            )

        else:

            estimated_days = None

            estimated_weeks = None

            estimated_months = None


        # -------------------------------------------------
        # DISPLAY PLAN
        # -------------------------------------------------

        st.write(
            f"**Weight Loss Plan: {plan}**"
        )


        st.write(
            f"**Daily Calorie Target: "
            f"{daily_calorie_target:.0f} "
            f"kcal/day**"
        )


        if weight_to_lose > 0:

            st.write(
                f"**Weight to Lose: "
                f"{weight_to_lose:.1f} kg**"
            )


            st.write(
                f"**Estimated Days: "
                f"{estimated_days:.0f} days**"
            )


            st.write(
                f"**Estimated Weeks: "
                f"{estimated_weeks:.1f} weeks**"
            )


            st.write(
                f"**Estimated Months: "
                f"{estimated_months:.1f} months**"
            )

        else:

            st.write(
                "**Estimated Days:** —"
            )

            st.write(
                "**Estimated Weeks:** —"
            )

            st.write(
                "**Estimated Months:** —"
            )


        # =================================================
        # CURRENT IST DATE/TIME
        # =================================================

        now = datetime.now(
            ZoneInfo("Asia/Kolkata")
        )

        current_date = now.strftime(
            "%d-%m-%Y"
        )

        current_time = now.strftime(
            "%I:%M:%S %p"
        )


        # =================================================
        # GOOGLE SHEET ROW
        # =================================================

        row_data = [

            data["name"],

            current_date,

            current_time,

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
                2
            ),

            round(
                data["tdee"],
                2
            ),

            plan,

            round(
                daily_calorie_target,
                2
            ),

            round(
                estimated_days,
                2
            )
            if estimated_days is not None
            else "",

            round(
                estimated_weeks,
                2
            )
            if estimated_weeks is not None
            else "",

            round(
                estimated_months,
                2
            )
            if estimated_months is not None
            else ""
        ]


        # =================================================
        # AUTOMATIC GOOGLE SHEET SAVE
        # =================================================

        try:

            worksheet = get_google_sheet()


            # ------------------------------------------------
            # FIRST SAVE
            # ------------------------------------------------

            if (
                st.session_state["sheet_row"]
                is None
            ):

                worksheet.append_row(
                    row_data,
                    value_input_option="USER_ENTERED"
                )


                all_values = (
                    worksheet.get_all_values()
                )


                st.session_state["sheet_row"] = (
                    len(all_values)
                )


                st.session_state[
                    "last_saved_plan"
                ] = plan


            # ------------------------------------------------
            # UPDATE SAME ROW IF PLAN CHANGES
            # ------------------------------------------------

            elif (
                st.session_state[
                    "last_saved_plan"
                ] != plan
            ):

                row_number = (
                    st.session_state[
                        "sheet_row"
                    ]
                )


                worksheet.update(

                    range_name=(
                        f"M{row_number}:Q{row_number}"
                    ),

                    values=[[

                        plan,

                        round(
                            daily_calorie_target,
                            2
                        ),

                        round(
                            estimated_days,
                            2
                        )
                        if estimated_days is not None
                        else "",

                        round(
                            estimated_weeks,
                            2
                        )
                        if estimated_weeks is not None
                        else "",

                        round(
                            estimated_months,
                            2
                        )
                        if estimated_months is not None
                        else ""
                    ]],

                    value_input_option="USER_ENTERED"
                )


                st.session_state[
                    "last_saved_plan"
                ] = plan


        except Exception as e:

            print(
                f"Google Sheet error: {e}"
            )


        # =================================================
        # PDF DATA
        # =================================================

        pdf_data = {

            **data,

            "plan": plan,

            "daily_calorie_target":
                daily_calorie_target,

            "weight_to_lose":
                weight_to_lose,

            "estimated_days":
                estimated_days
                if estimated_days is not None
                else 0,

            "estimated_weeks":
                estimated_weeks
                if estimated_weeks is not None
                else 0,

            "estimated_months":
                estimated_months
                if estimated_months is not None
                else 0
        }


        # =================================================
        # PDF DOWNLOAD
        # =================================================

        pdf_file = create_pdf(
            pdf_data
        )


        st.download_button(

            label="📄 Download PDF Report",

            data=pdf_file,

            file_name=(
                "BMI_Report_"
                f"{data['name'].replace(' ', '_')}.pdf"
            ),

            mime="application/pdf"
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "BMI & Weight Management Calculator"
)
