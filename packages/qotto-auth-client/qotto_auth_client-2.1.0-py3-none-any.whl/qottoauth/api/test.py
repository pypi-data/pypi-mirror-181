from datetime import datetime, timezone
from typing import Any, Tuple, Optional
from uuid import uuid4

from qottoauth import Namespace, Matching
from qottoauth.api.base import QottoAuthApi, QottoAuthApiError
from qottoauth.models import (
    Role,
    Organization,
    Identity,
    Account,
    Application,
    Permission,
    Authorization,
    Member,
    User,
    UserRequest,
    Actor,
    Cookie,
    CookiePair,
)

__all__ = [
    'QottoAuthTestApi',
]


def gen_uuid():
    return str(uuid4())


class QottoAuthTestApi(QottoAuthApi):

    def __init__(self):
        self._applications: dict[str, Application] = {}
        self._accounts: dict[str, Account] = {}
        self._permissions: dict[str, Permission] = {}
        self._authorizations: dict[str, Authorization] = {}
        self._authorization_permissions: dict[str, set[str]] = {}
        self._roles: dict[str, Role] = {}
        self._role_authorizations: dict[str, set[str]] = {}
        self._members: dict[str, Member] = {}
        self._member_cookies: dict[str, tuple[str, str]] = {}
        self._member_roles: dict[str, set[str]] = {}
        self._member_authorizations: dict[str, set[str]] = {}
        self._organizations: dict[str, Organization] = {}
        self._users: dict[str, User] = {}
        self._user_cookies: dict[str, tuple[str, str]] = {}
        self._identities: dict[str, Identity] = {}
        self._identity_tickets: dict[str, str] = {}
        self._user_requests: dict[str, UserRequest] = {}
        self._last_change_date: datetime = datetime.now(timezone.utc)

    def query(
            self,
            name: str,
            variables: list[Tuple[str, str, Any]] = None,
            body: str = None,
    ):
        kwargs = {}
        if variables:
            for var_name, var_type, var_value in variables:
                kwargs[var_name] = var_value
        if hasattr(self, name):
            try:
                return getattr(self, name)(**kwargs)
            except Exception as e:
                raise QottoAuthApiError from e
        raise QottoAuthApiError(f"Unknown query {name}")

    def mutation(
            self,
            name: str,
            body: str,
            input_name: str = 'input',
            input_type: str = None,
            input_value: dict[str, Any] = None,
    ):
        if hasattr(self, name):
            try:
                result = getattr(self, name)(**input_value)
                self._last_change_date = datetime.now(timezone.utc)
                return result
            except Exception as e:
                raise QottoAuthApiError from e
        raise QottoAuthApiError(f"Unknown mutation {name}")

    def lastChangeDate(self) -> str:
        return self._last_change_date.isoformat()

    def application(self, id) -> dict:
        if id in self._applications:
            return self._applications[id].to_dict()
        raise QottoAuthApiError(f"Application {id} does not exists")

    def applications(self, name_Icontains: str = None) -> dict:
        nodes = []
        for application in self._applications.values():
            if name_Icontains is None or name_Icontains.lower() in application.name.lower():
                nodes.append(application.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createApplication(self, name: str, description: str) -> dict:
        for application in self._applications.values():
            if application.name == name:
                raise QottoAuthApiError(f"Application {name} already exists")
        application = Application(gen_uuid(), name, description)
        self._applications[application.id] = application
        return dict(application=application.to_dict())

    def registerApplication(self, name, description) -> dict:
        for application in self._applications.values():
            if application.name == name:
                updated_application: Application = application.update(description=description)
                self._applications[application.id] = updated_application
                return dict(application=updated_application.to_dict())
        new_application = Application(gen_uuid(), name, description)
        self._applications[new_application.id] = new_application
        return dict(application=new_application.to_dict())

    def deleteApplication(self, applicationId: str) -> dict:
        if applicationId in self._applications:
            del self._applications[applicationId]
            for permission in list(self._permissions.values()):
                if permission.application.id == applicationId:
                    self.deletePermission(permission.id)
            for account in list(self._accounts.values()):
                if account.application.id == applicationId:
                    self.deleteAccount(account.id)
            return dict(deleted=True)
        return dict(deleted=False)

    def permission(self, id) -> dict:
        if id in self._permissions:
            return self._permissions[id].to_dict()
        raise QottoAuthApiError(f"Permission {id} does not exists")

    def permissions(
            self, name_Icontains: str = None,
            application_Id: str = None, authorization_Id: str = None
    ) -> dict:
        nodes = []
        for permission in self._permissions.values():
            if name_Icontains is not None and name_Icontains.lower() not in permission.name.lower():
                continue
            if application_Id is not None and application_Id != permission.application.id:
                continue
            if authorization_Id is not None and permission.id not in self._authorization_permissions.get(
                    authorization_Id, []
            ):
                continue
            nodes.append(permission.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createPermission(self, applicationId: str, name: str, description: str) -> dict:
        application = self._applications[applicationId]
        for permission in self._permissions.values():
            if permission.name == name and permission.application.id == application.id:
                raise QottoAuthApiError(f"Permission {name} already exists for this application")
        permission = Permission(gen_uuid(), application, name, description)
        self._permissions[permission.id] = permission
        return dict(permission=permission.to_dict())

    def registerPermission(self, applicationId: str, name, description) -> dict:
        application = self._applications[applicationId]
        for permission in self._permissions.values():
            if permission.name == name and permission.application.id == application.id:
                updated_permission: Permission = permission.update(description=description)
                self._permissions[permission.id] = updated_permission
                return dict(permission=updated_permission.to_dict())
        new_permission = Permission(gen_uuid(), application, name, description)
        self._permissions[new_permission.id] = new_permission
        return dict(permission=new_permission.to_dict())

    def deletePermission(self, permissionId: str) -> dict:
        if permissionId in self._permissions:
            del self._permissions[permissionId]
            for authorization_id, permission_id_set in self._authorization_permissions.items():
                permission_id_set.discard(permissionId)
            return dict(deleted=True)
        return dict(deleted=False)

    def organization(self, id: str) -> dict:
        if id in self._organizations:
            return self._organizations[id].to_dict()
        raise QottoAuthApiError(f"Organization {id} does not exists")

    def organizations(self, name_Icontains: str = None, namespace_Icontains: str = None) -> dict:
        nodes = []
        for organization in self._organizations.values():
            if name_Icontains is None or name_Icontains.lower() in organization.name.lower():
                if namespace_Icontains is None or namespace_Icontains.lower() in str(organization.namespace).lower():
                    nodes.append(organization.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createOrganization(self, name: str, namespace: str) -> dict:
        for organization in self._organizations.values():
            if organization.namespace == namespace:
                raise QottoAuthApiError(f"Organization {namespace} already exists")
        organization = Organization(gen_uuid(), name, Namespace(namespace))
        self._organizations[organization.id] = organization
        return dict(organization=organization.to_dict())

    def deleteOrganization(self, organizationId: str) -> dict:
        if organizationId in self._organizations:
            del self._organizations[organizationId]
            for member in list(self._members.values()):
                if member.organization.id == organizationId:
                    self.deleteMember(member.id)
            for authorization in list(self._authorizations.values()):
                if authorization.organization.id == organizationId:
                    self.deleteAuthorization(authorization.id)
            for role in list(self._roles.values()):
                if role.organization.id == organizationId:
                    self.deleteRole(role.id)
            return dict(deleted=True)
        return dict(deleted=False)

    def user(self, id: str) -> dict:
        if id in self._users:
            return self._users[id].to_dict()
        raise QottoAuthApiError(f"User {id} does not exists")

    def users(self, name_Icontains: str = None, associated: bool = None) -> dict:
        nodes = []
        for user in self._users.values():
            if name_Icontains is not None and name_Icontains.lower() not in user.name.lower():
                continue
            if associated is not None:
                for identity in self._identities.values():
                    if identity.user and identity.user.id == user.id:
                        has_identity = True
                        break
                else:
                    has_identity = False
                if associated != has_identity:
                    continue
            nodes.append(user.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createUser(self, name: str, email: str, uuid: str = None, **kwargs) -> dict:
        uuid = uuid or gen_uuid()
        user = User(uuid, name, False)
        self._users[user.id] = user
        self._user_cookies[user.id] = str(uuid4()), str(uuid4())
        return dict(user=user.to_dict())

    def updateUser(
            self, userId: str, addIdentityId: str = None, removeIdentityId: str = None,
            **kwargs,
    ) -> dict:
        user = self._users[userId]
        if addIdentityId:
            add_identity = self._identities[addIdentityId]
            if add_identity.user:
                raise QottoAuthApiError(f"Identity {addIdentityId} already belongs to user {add_identity.user.id}")
            self._identities[addIdentityId] = add_identity.update(user=user)
        if removeIdentityId:
            remove_identity = self._identities[removeIdentityId]
            if not remove_identity.user or remove_identity.user.id != userId:
                raise QottoAuthApiError(f"Identity {removeIdentityId} does not belongs to user {userId}")
            self._identities[removeIdentityId] = remove_identity.update(user=None)
        return dict(user=user.to_dict())

    def createUserFromIdentity(self, identityId: str) -> dict:
        identity = self._identities[identityId]
        user = User(gen_uuid(), identity.name, False)
        self._users[user.id] = user
        self._user_cookies[user.id] = str(uuid4()), str(uuid4())
        self._identities[identityId] = identity.update(user=user)
        return dict(user=user.to_dict())

    def deleteUser(self, userId: str) -> dict:
        if userId in self._users:
            del self._users[userId]
            del self._user_cookies[userId]
            for member in list(self._members.values()):
                if member.user.id == userId:
                    self.deleteMember(member.id)
            for account in list(self._accounts.values()):
                if account.user.id == userId:
                    self.deleteAccount(account.id)
            for user_request in list(self._user_requests.values()):
                if user_request.user.id == userId:
                    self.deleteUserRequest(user_request.id)
            return dict(deleted=True)
        return dict(deleted=False)

    def identity(self, id: str) -> dict:
        if id in self._identities:
            identity = self._identities[id]
            return identity.to_dict()
        raise QottoAuthApiError(f"Identity {id} does not exists")

    def identities(
            self,
            name_Icontains: str = None, email_Icontains: str = None,
            providerId: str = None,
            associated: bool = None, user_Id: str = None,
            blocked: bool = None,
    ) -> dict:
        nodes = []
        for identity in self._identities.values():
            if providerId is not None and identity.provider_id != providerId:
                continue
            if name_Icontains is not None and name_Icontains.lower() not in identity.name.lower():
                continue
            if email_Icontains is not None and email_Icontains.lower() not in identity.email.lower():
                continue
            if associated is not None and associated != (identity.user is not None):
                continue
            if user_Id is not None and (identity.user is None or identity.user.id != user_Id):
                continue
            if blocked is not None and blocked != identity.blocked:
                continue
            nodes.append(identity.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def registerIdentity(self, providerId: str, idToken: str) -> dict:
        if providerId != 'dummy':
            raise QottoAuthApiError(f"Provider {providerId} does not exists.")
        identity_uuid, identity_name, identity_email = idToken.split(':')
        if identity_uuid not in self._identities:
            self._identities[identity_uuid] = Identity(
                id=identity_uuid, name=identity_name, provider_id=providerId,
                email=identity_email, user=None, blocked=False
            )
            self._identity_tickets[identity_uuid] = str(uuid4())
        return dict(identity=self._identities[identity_uuid].to_dict())

    def updateIdentity(self, identityId: str, setBlocked: bool = None) -> dict:
        identity = self._identities[identityId]
        if setBlocked is not None and setBlocked != identity.blocked:
            identity = identity.update(blocked=setBlocked)
            self._identities[identityId] = identity
        return dict(identity=identity.to_dict())

    def deleteIdentity(self, identityId: str) -> dict:
        if identityId in self._identities:
            del self._identities[identityId]
            del self._identity_tickets[identityId]
            for user_request in list(self._user_requests.values()):
                if user_request.identity.id == identityId:
                    self.deleteUserRequest(user_request.id)
            return dict(deleted=True)
        return dict(deleted=False)

    def authorization(self, id: str) -> dict:
        if id in self._authorizations:
            return self._authorizations[id].to_dict()
        raise QottoAuthApiError(f"Authorization {id} does not exists")

    def authorizations(
            self, name_Icontains: str = None,
            organization_Id: str = None,
            member_Id: str = None, permission_Id: str = None, role_Id: str = None,
    ) -> dict:
        nodes = []
        for authorization in self._authorizations.values():
            if name_Icontains is not None and name_Icontains.lower() not in authorization.name.lower():
                continue
            if organization_Id is not None and authorization.organization.id != organization_Id:
                continue
            if member_Id is not None and authorization.id not in self._member_authorizations[member_Id]:
                continue
            if permission_Id is not None and permission_Id not in self._authorization_permissions[authorization.id]:
                continue
            if role_Id is not None and authorization.id not in self._role_authorizations[role_Id]:
                continue
            nodes.append(authorization.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createAuthorization(
            self, name: str, description: str,
            organizationId: str, matching: str, inheritance: bool,
    ) -> dict:
        organization = self._organizations[organizationId]
        authorization = Authorization(
            id=gen_uuid(), name=name, description=description,
            organization=organization, inheritance=inheritance, matching=Matching(matching),
        )
        self._authorizations[authorization.id] = authorization
        self._authorization_permissions[authorization.id] = set()
        return dict(authorization=authorization.to_dict())

    def updateAuthorization(
            self, authorizationId: str,
            addPermissionId: str = None, removePermissionId: str = None,
    ):
        if addPermissionId is not None:
            self._authorization_permissions[authorizationId].add(addPermissionId)
        if removePermissionId is not None:
            self._authorization_permissions[authorizationId].discard(removePermissionId)
        return dict(authorization=self._authorizations[authorizationId].to_dict())

    def deleteAuthorization(self, authorizationId: str) -> dict:
        if authorizationId in self._authorizations:
            del self._authorizations[authorizationId]
            del self._authorization_permissions[authorizationId]
            for role_id, authorization_id_set in self._role_authorizations.items():
                authorization_id_set.discard(authorizationId)
            for member_id, authorization_id_set in self._member_authorizations.items():
                authorization_id_set.discard(authorizationId)
            return dict(deleted=True)
        return dict(deleted=False)

    def role(self, id: str) -> dict:
        if id in self._roles:
            return self._roles[id].to_dict()
        raise QottoAuthApiError(f"Role {id} does not exists")

    def roles(
            self, name_Icontains: str = None,
            organization_Id: str = None,
            member_Id: str = None, authorization_Id: str = None,
    ) -> dict:
        nodes = []
        for role in self._roles.values():
            if name_Icontains is not None and name_Icontains.lower() not in role.name.lower():
                continue
            if organization_Id is not None and role.organization.id != organization_Id:
                continue
            if member_Id is not None and role.id not in self._member_roles[member_Id]:
                continue
            if authorization_Id is not None and authorization_Id not in self._role_authorizations[role.id]:
                continue
            nodes.append(role.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createRole(self, name: str, description: str, organizationId: str, inheritance: bool) -> dict:
        organization = self._organizations[organizationId]
        role = Role(
            id=gen_uuid(), name=name, description=description, organization=organization, inheritance=inheritance
        )
        self._roles[role.id] = role
        self._role_authorizations[role.id] = set()
        return dict(role=role.to_dict())

    def updateRole(
            self, roleId: str,
            addAuthorizationId: str = None, removeAuthorizationId: str = None,
    ) -> dict:
        if addAuthorizationId is not None:
            self._role_authorizations[roleId].add(addAuthorizationId)
        if removeAuthorizationId is not None:
            self._role_authorizations[roleId].discard(removeAuthorizationId)
        return dict(role=self._roles[roleId].to_dict())

    def deleteRole(self, roleId: str) -> dict:
        if roleId in self._roles:
            del self._roles[roleId]
            del self._role_authorizations[roleId]
            for member_id, role_id_set in self._member_roles.items():
                role_id_set.discard(roleId)
            return dict(deleted=True)
        return dict(deleted=False)

    def member(self, id: str) -> dict:
        if id in self._members:
            return self._members[id].to_dict()
        raise QottoAuthApiError(f"Member {id} does not exists")

    def members(self, user_Id: str = None, organization_Id: str = None) -> dict:
        nodes = []
        for member in self._members.values():
            if user_Id is None or user_Id == member.user.id:
                if organization_Id is None or organization_Id == member.organization.id:
                    nodes.append(member.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createMember(self, userId: str, organizationId: str) -> dict:
        user = self._users[userId]
        organization = self._organizations[organizationId]
        member = Member(gen_uuid(), user, organization)
        self._members[member.id] = member
        self._member_cookies[member.id] = str(uuid4()), str(uuid4())
        self._member_authorizations[member.id] = set()
        self._member_roles[member.id] = set()
        return dict(member=member.to_dict())

    def updateMember(
            self, memberId: str,
            addAuthorizationId: str = None, removeAuthorizationId: str = None,
            addRoleId: str = None, removeRoleId: str = None,
    ):
        if addAuthorizationId is not None:
            self._member_authorizations[memberId].add(addAuthorizationId)
        if removeAuthorizationId is not None:
            self._member_authorizations[memberId].discard(removeAuthorizationId)
        if addRoleId is not None:
            self._member_roles[memberId].add(addRoleId)
        if removeRoleId is not None:
            self._member_roles[memberId].discard(removeRoleId)
        return dict(member=self._members[memberId].to_dict())

    def deleteMember(self, memberId: str) -> dict:
        if memberId in self._members:
            del self._members[memberId]
            del self._member_authorizations[memberId]
            del self._member_roles[memberId]
            del self._member_cookies[memberId]
            return dict(deleted=True)
        return dict(deleted=False)

    def account(self, id: str) -> dict:
        if id in self._accounts:
            return self._accounts[id].to_dict()
        raise QottoAuthApiError(f"Account {id} does not exists")

    def accounts(
            self,
            user_Id: str = None, application_Id: str = None,
            enabled: bool = None,
    ) -> dict:
        nodes = []
        for account in self._accounts.values():
            if user_Id is not None and user_Id != account.user.id:
                continue
            if application_Id is not None and application_Id != account.application.id:
                continue
            if enabled is not None and enabled != account.enabled:
                continue
            nodes.append(account.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def createAccount(self, userId: str, applicationId: str) -> dict:
        user = self._users[userId]
        application = self._applications[applicationId]
        account = Account(id=gen_uuid(), user=user, application=application, enabled=True, data={})
        self._accounts[account.id] = account
        return dict(account=account.to_dict())

    def updateAccount(self, accountId: str, setEnabled: bool = None) -> dict:
        account = self._accounts[accountId]
        if setEnabled is not None and setEnabled != account.enabled:
            account = account.update(enabled=setEnabled)
            self._accounts[accountId] = account
        return dict(account=account.to_dict())

    def deleteAccount(self, accountId: str) -> dict:
        if accountId in self._accounts:
            del self._accounts[accountId]
            return dict(deleted=True)
        return dict(deleted=False)

    def createUserRequest(self, userId: str, identityId: str, comment: str = None) -> dict:
        user = self._users[userId]
        identity = self._identities[identityId]
        if self.userRequests(userId=userId)['edges']:
            raise QottoAuthApiError(f"User request for user {userId} already exists")
        if self.userRequests(identityId=identityId)['edges']:
            raise QottoAuthApiError(f"User request for identity {identityId} already exists")
        request = UserRequest(id=gen_uuid(), user=user, identity=identity, comment=comment)
        self._user_requests[request.id] = request
        return dict(userRequest=request.to_dict())

    def userRequest(self, id: str) -> dict:
        if id in self._user_requests:
            return self._user_requests[id].to_dict()
        raise QottoAuthApiError(f"User request {id} does not exists")

    def userRequests(self, userId: str = None, identityId: str = None) -> dict:
        nodes = []
        for request in self._user_requests.values():
            if userId is not None and userId != request.user.id:
                continue
            if identityId is not None and identityId != request.identity.id:
                continue
            nodes.append(request.to_dict())
        return dict(edges=[dict(node=node) for node in nodes])

    def deleteUserRequest(self, requestId: str) -> dict:
        if requestId in self._user_requests:
            del self._user_requests[requestId]
            return dict(deleted=True)
        return dict(deleted=False)

    def identityTicket(self, identityId: str) -> str:
        if identityId in self._identity_tickets:
            return self._identity_tickets[identityId]
        raise QottoAuthApiError(f"Identity ticket {identityId} does not exists")

    def checkIdentityTicket(self, identityTicket: str) -> str:
        for identityId, ticket in self._identity_tickets.items():
            if ticket == identityTicket:
                return identityId
        raise QottoAuthApiError(f"Identity ticket {identityTicket} does not exists")

    def actor(self, tokenCookie: str = None, secretCookie: str = None) -> dict:
        for member_id, cookies in self._member_cookies.items():
            if cookies == (tokenCookie, secretCookie):
                member = self._members[member_id]
                actor = Actor(user=member.user, member=member)
                return actor.to_dict()
        for user_id, cookies in self._user_cookies.items():
            if cookies == (tokenCookie, secretCookie):
                user = self._users[user_id]
                actor = Actor(user=user)
                return actor.to_dict()
        return Actor().to_dict()

    def cookies(self, userId: str = None, organizationId: str = None) -> dict:
        if userId and organizationId:
            for member in self._members.values():
                if member.organization.id == organizationId and member.user.id == userId:
                    token, secret = self._member_cookies[member.id]
                    break
            else:
                raise QottoAuthApiError(f"Member {userId} does not exists in organization {organizationId}")
        elif userId:
            if userId in self._user_cookies:
                token, secret = self._user_cookies[userId]
            else:
                raise QottoAuthApiError(f"User {userId} does not exists")
        else:
            token, secret = '', ''
        cookie_pair = CookiePair(
            token_cookie=Cookie(
                name='token', value=token, domain='localhost',
                max_age=0, secure=False, http_only=False,
            ),
            secret_cookie=Cookie(
                name='secret', value=secret, domain='localhost',
                max_age=0, secure=False, http_only=True,
            ),
        )
        return cookie_pair.to_dict()

    def isAuthorized(
            self,
            actorId: str,
            permissionId: str,
            organizationId: str = None,
    ) -> bool:
        member: Member
        if actorId in self._members:
            member = self._members[actorId]
        elif actorId in self._users:
            return self._users[actorId].is_superuser
        else:
            return False
        member_namespace = member.organization.namespace
        permission = self._permissions[permissionId]
        namespace: Optional[Namespace] = None
        if organizationId in self._organizations:
            namespace = self._organizations[organizationId].namespace
        elif organizationId is not None:
            namespace = Namespace(organizationId)

        all_authorizations: set[Authorization] = set()
        for authorization_id in self._member_authorizations[member.id]:
            all_authorizations.add(self._authorizations[authorization_id])
        for role_id in self._member_roles[member.id]:
            role = self._roles[role_id]
            for authorization_id in self._role_authorizations[role.id]:
                all_authorizations.add(self._authorizations[authorization_id])
        for authorization in all_authorizations:
            authorization_matching = authorization.matching
            authorization_namespace = authorization.organization.namespace
            if permission.id in self._authorization_permissions[authorization.id]:
                if not namespace:
                    return True
                if (
                        (authorization.inheritance and authorization_namespace >= namespace)
                        or authorization_namespace == namespace
                ):
                    if namespace.matches(member_namespace, authorization_matching):
                        return True
        return False
