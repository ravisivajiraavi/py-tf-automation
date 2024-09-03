provider "aws" {
    region = "us-east-1"  
}
provider "random" {}

resource "random_pet" "name" {}

resource "aws_instance" "web" {
  ami           = "ami-0e86e20dae9224db8"
  instance_type = "t2.micro"
  user_data     = file("init-script.sh")

  tags = {
    Name = "random_pet.name.id"
  }
}