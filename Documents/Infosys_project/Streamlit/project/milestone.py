import streamlit as st
import openai
import pandas as pd
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set up the OpenAI API key
openai.api_key = "" 

# Load data from the uploaded Excel file
uploaded_file = "C:/Users/PIYUSHA-LAP/Documents/Infosys_project/Streamlit/project/merged_cleaned_data_2019_2023.xlsx"
data = pd.read_excel(uploaded_file)

# css for login page
def apply_login_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FEF3E2;
        
        /* Style the login heading */
        .login-heading {
            font-size: 24px;
            font-weight: bold;
            color: #4CAF50; /* Green color */
            margin-bottom: 20px;
            text-align: center;
        }

        /* Style the input fields */
        input {
            background-color: #C2FFC7 !important; /* Light blue */
            border: 1px solid #cccccc;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            width: 100% !important;
        }

        /* Style the login button */
        .stButton>button {
            background-color: #FA4032; /* Green button */
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049; /* Darker green on hover */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Custom CSS for styling
def apply_custom_css():
    st.markdown(
        """
        <style>
        /* Sidebar background styling */
        [data-testid="stSidebar"] {
            background-color: #FFF7D1; 
            color: white; /* Text color */
            padding: 15px;
            border-radius: 10px;
        }

        /* Sidebar widget styles */
        [data-testid="stSidebar"] .stButton>button {
            background-color: #4CAF50; /* Green button */
            color: white;
            border-radius: 5px;
            border: none;
            padding: 8px 16px;
        }
        [data-testid="stSidebar"] .stButton>button:hover {
            background-color: #45a049; /* Lighter green on hover */
        }

        /* Sidebar header styling */
        [data-testid="stSidebar"] h1, h2, h3 {
            color: #FF8000; /* Yellow headings */
        }
        /* Set background color for the entire page */
        .stApp {
            background-color: #B1D690;
        }
        /* Set background for the main content container */
        .main-container {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        
        /* Style headings */
        .main-heading {
            background-color: #2196F3;
            color: white;
            padding: 10px;
            border-radius: 10px;
            text-align: left;
            font-size: 30px;
            font-weight: bold;
        }

        .sub-heading {
            background-color: #FFC107;
            color: black;
            padding: 6px; /* Keeps the height unchanged */
            border-radius: 10px; 
            margin-top: 5px;
            font-size: 20px;
            font-weight: bold;
            width: fit-content; /* Adjusts the background length to fit the content */
            display: inline-block; /* Ensures the width only wraps around the text */
        }


        /* Style buttons */
        .stButton>button {
            background-color: #FF4545;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            margin: 5px;
            border-radius: 5px;
            transition-duration: 0.4s;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }

        .chatbot-input {
            background-color: #f9f9d8; /* Light yellow background for input box */
            border: 1px solid #cccccc;
            border-radius: 5px;
            padding: 10px;
            font-size: 16px;
            width: 100%;
            margin-top: 10px;
            box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.05); /* Adds depth to input */
        }
        .chatbot-response {
            background-color: #FAB12F; /* Lighter blue for bot responses */
            padding: 15px;
            border-radius: 5px;
            font-size: 16px;
            color: #333;
            margin-top: 10px;
            border-left: 5px solid #4CAF50; /* Adds a green accent for the bot */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# User credentials
users = {
    "Piyusha": "piyu@123",
    "Nalini": "nalini.123"
}


# Login Function
def login():
    st.title("🔒 Login Page")
    apply_login_css()

    # Credential Input Fields
    username = st.text_input("👤 Username", key="username_input", placeholder="Enter your username")
    password = st.text_input("🔑 Password", type="password", key="password_input", placeholder="Enter your password")

    # Login Button
    if st.button("🚪 Login"):
        # Login Validation (Replace this with your logic)
        if username in users and users[username] == password:
            st.session_state["authenticated"] = True
            st.success("✅ Login Successful")
        else:
            st.error("❌ Invalid Username or Password")


# Chatbot functionality
def get_user_input():
    return st.text_input("You:", key="input", placeholder="Type your question here...")

def filter_data(question):
    keywords = question.split()
    filtered_data = data[data.apply(lambda row: row.astype(str).str.contains('|'.join(keywords), case=False).any(), axis=1)]
    return filtered_data.head(50)

def query_data(question):
    data_sample = filter_data(question)
    if data_sample.empty:
        return "I'm sorry, but the information you're looking for is not available in the dataset."
    data_sample_str = data_sample.to_string(index=False)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that only answers questions based on the provided dataset. If the information is not in the data, state that it is unavailable."},
            {"role": "system", "content": f"Here is the relevant data:\n{data_sample_str}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message["content"].strip()

def chatbot_section():
    st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="sub-heading">🤖 Chatbot Assistance</h3>', unsafe_allow_html=True)
    user_question = get_user_input()
    if user_question:
        answer = query_data(user_question)
        st.write("Bot:", answer)
        

# Function to render the Home page
def render_home_page():
    st.markdown('<h1 class="main-heading">🏠 Home Page</h1>', unsafe_allow_html=True)
    st.write("Welcome to the Home page! Here you can find general information and updates.")
    
    st.markdown('<h3 class="sub-heading">📖 Introduction</h3>', unsafe_allow_html=True)
    st.write("The Power BI dashboard provides an in-depth analysis of economic and innovation indicators across various cities from 2019 to 2023.")
    
    st.markdown('<h3 class="sub-heading">📅 Recent Activities</h3>', unsafe_allow_html=True)
    st.write("- 🌍 In 2023, the total GDP across the observed cities reached $3067 billion.")
    st.write("- 📈 Innovation has shown positive growth, with 59.9 patents per 100,000 inhabitants recorded in 2023.")
    
    st.markdown('<h3 class="sub-heading">📊 Key Metrics</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Total GDP", "$3067 billion", "+21.77%")
    with col2:
        st.metric("📉 Avg Unemployment Rate", "5.67%", "-15.17%")
    with col3:
        st.metric("💻 Avg Tech Sector Contribution", "21.36%")

    chatbot_section()
    

# Function to render the Reports page
def render_reports_page():
    st.markdown('<h1 class="main-heading">📊 Dashboard</h1>', unsafe_allow_html=True)
    st.write("This is embeded Power BI dashboard")
    st.markdown(
        f'<iframe title="project" width="900" height="600" src="https://app.powerbi.com/view?r=eyJrIjoiYjBkZWRkZTItOTE1ZS00MzFhLTk1NWMtZWQ4MjA1ODQxMDQzIiwidCI6ImY1YjNkYTY2LTA1YzAtNGFiZC1iNjA5LTk5MDYwNDZmZmY1ZiJ9" frameborder="0" allowFullScreen="true"></iframe>',
        unsafe_allow_html=True
    )
    # Summary Section
    st.markdown('<h3 class="sub-heading">📄 Summary</h3>', unsafe_allow_html=True)
    st.write("The analysis of data from 2019 to 2023 provides key insights into the economic, employment, and innovation trends across multiple cities. Here is a summary of the findings:")
    st.write("1. 🌍 **Economic Growth**: The combined GDP of the cities has grown significantly, reaching $3067 billion in 2023, which is a 21.77% increase since 2019. This growth highlights the economic resilience and expansion within these regions.")
    st.write("2. 📉 **Employment Improvement**: The unemployment rate has improved over the years, with an average of 5.67% in 2023, marking a 15.17% decrease from 2019. This trend reflects positive changes in job availability and economic stability.")
    st.write("3. 💡 **Innovation and Technology**: The innovation sector is on the rise, with 59.9 patents per 100,000 inhabitants reported in 2023, showcasing a strong emphasis on R&D and technological advancements. Additionally, the technology sector's contribution to the economy is substantial, averaging 21.36% in 2023, indicating a growing focus on tech-driven economic activities.")    
    st.write("4. 📊 **Sectoral Focus**: The dashboards reveal varying sectoral dominance across cities, with notable contributions from services, industry, and technology sectors. Technology, in particular, has seen a steady increase, underscoring its critical role in economic development.")
    st.write("Overall, these insights indicate robust economic growth, reduced unemployment, and an increasing reliance on innovation and technology. The upward trends in key metrics like GDP and patents per capita point to a positive economic outlook and a promising future for technology-driven growth in these cities.")
    chatbot_section()
    


# Function to render the Interactive Data Storytelling page
def render_interactive_storytelling_page():
    st.markdown('<h1 class="main-heading">📖 Interactive Data Storytelling</h1>', unsafe_allow_html=True)
    st.write("This page gives you details about the entire dashboard!")
    
    # Story Section
    st.markdown('<h3 class="sub-heading">🌍 How Innovation Grew in Major Cities</h3>', unsafe_allow_html=True)
    st.write("From 2019 to 2023, we observed a steady increase in patents and R&D spending across major cities. Innovation became a central theme as cities invested more in technology and research.")
    
    st.markdown('<h3 class="sub-heading"> Timeline of Key Innovations</h3>', unsafe_allow_html=True)
    st.write("Explore the major milestones in innovation across these cities:")
    st.write("2019: Initial investments in R&D were modest, focusing on foundational technologies.")
    st.write("2020: Cities increased funding to support remote work technologies.")
    st.write("2021-2022: Breakthroughs in AI and biotech sparked further investments.")
    st.write("2023: Major cities recorded the highest number of patents per capita.")
    
    # Interactive Metric Exploration
    st.markdown('<h3 class="sub-heading">📊 Explore Specific Metrics</h3>', unsafe_allow_html=True)
    metric = st.selectbox("Choose a metric to explore:", ["GDP Growth", "Unemployment Rate", "Patents per 100,000 Inhabitants"])
    if metric == "GDP Growth":
        st.write("Explore how GDP growth has evolved year by year.")
        st.line_chart([3067, 3200, 3400, 3600, 3800])
    elif metric == "Unemployment Rate":
        st.write("Unemployment rate trends over the years.")
        st.line_chart([5.67, 5.3, 5.1, 4.9, 4.7])
    elif metric == "Patents per 100,000 Inhabitants":
        st.write("Explore innovation growth through patents.")
        st.line_chart([59.9, 62.1, 65.3, 67.5, 70.0])
    
    # Audio/Video Explanation
    st.markdown('<h3 class="sub-heading">🎧 Audio Explanation</h3>', unsafe_allow_html=True)
    st.write("")
    st.audio("C:/Users/PIYUSHA-LAP/Documents/Infosys_project/Streamlit/project/data insights.mp3", format="audio/mp3")
    st.write("Listen to an audio summary of key economic trends from 2019 to 2023.")
    chatbot_section()
    

# Define your SMTP server configuration
SMTP_SERVER = "smtp.office365.com"  # Replace with your SMTP server, e.g., "smtp.gmail.com"
SMTP_PORT = 587  # SSL port for secure connection
SMTP_USER = "support@aptpath.in"  # Replace with your email
SMTP_PASSWORD = "kjydtmsbmbqtnydk"  # Replace with your email password

# Explicit sender and receiver emails
SENDER_EMAIL = "support@aptpath.in"  # Sender's email address
RECEIVER_EMAIL = "piyu.piyusha1111@gmail.com"  # Owner's email where feedback is sent

# Feedback form function
def render_feedback_form():
    st.title("📝 Feedback Page")
    st.write("We appreciate your feedback! Please fill out the form below to help us improve.")
    
    # Collect feedback details
    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    feedback_subject = st.text_input("Subject")
    feedback_message = st.text_area("Message")
    
    # When user submits feedback
    if st.button("Submit Feedback"):
        if user_name and user_email and feedback_message:
            send_feedback_email(user_name, user_email, feedback_subject, feedback_message)
            st.success("Thank you! Your feedback has been submitted successfully.")
        else:
            st.error("Please fill out all fields.")

def send_feedback_email(user_name, user_email, subject, message):
    # Prepare email content
    email_message = MIMEMultipart()
    email_message["From"] = SENDER_EMAIL
    email_message["To"] = RECEIVER_EMAIL
    email_message["Subject"] = f"Feedback from {user_name}: {subject}"

    # Body of the email
    body = f"Name: {user_name}\nEmail: {user_email}\n\nMessage:\n{message}"
    email_message.attach(MIMEText(body, "plain"))

    try:
        # Create SMTP session and upgrade to TLS
        with smtplib.SMTP(SMTP_SERVER, 587) as server:  # Use port 587 for TLS
            server.starttls(context=ssl.create_default_context())  # Secure the connection
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_message.as_string())
            st.info("Feedback email sent successfully.")
    except Exception as e:
        st.error(f"Failed to send feedback email. Error: {e}")


# Check if user is authenticated
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
else:
    apply_custom_css()  # Apply custom CSS for styling

    # Sidebar navigation with logout button
st.sidebar.title("📂 Navigation")
selected_page = st.sidebar.selectbox("Choose a page", ["🏠 Home", "📊 Reports", "📖 Interactive Data Storytelling", "📝 Feedback Form"])


if selected_page == "🏠 Home":
    render_home_page()
    
elif selected_page == "📊 Reports":
    render_reports_page()
    
elif selected_page == "📖 Interactive Data Storytelling":
    render_interactive_storytelling_page()
    
elif selected_page == "📝Feedback Form":
    render_feedback_form() 