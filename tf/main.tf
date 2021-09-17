terraform {
  required_version = ">= 1.0.4"
}

provider "aws" {
  profile = var.profile
  region  = var.region

  # Make it faster by skipping something
  skip_get_ec2_platforms      = true
  skip_metadata_api_check     = true
  skip_region_validation      = true
  skip_credentials_validation = true

  # skip_requesting_account_id should be disabled to generate valid ARN in apigatewayv2_api_execution_arn
  skip_requesting_account_id = false
}

locals {
  items_table_gsi_name = "${var.project}-${var.env}-items-gsi-name"
}

# API GATEWAY
module "api" {
  source = "terraform-aws-modules/apigateway-v2/aws"

  name                   = "${var.project}-${var.env}-api"
  description            = "API for lambdas"
  protocol_type          = "HTTP"
  create_api_domain_name = false

  cors_configuration = {
    allow_headers = ["content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent"]
    allow_methods = ["*"]
    allow_origins = ["*"]
  }

  integrations = {
    "GET /items/{name+}" = {
      lambda_arn             = module.api_lambda.lambda_function_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 3000
    }

    "GET /items" = {
      lambda_arn             = module.api_lambda.lambda_function_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 3000
    }

    "POST /items" = {
      lambda_arn             = module.api_lambda.lambda_function_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 3000
    }

    "GET /health" = {
      lambda_arn             = module.api_lambda.lambda_function_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 3000
    }
  }

  tags = {
    Name = "${var.project}-${var.env}-api"
  }
}

# LAMBDA
module "api_lambda" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.project}-${var.env}-api-lambda"
  description   = "A lambda for all of the API requests."
  handler       = "main.lambda_handler"
  runtime       = var.lambda_runtime
  publish = true

  create_package         = false
  local_existing_package = "../api/dist/lambda.zip"

  environment_variables = {
    DDB_ITEMS_TABLE           = module.items_table.dynamodb_table_id
    DDB_ITEMS_GSI_NAME          = local.items_table_gsi_name
    LOG_LEVEL                      = var.lambda_envs["log_level"]
    POWERTOOLS_SERVICE_NAME        = var.api_name
    POWERTOOLS_EVENT_HANDLER_DEBUG = var.lambda_envs["powertools_event_handler_debug"]
  }

  allowed_triggers = {
    AllowExecutionFromAPIGateway = {
      service    = "apigateway"
      source_arn = "${module.api.apigatewayv2_api_execution_arn}/*/*/*"
    }
  }

  attach_policy_statements = true
  policy_statements = {
    ddb_items_table_perms = {
      effect    = "Allow",
      actions   = [
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem",
        "dynamodb:DeleteItem",
        "dynamodb:DescribeTable",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:UpdateItem",
      ],
      resources = [module.items_table.dynamodb_table_arn]
    }
    ddb_items_gsi_name_perms = {
      effect = "Allow",
      actions = [
        "dynamodb:Query"
      ],
      resources = ["${module.items_table.dynamodb_table_arn}/index/${local.items_table_gsi_name}"]
    }
  }

  tags = {
    Name = "${var.project}-${var.env}-api-lambda"
  }
}

# DYNAMODB
module "items_table" {
  source   = "terraform-aws-modules/dynamodb-table/aws"

  name     = "${var.project}-${var.env}-items"
  hash_key = "id"
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    {
      name = "id"
      type = "S"
    },
    {
      name = "name"
      type = "S"
    }
  ]

  global_secondary_indexes = [
    {
      name = local.items_table_gsi_name
      hash_key = "name"
      billing_mode = "PAY_PER_REQUEST"
      projection_type = "INCLUDE"
      non_key_attributes = ["id"]
    }
  ]

  tags = {
    Name = "${var.project}-${var.env}-items"
  }
}
