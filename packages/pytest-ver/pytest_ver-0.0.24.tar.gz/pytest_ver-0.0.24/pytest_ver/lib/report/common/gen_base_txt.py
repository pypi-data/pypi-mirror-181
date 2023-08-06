import datetime

from ... import services
from ...constants import Constants


# -------------------
## Base class for generating a text file
class GenBaseTxt:  # pylint: disable=too-few-public-methods

    # -------------------
    ## constructor
    def __init__(self):
        ## holds file pointer for the generated text file
        self._fp = None

    # -------------------
    ## generate test run information
    #
    # @return None
    def _gen_test_run_details(self):
        self._gen_title2('Test Run Details')
        self._fp.write(f"{'Test Run Type': <20}: {services.cfg.test_run_type}\n")
        self._fp.write(f"{'Test Run ID': <20}: {services.cfg.test_run_id}\n")
        dts = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime(services.cfg.dts_format)
        self._fp.write(f"{'Document Generated': <20}: {dts}\n")
        self._fp.write(f"{'pytest_ver version': <20}: v{Constants.version}\n")

        services.cfg.page_info.report(self._fp)
        self._fp.write('\n')

    # -------------------
    ## generate title
    #
    # @param title  the title to draw
    # @return None
    def _gen_title(self, title):
        self._gen_title2(title)
        self._fp.write('\n')

    # -------------------
    ## generate title lines
    #
    # @param title  the title to draw
    # @return None
    def _gen_title2(self, title):
        self._fp.write(f'{title}\n')
        self._fp.write(f"{'-' * len(title)}\n")
