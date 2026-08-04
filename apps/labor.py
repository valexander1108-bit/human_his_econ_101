from apps.factor_common import independent_factor_app


def app():
    independent_factor_app("Labor", "Wage", default_supply=15.0, default_productivity=1.35, default_other_factor=65.0)
