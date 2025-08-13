# 📚 LearningCoach AI – Your Personalized Study Assistant  

**Author:** Arpitha Mulge

LearningCoach AI is an **AI-powered tutoring application** that helps students understand concepts, answer academic queries, and receive personalized study plans.  
It uses **OpenAI GPT models** and a **Streamlit UI** to create an interactive, adaptive learning experience.  

---

## 🚀 Features  

- **AI-Powered Tutoring** – Delivers clear, step-by-step answers and explanations for academic questions  
- **Interactive Chat Interface** – Real-time Q&A with an intuitive Streamlit-powered UI  
- **Personalized Learning** – Adapts responses based on each learner's profile and progress  
- **Smart Memory Management** – Remembers past conversations for more relevant answers  
- **Secure API Key Handling** – Uses `.env` file and `python-dotenv` to keep credentials safe  
- **Modular Code Structure** – Organized into separate files for tools, memory, and UI  

---

## 🛠️ Tech Stack  

- **Python**  
- **Streamlit**  
- **OpenAI API**  
- **python-dotenv** (for environment variables)  

---

## 🔑 Setup & Usage  

###  1️⃣ Clone the Repository
```bash  
git clone https://github.com/yourusername/learning-coach.git  
cd learning-coach  

### 2️⃣ Create & Activate Virtual Environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
### 3️⃣ Install Dependencies
pip install -r requirements.txt
### 4️⃣ Set Up .env File
Create a .env file in the project root and add your OpenAI API key:
env
OPENAI_API_KEY=your_api_key_here
### 5️⃣ Run the Application
streamlit run app.py
Your browser will open the LearningCoach AI interface

📄 Usage Instructions
Select preferred subjects and learning level in the sidebar.
Chat with the AI for questions and explanations.
Use Quick Tools for:
📝 Generating a study plan
🎯 Taking a quiz
📈 Viewing progress reports
🧠 Getting study techniques
The system remembers previous interactions for better guidance.

💡 Key Features Implemented
AI-powered tutoring and explanations
Interactive chat interface with Streamlit
User profile-based personalization
Memory management for conversation context
Secure API key handling via .env
Modular code structure

📚 Key Learnings & Challenges
Handling dynamic memory for past interactions
Integrating OpenAI API with real-time Streamlit chat
Personalizing responses based on user profile and learning level
Structuring code to be modular and maintainable
Learned best practices for state management and API key security


