output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_eip.weather_app_eip.public_ip
}

output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.weather_app_instance.id
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.weather_app_vpc.id
}

output "security_group_id" {
  description = "ID of the security group"
  value       = aws_security_group.weather_app_sg.id
}