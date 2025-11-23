# modules_data.py

MICRO_MODULES = [
    {
    "id": 1,
    "title": "Economic Thought and Modeling",
    "short_desc": "Scarcity, opportunity cost, and the basic models economists use to represent choice.",

    "overview_intuition": """
### Overview & Intuition

In this first module, we explore how economists think about the world and how they turn real choices into models.

We begin with **economic thought**: three core principles — scarcity, rational choice, and marginal analysis — and how they emerge from broader philosophical and historical debates about human behavior and resources.

We then move into **economic modeling**, using two foundational tools:

- the **budget constraint** to represent how an individual makes decisions under income constraints, and  
- the **Production Possibilities Curve (PPC)** to represent how producers and societies face tradeoffs and opportunity cost.

Finally, we use the PPCs of two countries to explore **comparative advantage** and think about how trade and marginal analysis can increase total production and growth over time.
""",

    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Scarcity**, **rational choice**, and **marginal analysis**  
- **Opportunity cost** and **tradeoffs**  
- **Budget constraint** and its key components  
- **Production Possibilities Curve (PPC)** and points on/inside/outside the curve  
- **Comparative advantage** vs. absolute advantage  
""",

    "tier2_solid": """
### Tier 2 — Solid Understanding (Assessment Tier)

By the end of Tier 2, you should be able to:

- Use course resources (syllabus, models, guided notes, labs) to meet expectations  
- Identify examples of scarcity, rational choice, and marginal analysis  
- Develop and interpret a **budget constraint**  
- Develop and interpret a **PPC** and calculate opportunity costs  
- Analyze two-country PPCs to determine comparative advantage  
- Explain how specialization and trade increase total production  
""",

    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

If you choose to explore Tier 3, you will:

- Trace the **philosophical origins** of scarcity and rational choice  
- Explore how economics became an academic discipline  
- Compare PPC and budget constraints as models of tradeoffs  
- Reflect on a historical case using opportunity cost & comparative advantage  
""",

    "materials": {
        "slides": "https://www.canva.com/design/DAGwfT91g1g/OdJml0o6MBrAhTj7OZbYCQ/view",
        "guided_notes": "https://www.canva.com/design/DAGkcbYfGCc/xhA7l6r-7u9gMBwsU6czsQ/edit",

        "labs": [
            {
                "label": "Lab 1 — Economic Theory: Before the Wealth of Nations",
                "url": "https://www.notion.so/Economic-Theory-Before-the-Wealth-of-Nations-2b04371a58ce817a880ffdf96c278b25?pvs=21"
            }
        ],

        "models": [
            {"label": "Budget Constraint Model", "url": "https://velazquez.streamlit.app/?page=Budget%20Constraint"},
            {"label": "PPC Model", "url": "https://velazquez.streamlit.app/?page=PPC"},
            {"label": "Comparative Advantage", "url": "https://velazquez.streamlit.app/?page=Comparative%20Advantage"},
        ],

        "khan": [],
        "videos": [],
        "audio": []
    },
},
{
    "id": 2,
    "title": "Supply & Demand",
    "short_desc": "How buyers and sellers interact to determine prices, quantities, and responses to shocks.",

    "overview_intuition": """
### Overview & Intuition

In this module, we study how markets bring buyers and sellers together.

We begin with **demand**, shaped by income, preferences, and related goods.

We then develop **supply**, representing producers’ willingness to sell at various prices.

Where these two forces meet, we find the **equilibrium price and quantity**.

Finally, we examine **market shocks** (e.g., income, technology, input costs) and **government interventions** (price ceilings and floors) to understand how institutional rules shape market outcomes.
""",

    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Demand** and the **Law of Demand**  
- **Supply** and the **Law of Supply**  
- **Quantity demanded vs. demand**  
- **Quantity supplied vs. supply**  
- **Normal** vs. **inferior** goods  
- **Substitutes** vs. **complements**  
- **Market equilibrium**  
- **Shortage** and **surplus**  
- **Shifts** vs. **movements along curves**
""",

    "tier2_solid": """
### Tier 2 — Solid Understanding (Assessment Tier)

By the end of Tier 2, you should be able to:

- Graph supply and demand curves from schedules  
- Distinguish between **shifts** and **movements along** curves  
- Determine equilibrium price and quantity  
- Predict the effects of:
  - income changes  
  - related goods prices  
  - technology  
  - input costs  
  - number of buyers/sellers  
- Analyze market adjustments when out of equilibrium  
- Evaluate the effects of **ceilings** and **floors** on price and quantity  
""",

    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

If you choose to explore Tier 3, you will:

- Investigate how shocks propagate across markets  
- Explore elasticity conceptually and intuitively  
- Examine short historical examples of markets adjusting over time  
- Reflect on institutional or social constraints that alter market outcomes  
- Compare equilibrium to decentralized coordination mechanisms  
""",

    "materials": {
        "slides": "https://www.canva.com/design/DAGwfg6_fC4/G92LFFFXnjivu2rtuX6JhA/view",
        "guided_notes": "https://www.canva.com/design/DAGkceAqddU/ycnKcBnBvTaC-VPFTr6-0A/edit",

        "labs": [
            {
                "label": "Supply & Demand Lab",
                "url": "https://www.notion.so/Supply-and-Demand-Lab-e73b6326ebb24d48bb031bdd1978f8bb?pvs=21"
            }
        ],

        "models": [
            {"label": "Demand (Schedule → Curve)", "url": "https://velazquez.streamlit.app/?page=Demand%20(schedule%20%E2%86%92%20line)"},
            {"label": "Supply (Schedule → Curve)", "url": "https://velazquez.streamlit.app/?page=Supply%20(schedule%20%E2%86%92%20line)"},
            {"label": "Market Model", "url": "https://velazquez.streamlit.app/?page=Market%20Model%20(Supply%20%26%20Demand)"},
            {"label": "Single Shifts", "url": "https://velazquez.streamlit.app/?page=Single%20Shifts"},
            {"label": "Double Shifts", "url": "https://velazquez.streamlit.app/?page=Double%20Shifts"},
        ],

        "khan": [
            {
                "label": "Khan Academy: Supply and Demand Basics",
                "url": "https://www.khanacademy.org/economics-finance-domain/microeconomics/supply-demand-equilibrium"
            }
        ],

        "videos": [],
        "audio": []
    },
},
# --- MODULE 3: Elasticity ---
{
    "id": 3,
    "title": "Elasticity",
    "short_desc": "Responsiveness of consumers and producers to price changes.",
    "overview_intuition": "### Overview & Intuition\n_Coming soon._",
    "tier1_definitions": "### Tier 1 — Formal Definitions\n_Coming soon._",
    "tier2_solid": "### Tier 2 — Solid Understanding (Assessment Tier)\n_Coming soon._",
    "tier3_extensions": "### Tier 3 — Extensions (Optional)\n_Coming soon._",
    "materials": {},
},

# --- MODULE 4: Welfare Economic & Government Intervention ---
{
    "id": 4,
    "title": "Welfare Economics and Government Intervention",
    "short_desc": "Consumer/producer surplus and the effects of taxes, price controls, and policies.",
    "overview_intuition": "### Overview & Intuition\n_Coming soon._",
    "tier1_definitions": "### Tier 1 — Formal Definitions\n_Coming soon._",
    "tier2_solid": "### Tier 2 — Solid Understanding\n_Coming soon._",
    "tier3_extensions": "### Tier 3 — Extensions (Optional)\n_Coming soon._",
    "materials": {},
},

# --- MODULE 5: Factors of Production ---
{
    "id": 5,
    "title": "Factors of Production ",
    "short_desc": "Land, labor, capital, and interdependencies across factor markets.",
    "overview_intuition": "### Overview & Intuition\n_Coming soon._",
    "tier1_definitions": "### Tier 1 — Formal Definitions\n_Coming soon._",
    "tier2_solid": "### Tier 2 — Solid Understanding\n_Coming soon._",
    "tier3_extensions": "### Tier 3 — Extensions (Optional)\n_Coming soon._",
    "materials": {},
},

# --- MODULE 6: Choice ---
{
    "id": 6,
    "title": "Choice (*Asynchronous Alternative*)",
    "short_desc": "Preferences, utility, and optimal bundles.",
    "overview_intuition": "### Overview & Intuition\n_Coming soon._",
    "tier1_definitions": "### Tier 1 — Formal Definitions\n_Coming soon._",
    "tier2_solid": "### Tier 2 — Solid Understanding\n_Coming soon._",
    "tier3_extensions": "### Tier 3 — Extensions (Optional)\n_Coming soon._",
    "materials": {},
},

# --- MODULE 7: Capitilism (UNTIERED) ---
{
    "id": 7,
    "title": "*Capitilism* (*Optional Full-Group Extension*)",
    "short_desc": "Capitlism Today using corECON.",
    "is_untiered": True,
    "untiered_markdown": "## Module 7 — Capitilism\n_Coming soon._",
    "materials": {}
},

# --- MODULE 8: Inequality (UNTIERED) ---
{
    "id": 8,
    "title": "*Inequality* (*Optional Independent Extension*)",
    "short_desc": "The distribution of income and wealth.",
    "is_untiered": True,
    "untiered_markdown": "## Module 8 — Inequality\n_Coming soon._",
    "materials": {},
},

# --- MODULE 9: Cost of Production ---
{
    "id": 9,
    "title": "Cost of Production",
    "short_desc": "Strategic interaction and equilibrium.",
    "overview_intuition": "### Overview & Intuition\n_Coming soon._",
    "tier1_definitions": "### Tier 1 — Formal Definitions\n_Coming soon._",
    "tier2_solid": "### Tier 2 — Solid Understanding\n_Coming soon._",
    "tier3_extensions": "### Tier 3 — Extensions\n_Coming soon._",
    "materials": {},
},

# --- MODULE 10: Profit Maximization ---
{
    "id": 10,
    "title": "Profit Maximization",
    "short_desc": "When markets fail and how societies respond.",
    "overview_intuition": "### Overview & Intuition\n_Coming soon._",
    "tier1_definitions": "### Tier 1 — Formal Definitions\n_Coming soon._",
    "tier2_solid": "### Tier 2 — Solid Understanding\n_Coming soon._",
    "tier3_extensions": "### Tier 3 — Extensions\n_Coming soon._",
    "materials": {},
},

# --- MODULE 11: Competition & Asymmetric Information ---
{
    "id": 11,
    "title": "Competition & Asymmetric Information",
    "short_desc": "Monopoly, oligopoly, and market power.",
    "overview_intuition": "### Overview & Intuition\n_Coming soon._",
    "tier1_definitions": "### Tier 1 — Formal Definitions\n_Coming soon._",
    "tier2_solid": "### Tier 2 — Solid Understanding\n_Coming soon._",
    "tier3_extensions": "### Tier 3 — Extensions\n_Coming soon._",
    "materials": {},
},

# --- MODULE 12: Micro-Policy ---
{
    "id": 12,
    "title": "Micro-Policy",
    "short_desc": "Externalities, public goods, and how policy fixes market misfires.",
    "overview_intuition": """
### Overview & Intuition

Markets can miss the social sweet spot when spillover costs or benefits aren’t priced in. In plain language—no math or graphs—we’ll see why externalities arise, why some goods (parks, education, roads, fisheries) struggle without rules, and what governments try to correct with taxes, subsidies, and regulation.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

- **Private goods**, **public goods**, **common resources**, **club goods**
- **Rivalry**, **excludability**, **free rider problem**, **tragedy of the commons**
- **Externality**, **negative externality**, **positive externality**, **social marginal cost**, **social marginal benefit**
- **Taxes**, **subsidies**, and market-correcting policy for externalities
- **Tax incidence** (conceptual; introduced here only)
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding (Assessment Tier)

- Model negative externalities as a leftward shift of supply (social cost)
- Model positive externalities as a rightward shift of demand (social benefit)
- Locate market vs. socially optimal equilibria on a graph
- Calculate and interpret deadweight loss from externalities
- Show how **Pigouvian taxes/subsidies** shift supply or demand
- Analyze **tax incidence** graphically (first and only appearance)
- Connect incidence to elasticity intuitively
- Use simple game theory (dominant strategies, incentives) to interpret policy setups
- Conduct structured cost–benefit analysis on a public policy case
- Apply full micro reasoning (S&D, externalities, incentives, equilibrium, welfare) to a real policy decision
""",
    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

- Historical, political, and institutional paths to public or regulated goods
- Behavioral reasons for under- or over-consumption with externalities
- Modern digital externalities (network effects, platforms)
- Links from policy to long-run inequality, education, and mobility
""",
    "materials": {},
},
]
