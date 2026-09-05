import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    max-width: 800px;
    margin: auto;
}

h1 {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


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
# PDF CREATION
# =========================================================

def create_pdf(data):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    story = []

    story.append(
        Paragraph(
            "BMI & Weight Management Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Name:</b> {data['name']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {data['date']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Time:</b> {data['time']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Age:</b> {data['age']} years",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Sex:</b> {data['sex']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Weight:</b> {data['weight_kg']:.1f} kg",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Height:</b> {data['height_cm']:.1f} cm",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Target Weight:</b> {data['target_weight']:.1f} kg",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>BMI:</b> {data['bmi']:.1f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>BMI Category:</b> {data['bmi_category']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>BMR:</b> {data['bmr']:.0f} kcal/day",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>TDEE:</b> {data['tdee']:.0f} kcal/day",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Activity Level:</b> "
            f"{data['activity']} "
            f"({data['activity_description']})",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Weight Loss Plan:</b> {data['plan']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Daily Calorie Target:</b> "
            f"{data['daily_target']:.0f} kcal/day",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            f"<b>Estimated Weight to Lose:</b> "
            f"{data['weight_to_lose']:.1f} kg",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Estimated Days:</b> "
            f"{data['estimated_days']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Estimated Weeks:</b> "
            f"{data['estimated_weeks']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Estimated Months:</b> "
            f"{data['estimated_months']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 25))

    story.append(
        Paragraph(
            "This calculator provides an estimate for educational "
            "purposes and should not replace individualized medical advice.",
            styles["Normal"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer


# =========================================================
# ACTIVITY LEVEL DESCRIPTIONS
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

st.title("🩺 BMI & Weight Management Calculator")

st.write(
    "Enter your details below to calculate BMI, BMR, TDEE "
    "and estimated weight-loss timeline."
)


# =========================================================
# INPUTS
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
    ["Male", "Female"]
)


# =========================================================
# WEIGHT
# =========================================================

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

height_unit = st.selectbox(
    "Select height unit",
    ["cm", "ft/in"]
)


if height_unit == "cm":

    height = st.number_input(
        "Enter height (cm)",
        min_value=50.0,
        max_value=250.0,
        value=None,
        placeholder="Enter height"
    )

else:

    col1, col2 = st.columns(2)

    with col1:

        feet = st.number_input(
            "Feet",
            min_value=1,
            max_value=8,
            value=None,
            placeholder="Feet"
        )

    with col2:

        inches = st.number_input(
            "Inches",
            min_value=0.0,
            max_value=11.0,
            value=None,
            placeholder="Inches"
        )

    height = None


# =========================================================
# TARGET WEIGHT
# =========================================================

target_weight_unit = st.selectbox(
    "Select target weight unit",
    ["kg", "lb"]
)


target_weight = st.number_input(
    f"Enter target weight ({target_weight_unit})",
    min_value=1.0,
    max_value=500.0,
    value=None,
    placeholder="Enter target weight"
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
    ]
)


# =========================================================
# SESSION STATE
# =========================================================

if "base_calculation" not in st.session_state:
    st.session_state["base_calculation"] = None

if "plan_selection" not in st.session_state:
    st.session_state["plan_selection"] = "Select a plan"

if "saved_base_id" not in st.session_state:
    st.session_state["saved_base_id"] = None

if "saved_row_number" not in st.session_state:
    st.session_state["saved_row_number"] = None

if "calculation" not in st.session_state:
    st.session_state["calculation"] = None


# =========================================================
# CALCULATE BUTTON
# =========================================================

calculate = st.button(
    "🧮 Calculate",
    use_container_width=True
)


# =========================================================
# BASIC CALCULATION
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

    if height_unit == "cm":

        if height is None:

            st.error("Please enter your height.")
            st.stop()

        height_cm = float(height)

    else:

        if feet is None or inches is None:

            st.error("Please enter both feet and inches.")
            st.stop()

        height_cm = (
            float(feet) * 30.48
            + float(inches) * 2.54
        )

    if target_weight is None:

        st.error("Please enter your target weight.")
        st.stop()


    # -----------------------------------------------------
    # WEIGHT TO KG
    # -----------------------------------------------------

    if weight_unit == "kg":

        weight_kg = float(weight)

    else:

        weight_kg = float(weight) * 0.453592


    # -----------------------------------------------------
    # TARGET WEIGHT TO KG
    # -----------------------------------------------------

    if target_weight_unit == "kg":

        target_weight_kg = float(target_weight)

    else:

        target_weight_kg = float(target_weight) * 0.453592


    # -----------------------------------------------------
    # BMI
    # -----------------------------------------------------

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)


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
    # BMR — MIFFLIN ST JEOR
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
    # ACTIVITY MULTIPLIER
    # -----------------------------------------------------

    activity_multipliers = {

        "Sedentary": 1.20,

        "Lightly active": 1.375,

        "Moderately active": 1.55,

        "Very active": 1.725,

        "Extra active": 1.90
    }


    activity_factor = activity_multipliers[activity]

    tdee = bmr * activity_factor


    # -----------------------------------------------------
    # STORE BASIC CALCULATION
    # -----------------------------------------------------

    st.session_state["base_calculation"] = {

        "name": name.strip(),

        "age": int(age),

        "sex": sex,

        "weight_kg": weight_kg,

        "height_cm": height_cm,

        "target_weight": target_weight_kg,

        "activity": activity,

        "activity_description":
            activity_descriptions[activity],

        "bmi": bmi,

        "bmi_category": bmi_category,

        "bmr": bmr,

        "tdee": tdee
    }


    # Reset plan

    st.session_state["plan_selection"] = "Select a plan"


    # Reset Google Sheet tracking

    st.session_state["saved_base_id"] = None

    st.session_state["saved_row_number"] = None

    st.session_state["calculation"] = None


# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state["base_calculation"] is not None:

    data = st.session_state["base_calculation"]


    # =====================================================
    # BASIC RESULTS
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Your Results")


    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "BMI",
            f"{data['bmi']:.1f}"
        )

    with col2:

        st.metric(
            "BMI Category",
            data["bmi_category"]
        )


    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "BMR",
            f"{data['bmr']:.0f} kcal/day"
        )

    with col2:

        st.metric(
            "TDEE",
            f"{data['tdee']:.0f} kcal/day"
        )


    # =====================================================
    # ACTIVITY LEVEL + DESCRIPTION
    # =====================================================

    st.markdown("---")

    st.write(
        f"**Activity Level:** "
        f"{data['activity']} "
        f"({data['activity_description']})"
    )


    # =====================================================
    # WEIGHT LOSS PLAN
    # =====================================================

    st.markdown("---")

    st.subheader("🎯 Select Your Weight Loss Plan")


    plan_options = [

        "Select a plan",

        "Mild",

        "Moderate",

        "More aggressive"
    ]


    plan = st.selectbox(

        "Choose your desired weight-loss plan",

        plan_options,

        key="plan_selection"
    )


    # =====================================================
    # PLAN SELECTED
    # =====================================================

    if plan != "Select a plan":


        # -------------------------------------------------
        # CALORIE DEFICIT
        # -------------------------------------------------

        if plan == "Mild":

            calorie_deficit = 250

        elif plan == "Moderate":

            calorie_deficit = 500

        else:

            calorie_deficit = 750


        # -------------------------------------------------
        # DAILY CALORIE TARGET
        # -------------------------------------------------

        daily_target = data["tdee"] - calorie_deficit


        if daily_target < 1200:

            daily_target = 1200


        # -------------------------------------------------
        # WEIGHT TO LOSE
        # -------------------------------------------------

        weight_to_lose = (
            data["weight_kg"]
            - data["target_weight"]
        )


        # -------------------------------------------------
        # ESTIMATED TIMELINE
        # -------------------------------------------------

        if weight_to_lose > 0:

            total_calories = (
                weight_to_lose * 7700
            )

            estimated_days = (
                total_calories / calorie_deficit
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
        # DAILY CALORIE TARGET
        # =================================================

        st.markdown("---")

        st.subheader("🔥 Daily Calorie Target")


        st.metric(
            "Recommended daily calorie target",
            f"{daily_target:.0f} kcal/day"
        )


        # =================================================
        # WEIGHT LOSS TIMELINE
        # =================================================

        st.subheader("⏱️ Estimated Weight-Loss Timeline")


        if weight_to_lose > 0:

            st.info(
                f"Estimated weight to lose: "
                f"**{weight_to_lose:.1f} kg**"
            )

        elif weight_to_lose == 0:

            st.info(
                "Your current weight is already equal "
                "to your target weight."
            )

        else:

            st.info(
                "Your target weight is higher than your "
                "current weight."
            )


        # -------------------------------------------------
        # DAYS / WEEKS / MONTHS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)


        with col1:

            if weight_to_lose > 0:

                st.metric(
                    "Days",
                    f"{estimated_days:.0f}"
                )

            else:

                st.metric(
                    "Days",
                    "—"
                )


        with col2:

            if weight_to_lose > 0:

                st.metric(
                    "Weeks",
                    f"{estimated_weeks:.1f}"
                )

            else:

                st.metric(
                    "Weeks",
                    "—"
                )


        with col3:

            if weight_to_lose > 0:

                st.metric(
                    "Months",
                    f"{estimated_months:.1f}"
                )

            else:

                st.metric(
                    "Months",
                    "—"
                )


        # =================================================
        # IST DATE & TIME
        # =================================================

        now = datetime.now(
            ZoneInfo("Asia/Kolkata")
        )

        report_date = now.strftime(
            "%d-%m-%Y"
        )

        report_time = now.strftime(
            "%I:%M:%S %p"
        )


        # =================================================
        # COMPLETE CALCULATION
        # =================================================

        calculation = {

            "name": data["name"],

            "age": data["age"],

            "sex": data["sex"],

            "weight_kg": data["weight_kg"],

            "height_cm": data["height_cm"],

            "target_weight": data["target_weight"],

            "activity": data["activity"],

            "activity_description":
                data["activity_description"],

            "bmi": data["bmi"],

            "bmi_category":
                data["bmi_category"],

            "bmr": data["bmr"],

            "tdee": data["tdee"],

            "plan": plan,

            "daily_target":
                daily_target,

            "weight_to_lose":
                weight_to_lose,

            "estimated_days":
                round(estimated_days)
                if weight_to_lose > 0 else 0,

            "estimated_weeks":
                round(estimated_weeks, 1)
                if weight_to_lose > 0 else 0,

            "estimated_months":
                round(estimated_months, 1)
                if weight_to_lose > 0 else 0,

            "date":
                report_date,

            "time":
                report_time
        }


        st.session_state["calculation"] = calculation


        # =================================================
        # UNIQUE BASE CALCULATION ID
        # =================================================

        base_id = (

            f"{data['name'].lower()}|"

            f"{data['age']}|"

            f"{data['sex']}|"

            f"{data['weight_kg']:.4f}|"

            f"{data['height_cm']:.4f}|"

            f"{data['target_weight']:.4f}|"

            f"{data['activity']}"
        )


        # =================================================
        # FIRST AUTOMATIC SAVE
        # =================================================

        if st.session_state["saved_base_id"] != base_id:

            try:

                worksheet = get_google_sheet()


                row = [

                    data["name"],

                    report_date,

                    report_time,

                    data["age"],

                    data["sex"],

                    round(
                        data["weight_kg"], 2
                    ),

                    round(
                        data["height_cm"], 2
                    ),

                    round(
                        data["target_weight"], 2
                    ),

                    data["activity"],

                    round(
                        data["bmi"], 2
                    ),

                    round(
                        data["bmr"], 0
                    ),

                    round(
                        data["tdee"], 0
                    ),

                    plan,

                    round(
                        daily_target, 0
                    ),

                    round(
                        estimated_days, 0
                    ),

                    round(
                        estimated_weeks, 1
                    ),

                    round(
                        estimated_months, 1
                    )
                ]


                worksheet.append_row(
                    row,
                    value_input_option="USER_ENTERED"
                )


                all_rows = worksheet.get_all_values()

                row_number = len(all_rows)


                st.session_state["saved_base_id"] = base_id

                st.session_state["saved_row_number"] = row_number


            except Exception as e:

                print(
                    f"Google Sheet saving failed: {e}"
                )


        # =================================================
        # UPDATE SAME ROW WHEN PLAN CHANGES
        # =================================================

        elif (
            st.session_state["saved_row_number"]
            is not None
        ):

            try:

                worksheet = get_google_sheet()

                row_number = (
                    st.session_state[
                        "saved_row_number"
                    ]
                )


                worksheet.update(

                    range_name=(
                        f"M{row_number}:Q{row_number}"
                    ),

                    values=[[
                        plan,

                        round(
                            daily_target, 0
                        ),

                        round(
                            estimated_days, 0
                        ),

                        round(
                            estimated_weeks, 1
                        ),

                        round(
                            estimated_months, 1
                        )
                    ]],

                    value_input_option="USER_ENTERED"
                )


            except Exception as e:

                print(
                    f"Google Sheet update failed: {e}"
                )


# =========================================================
# PDF REPORT
# =========================================================

if st.session_state["calculation"] is not None:

    st.markdown("---")

    st.subheader("📄 Download Report")


    pdf_buffer = create_pdf(
        st.session_state["calculation"]
    )


    st.download_button(

        label="📥 Download PDF Report",

        data=pdf_buffer,

        file_name=(
            f"{st.session_state['calculation']['name']}"
            "_BMI_Report.pdf"
        ),

        mime="application/pdf",

        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "BMI & Weight Management Calculator"
)
