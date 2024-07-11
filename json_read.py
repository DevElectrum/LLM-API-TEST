import json

with open("sample.json") as json_file:
    json_data = json.load(json_file)
    metric_value = json_data["metrics"]["component"]["measures"]
    # print(metric_value)

max_list = []
eq = []

with open("included_metrics.json") as json_file1:
    max_data = json.load(json_file1)
    for t in max_data["metrics"]:
        max_list.append(t["max_value"])
        eq.append(t["equalizer"])
    # print(metric_value)

# metrics = ['complexity', 'minor_violations', 'duplicated_lines_density', 'duplicated_lines', 'functions', 'new_vulnerabilities', 'security_remediation_effort', 'classes', 'sqale_index', 'blocker_violations', 'bugs', 'lines_to_cover', 'major_violations', 'new_violations', 'ncloc', 'reliability_remediation_effort', 'line_coverage', 'lines', 'coverage', 'reliability_rating', 'code_smells', 'new_lines', 'security_rating', 'violations', 'sqale_debt_ratio', 'comment_lines_density', 'new_bugs', 'critical_violations', 'new_code_smells', 'info_violations', 'comment_lines', 'uncovered_lines', 'duplicated_blocks', 'files', 'vulnerabilities', 'file_complexity']
metrics = ['reliability_rating', 'new_code_smells', 'new_vulnerabilities', 'sqale_index', 'security_rating', 'new_violations', 'new_bugs']

values = []
w_value = 0
m_value = 0


for i in metric_value:
    if i['metric'] == 'alert_status':
        continue
    elif i['metric'] in ['new_bugs', 'new_vulnerabilities', 'new_violations', 'new_code_smells']:
        values.append(i['period']['value'])
    elif i['metric'] in metrics:
        values.append(i['value'])

for j in range(0, len(eq)):
    w_value += eq[j] * float(values[j])
    m_value += eq[j] * max_list[j]

print(values, max_list)
print(w_value, m_value)

sonar_severity = (w_value / m_value) * 100

print(sonar_severity)

#--------------------------------------------------
#--
# weights = {
#         'ncloc': 1, 'lines': 1, 'files': 2, 'functions': 2, 'classes': 2,
#         'complexity': 3, 'file_complexity': 3,
#         'comment_lines': 1, 'comment_lines_density': 1,
#         'duplicated_lines': 4, 'duplicated_blocks': 4, 'duplicated_lines_density': 4,
#         'violations': 5, 'blocker_violations': 6, 'critical_violations': 5, 'major_violations': 4,
#         'minor_violations': 2, 'info_violations': 1,
#         'code_smells': 3, 'sqale_index': 5, 'sqale_debt_ratio': 4,
#         'bugs': 6, 'reliability_rating': 5, 'reliability_remediation_effort': 4,
#         'vulnerabilities': 6, 'security_rating': 5, 'security_remediation_effort': 4,
#         'coverage': 5, 'line_coverage': 5,
#         'lines_to_cover': 3, 'uncovered_lines': 4,
#         'new_lines': 1, 'new_violations': 5, 'new_bugs': 6, 'new_vulnerabilities': 6, 'new_code_smells': 3,
#         'alert_status': 5
#     }

# metrics_max_values = {
#     'complexity': 200,  # Maximum cyclomatic complexity
#     'minor_violations': 50,  # Maximum minor issues reported
#     'duplicated_lines_density': 10,  # Maximum percentage of duplicated lines (REVIEW)
#     'duplicated_lines': 1000,  # Maximum absolute count of duplicated lines (REVIEW)
#     'functions': 1500,  # Maximum number of functions/methods
#     'new_vulnerabilities': 20,  # Maximum count of new vulnerabilities
#     'security_remediation_effort': 72,  # Maximum effort in hours to remediate security issues
#     'classes': 1000,  # Maximum number of classes (REVIEW)
#     'sqale_index': 500,  # Maximum SQALE index (technical debt)
#     'blocker_violations': 10,  # Maximum count of blocker issues
#     'bugs': 20,  # Maximum count of bugs
#     'lines_to_cover': 5000,  # Maximum lines of code to cover
#     'major_violations': 20,  # Maximum count of major issues
#     'new_violations': 20,  # Maximum count of new violations
#     'ncloc': 5000,  # Maximum lines of non-commented code
#     'reliability_remediation_effort': 120,  # Maximum effort in hours to remediate reliability issues
#     'line_coverage': 100,  # Maximum percentage of line coverage
#     'lines': 20000,  # Maximum total lines of code
#     'coverage': 100,  # Maximum percentage of coverage
#     'reliability_rating': 5,  # Maximum reliability rating (e.g., 1-5 scale)
#     'code_smells': 500,  # Maximum count of code smells
#     'new_lines': 1000,  # Maximum count of new lines of code
#     'security_rating': 5,  # Maximum security rating (e.g., 1-5 scale)
#     'violations': 150,  # Maximum count of all types of violations
#     'sqale_debt_ratio': 20,  # Maximum SQALE debt ratio (%)
#     'comment_lines_density': 50,  # Maximum percentage of comment lines
#     'new_bugs': 20,  # Maximum count of new bugs
#     'critical_violations': 10,  # Maximum count of critical violations
#     'new_code_smells': 50,  # Maximum count of new code smells
#     'info_violations': 20,  # Maximum count of info level violations
#     'comment_lines': 5000,  # Maximum lines of comments
#     'uncovered_lines': 1000,  # Maximum count of uncovered lines
#     'duplicated_blocks': 200,  # Maximum count of duplicated code blocks
#     'files': 500,  # Maximum count of files
#     'vulnerabilities': 50,  # Maximum count of vulnerabilities
#     'file_complexity': 100  # Maximum complexity per file
# }