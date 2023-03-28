# https://developers.google.com/safe-browsing/v4/update-api?hl=pt-br#checking-urls

# https://stackoverflow.com/questions/10855601/google-safebrowsing-api-limits#:~:text=A%20single%20API%20key%20can,in%20a%20single%20POST%20request.
#A single API key can make requests for up to 10,000 clients per 24-hour period.
#You can query up to 500 URLs in a single POST request.

#teste de consistencia de linhas no output "safebrowsing.json" x entrada "mycrawler.json"
# jq length safebrowsing.json
# cat mycrawler-all.jsonl |grep -v file:// |wc -l

import json
from pysafebrowsing import SafeBrowsing
from pysafebrowsing.api import SafeBrowsingWeirdError

jsonl = open('mycrawler-all.jsonl', 'r')
output = open('safebrowsing.json', 'w') # Sobrescreve, caso o arquivo jah exista

# agrupar o conteudo em listas de 500 urls cada ou menos
listlen = 500
KEY = 'HEEEY_put_your_google_cloud_API_Key_here' # Em https://console.cloud.google.com/

s = SafeBrowsing(KEY)

counter = 0
url_list = []
all_lookups =  {}
for line in jsonl:
    try:
        line_json = json.loads(line)
    except:
        continue
    if line_json["desturl"].startswith("http"):
        url = line_json["desturl"]
    else:
        continue
    url_list.append(url)
    counter += 1
    if counter > listlen:
        # faz a query junto ao SafeBrowsing
        ##print(url_list)
        try:
            r = s.lookup_urls(url_list)
        except SafeBrowsingWeirdError:
            pass
        #exemplo de resultado (r)
        #{'http://malware.testing.google.test/testing/malware/': {'malicious': True, 'platforms': ['ANY_PLATFORM'], 'threats': ['MALWARE'], 'cache': '300s'}, 'http://www.lucasprojetos.com.br/': {'malicious': False}}
        # adiciono o resultado (r) ao dicionario all_lookups que serah escrito em arquivo
        all_lookups.update(r)
        url_list = []
        counter = 0

# faz a query junto ao SafeBrowsing - ultima vez ################################
r = s.lookup_urls(url_list)
# adiciono o resultado (r) ao dicionario all_lookups que serah escrito em arquivo
all_lookups.update(r)

to_output = json.dumps(all_lookups)
output.write(to_output)

output.close()
jsonl.close()
