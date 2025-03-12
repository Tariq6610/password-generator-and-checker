import streamlit as st
import random
import string as str
import re
import pandas as pd

option = st.sidebar.radio("",("Check Password", "Generate Password", "History"))
if option == "Generate Password":
    def generate_password(length, use_digits, use_special):
        char = str.ascii_letters

        if use_digits:
            char += str.digits

        if use_special:
            char += str.punctuation
            
        return "".join(random.choice(char) for _ in range(length))

    st.title("Password Generator")

    length = st.slider("Select Password Length",min_value=6, max_value=32, value=12)

    use_digits = st.checkbox("include digits")

    use_special = st.checkbox("include special characters")

    # Use session state to store the password
    if 'password' not in st.session_state:
        st.session_state.password = ""

    if st.button("Generate Password"):
        st.session_state.password = generate_password(length, use_digits, use_special)


    if st.session_state.password:   
            st.write(f"Password generated : ")
            st.code(st.session_state.password)
    st.write("_________________________________________________")
    st.write("")
    st.write("💡Tips")
    st.markdown(
        """
        Password should :
        - ✅ Be at least 8 characters long
        - ✅ Include both uppercase and lowercase letters.
        - ✅ Include at least one digit (0-9)
        - ✅ Have one special character (!@#$%^&*)
        """
    )

# Check password
def check_password_strength(password):
    score = 0
    remarks = []
    data = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
        data.append("✅ Password should be at least 8 characters long.")
    else:
        remarks.append("❌ Password should be at least 8 characters long.")
        data.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
        data.append("✅ Include both uppercase and lowercase letters.")
    else:
        remarks.append("❌ Include both uppercase and lowercase letters.")
        data.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
        data.append("✅ Add at least one number (0-9).")
    else:
        remarks.append("❌ Add at least one number (0-9).")
        data.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
        data.append("✅ Include at least one special character (!@#$%^&*).")
    else:
        remarks.append("❌ Include at least one special character (!@#$%^&*).")
        data.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if score == 4:
        remarks.append("✅ Strong Password!")
    elif score == 3:
        remarks.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        remarks.append("❌ Weak Password - Improve it using the suggestions below.")

    return (score, remarks, data)

if "history" not in st.session_state:
    st.session_state.history = []

if option == "Check Password":
    st.title("Password Strength Meter")
    password = st.text_input("write Password", type="password")
    score, remarks, data = check_password_strength(password)
    df = pd.DataFrame({"Checks" : data})
    if st.button("Check strength"):
        if password:
            st.session_state.history.append(password)
            st.write(f"Strength Score: `{score}`")
            st.write("Remarks :")
            for i in remarks:
                st.markdown(f"- {i}")
            st.write(df)
        else:
            st.error("Password length should not be zero")


# History
if option == "History":
    history_df = pd.DataFrame({"Recent": st.session_state.history})
    st.write(history_df)
           
            
         
     
    