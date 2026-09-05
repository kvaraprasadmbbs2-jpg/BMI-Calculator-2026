import streamlit as st
import gspread
from datetime import datetime
from zoneinfo import ZoneInfo


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🩺 BMI Calculator")


# --------------------------------------------------
# USER INPUTS
# --------------------------------------------------

name = st.text_input("Enter your name")

age = st.number_input(
    "Enter your age",
    min_value=1,
    max_value=120,
    value=None,
    placeholder="Enter age"
)


# --------------------------------------------------
# WEIGHT
# --------------------------------------------------

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


# --------------------------------------------------
# HEIGHT
# --------------------------------------------------

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


# --------------------------------------------------
# CALCULATE BMI
# --------------------------------------------------

if st.button("Calculate BMI"):

    # Check whether all information is entered

    if not name:
        st.error("Please enter your name.")

    elif age is None:
        st.error("Please enter your age.")

    elif weight is None:
        st.error("Please enter your weight.")

    elif height is None:
        st.error("Please enter your height.")

    else:

        # --------------------------------------------------
        # CONVERT WEIGHT TO KG
        # --------------------------------------------------

        if weight_unit == "lb":
            weight_kg = weight * 0.453592
        else:
            weight_kg = weight


        # --------------------------------------------------
        # CONVERT HEIGHT TO METERS
        # --------------------------------------------------

        if height_unit == "cm":
            height_m = height / 100

        elif height_unit == "inches":
            height_m = height * 0.0254

        else:
            height_m = height


        # --------------------------------------------------
        # CALCULATE BMI
        # --------------------------------------------------

        bmi = weight_kg / (height_m * height_m)


        # --------------------------------------------------
        # DISPLAY RESULTS
        # --------------------------------------------------

        st.success(f"Hello {name}!")

        st.write("Age:", age)

        st.write(
            "Weight:",
            round(weight_kg, 2),
            "kg"
        )

        st.write(
            "Height:",
            round(height_m, 2),
            "m"
        )

        st.write(
            "Your BMI is:",
            round(bmi, 2)
        )


        # --------------------------------------------------
        # BMI CATEGORY
        # --------------------------------------------------

        if bmi < 18.5:

            st.warning("BMI Category: Underweight")

            st.write(
                "Consider maintaining adequate calorie "
                "and nutrient intake."
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

            st.error("BMI Category: Obese")

            st.write(
                "Consider discussing weight management "
                "with a healthcare professional."
            )


        # --------------------------------------------------
        # SAVE TO GOOGLE SHEETS
        # --------------------------------------------------

        try:

            # Connect to Google using Streamlit secrets
            credentials = st.secrets["gcp_service_account"]

            gc = gspread.service_account_from_dict(credentials)

            # Open your Google Sheet
            spreadsheet = gc.open("BMI Calculator Visitor Log")

            # Open the first worksheet
            worksheet = spreadsheet.sheet1

            # Current date and time in India
            now = datetime.now(ZoneInfo("Asia/Kolkata"))

            date = now.strftime("%d-%m-%Y")
            time = now.strftime("%I:%M:%S %p")

            # Add the patient's information to Google Sheet
            worksheet.append_row(
                [
                    name,
                    date,
                    time,
                    round(bmi, 2)
                ]
            )

            st.success("✅ Details saved successfully to Google Sheets.")

        except Exception as e:

            st.error(
                "BMI calculated successfully, but the details "
                "could not be saved to Google Sheets."
            )

            st.write("Error:", e)
