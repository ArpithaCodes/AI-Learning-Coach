import streamlit as st
from openai import OpenAI
from learning_tools import LearningTools
from memory_manager import MemoryManager
import json

# ✅ Securely load API key from secrets.toml
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "learning_profile" not in st.session_state:
    st.session_state.learning_profile = {
        "preferred_subjects": [],
        "learning_level": "intermediate",
        "study_goals": [],
        "progress_tracking": {}
    }
if "memory_manager" not in st.session_state:
    st.session_state.memory_manager = MemoryManager()
if "learning_tools" not in st.session_state:
    st.session_state.learning_tools = LearningTools(openai_client)

def main():
    st.set_page_config(
        page_title="AI Learning Coach",
        page_icon="🎓",
        layout="wide"
    )
    
    st.title("🎓 AI Learning Coach")
    st.markdown("Your personalized AI tutor for all academic subjects")
    
    # Sidebar for learning profile and tools
    with st.sidebar:
        st.header("📊 Learning Profile")
        
        # Subject preferences
        st.subheader("Preferred Subjects")
        subject_categories = [
            "Mathematics", "Physics", "Chemistry", "Biology", "Computer Science",
            "English Literature", "Foreign Languages", "Creative Writing",
            "History", "Geography", "Economics", "Political Science",
            "Music Theory", "Art History", "Visual Arts",
            "SAT Prep", "ACT Prep", "AP Exams", "General Test Prep"
        ]
        
        selected_subjects = st.multiselect(
            "Select your subjects of interest:",
            subject_categories,
            default=st.session_state.learning_profile["preferred_subjects"]
        )
        st.session_state.learning_profile["preferred_subjects"] = selected_subjects
        
        # Learning level
        learning_level = st.selectbox(
            "Learning Level:",
            ["beginner", "intermediate", "advanced"],
            index=["beginner", "intermediate", "advanced"].index(
                st.session_state.learning_profile["learning_level"]
            )
        )
        st.session_state.learning_profile["learning_level"] = learning_level
        
        # Quick tools
        st.subheader("🛠️ Quick Tools")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Study Plan"):
                create_study_plan()
        with col2:
            if st.button("🎯 Quiz Me"):
                generate_quiz()
        
        if st.button("📈 Progress Report"):
            show_progress_report()
        
        if st.button("🧠 Study Tips"):
            get_study_techniques()
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    st.subheader("💬 Chat with your AI Learning Coach")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your studies..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process and add assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = process_learning_query(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Update memory
        st.session_state.memory_manager.add_interaction(prompt, response)

def process_learning_query(query):
    """Process user query and generate appropriate learning response."""
    try:
        # Get learning context
        learning_context = st.session_state.memory_manager.get_learning_context()
        profile = st.session_state.learning_profile
        
        # Determine if this requires a specialized tool
        tool_response = st.session_state.learning_tools.analyze_and_respond(
            query, profile, learning_context
        )
        
        if tool_response:
            return tool_response
        
        # General learning conversation
        system_prompt = f"""
        You are an expert AI Learning Coach providing personalized educational guidance across all academic subjects.
        
        Student Profile:
        - Preferred subjects: {', '.join(profile['preferred_subjects']) if profile['preferred_subjects'] else 'Not specified'}
        - Learning level: {profile['learning_level']}
        - Study goals: {', '.join(profile['study_goals']) if profile['study_goals'] else 'Not specified'}
        
        Learning Context from Previous Interactions:
        {learning_context}
        
        Guidelines:
        1. Provide clear, educational explanations appropriate for the student's level
        2. Use examples and analogies to make complex concepts understandable
        3. Encourage active learning and critical thinking
        4. Offer study strategies and techniques when relevant
        5. Be supportive and motivating
        6. If the question is about a specific subject, provide comprehensive coverage
        7. For test prep questions, include practice strategies and tips
        8. Always maintain an encouraging, educational tone
        
        Respond to the student's question with personalized guidance.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg:
            return """
🚨 **OpenAI API Quota Exceeded**

Your OpenAI API key has exceeded its usage quota. To continue using the AI Learning Coach:

1. **Check your OpenAI account**: Visit https://platform.openai.com/usage
2. **Add billing**: Go to https://platform.openai.com/settings/billing
3. **Add credits**: Purchase credits or upgrade your plan
4. **Free tier**: If using free tier, you may need to wait or upgrade

The application will work normally once your quota is restored.
"""
        elif "rate_limit" in error_msg.lower():
            return """
⏱️ **Rate Limit Reached**

Too many requests were made recently. Please wait a moment and try again.
Your OpenAI API has temporary rate limiting active.
"""
        else:
            return f"I encountered an error while processing your question: {error_msg}. Please check your OpenAI API configuration."

def create_study_plan():
    """Generate a personalized study plan."""
    try:
        profile = st.session_state.learning_profile
        subjects = profile["preferred_subjects"]
        level = profile["learning_level"]
        
        if not subjects:
            st.warning("Please select your preferred subjects in the sidebar first.")
            return
        
        prompt = f"""
        Create a comprehensive weekly study plan for a {level} level student focusing on: {', '.join(subjects)}.
        
        Include:
        1. Daily study schedule with time allocations
        2. Subject rotation strategy
        3. Break times and study techniques
        4. Review sessions and practice recommendations
        5. Goal-setting frameworks
        
        Format as a clear, actionable weekly schedule.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        
        study_plan = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown("📝 **Your Personalized Study Plan:**")
            st.markdown(study_plan)
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"📝 **Your Personalized Study Plan:**\n\n{study_plan}"
        })
        
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg:
            st.error("🚨 OpenAI API quota exceeded. Please add credits to your OpenAI account at https://platform.openai.com/settings/billing")
        else:
            st.error(f"Error generating study plan: {error_msg}")

