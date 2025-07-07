
import datetime
import os




blocked_host = ["127.0.0.1", "localhost", "0.0.0.0"]



def isSafeUrl(url):
    for hosts in blocked_host:
        if hosts in url:
            return False
    
    return True

def downloadManual(url):
    safeUrl = isSafeUrl(url)
    if safeUrl:
        # try:
            local_filename = url.split("/")[-1]
            print(f"Downloading manual from {url} to /opt/manualFiles/{local_filename}")
            # Ensure the directory exists
            
        #     r = requests.get(url)
            
        #     with open(f"/opt/manualFiles/{local_filename}", "wb") as f:
        #         for chunk in r.iter_content(chunk_size=1024):
        #             if chunk:
        #                 f.write(chunk)
        #     return True
        # except:
        #     return False
    
    return False

downloadManual("")
downloadManual("http://::1:55782/api/addAdmin?username=a")