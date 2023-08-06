"""Project API Object."""
import base64
from pathlib import Path

from yarl import URL

from ikcli.net.api import List, Object
from ikcli.net.http.core import HTTPRequest

from .archive import Archive


class Deployment(Object):
    """Deployment API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of Deployment object.

        :return: Deployment object representation
        """
        return f"Deployment {self['provider']} {self['region']} {self['flavour']} {self['endpoint']}"

    def run(self, task: str, image: str, output_indexes: list = None) -> list:
        """
        Call deployment endpoint.

        :param task: Task name to call
        :param image: Image filename to give
        :param output_indexes: List of output index to retreive. None = All
        :return: A list of output. Each one is a dict that contains 'type' and 'data'.
        """
        # Load image and encode to b64
        with open(image, "rb") as fh:
            b64_image = base64.b64encode(fh.read()).decode("UTF-8")

        # Craft data
        if output_indexes is None or len(output_indexes) == 0:
            outputs = [{"task_name": task, "task_index": 0}]
        else:
            outputs = [{"task_name": task, "task_index": 0, "output_index": index} for index in output_indexes]
        data = {
            "inputs": [{"image": b64_image}],
            "outputs": outputs,
            "parameters": [],
        }

        # Query endpoint
        outputs = HTTPRequest(URL(self["endpoint"]), timeout=180).put(URL("/run"), data)
        for output in outputs:
            # Convert b64 to binary if needed
            if output["type"] == "IMAGE" or output["type"] == "IMAGE_BINARY":
                output["data"] = base64.b64decode(output["data"]["image"])

        # Return outputs
        return outputs


class Deployments(List):
    """Deployment API List."""

    def __init__(self, http: HTTPRequest, url: URL):
        super().__init__(http, url, Deployment)


class Workflow(Object):
    """Workflow API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of Workflow object.

        :return: Workflow object representation
        """
        return f"Workflow {self['name']}"

    @property
    def deployments(self) -> Deployments:
        """
        Return workflow deployment list.

        :return: workflow deployment list
        """
        return Deployments(self._http, self._url / "deployments/")


class Workflows(List):
    """Workflow API List."""

    def __init__(self, http: HTTPRequest, url: URL):
        super().__init__(http, url, Workflow)

    def create(self, filename: Path) -> Workflow:
        """
        Create a new workflow from filename.

        :param filename: Workflow json file name
        :return: A new workflow
        """
        with Archive(filename) as zfh:
            data = self._http.post(self._url, None, files={"archive": zfh})
            return Workflow(self._http, URL(data["url"]), data=data)


class Project(Object):
    """Project API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of object.

        :return:  object representation
        """
        return f"Project {self['name']}"

    @property
    def workflows(self) -> Workflows:
        """
        Return project workflow list.

        :return: Project workflow list
        """
        return Workflows(self._http, self._url / "workflows/")


class Projects(List):
    """Project API List."""

    def __init__(self, http, url: URL = None):
        if url is None:
            url = URL("/v1/projects/")
        super().__init__(http, url, Project)
