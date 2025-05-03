resource "azurerm_resource_group" "rg" {# rg = interner Name, auf den später zugegriffen wird
  name     = "rg-cc_fundamentals"
  location = "West Europe"
}

# # SKU anpassen auf kostenlose Stufe
# resource "azurerm_app_service_plan" "main" {
#   name                = "appservice-plan"
#   location            = azurerm_resource_group.main.location
#   resource_group_name = azurerm_resource_group.main.name
#   kind                = "Linux"
#   reserved            = true
#   sku {
#     tier = ""
#     size = ""
#   }
# }

# resource "azurerm_app_service" "django" {
#   name                = "django-webapp"
#   location            = azurerm_resource_group.main.location
#   resource_group_name = azurerm_resource_group.main.name
#   app_service_plan_id = azurerm_app_service_plan.main.id
#   site_config {
#     linux_fx_version = "PYTHON|3.9"
#   }
# }

# resource "azurerm_app_service" "flask" {
#   name                = "flask-webapp"
#   location            = azurerm_resource_group.main.location
#   resource_group_name = azurerm_resource_group.main.name
#   app_service_plan_id = azurerm_app_service_plan.main.id
#   site_config {
#     linux_fx_version = "PYTHON|3.9"
#   }
# }

# resource "azurerm_virtual_network" "main" {
#   name                = "vnet-webapps"
#   address_space       = ["10.0.0.0/16"]
#   location            = azurerm_resource_group.main.location
#   resource_group_name = azurerm_resource_group.main.name
# }