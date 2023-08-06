import click
import os
import requests
import json
from sys import *


# Command Group
@click.group(name='configure')
def configure():
    pass

# Creating command 
@configure.command(name='configure')
def configure():
    """If this command is run with no arguments, you will be prompted for configuration values such as your  aitest  APIKey.If your configure file does not  exist
       (the default location is ~/.aitest/configure), the aitest CLI will create it for you.To keep an existing value, hit enter when prompted for the value.

       To save the configurations , you can run below command:\n
       vijay configure
              

    """
    apikey = input('Enter APIkey:')
    if apikey:
        folder_path =os.path.join( os.path.expanduser('~'),".vijay" )
        folder_exist = os.path.exists(folder_path)
        if not folder_exist:
            os.mkdir(folder_path)
            fd = open(os.path.join(folder_path, "configure"), 'w')
            fd.write(apikey)
            fd.close()
        else:
            fd = open(os.path.join(folder_path, "configure"), 'w')
            fd.write(apikey)
            fd.close()

# Command Group  
@click.group(name='run')
def run():
    pass

# Creating command
@run.command(name='run')
@click.argument("testrun_id")
def run(testrun_id):
    """If this command is run with testrun id as an argument, aitest CLI will create new test for you with same configuration of provided testrun id.


       To re-run the test, you can run below command:\n
       vijay run [testrun id]
    """    

    try:
        file_path =os.path.join( os.path.expanduser('~'),".vijay","configure" )
        fd = open(file_path,'r')
        bearer_token=fd.read().replace('Bearer ','')
    except:
        click.echo("\nPlease run the following command first:\n\nvijay configure\n")
        exit()


    headers = {"Authorization": f"Bearer {bearer_token}"}
    base_url = f"https://api.aitest.dev.appliedaiconsulting.com/testrun/{testrun_id}"
    
    try:
        res =requests.get(base_url,headers=headers)
        ex_test_data=res.json()

        if ex_test_data['test_details']['test_type']=="URL Health Check": # url test logic 
            new_test_name=ex_test_data['test_details']['testrun_name']
            new_test_url=ex_test_data['test_details']['aut_url']
            new_test_project_id=ex_test_data['test_details']['project_id']
            browser_under_test=ex_test_data['test_details']['testrun_browsers']

            # creating new list for storing the updated dictionary data .
            new_browser_under_test= []

            for i in browser_under_test:
                d = i
                d['browser_version']=d['versions'][0]
                d['browser_name']=d['name']
                del d['versions']
                del d['name']
                d['browser_resolution']="840x940"
                d['browser_count']=1
                new_browser_under_test.append(d)

            data = {    "aut_url":new_test_url,
                        "test_Description":"github",
                        "project_id":new_test_project_id,
                        "testrun_name":new_test_name,
                        "browser_under_test":new_browser_under_test
                    }

            payload = json.dumps(data)

            headers = {"Authorization": f"Bearer {bearer_token}"}
            base_url = "https://api.aitest.dev.appliedaiconsulting.com/testrun/url_test"
            
            res2 =requests.post(base_url,data=payload,headers=headers)
            test_data=res2.json()
            click.echo(f"\nTest created successfully\nTest Name : {test_data['test_details']['testrun_name']}\nTest Run ID : {test_data['test_details']['testrun_id']}\n")
        
        elif ex_test_data['test_details']['test_type']=="functional_test":  # Multibrowsertest logic
            git_pass=input("Enter github password: ")
            browser_under_test=ex_test_data['test_details']['testrun_browsers']
            new_browser_under_test= []

            for i in browser_under_test:
                d = i
                d['browser_version']=d['versions'][0]
                d['browser_name']=d['name']
                del d['versions']
                del d['name']
                d['browser_resolution']="840x940"
                d['browser_count']=1
                new_browser_under_test.append(d)

            
            project_id= ex_test_data['test_details']['project_id']
            testrun_name= ex_test_data['test_details']['testrun_name']
            version_control_url= ex_test_data['test_details']['version_control_url']
            git_username= ex_test_data['test_details']['git_username']
            git_password= git_pass
            s3_uri= ex_test_data['test_details']['s3_uri']
            report_file_location= ex_test_data['test_details']['report_file_location']
            report_file_name= ex_test_data['test_details']['report_name']
            testrun_command= ex_test_data['test_details']['testrun_command']
            test_Description= ex_test_data['test_details']['test_Description']
            browser_under_testmul= new_browser_under_test
            max_users= ex_test_data['test_details']['max_users']
            initial_users= ex_test_data['test_details']['initial_users']
            iteration= ex_test_data['test_details']['iteration']
            duration= ex_test_data['test_details']['duration']
            ramp_up_users= ex_test_data['test_details']['ramp_up_users']
            ramp_up_time= ex_test_data['test_details']['ramp_up_time']



            multibrowsertest = {
                        "test_type": "functional_test",
                        "project_id": project_id,
                        "testrun_name": testrun_name,
                        "version_control_url": version_control_url,
                        "git_username": git_username,
                        "git_password": git_password,
                        "s3_uri": s3_uri,
                        "report_file_location": report_file_location+report_file_name,
                        "testrun_command": testrun_command,
                        "test_Description": test_Description,
                        "browser_under_test": browser_under_testmul,
                        "max_users": max_users,
                        "initial_users": initial_users,
                        "iteration": iteration,
                        "duration": duration,
                        "ramp_up_users": ramp_up_users,
                        "ramp_up_time": ramp_up_time
                    }

            payload = json.dumps(multibrowsertest)

            headers = {"Authorization": f"Bearer {bearer_token}"}
            base_url = "https://api.aitest.dev.appliedaiconsulting.com/testrun/load_test"
            
            res2 =requests.post(base_url,data=payload,headers=headers)
            test_data=res2.json()
            click.echo(f"\nTest created successfully\nTest Name : {test_data['load_test_details']['testrun_name']}\nTest Run ID : {test_data['load_test_details']['testrun_id']}\n")


        elif ex_test_data['test_details']['test_type']=="load_test": # Performance test logic
            git_pass=input("Enter github password: ")
            browser_under_test=ex_test_data['test_details']['testrun_browsers']
            new_browser_under_test= []

            for i in browser_under_test:
                d = i
                d['browser_version']=d['versions'][0]
                d['browser_name']=d['name']
                del d['versions']
                del d['name']
                d['browser_resolution']="840x940"
                d['browser_count']=1
                new_browser_under_test.append(d)

            
            project_id= ex_test_data['test_details']['project_id']
            testrun_name= ex_test_data['test_details']['testrun_name']
            version_control_url= ex_test_data['test_details']['version_control_url']
            git_username= ex_test_data['test_details']['git_username']
            s3_uri= ex_test_data['test_details']['s3_uri']
            report_file_location= ex_test_data['test_details']['report_file_location']
            report_file_name= ex_test_data['test_details']['report_name']
            testrun_command= ex_test_data['test_details']['testrun_command']
            test_Description= ex_test_data['test_details']['test_Description']
            browser_under_testmul= new_browser_under_test
            max_users= ex_test_data['test_details']['max_users']
            initial_users= ex_test_data['test_details']['initial_users']
            iteration= ex_test_data['test_details']['iteration']
            duration= ex_test_data['test_details']['duration']
            ramp_up_users= ex_test_data['test_details']['ramp_up_users']
            ramp_up_time= ex_test_data['test_details']['ramp_up_time']
            s3_uri= ex_test_data['test_details']['s3_uri']


            performancetest = {
                        "duration": duration,
                        "git_password": git_pass,
                        "git_username": git_username,
                        "initial_users": initial_users,
                        "iteration": iteration,
                        "max_users": max_users,
                        "project_id": project_id,
                        "ramp_up_time": ramp_up_time,
                        "ramp_up_users": ramp_up_users,
                        "report_file_location": report_file_location+report_file_name,
                        "s3_uri": s3_uri,
                        "testrun_command": testrun_command,
                        "testrun_name": testrun_name,
                        "version_control_url": version_control_url
                    }

            payload = json.dumps(performancetest)

            headers = {"Authorization": f"Bearer {bearer_token}"}
            base_url = "https://api.aitest.dev.appliedaiconsulting.com/testrun/load_test"
            
            res2 =requests.post(base_url,data=payload,headers=headers)
            test_data=res2.json()
            click.echo(f"\nTest created successfully\nTest Name : {test_data['load_test_details']['testrun_name']}\nTest Run ID : {test_data['load_test_details']['testrun_id']}\n")
    except:
        click.echo("\nToken Expired, Please run below command :\n")
        click.echo("aitest configure")

