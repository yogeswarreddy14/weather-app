terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Create VPC
resource "aws_vpc" "weather_app_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "weather-app-vpc"
  }
}

# Create Internet Gateway
resource "aws_internet_gateway" "weather_app_igw" {
  vpc_id = aws_vpc.weather_app_vpc.id
  tags = {
    Name = "weather-app-igw"
  }
}

# Create Public Subnet
resource "aws_subnet" "weather_app_public_subnet" {
  vpc_id            = aws_vpc.weather_app_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
  tags = {
    Name = "weather-app-public-subnet"
  }
}

# Create Route Table
resource "aws_route_table" "weather_app_rt" {
  vpc_id = aws_vpc.weather_app_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.weather_app_igw.id
  }
  tags = {
    Name = "weather-app-rt"
  }
}

# Associate Route Table with Subnet
resource "aws_route_table_association" "weather_app_rta" {
  subnet_id      = aws_subnet.weather_app_public_subnet.id
  route_table_id = aws_route_table.weather_app_rt.id
}

# Create Security Group
resource "aws_security_group" "weather_app_sg" {
  name        = "weather-app-sg"
  description = "Security group for weather app"
  vpc_id      = aws_vpc.weather_app_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "weather-app-sg"
  }
}

# Create EC2 Instance
resource "aws_instance" "weather_app_instance" {
  ami           = "ami-0c7217cdde317cfec"  # Ubuntu 22.04 LTS
  instance_type = "t3.nano"  # Changed to t3.nano which has the lowest vCPU requirement
  subnet_id     = aws_subnet.weather_app_public_subnet.id
  vpc_security_group_ids = [aws_security_group.weather_app_sg.id]

  tags = {
    Name = "weather-app-instance"
  }

  user_data = <<-EOF
              #!/bin/bash
              apt-get update
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              docker pull nginx:latest
              docker run -d -p 80:80 nginx:latest
              EOF
}




# Create Elastic IP
resource "aws_eip" "weather_app_eip" {
  instance = aws_instance.weather_app_instance.id
  vpc      = true
  tags = {
    Name = "weather-app-eip"
  }
} 