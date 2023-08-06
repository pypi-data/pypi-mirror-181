from typing import Any

from algora.api.service.project.package.model import ProjectPackageRequest


def _get_project_package_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/project/package/{id}"
    }


def _get_project_packages_request_info() -> dict:
    return {
        'endpoint': f"config/project/package"
    }


def _create_project_package_request_info(request: ProjectPackageRequest) -> dict:
    return {
        'endpoint': f"config/project/package",
        'json': request.request_dict()
    }


def _update_project_package_request_info(id: str, request: ProjectPackageRequest) -> dict:
    return {
        'endpoint': f"config/project/package/{id}",
        'json': request.request_dict()
    }


def _delete_project_package_request_info(id: str) -> dict:
    return {
        'endpoint': f"config/project/package/{id}"
    }
