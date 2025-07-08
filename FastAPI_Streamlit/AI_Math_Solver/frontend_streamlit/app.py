import streamlit as st
import requests

st.set_page_config(page_title="AI Math Solver & Explainer")

st.title("AI Math Solver & Explainer")
st.write("Enter a math problem (eg. 'Solve 2x + 3 = 7')")

question = st.text_input("Your Question", placeholder = "e.g., Solve 2x + 3 = 7")

if st.button("Solve"):
    if not question.strip():
        st.warning("Please enter a math problem")
    else:
        with st.spinner("Solving....."):
            try:
                response = requests.post(
                    "http://localhost:8080/solve",
                    json=("question": question)
                )

                if response.status_code == 200:
                    solution = response.json()["solution"]
                    st.markdown("### Solution & Explaination:")
                    for line in solution.split("\n"):
                        line = line.strip()
                        if line.startwith("$$") and line.endswith("$$"):
                            st.latex(line.strip("$$"))
                        elif line.startwith("\\[") and line.endswith("\\]"):
                            st.latex(line[2:-2])
                        else:
                            st.markdown(line)
                else:
                    st.error("Failed to get response from backend.")
            except Exception as e:
                st.error(f"Error: {e}")


                        