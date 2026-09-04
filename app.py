import streamlit as st

# --------------------------------
# Title
# --------------------------------

st.title("🩺 BMI + BMR + TDEE Calculator")


# --------------------------------
# Personal Information
# --------------------------------

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


# --------------------------------
# Weight
# --------------------------------

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


# --------------------------------
# Height
# --------------------------------

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


# --------------------------------
# Activity Level
# --------------------------------

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


# Activity descriptions

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


# Activity factors

activity_factors = {

    "Sedentary": 1.2,

    "Lightly active": 1.375,

    "Moderately active": 1.55,

    "Very active": 1.725,

    "Extremely active": 1.9
}


# Show description

st.caption(activity_description[activity])


# --------------------------------
# Calculate Button
# --------------------------------

if st.button("Calculate"):

    # --------------------------------
    # Check Input
    # --------------------------------

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
        # Convert Weight to kg
        # --------------------------------

        if weight_unit == "lb":

            weight_kg = weight * 0.453592

        else:

            weight_kg = weight


        # --------------------------------
        # Convert Height to meters
        # --------------------------------

        if height_unit == "cm":

            height_m = height / 100

        elif height_unit == "inches":

            height_m = height * 0.0254

        else:

            height_m = height


        # --------------------------------
        # Convert Height to cm
        # --------------------------------

        height_cm = height_m * 100


        # --------------------------------
        # BMI Calculation
        # --------------------------------

        bmi = weight_kg / (height_m ** 2)


        # --------------------------------
        # BMR Calculation
        # Mifflin-St Jeor Equation
        # --------------------------------

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
        # TDEE Calculation
        # --------------------------------

        activity_factor = activity_factors[activity]

        tdee = bmr * activity_factor


        # --------------------------------
        # Display Personal Information
        # --------------------------------

        st.success(f"Hello {name}! 👋")

        st.write("## 📋 Your Information")

        st.write("**Age:**", age)

        st.write("**Sex:**", sex)

        st.write(
            "**Weight:**",
            round(weight_kg, 2),
            "kg"
        )

        st.write(
            "**Height:**",
            round(height_m, 2),
            "m"
        )


        # --------------------------------
        # BMI Result
        # --------------------------------

        st.write("## ⚖️ BMI")

        st.write(
            f"**Your BMI is {bmi:.2f}**"
        )


        # --------------------------------
        # BMI Category
        # --------------------------------

        if bmi < 18.5:

            st.warning(
                "BMI Category: Underweight"
            )

            st.write(
                "Consider maintaining adequate "
                "calorie and nutrient intake."
            )

        elif bmi < 25:

            st.success(
                "BMI Category: Normal"
            )

            st.write(
                "Your BMI is within the normal range. "
                "Regular exercise and a balanced diet "
                "will help maintain your health."
            )

        elif bmi < 30:

            st.warning(
                "BMI Category: Overweight"
            )

            st.write(
                "Regular exercise and a balanced diet "
                "may be helpful."
            )

        else:

            st.error(
                "BMI Category: Obesity"
            )

            st.write(
                "Consider discussing weight management "
                "with a healthcare professional."
            )


        # --------------------------------
        # BMR Result
        # --------------------------------

        st.write("## 🔥 BMR")

        st.write(
            f"**{bmr:.0f} kcal/day**"
        )

        st.caption(
            "BMR is the estimated energy your body "
            "needs at complete rest to maintain basic "
            "physiological functions."
        )


        # --------------------------------
        # Activity Result
        # --------------------------------

        st.write("## 🏃 Activity Level")

        st.write(
            f"**{activity}**"
        )

        st.caption(
            activity_description[activity]
        )


        # --------------------------------
        # TDEE Result
        # --------------------------------

        st.write("## 🔥 TDEE")

        st.write(
            f"**{tdee:.0f} kcal/day**"
        )

        st.info(
            "TDEE is the estimated number of calories "
            "you need each day to maintain your current weight."
        )
        # --------------------------------
        # Calorie Targets
        # --------------------------------
        
        st.write("## 🎯 Daily Calorie Targets")
        
        maintenance = tdee
        mild_weight_loss = tdee * 0.90
        moderate_weight_loss = tdee * 0.85
        aggressive_weight_loss = tdee * 0.80
        weight_gain = tdee * 1.10
        
        
        # Create columns
        
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
        
        
        st.info(
            "These calorie targets are estimates based on your calculated TDEE. "
            "Actual energy requirements can vary between individuals."
        )
