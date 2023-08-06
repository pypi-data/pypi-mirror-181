"""Destroy command"""
from thabala_cli.commands.utils.infra_code import InfraCode
from thabala_cli.commands.utils.profile import get_profile


def destroy(args):
    """Destroy an infrastructure component"""
    profile = get_profile(args)
    infra_code = InfraCode(profile)

    infra_code.destroy_yaml(args.file)
