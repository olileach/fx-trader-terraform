#### resources ####

resource "aws_lambda_function" "fx_trader" {

  description         = "Sends the FX trade results to kinesis."

  package_type        = "Image"
  image_uri           = "565692740138.dkr.ecr.us-east-1.amazonaws.com/fx-trader:latest"
  function_name       = "fx-trader"
  role                = aws_iam_role.fx_trader_lambda_role.arn
  timeout             = "300"
  memory_size         = "1024"

  tracing_config {
    mode  = "Active"
  }

  environment {
    variables = {
      FX_TRADE_STREAM = aws_kinesis_stream.fx_trader_stream.name
    }
  }

  tags = {
      Name = "fx-trader-demo"
      Env  = "POC"
  }
  dead_letter_config {
    target_arn         = aws_sqs_queue.fx_trader_dl_queue.arn
  }
}

resource "aws_lambda_function_event_invoke_config" "fx_trader_lambda_function_error_config" {
  function_name                = aws_lambda_function.fx_trader.function_name
  maximum_retry_attempts       = 0
}