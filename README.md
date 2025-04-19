# Weather App Infrastructure

This Terraform configuration sets up the infrastructure for the Weather App on AWS.

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed (version >= 1.0.0)

## Infrastructure Components

- VPC with public subnet
- Internet Gateway
- Route Table
- Security Group (allowing HTTP and SSH)
- EC2 Instance (t2.micro)
- Elastic IP

## Usage

1. Initialize Terraform:
```bash
terraform init
```

2. Review the execution plan:
```bash
terraform plan
```

3. Apply the configuration:
```bash
terraform apply
```

4. To destroy the infrastructure:
```bash
terraform destroy
```

## Outputs

After applying the configuration, Terraform will output:
- Public IP address of the EC2 instance
- Instance ID
- VPC ID
- Security Group ID

## Variables

The following variables can be customized in `variables.tf`:
- `aws_region`: AWS region (default: us-east-1)
- `instance_type`: EC2 instance type (default: t2.micro)
- `vpc_cidr`: VPC CIDR block (default: 10.0.0.0/16)
- `public_subnet_cidr`: Public subnet CIDR block (default: 10.0.1.0/24)
- `availability_zone`: Availability zone (default: us-east-1a)

## Security

- The security group allows inbound traffic on ports 80 (HTTP) and 22 (SSH)
- All outbound traffic is allowed
- Consider restricting SSH access to specific IP addresses in production 