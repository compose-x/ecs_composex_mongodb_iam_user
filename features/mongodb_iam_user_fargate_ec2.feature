# mongodb_iam_user
Feature: ecs_composex_mongodb_iam_user - Fargate & EC2

    Background: I run in Fargate only
        Given With docker-compose.yaml
        And With compute_modes/fargate_ec2.yaml

    @create
    Scenario Outline: Render docker-compose with new mongodb_iam_user resources
        Given With <override_file>
        And I use defined files as input to define execution settings
        Then I render all files to verify execution

        Examples:
            | override_file             |
            | create_only/services.yaml |
