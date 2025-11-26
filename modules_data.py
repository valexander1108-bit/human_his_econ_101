# modules_data.py
import csv
import re
from pathlib import Path

from data.openstax_plan import MODULE_OPENSTAX_MAP, OPENSTAX_CHAPTERS
from data.canonical_texts import CANONICAL_TEXTS, MODULE_CANONICAL_MAP

MICRO_MODULES = [
{
    "id": 1,
    "title": "Economic Thought & Modeling",
    "short_desc": "Scarcity, opportunity cost, and the basic models economists use to represent choice.",

    "overview_intuition": """
### Module 1 Learning

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
        "readings": [],
        "extensions": [],

        "models": [
            {"label": "Budget Constraint", "url": "?model=Budget%20Constraint"},
            {"label": "PPC", "url": "?model=PPC"},
            {"label": "Comparative Advantage", "url": "?model=Comparative%20Advantage"},
        ],

        "khan": [
            {
                "label": "Kahn - Quiz 1 - Basic Economic Concepts - Scarcity & Econ Systems",
                "url": "https://www.khanacademy.org/economics-finance-domain/ap-microeconomics/basic-economic-concepts/resource-allocation-and-economic-systems/quiz/basic-economic-concepts-quiz-1"
            },
            {
                "label": "Kahn - Quiz 2 - Basic Economic Concepts - PPC and Trade",
                "url": "https://www.khanacademy.org/economics-finance-domain/ap-microeconomics/basic-economic-concepts/comparative-advantage-and-trade/quiz/basic-economic-concepts-quiz-2"
            },
            {
                "label": "Kahn - Quiz 3 - Basic Economic Concepts - Cost-Benefit Analysis (Utility) ",
                "url": "https://www.khanacademy.org/economics-finance-domain/ap-microeconomics/basic-economic-concepts/16/quiz/basic-economic-concepts-quiz-3"
            },

            
        ],
        "videos": [],
        "audio": []
    },
},
{
    "id": 2,
    "title": "Supply & Demand",
    "short_desc": "How buyers and sellers interact to determine prices, quantities, and responses to shocks.",

    "overview_intuition": """
### Module 2 Learning

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
        "slides": "https://www.canva.com/design/DAGu3QAnbyo/X4tBmSFNVLX_Wjotx8TuKg/view?utm_content=DAGu3QAnbyo&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h17f367ac75",
        "guided_notes": "https://www.canva.com/design/DAGxSH8hCHk/I2kj289MFKsKjWqFfBHeUA/view?utm_content=DAGxSH8hCHk&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hb3c9693bc0",

        "labs": [
            {
                "label": "Supply & Demand Lab",
                "url": "https://www.notion.so/Supply-and-Demand-Lab-e73b6326ebb24d48bb031bdd1978f8bb?pvs=21"
            }
        ],
        "readings": [
            {
                "label": "OpenStax — Principles of Microeconomics 3e (relevant section)",
                "url": "https://openstax.org/books/principles-microeconomics-3e/pages/2-3-confronting-objections-to-the-economic-approach"
            }
        ],
        "extensions": [],

        "models": [
            {"label": "Demand (schedule → line)", "url": "?model=Demand%20(schedule%20%E2%86%92%20line)"},
            {"label": "Supply (schedule → line)", "url": "?model=Supply%20(schedule%20%E2%86%92%20line)"},
            {"label": "Market Model (Supply & Demand)", "url": "?model=Market%20Model%20(Supply%20%26%20Demand)"},
            {"label": "Single Shifts", "url": "?model=Single%20Shifts"},
            {"label": "Double Shifts", "url": "?model=Double%20Shifts"},
        ],

        "khan": [],

        "videos": [],
        "audio": []
    },
},
# --- MODULE 3: Elasticity ---
{
    "id": 3,
    "title": "Elasticity",
    "short_desc": "Responsiveness of consumers and producers to price changes.",
    "overview_intuition": """
### Module 3 Learning

In this module, we ask how sensitive buyers and sellers are to price changes and why it matters for revenue, policy, and growth.

We start with **price elasticity of demand** to classify goods as elastic, inelastic, unit elastic, or perfectly elastic/inelastic. We connect elasticity to **total revenue**, substitutes/complements, and normal/inferior goods to see how firms and policymakers anticipate behavior.

We then turn to **elasticity of supply**, highlighting time horizons and capacity constraints as drivers of responsiveness. Throughout, we anchor the math in real-life cases (gas, luxury goods, apps) and show how elasticity shapes who bears taxes, how markets adjust, and which goods boom or stagnate as economies grow.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Price elasticity of demand** (midpoint formula); **elastic**, **inelastic**, **unit elastic**, **perfectly elastic/inelastic**
- **Total revenue** and the **revenue test**
- **Cross-price elasticity** (substitutes vs. complements) and **income elasticity** (normal vs. inferior/luxury)
- **Price elasticity of supply** and key determinants (time, capacity, inputs)
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding (Assessment Tier)

By the end of Tier 2, you should be able to:

- Calculate price elasticity of demand/supply with the midpoint method and classify goods
- Use elasticity to predict **total revenue** changes from price moves
- Interpret **cross-price** and **income** elasticities to label relationships and normal/inferior goods
- Explain how time horizons shift supply and demand elasticities
- Apply elasticity logic to policy: who bears a tax/subsidy burden when curves are steep vs. flat
- Map elasticity concepts onto real markets (necessities vs. luxuries, apps vs. commodities)
""",
    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

- Explore common functional forms (constant elasticity, log-log) and growth implications
- Connect elasticity to market power and pricing strategy (markup rules)
- Examine long-run vs. short-run elasticity differences in environmental or labor markets
 - Analyze historical cases where changing elasticities reshaped industries
""",
    "materials": {
        "models": [
            {"label": "Price Elasticity of Demand", "url": "?model=Price%20Elasticity%20of%20Demand"},
            {"label": "Elasticity and Total Revenue", "url": "?model=Elasticity%20and%20Total%20Revenue"},
            {"label": "Price Elasticity of Supply", "url": "?model=Price%20Elasticity%20of%20Supply"},
        ],
        "readings": [
            {
                "label": "OpenStax — Principles of Microeconomics 3e (relevant section)",
                "url": "https://openstax.org/books/principles-microeconomics-3e/pages/2-3-confronting-objections-to-the-economic-approach"
            }
        ],
        "extensions": [],
        "labs": [],
        "khan": [],
        "videos": [],
        "audio": [],
    },
},

# --- MODULE 4: Welfare Economic & Government Intervention ---
{
    "id": 4,
    "title": "Welfare & Intervention",
    "short_desc": "Consumer/producer surplus and the effects of taxes, price controls, and policies.",
    "overview_intuition": """
### Module 4 Learning

Here we measure who benefits in a market and what happens when policy steps in.

We begin with **consumer and producer surplus** to see how equilibrium maximizes total surplus. Then we test **price controls** (floors and ceilings) and **taxes** to trace shortages, surpluses, and deadweight loss.

Finally, we connect efficiency to equity and preview how market rules shape winners, losers, and incentives.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Consumer surplus (CS)**, **producer surplus (PS)**, **total surplus**
- **Efficiency** vs. **deadweight loss (DWL)**
- **Price ceiling**, **price floor**, **tax**, **subsidy**
- **Tax incidence** (conceptual) and how it links to elasticity
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding

By the end of Tier 2, you should be able to:

- Compute CS, PS, and total surplus from a demand/supply graph
- Show how ceilings and floors create shortages/surpluses and measure resulting DWL
- Graph the effects of a per-unit tax or subsidy on equilibrium, surplus, and DWL
- Explain who bears a tax given different elasticities (qualitative incidence)
- Use a market model to judge when interventions help or hurt overall welfare
""",
    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

 - Explore surplus changes when demand or supply shifts over time
 - Analyze tax incidence quantitatively using elasticity formulas
 - Discuss equity-efficiency tradeoffs and the ethics of redistribution via market policy
 - Connect welfare analysis to real policies (rent control, minimum wage, sin taxes)
""",
    "materials": {
        "models": [
            {"label": "Surplus", "url": "?model=Surplus"},
            {"label": "Government Intervention: Price Floor", "url": "?model=Government%20Intervention:%20Price%20Floor"},
            {"label": "Government Intervention: Price Ceiling", "url": "?model=Government%20Intervention:%20Price%20Ceiling"},
            {"label": "Deadweight Loss", "url": "?model=Deadweight%20Loss"},
        ],
        "readings": [],
        "extensions": [],
        "labs": [],
        "khan": [],
        "videos": [],
        "audio": [],
    },
},

