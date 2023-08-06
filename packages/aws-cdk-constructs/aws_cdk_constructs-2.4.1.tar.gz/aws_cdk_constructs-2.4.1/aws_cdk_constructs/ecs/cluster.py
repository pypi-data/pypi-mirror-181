from __future__ import annotations

from os import getenv
from typing import List, Optional, TYPE_CHECKING, Dict

from aws_cdk import (
    aws_ecs as _ecs,
    aws_ec2 as _ec2,
    aws_elasticloadbalancingv2 as _elb,
    aws_route53 as _route53,
)
from constructs import Construct

if TYPE_CHECKING:
    from .microservice import ECSMicroservice


class ECSCluster(Construct):
    """
        A CDK construct that creates an AWS ECS Cluster.
        This cluster is the placeholder where ECSMicroservices will be deployed to

    Args:
            scope (Construct): Parent construct

            id (str): the logical id of the newly created resource

            environment_parameters (dict): The dictionary containing the references to CSI AWS environments. This will simplify the environment promotions and enable a parametric development of the infrastructures.

            domain_name (str): every cluster has associated a route53 hosted zone, where entries will be created to

            hosted_zone (aws_route53.IHostedZone): Route53 hosted zone where the cluster will create entries for the microservices

            lb_listener (aws_elasticloadbalancingv2.ApplicationListener): Listener of the LB that will proxy all request to the cluster components

            app_name (str): The name of the application that will be deployed in the cluster
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        environment_parameters: Dict,
        app_name: str,
        domain_name: str = "example.com",
        hosted_zone: Optional[_route53.IHostedZone] = None,
        lb_listener: _elb.ApplicationListener = None,
    ) -> None:
        self.id = id
        self.scope = scope
        self.environment_parameters = environment_parameters
        self.microservices: List[ECSMicroservice] = []
        self.hosted_zone = hosted_zone
        self.domain_name = domain_name
        self.lb_listener = lb_listener
        self.app_name = app_name
        self.vpc = self._get_vpc()

        super().__init__(scope, id)

        self._create_cluster()

    def _get_vpc(self) -> _ec2.IVpc:
        return _ec2.Vpc.from_lookup(
            self.scope, "VPC", vpc_id=self.environment_parameters.get("vpc")
        )

    def _create_cluster(self) -> None:
        self.cluster = _ecs.Cluster(scope=self.scope, id="cluster", vpc=self._get_vpc())

    def register_ms(self, microservice: ECSMicroservice) -> None:
        """Adds a ECSMicroservice instance to the list of hosted services in the cluster"""
        self.microservices.append(microservice)
