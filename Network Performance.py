import subprocess, os, re

results = []
pingAttempts = 10

def pingServer(url):
    print("Pinging " + url + " with iPv4")

    try:
        response = subprocess.check_output("ping -4 -n "+str(pingAttempts)+" "+url)
        print("Test succesful")
        gatherData(response, url)
    except subprocess.CalledProcessError:
        print("Connection timed out or site is not a valid IP")

def gatherData(response, url):
    splitLines = response.splitlines()
    packetLoss = splitLines[pingAttempts+4].split()             #8
    lost = re.sub("\D", "", packetLoss[9].decode('utf-8'))
    percentageLost = re.sub("\D", "", packetLoss[10].decode('utf-8'))

    tripTime = splitLines[pingAttempts+6].split()   #10
    minimum = re.sub("\D", "", tripTime[2].decode('utf-8'))
    maximum = re.sub("\D", "", tripTime[5].decode('utf-8'))
    average = re.sub("\D", "", tripTime[8].decode('utf-8'))
    results.append({'URL': url, 'sent': str(pingAttempts), 'received': str(pingAttempts), 'lost': lost, 'percentagelost': percentageLost
                    ,'minimum': minimum, 'maximum': maximum, 'average': average})

def saveResults():
    with open('resultsFile.csv','w') as resultsFile:
        resultsFile.write('URL'+","+'Packets Sent'+","+'Packets Received'+","+'Packets Lost'+","+'Percentage packets lost (%)'
                               +","+'Minimum Round Trip Time (ms)'+","+'Maximum Round Trip Time (ms)'+","+'Average Round Trip Time (ms)'+'\n')
        for record in results:
           resultsFile.writelines(record['URL']+","+str(record['sent'])+","+str(record['received'])+","+str(record['lost'])+","+str(record['percentagelost'])
                                   +","+record['minimum']+","+record['maximum']+","+record['average']+'\n')

def main():
    sitesFile = open("top100Sites.csv", "r")
    with sitesFile as file:
        for line in file:
            url = re.sub(r"\d+,", "", line).rstrip('\r\n')
            pingServer(url)

    saveResults()

if __name__ == "__main__":
    main()

