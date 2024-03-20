import subprocess

def get_terraform_output(tf_output_name) -> str:

    if tf_output_name is None:
        raise ValueError('tf_output_name not specified')

    terraform_output = subprocess.run(["terraform", "output", tf_output_name], cwd="../terraform", capture_output=True, text=True).stdout
    terraform_output = terraform_output.replace('"', '').replace('\n', '')

    return terraform_output