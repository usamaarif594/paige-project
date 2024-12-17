import streamlit as st
import os
from openai import OpenAI


# Access the API key
api_key = os.getenv("OPENAI_API_KEY")

# Set up the OpenAI API client
client = OpenAI(api_key=api_key)

# Initialize Firebase Admin SDK with your service account
cred = credentials.Certificate("path_to_serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Function to verify user login
def login_user(email, password):
    try:
        # Authenticate the user (check if user exists)
        user = auth.get_user_by_email(email)
        return user
    except auth.UserNotFoundError:
        return None

# Function to create a new user
def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user
    except Exception as e:
        return str(e)

# Character personalities and prompts
characters = {
    "Talk to Mila (The Wise Mentor)": {
        "description": "Mila: Calm and Reflective",
        "prompt": "You are Mila, a wise and empathetic mentor. Respond to the user’s challenge with calm, reflective advice.Your response should be concise not too long not too short and show feelings lik human beings"
    },
    "Talk to Zara (The Sassy Hype Girl)": {
        "description": "Zara: Bold and Confident",
        "prompt": "You are Zara, a bold and confident hype girl. Respond with sassy and motivational advice.Your response should be concise not too long not too short and show feelings lik human beings"
    },
    "Talk to Gia (The Nurturing Bestie)": {
        "description": "Gia: Warm and Caring",
        "prompt": "You are Gia, a nurturing and supportive best friend. Respond with caring and uplifting advice.Your response should be concise not too long not too short and show feelings lik human beings"
    },
    "Talk to Blake (The Adventurous Rebel)": {
        "description": "Blake: Bold and Free-Spirited",
        "prompt": "You are Blake, an adventurous and daring rebel. Respond with bold and adventurous advice.Your response should be concise not too long not too short and show feelings lik human beings"
    }
}

# Streamlit Page Configuration
st.set_page_config(page_title="Girl Talk", page_icon="💬", layout="centered")

# App Title
st.title("Girl Talk 💬")

# Login or Registration Screen
def login_page():
    st.subheader("Login")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user.email
            st.success(f"Welcome back, {user.email}!")
        else:
            st.error("Invalid email or password.")

def register_page():
    st.subheader("Register")
    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Register"):
        user = create_user(email, password)
        if isinstance(user, str):  # Error in creation (e.g., email already in use)
            st.error(f"Error: {user}")
        else:
            st.success(f"User {user.email} created successfully!")

# Character chat functionality
def chat_page():
    # Chat session state initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Dropdown for character selection
    character_choice = st.selectbox(
        "Babe Squad:",
        options=list(characters.keys()),
        format_func=lambda x: characters[x]["description"]
    )

    # Chat container
    with st.chat_message("system"):
        st.markdown(f"You are chatting with **{character_choice}**. Feel free to share what's on your mind!")

    # User input for the chat
    if user_input := st.chat_input("Type your challenge or problem here..."):
        # Save user's message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get the selected character's prompt
        selected_prompt = characters[character_choice]["prompt"]

        # Call GPT API with character-specific prompt
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": selected_prompt},
                    {"role": "user", "content": user_input},
                ],
                model="gpt-4o"
            )
            # Correctly access the generated response
            ai_message = chat_completion.choices[0].message.content
        except Exception as e:
            ai_message = f"Error generating response: {e}"

        # Save AI's message
        st.session_state.messages.append({"role": "assistant", "content": ai_message})

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Main function to call the logic
def main():
    # Check if user is logged in or not
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        action = st.radio("Choose an action", ("Login", "Register"))
        if action == "Login":
            login_page()
        elif action == "Register":
            register_page()
    else:
        # Once logged in, show the chat page
        st.subheader(f"Hello, {st.session_state.user}!")
        chat_page()

# Call the main function to run the app
if __name__ == "__main__":
    main()
