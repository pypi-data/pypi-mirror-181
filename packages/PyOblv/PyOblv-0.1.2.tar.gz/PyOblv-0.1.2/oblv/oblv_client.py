from typing import Union

import requests
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from oblv.models.name_input import NameInput
from oblv.types import UNSET, Unset

from .api.account import get_user_accounts_account_get
from .api.auth import logout_session_logout_delete
from .api.deployment import (
    create_new_deployment_deployment_post, delete_deployment_deployment_delete,
    generate_build_args_deployment_arguments_get,
    get_available_deployments_deployment_available_get,
    get_deployment_info_deployment_get,
    get_deployment_roles_deployment_roles_get,
    get_supported_regions_deployment_supported_regions_get,
    get_user_owned_deployments_deployment_owned_get)
from .api.repo import (get_all_repos_repo_linked_get,
                       get_repo_from_vcs_repo_get, get_repo_refs_repo_refs_get,
                       get_repo_repo_repo_id_get, link_repo_repo_post,
                       search_repo_from_vcs_repo_search_get,
                       unlink_repo_repo_repo_id_delete)
from .api.service import (
    add_repo_service_repo_service_post,
    delete_repo_services_repo_service_delete,
    get_repo_service_yaml_form_content_repo_service_yaml_get,
    get_repo_services_repo_service_get, get_user_services_service_get,
    update_repo_service_repo_service_put,
    validate_repo_service_repo_service_validate_get)
from .api.user import (add_user_public_shared_key_user_psk_put,
                       get_user_deployment_credit_usage_user_credit_usage_get,
                       get_user_profile_view_user_profile_get,
                       get_user_public_shared_key_user_psk_get,
                       update_user_name_user_name_put,
                       update_user_password_user_password_put)
from .client import AuthenticatedClient
from .config import URL
from .exceptions import BadRequestError, BadYamlData, UnauthorizedTokenError
from .models import (PSK, CreateDeploymentInput, ServiceYamlAddInput,
                     ServiceYamlUpdateInput, UserPasswordInput)


