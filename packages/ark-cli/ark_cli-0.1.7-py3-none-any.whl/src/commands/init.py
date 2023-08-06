# coding: utf-8

import os
import shutil
import click
from functools import partial
from binaryornot.check import is_binary
from src.definitions.ark_definitions import ArkDefinitions
from src.definitions.platform import Platform
from src.models.project import Project
from src.models.ios_config import IOSConfig
from src.utils.git import git_clone, git_cleanup
from src.utils.file import (
    find_files_recursively,
    find_dirs_recursively,
    read_text_file,
    write_text_file,
    update_dir_tree,
)


def __on_walk_project_file_android(file: str, name: str, package: str):
    if not is_binary(file):
        text = read_text_file(file)
        text = text.replace(
            ArkDefinitions.PACKAGE_ANDROID, package)
        text = text.replace(
            ArkDefinitions.PATH_ANDROID, package.replace('.', '/'))
        text = text.replace(
            ArkDefinitions.NAME_ANDROID, name)
        write_text_file(file, text)

        return True


def __on_walk_project_file_ios(file: str, ios_config: IOSConfig):
    if not is_binary(file):
        text = read_text_file(file)
        text = text.replace(
            ArkDefinitions.PACKAGE_IOS,
            ios_config.app_identifier)
        text = text.replace(
            ArkDefinitions.PATH_IOS,
            ios_config.app_identifier.replace('.', '/'))

        write_text_file(file, text)

        return True


def __on_walk_project_dir(dir: str, package: str, platform: str):
    platform_package_path = \
        ArkDefinitions.PACKAGE_ANDROID \
        if platform == Platform.ANDROID else ArkDefinitions.PACKAGE_IOS

    package_path = platform_package_path.replace('.', Platform.PATH_SEP)
    dst_package_path = package.replace('.', Platform.PATH_SEP)

    if dir.endswith(package_path):
        update_dir_tree(dir, package_path, dst_package_path)

        return True


def __process_android_project(
        name: str,
        project_dir: str,
        package: str,
        platform: str):
    # walk all text file and replace package
    find_files_recursively(
        project_dir,
        partial(__on_walk_project_file_android, name=name, package=package))

    # walk all dirs end with ark package
    find_dirs_recursively(
        project_dir,
        partial(__on_walk_project_dir, package=package, platform=platform))

    click.echo('Project generated at: {0}'.format(project_dir))
    click.echo('\nDone!')


def __process_ios_project(ios_config: IOSConfig):
    def process_sources(file: str):
        if file.endswith('.swift'):
            text = read_text_file(file)
            text = text.replace(
                ArkDefinitions.PROJECT_NAME_IOS,
                ios_config.project_name)
            text = text.replace(
                ArkDefinitions.PACKAGE_IOS,
                ios_config.app_identifier)
            write_text_file(file, text)

    def process_tests(file: str):
        if file.endswith('.swift'):
            text = read_text_file(file)
            text = text.replace(
                ArkDefinitions.PROJECT_NAME_IOS,
                ios_config.project_name)
            text = text.replace(
                ArkDefinitions.PACKAGE_IOS,
                ios_config.app_identifier)
            text = text.replace(
                f'import ARK', 'import {ios_config.project_name}')
            write_text_file(file, text)

    def process_configs(file: str):
        if file.endswith('.xcconfig'):
            text = read_text_file(file)
            text = text.replace(
                ArkDefinitions.PROJECT_NAME_IOS, ios_config.project_name)
            text = text.replace(
                ArkDefinitions.PACKAGE_IOS, ios_config.app_identifier)
            write_text_file(file, text)

    def __install_ark_tools():
        temp_dir = os.getcwd() + Platform.PATH_SEP + Platform.ARK_TEMP_FOLDER

        shutil.rmtree(temp_dir, True)

        # download latest ark project from branch 'main'
        git_clone(
            ArkDefinitions.REPO_ARK_TOOLS,
            f'{temp_dir}{Platform.PATH_SEP}ark-tools',
            'main'
        )

        os.system(
            f'cd {temp_dir}{Platform.PATH_SEP}ark-tools && bundle install')
        os.system(f'cd {temp_dir}{Platform.PATH_SEP}ark-tools && ' +
                  f'ruby ./ios/sync_project.rb {ios_config.project_dir}')
        shutil.rmtree(temp_dir, True)

    # walk all text file and replace package
    find_files_recursively(
        ios_config.project_dir,
        partial(__on_walk_project_file_ios, ios_config=ios_config))

    env_file = '{0}{1}.env'.format(ios_config.project_dir, Platform.PATH_SEP)
    text = read_text_file(env_file)
    text = text.replace('25EZUPR5QA', ios_config.team_id)
    text = text.replace(
        ArkDefinitions.PROJECT_NAME_IOS,
        ios_config.project_name)
    write_text_file(env_file, text)

    pod_file = f'{ios_config.project_dir}{Platform.PATH_SEP}Podfile'
    text = read_text_file(pod_file)
    text = text.replace(
        ArkDefinitions.PROJECT_NAME_IOS,
        ios_config.project_name)
    write_text_file(pod_file, text)

    sources_path = f'{ios_config.project_dir}{Platform.PATH_SEP}Sources'
    find_dirs_recursively(sources_path, process_sources)

    tests_path = f'{ios_config.project_dir}{Platform.PATH_SEP}Tests'
    find_dirs_recursively(tests_path, process_tests)

    configs_path = f'{ios_config.project_dir}{Platform.PATH_SEP}Configs'
    find_dirs_recursively(configs_path, process_configs)

    shutil.rmtree('{0}{1}{2}.xcworkspace'.format(
        ios_config.project_dir,
        Platform.PATH_SEP,
        ArkDefinitions.PROJECT_NAME_IOS),
        True)

    __install_ark_tools()

    click.echo('Project generated at: {0}'.format(ios_config.project_dir))
    click.echo('\nDone')


def __extract_ios_config(
        project_dir: str,
        name: str,
        platform: str,
        package: str) -> IOSConfig:
    if platform != Platform.IOS:
        return None

    ios_config = IOSConfig()
    ios_config.app_identifier = package
    ios_config.project_name = name
    ios_config.project_dir = project_dir
    ios_config.team_id = click.prompt('Please enter team id')

    return ios_config


def init(name: str, platform: str, package: str):
    current_directory = os.getcwd()

    # list folders of current_directory
    dirs = list(filter(
        lambda x: os.path.isdir(x), os.listdir(current_directory)))

    # check folder exists
    if name in dirs:
        click.echo('Error: Directory name "{0}" already exists!'.format(name))
        exit(-1)

    project_dir = f'{current_directory}{Platform.PATH_SEP}{name}'

    ios_config = __extract_ios_config(project_dir, name, platform, package)

    # download latest ark project from branch 'main'
    git_clone(
        ArkDefinitions.REPO_ANDROID
        if platform == Platform.ANDROID else ArkDefinitions.REPO_IOS,
        project_dir,
        'main')

    # clear .git, .github
    git_cleanup(project_dir)

    # different process on each platform
    if platform == Platform.ANDROID:
        __process_android_project(name, project_dir, package, platform)
    else:
        __process_ios_project(ios_config)
