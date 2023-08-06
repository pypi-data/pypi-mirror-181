import json
import shlex
import shutil
import sys
from typing import Sequence
from unittest.mock import patch

import pytest
from click.testing import Result
from cliconf import CLIConf
from cliconf.testing import CLIRunner

from multivenv import _platform
from multivenv._cli import cli
from multivenv._cli import info as info_cli
from multivenv._config import VenvConfig, VenvUserConfig
from multivenv.exc import CommandExitException, VenvNotSyncedException
from tests import ext_click
from tests.config import (
    AUTO_SYNC_CHANGED_CONFIG_PATH,
    BASIC_CONFIG_PATH,
    BASIC_REQUIREMENTS_HASH,
    EPHEMERAL_CONFIG_PATH,
    HOOKS_CONFIG_PATH,
    REQUIREMENTS_IN_PATH,
    REQUIREMENTS_MULTIPLATFORM_CONFIG_PATH,
    REQUIREMENTS_OUT_PATH,
    UPGRADE_REQUIREMENTS_IN_PATH,
    UPGRADE_REQUIREMENTS_OUT_PATH,
)
from tests.dirutils import change_directory_to
from tests.fixtures.targets import linux_310_environment
from tests.fixtures.temp_dir import *
from tests.osutils import is_not_found_output
from tests.venvutils import get_installed_packages_in_venv

runner = CLIRunner()


class CLIRunnerException(Exception):
    pass


def run_cli(command: str, catch_exceptions: bool = False) -> Result:
    args = shlex.split(command)
    result = runner.invoke(cli, args, catch_exceptions=catch_exceptions)
    return result


def test_compile_cli(temp_dir: Path):
    expect_out_path = temp_dir / "requirements.txt"
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        assert not expect_out_path.exists()
        run_cli("compile")
        assert expect_out_path.exists()
        assert "multivenv-test-package==1.1.0" in expect_out_path.read_text()


