# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille<john@compose-x.io>

from os import path

from behave import given, then
from ecs_composex.common.settings import ComposeXSettings
from ecs_composex.common.stacks import process_stacks
from ecs_composex.ecs_composex import generate_full_template
from ecs_composex.exceptions import ComposeBaseException
from pytest import raises


def here():
    return path.abspath(path.dirname(__file__))


@given("With {file_path}")
def step_impl(context, file_path):
    if not hasattr(context, "files"):
        files = []
        setattr(context, "files", files)
    else:
        files = getattr(context, "files")
    files.append(file_path)


@given("I use defined files as input to define execution settings")
def step_impl(context):

    cases_path = [
        path.abspath(f"{here()}/../../use-cases/{file_name}")
        for file_name in context.files
    ]
    print(cases_path)
    context.settings = ComposeXSettings(
        profile_name=getattr(context, "profile_name")
        if hasattr(context, "profile_name")
        else None,
        **{
            ComposeXSettings.name_arg: "test",
            ComposeXSettings.command_arg: ComposeXSettings.render_arg,
            ComposeXSettings.input_file_arg: cases_path,
            ComposeXSettings.format_arg: "yaml",
        },
    )
    context.settings.set_bucket_name_from_account_id()


@then("I use defined files as input expecting an error")
def step_impl(context):

    cases_path = [
        path.abspath(f"{here()}/../../use-cases/{file_name}")
        for file_name in context.files
    ]
    print(cases_path)
    with raises((ValueError, KeyError, ComposeBaseException)):
        context.settings = ComposeXSettings(
            profile_name=getattr(context, "profile_name")
            if hasattr(context, "profile_name")
            else None,
            **{
                ComposeXSettings.name_arg: "test",
                ComposeXSettings.command_arg: ComposeXSettings.render_arg,
                ComposeXSettings.input_file_arg: cases_path,
                ComposeXSettings.format_arg: "yaml",
            },
        )
        context.settings.set_bucket_name_from_account_id()
        generate_full_template(context.settings)


@then("I render all files to verify execution")
def set_impl(context):
    if not hasattr(context, "root_stack"):
        context.root_stack = generate_full_template(context.settings)
    process_stacks(context.root_stack, context.settings)


@given("I want to use aws profile {profile_name}")
def step_impl(context, profile_name):
    """
    Function to change the session to a specific one.
    """
    context.session_name = profile_name


@then("I render the docker-compose to composex to validate")
def step_impl(context):
    context.root_stack = generate_full_template(context.settings)


@then("I render the docker-compose expecting an error")
def step_impl(context):
    with raises((ValueError, KeyError, ComposeBaseException)):
        context.root_stack = generate_full_template(context.settings)
