output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "aks_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "acr_name" {
  value = azurerm_container_registry.acr.name
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "postgres_fqdn" {
  value = azurerm_postgresql_flexible_server.postgres.fqdn
}

output "postgres_database" {
  value = azurerm_postgresql_flexible_server_database.appdb.name
}

output "key_vault_name" {
  value = azurerm_key_vault.kv.name
}

output "servicebus_namespace" {
  value = azurerm_servicebus_namespace.servicebus.name
}

output "servicebus_queue" {
  value = azurerm_servicebus_queue.orders.name
}

output "app_identity_client_id" {
  value = azurerm_user_assigned_identity.app.client_id
}

output "aks_oidc_issuer_url" {
  value = azurerm_kubernetes_cluster.aks.oidc_issuer_url
}
