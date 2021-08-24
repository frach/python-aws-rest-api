output "api_default_stage_url" {
  description = "An ARN of the bucket that stores images."
  value       = module.api.default_apigatewayv2_stage_invoke_url
}
