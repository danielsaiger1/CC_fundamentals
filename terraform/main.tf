resource "azurerm_resource_group" "rg" {
  name     = "cc-fund-rg"
  location = "North Europe"
}

resource "azurerm_service_plan" "asp" {
  name                = "cc-fund-asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "frontend-app" {
  name                = "cc-fund-frontend-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.asp.id
  https_only          = true
  client_certificate_mode = "Required"
  public_network_access_enabled = true

  site_config {
    always_on     = false
    http2_enabled = false

    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_linux_web_app" "classification-app" {
  name                = "cc-fund-classification-api"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.asp.id
  https_only          = true
  client_certificate_mode = "Required"
  public_network_access_enabled = true

  site_config {
    always_on     = false
    http2_enabled = false

    application_stack {
      python_version = "3.11"
    }
  }

  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  identity {
    type = "SystemAssigned"
  }
}