provider "aws" {
  region = "us-east-1" // Defina sua região AWS aqui
}

resource "aws_cloudwatch_metric_alarm" "stepfunctions_failure_alarm" {
  alarm_name          = "stepfunctions_failure_alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "ExecutionsFailed"
  namespace           = "AWS/States"
  period              = "300"
  statistic           = "Sum"
  threshold           = "1"
  alarm_description   = "Alarm when Step Functions has at least 1 failed execution"
  alarm_actions       = ["${aws_sns_topic.notification_topic.arn}"]

  dimensions = {
    StateMachineArn = "${aws_sfn_state_machine.state_machine.arn}"
  }
}

resource "aws_sfn_state_machine" "state_machine" {
  name     = "example_state_machine"
  role_arn = "${aws_iam_role.state_machine_role.arn}"
  definition = <<DEFINITION
{
  "Comment": "An example State Machine",
  "StartAt": "FirstState",
  "States": {
    "FirstState": {
      "Type": "Pass",
      "End": true
    }
  }
}
DEFINITION
}

resource "aws_iam_role" "state_machine_role" {
  name               = "example_state_machine_role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "states.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_sns_topic" "notification_topic" {
  name = "example_notification_topic"
}

resource "aws_sns_topic_subscription" "email_notification" {
  topic_arn = aws_sns_topic.notification_topic.arn
  protocol  = "email"
  endpoint  = "example@example.com"
}