# --- MODULE 5: Factors of Production ---
{
    "id": 5,
    "title": "Factors of Production ",
    "short_desc": "Land, labor, capital, and interdependencies across factor markets.",
    "overview_intuition": """
### Module 5 Learning

This module shifts from goods markets to the markets for **land, labor, and capital**—the inputs that make production possible.

We start with the **Neoclassical view of income distribution**, where factor prices come from marginal productivity. We build supply and demand stories for **capital (credit/interest)** and **land (rents)**, then turn to **labor** to see how wages emerge and what shifts labor supply and demand.

Throughout, we use marginal analysis to link firm choices to factor demand and explore how shocks to one factor market spill into others.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Factors of production**: land, labor, capital
- **Derived demand**, **marginal product (MP)**, **marginal revenue product / value of marginal product (MRP/VMP)**
- **Economic rent**, **interest rate**, **wage**
- **Elasticity** in factor markets and determinants of factor supply/demand
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding

By the end of Tier 2, you should be able to:

- Model supply and demand for **capital** and analyze floors/ceilings on interest rates
- Model supply and demand for **land** and discuss inelastic land supply over time
- Build and interpret a **labor market** graph; identify shifts in labor supply and demand
- Use **marginal analysis** (MRP = wage) to derive a firm’s labor demand
- Explain how shocks in one factor market affect others (e.g., capital deepening on wages)
""",
    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

- Examine historical cases of inelastic land supply and rent dynamics
- Explore capital-labor substitution, automation, and implications for wages
- Consider monopsony/union power and policy levers in factor markets
 - Discuss global factor mobility and distributional consequences
""",
    "materials": {
        "models": [
            {"label": "Interdependent Factors", "url": "?model=Interdependent%20Factors"},
            {"label": "Land + Rent", "url": "?model=Land%20+%20Rent"},
            {"label": "Labor + Wage", "url": "?model=Labor%20+%20Wage"},
            {"label": "Capital + Interest", "url": "?model=Capital%20+%20Interest"},
        ],
        "readings": [],
        "extensions": [],
        "labs": [],
        "khan": [],
        "videos": [],
        "audio": [],
    },
},

# --- MODULE 6: Choice ---
{
    "id": 6,
    "title": "Choice & Constraint (*Asynchronous*)",
    "short_desc": "Preferences, utility, and optimal bundles.",
    "overview_intuition": """
### Module 6 Learning

This asynchronous module zooms in on individual choice—how people rank bundles, trade off time and money, and make decisions across today and tomorrow.

We start with **utility and diminishing marginal utility** to see why variety matters. We map **budget constraints** against **indifference curves** to find optimal consumption. Then we extend the same logic to **labor vs. leisure** and **intertemporal choice** (borrowing/lending over time).

Finally, we confront **bounded rationality** and behavioral limits to the tidy model, asking how real people depart from perfect optimization.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Utility**, **marginal utility**, **diminishing marginal utility**
- **Indifference curve**, **marginal rate of substitution (MRS)**
- **Budget constraint**, **feasible set** (work vs. free time), **optimal bundle**
- **Intertemporal budget**, **interest rate**, **present value**
- **Bounded rationality** and common behavioral limits
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding

By the end of Tier 2, you should be able to:

- Draw a budget line with indifference curves and locate the tangency optimal bundle
- Build a labor–leisure feasible set and show how wages shift the work/consumption choice
- Trace the effects of an interest rate change on borrowing/lending in an intertemporal model
- Use marginal analysis (MU per dollar) to justify optimal consumption choices
- Apply the choice toolkit to real decisions (saving, studying, working hours)
""",
    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

- Explore behavioral models: heuristics, present bias, and time-inconsistent preferences
- Compare exponential vs. hyperbolic discounting in intertemporal choice
- Discuss revealed preference and how data uncovers underlying utility
- Analyze policy nudges aimed at bounded rational decision makers
""",
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
    "overview_intuition": """
### Module 9 Learning

We move inside the firm to link production, costs, and profits.

First, we separate **accounting profit** from **economic profit** and map how different market structures shape firm choices. We study **short-run production** (total, average, marginal product) and translate inputs into costs.

Then we build the **short-run cost curves** (TC, FC, VC, MC, ATC, AVC) and explore how scale and technology drive costs down or up. Real examples and a manager’s perspective ground the theory in organizational choices.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Accounting profit** vs. **economic profit**
- **Total/average/marginal product**, **diminishing marginal returns**
- **Total cost (TC)**, **fixed vs. variable cost (FC/VC)**, **ATC**, **AVC**, **MC**
- **Economies of scale**, **short run** vs. **long run**
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding

By the end of Tier 2, you should be able to:

- Classify profits as accounting vs. economic in sample problems
- Compute and interpret TP, AP, MP; connect diminishing returns to rising MC
- Derive MC, ATC, and AVC from cost data and explain their shapes
- Identify economies/diseconomies of scale and short-run vs. long-run cost differences
- Relate market structure (perfect competition vs. other forms) to cost and output choices
""",
    "tier3_extensions": """
### Tier 3 — Extensions

- Analyze learning curves and technological change on long-run costs
- Discuss sunk costs and real-world managerial decision pitfalls
- Explore links between cost structure and market entry/exit dynamics
""",
    "materials": {},
},

