import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from python_terraform import Terraform, IsFlagged, TerraformCommandError

# Set up logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)

# Create a file handler for logging
file_handler = RotatingFileHandler('terraform_automation.log', maxBytes=1024*1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

# Create a console handler for logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(log_format))

# Get the root logger
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def run_terraform():
    
    # tf_workingdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
    try:
        logger.info("Starting Terraform automation script...")

        # Prompt the user to select an action
        action = input("Choose a Terraform action (init/plan/apply/destroy): ").strip().lower()
        
        if action not in ["init","plan", "apply", "destroy"]:
            logger.error("Invalid action. Please choose 'plan', 'apply', or 'destroy'.")
            return

        # Initialize Terraform object
        tf = Terraform(working_dir='C:\Raavi\Python_Terraform_Automation_Tool\pytfautomationtool')

        if action == "init":
            # Initialize Terraform
            logger.info("Initializing Terraform...")
            return_code, stdout, stderr = tf.init(capture_output=False)
            logger.debug(f"Terraform init STDOUT: {stdout}")
            logger.debug(f"Terraform init STDERR: {stderr}")

        elif action == "plan":
            # Generate a plan
            logger.info("Generating Terraform plan...")
            return_code, stdout, stderr = tf.plan(out="terraform.tfplan")
            logger.debug(f"Terraform plan STDOUT: {stdout}")
            logger.debug(f"Terraform plan STDERR: {stderr}")

        elif action == "apply":           
            # Confirm apply action
            confirm = input("Are you sure you want to apply the changes? (yes/no): ").strip().lower()
            if confirm == "yes":
                logger.debug("Applying Terraform plan...")
                return_code, stdout, stderr = tf.apply(skip_plan=True, auto_approve=True)
                logger.debug(f"Terraform apply STDOUT: {stdout}")
                logger.debug(f"Terraform apply STDERR: {stderr}")
            else:
                logger.info("Terraform apply action canceled by user.")

        elif action == "destroy":
            # Confirm destroy action
            confirm = input("Are you sure you want to destroy the infrastructure? (yes/no): ").strip().lower()
            if confirm == "yes":
                logger.debug("Destroying Terraform-managed infrastructure...")
                return_code, stdout, stderr = tf.destroy(auto_approve=True)
                logger.debug(f"Terraform destroy STDOUT: {stdout}")
                logger.debug(f"Terraform destroy STDERR: {stderr}")
            else:
                logger.info("Terraform destroy action canceled by user.")

        if return_code == 0:
            logger.info(f"Terraform {action} completed successfully.")
        else:
            logger.error(f"Terraform {action} failed.")

    except TerraformCommandError as e:
        logger.error(f"Terraform command failed: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Terraform automation script finished.")

if __name__ == "__main__":
    run_terraform()
