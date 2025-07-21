import yaml 

with open("data_validation_report.yaml", 'w') as report_file:
    report = {'STATUS': False}
    yaml.dump(report, report_file)