import streamlit as st
import openai
openai.api_key = st.secrets["OPENAI_API_KEY"]

import json
import datetime
from typing import List, Dict, Optional
from collections import Counter



class LearningTools:
    """Specialized tools for different academic subjects and learning tasks."""

    def __init__(self, openai_client):
        self.client = openai_client
        self.tools = {
            # STEM Tools
            "math_solver": self._solve_math_problem,
            "science_explainer": self._explain_science_concept,
            "coding_helper": self._help_with_coding,
            "formula_reference": self._provide_formula_reference,

            # Language Tools
            "writing_assistant": self._assist_with_writing,
            "literature_analysis": self._analyze_literature,
            "language_practice": self._practice_language,
            "grammar_checker": self._check_grammar,

            # Social Studies Tools
            "history_timeline": self._create_history_timeline,
            "geography_helper": self._help_with_geography,
            "economics_explainer": self._explain_economics,
            "political_analysis": self._analyze_politics,

            # Arts Tools
            "music_theory": self._explain_music_theory,
            "art_analysis": self._analyze_artwork,
            "creative_writing": self._assist_creative_writing,

            # Test Prep Tools
            "test_strategy": self._provide_test_strategy,
            "practice_problems": self._generate_practice_problems,
            "study_schedule": self._create_study_schedule,
        }

    def analyze_and_respond(self, query: str, profile: Dict,
                            context: str) -> Optional[str]:
        """Analyze query and determine if a specialized tool should be used."""
        try:
            # Determine which tool to use based on query content
            tool_prompt = f"""
            Analyze this student query and determine if it requires a specialized learning tool.
            
            Query: "{query}"
            Student Level: {profile.get('learning_level', 'intermediate')}
            Preferred Subjects: {profile.get('preferred_subjects', [])}
            
            Available tools:
            - math_solver: For solving mathematical problems, equations, calculations
            - science_explainer: For explaining physics, chemistry, biology concepts
            - coding_helper: For programming questions, debugging, algorithms
            - writing_assistant: For essay writing, composition, writing improvement
            - literature_analysis: For analyzing poems, novels, literary works
            - history_timeline: For historical events, chronology, historical analysis
            - test_strategy: For test preparation, exam strategies, study tips
            - practice_problems: For generating practice questions and exercises
            
            Respond with JSON in this format:
            {{"tool": "tool_name or null", "reasoning": "explanation"}}
            
            Only suggest a tool if the query clearly requires specialized functionality.
            Return null for general conversation or broad educational questions.
            """

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": tool_prompt
                }],
                response_format={"type": "json_object"},
                max_tokens=200)

            result = json.loads(response.choices[0].message.content)
            tool_name = result.get("tool")

            if tool_name and tool_name in self.tools:
                return self.tools[tool_name](query, profile, context)

            return None

        except Exception as e:
            # If tool analysis fails, return None to fall back to general response
            return None

    def _solve_math_problem(self, query: str, profile: Dict,
                            context: str) -> str:
        """Solve mathematical problems with step-by-step explanations."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a mathematics tutor helping a {level} level student.
        
        Problem: {query}
        
        Provide a complete solution with:
        1. Problem identification and what type of math this is
        2. Step-by-step solution with clear explanations
        3. Final answer highlighted
        4. Verification or check of the answer
        5. Similar problem types they might encounter
        6. Key concepts or formulas used
        
        Make explanations appropriate for {level} level understanding.
        Use clear mathematical notation and reasoning.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"🔢 **Math Problem Solver**\n\n{response.choices[0].message.content}"

    def _explain_science_concept(self, query: str, profile: Dict,
                                 context: str) -> str:
        """Explain scientific concepts across physics, chemistry, and biology."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a science tutor explaining concepts to a {level} level student.
        
        Question: {query}
        
        Provide a comprehensive explanation including:
        1. Clear definition of the concept
        2. How it works or why it happens (mechanisms)
        3. Real-world examples and applications
        4. Visual descriptions or analogies to aid understanding
        5. Key terms and vocabulary
        6. Common misconceptions to avoid
        7. Related concepts they should know
        
        Use language appropriate for {level} level and include practical examples.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"🔬 **Science Concept Explainer**\n\n{response.choices[0].message.content}"

    def _help_with_coding(self, query: str, profile: Dict,
                          context: str) -> str:
        """Assist with programming questions and coding problems."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a programming tutor helping a {level} level student with coding.
        
        Coding Question: {query}
        
        Provide helpful guidance including:
        1. Problem analysis and approach
        2. Step-by-step solution strategy
        3. Code examples with explanations
        4. Best practices and coding conventions
        5. Common pitfalls to avoid
        6. Testing and debugging tips
        7. Alternative approaches or optimizations
        
        Explain concepts clearly for {level} level programming understanding.
        Include comments in code examples.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"💻 **Coding Helper**\n\n{response.choices[0].message.content}"

    def _assist_with_writing(self, query: str, profile: Dict,
                             context: str) -> str:
        """Help with writing assignments, essays, and composition."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a writing tutor helping a {level} level student improve their writing.
        
        Writing Request: {query}
        
        Provide comprehensive writing assistance including:
        1. Understanding the writing task or assignment
        2. Structure and organization suggestions
        3. Content development strategies
        4. Style and tone guidance
        5. Grammar and mechanics tips
        6. Revision and editing advice
        7. Examples of effective techniques
        
        Tailor advice to {level} level writing skills and academic expectations.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"✍️ **Writing Assistant**\n\n{response.choices[0].message.content}"

    def _analyze_literature(self, query: str, profile: Dict,
                            context: str) -> str:
        """Analyze literary works, themes, and literary devices."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a literature teacher helping a {level} level student analyze literary works.
        
        Literature Question: {query}
        
        Provide thorough literary analysis including:
        1. Context and background of the work/author
        2. Theme identification and analysis
        3. Literary devices and techniques used
        4. Character analysis and development
        5. Symbolism and deeper meanings
        6. Historical and cultural significance
        7. Personal reflection and interpretation guidance
        
        Make analysis accessible for {level} level literary understanding.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"📚 **Literature Analysis**\n\n{response.choices[0].message.content}"

    def _create_history_timeline(self, query: str, profile: Dict,
                                 context: str) -> str:
        """Create historical timelines and explain historical events."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a history teacher helping a {level} level student understand historical events.
        
        History Question: {query}
        
        Provide comprehensive historical information including:
        1. Timeline of key events
        2. Causes and effects
        3. Important figures and their roles
        4. Historical context and significance
        5. Connections to other historical events
        6. Primary sources or evidence
        7. Long-term impact and legacy
        
        Present information clearly for {level} level historical understanding.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"📜 **History Timeline & Analysis**\n\n{response.choices[0].message.content}"

    def _provide_test_strategy(self, query: str, profile: Dict,
                               context: str) -> str:
        """Provide test preparation strategies and exam tips."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a test prep specialist helping a {level} level student prepare for exams.
        
        Test Prep Question: {query}
        
        Provide strategic test preparation guidance including:
        1. Test format and structure overview
        2. Study timeline and scheduling
        3. Content review strategies
        4. Practice test recommendations
        5. Test-taking techniques and tips
        6. Stress management and preparation
        7. Last-minute review strategies
        
        Tailor advice to {level} level academic preparation needs.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"🎯 **Test Preparation Strategy**\n\n{response.choices[0].message.content}"

    def _generate_practice_problems(self, query: str, profile: Dict,
                                    context: str) -> str:
        """Generate practice problems and exercises."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are creating practice problems for a {level} level student.
        
        Subject/Topic Request: {query}
        
        Create a set of practice problems including:
        1. 3-5 problems of varying difficulty
        2. Clear instructions for each problem
        3. Answer key with explanations
        4. Tips for solving similar problems
        5. Common mistakes to avoid
        6. Extension questions for deeper thinking
        
        Make problems appropriate for {level} level and educational.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=800)

        return f"📝 **Practice Problems**\n\n{response.choices[0].message.content}"

    def _provide_formula_reference(self, query: str, profile: Dict,
                                   context: str) -> str:
        """Provide mathematical and scientific formula references."""
        prompt = f"""
        Provide a comprehensive formula reference for: {query}
        
        Include:
        1. The formula(s) with clear notation
        2. Variable definitions
        3. When and how to use each formula
        4. Example applications
        5. Related formulas
        6. Common variations or special cases
        
        Make it a useful reference guide.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=600)

        return f"📐 **Formula Reference**\n\n{response.choices[0].message.content}"

    def _practice_language(self, query: str, profile: Dict,
                           context: str) -> str:
        """Help with foreign language practice and learning."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a language tutor helping a {level} level student with language learning.
        
        Language Question: {query}
        
        Provide language learning support including:
        1. Grammar explanations with examples
        2. Vocabulary building exercises
        3. Pronunciation tips
        4. Cultural context
        5. Practice sentences and conversations
        6. Common mistakes to avoid
        7. Learning strategies and tips
        
        Adapt to {level} level language proficiency.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"🌍 **Language Practice**\n\n{response.choices[0].message.content}"

    def _check_grammar(self, query: str, profile: Dict, context: str) -> str:
        """Check and explain grammar issues."""
        prompt = f"""
        Analyze the following text for grammar, style, and clarity:
        
        "{query}"
        
        Provide:
        1. Corrected version if needed
        2. Explanation of any errors found
        3. Grammar rules that apply
        4. Style suggestions for improvement
        5. Tips for avoiding similar mistakes
        
        Be constructive and educational in feedback.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=600)

        return f"✅ **Grammar Check**\n\n{response.choices[0].message.content}"

    def _help_with_geography(self, query: str, profile: Dict,
                             context: str) -> str:
        """Help with geography concepts and questions."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a geography teacher helping a {level} level student.
        
        Geography Question: {query}
        
        Provide comprehensive geographic information including:
        1. Location and physical characteristics
        2. Climate and environmental factors
        3. Human geography and demographics
        4. Economic and political aspects
        5. Cultural significance
        6. Maps, coordinates, or spatial relationships
        7. Current issues or changes
        
        Make explanations appropriate for {level} level geography understanding.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"🌍 **Geography Helper**\n\n{response.choices[0].message.content}"

    def _explain_economics(self, query: str, profile: Dict,
                           context: str) -> str:
        """Explain economic concepts and principles."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are an economics teacher explaining concepts to a {level} level student.
        
        Economics Question: {query}
        
        Provide clear economic analysis including:
        1. Definition and explanation of concepts
        2. Economic principles involved
        3. Real-world examples and applications
        4. Graphs or models if relevant
        5. Cause and effect relationships
        6. Different economic perspectives
        7. Current relevance and implications
        
        Use language appropriate for {level} level economics education.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"💰 **Economics Explainer**\n\n{response.choices[0].message.content}"

    def _analyze_politics(self, query: str, profile: Dict,
                          context: str) -> str:
        """Analyze political concepts and systems."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a political science teacher helping a {level} level student understand political concepts.
        
        Political Science Question: {query}
        
        Provide balanced political analysis including:
        1. Explanation of political concepts or systems
        2. Historical context and development
        3. Different perspectives and viewpoints
        4. Comparative analysis if relevant
        5. Key figures and their contributions
        6. Current applications and relevance
        7. Critical thinking questions
        
        Maintain objectivity and present multiple viewpoints for {level} level understanding.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"🏛️ **Political Analysis**\n\n{response.choices[0].message.content}"

    def _explain_music_theory(self, query: str, profile: Dict,
                              context: str) -> str:
        """Explain music theory concepts."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a music theory instructor teaching a {level} level student.
        
        Music Theory Question: {query}
        
        Provide comprehensive music theory explanation including:
        1. Clear definition of concepts
        2. Musical notation examples
        3. How it applies to composition and performance
        4. Listening examples or references
        5. Practice exercises or applications
        6. Connections to other musical concepts
        7. Historical context in music
        
        Make explanations accessible for {level} level music education.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"🎵 **Music Theory Guide**\n\n{response.choices[0].message.content}"

    def _analyze_artwork(self, query: str, profile: Dict, context: str) -> str:
        """Analyze artworks and art history."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are an art history teacher helping a {level} level student analyze artwork.
        
        Art Question: {query}
        
        Provide thorough art analysis including:
        1. Visual description and composition
        2. Artistic techniques and mediums used
        3. Historical and cultural context
        4. Artist background and style
        5. Symbolism and meaning
        6. Influence and significance
        7. Comparison to other works or movements
        
        Make analysis engaging and educational for {level} level art appreciation.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"🎨 **Art Analysis**\n\n{response.choices[0].message.content}"

    def _assist_creative_writing(self, query: str, profile: Dict,
                                 context: str) -> str:
        """Assist with creative writing projects."""
        level = profile.get('learning_level', 'intermediate')

        prompt = f"""
        You are a creative writing instructor helping a {level} level student with their creative work.
        
        Creative Writing Request: {query}
        
        Provide creative writing guidance including:
        1. Story development and plot structure
        2. Character creation and development
        3. Setting and world-building
        4. Dialogue and voice techniques
        5. Literary devices and style
        6. Revision and editing strategies
        7. Inspiration and brainstorming methods
        
        Encourage creativity while providing practical writing advice for {level} level.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"🖋️ **Creative Writing Assistant**\n\n{response.choices[0].message.content}"

    def _create_study_schedule(self, query: str, profile: Dict,
                               context: str) -> str:
        """Create personalized study schedules."""
        level = profile.get('learning_level', 'intermediate')
        subjects = profile.get('preferred_subjects', [])

        prompt = f"""
        Create a detailed study schedule for a {level} level student.
        
        Request: {query}
        Preferred Subjects: {', '.join(subjects) if subjects else 'General studies'}
        
        Include:
        1. Daily time blocks and study periods
        2. Subject rotation and priority
        3. Break times and active rest
        4. Review sessions and practice time
        5. Flexibility for different learning styles
        6. Progress tracking methods
        7. Adjustment strategies
        
        Make it practical and sustainable for consistent use.
        """

        response = self.client.chat.completions.create(model="gpt-4o",
                                                       messages=[{
                                                           "role":
                                                           "user",
                                                           "content":
                                                           prompt
                                                       }],
                                                       max_tokens=700)

        return f"📅 **Study Schedule Planner**\n\n{response.choices[0].message.content}"
    