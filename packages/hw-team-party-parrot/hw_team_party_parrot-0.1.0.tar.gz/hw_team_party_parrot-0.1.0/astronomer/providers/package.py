from typing import Any, Dict


def get_provider_info() -> Dict[str, Any]:
    """Return provider metadata to Airflow"""
    return {
        # Required.
        "package-name": "hw-team-party-parrot",
        "name": "hw-team-party-parrot",
        "description": "Apache Airflow Providers containing Operators and Plugins from Astronomer",
        "versions": "0.1.0",
        # Optional.
        "hook-class-names": [],
        "extra-links": [],
    }