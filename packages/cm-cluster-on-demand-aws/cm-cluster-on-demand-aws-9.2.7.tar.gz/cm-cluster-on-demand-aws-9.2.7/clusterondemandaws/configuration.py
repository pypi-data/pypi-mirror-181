# Copyright 2004-2022 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import clusterondemand.configuration
from clusterondemandconfig import DEFAULT_HELP_SECTION, ConfigNamespace, may_not_equal_none

awscredentials_ns = ConfigNamespace("aws.credentials", help_section="AWS credentials")
awscredentials_ns.add_parameter(
    "aws_access_key_id",
    help="AWS Access Key ID (generate it in AWS dashboard).",
    help_varname="ID",
    env="AWS_ACCESS_KEY_ID",
    validation=may_not_equal_none
)
awscredentials_ns.add_parameter(
    "aws_secret_key",
    help="AWS Secret Key (generate it in AWS dashboard).",
    help_varname="KEY",
    env="AWS_SECRET_ACCESS_KEY",
    secret=True,
    validation=may_not_equal_none
)
awscredentials_ns.add_parameter(
    "aws_region",
    default="eu-central-1",
    help="Name of the AWS region to use for the operation.",
    env="AWS_REGION",
    validation=may_not_equal_none
)


awscommon_ns = ConfigNamespace("aws.common")
awscommon_ns.import_namespace(clusterondemand.configuration.common_ns)
awscommon_ns.remove_imported_parameter("version")
awscommon_ns.import_namespace(awscredentials_ns)
awscommon_ns.add_parameter(
    "fixed_cluster_prefix",
    advanced=True,
    default="on-demand ",  # space is intentional
    help="This prefix is used for creating and finding new cluster in AWS.",
    help_section=DEFAULT_HELP_SECTION
)
