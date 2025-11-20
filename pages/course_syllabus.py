# pages/course_syllabus.py
import streamlit as st
from modules_data import MICRO_MODULES

def render_course_header():
    st.title("ECON 101: Introduction to Microeconomics")
    st.subheader("Course Syllabus & Knowledge Base")

    st.markdown("""
This view is your **central hub** for ECON 101.

Scroll down to:

- Read the course overview and learning outcomes
- Open each module to see:
  - Overview & Intuition
  - Tier 1 – Formal Definitions
  - Tier 2 – Solid Understanding (assessment tier)
  - Tier 3 – Extensions (optional, except Module 8)
  - All required materials: slides, notes, labs, interactive models, and practice links
    """)

    st.markdown("---")

    st.markdown("### Course Description")
    st.markdown("_TODO: Paste your original course description here._")

    st.markdown("### Course Learning Outcomes")
    st.markdown("_TODO: Paste your course-wide learning objectives here._")

    st.markdown("### Assessment & Course Structure")
    st.markdown("_TODO: Paste your grading breakdown & assessment overview here._")

    st.markdown("---")
    st.markdown("## Modules")

def render_module_block(module: dict):
    title = f"Module {module['id']}: {module['title']}"
    with st.expander(title, expanded=False):
        st.markdown(f"**Short description:** {module['short_desc']}")
        st.markdown("---")

        # Module 8 (and any future untiered modules)
        if module.get("is_untiered", False):
            st.markdown(module.get("untiered_markdown", "_Coming soon._"))
        else:
            st.markdown(module.get("overview_intuition", "### Overview & Intuition\n_Coming soon._"))
            st.markdown(module.get("tier1_definitions", "### Tier 1 – Formal Definitions\n_Coming soon._"))
            st.markdown(module.get("tier2_solid", "### Tier 2 – Solid Understanding (Assessment Tier)\n_Coming soon._"))
            st.markdown(module.get("tier3_extensions", "### Tier 3 – Extensions (Optional)\n_Coming soon._"))

        st.markdown("---")
        st.markdown("### Required Course Materials")

        materials = module.get("materials", {})
        col1, col2, col3 = st.columns(3)

        with col1:
            slides = materials.get("slides")
            notes = materials.get("guided_notes")
            if slides:
                st.markdown(f"- [📑 Slide Deck]({slides})")
            if notes:
                st.markdown(f"- [📝 Guided Notes]({notes})")

        with col2:
            labs = materials.get("labs", [])
            if labs:
                st.markdown("**Labs / Activities**")
                for lab in labs:
                    st.markdown(f"- [🧪 {lab['label']}]({lab['url']})")

            khan = materials.get("khan", [])
            if khan:
                st.markdown("**Khan Academy / Practice**")
                for item in khan:
                    st.markdown(f"- [📘 {item['label']}]({item['url']})")

        with col3:
            models = materials.get("models", [])
            if models:
                st.markdown("**Interactive Models**")
                for model in models:
                    st.markdown(f"- [📊 {model['label']}]({model['url']})")

            videos = materials.get("videos", [])
            audio = materials.get("audio", [])
            if videos:
                st.markdown("**Videos**")
                for vid in videos:
                    st.markdown(f"- [🎥 {vid['label']}]({vid['url']})")
            if audio:
                st.markdown("**Audio**")
                for a in audio:
                    st.markdown(f"- [🎧 {a['label']}]({a['url']})")

        st.caption("You are expected to engage with all required materials listed above for this module.")

def app():
    render_course_header()
    for module in MICRO_MODULES:
        render_module_block(module)