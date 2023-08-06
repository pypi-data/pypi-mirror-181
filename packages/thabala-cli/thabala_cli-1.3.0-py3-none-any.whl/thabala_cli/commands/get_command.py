"""Get command"""
from thabala_cli.commands.utils.api_client import ApiClient
from thabala_cli.commands.utils.infra_code import VALID_KINDS
from thabala_cli.commands.utils.profile import get_profile


def users(args):
    """Get users"""
    api_client = ApiClient(get_profile(args))
    api_client.get_users(args.limit, args.offset)


def service_instances(args):
    """Get service instances"""
    api_client = ApiClient(get_profile(args))
    api_client.get_service_instances(
        args.limit,
        args.offset,
        args.service_id,
        args.service_instance_id,
        args.service_instance_name,
    )


def service_instance_users(args):
    """Get service instance users"""
    api_client = ApiClient(get_profile(args))
    api_client.get_service_instance_users(
        args.limit, args.offset, args.username, args.service_instance_id
    )


def health(args):
    """Get account health"""
    api_client = ApiClient(get_profile(args))
    api_client.get_health()


def infra(args):
    """Get infrastructure as a code of the Thabala account"""
    api_client = ApiClient(get_profile(args))
    api_client.get_infra(args.kind, valid_kinds=VALID_KINDS)


def network_policy(args):
    """Get network policy rules"""
    api_client = ApiClient(get_profile(args))
    api_client.get_network_policy(args.limit, args.offset)


def version(args):
    """Get account version"""
    api_client = ApiClient(get_profile(args))
    api_client.get_version()
