output "api_url" {
  description = "The URI of the API."
  value       = module.api.apigatewayv2_api_api_endpoint
}

output "api_id" {
  description = "The API identifier."
  value       = module.api.apigatewayv2_api_id
}

output "user_pool_endpoint" {
  value = aws_cognito_user_pool.api_user_pool.endpoint
}

output "user_pool_client_id" {
  value = aws_cognito_user_pool_client.api_user_pool_client.id
}