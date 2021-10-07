output "api_default_stage_url" {
  description = "An ARN of the bucket that stores images."
  value       = module.api.default_apigatewayv2_stage_invoke_url
}

output "user_pool_endpoint" {
  value = aws_cognito_user_pool.api_user_pool.endpoint
}

output "user_pool_client_id" {
  value = aws_cognito_user_pool_client.api_user_pool_client.id
}