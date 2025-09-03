# Terraform 0.13+ uses the Terraform Registry:
terraform {
  required_providers {
    datadog = {
      source = "DataDog/datadog"
    }
  }
}

# Configure the Datadog provider
provider "datadog" {
  api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  app_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
