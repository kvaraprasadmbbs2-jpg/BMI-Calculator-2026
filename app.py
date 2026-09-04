import streamlit as st

st.title("🩺 BMI Calculator")

name = st.text_input("Enter your name")

age = st.number_input(
    "Enter your age",
    min_value=1,
    max_value=120,
    value=None,
    placeholder="Enter age"
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

        # Convert weight to kg

        if weight_unit == "lb":
            weight_kg = weight * 0.453592
        else:
            weight_kg = weight


        # Convert height to meters

        if height_unit == "cm":
            height_m = height / 100

        elif height_unit == "inches":
            height_m = height * 0.0254

        else:
            height_m = height


        # Calculate BMI

        bmi = weight_kg / (height_m * height_m)


        # Display results

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
