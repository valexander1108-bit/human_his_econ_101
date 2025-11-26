# OpenStax chapter catalog + module mapping
OPENSTAX_BASE_URL = "https://openstax.org/books/principles-microeconomics-3e/pages/"

# First section of each chapter (serves as the landing link)
OPENSTAX_CHAPTERS = {
    1: {
        "title": "Welcome to Economics!",
        "slug": "1-introduction",
        "url": f"{OPENSTAX_BASE_URL}1-introduction",
    },
    2: {
        "title": "Choice in a World of Scarcity",
        "slug": "2-introduction-to-choice-in-a-world-of-scarcity",
        "url": f"{OPENSTAX_BASE_URL}2-introduction-to-choice-in-a-world-of-scarcity",
    },
    3: {
        "title": "Demand and Supply",
        "slug": "3-introduction-to-demand-and-supply",
        "url": f"{OPENSTAX_BASE_URL}3-introduction-to-demand-and-supply",
    },
    4: {
        "title": "Labor and Financial Markets",
        "slug": "4-introduction-to-labor-and-financial-markets",
        "url": f"{OPENSTAX_BASE_URL}4-introduction-to-labor-and-financial-markets",
    },
    5: {
        "title": "Elasticity",
        "slug": "5-introduction-to-elasticity",
        "url": f"{OPENSTAX_BASE_URL}5-introduction-to-elasticity",
    },
    6: {
        "title": "Consumer Choices",
        "slug": "6-introduction-to-consumer-choices",
        "url": f"{OPENSTAX_BASE_URL}6-introduction-to-consumer-choices",
    },
    7: {
        "title": "Production, Costs, and Industry Structure",
        "slug": "7-introduction-to-production-costs-and-industry-structure",
        "url": f"{OPENSTAX_BASE_URL}7-introduction-to-production-costs-and-industry-structure",
    },
    8: {
        "title": "Perfect Competition",
        "slug": "8-introduction-to-perfect-competition",
        "url": f"{OPENSTAX_BASE_URL}8-introduction-to-perfect-competition",
    },
    9: {
        "title": "Monopoly",
        "slug": "9-introduction-to-a-monopoly",
        "url": f"{OPENSTAX_BASE_URL}9-introduction-to-a-monopoly",
    },
    10: {
        "title": "Monopolistic Competition and Oligopoly",
        "slug": "10-introduction-to-monopolistic-competition-and-oligopoly",
        "url": f"{OPENSTAX_BASE_URL}10-introduction-to-monopolistic-competition-and-oligopoly",
    },
    11: {
        "title": "Monopoly and Antitrust Policy",
        "slug": "11-introduction-to-monopoly-and-antitrust-policy",
        "url": f"{OPENSTAX_BASE_URL}11-introduction-to-monopoly-and-antitrust-policy",
    },
    12: {
        "title": "Environmental Protection and Negative Externalities",
        "slug": "12-introduction-to-environmental-protection-and-negative-externalities",
        "url": f"{OPENSTAX_BASE_URL}12-introduction-to-environmental-protection-and-negative-externalities",
    },
    13: {
        "title": "Positive Externalities and Public Goods",
        "slug": "13-introduction-to-positive-externalities-and-public-goods",
        "url": f"{OPENSTAX_BASE_URL}13-introduction-to-positive-externalities-and-public-goods",
    },
    14: {
        "title": "Labor Markets and Income",
        "slug": "14-introduction-to-labor-markets-and-income",
        "url": f"{OPENSTAX_BASE_URL}14-introduction-to-labor-markets-and-income",
    },
    15: {
        "title": "Poverty and Economic Inequality",
        "slug": "15-introduction-to-poverty-and-economic-inequality",
        "url": f"{OPENSTAX_BASE_URL}15-introduction-to-poverty-and-economic-inequality",
    },
    16: {
        "title": "Information, Risk, and Insurance",
        "slug": "16-introduction-to-information-risk-and-insurance",
        "url": f"{OPENSTAX_BASE_URL}16-introduction-to-information-risk-and-insurance",
    },
    17: {
        "title": "Financial Markets",
        "slug": "17-introduction-to-financial-markets",
        "url": f"{OPENSTAX_BASE_URL}17-introduction-to-financial-markets",
    },
    18: {
        "title": "Public Economy",
        "slug": "18-introduction-to-public-economy",
        "url": f"{OPENSTAX_BASE_URL}18-introduction-to-public-economy",
    },
    19: {
        "title": "International Trade",
        "slug": "19-introduction-to-international-trade",
        "url": f"{OPENSTAX_BASE_URL}19-introduction-to-international-trade",
    },
    20: {
        "title": "Globalization and Protectionism",
        "slug": "20-introduction-to-globalization-and-protectionism",
        "url": f"{OPENSTAX_BASE_URL}20-introduction-to-globalization-and-protectionism",
    },
}

# Module → OpenStax chapter mapping
MODULE_OPENSTAX_MAP = [
    {
        "module": 1,
        "slug": "economic_thought_modeling",
        "title": "Economic Thought & Modeling",
        "core_openstax": [1, 2],
        "optional_openstax": [3],
    },
    {
        "module": 2,
        "slug": "supply_demand",
        "title": "Supply & Demand",
        "core_openstax": [3],
        "optional_openstax": [4],
    },
    {
        "module": 3,
        "slug": "elasticity",
        "title": "Elasticity",
        "core_openstax": [5],
        "optional_openstax": [6],
    },
    {
        "module": 4,
        "slug": "welfare_intervention",
        "title": "Welfare & Intervention",
        "core_openstax": [3, 4],
        "optional_openstax": [12, 13],
    },
    {
        "module": 5,
        "slug": "factors_of_production",
        "title": "Factors of Production",
        "core_openstax": [4, 14],
        "optional_openstax": [7],
    },
    {
        "module": 6,
        "slug": "choices_constraints",
        "title": "Choices & Constraints",
        "core_openstax": [2, 6],
        "optional_openstax": [17],
    },
    {
        "module": 7,
        "slug": "capitalism",
        "title": "Capitalism",
        "core_openstax": [],
        "optional_openstax": [18, 19, 20],
    },
    {
        "module": 8,
        "slug": "inequality",
        "title": "Inequality",
        "core_openstax": [14, 15],
        "optional_openstax": [18],
    },
    {
        "module": 9,
        "slug": "cost_of_production",
        "title": "Cost of Production",
        "core_openstax": [7],
        "optional_openstax": [8],
    },
    {
        "module": 10,
        "slug": "profit_maximization",
        "title": "Profit Maximization",
        "core_openstax": [8, 9],
        "optional_openstax": [ 10],
    },
    {
        "module": 11,
        "slug": "competition_information",
        "title": "Competition & Information",
        "core_openstax": [8, 9, 10],
        "optional_openstax": [11, 16],
    },
    {
        "module": 12,
        "slug": "policy_paradox_human_perspective",
        "title": "Policy, Paradox & Human Perspective",
        "core_openstax": [12, 13, 18],
        "optional_openstax": [],
    },
]
