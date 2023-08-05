import logging

from ipykernel.ipkernel import IPythonKernel
import configparser
import os


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


IPY_MAGIC_USE_ERROR_MSG = f"{bcolors.FAIL}{bcolors.BOLD}{bcolors.UNDERLINE}This notebook is not attached to a cluster. Please attach it to a cluster for parallel execution.\n{bcolors.ENDC}"
WARNING_MSG = f"{bcolors.WARNING}{bcolors.BOLD}{bcolors.UNDERLINE}WARNING: This notebook is not attached to a cluster.\n{bcolors.ENDC}"

KERNEL_ERROR_MSG = f"{bcolors.FAIL}{bcolors.BOLD}{bcolors.UNDERLINE}This notebook is not attached to a cluster.\n{bcolors.ENDC}"

IPYPARALLEL_LINE_MAGICS = ("px", "autopx", "pxconfig", "pxresult")
IPYPARALLEL_CELL_MAGICS = ("px",)
IPYPARALLEL_MAGICS = tuple(
    [f"%{m}" for m in IPYPARALLEL_LINE_MAGICS]
    + [f"%%{m}" for m in IPYPARALLEL_CELL_MAGICS]
)


class DummyKernel(IPythonKernel):
    banner = "Dummy Kernel"

    DEFAULT_CONFIG = """
    [Security]
    ALLOW_LOCAL_EXECUTION=false
    """
    allow_exec = False

    def start(self):

        config_file_loc = os.environ.get(
            "BODO_JUPYTERLAB_SERVERAPP_CONFIGFILE",
            os.path.expanduser("~/bodo_jupyterlab_serverapp.ini"),
        )
        logger = logging.getLogger()
        config = configparser.ConfigParser()

        # checking if config file exists or not
        if os.path.exists(config_file_loc):
            logger.warning(
                f"[Bodo Jupyter Server Extension] Found config file {config_file_loc}. Reading from it now..."
            )
            config.read(config_file_loc)
        else:
            logger.warning(
                f"[Bodo Jupyter Server Extension] Config file {config_file_loc} not found. Loading default config..."
            )
            config.read(self.DEFAULT_CONFIG)

        # Check the value of ALLOW_LOCAL_EXECUTION in the config file
        if "Security" in config:
            security_config = config["Security"]
            self.allow_exec = security_config.getboolean("ALLOW_LOCAL_EXECUTION", False)

        super().start()

    async def do_execute(
            self,
            code: str,
            silent,
            store_history=True,
            user_expressions=None,
            allow_stdin=False,
    ):
        # If Allow local execution is false, display error message
        if not self.allow_exec:
            stream_content = {"name": "stdout", "text": KERNEL_ERROR_MSG}
            self.send_response(self.iopub_socket, "stream", stream_content)
            return {
                "status": "error",
                "ename": "KERNEL ERROR",
                "evalue": KERNEL_ERROR_MSG
            }

        # If user tries to use an IPyParallel magic, display an error message.
        if code.startswith(IPYPARALLEL_MAGICS):
            if not silent:
                stream_content = {"name": "stderr", "text": IPY_MAGIC_USE_ERROR_MSG}
                self.send_response(self.iopub_socket, "stream", stream_content)
            return {
                "status": "ok",
                # The base class increments the execution count
                "execution_count": self.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        # Otherwise, display a warning message before executing
        if not silent:
            stream_content = {"name": "stdout", "text": WARNING_MSG}
            self.send_response(self.iopub_socket, "stream", stream_content)

        # Then execute the command as usual
        return await super().do_execute(
            code=code,
            silent=silent,
            store_history=store_history,
            user_expressions=user_expressions,
            allow_stdin=allow_stdin,
        )
