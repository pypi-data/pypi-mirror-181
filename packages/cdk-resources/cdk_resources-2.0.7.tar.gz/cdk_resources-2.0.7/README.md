# CDK Resources #

## Motivation

### Architecture
Regular **aws-cdk** has a *stack-based* architecture where resources are defined in each stack and then resources are
shared between stacks (import from stacks). This project is proposing a *resource-based* architecture as this would enable a more natural
organization of resources based on AWS services.

**Typical CDK Structure** 
```
└── custom_construct/
|    └── constructs1.py
|    └── ...
|    └── constructs1.py
| 
└── stacks/
|    └── stack1.py
|    └── stack2.py
|    ...
|    └── stackN.py

└── app.py
└── cdk.json
```

**CDK Resources Approach**
```
└── custom_construct/
|    └── constructs1.py
|    └── ...
|    └── constructs1.py
| 
└── resources/
|    └── apigateway.py
|    └── ec2.py
|    └── ecs.py
|    └── eks.py
|    └── elasticsearch.py
|    └── ...
|    └── vpc.py
|
└── stacks/
|    └── stack1.py
|    └── stack2.py
|    ...
|    └── stackN.py

└── app.py
└── cdk.json
```

### Environment Parameters
One of the most broadly used approach to parameterize a cdk stack based on 
environments also knows as stages (`dev`, ..., `prod`) is to pass them as 
configurations in the`cdk.json` file. 

In a big multi stack project, this approach become a issue as `cdk.json` starts
growing is difficult to manage

**Parameterization based on context** 
```json
{
  "app": "python3 app.py",
  "context": {
    "configurations": {
      "stack1": {
        "dev": {
          "aurora_cluster_instances": 1,
          ...
          "ecs_service_desired_container_count": 1
        },
        "prod": {
          "aurora_cluster_instances": 3,
          ...
          "ecs_service_desired_container_count": 5
        }
      },
      ...
    }
  }
}
```

**CDK Resources Parameterization** 
```python
class PostgreSqlRdsDatabase(Resource[aws_rds.DatabaseCluster]):
    construct_class = aws_rds.DatabaseCluster
    construct_props = dict(
        default=dict(
            ...
            instances=1,
            ...
        ),
        prod=dict(
            instances=2,
        )
    )
```

## Installation
To install use pip
```
$ pip install cdk-resources
```

## Components
### Resource
Resources are the most important component as it contains mostly all the logic 
of the project. A resource is a natural representation of an AWS element, and in 
terms of cdk is the equivalent of a **Construct Manager**. Components must
inherit from `cdk_resources.Resource`.

There are two types of resources: *resource managed by the stack* and *imported 
resources*.

#### Resource Attributes:

* **construct_class** (Required): The **aws_cdk.construct** class this resource 
represent.

* **construct_props**: Required only if it is a managed resource. The cdk 
construct class properties.

* **construct_lookup_method**: Method of the **aws_cdk.construct** construct to 
be used to import the object.

* **construct_lookup_props**: Required if the object is an imported resource. 
Kwargs used by `construct_lookup_method` to lookup for the object.


#### Resource Methods:

* **get()**: Class method of the resource that returns the **aws_cdk.construct**. 
Either by lookup or because was previously created.

* **post_create()**: Extra configurations to apply to the construct *after* 
construct was init.


#### Resource Examples:
As it can seen in the example below for the `PostgreSqlRdsDatabase` 
**construct_class** is `aws_rds.DatabaseCluster`, desired configurations for all 
the environments are being specified in the **construct_props** attr. And other
resources are imported. 

```python
from aws_cdk import aws_rds, core, aws_ec2

from cdk_resources import Resource

from resources.ec2 import PostgreSqlRdsDatabaseSg
from resources.vpc import (
    DefaultVpc,
    DefaultPrivateDbASubnet,
    DefaultPrivateDbBSubnet,
    DefaultPrivateDbCSubnet,
)

class PostgreSqlRdsDatabase(Resource[aws_rds.DatabaseCluster]):
    construct_class = aws_rds.DatabaseCluster
    construct_props = dict(
        default=dict(
            engine=aws_rds.DatabaseClusterEngine.aurora_postgres(
                version=aws_rds.AuroraPostgresEngineVersion.VER_13_4
            ),
            backup=aws_rds.BackupProps(retention=core.Duration.days(3)),
            deletion_protection=True,
            instance_props=lambda: aws_rds.InstanceProps(
                instance_type=aws_ec2.InstanceType.of(
                    aws_ec2.InstanceClass.BURSTABLE3,
                    aws_ec2.InstanceSize.MEDIUM,
                ),
                security_groups=[PostgreSqlRdsDatabaseSg.get()],
                vpc=DefaultVpc.get(),
                vpc_subnets=aws_ec2.SubnetSelection(
                    subnets=[
                        DefaultPrivateDbASubnet.get(),
                        DefaultPrivateDbBSubnet.get(),
                        DefaultPrivateDbCSubnet.get(),
                    ]
                ),
                parameter_group=PostgreSqlParameterGroup().construct,
            ),
            instances=1,
            port=5432,
            removal_policy=core.RemovalPolicy.RETAIN,
            storage_encrypted=True,
        ),
        prod=dict(
            backup=aws_rds.BackupProps(retention=core.Duration.days(30)),
            instances=2,
            vpc_subnets=lambda: aws_ec2.SubnetSelection(
                subnets=[
                    DefaultPrivateDbASubnet.get(),
                    DefaultPrivateDbCSubnet.get(),
                    DefaultPrivateDbCSubnet.get()
                ]
            ),
        ),
    )
```

### Stacks
A stack is the natural representation of a `CFN Stack`. All stacks must inherit 
from `cdk_resources.ResourceStack`.

#### Resource Attributes:

* **EXISTING_RESOURCES** (list): The list of existing resources that must be 
inited in **aws_cdk.scope**. These are resources that are used by the Stack 
resources.

* **RESOURCES** (list): The resources own for this stack.

#### Resource Examples:

As it can be seen in the example below for the `SampleStack`. The stack 
creates a DynamoTable, Security Group, RDS Aurora Parameter Group, and 
RDS Cluster.

Also, some resources must be imported. Those are specified in 
**EXISTING_RESOURCE** list as the VPC resources.

```python
from cdk_resources import ResourceStack

from resources.dynamodb import DynamoTable
from resources.ec2 import PostgreSqlRdsDatabaseSg
from resources.rds import PostgreSqlRdsDatabase, PostgreSqlParameterGroup
from resources.sns import SnsTopic
from resources.vpc import (
    DefaultVpc,
    DefaultPrivateDbASubnet,
    DefaultPrivateDbBSubnet,
    DefaultPrivateDbCSubnet,
)


class SampleStack(ResourceStack):
    EXISTING_RESOURCES = [
        ("vpc", DefaultVpc),
        ("subnet_db_a", DefaultPrivateDbASubnet),
        ("subnet_db_b", DefaultPrivateDbBSubnet),
        ("subnet_db_c", DefaultPrivateDbCSubnet),
    ]
    RESOURCES = [
        # DynamoDB
        ("dynamodb", DynamoTable),
        # RDS
        ("postgresql-sg", PostgreSqlRdsDatabaseSg),
        ("postgresql-parameter-group", PostgreSqlParameterGroup),
        ("postgresqlDb", PostgreSqlRdsDatabase),
        # SNS
        ("sns-topic", SnsTopic),
    ]
```

## Parameterization
to do

## Examples
[Here](https://github.com/sfernandezf/cdk-resources/tree/main/samples) are some
availables examples.
