# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.56.0"
    }
  }
  required_version = ">= 0.14.9"
}
provider "azurerm" {
  features {}
}

variable "pat" {
  type = string
  sensitive = true
  
}

# Create the resource group
resource "azurerm_resource_group" "rg" {
  name     = "bfb-temperature-py-rg"
  location = "eastus2"
}

# Create the Linux App Service Plan
resource "azurerm_service_plan" "appserviceplan" {
  name                = "appserviceplan-temperature-py"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"
}

# Create the web app, pass in the App Service Plan ID
resource "azurerm_linux_web_app" "webapp" {
  name                  = "temperature-py"
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name
  service_plan_id       = azurerm_service_plan.appserviceplan.id
  https_only            = true
  site_config { 
    minimum_tls_version = "1.2"
    #use_32_bit_worker = true
    #always_on = false
    application_stack {
    python_version = "3.9"
  }  
  }
  logs {
    application_logs {
      file_system_level = "Verbose"
    }
  }
}

resource "azurerm_source_control_token" "source_control_token" {
  type  = "GitHub"
  token = var.pat
}
#  Deploy code from a public GitHub repo
resource "azurerm_app_service_source_control" "sourcecontrol" {
  app_id             = azurerm_linux_web_app.webapp.id
  repo_url           = "https://github.com/bfbarkhouse/temperature-py"
  branch             = "main"
  use_manual_integration = false
  #use_mercurial      = false
  #depends_on = [ azurerm_source_control_token.source_control_token ]
}