import json
from copy import deepcopy

from ciocore import conductor_submit
from griptape.artifacts import TextArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Literal, Schema


class ConductorTool(BaseTool):
    @activity(
        config={
            "description": "Can be used to execute a conductor submission",
            "schema": Schema(
                {Literal("submission", description="The submission dict"): dict}
            ),
        }
    )
    def submit(self, params: dict) -> TextArtifact:
        SUBMISSION = params["values"].get("submission")
        # host_target = "blender 4.2.1.glibc217 linux"
        # pt = package_tree.PackageTree(api_client.request_software_packages())
        # host_listing = pt.find_by_name(host_target)

        data = deepcopy(SUBMISSION)
        # data["package_id"] = [host_listing["package_id"]]
        # job_env = package_environment.PackageEnvironment(
        #     env_list=host_listing["environment"]
        # )
        # data["environment"] = dict(job_env)

        submission = conductor_submit.Submit(data)
        response, response_code = submission.main()
        print(response_code)
        return TextArtifact(str(json.dumps(response)))
