terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_security_group" "radicados_bot" {
  name        = "radicados-bot-sg"
  description = "Security group for radicados bot EC2"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "radicados-bot-sg"
  }
}

resource "aws_instance" "radicados_bot" {
  ami           = data.aws_ami.amazon_linux_2023.id
  instance_type = var.instance_type
  
  vpc_security_group_ids = [aws_security_group.radicados_bot.id]

  user_data = templatefile("${path.module}/user_data.sh", {
    mongodb_uri        = var.mongodb_uri
    telegram_bot_token = var.telegram_bot_token
    git_repo_url       = var.git_repo_url
  })

  tags = {
    Name = "radicados-bot"
  }
}

resource "aws_eip" "radicados_bot" {
  instance = aws_instance.radicados_bot.id
  domain   = "vpc"

  tags = {
    Name = "radicados-bot-eip"
  }
  
  lifecycle {
    prevent_destroy = true
  }
}