class OblvClient(AuthenticatedClient):

    def logout(self):
        """Logout Session

     This API invalidates the user's token. After a successul response, the user will not be able to use
    the auth token provided in the auth APIs.
    
    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel]]
    """
        try:
            logout_session_logout_delete.sync(
                client=self, oblivious_user_id=self.oblivious_user_id)
        except Exception as e:
            raise e
        finally:
            self.token = ""
            self.oblivious_user_id = ""
    ###### Account Method ######

    def accounts(self):
        """Get User Accounts

     API to fetch user's linked VCS accounts

    Returns:
        Response[Union[Any, HTTPValidationError, List[Account], MessageModel]]
    """
        return get_user_accounts_account_get.sync(client=self, oblivious_user_id=self.oblivious_user_id)

    ############################

    ####### User Methods #######
    def psk(self):
        """Get User PSK

     API to fetch user's psk

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, str]]
    """
        return get_user_public_shared_key_user_psk_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, user_id=self.oblivious_user_id)

    def credit_usage(self):
        """Get User Credit Usage

     API to fetch user's credit usage

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, UserCreditUtilization]]
    """
        return get_user_deployment_credit_usage_user_credit_usage_get.sync(client=self, oblivious_user_id=self.oblivious_user_id)

    def set_psk(self, public_key):
        """Update user's publically shareable key

        API to update user's publically shareable key

        Args:
            public_key (str): Public Key to be shared

        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel, PSK]]
        """

        input = PSK(public_key)
        return add_user_public_shared_key_user_psk_put.sync(client=self, oblivious_user_id=self.oblivious_user_id, json_body=input)

    def update_name(self, name):
        """Update Name

        API to update the name.

        Args:
            name (str): User Name

        Returns:
            Response[Union[Any, HTTPValidationError, MessageModel]]
        """
        return update_user_name_user_name_put.sync(client=self, oblivious_user_id=self.oblivious_user_id, json_body = NameInput(name))

    def update_password(self, old_pass, new_pass):
        """Update User's Password

     API to update user's password

    Args:
        old_pass (str): Old Password
        new_pass (str): New Password

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel]]
    """
        input = UserPasswordInput(old_password=old_pass, password=new_pass)
        return update_user_password_user_password_put.sync(client=self, oblivious_user_id=self.oblivious_user_id, json_body=input)
    
    def user_profile(self):
        """Get User Profile

     API to fetch user's profile details

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, UserProfileResponse]]
    """
        return get_user_profile_view_user_profile_get.sync(client=self, oblivious_user_id=self.oblivious_user_id)
    
    ############################

    ####### Repo Methods #######
    def get_repo(self, repo_id):
        """Get User Repo with Services

     API to fetch user's repo with services created for every repo.

    Args:
        repo_id (str): Repo Id

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]
    """
        return get_repo_repo_repo_id_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id)

    def link_repo(self, owner, name):
        """Link Repo

     API to link a repo to user.

    Args:
        owner (str): Repo Owner
        name (str): Repo Name

    Returns:
        Response[Union[Any, HTTPValidationError, List[RepoAllResponse], MessageModel]]
    """
        return link_repo_repo_post.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_owner=owner, repo_name=name)

    def unlink_repo(self, repo_id):
        """Unlink Repo

     API to unlink a repo from user. It removes the services created under that repo as well.

    Args:
        repo_id (str): Repo Id

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, str]]
    """
        return unlink_repo_repo_repo_id_delete.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id)

    def search_repo(self, keyword):
        """Add Repo Service With Yaml

     API to search a repository in VCS, on which the user has access (via their own account, or by any
    organization they are member of).

    Args:
        keyword (str): Search Keyword

    Returns:
        Response[Union[Any, HTTPValidationError, List[Repo], MessageModel]]
    """
        return search_repo_from_vcs_repo_search_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, search_string=keyword)

    def linked_repos(self):
        """Get User Repos

     API to fetch user's repo without services

    Returns:
        Response[Union[Any, HTTPValidationError, List[RepoAllResponse], MessageModel]]
    """
        return get_all_repos_repo_linked_get.sync(client=self, oblivious_user_id=self.oblivious_user_id)
    # To Do - Change Path

    def repo_refs(self, repo_id):
        """Get Repo Refs

     API to fetch the repository refs (branches and tags).

    If parameter **repo_id** is provided, then it checks for a linked user repo, otherwise, if repo's
    owner and name is given, then the repo is searched in the VCS (all public repos included).

    Note - Either repo id must be provided or its owner and name must be given. A failed response is
    provided if both or none of them are given.

    Args:
        repo_id (str): Repo Id

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, RefResponse]]
    """
        return get_repo_refs_repo_refs_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id)

    def repos(self, page: int = 1, per_page: int = 10):
        """Get Repos From VCS

     API to get all the repositories from VCS, on which the user has access (via their own account, or by
    any organization they are member of).

    Args:
        page (Union[Unset, None, int]):  Page (Default: 1)
        per_page (Union[Unset, None, int]):  Repositiories Per Page (Default: 10)

    Returns:
        Response[Union[Any, HTTPValidationError, VCSRepoResponse]]
    """
        return get_repo_from_vcs_repo_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, page=page, per_page=per_page)
    ############################

    ##### Services Methods #####
    def add_service(self, ref, ref_type="branch", data: dict = {}, repo_id: Union[Unset, str] = UNSET, repo_owner: Union[Unset, str] = UNSET, repo_name: Union[Unset, str] = UNSET):
        """Add Repo Service

     API to create a service after validation.

    Args:
        repo_id (Union[Unset, str]): Repo Id
        repo_owner (Union[Unset, str]): Repo's Owner Name
        repo_name (Union[Unset, str]): Repo Name
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default: 'branch')
        data (dict): Service Yaml Content in dictionary format.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
    """
        if repo_id == UNSET and (repo_name==UNSET or repo_owner==UNSET):
            raise BadRequestError("Either RepoId or Repo name along with Repo Owner's name is required")
        elif repo_id!=UNSET and repo_name!=UNSET and repo_owner!=UNSET:
            print("Warning : Repo Id will be given preference over repo name if they dont belong to same repo.")
        if data!={}:
            try:
                req = requests.get(URL+"/service_schema")
                if req.status_code!=200:
                    raise Exception("Failed to validate service yaml data")
                validate(data,req.json())
            except ValidationError as e:
                raise BadYamlData(e.message)
            except Exception as e:
                raise e
        input = ServiceYamlAddInput.from_dict(
                data)
        return add_repo_service_repo_service_post.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id, ref=ref, ref_type=ref_type, repo_owner=repo_owner, repo_name=repo_name, json_body=input)

    def remove_service(self, ref, ref_type="branch", repo_id: Union[Unset, str] = UNSET, repo_owner: Union[Unset, str] = UNSET, repo_name: Union[Unset, str] = UNSET):
        """Delete Repo Service

     API to delete a service. It does not delete the existing deployments created from this service.

    Args:
        repo_id (Union[Unset, str]): Repo Id
        repo_owner (Union[Unset, str]): Repo's Owner Name
        repo_name (Union[Unset, str]): Repo Name
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default: 'branch')

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel]]
    """
        if repo_id == UNSET and (repo_name==UNSET or repo_owner==UNSET):
            raise BadRequestError("Either RepoId or Repo name along with Repo Owner's name is required")
        elif repo_id!=UNSET and repo_name!=UNSET and repo_owner!=UNSET:
            print("Warning : Repo Id will be given preference over repo name if they dont belong to same repo.")
        return delete_repo_services_repo_service_delete.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id, ref=ref, ref_type=ref_type,repo_name=repo_name,repo_owner=repo_owner)

    def service_content(self, repo_id, ref, ref_type="branch"):
        """Get Repo Service Yaml

     API to fetch the service.yaml content as object for the given service.

    Args:
        repo_id (Union[Unset, str]): Repo Id
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default: 'branch')

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]
    """
        return get_repo_service_yaml_form_content_repo_service_yaml_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id, ref=ref, ref_type=ref_type)

    def repo_services(self, repo_id):
        """Get Repo Services

     API to fetch all the services available for the given repository. This API is valid only for linked
    repositories.

    Args:
        repo_id (str): Repo Id

    Returns:
        Response[Union[Any, HTTPValidationError, List[ValidatedService], MessageModel]]
    """
        return get_repo_services_repo_service_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id)

    def user_services(self):
        """Get User Services

     API to fetch user's services

    Args:

    Returns:
        Response[Union[Any, HTTPValidationError, List[UserServices], MessageModel]]
    """
        return get_user_services_service_get.sync(client=self, oblivious_user_id=self.oblivious_user_id)

    def update_service(self, ref, ref_type="branch", data: dict = {}, repo_id: Union[Unset, str] = UNSET, repo_owner: Union[Unset, str] = UNSET, repo_name: Union[Unset, str] = UNSET):
        """Updaye Repo Service With Yaml

     API to update a service, along with updating the service.yaml file. After updating the service.yaml
    file, the service is validate as well (for missing Dockerfile).

    Args:
        repo_id (Union[Unset, str]): Repo Id
        repo_owner (Union[Unset, str]): Repo's Owner Name
        repo_name (Union[Unset, str]): Repo Name
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default: 'branch')
        data (dict): Service Yaml Content in dictionary format.
        
    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
    """
        if repo_id == UNSET and (repo_name==UNSET or repo_owner==UNSET):
            raise BadRequestError("Either RepoId or Repo name along with Repo Owner's name is required")
        elif repo_id!=UNSET and repo_name!=UNSET and repo_owner!=UNSET:
            print("Warning : Repo Id will be given preference over repo name if they dont belong to same repo.")
        if data!={}:
            try:
                req = requests.get(URL+"/service_schema")
                if req.status_code!=200:
                    raise Exception("Failed to validate service yaml data")
                validate(data,req.json())
            except ValidationError as e:
                raise BadYamlData(e.message)
            except Exception as e:
                raise e
        input = ServiceYamlUpdateInput.from_dict(
                data)
        #     return update_repo_service_with_yaml_repo_service_yaml_put.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id, ref=ref, ref_type=ref_type, json_body=input, repo_owner=repo_owner, repo_name=repo_name)
        return update_repo_service_repo_service_put.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id, ref=ref, ref_type=ref_type, repo_owner=repo_owner, repo_name=repo_name, json_body=input)

    def revalidate_service(self, repo_id, ref, ref_type="branch"):
        """Validate Repo Service

     API to validate a service with supported service schema. The checks include

    - Presence of service.yaml in ./oblivious folder.
    - Presence of Dockerfile in ./oblivious folder.
    - Content of service.yaml must be valid with respect to supported service schema.

    Args:
        repo_id (Union[Unset, None, str]): Repo Id
        ref (str): Service Ref
        ref_type (Union[Unset, None, str]):  Ref Type branch/tag (Default: 'branch')

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
    """
        return validate_repo_service_repo_service_validate_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo_id=repo_id, ref=ref, ref_type=ref_type)
    ############################

    #### Deployment Methods ####

    def deployment_info(self, deployment_id):
        """Get Deployment

     API to fetch a deployment's details.

    Args:
        deployment_id (str): Deployment Id

    Returns:
        Response[Union[Any, DeploymentResponse, HTTPValidationError, MessageModel]]
    """
        return get_deployment_info_deployment_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, deployment_id=deployment_id)

    def create_deployment(self, deployment: CreateDeploymentInput):
        """Create Deployment

     API to create a new deployment.

    Args:
        deployment (CreateDeploymentInput): Deployment Details Input

    Returns:
        Response[Union[Any, CreateDeploymentResponse, HTTPValidationError, MessageModel]]
    """
        return create_new_deployment_deployment_post.sync(client=self, oblivious_user_id=self.oblivious_user_id, json_body=deployment)

    def remove_deployment(self, deployment_id):
        """Delete Deployment

     API to initiate termination of a deployment.

    Args:
        deployment_id (str): Deployment Id

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel]]
    """
        return delete_deployment_deployment_delete.sync(client=self, oblivious_user_id=self.oblivious_user_id, deployment_id=deployment_id)

    def generate_deployment_build_args(self, owner: str,
                                       repo: str,
                                       ref: str):
        """Get Build Deployment Arguments

        API to fetch the arguments schema necessary for creating a deployment. It also gives the commit sha,
        at which point it was generated. This is to be passed to the create deployment API.

        Note - A service could have different build args schema depending on the service's commit history.

        Args:
            owner (str): Repo Owner
            repo (str): Repo Name
            ref (str): Service Ref

        Returns:
            Response[Union[Any, BuildArgsSchema, HTTPValidationError, MessageModel]]
        """
        return generate_build_args_deployment_arguments_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, repo=repo, owner=owner, ref=ref)

    def available_deployments(self):
        """Get Available Deployments

     API to fetch all the deployments the user can connect to.

    Returns:
        Response[Union[Any, HTTPValidationError, List[DeploymentComplete], MessageModel]]
    """
        return get_available_deployments_deployment_available_get.sync(client=self, oblivious_user_id=self.oblivious_user_id)

    def deployment_roles(self, deployment_id):
        """Get Deployment Roles

     API to get a deployment's roles.

    Args:
        deployment_id (str): Deployment Id

    Returns:
        Response[Union[Any, HTTPValidationError, List[RoleResponse], MessageModel]]
    """
        return get_deployment_roles_deployment_roles_get.sync(client=self, oblivious_user_id=self.oblivious_user_id, deployment_id=deployment_id)

    def supported_aws_regions(self):
        """Deployment Supported Regions

     API to fetch a deployment's details.

    Returns:
        Response[Union[Any, MessageModel]]
    """
        return get_supported_regions_deployment_supported_regions_get.sync(client=self)

    def deployments(self):
        """Get Owned Deployments

     API to fetch a user's owned deployments.

    Returns:
        Response[Union[Any, HTTPValidationError, List[DeploymentResponse], MessageModel]]
    """
        return get_user_owned_deployments_deployment_owned_get.sync(client=self, oblivious_user_id=self.oblivious_user_id)

    ############################
