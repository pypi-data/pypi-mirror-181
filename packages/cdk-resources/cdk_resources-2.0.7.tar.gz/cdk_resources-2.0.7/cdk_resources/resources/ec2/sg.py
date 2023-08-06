from aws_cdk import aws_ec2

from cdk_resources.resources.base import Resource
from cdk_resources.utils import combine_configurations


__all__ = ("BaseSecurityGroup",)


class BaseSecurityGroup(Resource[aws_ec2.SecurityGroup]):
    # Others
    sg_ingress_rules_props = None

    @classmethod
    def post_create(cls, construct: aws_ec2.SecurityGroup) -> None:
        sg_ingress_rules_props = combine_configurations(
            cls.sg_ingress_rules_props or {}
        )
        for rules in sg_ingress_rules_props["ingress_rules"]:
            construct.add_ingress_rule(**rules)
