output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.radicados_bot.id
}

output "public_ip" {
  description = "Public IP address"
  value       = aws_eip.radicados_bot.public_ip
}

output "logs_command" {
  description = "Command to view bot logs (requires SSM Session Manager)"
  value       = "aws ssm start-session --target ${aws_instance.radicados_bot.id} --profile SandboxNQ"
}
