#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_bohicalog
----------------------------------

Tests for `bohicalog` module.
"""
import os
import tempfile

import bohicalog


def test_api_logfile(capsys):
    """
    bohicalog.logfile(..) should work as expected
    """
    bohicalog.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        bohicalog.logger.info("info1")

        # Set logfile
        bohicalog.logfile(temp.name)
        bohicalog.logger.info("info2")

        # Remove logfile
        bohicalog.logfile(None)
        bohicalog.logger.info("info3")

        # Set logfile again
        bohicalog.logfile(temp.name)
        bohicalog.logger.info("info4")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" not in content
            assert "] info2" in content
            assert "] info3" not in content
            assert "] info4" in content

    finally:
        temp.close()


def test_api_loglevel(capsys):
    """
    Should reconfigure the internal logger loglevel
    """
    bohicalog.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        bohicalog.logfile(temp.name)
        bohicalog.logger.info("info1")
        bohicalog.loglevel(bohicalog.WARN)
        bohicalog.logger.info("info2")
        bohicalog.logger.warning("warn1")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" in content
            assert "] info2" not in content
            assert "] warn1" in content

    finally:
        temp.close()


def test_api_loglevel_custom_handlers(capsys):
    """
    Should reconfigure the internal logger loglevel and custom handlers
    """
    bohicalog.reset_default_logger()
    # TODO
    pass
    # temp = tempfile.NamedTemporaryFile()
    # try:
    #     bohicalog.logfile(temp.name)
    #     bohicalog.logger.info("info1")
    #     bohicalog.loglevel(bohicalog.WARN)
    #     bohicalog.logger.info("info2")
    #     bohicalog.logger.warning("warn1")

    #     with open(temp.name) as f:
    #         content = f.read()
    #         assert "] info1" in content
    #         assert "] info2" not in content
    #         assert "] warn1" in content

    # finally:
    #     temp.close()


def test_api_rotating_logfile(capsys):
    """
    bohicalog.rotating_logfile(..) should work as expected
    """
    bohicalog.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        bohicalog.logger.info("info1")

        # Set logfile
        bohicalog.logfile(temp.name, maxBytes=10, backupCount=3)
        bohicalog.logger.info("info2")
        bohicalog.logger.info("info3")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" not in content  # logged before setting up logfile
            assert "] info2" not in content  # already rotated out
            assert "] info3" in content  # already rotated out

        fn_rotated = temp.name + ".1"
        assert os.path.exists(fn_rotated)
        with open(fn_rotated) as f:
            content = f.read()
            assert "] info2" in content

    finally:
        temp.close()


def test_api_logfile_custom_loglevel():
    """
    bohicalog.logfile(..) should be able to use a custom loglevel
    """
    bohicalog.reset_default_logger()
    temp = tempfile.NamedTemporaryFile()
    try:
        # Set logfile with custom loglevel
        bohicalog.logfile(temp.name, loglevel=bohicalog.WARN)
        bohicalog.logger.info("info1")
        bohicalog.logger.warning("warn1")

        # If setting a loglevel with bohicalog.loglevel(..) it will not overwrite
        # the custom loglevel of the file handler
        bohicalog.loglevel(bohicalog.INFO)
        bohicalog.logger.info("info2")
        bohicalog.logger.warning("warn2")

        with open(temp.name) as f:
            content = f.read()
            assert "] info1" not in content
            assert "] warn1" in content
            assert "] info2" not in content
            assert "] warn2" in content

    finally:
        temp.close()
