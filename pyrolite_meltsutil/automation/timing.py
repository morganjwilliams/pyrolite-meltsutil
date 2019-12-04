import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

TIME_PER_STEP = 0.05  # seconds per iteration, varies


def get_P_steps(exp):
    """
    """

    if "isobaric" in exp.get("modes", []):
        steps = 0
    else:
        steps = 1


def estimate_experiment_duration(experiment):
    n, exp, env = experiment
    # get pressure steps

    # get temperature steps

    # check if isobaric or isothermal

    #
