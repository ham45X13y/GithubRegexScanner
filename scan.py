"""
Useage: This is only to be used in a researching purpose. No vouch for missuse
"""
import requests
import os
import shutil
import git

# global config:
total, used, free = shutil.disk_usage("/")
baseurlCode=" https://api.github.com/search/code?q="
wordlist=['openai','chatgpt','chatgpt3','chatgpttoken','GPT-3','gpt-4','gpt-35','openai-api','openaiapi','chatgpt api']
customHeaders={
    'Accept': 'application/json',
    'Authorization': 'Bearer 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', # Token expiration is intended :) 
    'X-GitHub-Api-Version': '2022-11-28'
}

regexPattern="sk-^[a-zA-Z0-9]{32}"

# directory config
parentdir="/tmp/gitquery"
tmpdir=parentdir+"/tmp"
storefile=parentdir+"/store"
logfile=parentdir+"/log"
savefile=parentdir+"/save"
tmpstore=parentdir+"/tmpstore"


def is_valid_api_key(apiKey):
    """Checks for validity as a openai api key"""
    head={
        'Authorization': f'Bearer {apiKey}'
    }
    print("[+] Called token test with token: "+apiKey)
    url="https://api.openai.com/v1/models"
    response = requests.get(url,headers=head)
    return response.status_code == 200

def getSizeOfRepo(url):
    count=0
    tname=""
    for i in reversed(url):
        if i == "/":
            count +=1
        if count == 2:
            break
        else:
            tname += i
    name=""
    for i in reversed(tname):
        name+=i
    r = requests.get("https://api.github.com/repos/"+name)
    s=r.json()["size"]
    if s is not None:
        return s
    else:
        return -1


def cloneScanDelete(htmlUrl):
    findings=[]
    total, used, free = shutil.disk_usage("/")

    #check for space
    if((free //2*30) <= 50):
        print("[+] Error: out of free space. Exit.")
        exit(1)
    
    # get repository
    os.mkdir(tmpdir)
    git.Git(tmpdir).clone(htmlUrl+".git")
    print("[+] cloned "+htmlUrl+" with "+str(getSizeOfRepo(htmlUrl)//1000000)+"mb of Data")
    with open(logfile,'a') as f:
        f.write("[+] cloned "+htmlUrl)
        f.close()
    
    # search
    print("[+] start searching...")
    with open(logfile,'a') as f:
        f.write("[+] started searching in "+htmlUrl+"\n")
        f.close()
    os.system("grep -rwoh -E '"+regexPattern+"' "+tmpdir+" > "+tmpstore)
    
    #logging
    with open(tmpstore,'r') as tm:
        with open(storefile,'a') as f:
            f.write(tm.read()+"\n")

    with open(tmpstore) as f:
        findings = [line.rstrip('\n') for line in f]
        f.close()

    for i in findings:
        if is_valid_api_key(i):
            with open(savefile,'a') as f:
                f.write("Found Key,repo: "+i+", "+htmlUrl+"\n")
                print("[+] Found Key,repo: "+i+", "+htmlUrl)
                f.close()

    # clean up
    total, used, free = shutil.disk_usage("/")
    with open(logfile,'a') as f:
        f.write("[+] system space total,used,free "+str(total)+","+str(used)+","+str(free)+"\n")
        f.close()

    shutil.rmtree(tmpdir)
    print("[+] removed repository")
    with open(logfile,'a') as f:
        f.write("[+] removed repository "+htmlUrl+"\n")
        f.close()
    
    total, used, free = shutil.disk_usage("/")
    print("[+] free space: "+str(total//2**30)+","+str(used//2**30)+","+str(free//2**30)+"\n")


def main():

    # init directory
    print("[+] INIT: creating directory")
    if os.path.isdir(parentdir):
        shutil.rmtree(parentdir)

    os.mkdir(parentdir)
    open(savefile,'a').close()
    open(logfile,'a').close()
    open(storefile,'a').close()
    repo_list=[]
    responseList=[]
    tmp=[]

    # get response from git api with all repositorys
    not200code=0
    print("[+] INIT: sending requests to git api")
    for i in wordlist:
        r = requests.get(url=baseurlCode+i,headers=customHeaders)
        if r.status_code != 200:
            not200code +=1
            continue

        x = r.json()
        responseList.append(x)
    print("[+] INIT: got "+str(not200code)+" responses that were not sc 200 ")

    # get all repository names
    for i in responseList:
        for j in i["items"]:
            repo_list.append(j["repository"]["html_url"])

    print("[+] INIT: over all found "+str(len(repo_list))+" repositories")
    # shorten list
    [tmp.append(c) for c in repo_list if c not in tmp]    
    repo_list = tmp
    print("[+] INIT: removed doubles to now "+str(len(repo_list)))
    print("[+] INIT finished. starting now. \n")


    # run search
    a=1
    for i in repo_list:
        print("[+] scan "+str(a)+"/"+str(len(repo_list)))
        cloneScanDelete(i)
        a +=1
    
    print("[+] Finished.")
    print("[+] Note: It is recommended to move all findings to a different location before rerunning to avoid deletion")
    print("[+] Bye")



main()


# token: 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
# valid until 29.04.23 