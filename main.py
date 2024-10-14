from prometheus_client import start_http_server, Gauge
import time
import requests
import warnings
warnings.filterwarnings("ignore")
server = 'http://100.100.240.205:9000'
stats_podpislon = Gauge('sonarqube_python', 'Sonarqube from API statistics', ['project_key','name','metric'])
headers = {
        'Accept': '*/*',
        'Authorization': 'Bearer squ_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    }
url_projects = server + '/api/projects/search'

req_projects = requests.get(url_projects, headers=headers, verify=False)
projects = req_projects.json()

def get_stats(project_key):

    url_analyses = server + \
    '/api/measures/component?' \
    'component=' \
    + project_key + \
    '&metricKeys=' \
    'complexity,bugs,code_smells,comment_lines_density,accepted_issues,coverage,reliability_issues,duplicated_lines_density,violations,lines,open_issues,security_hotspots,vulnerabilities'
    
    req = requests.get(url_analyses, headers=headers, verify=False)
    data = req.json()
    names = data['component']['measures']
    for i in range(0,len(names),1):
        if names[i]['metric'] != 'reliability_issues':
            stats_podpislon.labels( project_key, data['component']['name'], 
                                names[i]['metric']).set(names[i]['value'])
        else:
            rel_iss_value = names[i]['value'][names[i]['value'].index('total')+7:len(names[i]['value'])-1]
            stats_podpislon.labels( project_key, data['component']['name'], 
                                names[i]['metric']).set(rel_iss_value)
if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(18000)
    # Generate some requests.
    while True:
        req_projects = requests.get(url_projects, headers=headers, verify=False)
        projects = req_projects.json()
        for j in range(0,len(projects['components']),1):
            get_stats(projects['components'][j]['key'])
        time.sleep(10)
