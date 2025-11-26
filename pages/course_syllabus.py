import streamlit as st
import streamlit.components.v1 as components
from modules_data import MICRO_MODULES

def render_course_header(): 
    st.title("ECON 101: Introduction to Microeconomics")
    st.subheader("Choices, Markets, and Institutions in Time and Space")
    st.markdown("---")
    st.markdown("## Overview")
    st.markdown("""_ECON 101_ introduces the foundational tools economists use to analyze how individuals and firms make decisions under constraints, and how different institutional and historical environments have shaped and continue to shape these decisions.""")
    with st.expander("Course Information", expanded=False):
        st.markdown("""
- **Class Location:** _TBD_  
- **Class Hours:** _TBD_  
- **Instructor:** Prof. Alexander Velazquez  
- **Email:** av663411@sju.edu  
- **Office Hours:** _TBD_  
- **Course Website:** Canvas (materials and updates)  
""")
    with st.expander("Full Description"):
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
    st.markdown("## Objectives")
    st.markdown("""_By the end of this course, students will be able to:_
- **Explain** how core microeconomic thoeries and principles (scarcity, rational choice, marginal analysis, etc.) describe consumer and firm decision-making. 
- **Represent and interpret** fundamental microeconomic models (e.g., budget constraint, PPC, supply and demand, perfectly competitive market model, and more). 
- **Analyze** how markets coordinate choice through incentives and price signals.
- **Identify** how economic outcomes vary when key neoclassical assumptions are altered. 
- **Apply** microeconomic reasoning to historical and contemporary cases. 
- **Evaluate** the limitations of standard models and **compare** these models to behavioral and institutional alternatives.
""")

    st.markdown("---")
    st.markdown("## Content")
    st.markdown("""
_This course uses a **tiered learning structure** to support a wide range of learners._

- **Baseline — _Intuition & Big Ideas_** — A conceptual introduction that builds intuition before formal tools  

- **Tier 1 — _Formal Definitions_** — Core vocabulary and basic theory  

- **Tier 2 — _Solid Understanding (Assessed at this Tier)_** — Graphical, numerical, and applied reasoning using standard microeconomic models  

- **Tier 3 — _Extensions (Optional, for the \"econ-nerd\")_** — Deeper exploration of historical, institutional, or behavioral topics  
""")
    
    with st.expander("Required Materials", expanded=False):
        st.markdown("""
**Classroom Materials**  
- Notebook and laptop each class - PHONES IN BAGS - I will direct laptop usage. 
                    
**Primary Text**  
- *OpenStax – Principles of Microeconomics 3e*  
  https://openstax.org/books/principles-microeconomics-3e/pages/2-3-confronting-objections-to-the-economic-approach

**Material Access**
- Main "Knowledge Base": Streamlit app designed by Prof. Velazquez
- Slides and Guided Notes: Canva
- Interactive assignments: Notion 
- Independent Practice: Khan Academy & Physical Notebook             
- Assignments/submissions: Canvas
                                      
**Additional Texts**  
- The course draws on my own learning experiences with multiple economics texts (e.g. Mankiw, McConnell, Brue & Finn 19e, corECON) to deepen selected topics and ensure alignment to cannonical economic coursework. 
""")
    st.markdown("---")
