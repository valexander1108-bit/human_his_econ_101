from apps.factor_common import independent_factor_app


def app():
    independent_factor_app("Land", "Rent", default_supply=25.0, default_productivity=1.10, default_other_factor=70.0)
