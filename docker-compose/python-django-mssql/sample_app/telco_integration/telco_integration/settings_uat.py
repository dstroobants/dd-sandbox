"""
UAT settings module loaded via SETTINGS_PATH=telco_integration.settings_uat
(matches the production Kubernetes pod environment).
"""

from .settings import *  # noqa: F401,F403

# UAT-specific overrides go here. Kept as a thin wrapper around base settings
# on purpose so the repro stays close to a vanilla Django app.
DEBUG = False