# Command Group 
@click.group(name='status')
def status():
    """ status command is use to display the status of particular test.  """
    pass

# Creating command
@status.command(name='status')
@click.argument("testrun_id")
def status(testrun_id):
    """ If this command is run with testrun id as an argument, aitest CLI will display the test details .\n  
        To see the status of test , you can run below command:\n
        vijay status [testrun_id]
    """
    try:
        file_path =os.path.join( os.path.expanduser('~'),".vijay","configure" )
        fd = open(file_path,'r')
        bearer_token=fd.read().replace('Bearer ','')
    except:
        click.echo("\nPlease run the following command first:\n\naitest configure\n")
        exit()

    headers = {"Authorization": f"Bearer {bearer_token}"}
    base_url = f"https://api.aitest.dev.appliedaiconsulting.com/testrun_result/status/{testrun_id}"
    try:
        status_res =requests.get(base_url,headers=headers)
        status_test_data=status_res.json()
        test_status = status_test_data['testrun_status'] 
        testrun_status_details=status_test_data['testrun_status_details']
        click.echo(f"\ntest status : {test_status}\n")
        for i in testrun_status_details:
            click.echo(f"   {i['browser_name']}-{i['browser_version']}    test run result id: {i['testrun_result_id']}   status: {i['testrun_result_status']}   time taken: {i['time_taken']} secs", )
    except:
        click.echo("\nToken Expired , Please run below command :\n")
        click.echo("aitest configure\n")
        