def render_module_block(module: dict):
    title = f"Module {module['id']}: {module['title']}"
    with st.expander(title, expanded=False):
        openstax_optional = module.get("openstax", {}).get("optional", [])
        
        # Module 8 (and any future untiered modules)
        if module.get("is_untiered", False):
            st.markdown(module.get("untiered_markdown", "_Coming soon._"))
        else:
            st.markdown(module.get("overview_intuition", "### Intuition\n_Coming soon._"))
            primary_texts = module.get("materials", {}).get("primary_texts", [])
            readings = module.get("materials", {}).get("readings", [])
            if readings:
                with st.expander("Textbook Readings", expanded=False):
                    for rd in readings:
                        st.markdown(f"- [{rd['label']}]({rd['url']})")
            st.markdown("---")
            st.markdown(module.get("tier1_definitions", "### Tier 1 – Formal Definitions\n_Coming soon._"))
            st.markdown(module.get("tier2_solid", "### Tier 2 – Solid Understanding (Assessment Tier)\n_Coming soon._"))
            st.markdown(module.get("tier3_extensions", "### Tier 3 – Extensions (Optional)\n_Coming soon._"))
            if primary_texts:
                with st.expander("Primary Literature Readings", expanded=False):
                    st.markdown("_If you want the source texts behind these ideas, start here._")
                    for pt in primary_texts:
                        note = pt.get("note")
                        meta_parts = [pt.get("tradition"), pt.get("era")]
                        meta = f" ({', '.join([m for m in meta_parts if m])})" if any(meta_parts) else ""
                        note_suffix = f" — {note}" if note else ""
                        st.markdown(f"- [{pt['label']}]({pt['url']}){note_suffix}{meta}")

        st.markdown("---")
        st.markdown(f"### Module {module['id']} Course Materials")

        materials = module.get("materials", {})
        slides = materials.get("slides")
        notes = materials.get("guided_notes")
        labs = materials.get("labs", [])
        khan = materials.get("khan", [])
        models = materials.get("models", [])
        extensions = materials.get("extensions", [])
        videos = materials.get("videos", [])
        audio = materials.get("audio", [])

        # Helper to generate embed-friendly Canva URLs
        def _embed_url(url: str) -> str:
            if not url:
                return url
            if "canva.com" in url:
                if "/edit" in url:
                    base = url.replace("/edit", "/view")
                    return f"{base}{'&' if '?' in base else '?'}embed"
                if "/view" in url and "embed" not in url:
                    return f"{url}{'&' if '?' in url else '?'}embed"
            if "docs.google.com/presentation" in url:
                # Use the clean embed endpoint to avoid letterboxing bars
                clean = url.split("#", 1)[0].split("?", 1)[0]
                if "/preview" in clean:
                    return clean.replace("/preview", "/embed")
                if "/edit" in clean:
                    return clean.replace("/edit", "/embed")
                return clean
            return url

        # Embed slides when available
        if slides:
            st.markdown("#### Lecture Slides")
            components.html(
                f'<iframe src="{_embed_url(slides)}" width="100%" height="640" style="border:0; background:transparent;" allowfullscreen></iframe>',
                height=660,
            )
            st.markdown(f"[Open in new tab]({slides})")
            st.markdown("---")

        # Consistent two-column layout for all modules
        col_left, col_right = st.columns(2)

        with col_left:
            if notes:
                st.markdown("#### Guided Notes")
                components.html(
                    f'<iframe src="{_embed_url(notes)}" width="100%" height="640" style="border:0; background:transparent;" allowfullscreen></iframe>',
                    height=660,
                )
                st.markdown(f"[Open in new tab]({notes})")
            else:
                st.markdown("#### Guided Notes")
                if notes:
                    st.markdown(f"- [📝 Guided Notes]({notes})")
                else:
                    st.markdown("_No guided notes provided._")

        with col_right:
            if models:
                st.markdown("#### Economic Models")
                for model in models:
                    st.markdown(f"- [📊 {model['label']}]({model['url']})")

            if labs:
                st.markdown("#### Activities")
                for lab in labs:
                    st.markdown(f"- [🧪 {lab['label']}]({lab['url']})")

            st.markdown("#### Independent Practice")
            if khan:
                for item in khan:
                    st.markdown(f"- [📘 {item['label']}]({item['url']})")
            else:
                st.markdown("_No independent practice links added yet._")

            if openstax_optional:
                st.markdown("#### Read Ahead")
                for rd in openstax_optional:
                    st.markdown(f"- [📖 {rd['label']}]({rd['url']})")

            background = materials.get("background", [])
            if background:
                st.markdown("#### Background Knowledge")
                for item in background:
                    st.markdown(f"- [{item['label']}]({item['url']})")

            if extensions or videos or audio:
                st.markdown("#### Deeper Meanings")
                for ext in extensions:
                    st.markdown(f"- [{ext['label']}]({ext['url']})")
                for vid in videos:
                    st.markdown(f"- [🎥 {vid['label']}]({vid['url']})")
                for a in audio:
                    st.markdown(f"- [🎧 {a['label']}]({a['url']})")

