import os


def is_interactive():

    if os.isatty(0) or "PYCHARM_HOSTED" in os.environ:
        return 'true'
    # this condition is nearly always false, except for CI builds
    elif "CI_INTERACTIVE_TESTS" in os.environ:
        return 'non_interactive_ci'
    else:
        return 'false'