# --- MODULE 10: Profit Maximization ---
{
    "id": 10,
    "title": "Profit Maximization",
    "short_desc": "When markets fail and how societies respond.",
    "overview_intuition": """
### Module 10 Learning

Now we pair cost with revenue to choose output levels in different market structures.

We begin with **perfect competition**, using marginal analysis (MR = MC) to pick short-run output and decide when to shut down or exit long run. Then we repeat the exercise for **monopoly**, comparing pricing, output, and welfare to the competitive benchmark.

The goal: a clear playbook for firm behavior across market types and a lens on why market power creates inefficiency.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Perfect competition**, **monopoly**
- **Total revenue (TR)**, **marginal revenue (MR)**, **marginal cost (MC)**, **average variable cost (AVC)**
- **Profit-maximizing rule** (MR = MC) and **shutdown rule** (P < AVC in short run)
- **Long-run entry/exit** in perfect competition; monopoly pricing via the demand curve
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding

By the end of Tier 2, you should be able to:

- Given cost/revenue data, find the **profit-maximizing quantity and price** in perfect competition
- Identify profits/losses and apply shutdown vs. continue in the short run; predict long-run entry/exit
- For a monopoly, derive MR from demand, set MR = MC, and find the profit-maximizing price/quantity
- Compare efficiency: show monopoly DWL relative to perfect competition
- Use marginal analysis graphs to justify each decision rule
""",
    "tier3_extensions": """
### Tier 3 — Extensions

- Explore price discrimination types and effects on output and surplus
- Examine natural monopoly logic and regulatory options
- Discuss contestable markets and strategic pricing to deter entry
""",
    "materials": {},
},

