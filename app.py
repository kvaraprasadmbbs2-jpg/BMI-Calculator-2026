```python
import streamlit as st

st.title("🩺 BMI + BMR + TDEE Calculator")

# Name
name = st.text_input("Enter your name")

# Age
age = st.number_input(
    "Enter your age",
    min_value=1,
    max_value=120,
    value=None,
    placeholder="Enter age"
)

# Sex
sex = st.selectbox(
    "Select sex",
    ["Male", "Female"]
)

# Weight unit selection
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

# Height unit selection
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

# Activity level
activity = st.selectbox(
    "Select your activity level",
    [
        "Sedentary (Desk job, little or no exercise)",
        "Lightly active (Exercise 1–3 days/week, 5,000–7,500 steps/day)",
        "Moderately active (Exercise 3–5 days/week, 7,500–12,000 steps/day)",
        "Very active (Exercise 6–7 days/week, >12,000 steps/day)",
        "Extremely active (Athlete, heavy physical work, intense training)"
    ]
)


if st.button("Calculate"):

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

        # --------------------------------
        # Convert weight to kg
        # --------------------------------

        if weight_unit == "lb":
            weight_kg = weight * 0.453592
        else:
            weight_kg = weight


        # --------------------------------
        # Convert height to meters
        # --------------------------------

        if height_unit == "cm":
            height_m = height / 100

        elif height_unit == "inches":
            height_m = height * 0.0254

        else:
            height_m = height


        # --------------------------------
        # Calculate BMI
        # --------------------------------

        bmi = weight_kg / (height_m ** 2)


        # --------------------------------
        # Calculate BMR
        # Mifflin-St Jeor Equation
        # --------------------------------

        height_cm = height_m * 100

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


        # --------------------------------
        # Activity factors
        # --------------------------------

        activity_factors = {

            "Sedentary (Desk job, little or no exercise)": 1.2,

            "Lightly active (Exercise 1–3 days/week, 5,000–7,500 steps/day)": 1.375,

            "Moderately active (Exercise 3–5 days/week, 7,500–12,000 steps/day)": 1.55,

            "Very active (Exercise 6–7 days/week, >12,000 steps/day)": 1.725,

            "Extremely active (Athlete, heavy physical work, intense training)": 1.9
        }


        # --------------------------------
        # Calculate TDEE
        # --------------------------------

        activity_factor = activity_factors[activity]

        tdee = bmr * activity_factor


        # --------------------------------
        # Display basic information
        # --------------------------------

        st.success(f"Hello {name}!")

        st.write("### 📋 Your Information")

        st.write("Age:", age)

        st.write("Sex:", sex)

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


        # --------------------------------
        # Display BMI
        # --------------------------------

        st.write("### ⚖️ BMI")

        st.write(
            "Your BMI is:",
            round(bmi, 2)
        )


        # BMI category

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


        # --------------------------------
        # Display BMR
        # --------------------------------

        st.write("### 🔥 BMR")

        st.write(
            f"Your Basal Metabolic Rate is approximately "
            f"**{bmr:.0f} kcal/day**"
        )


        # --------------------------------
        # Display Activity Level
        # --------------------------------

        st.write("### 🏃 Activity Level")

        st.write(activity)


        # --------------------------------
        # Display TDEE
        # --------------------------------

        st.write("### 🔥 TDEE")

        st.write(
            f"Your estimated TDEE is approximately "
            f"**{tdee:.0f} kcal/day**"
        )

        st.info(
            "TDEE is the estimated number of calories "
            "you need each day to maintain your current weight."
        )
```
