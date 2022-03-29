import json
import os
import requests
import sys
import time

auth_token = sys.argv[1]
project_id = sys.argv[2]
job_id = sys.argv[3]
execution_parameters = json.loads(sys.argv[4])
junit_report = sys.argv[5] == 'on'
json_report = sys.argv[6] == 'on'
pdf_report = sys.argv[7] == 'on'
github_workspace = os.environ['GITHUB_WORKSPACE']

api_url = "https://api.testproject.io"
run_job_url = f"{api_url}/v2/projects/{project_id}/jobs/{job_id}/run"
headers = {'Authorization': f"{auth_token}"}
finished_states = ['Skipped', 'Passed', 'Failed', 'Suspended', 'Aborted', 'Error']

resp = requests.post(run_job_url, headers=headers, json=execution_parameters)

if resp.ok:
  r = resp.json()
  execution_id = r.get('id')
  if execution_id:
    execution_url = f"{api_url}/v2/projects/{project_id}/jobs/{job_id}/executions/{execution_id}/state"
    resp = requests.get(execution_url, headers=headers)
    while resp.ok and resp.json().get('state') not in finished_states:
      info = resp.json()
      print("\n")
      print(f"State: {info['state']}")
      targets = info.get('progress', {}).get('targets', [])
      for target in targets:
        print(f"  Target: {target.get('platform', 'Unknown Platform')} - {target.get('name', 'Unknown Name')}")
        print(f"    Executed {target.get('executedTests', 0)}/{target.get('totalTests', 'Unknown')} tests")
        print(f"    Executed {target.get('executedSteps', 0)}/{target.get('totalSteps', 'Unknown')} total steps")
        for running in target.get('executingTests', []):
          print(f"    Running \"{running.get('name', 'Unknown')}\", Executed {running.get('currentStepIndex', 0)}/{running.get('totalSteps', 0)} steps")

      time.sleep(10)
      resp = requests.get(execution_url, headers=headers)

report_url = f"{api_url}/v2/projects/{project_id}/jobs/{job_id}/reports/{execution_id}"
test_project_report_url = f"{report_url}?format=TestProject"
junit_report_url = f"{report_url}?format=JUnit"
pdf_report_url = f"{report_url}?format=PDF"

if junit_report:
  resp = requests.get(junit_report_url, headers=headers)
  f = open(f"{github_workspace}/{job_id}-report.xml", "wb")
  f.write(resp.content)
  f.close()

if json_report:
  resp = requests.get(test_project_report_url, headers=headers)
  f = open(f"{github_workspace}/{job_id}-report.json", "wb")
  f.write(resp.content)
  f.close()

if pdf_report:
  resp = requests.get(pdf_report_url, headers=headers)
  if resp.ok:
    pdf_url = resp.json().get('reportUrl')
    print(pdf_url)
    if pdf_url:
      resp = requests.get(pdf_url)
      print(resp.ok)
      if resp.ok:
        f = open(f"{github_workspace}/{job_id}-report.pdf", "wb")
        f.write(resp.content)
        f.close()