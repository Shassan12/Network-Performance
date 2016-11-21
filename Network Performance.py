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
        #ping the site with iPv4 and save the output
        response = subprocess.check_output("ping -4 -n "+str(pingAttempts)+" "+url)
        #output success message
        print("Test successful")
        #extract useful data from output
        gatherData(response, url, 4)
    except subprocess.CalledProcessError:
        #report that ping test failed for this site
        print("Connection timed out or site is not a valid IP")
        #save a failed test for this site
        reportFailedTest(url, 4)

#pings the server defined by the parameter url via iPv6 and reads the output of the command to store the result
def pingServer6(url):
    print("Pinging " + url + " with iPv6")

    try:
        #ping the site with iPv6 and save the output
        response = subprocess.check_output("ping -6 -n " + str(pingAttempts)+" "+url)
        #output success message
        print("Test successful")
        #extract useful data from output
        gatherData(response, url, 6)
    except subprocess.CalledProcessError as e:
        #report that ping test failed for this site
        print("Connection timed out or site does not support iPv6")
        #save failed test result for this site
        reportFailedTest(url, 6)

#processes the result of a ping to extract useful information and stores this data
def gatherData(response, url, option):
    #split output from ping by newlines
    splitLines = response.splitlines()
    #get the line containing packetloss data
    packetLoss = splitLines[pingAttempts+4].split()
    #get the number of packets lost
    lost = re.sub("\D", "", packetLoss[9].decode('utf-8'))
    #get the percentage packet loss
    percentageLost = re.sub("\D", "", packetLoss[10].decode('utf-8'))

    #get the line containing round trip data
    tripTime = splitLines[pingAttempts+6].split()   #10
    #get minimum pround trip time
    minimum = re.sub("\D", "", tripTime[2].decode('utf-8'))
    #get maximum pround trip time
    maximum = re.sub("\D", "", tripTime[5].decode('utf-8'))
    #get average pround trip time
    average = re.sub("\D", "", tripTime[8].decode('utf-8'))

    #if ping was using iPv4, store a iPv4 record for the site otherwise store an iPv6 version
    if(option == 4):
        results4.append({'URL': url, 'sent': str(pingAttempts), 'received': str(pingAttempts), 'lost': lost, 'percentagelost': percentageLost
                        ,'minimum': minimum, 'maximum': maximum, 'average': average, 'Test Status': "Success"})
    else:
        results6.append({'URL': url, 'sent': str(pingAttempts), 'received': str(pingAttempts), 'lost': lost,
                         'percentagelost': percentageLost
                            , 'minimum': minimum, 'maximum': maximum, 'average': average, 'Test Status': "Success"})

#writes the results of both iPv4 and iPv6 tests to two seperate files
def saveResults():
    #write iPv4 records to file
    with open('resultsFileiPv4.csv','w') as resultsFileiPv4:
        resultsFileiPv4.write('URL'+","+'Packets Sent'+","+'Packets Received'+","+'Packets Lost'+","+'Percentage packets lost (%)'
                               +","+'Minimum Round Trip Time (ms)'+","+'Maximum Round Trip Time (ms)'+","+'Average Round Trip Time (ms)'+","+'Test Status'+'\n')
        for record in results4:
           resultsFileiPv4.writelines(record['URL']+","+str(record['sent'])+","+str(record['received'])+","+str(record['lost'])+","+str(record['percentagelost'])
                                   +","+record['minimum']+","+record['maximum']+","+record['average']+","+record['Test Status']+'\n')

    #write iPv6 records to file
    with open('resultsFileiPv6.csv', 'w') as resultsFileiPv6:
        resultsFileiPv6.write('URL'+","+'Packets Sent'+","+'Packets Received'+","+'Packets Lost'+","+'Percentage packets lost (%)'
                                +","+ 'Minimum Round Trip Time (ms)'+","+'Maximum Round Trip Time (ms)'+","+'Average Round Trip Time (ms)'+","+'Test Status'+'\n')
        for record in results6:
            resultsFileiPv6.writelines(record['URL']+","+str(record['sent'])+","+str(record['received'])+","+str(record['lost'])+","+
                            str(record['percentagelost'])+","+record['minimum']+","+record['maximum']+","+record['average']+","+record['Test Status'] + '\n')

#saves a failed test report for failed pings
def reportFailedTest(url, option):
    #save a failed test record for iPv4 for this site otherwise save a failed test report for iPv6
    if(option == 4):
        results4.append({'URL': url, 'sent': str(pingAttempts), 'received': 0, 'lost': str(pingAttempts),
                         'percentagelost': 100
                            , 'minimum': "#N/A", 'maximum': "#N/A", 'average': "#N/A", 'Test Status': "Failed"})
    else:
        results6.append({'URL': url, 'sent': str(pingAttempts), 'received': 0, 'lost': str(pingAttempts),
                         'percentagelost': 100
                            , 'minimum': "#N/A", 'maximum': "##N/A", 'average': "##N/A", 'Test Status': "Failed"})

#main method
def main():
    sitesFile = open("top100Sites.csv", "r")
    with sitesFile as file:
        for line in file:
            url = re.sub(r"\d+,", "", line).rstrip('\r\n')
            pingServer(url)

    print("Done")
    saveResults()

if __name__ == "__main__":
    main()

