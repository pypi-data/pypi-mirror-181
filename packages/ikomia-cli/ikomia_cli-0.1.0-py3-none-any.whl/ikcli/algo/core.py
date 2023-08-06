import os
import sys
import re
import stat
import shutil
import logging
import subprocess
import datetime
from rich.progress import Progress, DownloadColumn, TextColumn, BarColumn
from requests_toolbelt.multipart import encoder, MultipartEncoderMonitor
import ikomia
from ikomia import utils
from ikomia.core.auth import LoginSession
from ikomia.core import config

logger = logging.getLogger(__name__)


def remove_read_only(func, path, exc_info):
    # from: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


class PluginMaker:
    def __init__(self, base_class: str, widget_class: str, qt_framework: str):
        self.base_class = base_class
        self.widget_class = widget_class
        self.qt_framework = qt_framework
        self.ik_root_folder = config.main_cfg["root_folder"]
        self.current_folder = os.path.dirname(os.path.realpath(__file__))
        self.plugin_dir = None
        self.plugin_name = None

    def check_name(self, name: str):
        self.plugin_name = re.sub(r"\s+", "", name, flags=re.UNICODE).lower()

    @staticmethod
    def _to_pascal_case(string: str):
        return re.sub(r"(_|-)+", " ", string).title().replace(" ", "")

    @staticmethod
    def _get_full_base_class(base_class: str):
        if base_class == "CWorkflowTask":
            return "core.CWorkflowTask"
        elif base_class == "CWorkflowTaskWidget":
            return "core.CWorkflowTaskWidget"
        else:
            return f"dataprocess.{base_class}"

    def _get_qt_import(self):
        if self.qt_framework == "pyqt":
            return "from PyQt5.QtWidgets import *"
        else:
            return "from PySide2 import QtCore, QtGui, QtWidgets"

    def _get_qt_layout(self):
        if self.qt_framework == "pyqt":
            template_path = os.path.join(self.current_folder, "templates", "pyqt_layout.pyt")
        else:
            template_path = os.path.join(self.current_folder, "templates", "pyside_layout.pyt")

        with open(template_path, "r") as template_file:
            content = template_file.read()
            return content

    def generate(self, name: str):
        self.check_name(name)
        self.plugin_dir = os.path.join(self.ik_root_folder, "Plugins", "Python", name)

        # Create new algorithm directory
        os.makedirs(self.plugin_dir)

        # Create source files
        open(os.path.join(self.plugin_dir, "__init__.py"), "w+")
        open(os.path.join(self.plugin_dir, "requirements.txt"), "w+")
        self._generate_entry_point()
        self._generate_process()
        self._generate_widget()
        self._generate_test()
        return self.plugin_dir

    def _generate_entry_point(self):
        template_path = os.path.join(self.current_folder, "templates", "entry_point.pyt")
        with open(template_path, "r") as template_file:
            class_name = self._to_pascal_case(self.plugin_name)
            content = template_file.read()
            content = content.replace("{{ PluginName }}", self.plugin_name)
            content = content.replace("{{ PluginClassName }}", class_name)

            with open(os.path.join(self.plugin_dir, f"{self.plugin_name}.py"), "w") as f:
                f.write(content)

    def _generate_process(self):
        template_path = os.path.join(self.current_folder, "templates", "process.pyt")
        with open(template_path, "r") as template_file:
            class_name = self._to_pascal_case(self.plugin_name)
            content = template_file.read()
            content = content.replace("{{ PluginName }}", self.plugin_name)
            content = content.replace("{{ PluginClassName }}", class_name)
            content = content.replace("{{ ProcessBaseClass }}", self._get_full_base_class(self.base_class))

            with open(os.path.join(self.plugin_dir, f"{self.plugin_name}_process.py"), "w") as f:
                f.write(content)

    def _generate_widget(self):
        template_path = os.path.join(self.current_folder, "templates", "widget.pyt")
        with open(template_path, "r") as template_file:
            class_name = self._to_pascal_case(self.plugin_name)
            content = template_file.read()
            content = content.replace("{{ PluginName }}", self.plugin_name)
            content = content.replace("{{ PluginClassName }}", class_name)
            content = content.replace("{{ WidgetBaseClass }}", self._get_full_base_class(self.widget_class))
            content = content.replace("{{ QtImport }}", self._get_qt_import())
            content = content.replace("{{ QtLayout }}", self._get_qt_layout())

            with open(os.path.join(self.plugin_dir, f"{self.plugin_name}_widget.py"), "w") as f:
                f.write(content)

    def _generate_test(self):
        template_path = os.path.join(self.current_folder, "templates", "test.pyt")
        with open(template_path, "r") as template_file:
            content = template_file.read()

            with open(os.path.join(self.plugin_dir, f"{self.plugin_name}_test.py"), "w") as f:
                f.write(content)


