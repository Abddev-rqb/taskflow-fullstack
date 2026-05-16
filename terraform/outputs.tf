output "ec2_public_ip" {
  description = "Public IP address of the TaskFlow EC2 instance"
  value       = aws_instance.taskflow_server.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the TaskFlow EC2 instance"
  value       = aws_instance.taskflow_server.public_dns
}

output "ssh_command" {
  description = "SSH command to connect to the server"
  value       = "ssh -i <your-key-file.pem> ubuntu@${aws_instance.taskflow_server.public_ip}"
}

output "app_url" {
  description = "TaskFlow application URL"
  value       = "http://${aws_instance.taskflow_server.public_ip}"
}

output "admin_url" {
  description = "TaskFlow Django admin URL"
  value       = "http://${aws_instance.taskflow_server.public_ip}/admin/"
}