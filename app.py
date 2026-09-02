import streamlit as st

st.title("🩺 BMI Calculator")

name = st.text_input("Enter your name")

age = st.number_input(
    "Enter your age",
    min_value=1,
    max_value=120,
    value=45
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
    value=69.0
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
    value=167.0
)

if st.button("Calculate BMI"):

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

    st.success(f"Hello {name}!")

    st.write("Age:", age)
    st.write("Weight:", round(weight_kg, 2), "kg")
    st.write("Height:", round(height_m, 2), "m")
    st.write("Your BMI is:", round(bmi, 2))
    if bmi < 18.5:
        st.warning("BMI Category: Underweight")
        st.write("Consider maintaining adequate calorie and nutrient intake.")

    elif bmi < 25:
        st.success("BMI Category: Normal")
        st.write("Your BMI is within the normal range.")

    elif bmi < 30:
        st.warning("BMI Category: Overweight")
        st.write("Regular exercise and a balanced diet may be helpful.")

    else:
        st.error("BMI Category: Obese")
        st.write("Consider discussing weight management with a healthcare professional.")
