variable "env" {
  type = string
}

variable "lambda_runtime" {
  type = string
}

variable "profile" {
  type = string
}

variable "region" {
  type = string
}

variable "project" {
  type = string
}

variable "api_name" {
  type = string
}

variable "lambda_envs" {
  type        = map(string)
  description = "Configuration passed to Lambdas as environment variables."
}