# --- MODULE 11: Competition & Asymmetric Information ---
{
    "id": 11,
    "title": "Competition & Information",
    "short_desc": "Monopoly, oligopoly, and market power.",
    "overview_intuition": """
### Module 11 Learning

We extend beyond perfect competition and monopoly to the messy middle: **oligopoly** and **monopolistic competition**, plus the role of information.

We learn basic **game theory** (prisoner’s dilemma, dominant strategies, Nash equilibrium) to model strategic interaction among a few firms. We contrast that with many firms selling differentiated products in **monopolistic competition**, focusing on pricing, variety, and excess capacity. We close with policy and a hands-on business lab to apply the models.
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Oligopoly**, **monopolistic competition**, **product differentiation**
- **Payoff matrix**, **dominant strategy**, **Nash equilibrium**, **prisoner’s dilemma**
- **Cartel/collusion**, **antitrust** (conceptual)
- **Excess capacity** and long-run outcomes in monopolistic competition
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding

By the end of Tier 2, you should be able to:

- Solve simple payoff matrices to find dominant strategies and Nash equilibria
- Use game-theory logic to explain oligopoly pricing/quantity outcomes and incentives to collude/cheat
- Graph monopolistic competition in short run vs. long run (profits → entry → zero economic profit with variety)
- Compare efficiency and consumer outcomes across perfect competition, monopolistic competition, oligopoly, and monopoly
- Identify where policy (antitrust, regulation) enters to address market power
""",
    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

- Explore repeated games, credible threats, and cooperation in oligopolies
- Introduce asymmetric information topics (adverse selection, moral hazard) as seeds for further study
- Analyze real-world antitrust cases and platform market power
- Build richer business-lab scenarios that blend differentiation, strategy, and information
""",
    "materials": {},
},

# --- MODULE 12: Policy, Paradox, & Human Perspective ---
{
    "id": 12,
    "title": "Policy, Paradox & Human Perspective ",
    "short_desc": "Externalities, public goods, and how policy fixes market misfires.",
    "overview_intuition": """
### Module 12 Learning

In this chapter, we think about the paradox of price and explore what happens when markets get prices wrong. We uncover how societies have intervened in their economic fates throughout history, and continue to address common economic contradictions today. 

First, we develop clear definitions for the **four types of goods** — private goods, club goods, common resources, and public goods — to see how rivalry and excludability shape incentives, cooperation problems, and more specifically - free riding and overuse.

Through forming an understanding of **externalities** as "missing prices": pollution that’s too cheap, education that’s underbought, or parks that are underfunded - we calculate and contrast market outcomes with socially efficienct outcomes, and measure the wedge between them to understand deadweight loss. 

Finally, we walk through the **policy toolkit** — Pigouvian taxes and subsidies, permits, regulations, and public provision. 

Along the way we peek at how elasticity influences **tax incidence** and who actually bears the tax burdens, while also exploring simple game-theory narratives to support our understanding of how rules, enforcement, and institutions coagulate within market outcomes.  
""",
    "tier1_definitions": """
### Tier 1 — Formal Definitions

By the end of Tier 1, you should be able to define:

- **Private goods**, **club goods**, **common resources**, **public goods**
- **Rivalry**, **excludability**, **free rider problem**, **tragedy of the commons**
- **Externality**, **negative/positive externality**, **marginal social cost (MSC)**, **marginal social benefit (MSB)**
- **Pigouvian tax**, **Pigouvian subsidy**, **tradable permit**, **command-and-control regulation**
- **Tax incidence** (conceptual) and how elasticity influences who pays
""",
    "tier2_solid": """
### Tier 2 — Solid Understanding (Assessment Tier)

By the end of Tier 2, you should be able to:

- Classify a real-world example into the four goods categories and predict incentive problems
- Graph and quantify **negative externalities** (supply with MSC) and **positive externalities** (demand with MSB)
- Identify market vs. socially optimal quantity/price and compute **deadweight loss**
- Design the **Pigouvian tax or subsidy** that closes the MSC–MPC or MSB–MPB gap
- Show **tax incidence** on a graph and explain how elasticity splits the burden
- Compare policy tools (tax, subsidy, permit, regulation, public provision) for efficiency and equity
- Use simple payoff matrices or dominant strategies to explain cooperation and enforcement challenges
- Run a basic **cost–benefit analysis** of a policy using the micro toolkit (S&D, externalities, incidence, welfare)
""",
    "tier3_extensions": """
### Tier 3 — Extensions (Optional)

- Derive Pigouvian tax/subsidy formulas from marginal benefit/cost schedules and elasticity
- Explore **Coasean bargaining** and transaction costs as alternative fixes to externalities
- Model repeated-game or dynamic versions of commons and public-goods problems
    - Trace political economy: who designs the policy, who captures the rents, and how institutions evolve
    - Analyze modern digital externalities (platforms, network effects, data privacy) and their normative tradeoffs
""",
    "materials": {
        "slides": "https://docs.google.com/presentation/d/1Uvmyw3XTlZEOnrqcMVwBTYPUu5DPrSwn/preview",
        "guided_notes": "https://www.canva.com/design/DAGj-XcXXCQ/HqFSA-Y9C1A6335ZWD98EQ/view?embed",
        "labs": [
            {
                "label": "Urban Micro-Policy Lab: Education Subsidies (Philadelphia)",
                "url": "https://shy-plane-8b3.notion.site/Urban-Micro-Policy-Lab-Education-Subsidies-in-Philadelphia-2b04371a58ce81549beec6cc94388503?source=copy_link"
            }
        ],
        "models": [
            {"label": "Externality: Social Cost (Pigouvian Tax)", "url": "?model=Externality:%20Social%20Cost%20(Pigouvian%20Tax)"},
            {"label": "Externality: Social Benefit (Pigouvian Subsidy)", "url": "?model=Externality:%20Social%20Benefit%20(Pigouvian%20Subsidy)"}
        ],
        "khan": [
            {
                "label": "Quiz 1 - Market Failure and the Role of Government - Externalities & Types of Goods ",
                "url": "https://www.khanacademy.org/economics-finance-domain/ap-microeconomics/ap-consumer-producer-surplus/public-and-private-goods/quiz/ap-consumer-producer-surplus-quiz-1"
            }
        ],
        "readings": [],
        "extensions": [],
        "videos": [],
        "audio": []
    },
},
]

# --- Link OpenStax chapters to modules (core + optional) ---
def _build_openstax_item(chapter_num: int):
    chapter = OPENSTAX_CHAPTERS.get(chapter_num)
    if not chapter:
        return None
    return {
        "chapter": chapter_num,
        "label": f"OpenStax Ch {chapter_num}: {chapter['title']}",
        "url": chapter["url"],
    }


_PLAN_BY_MODULE = {m["module"]: m for m in MODULE_OPENSTAX_MAP}

for module in MICRO_MODULES:
    mapping = _PLAN_BY_MODULE.get(module.get("id"))
    if not mapping:
        continue

    core_items = []
    optional_items = []

    for num in mapping.get("core_openstax", []):
        item = _build_openstax_item(num)
        if item:
            core_items.append(item)

    for num in mapping.get("optional_openstax", []):
        item = _build_openstax_item(num)
        if item:
            optional_items.append(item)

    if not core_items and not optional_items:
        continue

    module.setdefault("openstax", {})
    if core_items:
        module["openstax"]["core"] = core_items
    if optional_items:
        module["openstax"]["optional"] = optional_items

    # Put core OpenStax links into required readings (avoid duplicates)
    materials = module.setdefault("materials", {})
    existing_readings = materials.get("readings", [])
    seen_urls = {item["url"] for item in core_items}
    deduped_existing = [r for r in existing_readings if r.get("url") not in seen_urls]
    materials["readings"] = core_items + deduped_existing

# --- Link Primary/Canonical texts (classic + contemporary) to modules ---
def _build_canonical_item(key: str):
    item = CANONICAL_TEXTS.get(key)
    if not item:
        return None
    return {
        "label": item["label"],
        "url": item["url"],
        "era": item["era"],
        "tradition": item["tradition"],
        "note": item.get("note", ""),
    }


for module in MICRO_MODULES:
    keys = MODULE_CANONICAL_MAP.get(module.get("id"), [])
    if not keys:
        continue
    new_items = []
    for k in keys:
        built = _build_canonical_item(k)
        if built:
            new_items.append(built)
    if not new_items:
        continue

    materials = module.setdefault("materials", {})
    existing = materials.get("primary_texts", [])
    existing_urls = {itm.get("url") for itm in existing}
    merged = existing + [itm for itm in new_items if itm["url"] not in existing_urls]
    materials["primary_texts"] = merged


# --- Ingest course links CSV to fill module resources ---
COURSE_LINKS_CSV = Path(__file__).parent / "dev_materials" / "Course Links & Resources 6d6e76ec5670407fb399d4ec39993f2c_all.csv"


def _parse_module_id(module_str: str):
    match = re.search(r"(\d+)", module_str or "")
    return int(match.group(1)) if match else None


def _merge_unique(existing, new):
    merged = list(existing or [])
    seen = {item.get("url") for item in merged if isinstance(item, dict)}
    for item in new or []:
        url = item.get("url")
        if url and url not in seen:
            merged.append(item)
            seen.add(url)
    return merged


def _load_course_links(csv_path: Path):
    if not csv_path.exists():
        return {}

    by_module = {}
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            module_id = _parse_module_id(row.get("Module", ""))
            if not module_id:
                continue

            url = (row.get("document url") or "").strip()
            resource_type = (row.get("Resource Type 1") or "").strip().lower()
            title = (row.get("Link Title") or row.get("\ufeffLink Title") or "").strip()
            desc = (row.get("Description") or "").strip()
            label = title or desc or "Resource"

            if not url or not resource_type:
                continue

            record = by_module.setdefault(
                module_id,
                {"quizzes": [], "required_readings": [], "optional_readings": []},
            )

            if resource_type == "lecture slides":
                record["slides"] = url
            elif resource_type == "guided notes":
                record["guided_notes"] = url
            elif resource_type == "quiz":
                record["quizzes"].append({"label": label, "url": url})
            elif resource_type == "required reading - textbook":
                record["required_readings"].append({"label": label, "url": url})
            elif resource_type == "optional reading - textbook":
                record["optional_readings"].append({"label": label, "url": url})

    return by_module


COURSE_LINKS_BY_MODULE = _load_course_links(COURSE_LINKS_CSV)

for module in MICRO_MODULES:
    links = COURSE_LINKS_BY_MODULE.get(module.get("id"))
    if not links:
        continue

    materials = module.setdefault("materials", {})

    if links.get("slides"):
        materials["slides"] = links["slides"]
    if links.get("guided_notes"):
        materials["guided_notes"] = links["guided_notes"]
    if links.get("quizzes"):
        materials["khan"] = _merge_unique(materials.get("khan", []), links["quizzes"])

    if links.get("required_readings"):
        materials["readings"] = _merge_unique(
            materials.get("readings", []), links["required_readings"]
        )

    if links.get("optional_readings"):
        openstax_links = module.setdefault("openstax", {})
        openstax_links["optional"] = _merge_unique(
            openstax_links.get("optional", []), links["optional_readings"]
        )
