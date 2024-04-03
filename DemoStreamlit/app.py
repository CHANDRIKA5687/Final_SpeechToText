import streamlit as st
def main():
    st.title("Sample Streamlit Application")
    
    # Add a sidebar
    st.sidebar.header("User Input")
    
    # Add widgets for user input
    name = st.sidebar.text_input("Enter Your Name", "John Doe")
    age = st.sidebar.slider("Enter Your Age", 0, 100, 25)
    
    # Display the user input
    st.write(f"Name: {name}")
    st.write(f"Age: {age}")
    
if __name__ == "__main__":
    main()
#  C:\Users\Chandrika\AppData\Roaming\Python\Python312\site-packages
# Python 3.12.
# C:\Program Files\Python312\Scripts