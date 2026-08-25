MODULE_BIG_QUESTIONS = {
    1: [
        "What are the foundational principles of economic analysis, and how do economists construct valid arguments?",
        "How do economists model the tradeoffs faced by consumers and producers under conditions of scarcity?",
        "Why do markets sometimes fail to allocate resources in ways that equitably meet human needs, and what, if anything, should be done about it?",
    ],
    2: [
        "How do economists model the tradeoff between work and leisure, and between present and future consumption?",
        "Do individuals actually optimize, or do cognitive and institutional limits produce systematic, predictable departures from rationality?",
        "When choice sets are shaped by institutional power rather than individual preference, who designed those constraints, and who benefits?",
    ],
    3: [
        "How do consumers rank competing bundles of goods, and what determines where they choose to be?",
        "How do dispersed prices coordinate buyers and sellers without any central authority directing them?",
        "What happens to the equilibrium outcome when a social, political, or ecological force shifts supply or demand, or both simultaneously?",
    ],
    4: [
        "How responsive are buyers and sellers to price changes, and what factors determine the magnitude of that response?",
        "Under what conditions does a competitive market maximize aggregate well-being, and how do price controls distort that outcome?",
        "Who bears the burden of a tax or a government intervention, and how does elasticity influence the answer?",
    ],
    5: [
        "How are wages, rents, and interest rates determined in competitive factor markets?",
        "Under what conditions does a worker's wage equal the value they add, and when does that prediction break down?",
    ],
    6: [
        "Why did global living standards remain stagnant for ten thousand years and then explode in the last 200, and why did this explosion happen unevenly?",
        "What are the three engines of long-run economic growth, and how does each generate the others?",
        "When markets generate negative externalities, what tool do economists reach for, and is it sufficient?",
    ],
    7: [
        "Why do poverty traps persist even in growing economies, and what mechanisms sustain them?",
        "How does market power in labor markets (monopsony) explain wages below VMP, and who designs the institutions that allow it?",
        "What is game theory, and why do rational individual strategies sometimes produce collectively irrational outcomes?",
    ],
    8: [
        "How does unequal access to digital technology amplify existing economic inequalities, and who bears the cost of the platform economy?",
        "How can algorithmic systems produce discriminatory outcomes even without discriminatory intent, and what corrective mechanisms are available?",
        "Who bears the greatest cost of climate change, and does the distribution of burdens match the distribution of responsibility?",
    ],
    9: [
        "How do economists model the relationship between inputs and outputs, and what is the law of diminishing returns?",
        "How does a firm's cost structure (fixed versus variable) shape its short-run and long-run decisions?",
        "At what scale of operation does a firm minimize its average cost, and what determines that scale?",
    ],
    10: [
        "What are the conditions of perfect competition, and how do they determine a firm's pricing power?",
        "How does the profit-maximization rule (MR = MC) operate, and what does it predict about output, price, and profit?",
        "How does monopoly power change market efficiency?",
        "Why does entry and exit drive economic profit to zero in the long run, and what survives that process?",
    ],
    11: [
        "How does market power allow a monopolist to set price above marginal cost, and what is the social cost of that power?",
        "When firms are strategically interdependent, how do they reason about competitors' moves, and what equilibria emerge?",
        "Why do cartels tend to collapse, and when can cooperation be sustained through repeated interaction?",
    ],
    12: [
        "What is the complete taxonomy of market failures, and what is the appropriate policy instrument for each type?",
        "What paradoxes and limitations does economics itself reveal about its own framework, and what lies beyond GDP as a measure of human flourishing?",
        "Having completed this course, how would you answer the question posed in Module 1: what is the most important market failure, and what should be done about it?",
    ],
}


def format_big_questions(module_id: int) -> str:
    questions = MODULE_BIG_QUESTIONS.get(module_id, [])
    if not questions:
        return ""
    bullets = "\n".join(f"- {question}" for question in questions)
    return f"### Big Questions\n\n{bullets}"