def generate_quiz():
    """Generate a quiz based on preferred subjects."""
    try:
        profile = st.session_state.learning_profile
        subjects = profile["preferred_subjects"]
        level = profile["learning_level"]
        
        if not subjects:
            st.warning("Please select your preferred subjects in the sidebar first.")
            return
        
        # Pick a random subject for the quiz
        import random
        subject = random.choice(subjects) if subjects else "General Knowledge"
        
        prompt = f"""
        Create a {level} level quiz on {subject} with 5 multiple choice questions.
        
        Format:
        Question 1: [Question text]
        A) Option A
        B) Option B  
        C) Option C
        D) Option D
        
        Include the correct answers at the end.
        Make questions educational and thought-provoking for {level} level students.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        
        quiz = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(f"🎯 **Quiz Time: {subject}**")
            st.markdown(quiz)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🎯 **Quiz Time: {subject}**\n\n{quiz}"
        })
        
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg:
            st.error("🚨 OpenAI API quota exceeded. Please add credits to your OpenAI account.")
        else:
            st.error(f"Error generating quiz: {error_msg}")

def show_progress_report():
    """Show learning progress and insights."""
    try:
        interactions = st.session_state.memory_manager.get_interaction_summary()
        profile = st.session_state.learning_profile
        
        prompt = f"""
        Based on this student's learning interaction history, create a progress report:
        
        Student Profile: {profile}
        Recent Interactions Summary: {interactions}
        
        Include:
        1. Learning strengths observed
        2. Areas for improvement
        3. Study pattern analysis
        4. Recommendations for continued growth
        5. Motivational insights
        
        Keep it encouraging and constructive.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        
        report = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown("📈 **Your Learning Progress Report:**")
            st.markdown(report)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"📈 **Your Learning Progress Report:**\n\n{report}"
        })
        
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg:
            st.error("🚨 OpenAI API quota exceeded. Please add credits to your OpenAI account.")
        else:
            st.error(f"Error generating progress report: {error_msg}")

def get_study_techniques():
    """Provide personalized study techniques."""
    try:
        profile = st.session_state.learning_profile
        level = profile["learning_level"]
        subjects = profile["preferred_subjects"]
        
        prompt = f"""
        Provide personalized study techniques and learning strategies for a {level} level student studying: {', '.join(subjects) if subjects else 'various subjects'}.
        
        Include:
        1. Active learning techniques
        2. Memory improvement strategies
        3. Note-taking methods
        4. Test preparation strategies
        5. Time management tips
        6. Subject-specific study approaches
        
        Make recommendations practical and actionable.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700
        )
        
        techniques = response.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown("🧠 **Personalized Study Techniques:**")
            st.markdown(techniques)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🧠 **Personalized Study Techniques:**\n\n{techniques}"
        })
        
    except Exception as e:
        error_msg = str(e)
        if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg:
            st.error("🚨 OpenAI API quota exceeded. Please add credits to your OpenAI account.")
        else:
            st.error(f"Error generating study techniques: {error_msg}")

if __name__ == "__main__":
    main()