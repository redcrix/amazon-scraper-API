from flask import Flask, request, json
from bs4 import BeautifulSoup
import urllib3
import pandas as pd
import io

app=Flask(__name__)
@app.route('/', methods=['POST','GET'])
def input():
	if request.method == 'POST':
		url = str(request.form['url'])
		n = int(request.form['pgno'])

		def level1(url, soup):
			for i in soup.find_all('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2'):
				if '/dp/' in i.find('a').attrs['href']:
					#if a>2:
						#break
					level2(str('https://www.amazon.in'+i.find('a').attrs['href']))
					#a+=1
			return print(url, "MU >>> DONE")

		def level2(purl):
			p_http=urllib3.PoolManager()
			p_response=p_http.request('GET',purl)
			a=BeautifulSoup(p_response.data)
			with open('testing.html','w') as file:
				file.write(str(a))
			p_soup=BeautifulSoup(open("testing.html"), "html.parser")
			print('>>>',purl)
			f.write('"')
			try:
				f.write(str(p_soup.find('span', id='productTitle').text.strip().replace('"',"'")))
			except:
				print('Not Found')
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				f.write(str(p_soup.find('a', id='bylineInfo').text.strip()))
			except:
				print('Not Found')
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				for div in p_soup.findAll('div', {'id': 'imgTagWrapperId'}):
					f.write(str(div.find('img')['data-a-dynamic-image'].split('"')[1]))
			except:
				print("Not Found")
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				f.write(str(p_soup.find('span', class_='priceBlockStrikePriceString a-text-strike').text.strip()))
			except:
				print('Not Found')
				try:
					f.write(str(p_soup.find('span', id='priceblock_ourprice').text.strip()))
				except:
					try:
						f.write(str(p_soup.find('span', id='priceblock_dealprice').text.strip()))
					except:
						print("Not Found")
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				f.write(str(p_soup.find('span', class_='arp-rating-out-of-text a-color-base').text.strip()))
			except:
				print("Not Found")
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				f.write(str(p_soup.find('span', id='acrCustomerReviewText').text))
			except:
				print("Not Found")
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				for div in p_soup.findAll('a', {'id': 'askATFLink'}):
					f.write(str(div.find('span', class_='a-size-base').text.strip()))
			except:
				print("Not Found")
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				for div in p_soup.findAll('div', {'id': 'productDescription'}):
					f.write(str(div.find('p').text.strip().replace('"', "'")))
			except:
				print("Not Found")
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				for div in p_soup.findAll('div', id='feature-bullets'):
					for i in div.findAll('span', class_='a-list-item'):
						f.write(str(i.text.strip().replace('"', "'")))
			except:
				print("Not Found")
			f.write('"')
			f.write(',')
			f.write('"')
			try:
				for div in p_soup.findAll('div', class_='a-expander-content reviewText review-text-content a-expander-partial-collapse-content'):
					for i in div.findAll('span'):
						f.write(str(i.text.strip().replace('"', "'")))
						f.write('***')
			except:
				print("Not Found")
			f.write('"')
			f.write('\n')
			return print(purl, ' PU>>> Done')
		def result():
			data=pd.read_csv('1.csv')
			price=[]
			for i in data['Product_price']:
				try:
					price.append(int(i.split('\xa0')[1].replace(',','').split('.')[0]))
				except:
					price.append(0)
			rating=[]
			for i in data['rating']:
				try:
					rating.append(float(i.split(' ')[0]))
				except:
					rating.append(float(0))
			total_review=[]
			for i in data['total_review']:
				try:
					total_review.append(int(i.split(' ')[0].replace(',','')))
				except:
					total_review.append(0)
			ans_ask=[]
			for i in data['ans_ask']:
				try:
					ans_ask.append(int(i.split(' ')[0].replace('+','')))
				except:
					ans_ask.append(0)
			score=[]
			for i in range(len(data.Product_name)):
				if rating[i]>2.5:
					score.append(((rating[i] * total_review[i] + ans_ask[i]) / sum(total_review)) * 100)
				else:
					score.append(((rating[i] * total_review[i] - ans_ask[i]) / sum(total_review)) * 100)
			data['score']=score
			sorted=data.sort_values(by=['score'], ascending=False)
			return sorted

		f=open('1.csv','w')
		f.write('Product_name,by_info,Product_url,Product_img,Product_price,rating,total_review,ans_ask,prod_des,feature,cust_review\n')
		next=''
		#a=1
		while n>0:
			http=urllib3.PoolManager()
			response=http.request('GET',url)
			soup=BeautifulSoup(response.data, 'html.parser')
			for li in soup.findAll('li',{'class': 'a-last'}):
				next='https://www.amazon.in'+str(li.find('a').attrs['href'].strip())
			level1(url,soup)
			url=next
			n-=1
		f.close()
		sorted=result()
		sort_json = sorted.to_json()
		data=pd.read_csv('1.csv')
		str_io = io.StringIO()
		data.to_html(buf=str_io, classes='table table-striped')
		html_str = str_io.getvalue()
		sorted_io = io.StringIO()
		sorted.to_html(buf=sorted_io, classes='table table-striped')
		sorted_str = sorted_io.getvalue()
		return json.dumps(sort_json)

if __name__=="__main__":
	app.run(debug=True)
