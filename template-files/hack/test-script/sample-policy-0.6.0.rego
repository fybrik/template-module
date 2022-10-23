package dataapi.authz

rule[{}] {
  description := "Template rule"
  input.action.actionType == "@{{action_type}}"
}