variable "location" {
  type    = string
  default = "East US"
}

variable "project_name" {
  type    = string
  default = "prep"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "postgres_admin" {
  type    = string
  default = "pgadmin"
}

variable "postgres_password" {
  type      = string
  sensitive = true
}

variable "aks_node_count" {
  type    = number
  default = 2
}

variable "aks_vm_size" {
  type    = string
  default = "Standard_D2s_v5"
}
