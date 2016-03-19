from bs4 import BeautifulSoup
import re,time
import csv,json,sqlite3
def fix_unicode(data):
	if isinstance(data, unicode):
		return data.encode('utf-8');
	elif isinstance(data, dict):
		data = dict((fix_unicode(k), fix_unicode(data[k])) for k in data);
	elif isinstance(data, list):
		for i in xrange(0, len(data)):
			data[i] = fix_unicode(data[i]);
	return data;
def refine(t):
	t=t.get_text()
	t=fix_unicode(t)
	tt=t.translate(None,'\t\n')
	tt=tt.replace('\xc2\xa0','')
	return(tt.replace(',',''))
#print(refine(temp[3]))
def create_amount_part(temp,n):
	myDict={}
	ind=1;
	myDict[ind]={}
	myDict[ind]["Deb"]=refine(temp[3])
	i=4;
	while(i<n):
			if(i%6==0):
				i+=3;
				ind+=1;
				myDict[ind]={}
				#print("*********")
			else:
				#print(refine(temp[i]))
				if((i+2)%6==0):
					myDict[ind]["Cred"]=refine(temp[i]);
					
				elif((i+3)%6==0):
					myDict[ind]["Deb"]=refine(temp[i]);
				i+=1;
	return(myDict)
############################################################################
def create_date_part(temp1,n,myDict):
	ind=1;
	for i in range(30,n):
		temp2=fix_unicode(temp1[i].get_text())
		pf1=re.compile("\d{2}\-\w+\-\d{4}")
		date=re.search(pf1,temp2)
		if(date!=None):
			myDict[ind]["Date"]=date.group()
			ind+=1;
	return(myDict)
#Convert python dictionary to .csv########################################
def csv_writter(path,sch):
	with open(path+"/name.csv", "w") as toWrite:
		writer = csv.writer(toWrite, delimiter=",");
		writer.writerow(["Index","Date","Debited","Credited"]);
		for a in sch.keys():
			if(sch[a]["Deb"]==" "):
				sch[a]["Deb"]=0;
			if(sch[a]["Cred"]==" "):
				sch[a]["Cred"]=0;

			writer.writerow([(a),sch[a]["Date"],sch[a]["Deb"],sch[a]["Cred"]]);
	time.sleep(1)
###########################################################################
def csv_to_database(path):
	conn = sqlite3.connect(path+"/name.db");
	curs = conn.cursor();
	curs.executescript('drop table if exists Transactions;')
	curs.execute("CREATE TABLE Transactions (INDx INT,DATe char(100),DEBITEd real ,CREDITEd real);");
	reader = csv.reader(open(path+'/name.csv', 'r'), delimiter=',');
	for row in reader:
		to_db = [(row[0]), row[1], row[2], row[3]];
		curs.execute("INSERT INTO Transactions (INDx, DATe,DEBITEd,CREDITEd) VALUES (?, ?, ?, ?);", to_db);
		conn.commit();

#############################################################################
#Convert python dictionary to .JSON
def convert_to_json(path,sch):
	#os.chdir(path);
	with open(path+"/name.json", "w") as writeJSON:
		json.dump(sch, writeJSON)

	
if __name__ == '__main__':
	path="/home/maulo/2Project/data"
	soup=BeautifulSoup(open(path+'/name.html').read(),"lxml");
	temp=soup.find_all("td",{"class":"accountsStatementGrid"})
	temp1=soup.find_all("tr")
	myDict={}
	myDict=create_amount_part(temp,len(temp))
	myDict=create_date_part(temp1,len(temp1),myDict)
	csv_writter(path,myDict)
	csv_to_database(path)
	convert_to_json(path,myDict)


