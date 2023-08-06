import enum
import json

import typer

from oblv.models.create_deployment_input import CreateDeploymentInput

from . import utils

app = typer.Typer()

regions = ["us-east-1","us-west-2","eu-central-1","eu-west-2"]

class reg(enum.Enum):
    N_Virginia ="us-east-1"
    Oregon ="us-west-2"
    Frankfurt= "eu-central-1"
    London = "eu-west-2"

@app.command(help="To create a deployment")
def create(repo_owner: str = typer.Argument(..., help=("Repository Owner")), repo_name: str = typer.Argument(..., help=("Repository Name")), ref: str = typer.Argument(..., help=("Service ref name")), name: str = typer.Argument(..., help=("Deployment Name")), public: bool = typer.Option(False, "--public", help="If provided, the deployment is made public"), is_dev: bool = typer.Option(False, "--is-dev", help="Sets the environment of the deployment as DEV"),region: reg = typer.Option("us-east-1",help="Region where enclave will be deployed. The options include [\"us-east-1\" (N. Virginia),  \"us-west-2\" (Oregon), \"eu-central-1\" (Frankfurt), \"eu-west-2\" (London)]"),args_file : str = typer.Option(None,help="arguments file path for enclave deployment")):
    try:
        client = utils.read_credentials()
    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    try:
        visibility = "public" if public else "private"
        if args_file==None:
            args_file = typer.prompt("Provide the arguments file for enclave deployment ")
        with open(args_file,"r") as f:
            args = json.load(f)
        input = CreateDeploymentInput(repo_owner,repo_name,"github",ref,region._value_,name,visibility,is_dev,[],args)
        res = client.create_deployment(input)
        # print(res.message)
        print("Deployment created successfully with id - {}".format(res.deployment_id))
    except FileNotFoundError as e:
        print("Could not find the arguments file at \""+args_file+"\"")
    except Exception as e:
        print(e)

@app.command(help="To terminate a deployment")
def terminate(deployment_id: str = typer.Argument(...,help="Deployment Id to terminate")):
    try:
        client = utils.read_credentials()
        client.remove_deployment(deployment_id)
    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    except Exception as e:
        print(e)
    else:
        print("Terminating deployment with id {}".format(deployment_id))

@app.command(help="To get the deployment information.\n\nIf no option is provided, complete information of the deployment is shown")
def info(deployment_id: str = typer.Argument(...,help="Deployment Id for which information is requested"),state: bool = typer.Option(False,"--state",help="To get the current state of deployment"),instance: bool = typer.Option(False,"--instance",help="To get the instance info of deployment"),pcrs: bool = typer.Option(False,"--pcrs",help="To get the pcrs of deployment")):
    try:
        client = utils.read_credentials()
        depl = client.deployment_info(deployment_id)
        if not state and not instance and not pcrs:
            print(depl)
        else:
            resp = {}
            if state:
                resp["state"]=depl.current_state
            if pcrs:
                resp["pcr_codes"]=depl.pcr_codes
            if instance:
                resp["instance"]=depl.instance
            print(resp)
    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    except Exception as e:
        print(e)
        
@app.command(help="To get the owned deployments")
def owned():
    try:
        client = utils.read_credentials()
        depl_l = client.deployments()
        depl = []
        for d in depl_l if depl_l != None else []:
            depl.append({
                "deployment_id": d.deployment_id,
                "deployment_name": d.deployment_name
            })
        print(depl)

    except FileNotFoundError as e:
        print("Kindly login before performing this action")
    except Exception as e:
        print(e)
