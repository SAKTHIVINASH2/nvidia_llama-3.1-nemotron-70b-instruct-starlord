import streamlit as st
import openai

# Set up the Streamlit page configuration
st.set_page_config(page_title="NVIDIA OpenAI ChatGPT", layout="centered")

# Sidebar for API key input
with st.sidebar:
    st.header("API Key Configuration")
    api_key = st.text_input("Enter your NVIDIA API Key:")

st.sidebar.markdown(
    """
    <div style="padding: 20px; background-color: #292b2c; border-radius: 10px; color: #f0f0f0;">
        <h3 style="text-align: center;">Steps to Get an API Key from NVIDIA</h3>
        <ul style="font-size: 14px; color: #dcdcdc;">
            <li><strong>1. Create an NVIDIA Developer Account:</strong> Go to <a href="https://developer.nvidia.com/" target="_blank" style="color: #4caf50;">NVIDIA Developer's website</a>. Sign up or log in.</li>
            <li><strong>2. Access NVIDIA's Cloud AI Services:</strong> Once logged in, navigate to the <a href="https://www.nvidia.com/en-us/cloud/" target="_blank" style="color: #4caf50;">NVIDIA Cloud page</a>.</li>
            <li><strong>3. Find the API Access Section:</strong> Look for the API section for models like LLaMA or similar in the "Generative AI" or "NLP" tools category.</li>
            <li><strong>4. Request Access (if needed):</strong> Some APIs may require joining a waitlist or submitting a request form to get access.</li>
            <li><strong>5. Get the API Key:</strong> Once granted access, you'll receive an API key for authentication in your requests.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant."}]

# Main Title
st.title("NVIDIA OpenAI ChatGPT Interface")

if not api_key:
    st.warning("Please enter your API key in the sidebar to start.")
else:
    try:
        # Configure the OpenAI client
        openai.api_base = "https://integrate.api.nvidia.com/v1"
        openai.api_key = api_key

        # Create containers for chat history and input field
        chat_container = st.container()
        input_container = st.empty()  # Ensures the input stays fixed at the bottom

        # Display the conversation
        with chat_container:
            # Display the conversation
            for message in st.session_state["messages"]:
                if message["role"] == "user":
                    st.markdown(f"**🧑 You:** {message['content']}")
                elif message["role"] == "assistant":
                    st.markdown(f"**🤖 Bot:** {message['content']}")

        with input_container:
            # Input form for user messages
            with st.form("chat_form", clear_on_submit=True):
                user_input = st.text_input("Your message:", placeholder="Type your message here...")
                submitted = st.form_submit_button("Send")

        if submitted and user_input:
            # Add the user's message to the chat history
            st.session_state["messages"].append({"role": "user", "content": user_input})

            # Display the user's message immediately
            st.markdown(f"**🧑 You:** {user_input}")

            # Fetch the assistant's response
            with st.spinner("🤖 Bot is typing..."):
                try:
                    # Call the API
                    response = openai.ChatCompletion.create(
                        model="nvidia/llama-3.1-nemotron-70b-instruct",
                        messages=st.session_state["messages"],
                        temperature=0.5,
                        top_p=0.7,
                        max_tokens=1024,
                        stream=True
                    )

                    # Stream response in real-time
                    response_container = st.empty()
                    full_response = ""
                    for chunk in response:
                        if chunk.choices[0].delta.content is not None:
                            delta_content = chunk.choices[0].delta.content
                            full_response += delta_content
                            response_container.markdown(f"**🤖 Bot:** {full_response}")

                    # Add the assistant's response to chat history
                    st.session_state["messages"].append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"An error occurred while fetching the response: {e}")

    except Exception as e:
        st.error(f"Failed to configure OpenAI API: {e}")
