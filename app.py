import streamlit as st


# ==========================================
# TITLE
# ==========================================

st.title("🩺 BMI + BMR + TDEE Calculator")

st.write(
    "Calculate your BMI, BMR, estimated TDEE, "
    "daily calorie targets and weight-loss goal."
)


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


# Show activity description

st.caption(activity_description[activity])


# ==========================================
# CALCULATE BUTTON
# ==========================================

if st.button("Calculate"):

    # ======================================
    # INPUT VALIDATION
    # ======================================

    if not name:

        st.error("Please enter your name.")

    elif age is None:

        st.error("Please enter your age.")

    elif weight is None:

        st.error("Please enter your weight.")

    elif height is None:

        st.error("Please enter your height.")

    elif target_weight is None:

        st.error("Please enter your target weight.")

    else:

        # ==================================
        # CONVERT WEIGHT TO KG
        # ==================================

        if weight_unit == "lb":

            weight_kg = weight * 0.453592

        else:

            weight_kg = weight


        # ==================================
        # CONVERT HEIGHT TO METERS
        # ==================================

        if height_unit == "cm":

            height_m = height / 100

        elif height_unit == "inches":

            height_m = height * 0.0254

        else:

            height_m = height


        # Convert height to cm

        height_cm = height_m * 100


        # ==================================
        # BMI
        # ==================================

        bmi = weight_kg / (height_m ** 2)


        # ==================================
        # BMR
        # Mifflin-St Jeor Equation
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
        # DISPLAY PERSONAL INFORMATION
        # ==================================

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


        # ==================================
        # BMI RESULT
        # ==================================

        st.write("## ⚖️ BMI")

        st.metric(
            "Your BMI",
            f"{bmi:.2f}"
        )


        # ==================================
        # BMI CATEGORY
        # ==================================

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


        # ==================================
        # BMR RESULT
        # ==================================

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


        # ==================================
        # ACTIVITY LEVEL
        # ==================================

        st.write("## 🏃 Activity Level")

        st.write(
            f"**{activity}**"
        )

        st.caption(
            activity_description[activity]
        )


        # ==================================
        # TDEE RESULT
        # ==================================

        st.write("## 🔥 TDEE")

        st.metric(
            "Estimated Daily Energy Requirement",
            f"{tdee:.0f} kcal/day"
        )

        st.info(
            "TDEE is the estimated number of calories "
            "you need each day to maintain your current weight."
        )


        # ==================================
        # CALORIE TARGETS
        # ==================================

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


        st.info(
            "These calorie targets are estimates based on "
            "your calculated TDEE. Actual energy requirements "
            "can vary between individuals."
        )


        # ==================================
        # WEIGHT LOSS / GAIN GOAL
        # ==================================

        st.write("## 🎯 Weight Goal")


        weight_difference = weight_kg - target_weight


        # ==================================
        # IF TARGET IS LOWER
        # ==================================

        if weight_difference > 0:

            st.write(
                f"**Weight to lose: "
                f"{weight_difference:.1f} kg**"
            )


            # Weight loss plan

            weight_loss_plan = st.selectbox(
                "Select your weight-loss plan",
                [
                    "Mild (10% calorie deficit)",
                    "Moderate (15% calorie deficit)",
                    "More aggressive (20% calorie deficit)"
                ]
            )


            # Deficit factors

            deficit_factors = {

                "Mild (10% calorie deficit)": 0.10,

                "Moderate (15% calorie deficit)": 0.15,

                "More aggressive (20% calorie deficit)": 0.20
            }


            deficit_percentage = (
                deficit_factors[weight_loss_plan]
            )


            # Daily calorie deficit

            daily_deficit = (
                tdee * deficit_percentage
            )


            # Daily calorie target

            weight_loss_calories = (
                tdee - daily_deficit
            )


            st.metric(
                "🔥 Daily Calorie Target",
                f"{weight_loss_calories:.0f} kcal/day"
            )


            # ==================================
            # ESTIMATED WEIGHT LOSS TIME
            # ==================================

            # Approximation:
            # 7,700 kcal ≈ 1 kg body fat

            calories_to_lose = (
                weight_difference * 7700
            )


            if daily_deficit > 0:

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


        # ==================================
        # IF TARGET IS SAME
        # ==================================

        elif weight_difference == 0:

            st.success(
                "🎯 Your target weight is the same "
                "as your current weight."
            )


        # ==================================
        # IF TARGET IS HIGHER
        # ==================================

        else:

            weight_to_gain = abs(weight_difference)


            st.write(
                f"**Weight to gain: "
                f"{weight_to_gain:.1f} kg**"
            )


            st.info(
                "Your target weight is higher than your current "
                "weight. A dedicated weight-gain calorie plan "
                "can be added separately."
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "⚠️ This calculator provides estimates for educational "
    "purposes and should not replace individualized medical advice."
)