def test_compile_upgrade_cli(temp_dir: Path):
    expect_out_path = temp_dir / "requirements.txt"
    shutil.copy(UPGRADE_REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(UPGRADE_REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("compile")
        assert "multivenv-test-package==1.1.0" in expect_out_path.read_text()


def test_compile_no_upgrade_cli(temp_dir: Path):
    expect_out_path = temp_dir / "requirements.txt"
    shutil.copy(UPGRADE_REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(UPGRADE_REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("compile --no-upgrade")
        assert "multivenv-test-package==1.0.0" in expect_out_path.read_text()


def test_sync_cli(temp_dir: Path):
    venv_name = "basic"
    venvs_folder = temp_dir / "venvs"
    venv_folder = venvs_folder / venv_name
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        config = VenvConfig.from_user_config(
            VenvUserConfig(
                requirements_in=temp_dir / "requirements.in",
                requirements_out=temp_dir / "requirements.txt",
            ),
            name=venv_name,
            venv_path=venv_folder,
            config_path=temp_dir / "mvenv.yaml",
        )
        run_cli("sync")
        assert "multivenv-test-package==1.1.0" in get_installed_packages_in_venv(config)


def test_sync_ephemeral(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(EPHEMERAL_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        result = run_cli("sync")
        assert "No persistent venvs found" in result.stdout


def test_post_create_and_sync(temp_dir: Path):
    venv_name = "basic"
    venvs_folder = temp_dir / "venvs"
    venv_folder = venvs_folder / venv_name
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(HOOKS_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        config = VenvConfig.from_user_config(
            VenvUserConfig(
                requirements_in=temp_dir / "requirements.in",
                requirements_out=temp_dir / "requirements.txt",
            ),
            name=venv_name,
            venv_path=venv_folder,
            config_path=temp_dir / "mvenv.yaml",
        )
        expect_path = (config.path / "post_create.txt").resolve()
        assert not expect_path.exists()
        run_cli("sync")
        # Check post_create hook
        assert expect_path.exists()
        packages = get_installed_packages_in_venv(config)
        assert "multivenv-test-package==1.1.0" in packages
        # Check post_sync hook
        assert "flake8==5.0.3" in packages


def test_update_cli(temp_dir: Path):
    venv_name = "basic"
    venvs_folder = temp_dir / "venvs"
    venv_folder = venvs_folder / venv_name
    expect_requirements_out_path = temp_dir / "requirements.txt"
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        config = VenvConfig.from_user_config(
            VenvUserConfig(
                requirements_in=temp_dir / "requirements.in",
                requirements_out=temp_dir / "requirements.txt",
            ),
            name=venv_name,
            venv_path=venv_folder,
            config_path=temp_dir / "mvenv.yaml",
        )
        assert not expect_requirements_out_path.exists()
        run_cli("update")
        assert expect_requirements_out_path.exists()
        assert "multivenv-test-package==1.1.0" in get_installed_packages_in_venv(config)


def test_update_multiplatform_cli(temp_dir: Path, linux_310_environment):
    venv_name = "basic"
    venvs_folder = temp_dir / "venvs"
    venv_folder = venvs_folder / venv_name
    expect_requirements_out_names = [
        "requirements-3.7-linux-Linux-x86_64.txt",
        "requirements-3.7-win32-Windows-AMD64.txt",
        "requirements-3.10-linux-Linux-x86_64.txt",
        "requirements-3.10-win32-Windows-AMD64.txt",
    ]
    expect_requirements_out_paths = [
        temp_dir / name for name in expect_requirements_out_names
    ]
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_MULTIPLATFORM_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        config = VenvConfig.from_user_config(
            VenvUserConfig(
                requirements_in=temp_dir / "requirements.in",
                requirements_out=temp_dir / "requirements.txt",
            ),
            name=venv_name,
            venv_path=venv_folder,
            config_path=temp_dir / "mvenv.yaml",
        )
        for path in expect_requirements_out_paths:
            assert not path.exists()
        run_cli("update")
        for path in expect_requirements_out_paths:
            assert path.exists()
        assert "multivenv-test-package==1.1.0" in get_installed_packages_in_venv(config)


def test_update_ephemeral(temp_dir: Path):
    expect_requirements_out_path = temp_dir / "requirements.txt"
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(EPHEMERAL_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        assert not expect_requirements_out_path.exists()
        run_cli("update")
        assert expect_requirements_out_path.exists()


def test_update_cli_with_upgrade(temp_dir: Path):
    venv_name = "basic"
    venvs_folder = temp_dir / "venvs"
    venv_folder = venvs_folder / venv_name
    shutil.copy(UPGRADE_REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(UPGRADE_REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        config = VenvConfig.from_user_config(
            VenvUserConfig(
                requirements_in=temp_dir / "requirements.in",
                requirements_out=temp_dir / "requirements.txt",
            ),
            name=venv_name,
            venv_path=venv_folder,
            config_path=temp_dir / "mvenv.yaml",
        )
        run_cli("update")
        assert "multivenv-test-package==1.1.0" in get_installed_packages_in_venv(config)


def test_update_cli_with_no_upgrade(temp_dir: Path):
    venv_name = "basic"
    venvs_folder = temp_dir / "venvs"
    venv_folder = venvs_folder / venv_name
    shutil.copy(UPGRADE_REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(UPGRADE_REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        config = VenvConfig.from_user_config(
            VenvUserConfig(
                requirements_in=temp_dir / "requirements.in",
                requirements_out=temp_dir / "requirements.txt",
            ),
            name=venv_name,
            venv_path=venv_folder,
            config_path=temp_dir / "mvenv.yaml",
        )
        run_cli("update --no-upgrade")
        assert "multivenv-test-package==1.0.0" in get_installed_packages_in_venv(config)


def test_run_cli(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("sync")
        output = run_cli("run basic pip freeze")
        assert "multivenv-test-package==1.1.0" in output.stdout


def test_run_cli_auto_sync(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        output = run_cli("run basic pip freeze")
        assert "multivenv-test-package==1.1.0" in output.stdout


def test_run_cli_no_auto_sync(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        with pytest.raises(VenvNotSyncedException):
            run_cli("run basic pip freeze --no-auto-sync")


def test_run_ephemeral(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(EPHEMERAL_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        output = run_cli("run basic pip freeze")
        assert "multivenv-test-package==1.1.0" in output.stdout


def test_run_cli_error_propagate(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("sync")
        # Propagate is the default, no need to add option
        output = run_cli("run basic sdfsdfsgsdfgsdfgf")
        assert is_not_found_output(output.stdout)
        assert "CommandExitException" not in output.stdout
        assert output.exit_code != 0


def test_run_cli_error_ignore(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("sync")
        output = run_cli("run --errors ignore basic sdfsdfsgsdfgsdfgf")
        assert is_not_found_output(output.stdout)
        assert "CommandExitException" not in output.stdout
        assert output.exit_code == 0


def test_run_cli_error_raise(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("sync")
        output = run_cli(
            "run --errors raise basic sdfsdfsgsdfgsdfgf", catch_exceptions=True
        )
        assert is_not_found_output(output.stdout)
        assert output.exit_code != 0
        assert isinstance(output.exception, CommandExitException)


def test_run_all_cli(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("sync")
        output = run_cli("run-all pip freeze")
        assert "multivenv-test-package==1.1.0" in output.stdout


def test_run_all_ephemeral(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(EPHEMERAL_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        output = run_cli("run-all pip freeze")
        assert "multivenv-test-package==1.1.0" in output.stdout


def test_info_no_venv(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        output = run_cli("info")
        assert "basic" in output.stdout
        assert "venvs" in output.stdout
        assert "requirements.txt" in output.stdout
        assert "requirements.in" in output.stdout
        assert "exists=False" in output.stdout
        assert "mvenv.yaml" in output.stdout


def test_info_json(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        output = run_cli("info --info-format json")
        data = json.loads(output.stdout)
        info = data["venv_info"][0]
        assert info["name"] == "basic"
        assert "venvs" in info["path"]
        assert "requirements.txt" in output.stdout
        assert info["config_requirements"]["in_path"] == "requirements.in"
        assert info["config_requirements"]["out_path"] == "requirements.txt"
        assert info["discovered_requirements"]["in_path"] == str(
            temp_dir / "requirements.in"
        )
        assert info["discovered_requirements"]["out_path"] == None
        assert info["exists"] is False
        assert data["system"]["version"]["version"]["major"] == 3
        assert info["state"]["needs_sync"] is True
        assert info["state"]["requirements_hash"] is None


def test_info_with_venv(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("sync")
        output = run_cli("info")
        assert "basic" in output.stdout
        assert "venvs" in output.stdout
        assert "requirements.txt" in output.stdout
        assert "requirements.in" in output.stdout
        assert "exists=True" in output.stdout
        assert "3" in output.stdout
        assert BASIC_REQUIREMENTS_HASH in output.stdout


def test_info_from_subdir(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    subdir = temp_dir / "subdir"
    subdir.mkdir()
    with change_directory_to(subdir):
        output = run_cli("info")
        assert "basic" in output.stdout
        assert "venvs" in output.stdout
        assert "requirements.txt" in output.stdout
        assert "requirements.in" in output.stdout
        assert "exists=False" in output.stdout


def test_info_from_subdir_with_absolute_path_in_config(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    cls = info_cli.model_cls
    model = cls(
        venvs={
            "basic": VenvUserConfig(
                requirements_in=(temp_dir / "requirements.in").resolve(),
                requirements_out=(temp_dir / "requirements.txt").resolve(),
            )
        }
    )
    model.settings.custom_config_folder = temp_dir
    model.save()
    subdir = temp_dir / "subdir"
    subdir.mkdir()
    with change_directory_to(subdir):
        output = run_cli("info")
        info_line = output.stdout.replace("\n", "")
        assert "basic" in info_line
        assert "venvs" in info_line
        assert "requirements.txt" in info_line
        assert "requirements.in" in info_line
        assert "exists=False" in info_line


# TODO: Tests for run-all error handling


def test_delete_cli(temp_dir: Path):
    venv_name = "basic"
    venvs_folder = temp_dir / "venvs"
    venv_folder = venvs_folder / venv_name
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        run_cli("sync")
        assert venv_folder.exists()
        run_cli("delete")
        assert not venv_folder.exists()


def test_delete_ephemeral(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(EPHEMERAL_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        result = run_cli("delete")
        assert "No existing venvs found matching the given criteria" in result.stdout


def test_delete_non_synced(temp_dir: Path):
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    shutil.copy(REQUIREMENTS_OUT_PATH, temp_dir)
    shutil.copy(BASIC_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        result = run_cli("delete")
        assert "No existing venvs found matching the given criteria" in result.stdout


def test_manage_external_dependencies(temp_dir: Path):
    # Set up dependencies so that they are specified in an external file
    extra_path = temp_dir / "extra.txt"
    shutil.copy(REQUIREMENTS_IN_PATH, temp_dir)
    (temp_dir / "requirements.txt").write_text("")
    extra_path.write_text("")
    shutil.copy(AUTO_SYNC_CHANGED_CONFIG_PATH, temp_dir)
    with change_directory_to(temp_dir):
        output = run_cli("run basic pip freeze")
        assert "multivenv-test-package==1.1.0" not in output.stdout

        # Now change the extra file to add the requirement
        shutil.copy(REQUIREMENTS_OUT_PATH, extra_path)

        # Should auto-sync before running the command
        output2 = run_cli("run basic pip freeze")
        # Now the dependency is installed
        assert "multivenv-test-package==1.1.0" in output2.stdout
