import subprocess, os, re

results4 = []
results6 = []
pingAttempts = 10

#ping the server over iPv4 and iPv6
def pingServer(url):
    pingServer4(url)
    pingServer6(url)

#pings the server defined by the parameter url via iPv4 and reads the output of the command to store the result
def pingServer4(url):
    print("Pinging " + url + " with iPv4")

    try:
        response = subprocess.check_output("ping -4 -n "+str(pingAttempts)+" "+url)
        print("Test successful")
        gatherData(response, url, 4)
    except subprocess.CalledProcessError:
        print("Connection timed out or site is not a valid IP")
        reportFailedTest(url, 4)

#pings the server defined by the parameter url via iPv6 and reads the output of the command to store the result
def pingServer6(url):
    print("Pinging " + url + " with iPv6")

    try:
        response = subprocess.check_output("ping -6 -n " + str(pingAttempts)+" "+url)
        print("Test successful")
        gatherData(response, url, 6)
    except subprocess.CalledProcessError as e:
        print("Connection timed out or site does not support iPv6")
        reportFailedTest(url, 6)

#processes the result of a ping to extract useful information and stores this data
def gatherData(response, url, option):
    splitLines = response.splitlines()
    packetLoss = splitLines[pingAttempts+4].split()             #8
    lost = re.sub("\D", "", packetLoss[9].decode('utf-8'))
    percentageLost = re.sub("\D", "", packetLoss[10].decode('utf-8'))

    tripTime = splitLines[pingAttempts+6].split()   #10
    minimum = re.sub("\D", "", tripTime[2].decode('utf-8'))
    maximum = re.sub("\D", "", tripTime[5].decode('utf-8'))
    average = re.sub("\D", "", tripTime[8].decode('utf-8'))

    if(option == 4):
        results4.append({'URL': url, 'sent': str(pingAttempts), 'received': str(pingAttempts), 'lost': lost, 'percentagelost': percentageLost
                        ,'minimum': minimum, 'maximum': maximum, 'average': average, 'Test Status': "Success"})
    else:
        results6.append({'URL': url, 'sent': str(pingAttempts), 'received': str(pingAttempts), 'lost': lost,
                         'percentagelost': percentageLost
                            , 'minimum': minimum, 'maximum': maximum, 'average': average, 'Test Status': "Success"})

#writes the results of both iPv4 and iPv6 tests to two seperate files
def saveResults():
    with open('resultsFileiPv4.csv','w') as resultsFileiPv4:
        resultsFileiPv4.write('URL'+","+'Packets Sent'+","+'Packets Received'+","+'Packets Lost'+","+'Percentage packets lost (%)'
                               +","+'Minimum Round Trip Time (ms)'+","+'Maximum Round Trip Time (ms)'+","+'Average Round Trip Time (ms)'+","+'Test Status'+'\n')
        for record in results4:
           resultsFileiPv4.writelines(record['URL']+","+str(record['sent'])+","+str(record['received'])+","+str(record['lost'])+","+str(record['percentagelost'])
                                   +","+record['minimum']+","+record['maximum']+","+record['average']+","+record['Test Status']+'\n')

           with open('resultsFileiPv6.csv', 'w') as resultsFileiPv6:
               resultsFileiPv6.write(
                   'URL'+","+'Packets Sent'+","+'Packets Received'+","+'Packets Lost'+","+'Percentage packets lost (%)'
                   +","+ 'Minimum Round Trip Time (ms)'+","+'Maximum Round Trip Time (ms)'+","+'Average Round Trip Time (ms)'+","+'Test Status'+'\n')
               for record in results6:
                   resultsFileiPv6.writelines(
                       record['URL']+","+str(record['sent'])+","+str(record['received'])+","+str(record['lost'])+","+
                       str(record['percentagelost'])+","+record['minimum']+","+record['maximum']+","+record['average']+","+record['Test Status'] + '\n')

#saves a failed test report for failed pings
def reportFailedTest(url, option):
    if(option == 4):
        results4.append({'URL': url, 'sent': str(pingAttempts), 'received': 0, 'lost': str(pingAttempts),
                         'percentagelost': 100
                            , 'minimum': "-", 'maximum': "-", 'average': "-", 'Test Status': "Failed"})
    else:
        results6.append({'URL': url, 'sent': str(pingAttempts), 'received': 0, 'lost': str(pingAttempts),
                         'percentagelost': 100
                            , 'minimum': "-", 'maximum': "-", 'average': "-", 'Test Status': "Failed"})

#main method
def main():
    sitesFile = open("top100Sites.csv", "r")
    with sitesFile as file:
        for line in file:
            url = re.sub(r"\d+,", "", line).rstrip('\r\n')
            pingServer(url)

    saveResults()

if __name__ == "__main__":
    main()

