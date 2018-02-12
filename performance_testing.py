from selenium import webdriver
import pandas as ps

import collections
Performance = collections.namedtuple('Performance', ['front', 'back'])

def getPerformance(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")
    domComplete = driver.execute_script("return window.performance.timing.domComplete")
    
    driver.quit()
    
    frontendPerformance = domComplete - responseStart
    backendPerformance = responseStart - navigationStart
    
    result = Performance(frontendPerformance, backendPerformance)
    
    return result

icon_pages = ps.read_csv("icons_input.csv")

experiments = 20

for index, page in icon_pages.iterrows():
    print(page["URL"])
    
    frontSum = 0
    backSum = 0
    
    for i in range(1, experiments + 1):
        
        expResult = getPerformance(page["URL"])
        print("%s - Front End: %sms" % (i, expResult.front))
        print("    Back End: %sms" % expResult.back)

        frontTitle = "Front: Exp " + "%02d" % i
        backTitle = "Back: Exp " + "%02d" % i
        
        icon_pages.loc[index, frontTitle] = expResult.front
        icon_pages.loc[index, backTitle] = expResult.back
        
        frontSum += expResult.front
        backSum += expResult.back
        
    icon_pages.loc[index, "Front: Avg"] = frontSum / experiments
    icon_pages.loc[index, "Back: Avg"] = backSum/ experiments

icon_pages.to_csv("icons_output.csv")







        
        
        
        