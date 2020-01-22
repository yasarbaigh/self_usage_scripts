import subprocess
import datetime
from dateutil.relativedelta import relativedelta


from python3_send_mail import Gmail
 
files_pattern = '/var/log/nginx/user_access.log*'
gz_files_pattern = '/var/log/nginx/user_access.log-*gz'


def prepare_output_in_file(date_pattern, absolute_file_url, zipped_file_url):   
   
   
    
    subprocess.call('gzip -d ' + gz_files_pattern, shell=True)
    
    subprocess.call('echo "header-1    header-2    header-3" ' + " >  " + absolute_file_url, shell=True)
    subprocess.call('cat ' + files_pattern + "  | grep -i " + date_pattern  +  " >>  " + absolute_file_url, shell=True)
    
    subprocess.call("sed -i 's/GET \\///g' " + absolute_file_url, shell=True)
    subprocess.call("sed -i 's/~~~/\t/g' " + absolute_file_url, shell=True)
    subprocess.call("sed -i 's/$//g' " + absolute_file_url, shell=True)
    
    subprocess.call("zip -r -j " + zipped_file_url + "  " + absolute_file_url, shell=True)


today_date = datetime.date.today()

yesterday_date = (today_date + relativedelta(days=-1))
formatted_yesterday_date = str(yesterday_date.strftime("%d/%b/%Y"))
formatted_yesterday_date_2 = str(yesterday_date.strftime("%d_%b_%Y"))  + ".tsv" 


# custom-date
#formatted_yesterday_date = '20/Jan/2020'
#formatted_yesterday_date_2 = '20_Jan_2020' + '.tsv'
 

print("Processing for Date : " +  formatted_yesterday_date)

date_pattern = formatted_yesterday_date


absolute_file_url = "/tmp/disp-imps-logs-" + formatted_yesterday_date_2

zipped_file_name = formatted_yesterday_date_2 + ".zip"
zipped_file_url = "/tmp/disp-imps-logs-" + zipped_file_name
 


prepare_output_in_file(date_pattern, absolute_file_url , zipped_file_url)