def app():
    # Sidebar table of contents for quick jumps (uses header anchors)
    with st.sidebar.expander("**Table of Contents**", expanded=True):
        st.markdown("[**Overview**](#overview)")
        st.markdown("[**Objectives**](#objectives)")
        st.markdown("[**Content**](#content)")
        st.markdown("[**1 - Economic Thought & Modeling**](#module-1-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🧭 *explore content*](#module-1-course-materials)")
        st.markdown("[**2 - Supply & Demand**](#module-2-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[❌ *explore content*](#module-2-course-materials)")
        st.markdown("[**3 - Elasticity**](#module-3-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🧲 *explore content*](#module-3-course-materials)")
        st.markdown("[**4 - Welfare & Intervention**](#module-4-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[⚖️ *explore content*](#module-4-course-materials)")
        st.markdown("[**5 - Factors of Production**](#module-5-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🏭 *explore content*](#module-5-course-materials)")
        st.markdown("[**6 - Choices & Constraints**](#module-6-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🎯 *explore content*](#module-6-course-materials)")
        st.markdown("[**7 - Capitalism**](#module-7-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🌍 *explore content*](#module-7-course-materials)")
        st.markdown("[**8 - Inequality**](#module-8-learningt)")
        st.markdown("&nbsp;&nbsp;&nbsp;[📊 *explore content*](#module-8-course-materials)")
        st.markdown("[**9 - Cost of Production**](#module-9-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🧮 *explore content*](#module-9-course-materials)")
        st.markdown("[**10 - Profit Maximization**](#module-10-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[💹 *explore content*](#module-10-course-materials)")
        st.markdown("[**11 - Competition & Information**](#module-11-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🎲 *explore content*](#module-11-course-materials)")
        st.markdown("[**12- Policy, Paradox & Human Perspective**](#module-12-learning)")
        st.markdown("&nbsp;&nbsp;&nbsp;[🛠️ *explore content*](#module-12-course-materials)")
        st.markdown("[**Grades**](#grades)")
        st.markdown("[**Policies**](#policies)")
        st.markdown("[**Resources**](#resources)")

    render_course_header()
    for module in MICRO_MODULES:
        render_module_block(module)
    st.markdown("---")
    st.markdown("## Grades")
    st.markdown("""Course assessments focus on the understanding, explanation, and application of microeconomics concepts rather than rope quantification or memorization . 

Students engage directly with core microeconomic theory, primary economic texts, a variety of historical sources, and various sizes of contemporary data through lectures, guided notes, thought experiments, online independent practice, group lab activites, formative assessments, summative assessments and item analysis.""")

    with st.expander("Math Prerequisites", expanded=False):
        st.markdown("""
Economics leans on proportional reasoning, linear relationships on a quadrant plane, and marginal thinking. We build these skills in tiers so every student has a clear path into the math economists use.

**Tiered objectives (choose your lane)**
- **Tier 1 — Building comfort (not confident yet):** solidify ratios/percents/decimals/fractions; read the coordinate plane; connect slope to “rise over run”; use simple tables to see how small changes create marginal effects; explore straight-line growth to preview marginal analysis.
- **Tier 2 — Solid footing (okay with math):** apply proportional and linear relationships to demand/supply/cost lines; use midpoint/percent change with graphs; visualize marginal analysis with common growth shapes (linear, concave, convex) and link slopes to “how fast” outcomes change.
- **Tier 3 — Confident/strong:** bring algebra and intro calculus intuition to quantify marginal changes; compute slopes from data and simple derivatives; use visuals and computation to interpret real settings (cost curves, revenue, surplus, externalities); compare discrete vs. continuous marginal analysis.

**Where it shows up**
- Modules 1–4: slopes, intercepts, and 2×2 systems for equilibrium; triangle/rectangle areas for surplus and DWL; percent changes for shocks.
- Modules 5–6: ratios and marginal-per-dollar in factor markets; optional intertemporal choice with simple growth/discounting.
- Modules 9–11: turning tables into MC/ATC/AVC, MR = MC decisions, profit boxes.
- Module 12: wedge diagrams for externalities, triangle areas for DWL, elasticity logic for tax incidence.
""")
        st.caption("All practice materials and assessments align to these objectives. Recommended prerequisite: Algebra 1.")

    with st.expander("Assignments"):
        st.markdown("""
**Graded Work**
- **Independent Practice (HW 1–5): 10%** — Khan Academy problems, show work by hand and upload.
- **Formative Assessments (Quiz 1–4): 10%** — two traditional quizzes; two self-graded (study guide + policy lab). Lowest quiz dropped.
- **Summative Assessments (Midterms 1 & 2): 40%** — cumulative up to each exam; small notecard allowed; approved calculator only.
- **Cumulative Final: 30%** — no curve; limited exemptions based on midterm averages and approved contributions.

- **Participation: 10%** - Attendance required; participation includes digital/class activities and two subjective checks (after Midterm 1 and Final). Four unexcused absences allowed; excused requires documentation.

**Key Weekly/Assessment Milestones**  
| MOD | Title | Description | Submit | Weight |
| --- | --- | --- | --- | --- |
| 1 | Economics Pretest | Khan Academy Course Challenge | Khan Academy (keep scratch) | Participation |
| 1 | Math Diagnostic | Khan Academy Middle/HS Math | Khan Academy (keep scratch) | Participation |
| 2 | Independent Practice - Notebook 1 | Khan Academy Basic Concepts | Khan + upload to Canvas | 2% |
| 2 | Formative 1 | Units 1 & 2 | In-class | ~3.33% |
| 5 | Independent Practice - Notebook 2 | Khan Academy Supply & Demand | Khan + upload to Canvas | 2% |
| 6 | Formative 2 | Units 4,5,6,7 | In-class | ~3.33% |
| 8 | Summative 1 (Midterm) | Units 1–7 | In-class | 20% |
| 8 | Participation (First Half) | Discussions/tutorials | Instructor entered | 2% |
| 10 | Independent Practice - Notebook 3 | Khan Academy Cost/PC | Khan + upload to Canvas | 2% |
| 10 | Formative 3 | Midterm 2 Study Guide | Hand-in | ~3.33% |
| 11 | Independent Practice - Notebook 4 | Khan Academy Imperfect Comp | Khan + upload to Canvas | 2% |
| 11 | Summative 2 (Midterm) | Units 9–12 | In-person | 20% |
| 12 | Formative 4 | Public Policy Lab (group) | In/out of class | ~3.33% |
| 12 | Economics Posttest | Khan Academy Course Challenge | In-person | Participation |
| 12 | Independent Practice - Notebook 5 | Midterm Item Analysis | Online | 2% |
| — | Cumulative Final | All material | In-person | 30% |
| — | Participation (Second Half) | — | Instructor entered | 2% |
""")

    with st.expander("Late & Missed Work"):
        st.markdown("""
**Late Policy**  
- Two late passes total (one assignment = one pass = up to two days). After passes, late work = 0.

**Make-Up Policy**  
- No makeups for formatives; lowest quiz dropped.  
- Missed midterm: weight shifts to final (no makeup).  
- Missed final: makeup only for unavoidable, verifiable reasons per university policy; otherwise 0.  
- Exam accommodations per university guidelines; travel plans are not grounds for changes.
""")
    st.markdown("---")
    st.markdown("### Policies")
    with st.expander("Inclusive Learning"):
        st.markdown("""Source: Dr. Cecilia M. Orphan, University of  Denver

In this class, we will work together to develop a learning community that is inclusive and respectful. Our diversity may be reflected by differences in race, culture, age, religion,  sexual orientation, socioeconomic background, and myriad other social identities and life  experiences. The goal of inclusiveness, in a diverse community, encourages and  appreciates expressions of different ideas, opinions, and beliefs, so that conversations and  interactions that could potentially be divisive turn instead into opportunities for  intellectual and personal enrichment.

A dedication to inclusiveness requires respecting what others say, their right to say it, and  the thoughtful consideration of others’ communication. Both speaking up and listening  are valuable tools for furthering thoughtful, enlightening dialogue. Respecting one  another’s individual differences is critical in transforming a collection of diverse  individuals into an inclusive, collaborative and excellent learning community. Our core  commitment shapes our core expectation for behavior inside and outside of the classroom.
                    """)
    with st.expander("Community Standards"):
        st.markdown("""The Office of Community Standards supports the University’s Catholic and Jesuit mission through the education and administration of policies and expectations designed to promote a safe, respectful, inclusive, and welcoming environment, in which all students can learn, grow, and become moral leaders in their communities. The Office of Community Standards encourages all students to reflect on what it means to be a Hawk, on and off campus, and understand the impact and harm their individual decisions and actions can have on others.

To support the continuation of a positive, safe, and educational setting, the University has adopted an array of policies, rules, regulations, and expectations. Should any member of the University community violate an established policy, rule, regulation, or expectation, the University has in place processes intended to educate and hold accountable those in violation and deter further violations by that and/or other individuals. For more information, please refer to the Student Handbook or email

[communitystandards@sju.edu](mailto:communitystandards@sju.edu)
                    """)
    with st.expander("AI Statement"):
        st.markdown("""Like all technology, artificial intelligence (A.I.) is moving quickly. It can be an amazing  tool, but can also be used to circumvent the learning process, depriving you of important  skill development and learning opportunities. *In this course, the appropriate and  approved use of A.I. will differ across assignments*. For each assignment, I will provide  guidelines on how A.I. can and cannot be used, as well as how to document its usage.  Using A.I. appropriately and ethically can enhance your learning experience. However,  using A.I. inappropriately or without approval will be considered an academic honesty  violation and will be subject to the same consequences as cheating and plagiarism. As a warning, ChatGPT and other language learning models (LLMs) have limits and  make mistakes. You need to be critical of the output from any LLM, as you will  ultimately be responsible for any errors or omissions that the tool may make.

Finally, a note about your humanity: our job as humans is to experience the world and to  think about our experiences, to provide insight and intuition to accomplish our goals – don’t be quick to outsource this to A.I.!
                    """)
    with st.expander("Academic Honesty"):
        st.markdown("""Saint Joseph’s University encourages the free and open pursuit of knowledge; we consider this to be a fundamental principle and strength of a democratic people. To this end, SJU expects its students, its faculty, its administrators, and its staff to uphold the highest standards of academic integrity. The University expects all members of the University community to both honor and protect one another’s individual and collective rights.

**The [SJU Academic Honesty Policy](https://sites.sju.edu/registrar/academic-honesty-policy/)** which is published both in the Student Handbook and in the University Catalog, will be strictly enforced.  It is your responsibility to understand this policy.  Use of unauthorized notes or assistance during an exam will result in at least failure of the assignment.  Plagiarism will also result in at least failure of the assignment.  Plagiarism occurs in any instance where one submits as one’s own work statements or ideas taken from another source but not properly acknowledged as such. Any material copied or derived from another source must be acknowledged by giving a reference. For direct quotes, always use quotation marks and provide a reference. If you paraphrase something, you must provide a reference to acknowledge where you found the material.  Internet sources, if used, must be cited.
                    """)
    with st.expander("Technology & Participation"):
        st.markdown("""Texting, cell phone, and laptop use during class is distracting to your peers and your  professor, and therefore, the use of laptops and cell phones is not permitted during class EXCEPT when instructed to do so by your professor. Should you need to make a phone  call or send a text message, please do so before or after class. If your texting during class  becomes a distraction, Professor Velazquez reserves the right to ask you to leave the classroom for  the remainder of the lecture to ensure a distraction free learning environment for your peers. 
                    """)
    with st.expander("Class Recording"):
        st.markdown("""You may not record, videotape, or photograph during class without prior written consent  of faculty and/or students. This includes recording of lectures and photographs of slides  or presentations. Please see https://sites.sju.edu/atdl/dev-intellectual-property-rights/ for  information regarding intellectual property rights and consent.
                    """)     
    with st.expander("Inclement Weather"):
        st.markdown("""Depending on weather conditions, if faced with unsafe travel conditions, SJU may delay our opening, in which case we will provide detailed instructions at https://www.sju.edu/status. Or, SJU may declare a virtual work and learn day.  The University will communicate this information through text, email, phone call, the website and SJU Safe. To ensure you are signed up for these notifications, download SJU Safe https://www.sju.edu/offices/student-life/public-safety/resources-services/safe-app and update your cell phone number in the Nest.
                    """)
    with st.expander("Asynchronous Learning"):
        st.markdown("""Classes will not meet face-to-face. Faculty will determine which virtual option will best meet instructional goals for each class — synchronous or asynchronous — and will be responsible for communicating through Canvas to students. Students should follow the guidance of their field placements, service learning and clinical sites regarding attendance.
                    """)
    with st.expander("Covid-19 Safety"):
        st.markdown("""We must work together to keep our community as safe and active as possible. Please review the current guidance and requirements on the Student Health Center website https://www.sju.edu/offices/student-life/student-health-center and know they are subject to change, particularly when recommended by the Philadelphia Department of Public Health (PDPH). While the COVID vaccine is not required, it is recommended that students, faculty and staff be up-to-date on their vaccine status as recommended by the CDC https://www.cdc.gov/coronavirus/2019-ncov/vaccines/stay-up-to-date.html .
                    """)
    with st.expander("Religious Accomodation"):
        st.markdown("""As a Jesuit, Catholic institution, days of religious observance may be noted on the course schedule as class not meeting. However, it is noted that not all students identify as Catholic or with similar Christian beliefs. In response, students may be granted excused absences from class or other organized activities or observance of religious holy days, unless the accommodation would create an undue hardship. Students must notify the instructor by the end of the first week of classes to discuss any conflicts that may require an absence. It is the student’s responsibility to arrange with the instructor in advance to make up any missed work or class material. For more information about religious accommodations, please contact the Office of Title IX & Equity Compliance at 610-660-1145 or titleix@sju.edu / bias@sju.edu. 
                    """)
    
    st.markdown("---")
    st.markdown("### Resources")
    with st.expander("Office of Learning Resources (OLR)"):
        st.markdown("""Want to strengthen your approach in this class or fine-tune your learning strategies?  The Saint Joseph’s University Office of Learning Resources (OLR) empowers students to make a smooth transition to the university and to hone their skills in order to study more efficiently and effectively. For course-based support, they offer undergraduate-level peer tutoring in a wide range of subjects.  If you are an undergraduate or graduate student seeking to strengthen your learning strategies (time management, textbook reading, test taking, etc.), they offer one-on-one appointments with professional staff members.  Most services are free, unless otherwise noted, and online students may access services via Zoom. The OLR is located in Bellarmine G10.  For more information or to make an appointment, please visit their website at https://www.sju.edu/offices/student-life/learning-resources. 
                    """)
    with st.expander("Writing Center"):
        st.markdown("""The Saint Joseph’s University Writing Center is free to all members of the SJU community. The undergraduate and graduate student writers who make up the staff can assist you in any stage of the writing process, from brainstorming to organizing and developing your ideas, to citing sources to proofreading. They work with writers from across the university on a variety of assignments and individual and group projects: lab reports, business policy papers, poems, essays, research papers, dissertations, resumes, and personal statements for graduate school applications, among many others. You name it; they’ve helped writers write it.

Both in-person (Hawk Hill and UCity campuses) and synchronous online [appointments](https://sju.mywconline.com/schedule/calendar) (all three campuses) are offered any time the Writing Center is open. Asynchronous eTutoring appointments, with a 24-hour turnaround time for feedback, are also available to writers at all three campuses for assignments that are seven pages or fewer. Writers who wish to work with the same tutor at the same time/day throughout the semester can also sign up for the [Writing Partnership Program](https://sites.sju.edu/writingcenter/how-our-tutorials-work/writing-partnership-program/). For more information, including hours of operation, instructions on how to make an appointment, and other workshops and events, please visit the SJU Writing Center website at [sju.edu/writingcenter](http://sju.edu/writingcenter) or follow them on Instagram @sjuwrites.
                    """)
    with st.expander("Students with Disabilities (SDS)"):
        st.markdown("""Reasonable academic accommodations may be provided to students who submit appropriate documentation of their disability. If students have need of assistance or questions with this issue, they  are encouraged to contact the Office of Student Disability Services (SDS) at sds@sju.edu or by phone at 610.660.1774. The Office of SDS also provides an appeal/grievance procedure for complaints regarding requested or offered reasonable accommodations.  More information can be found at: www.sju.edu/sds
                    """)
    with st.expander("Bias, Discrimination & Harassment"):
        st.markdown("""As a Catholic, Jesuit University, Saint Joseph’s is committed to providing a workplace and educational environment, as well as other benefits, programs, and activities, that are free from acts of bias, discrimination, harassment, including acts of sexual harassment, sexual assault, dating and domestic violence, and stalking. We encourage anyone who has experienced this type of harm to seek help from the University by filing a report through the [incident reporting form](https://ssb.sju.edu/pls/PRODSSB/bzgkrpfr.P_DPBRP_Display), or by calling 610-660-1145.

For information about the University’s response to reports of bias, harassment, and discrimination, including definitions of prohibited conduct, information regarding confidential reporting options on- and off-campus, and resources for support, please visit https://www.sju.edu/offices/titleix-equity or contact [titleix@sju.edu](mailto:titleix@sju.edu) [/ bias@sju.edu](http://sju.edu/bias@sju.edu).

While I want you to feel comfortable coming to me for support, please know that I have some reporting requirements that are part of my job responsibilities at Saint Joseph’s University. For example, I am required to report any student disclosures of bias, discrimination, and harassment. I will keep the information as private as I can, but I am required to bring it to the attention of the institution’s Director Office of Title IX, Equity & Compliance.
                    """)
    with st.expander("Food & Basic Needs"):
        st.markdown("""Saint Joseph’s University recognizes that not all students may have access to adequate resources to meet commonplace or basic needs. If at any point in the semester you find that your academic performance or overall wellbeing is negatively affected by challenges related to access to class materials, technology, food or basic needs (e.g., skipped meals and/or unable to buy groceries, etc.), [please complete this form](https://forms.sju.edu/studentsuccess/view.php?id=110416), which will be sent to the Office of Student Success. A staff member will work with you to connect you with University and/or other resources.  For support with food and basic needs, you are encouraged to visit [HawkHUB](https://clubs.sju.edu/hawkhubclub/) in person or submit an online order.

Finally, you are welcome to contact me to discuss specific ways in which I can support you.  I am committed to helping you succeed.
                    """)
    with st.expander("Health & Wellbeing"):
        st.markdown("""Saint Joseph's University recognizes that one’s health and well-being strongly impact one's ability to do well in school and in life. As a result, there are many helpful campus resources designed to help students care for themselves in a holistic way. Students may experience stressors that can impact both their academic experience and their personal well-being. These may include academic pressure and challenges associated with relationships, mental health, alcohol or other drugs, identities, finances, etc. All of us benefit from support during times of struggle and challenges. If you are experiencing concerns, seeking assistance sooner rather than later is a courageous thing to do for yourself and those who care about you. Visit https://www.sju.edu/offices/student-life/wellbeing to learn more about the Nine Dimensions of Well-being (physical, emotional, intellectual, occupational, social, cultural, environmental, spiritual, and financial).  The resources below can help you to cope with stress and to achieve your academic and personal goals.
                    """)
    with st.expander("Counseling and Psychological Services (CAPS)"):
        st.markdown("""provides free and confidential mental health counseling for all full-time, degree-seeking Saint Joseph’s University students at Hawk Hill and University City. Additionally, brief consultation and referral support is provided for part-time students at Hawk Hill and University City, and also for all students enrolled at the Lancaster location. CAPS therapists are available for goal-focused individual and group counseling services; for consultation with faculty, staff, and other students; for outreach programming; and for mental health emergencies. To access services or for more information, please call CAPS on Hawk Hill (610-660-1090) or University City (215-596-8536) Monday through Friday between 8:30 am - 4:30 pm. For access to services at Lancaster, please email [CAPS_L@sju.edu](mailto:CAPS_L@sju.edu).

In addition to CAPS daytime services, counselors are available after office hours, on weekends, and during holidays to attend to emergency mental health concerns for Hawk Hill and University City students. To access emergency on-call services, Hawk Hill or University City students should call either of the CAPS phone numbers listed above and select option "2" when prompted. Lancaster students should call the Lancaster County Crisis Intervention Team at 717-394-2631, or dial 9-1-1. Please visit the CAPS website at [sju.edu/caps](http://sju.edu/caps) for more information.

Behavioral health is a key part of your overall well-being. A brief screening is the quickest way to determine if you should connect with a behavioral health professional. CAPS offers the CCAPS-Screen, an anonymous mental health screening instrument that assesses some of the most common psychological problems experienced by college students. To complete the screening, visit the [SJU CCAPS-Screen website](https://ccmh-s.psu.edu/ccaps-web/Csp/006ea35e5e2840beb7b8b4878e89d7b3).
                    """)
    with st.expander("Additional Wellbeing Resources"):
        st.markdown("""- Student Health Center: [https://www.sju.edu/studenthealth](https://www.sju.edu/offices/student-life/student-health-center)
- Student Support & Well-being: [sju.edu/sos](http://sju.edu/sos)
- Student Success: https://sites.sju.edu/thesuccesscenter/student-success/
- Fitness & Recreation: https://www.sju.edu/health-well-being/fitness-recreation
- Center for Inclusion and Diversity: https://sites.sju.edu/oid/
- Campus Ministry: https://sites.sju.edu/campusministry/
- SJU’s [Collegiate Recovery Program](https://www.sju.edu/CRP) is a supportive, inclusive community for students in recovery from Substance Use Disorder (SUD). The CRP also offers a space for Allies of Recovery to collaborate in breaking the stigma around SUD and to create a recovery friendly campus community. All are welcome and encouraged to inquire about the CRP, especially those who are in recovery from SUD, have been affected by SUD, or are looking to explore their behaviors/relationship with substances. The CRP offers a community space and Recovery Residence, an on-campus housing option for those in recovery from SUD who prefer to live in an abstinence based community environment. For more information, contact [recovery@sju.edu](mailto:recovery@sju.edu) or visit [sju.edu/CRP](http://sju.edu/CRP). 
                    """)
