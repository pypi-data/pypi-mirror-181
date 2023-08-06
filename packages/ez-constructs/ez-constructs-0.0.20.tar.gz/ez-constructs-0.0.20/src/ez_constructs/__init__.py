'''
# EZ Constructs

A collection of heaviliy opinionated AWS CDK highlevel constructs.
[construct.dev](https://constructs.dev/packages/ez-constructs/) || [npmjs](https://www.npmjs.com/package/ez-constructs)

## Installation

> The library requires AWS CDK version >= 2.7.0.

` npm install ez-constructs` or ` yarn add ez-constructs`

## Constructs

1. [SecureBucket](src/secure-bucket) - Creates an S3 bucket that is secure, encrypted at rest along with object retention and intelligent transition rules
2. [SimpleCodeBuildProject](src/codebuild-ci) - Creates Codebuild projects the easy way.

## Libraries

1. Utils - A collection of utility functions
2. CustomSynthesizer - A custom CDK synthesizer that will alter the default service roles that CDK uses.

## Aspects

1. [PermissionsBoundaryAspect](src/aspects) - A custom aspect that can be used to apply a permission boundary to all roles created in the contex.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk
import aws_cdk.aws_codebuild
import aws_cdk.aws_ec2
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import constructs


class CustomSynthesizer(
    aws_cdk.DefaultStackSynthesizer,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.CustomSynthesizer",
):
    '''As a best practice organizations enforce policies which require all custom IAM Roles created to be defined under a specific path and permission boundary.

    In order to adhere with such compliance requirements, the CDK bootstrapping is often customized
    (refer: https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html#bootstrapping-customizing).
    So, we need to ensure that parallel customization is applied during synthesis phase.
    This Custom Synthesizer is used to modify the default path of the following IAM Roles internally used by CDK:

    - deploy role
    - file-publishing-role
    - image-publishing-role
    - cfn-exec-role
    - lookup-role

    :see:

    PermissionsBoundaryAspect

    Example Usage::

    new DbStack(app, config.id('apiDbStack'), {
    env: {account: '123456789012', region: 'us-east-1'},
    synthesizer: new CustomSynthesizer('/banking/dev/'),
    });
    '''

    def __init__(self, role_path: builtins.str) -> None:
        '''
        :param role_path: -
        '''
        jsii.create(self.__class__, self, [role_path])


class EzConstruct(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.EzConstruct",
):
    '''A marker base class for EzConstructs.'''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        jsii.create(self.__class__, self, [scope, id])


@jsii.enum(jsii_type="ez-constructs.GitEvent")
class GitEvent(enum.Enum):
    '''The Github events which should trigger this build.'''

    PULL_REQUEST = "PULL_REQUEST"
    PUSH = "PUSH"
    ALL = "ALL"


@jsii.implements(aws_cdk.IAspect)
class PermissionsBoundaryAspect(
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.PermissionsBoundaryAspect",
):
    '''As a best practice organizations enforce policies which require all custom IAM Roles created to be defined under a specific path and permission boundary.

    Well, this allows better governance and also prevents unintended privilege escalation.
    AWS CDK high level constructs and patterns encapsulates the role creation from end users.
    So it is a laborious and at times impossible to get a handle of newly created roles within a stack.
    This aspect will scan all roles within the given scope and will attach the right permission boundary and path to them.
    Example::

           const app = new App();
           const mystack = new MyStack(app, 'MyConstruct'); // assuming this will create a role by name `myCodeBuildRole` with admin access.
           Aspects.of(app).add(new PermissionsBoundaryAspect('/my/devroles/', 'boundary/dev-max'));
    '''

    def __init__(
        self,
        role_path: builtins.str,
        role_permission_boundary: builtins.str,
    ) -> None:
        '''Constructs a new PermissionsBoundaryAspect.

        :param role_path: - the role path to attach to newly created roles.
        :param role_permission_boundary: - the permission boundary to attach to newly created roles.
        '''
        jsii.create(self.__class__, self, [role_path, role_permission_boundary])

    @jsii.member(jsii_name="visit")
    def visit(self, node: constructs.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rolePath")
    def role_path(self) -> builtins.str:
        '''The role path to attach to newly created roles.'''
        return typing.cast(builtins.str, jsii.get(self, "rolePath"))

    @role_path.setter
    def role_path(self, value: builtins.str) -> None:
        jsii.set(self, "rolePath", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rolePermissionBoundary")
    def role_permission_boundary(self) -> builtins.str:
        '''The permission boundary to attach to newly created roles.'''
        return typing.cast(builtins.str, jsii.get(self, "rolePermissionBoundary"))

    @role_permission_boundary.setter
    def role_permission_boundary(self, value: builtins.str) -> None:
        jsii.set(self, "rolePermissionBoundary", value)


class SecureBucket(
    EzConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.SecureBucket",
):
    '''Will create a secure bucket with the following features: - Bucket name will be modified to include account and region.

    - Access limited to the owner
    - Object Versioning
    - Encryption at rest
    - Object expiration max limit to 10 years
    - Object will transition to IA after 60 days and later to deep archive after 365 days

    Example::

           let aBucket = new SecureBucket(mystack, 'secureBucket', {
             bucketName: 'mybucket',
             objectsExpireInDays: 500,
             enforceSSL: false,
            });
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''Creates the SecureBucket.

        :param scope: - the stack in which the construct is defined.
        :param id: - a unique identifier for the construct.
        '''
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="assemble")
    def assemble(self) -> "SecureBucket":
        '''Creates the underlying S3 bucket.'''
        return typing.cast("SecureBucket", jsii.invoke(self, "assemble", []))

    @jsii.member(jsii_name="bucketName")
    def bucket_name(self, name: builtins.str) -> "SecureBucket":
        '''The name of the bucket.

        Internally the bucket name will be modified to include the account and region.

        :param name: - the name of the bucket to use.
        '''
        return typing.cast("SecureBucket", jsii.invoke(self, "bucketName", [name]))

    @jsii.member(jsii_name="moveToGlacierDeepArchive")
    def move_to_glacier_deep_archive(
        self,
        move: typing.Optional[builtins.bool] = None,
    ) -> "SecureBucket":
        '''Use only for buckets that have archiving data.

        CAUTION, once the object is archived, a temporary bucket to store the data.

        :param move: -

        :default: false

        :return: SecureBucket
        '''
        return typing.cast("SecureBucket", jsii.invoke(self, "moveToGlacierDeepArchive", [move]))

    @jsii.member(jsii_name="objectsExpireInDays")
    def objects_expire_in_days(self, expiry_in_days: jsii.Number) -> "SecureBucket":
        '''The number of days that object will be kept.

        :param expiry_in_days: -

        :default: 3650 - 10 years

        :return: SecureBucket
        '''
        return typing.cast("SecureBucket", jsii.invoke(self, "objectsExpireInDays", [expiry_in_days]))

    @jsii.member(jsii_name="overrideBucketProperties")
    def override_bucket_properties(
        self,
        *,
        access_control: typing.Optional[aws_cdk.aws_s3.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[aws_cdk.aws_s3.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[aws_cdk.aws_s3.CorsRule]] = None,
        encryption: typing.Optional[aws_cdk.aws_s3.BucketEncryption] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IntelligentTieringConfiguration]] = None,
        inventories: typing.Optional[typing.Sequence[aws_cdk.aws_s3.Inventory]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[aws_cdk.aws_s3.LifecycleRule]] = None,
        metrics: typing.Optional[typing.Sequence[aws_cdk.aws_s3.BucketMetrics]] = None,
        notifications_handler_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        object_ownership: typing.Optional[aws_cdk.aws_s3.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[aws_cdk.aws_s3.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[aws_cdk.aws_s3.RedirectTarget] = None,
        website_routing_rules: typing.Optional[typing.Sequence[aws_cdk.aws_s3.RoutingRule]] = None,
    ) -> "SecureBucket":
        '''This function allows users to override the defaults calculated by this construct and is only recommended for advanced usecases.

        The values supplied via props superseeds the defaults that are calculated.

        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Specifies whether Amazon S3 should use an S3 Bucket Key with server-side encryption using KMS (SSE-KMS) for new objects in the bucket. Only relevant, when Encryption is set to {@link BucketEncryption.KMS} Default: - false
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        :param encryption_key: External KMS key to use for bucket encryption. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "Managed". Default: - If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.

        :return: SecureBucket
        '''
        props = aws_cdk.aws_s3.BucketProps(
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            notifications_handler_role=notifications_handler_role,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            transfer_acceleration=transfer_acceleration,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        return typing.cast("SecureBucket", jsii.invoke(self, "overrideBucketProperties", [props]))

    @jsii.member(jsii_name="restrictAccessToIpOrCidrs")
    def restrict_access_to_ip_or_cidrs(
        self,
        ips_or_cidrs: typing.Sequence[builtins.str],
    ) -> "SecureBucket":
        '''Adds access restrictions so that the access is allowed from the following IP ranges.

        :param ips_or_cidrs: -
        '''
        return typing.cast("SecureBucket", jsii.invoke(self, "restrictAccessToIpOrCidrs", [ips_or_cidrs]))

    @jsii.member(jsii_name="restrictAccessToVpcs")
    def restrict_access_to_vpcs(
        self,
        vpc_ids: typing.Sequence[builtins.str],
    ) -> "SecureBucket":
        '''Adds access restrictions so that the access is allowed from the following VPCs.

        :param vpc_ids: -
        '''
        return typing.cast("SecureBucket", jsii.invoke(self, "restrictAccessToVpcs", [vpc_ids]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.Bucket]:
        '''The underlying S3 bucket created by this construct.'''
        return typing.cast(typing.Optional[aws_cdk.aws_s3.Bucket], jsii.get(self, "bucket"))


class SimpleCodebuildProject(
    EzConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="ez-constructs.SimpleCodebuildProject",
):
    '''Most of the cases,a developer will use CodeBuild setup to perform simple CI tasks such as: - Build and test your code on a PR - Run a specific script based on a cron schedule.

    Also, they might want:

    - artifacts like testcase reports to be available via Reports UI and/or S3.
    - logs to be available via CloudWatch Logs.

    However, there can be additional organizational retention policies, for example retaining logs for a particular period of time.
    With this construct, you can easily create a basic CodeBuild project with many opinated defaults that are compliant with FISMA and NIST.

    Example, creates a project named ``my-project``, with artifacts going to my-project-artifacts--
    and logs going to ``/aws/codebuild/my-project`` log group with a retention period of 90 days and 14 months respectively::

           new SimpleCodebuildProject(stack, 'MyProject')
             .projectName('myproject')
             .gitRepoUrl('https://github.com/bijujoseph/cloudbiolinux.git')
             .gitBaseBranch('main')
             .triggerEvent(GitEvent.PULL_REQUEST)
             .buildSpecPath('buildspecs/my-pr-checker.yml')
             .assemble();
    '''

    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="addEnv")
    def add_env(
        self,
        name: builtins.str,
        *,
        value: typing.Any,
        type: typing.Optional[aws_cdk.aws_codebuild.BuildEnvironmentVariableType] = None,
    ) -> "SimpleCodebuildProject":
        '''A convenient way to set the project environment variables.

        The values set here will be presnted on the UI when build with overriding is used.

        :param name: - The environment variable name.
        :param value: The value of the environment variable. For plain-text variables (the default), this is the literal value of variable. For SSM parameter variables, pass the name of the parameter here (``parameterName`` property of ``IParameter``). For SecretsManager variables secrets, pass either the secret name (``secretName`` property of ``ISecret``) or the secret ARN (``secretArn`` property of ``ISecret``) here, along with optional SecretsManager qualifiers separated by ':', like the JSON key, or the version or stage (see https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html#build-spec.env.secrets-manager for details).
        :param type: The type of environment variable. Default: PlainText
        '''
        env_var = aws_cdk.aws_codebuild.BuildEnvironmentVariable(
            value=value, type=type
        )

        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "addEnv", [name, env_var]))

    @jsii.member(jsii_name="artifactBucket")
    def artifact_bucket(
        self,
        artifact_bucket: typing.Union[builtins.str, aws_cdk.aws_s3.IBucket],
    ) -> "SimpleCodebuildProject":
        '''The name of the bucket to store the artifacts.

        By default the buckets will get stored in ``<project-name>-artifacts`` bucket.
        This function can be used to ovrride the default behavior.

        :param artifact_bucket: - a valid existing Bucket reference or bucket name to use.
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "artifactBucket", [artifact_bucket]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        *,
        artifacts: typing.Optional[aws_cdk.aws_codebuild.IArtifacts] = None,
        secondary_artifacts: typing.Optional[typing.Sequence[aws_cdk.aws_codebuild.IArtifacts]] = None,
        secondary_sources: typing.Optional[typing.Sequence[aws_cdk.aws_codebuild.ISource]] = None,
        source: typing.Optional[aws_cdk.aws_codebuild.ISource] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional[aws_cdk.aws_codebuild.BuildSpec] = None,
        cache: typing.Optional[aws_cdk.aws_codebuild.Cache] = None,
        check_secrets_in_plain_text_env_variables: typing.Optional[builtins.bool] = None,
        concurrent_build_limit: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        environment: typing.Optional[aws_cdk.aws_codebuild.BuildEnvironment] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]] = None,
        file_system_locations: typing.Optional[typing.Sequence[aws_cdk.aws_codebuild.IFileSystemLocation]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        logging: typing.Optional[aws_cdk.aws_codebuild.LoggingOptions] = None,
        project_name: typing.Optional[builtins.str] = None,
        queued_timeout: typing.Optional[aws_cdk.Duration] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> "SimpleCodebuildProject":
        '''
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param check_secrets_in_plain_text_env_variables: Whether to check for the presence of any secrets in the environment variables of the default type, BuildEnvironmentVariableType.PLAINTEXT. Since using a secret for the value of that kind of variable would result in it being displayed in plain text in the AWS Console, the construct will throw an exception if it detects a secret was passed there. Pass this property as false if you want to skip this validation, and keep using a secret in a plain text environment variable. Default: true
        :param concurrent_build_limit: Maximum number of concurrent builds. Minimum value is 1 and maximum is account build limit. Default: - no explicit limit is set
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param logging: Information about logs for the build project. A project can create logs in Amazon CloudWatch Logs, an S3 bucket, or both. Default: - no log configuration is set
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param queued_timeout: The number of minutes after which AWS CodeBuild stops the build if it's still in queue. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: - no queue timeout is set
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        '''
        default_props = aws_cdk.aws_codebuild.ProjectProps(
            artifacts=artifacts,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            source=source,
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            check_secrets_in_plain_text_env_variables=check_secrets_in_plain_text_env_variables,
            concurrent_build_limit=concurrent_build_limit,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            logging=logging,
            project_name=project_name,
            queued_timeout=queued_timeout,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "assemble", [default_props]))

    @jsii.member(jsii_name="buildSpecPath")
    def build_spec_path(
        self,
        build_spec_path: builtins.str,
    ) -> "SimpleCodebuildProject":
        '''The build spec file path.

        :param build_spec_path: - relative location of the build spec file.
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "buildSpecPath", [build_spec_path]))

    @jsii.member(jsii_name="computeType")
    def compute_type(
        self,
        compute_type: aws_cdk.aws_codebuild.ComputeType,
    ) -> "SimpleCodebuildProject":
        '''The compute type to use.

        :param compute_type: -

        :see: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-compute-types.html
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "computeType", [compute_type]))

    @jsii.member(jsii_name="gitBaseBranch")
    def git_base_branch(self, branch: builtins.str) -> "SimpleCodebuildProject":
        '''The main branch of the github project.

        :param branch: -
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "gitBaseBranch", [branch]))

    @jsii.member(jsii_name="gitRepoUrl")
    def git_repo_url(self, git_repo_url: builtins.str) -> "SimpleCodebuildProject":
        '''The github or enterprise github repository url.

        :param git_repo_url: -
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "gitRepoUrl", [git_repo_url]))

    @jsii.member(jsii_name="overrideProjectProps")
    def override_project_props(
        self,
        *,
        artifacts: typing.Optional[aws_cdk.aws_codebuild.IArtifacts] = None,
        secondary_artifacts: typing.Optional[typing.Sequence[aws_cdk.aws_codebuild.IArtifacts]] = None,
        secondary_sources: typing.Optional[typing.Sequence[aws_cdk.aws_codebuild.ISource]] = None,
        source: typing.Optional[aws_cdk.aws_codebuild.ISource] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        badge: typing.Optional[builtins.bool] = None,
        build_spec: typing.Optional[aws_cdk.aws_codebuild.BuildSpec] = None,
        cache: typing.Optional[aws_cdk.aws_codebuild.Cache] = None,
        check_secrets_in_plain_text_env_variables: typing.Optional[builtins.bool] = None,
        concurrent_build_limit: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        environment: typing.Optional[aws_cdk.aws_codebuild.BuildEnvironment] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]] = None,
        file_system_locations: typing.Optional[typing.Sequence[aws_cdk.aws_codebuild.IFileSystemLocation]] = None,
        grant_report_group_permissions: typing.Optional[builtins.bool] = None,
        logging: typing.Optional[aws_cdk.aws_codebuild.LoggingOptions] = None,
        project_name: typing.Optional[builtins.str] = None,
        queued_timeout: typing.Optional[aws_cdk.Duration] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnet_selection: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> "SimpleCodebuildProject":
        '''
        :param artifacts: Defines where build artifacts will be stored. Could be: PipelineBuildArtifacts, NoArtifacts and S3Artifacts. Default: NoArtifacts
        :param secondary_artifacts: The secondary artifacts for the Project. Can also be added after the Project has been created by using the {@link Project#addSecondaryArtifact} method. Default: - No secondary artifacts.
        :param secondary_sources: The secondary sources for the Project. Can be also added after the Project has been created by using the {@link Project#addSecondarySource} method. Default: - No secondary sources.
        :param source: The source of the build. *Note*: if {@link NoSource} is given as the source, then you need to provide an explicit ``buildSpec``. Default: - NoSource
        :param allow_all_outbound: Whether to allow the CodeBuild to send all network traffic. If set to false, you must individually add traffic rules to allow the CodeBuild project to connect to network targets. Only used if 'vpc' is supplied. Default: true
        :param badge: Indicates whether AWS CodeBuild generates a publicly accessible URL for your project's build badge. For more information, see Build Badges Sample in the AWS CodeBuild User Guide. Default: false
        :param build_spec: Filename or contents of buildspec in JSON format. Default: - Empty buildspec.
        :param cache: Caching strategy to use. Default: Cache.none
        :param check_secrets_in_plain_text_env_variables: Whether to check for the presence of any secrets in the environment variables of the default type, BuildEnvironmentVariableType.PLAINTEXT. Since using a secret for the value of that kind of variable would result in it being displayed in plain text in the AWS Console, the construct will throw an exception if it detects a secret was passed there. Pass this property as false if you want to skip this validation, and keep using a secret in a plain text environment variable. Default: true
        :param concurrent_build_limit: Maximum number of concurrent builds. Minimum value is 1 and maximum is account build limit. Default: - no explicit limit is set
        :param description: A description of the project. Use the description to identify the purpose of the project. Default: - No description.
        :param encryption_key: Encryption key to use to read and write artifacts. Default: - The AWS-managed CMK for Amazon Simple Storage Service (Amazon S3) is used.
        :param environment: Build environment to use for the build. Default: BuildEnvironment.LinuxBuildImage.STANDARD_1_0
        :param environment_variables: Additional environment variables to add to the build environment. Default: - No additional environment variables are specified.
        :param file_system_locations: An ProjectFileSystemLocation objects for a CodeBuild build project. A ProjectFileSystemLocation object specifies the identifier, location, mountOptions, mountPoint, and type of a file system created using Amazon Elastic File System. Default: - no file system locations
        :param grant_report_group_permissions: Add permissions to this project's role to create and use test report groups with name starting with the name of this project. That is the standard report group that gets created when a simple name (in contrast to an ARN) is used in the 'reports' section of the buildspec of this project. This is usually harmless, but you can turn these off if you don't plan on using test reports in this project. Default: true
        :param logging: Information about logs for the build project. A project can create logs in Amazon CloudWatch Logs, an S3 bucket, or both. Default: - no log configuration is set
        :param project_name: The physical, human-readable name of the CodeBuild Project. Default: - Name is automatically generated.
        :param queued_timeout: The number of minutes after which AWS CodeBuild stops the build if it's still in queue. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: - no queue timeout is set
        :param role: Service Role to assume while running the build. Default: - A role will be created.
        :param security_groups: What security group to associate with the codebuild project's network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: VPC network to place codebuild network interfaces. Specify this if the codebuild project needs to access resources in a VPC. Default: - No VPC is specified.
        '''
        props = aws_cdk.aws_codebuild.ProjectProps(
            artifacts=artifacts,
            secondary_artifacts=secondary_artifacts,
            secondary_sources=secondary_sources,
            source=source,
            allow_all_outbound=allow_all_outbound,
            badge=badge,
            build_spec=build_spec,
            cache=cache,
            check_secrets_in_plain_text_env_variables=check_secrets_in_plain_text_env_variables,
            concurrent_build_limit=concurrent_build_limit,
            description=description,
            encryption_key=encryption_key,
            environment=environment,
            environment_variables=environment_variables,
            file_system_locations=file_system_locations,
            grant_report_group_permissions=grant_report_group_permissions,
            logging=logging,
            project_name=project_name,
            queued_timeout=queued_timeout,
            role=role,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
        )

        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "overrideProjectProps", [props]))

    @jsii.member(jsii_name="privileged")
    def privileged(self, p: builtins.bool) -> "SimpleCodebuildProject":
        '''Set privileged mode of execution.

        Usually needed if this project builds Docker images,
        and the build environment image you chose is not provided by CodeBuild with Docker support.
        By default, Docker containers do not allow access to any devices.
        Privileged mode grants a build project's Docker container access to all devices
        https://docs.aws.amazon.com/codebuild/latest/userguide/change-project-console.html#change-project-console-environment

        :param p: - true/false.
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "privileged", [p]))

    @jsii.member(jsii_name="projectDescription")
    def project_description(
        self,
        project_description: builtins.str,
    ) -> "SimpleCodebuildProject":
        '''The description of the codebuild project.

        :param project_description: - a valid description string.
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "projectDescription", [project_description]))

    @jsii.member(jsii_name="projectName")
    def project_name(self, project_name: builtins.str) -> "SimpleCodebuildProject":
        '''The name of the codebuild project.

        :param project_name: - a valid name string.
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "projectName", [project_name]))

    @jsii.member(jsii_name="triggerBuildOnGitEvent")
    def trigger_build_on_git_event(self, event: GitEvent) -> "SimpleCodebuildProject":
        '''The Github events that can trigger this build.

        :param event: -
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "triggerBuildOnGitEvent", [event]))

    @jsii.member(jsii_name="triggerBuildOnSchedule")
    def trigger_build_on_schedule(
        self,
        schedule: aws_cdk.aws_events.Schedule,
    ) -> "SimpleCodebuildProject":
        '''The cron schedule on which this build gets triggerd.

        :param schedule: -
        '''
        return typing.cast("SimpleCodebuildProject", jsii.invoke(self, "triggerBuildOnSchedule", [schedule]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="project")
    def project(self) -> typing.Optional[aws_cdk.aws_codebuild.Project]:
        '''The underlying codebuild project that is created by this construct.'''
        return typing.cast(typing.Optional[aws_cdk.aws_codebuild.Project], jsii.get(self, "project"))


class Utils(metaclass=jsii.JSIIMeta, jsii_type="ez-constructs.Utils"):
    '''A utility class that have common functions.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="appendIfNecessary") # type: ignore[misc]
    @builtins.classmethod
    def append_if_necessary(
        cls,
        name: builtins.str,
        *suffixes: builtins.str,
    ) -> builtins.str:
        '''Will append the suffix to the given name if the name do not contain the suffix.

        :param name: - a string.
        :param suffixes: - the string to append.

        :return: the name with the suffix appended if necessary delimited by a hyphen
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "appendIfNecessary", [name, *suffixes]))

    @jsii.member(jsii_name="endsWith") # type: ignore[misc]
    @builtins.classmethod
    def ends_with(cls, str: builtins.str, s: builtins.str) -> builtins.bool:
        '''Will check if the given string ends with the given suffix.

        :param str: - a string.
        :param s: - suffix to check.
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "endsWith", [str, s]))

    @jsii.member(jsii_name="isEmpty") # type: ignore[misc]
    @builtins.classmethod
    def is_empty(cls, value: typing.Any = None) -> builtins.bool:
        '''Will check if the given object is empty.

        :param value: -
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isEmpty", [value]))

    @jsii.member(jsii_name="kebabCase") # type: ignore[misc]
    @builtins.classmethod
    def kebab_case(cls, str: builtins.str) -> builtins.str:
        '''Will convert the given string to lower case and transform any spaces to hyphens.

        :param str: - a string.
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "kebabCase", [str]))

    @jsii.member(jsii_name="parseGithubUrl") # type: ignore[misc]
    @builtins.classmethod
    def parse_github_url(cls, url: builtins.str) -> typing.Any:
        '''Splits a given Github URL and extracts the owner and repo name.

        :param url: -
        '''
        return typing.cast(typing.Any, jsii.sinvoke(cls, "parseGithubUrl", [url]))

    @jsii.member(jsii_name="prettyPrintStack") # type: ignore[misc]
    @builtins.classmethod
    def pretty_print_stack(
        cls,
        stack: aws_cdk.Stack,
        persist: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''A utility function that will print the content of a CDK stack.

        :param stack: - a valid stack.
        :param persist: -

        :warning: This function is only used for debugging purpose.
        '''
        return typing.cast(None, jsii.sinvoke(cls, "prettyPrintStack", [stack, persist]))

    @jsii.member(jsii_name="startsWith") # type: ignore[misc]
    @builtins.classmethod
    def starts_with(cls, str: builtins.str, s: builtins.str) -> builtins.bool:
        '''Will check if the given string starts with the given prefix.

        :param str: - a string.
        :param s: - the prefix to check.
        '''
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "startsWith", [str, s]))

    @jsii.member(jsii_name="suppressNagRule") # type: ignore[misc]
    @builtins.classmethod
    def suppress_nag_rule(
        cls,
        scope: constructs.IConstruct,
        rule_id: builtins.str,
        reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Will disable the CDK NAG rule for the given construct and its children.

        :param scope: - the scope to disable the rule for.
        :param rule_id: - the rule id to disable.
        :param reason: - reason for disabling the rule.
        '''
        return typing.cast(None, jsii.sinvoke(cls, "suppressNagRule", [scope, rule_id, reason]))

    @jsii.member(jsii_name="wrap") # type: ignore[misc]
    @builtins.classmethod
    def wrap(cls, str: builtins.str, delimiter: builtins.str) -> builtins.str:
        '''Will wrap the given string using the given delimiter.

        :param str: - the string to wrap.
        :param delimiter: - the delimiter to use.

        :return: the wrapped string
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "wrap", [str, delimiter]))


__all__ = [
    "CustomSynthesizer",
    "EzConstruct",
    "GitEvent",
    "PermissionsBoundaryAspect",
    "SecureBucket",
    "SimpleCodebuildProject",
    "Utils",
]

publication.publish()
