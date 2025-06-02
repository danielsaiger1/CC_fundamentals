resource "azurerm_resource_group" "rg" {
  name     = "cc-fund-rg"
  location = "North Europe"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "cc-fund-vn"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet-frontend" {
  name                 = "cc-fund-subnet-frontend"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "delegation"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }

  service_endpoints                     = ["Microsoft.Web"]
  private_endpoint_network_policies     = "Disabled"
  private_link_service_network_policies_enabled = true
}

resource "azurerm_subnet" "subnet-backend" {
  name                 = "cc-fund-subnet-backend"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]

  private_endpoint_network_policies     = "Disabled"
  private_link_service_network_policies_enabled = true
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
  virtual_network_subnet_id = azurerm_subnet.subnet-frontend.id

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

    ip_restriction {
    name        = "Deny all"
    priority    = 100
    action      = "Deny"
    ip_address  = "0.0.0.0/0"
  }
  }

  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_app_service_virtual_network_swift_connection" "frontend_vnet_integration" {
  app_service_id = azurerm_linux_web_app.frontend-app.id
  subnet_id      = azurerm_subnet.subnet-frontend.id
}

resource "azurerm_private_dns_zone" "dns-zone" {
  name                = "privatelink.azurewebsites.net"
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "dns_link" {
  name                  = "dns-vnet-link"
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.dns-zone.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
}


resource "azurerm_private_endpoint" "classification-app-pe" {
  name                = "api-pe"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.subnet-backend.id

  private_service_connection {
    name                           = "api-psc"
    private_connection_resource_id = azurerm_linux_web_app.classification-app.id
    subresource_names              = ["sites"]
    is_manual_connection           = false
  }

  private_dns_zone_group {
    name                 = "default"
    private_dns_zone_ids = [azurerm_private_dns_zone.dns-zone.id]
  }
}
