from apps.factor_common import independent_factor_app


def app():
    independent_factor_app("Capital", "Interest/rental rate", default_supply=20.0, default_productivity=1.25, default_other_factor=75.0)
