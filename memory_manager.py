import streamlit as st
from typing import List, Dict, Any
from datetime import datetime, timedelta

class MemoryManager:
    """Manages learning session memory and progress tracking."""
    
    def __init__(self):
        self.max_interactions = 50  # Limit memory size
        self.session_key = "learning_memory"
        
        # Initialize memory in session state if not exists
        if self.session_key not in st.session_state:
            st.session_state[self.session_key] = {
                "interactions": [],
                "learning_patterns": {},
                "subject_focus": {},
                "difficulty_tracking": {},
                "last_session": None
            }
    
    def add_interaction(self, user_query: str, ai_response: str):
        """Add a new learning interaction to memory."""
        try:
            memory = st.session_state[self.session_key]
            
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "user_query": user_query,
                "ai_response": ai_response,
                "topics": self._extract_topics(user_query),
                "difficulty": self._estimate_difficulty(user_query),
                "subject": self._identify_subject(user_query)
            }
            
            # Add interaction
            memory["interactions"].append(interaction)
            
            # Maintain memory limit
            if len(memory["interactions"]) > self.max_interactions:
                memory["interactions"] = memory["interactions"][-self.max_interactions:]
            
            # Update learning patterns
            self._update_learning_patterns(interaction)
            
            # Update session state
            st.session_state[self.session_key] = memory
            
        except Exception as e:
            # Silent fail to not disrupt user experience
            pass
    
    def get_learning_context(self) -> str:
        """Get relevant learning context from recent interactions."""
        try:
            memory = st.session_state[self.session_key]
            recent_interactions = memory["interactions"][-5:]  # Last 5 interactions
            
            if not recent_interactions:
                return "No previous learning interactions in this session."
            
            context_parts = []
            
            # Recent topics discussed
            recent_topics = []
            recent_subjects = []
            
            for interaction in recent_interactions:
                recent_topics.extend(interaction.get("topics", []))
                if interaction.get("subject"):
                    recent_subjects.append(interaction["subject"])
            
            if recent_topics:
                context_parts.append(f"Recent topics: {', '.join(list(set(recent_topics)))}")
            
            if recent_subjects:
                subject_counts = {}
                for subject in recent_subjects:
                    subject_counts[subject] = subject_counts.get(subject, 0) + 1
                most_discussed = max(subject_counts.items(), key=lambda x: x[1])[0]
                context_parts.append(f"Primary subject focus: {most_discussed}")
            
            # Learning patterns
            patterns = memory.get("learning_patterns", {})
            if patterns:
                if patterns.get("preferred_question_types"):
                    context_parts.append(f"Student prefers: {', '.join(patterns['preferred_question_types'])}")
                
                if patterns.get("difficulty_trend"):
                    context_parts.append(f"Difficulty progression: {patterns['difficulty_trend']}")
            
            return "; ".join(context_parts) if context_parts else "Beginning of learning session."
            
        except Exception as e:
            return "Unable to retrieve learning context."
    
    def get_interaction_summary(self) -> str:
        """Get a summary of all learning interactions for progress reports."""
        try:
            memory = st.session_state[self.session_key]
            interactions = memory["interactions"]
            
            if not interactions:
                return "No learning interactions recorded yet."
            
            # Calculate statistics
            total_interactions = len(interactions)
            
            # Subject distribution
            subjects = [i.get("subject", "Unknown") for i in interactions if i.get("subject")]
            subject_counts = {}
            for subject in subjects:
                subject_counts[subject] = subject_counts.get(subject, 0) + 1
            
            # Topic diversity
            all_topics = []
            for interaction in interactions:
                all_topics.extend(interaction.get("topics", []))
            unique_topics = list(set(all_topics))
            
            # Difficulty progression
            difficulties = [i.get("difficulty", "medium") for i in interactions[-10:]]  # Last 10
            
            # Time span
            if total_interactions > 1:
                first_time = datetime.fromisoformat(interactions[0]["timestamp"])
                last_time = datetime.fromisoformat(interactions[-1]["timestamp"])
                session_duration = last_time - first_time
            else:
                session_duration = timedelta(0)
            
            summary_parts = [
                f"Total interactions: {total_interactions}",
                f"Session duration: {self._format_duration(session_duration)}",
                f"Topics explored: {len(unique_topics)} unique topics",
                f"Most discussed subject: {max(subject_counts.items(), key=lambda x: x[1])[0] if subject_counts else 'Various'}",
                f"Recent difficulty level: {difficulties[-1] if difficulties else 'Not assessed'}"
            ]
            
            return "; ".join(summary_parts)
            
        except Exception as e:
            return "Unable to generate interaction summary."
    
    def _extract_topics(self, query: str) -> List[str]:
        """Extract key topics from user query."""
        # Simple keyword extraction
        topics = []
        
        # Math topics
        math_keywords = ["equation", "algebra", "geometry", "calculus", "trigonometry", 
                        "statistics", "probability", "derivative", "integral", "formula"]
        
        # Science topics
        science_keywords = ["physics", "chemistry", "biology", "atom", "molecule", 
                           "cell", "force", "energy", "reaction", "evolution"]
        
        # Language topics
        language_keywords = ["grammar", "essay", "writing", "literature", "poem", 
                            "analysis", "thesis", "paragraph", "vocabulary"]
        
        # History topics
        history_keywords = ["war", "revolution", "empire", "civilization", "timeline",
                           "ancient", "medieval", "modern", "century"]
        
        all_keywords = math_keywords + science_keywords + language_keywords + history_keywords
        
        query_lower = query.lower()
        for keyword in all_keywords:
            if keyword in query_lower:
                topics.append(keyword)
        
        return topics[:3]  # Limit to 3 topics
    
    def _estimate_difficulty(self, query: str) -> str:
        """Estimate the difficulty level of the query."""
        query_lower = query.lower()
        
        # Advanced indicators
        advanced_indicators = ["advanced", "complex", "analyze", "evaluate", "synthesize",
                              "derivative", "integral", "quantum", "molecular", "theorem"]
        
        # Basic indicators  
        basic_indicators = ["what is", "how to", "explain", "simple", "basic", "introduction"]
        
        advanced_count = sum(1 for indicator in advanced_indicators if indicator in query_lower)
        basic_count = sum(1 for indicator in basic_indicators if indicator in query_lower)
        
        if advanced_count > basic_count:
            return "advanced"
        elif basic_count > 0:
            return "beginner"
        else:
            return "intermediate"
    
    def _identify_subject(self, query: str) -> str:
        """Identify the primary subject of the query."""
        query_lower = query.lower()
        
        subject_keywords = {
            "Mathematics": ["math", "algebra", "geometry", "calculus", "equation", "formula", "solve"],
            "Physics": ["physics", "force", "energy", "momentum", "wave", "electricity", "magnetism"],
            "Chemistry": ["chemistry", "atom", "molecule", "reaction", "compound", "element"],
            "Biology": ["biology", "cell", "DNA", "evolution", "organism", "genetics", "anatomy"],
            "Computer Science": ["programming", "code", "algorithm", "software", "computer", "python", "java"],
            "English": ["essay", "writing", "grammar", "literature", "poem", "analysis", "thesis"],
            "History": ["history", "war", "empire", "revolution", "ancient", "medieval", "timeline"],
            "Geography": ["geography", "map", "climate", "country", "continent", "ocean", "mountain"],
            "Art": ["art", "painting", "sculpture", "artist", "museum", "drawing", "design"],
            "Music": ["music", "note", "chord", "rhythm", "melody", "instrument", "composer"],
        }
        
        subject_scores = {}
        for subject, keywords in subject_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                subject_scores[subject] = score
        
        if subject_scores:
            return max(subject_scores.items(), key=lambda x: x[1])[0]
        
        return "General"
    
    def _update_learning_patterns(self, interaction: Dict[str, Any]):
        """Update learning patterns based on new interaction."""
        try:
            memory = st.session_state[self.session_key]
            patterns = memory.get("learning_patterns", {})
            
            # Track question types
            query_type = self._classify_question_type(interaction["user_query"])
            if "preferred_question_types" not in patterns:
                patterns["preferred_question_types"] = []
            
            patterns["preferred_question_types"].append(query_type)
            patterns["preferred_question_types"] = patterns["preferred_question_types"][-10:]  # Keep last 10
            
            # Track difficulty progression
            if "difficulty_history" not in patterns:
                patterns["difficulty_history"] = []
            
            patterns["difficulty_history"].append(interaction["difficulty"])
            patterns["difficulty_history"] = patterns["difficulty_history"][-10:]  # Keep last 10
            
            # Determine difficulty trend
            if len(patterns["difficulty_history"]) >= 3:
                recent_difficulties = patterns["difficulty_history"][-3:]
                difficulty_values = {"beginner": 1, "intermediate": 2, "advanced": 3}
                scores = [difficulty_values[d] for d in recent_difficulties]
                
                if scores[-1] > scores[0]:
                    patterns["difficulty_trend"] = "increasing"
                elif scores[-1] < scores[0]:
                    patterns["difficulty_trend"] = "decreasing"
                else:
                    patterns["difficulty_trend"] = "stable"
            
            memory["learning_patterns"] = patterns
            st.session_state[self.session_key] = memory
            
        except Exception as e:
            # Silent fail
            pass
    
    def _classify_question_type(self, query: str) -> str:
        """Classify the type of question being asked."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["solve", "calculate", "find", "compute"]):
            return "problem_solving"
        elif any(word in query_lower for word in ["explain", "what is", "how does", "why"]):
            return "conceptual"
        elif any(word in query_lower for word in ["analyze", "compare", "evaluate", "discuss"]):
            return "analytical"
        elif any(word in query_lower for word in ["help", "check", "review", "feedback"]):
            return "assistance"
        else:
            return "general"
    
    def _format_duration(self, duration: timedelta) -> str:
        """Format duration for display."""
        total_seconds = int(duration.total_seconds())
        
        if total_seconds < 60:
            return f"{total_seconds} seconds"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            return f"{minutes} minutes"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def clear_memory(self):
        """Clear all learning memory."""
        st.session_state[self.session_key] = {
            "interactions": [],
            "learning_patterns": {},
            "subject_focus": {},
            "difficulty_tracking": {},
            "last_session": None
        }
    
    def get_subject_statistics(self) -> Dict[str, int]:
        """Get statistics about subject engagement."""
        try:
            memory = st.session_state[self.session_key]
            interactions = memory["interactions"]
            
            subject_counts = {}
            for interaction in interactions:
                subject = interaction.get("subject", "Unknown")
                subject_counts[subject] = subject_counts.get(subject, 0) + 1
            
            return subject_counts
            
        except Exception as e:
            return {}