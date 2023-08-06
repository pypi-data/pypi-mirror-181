from tools.functions import aws, utils, ssh
import signal

def eksm():
  
  stacks = [
    aws.set_profile,
    aws.set_region,
    aws.set_eks_name
  ]
        
  if utils.ex_stacks(stacks) :
    aws.set_cluster()  

def sshm():
  stacks = [
    ssh.set_profile,
    ssh.set_ssh
  ]
  if utils.ex_stacks(stacks) :
    aws.set_cluster() 

signal.signal(signal.SIGINT, utils.exist_handler)
