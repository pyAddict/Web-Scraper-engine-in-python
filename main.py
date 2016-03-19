#Used this micro framework to show our data on the browser with "localhost:5000/result"
from flask import *
import sqlite3
import os,json
import matplotlib.pyplot as plt
#import the sqlite database which I previously made.
DATABASE = '/home/maulo/2Project/data/name.db'
app = Flask(__name__)
app.config.from_object(__name__)
#used in the connection with database
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
#Used to convert unicode to string
def fix_unicode(data):
	if isinstance(data, unicode):
		return data.encode('utf-8');
	elif isinstance(data, dict):
		data = dict((fix_unicode(k), fix_unicode(data[k])) for k in data);
	elif isinstance(data, list):
		for i in xrange(0, len(data)):
			data[i] = fix_unicode(data[i]);
	return data;

def modify_details(dict):
	date_list=[];
	deb_list=[];
	cred_list=[];j=0;
	for i in dict.keys():
		date_list.append(dict[i]["date"])
		cred_list.append(dict[i]["cred"] if((dict[i]["cred"])!=" ") else 0 )
		deb_list.append(dict[i]["deb"] if((dict[i]["deb"])!=" ") else 0 )
	'''for i in date_list:
		j+=1;
		print(i)
		print(type(i))
	print(j)'''
	new_dict_deb={}
	new_dict_cred={}
	new_dict_deb[date_list[0]]=deb_list[0]
	new_dict_cred[date_list[0]]=cred_list[0]
	for i in range(1,len(date_list)):
		if(date_list[i]==date_list[i-1]):
			new_dict_deb[date_list[i]]+=deb_list[i];
			new_dict_cred[date_list[i]]+=cred_list[i];

		else:
			new_dict_deb[date_list[i]]=deb_list[i]
			new_dict_cred[date_list[i]]=cred_list[i]

	labels=[];final_amnt_deb=[];final_amnt_cred=[]
	for i in new_dict_deb.keys():
		labels.append(i)
		final_amnt_deb.append(new_dict_deb[i])
	for i in new_dict_cred.keys():
		final_amnt_cred.append(new_dict_cred[i])
	return(labels,final_amnt_deb,final_amnt_cred)

@app.route('/result')
#used to pull the information from database save to a dictionary and then display to the html webpage
def disp():
	g.db=connect_db()
	j=0;
	mydict={};
	#Pull the data from database
	for row in g.db.execute('SELECT * FROM Transactions'):
		#Logic to omit the label of the table
		if(j>0):
			mydict[row[0]]={}
			mydict[row[0]]["date"]=fix_unicode(row[1])
			mydict[row[0]]["deb"]=fix_unicode(row[2])
			mydict[row[0]]["cred"]=fix_unicode(row[3])
		j+=1;
	#As in same date there may be more than one transaction,So handle those cases my modify_details()
	#Save the pie chart
	modify_details(mydict)
	(labels,final_amnt_deb,final_amnt_cred)=modify_details(mydict)
	temp_dict_deb={'Sep':0,'Oct':0,'Nov':0,'Dec':0,'Jan':0,'Feb':0,'Mar':0}
	temp_dict_cred={'Sep':0,'Oct':0,'Nov':0,'Dec':0,'Jan':0,'Feb':0,'Mar':0}
	for i in range(0,len(labels)):
		aa=list(labels[i])
		aaa=''.join(aa[3:6])
		temp_dict_deb[aaa]+=final_amnt_deb[i]
		temp_dict_cred[aaa]+=final_amnt_cred[i]
	#Plotting and saving figure############################################
	'''plt.figure(1, figsize=(6,6))
	ax = plt.axes([0.1, 0.1, 0.8, 0.8])
	plt.pie(temp_dict_deb.values(), labels=temp_dict_deb.keys(),autopct='%1.1f%%', shadow=True, startangle=90);
	plt.title('Debit Details  ', bbox={'facecolor':'0.8', 'pad':5})
	plt.figure(2, figsize=(6,6))
	plt.axes([0.1, 0.1, 0.8, 0.8])
	plt.pie(temp_dict_cred.values(), labels=temp_dict_cred.keys(),autopct='%1.1f%%', shadow=True, startangle=90);
	plt.title('Credit Details  ', bbox={'facecolor':'0.8', 'pad':5})
	fig1=plt.figure(1, figsize=(6,6))
	fig1.savefig('/home/maulo/2Project/final_project/static/debit.png')
	fig2=plt.figure(2, figsize=(6,6))
	fig2.savefig('/home/maulo/2Project/final_project/static/credit.png')'''
	#########################################################################################
	#Making suitable .JSON file
	with open("/home/maulo/2Project/final_project/static/nameDeb.json", "w") as writeJSON:
		json.dump(temp_dict_deb, writeJSON)
	with open("/home/maulo/2Project/final_project/static/nameCred.json", "w") as writeJSON:
		json.dump(temp_dict_cred, writeJSON)
	return render_template('abc.html',result=mydict)
	#return render_template('tabular.html', result=mydict)



if __name__ == '__main__':
   app.run(debug=True)