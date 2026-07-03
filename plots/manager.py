"""
plots/manager.py
"""

from plots.logger import setup_logger
from plots.detector_metrics import detector_metrics_plot
from plots.attack_recall import attack_recall_plot
from plots.country_heatmap import country_heatmap_plot
from plots.confidence_intervals import confidence_interval_plot
from plots.confusion_matrix import confusion_matrix_plot
from plots.significance import significance_plot
from plots.campaign_summary import campaign_summary_plot
from plots.workflow_diagram import workflow_diagram

def run():

    logger = setup_logger()

    logger.info(

        "Generating detector comparison..."

    )

    # detector_metrics_plot()
    #
    # attack_recall_plot()
    #
    # country_heatmap_plot()
    #
    # confidence_interval_plot()
    #
    # confusion_matrix_plot()

    # significance_plot()

    # campaign_summary_plot()

    workflow_diagram()

    logger.info(

        "Finished."
    )