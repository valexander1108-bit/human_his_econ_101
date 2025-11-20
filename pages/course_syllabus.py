import streamlit as st
from modules_data import MICRO_MODULES

def render_course_header(): 
    st.title("ECON 101: Introduction to Microeconomics")
    st.subheader("Choice, the Market, and Institutions Through Time")

    st.markdown("---")
    st.markdown("### Learning Outcomes")
    st.markdown("""
_By the end of this course, students will be able to:_

- **Explain** how core microeconomic thoeries and principles (scarcity, rational choice, marginal analysis, etc.) describe consumer and firm decision-making. 
- **Represent and interpret** fundamental microeconomic models (e.g., budget constraint, PPC, supply and demand, perfectly competitive market model, and more). 
- **Analyze** how markets coordinate choice through incentives and price signals.
- **Identify** how economic outcomes vary when key neoclassical assumptions are altered. 
- **Apply** microeconomic reasoning to historical and contemporary cases. 
- **Evaluate** the limitations of standard models and **compare** these models to behavioral and institutional alternatives.
""")
    st.markdown("---")
    st.markdown("### Course Description")
    st.markdown("""_ECON 101_ introduces the foundational tools economists use to analyze how individuals and firms make decisions under constraints, and how different institutional and historical environments have shaped and continue to shape these decisions.""")
    with st.expander("Read the full description"):
        st.markdown("""
**Students learn to:**
- Represent tradeoffs using microeconomic models  
- Analyze how prices and quantities emerge from interactions between buyers and sellers  
- Understand production, costs, and strategic behavior  
- Examine how rules, norms, and institutions create different patterns of incentives  
- Connect microeconomic theory to diverse historical and contemporary settings  

Throughout the course, economic models are presented as **analytical frameworks** rather than prescriptive systems. Historical cases are used descriptively—to illustrate how different economic environments shape, and are shaped by, human decision-making. Students learn to interpret theory, evaluate assumptions, and observe where models align with or diverge from real human behavior.

The course ends with an overview of how individual decision-making relates to broader social outcomes, including distributional patterns and economic inequality.
""")

    st.markdown("---")
    st.markdown("### Assessment & Course Structure")
    st.markdown("""
This course uses a _tiered learning structure_ to support a wide range of learners:
- Baseline - Intution & Big Ideas
- Tier 1 - Formal Definitions
- Tier 2 - Solid Understanding
- Tier 3 - Extension""")
    with st.expander("Learn More"):
        st.markdown("""

**Baseline - Intuition & Big Ideas**  
- A conceptual introduction that builds intuition before formal tools  

**Tier 1 — Formal Definitions**  
- Core vocabulary and basic theory  

**Tier 2 — Solid Understanding (Assessed at this Tier)**  
- Graphical, numerical, and applied reasoning using standard microeconomic models  

**Tier 3 — Extensions (Optional, for the \"econ-nerd\")**  
- Deeper exploration of historical, institutional, or behavioral topics  

Course assessments focus on understanding, explanation, and application rather than memorization. 

Students are encouraged to reference primary texts, historical sources, and contemporary data whenever relevant.
""")

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