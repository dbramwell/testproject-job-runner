# TestProject Job Runner

A github action to run automated testing jobs via [TestProject](https://testproject.io/)

## Usage
Example:
```yaml
on: [push]

jobs:
  run_testproject_job:
    runs-on: ubuntu-latest
    name: Run TestProject Job
    steps:
      - name: Step to run TestProject Job
        uses: dbramwell/testproject-job-runner
        with:
          api-key: ${{ secrets.TESTPROJECT_API_KEY }}
          project-id: 'abcdefghijklmnopqrstuv'
          job-id: 'abcdefghijklmnopqrstuv'
```
### Options
| Option                 | Description                                                         | Required | Default |
|------------------------|---------------------------------------------------------------------|----------|---------|
| `api-key`              | TestProject API Key with permissions to execute the TestProject job | True     | None    |
| `project-id`           | TestProject Project Id                                              | True     | None    |
| `job-id`               | TestProject Job Id                                                  | True     | None    |
| `execution-parameters` | String in JSON format defining [TestProject job execution parameters](https://api.testproject.io/docs/v2/#/Jobs/Jobs_RunJobAsync) | False     | "{}"    |
| `json-report`          | Set to "on" to download json report to `$GITHUB_WORKSPACE/{job-id}-report.json`  | False     | Off    |
| `junit-report`         | Set to "on" to download junit report to `$GITHUB_WORKSPACE/{job-id}-report.xml`  | False     | Off    |
| `pdf-report`           | Set to "on" to download pdf report to `$GITHUB_WORKSPACE/{job-id}-report.pdf`    | False     | Off    |