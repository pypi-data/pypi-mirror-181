from __future__ import annotations
import subprocess


def _fake_echo_to_file(content_file, write_file) -> dict[str, bool]:
    with open(content_file) as f:
        s = f.read()
        f = open(write_file, "w")
        f.write(s)
        f.close()
    return {"logs": "file written", "status": True}


def _do(command: list | str, WAIT_FOR_OUTPUT: bool = True) -> dict[str, bool]:
    if type(command) == str:
        command = command.split(" ")
    if type(command) != list:
        return {"logs": "Command is not a string nor a list", "status": False}
    try:
        if not WAIT_FOR_OUTPUT:
            subprocess.Popen(command)
            return {"logs": "Command executed in background", "status": True}
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        err = None if err == b"" else err.decode("utf-8")
        out = None if out == b"" else out.decode("utf-8")
        logs = out if out else err
        if out and err:
            logs = " &>1 " + out + " &>2 " + err
        success = True if p.returncode != 1 else False
        return {"logs": logs, "status": success}
    except FileNotFoundError as e:
        return {"logs": str(e), "status": False}


def _mkdir(path: str) -> dict[str, bool]:
    return _do(f"mkdir -p {path}")


def _rmdir(path: str) -> dict[str, bool]:
    return _do(f"rm -rf {path}")


def _cp(src: str, dst: str) -> dict[str, bool]:
    return _do(f"cp -r {src} {dst}")


def _rm(path: str) -> dict[str, bool]:
    return _do(f"rm {path}")


def _mv(src: str, dst: str) -> dict[str, bool]:
    return _do(f"mv {src} {dst}")


def _chmod(path: str, mode: str) -> dict[str, bool]:
    return _do(f"chmod {mode} {path}")


def _read_file(path: str) -> dict[str, bool]:
    return _do(f"cat {path}")


def _run_script(path: str, args: list) -> dict[str, bool]:
    return _do(f"{path} {' '.join(args)}")


class Bash:
    @staticmethod
    def do(command: list | str, WAIT_FOR_OUTPUT: bool = True) -> dict[str, bool]:
        """
        Run a command in the shell and return the output and error code.
        Some commands will not work and some others will cause infinite loops.
        A list of tested commands is available in the documentation.

        :param WAIT_FOR_OUTPUT: boolean to wait for the output of the command
        :param command: a String or a List of Strings to be executed in the shell
        :return: a dict containing the output and the error code
        """
        return _do(command, WAIT_FOR_OUTPUT)

    @staticmethod
    def mkdir(path: str) -> dict[str, bool]:
        """
        Create a directory and all its parents.

        :param path: the path of the directory to create
        :return: a dict containing the output and the error code
        """
        return _mkdir(path)

    @staticmethod
    def rmdir(path: str) -> dict[str, bool]:
        """
        Remove a directory and all its children.

        :param path: the path of the directory to remove
        :return: a dict containing the output and the error code
        """
        return _rmdir(path)

    @staticmethod
    def cp(src: str, dst: str) -> dict[str, bool]:
        """
        Copy a file or a directory to another location.

        :param src: the path of the file or directory to copy
        :param dst: the path of the destination
        :return: a dict containing the output and the error code
        """
        return _cp(src, dst)

    @staticmethod
    def rm(path: str) -> dict[str, bool]:
        """
        Remove a file.

        :param path: the path of the file to remove
        :return: a dict containing the output and the error code
        """
        return _rm(path)

    @staticmethod
    def mv(src: str, dst: str) -> dict[str, bool]:
        """
        Move a file or a directory to another location.

        :param src: the path of the file or directory to move
        :param dst: the path of the destination
        :return: a dict containing the output and the error code
        """
        return _mv(src, dst)

    @staticmethod
    def chmod(path: str, mode: str) -> dict[str, bool]:
        """
        Change the permissions of a file or a directory.

        :param path: the path of the file or directory to change
        :param mode: the mode to apply
        :return: a dict containing the output and the error code
        """
        return _chmod(path, mode)

    @staticmethod
    def read_file(path: str) -> dict[str, bool]:
        """
        Read the content of a file.

        :param path: the path of the file to read
        :return: a dict containing the output and the error code
        """
        return _read_file(path)

    @staticmethod
    def run_script(path: str, args: list) -> dict[str, bool]:
        """
        Run a bash script and log the output.

        :param path: the path of the script to run
        :param args: the arguments to pass to the script
        :return: a dict containing the output and the error code
        """
        Bash.chmod(path, "755")
        return _run_script(path, args)

    @staticmethod
    def echo_to_file(content_file: str, write_file: str) -> dict[str, bool]:
        """
        Write the content of a file to another file.

        :param content_file: the path of the file to read
        :param write_file: the path of the file to write
        :return: a dict containing the output and the error code
        """
        return _fake_echo_to_file(content_file, write_file)
