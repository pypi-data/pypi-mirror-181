"""@Author: Rayane AMROUCHE

Report view functions
"""

import os
from typing import Any

import explainerdashboard as ed  # type: ignore


def view_shap_explainer(explainer: Any):
    """Launch a flask dash server of an explainer dashboard

    Args:
        explainer (Any): explainer to display
    """
    ed.ExplainerDashboard(explainer).run()


def view_eda_report(report: Any, dir_path: str, report_name: str):
    """Save an html eda report from a given report

    Args:
        report (Any): report to save as an html
        dir_path (str): directory path of the html report to save
        report_name (str): name of the html report to save
    """
    os.makedirs(dir_path, exist_ok=True)
    report.show_html(os.path.join(dir_path, report_name))
