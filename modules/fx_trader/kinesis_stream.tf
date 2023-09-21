resource "aws_kinesis_stream" "fx_trader_stream" {
  name             = "fx-trader"
  retention_period = 48

  shard_level_metrics = [
    "IncomingBytes",
    "OutgoingBytes",
  ]

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }
}