class Algos:
    def __init__(self, url: str, username: str, password: str):
        # Override Hub url if not empty
        if url:
            self.url = url
            config.main_cfg["hub"]["url"] = url
        else:
            self.url = config.main_cfg["hub"]["url"]

        self.session = None
        if username and password:
            self.session = LoginSession(username=username, pwd=password)

        self.progress = None
        self.progress_task = None
        self.last_bytes_read = 0

    def is_logged(self):
        return self.session is not None

    def login(self, username, password):
        if username and password:
            self.session = LoginSession(username=username, pwd=password)
        else:
            raise ValueError("Authentication failed: invalid user name or password")

    @staticmethod
    def create(name: str, base_class: str, widget_class: str, qt: str):
        maker = PluginMaker(base_class, widget_class, qt)
        return maker.generate(name)

    @staticmethod
    def get_list():
        algo_list = []
        algos = ikomia.ik_registry.getAlgorithms()
        columns = ["Name", "Version", "Language", "Ikomia API"]

        for algo in algos:
            info = ikomia.ik_registry.getAlgorithmInfo(algo)
            if info.internal:
                continue

            if info.language == 0:
                language_str = "C++"
            else:
                language_str = "Python"

            algo_list.append([info.name, info.version, language_str, info.ikomiaVersion])

        return algo_list, columns

    def publish(self, name: str):
        if self.session is None or self.session.token is None:
            raise RuntimeError(f"Authentication failed: unable to publish {name}.")

        ikomia.ik_api_session = self.session
        plugins_dir = ikomia.ik_registry.getPluginsDirectory()
        info = ikomia.ik_registry.getAlgorithmInfo(name)
        online_plugins = ikomia.ik_registry.get_online_algorithms()

        if info.internal:
            raise ValueError("Internal algorithms can't be published.")

        if info.language == utils.ApiLanguage.CPP:
            plugin_dir = os.path.join(plugins_dir, "C++", name)
        else:
            plugin_dir = os.path.join(plugins_dir, "Python", name)

        # Get plugin server id
        server_id = -1
        for plugin in online_plugins:
            if plugin["name"] == name and self._check_compatibility(plugin):
                server_id = plugin["id"]
                info.createdDate = plugin["createdDate"]
                break

        if server_id == -1:
            # Publish new plugin
            server_id = self._add_new_plugin(info)
        else:
            self._update_plugin(server_id, info)

        self._upload_plugin_icon(server_id, info, plugin_dir)
        self._upload_plugin_package(server_id, info, plugin_dir)

    @staticmethod
    def _check_compatibility(plugin):
        language = utils.ApiLanguage.CPP if plugin["language"] == 0 else utils.ApiLanguage.PYTHON
        if language == utils.ApiLanguage.PYTHON:
            return True
        else:
            return utils.checkArchitectureKeywords(plugin["keywords"])

    def _add_new_plugin(self, info):
        plugin_data = self._get_plugin_json(info)
        url = self.url + "/api/plugin/"
        r = ikomia.ik_api_session.session.post(url, json=plugin_data)
        r.raise_for_status()
        r_data = r.json()
        logger.debug(f"New algorithm {info.name} is added to Ikomia HUB")
        return r_data["id"]

    def _update_plugin(self, plugin_id, info):
        plugin_data = self._get_plugin_json(info)
        url = self.url + "/api/plugin/" + str(plugin_id) + "/"
        r = ikomia.ik_api_session.session.put(url, json=plugin_data)
        r.raise_for_status()

    @staticmethod
    def _get_plugin_json(info):
        if info.language == utils.ApiLanguage.CPP:
            language = 0
        else:
            language = 1

        if info.os == utils.OSType.ALL:
            op_system = 0
        elif info.os == utils.OSType.LINUX:
            op_system = 1
        elif info.os == utils.OSType.WIN:
            op_system = 2
        elif info.os == utils.OSType.OSX:
            op_system = 3

        modification_date = datetime.datetime.now().replace(microsecond=0).isoformat()

        creation_date = info.createdDate
        if not creation_date:
            creation_date = modification_date

        data = {"name": info.name, "short_description": info.shortDescription, "description": info.description,
                "keywords": info.keywords, "authors": info.authors, "article": info.article,
                "journal": info.journal, "year": info.year, "docLink": info.documentationLink,
                "license": info.license, "repository": info.repository, "createdDate": creation_date,
                "modifiedDate": modification_date, "version": info.version, "ikomiaVersion": info.ikomiaVersion,
                "language": language, "os": op_system}

        return data

    def _upload_plugin_icon(self, plugin_id, info, directory):
        if not info.iconPath:
            logger.debug(f"No icon found for {info.name}")
            return

        icon_path = directory + os.sep + info.iconPath
        url = self.url + "/api/plugin/" + str(plugin_id) + "/icon/"
        form = encoder.MultipartEncoder({
            "iconFile": (os.path.basename(icon_path), open(icon_path, 'rb'), "image/png"),
        })
        headers = {"Prefer": "respond-async", "Content-Type": form.content_type}

        self.progress = Progress(
            TextColumn(f"Uploading {info.name} icon"),
            BarColumn(),
            DownloadColumn())

        with self.progress:
            self.last_bytes_read = 0
            self.progress_task = self.progress.add_task("Download", total=os.path.getsize(icon_path))
            multipart_monitor = MultipartEncoderMonitor(
                form,
                callback=self._update_progress
            )
            r = ikomia.ik_api_session.session.put(url, headers=headers, data=multipart_monitor)
            r.raise_for_status()

        logger.debug(f"{info.name} icon uploaded")

    def _upload_plugin_package(self, plugin_id, info, plugin_dir):
        plugins_dir = ikomia.ik_registry.getPluginsDirectory()
        plugin_dir_name = info.name.replace(" ", "")
        dst_dir = os.path.join(plugins_dir, "Transfer", plugin_dir_name)

        # Copy plugin directory
        shutil.copytree(plugin_dir, dst_dir)

        # Remove .git folder
        for subdir in os.listdir(dst_dir):
            if subdir.endswith('.git'):
                tmp = os.path.join(dst_dir, subdir)

                if sys.platform == "win32":
                    # We want to make visible the .git folder before unlinking it.
                    while True:
                        subprocess.call(['attrib', '-H', tmp])
                        break

                shutil.rmtree(tmp, onerror=remove_read_only)

        # zip plugin
        logger.debug("Algorithm package compression...")
        zip_path = dst_dir
        shutil.make_archive(zip_path, "zip", dst_dir)
        zip_path += ".zip"

        # Remove plugin dir
        shutil.rmtree(dst_dir)

        # upload
        logger.debug("Uploading package...")
        url = self.url + "/api/plugin/" + str(plugin_id) + "/package/"

        with open(zip_path, 'rb') as zip_file:
            form = encoder.MultipartEncoder({
                "packageFile": (os.path.basename(zip_path), zip_file, "application/zip"),
            })
            headers = {"Prefer": "respond-async", "Content-Type": form.content_type}

            self.progress = Progress(
                    TextColumn(f"Uploading {info.name} package"),
                    BarColumn(),
                    DownloadColumn())

            with self.progress:
                self.last_bytes_read = 0
                self.progress_task = self.progress.add_task("Download", total=os.path.getsize(zip_path))
                multipart_monitor = MultipartEncoderMonitor(
                    form,
                    callback=self._update_progress
                )
                r = ikomia.ik_api_session.session.put(url, headers=headers, data=multipart_monitor)
                r.raise_for_status()

        os.remove(zip_path)
        logger.debug(f"{info.name} package uploaded")

    def _update_progress(self, monitor):
        advance = monitor.bytes_read - self.last_bytes_read
        self.progress.update(self.progress_task, advance=advance)
        self.last_bytes_read = monitor.bytes_read
