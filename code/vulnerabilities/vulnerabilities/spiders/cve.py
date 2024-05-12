import scrapy
import csv
import json
import sqlite3

class CveSpider(scrapy.Spider):
    name = "cve"
    allowed_domains = ["cve.mitre.org"]
    start_urls = ["https://cve.mitre.org/data/refs/refmap/source-EXPLOIT-DB.html"]

    def parse(self, response):
        # FOR DATABASE STORAGE
        connection = sqlite3.connect('data.db')
        table = 'CREATE TABLE IF NOT EXISTS vuln (exploit TEXT, cve TEXT)'
        cursor = connection.cursor()
        cursor.execute(table)
        connection.commit()
        
        
        # FOR CSV FILE STORAGE
        csv_file = open('data.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(['exploit_id', 'cve_id'])
        
        # FOR JSON FILE STORAGE
        json_file = open('data.json', 'w')
        json_data = {}
        
        for child in response.xpath('//table'):
            if len(child.xpath('tr')) > 100:
                table = child
                break    
        count = 0
        
        for row in table.xpath('//tr'):

            if count > 100:
                break
            try:
                exploit_id = (row.xpath('td//text()')[0].extract())
                cve_id = (row.xpath('td//text()')[2].extract())
                print(exploit_id, cve_id)
                
                # if the entries are whitespace, skip
                if exploit_id.strip() and cve_id.strip():
                    
                    # FOR DATABASE STORAGE
                    cursor.execute('INSERT INTO vuln (exploit, cve) VALUES (?, ?)', (exploit_id, cve_id))
                    connection.commit()
                   
                    # FOR CSV FILE STORAGE
                    writer.writerow([exploit_id, cve_id])      
                    
                    # FOR JSON FILE STORAGE
                    json_data[exploit_id] = cve_id       
                else:   pass    

                count += 1
                
            except IndexError :
                pass
        
        # Commit changes and close files
        connection.close()
        csv_file.close()    
        
        json.dump(json_data, json_file, indent=4)
        json_file.close()
        
