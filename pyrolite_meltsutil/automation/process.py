import os, sys, platform
import subprocess
import threading
import stat
import psutil
import queue
import time
from pathlib import Path
from pyrolite.util.general import get_process_tree
from ..util.general import get_local_link

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def enqueue_output(out, queue):
    """
    Send output to a queue.

    Parameters
    -----------
    out
        Readable output object.
    queue : :class:`queue.Queue`
        Queue to send ouptut to.
    """
    for line in iter(out.readline, b""):
        queue.put(line)
    out.close()


class MeltsProcess(object):
    def __init__(
        self,
        executable=None,
        env="alphamelts_default_env.txt",
        meltsfile=None,
        fromdir=r"./",
        log=logger.debug,
        timeout=None,
    ):
        """
        Parameters
        ----------
        executable : :class:`str` | :class:`pathlib.Path`
            Executable to run. Enter path to the the `run_alphamelts.command `
            script. Falls back to local installation if no exectuable is specified
            and a local instllation exists.
        env : :class:`str` | :class:`pathlib.Path`
            Environment file to use.
        meltsfile : :class:`str` | :class:`pathlib.Path`
            Path to meltsfile to use for calculations.
        fromdir : :class:`str` | :class:`pathlib.Path`
            Directory to use as the working directory for the execution.
        log : :class:`callable`
            Function for logging output.

        Todo
        -----
            * Recognise errors from stdout
            * Input validation (graph of available options vs menu level)
            * Logging of failed runs
            * Facilitation of interactive mode upon error
            * Error recovery methods (e.g. change the temperature)

        Notes
        ------
            * Need to specify an exectuable or perform a local installation of alphamelts.
            * Need to get full paths for melts files, directories etc
        """
        self.env = None
        self.meltsfile = None
        self.fromdir = None  # default to None, runs from cwd
        self.log = log
        self.timeout = timeout or 60.0  # 1 minute max
        if fromdir is not None:
            self.log("Setting working directory: {}".format(fromdir))
            fromdir = Path(fromdir)
            try:
                assert fromdir.exists() and fromdir.is_dir()
            except AssertionError:
                fromdir.mkdir(parents=True)
            self.fromdir = Path(fromdir)

        if executable is None:
            # check for local install
            if platform.system() == "Windows":
                local_run = get_local_link("run_alphamelts.bat")
            else:
                local_run = get_local_link("run_alphamelts.command")

            executable = local_run
            self.log(
                "Using local executable: {} @ {}".format(
                    executable.name, executable.parent
                )
            )

        executable = Path(executable)
        self.exname = str(executable.name)
        self.executable = str(executable)
        st = os.stat(self.executable)
        assert bool(stat.S_IXUSR), "User needs execution permission."
        self.run = []

        self.run.append(self.executable)  # executable file

        self.init_args = []  # initial arguments to pass to the exec before returning
        if meltsfile is not None:
            self.log("Setting meltsfile: {}".format(meltsfile))
            self.meltsfile = Path(meltsfile)
            self.run += ["-m", str(self.meltsfile)]
            self.init_args += ["1", str(self.meltsfile)]  # enter meltsfile
        if env is not None:
            self.log("Setting environment file: {}".format(env))
            self.env = Path(env)
            self.run += ["-f", str(env)]

        self.start()  # could split this out such that processes can be prepared beforehand
        time.sleep(0.5)
        self.log("Passing Inital Variables: " + " ".join(self.init_args))
        self.write(self.init_args)

    @property
    def callstring(self):
        """Get the call string such that analyses can be reproduced manually."""
        return " ".join(["cd", str(self.fromdir), "&&"] + self.run)

    def log_output(self):
        """
        Log output to the configured logger.
        """
        self.log("\n" + self.read())

    def start(self):
        """
        Start the process.

        Returns
        --------
        :class:`subprocess.Popen`
            Melts process object.
        """
        self.started = time.time()
        self.log(
            "Starting Melts Process with: " + " ".join([self.exname] + self.run[1:])
        )
        config = dict(
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(self.fromdir),
            close_fds=(os.name == "posix"),
        )
        self.process = subprocess.Popen(self.run, **config)
        logger.debug("Process Started with ID {}".format(self.process.pid))
        logger.debug("Reproduce using: {}".format(self.callstring))
        # Queues and Logging
        self.q = queue.Queue()
        self.T = threading.Thread(
            target=enqueue_output, args=(self.process.stdout, self.q)
        )
        self.T.daemon = True  # kill when process dies
        self.T.start()  # start the output thread

        self.errq = queue.Queue()
        self.errT = threading.Thread(  # separate thread for error reporting
            target=enqueue_output, args=(self.process.stderr, self.errq)
        )
        self.errT.daemon = True  # kill when process dies
        self.errT.start()  # start the err output thread
        return self.process

    def read(self):
        """
        Read from the output queue.

        Returns
        ---------
        :class:`str`
            Concatenated output from the output queue.
        """
        lines = []
        while not self.q.empty():
            lines.append(self.q.get_nowait().decode())
        return "".join(lines)

    @property
    def timed_out(self):
        return (time.time() - self.started) > self.timeout

    def wait(self, step=1.0):
        """
        Wait until addtions to process.stdout stop.

        Parameters
        -----------
        step : :class:`float`
            Step in seconds at which to check the stdout queue.
        """
        while True:
            size = self.q.qsize()
            time.sleep(step)
            if self.timed_out:
                self.log(
                    "Process timed out after {:2.1f} s".format(
                        time.time() - self.started
                    )
                )
                self.terminate()
                break
            elif size == self.q.qsize():
                break

    def write(self, messages, wait=True, log=False):
        """
        Send commands to the process.

        Parameters
        -----------
        messages
            Sequence of messages/commands to send.
        wait : :class:`bool`
            Whether to wait for process.stdout to finish.
        log : :class:`bool`
            Whether to log output to the logger.
        """
        for message in messages:
            msg = (str(message).strip() + str(os.linesep)).encode("utf-8")
            self.process.stdin.write(msg)
            self.process.stdin.flush()
            if wait:
                self.wait()
            if log:
                self.log(message)
                self.log_output()

    def terminate(self):
        """
        Terminate the process.

        Notes
        -------
            * Will likely terminate as expected using the command '0' to exit.
            * Otherwise will attempt to cleanup the process.
        """
        self.alphamelts_ex = []
        try:
            for p in get_process_tree(self.process.pid):
                if "alpha" in p.name():
                    self.alphamelts_ex.append(p)
            self.write("0")
            time.sleep(0.5)
        except (ProcessLookupError, psutil.NoSuchProcess):
            logger.warning("Process terminated unexpectedly.")

        try:
            self.process.stdin.close()
            self.process.terminate()
            self.process.wait(timeout=0.2)
        except ProcessLookupError:
            logger.debug("Process terminated successfully.")

        self.cleanup()

    def cleanup(self):
        for p in self.alphamelts_ex:  # kill the children executables
            try:
                # kill the alphamelts executable which can hang
                logger.debug("Terminating {}".format(p.name()))
                p.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                pass
