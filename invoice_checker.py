from pyzbar.pyzbar import decode#偵測和解碼qrcode
from PIL import Image#讀取圖片所需的函式庫
from os import walk,path#將查詢資料夾內所有檔案所需要的函式庫
from re import match#正規表示式的函式庫
from requests import get#抓取網頁原始碼的函式庫
from bs4 import BeautifulSoup#分析網頁的函式庫
for tops, dirs, files in walk('qrcode'):#查詢資料夾內所有檔案
    for f in files:#將檔案一個一個弄出來
        print(f)#顯示檔案名稱
        for invoice in decode(Image.open(path.join(tops,f))):#查詢圖片內所有的qrcode，並且一個一個列出來
            invoice_num_and_month = match('^[A-Z]{2}[0-9]{13}',invoice.data.decode())#使用正規表示式找出發票號碼的qrcode，排除購物明細的qrcode，取得發票號碼及月份
            if(invoice_num_and_month):#如果找到的是有發票號碼的qrcode(沒有發票號碼的結果是NULL)
                invoice_num = invoice_num_and_month.group()[2:10]#去除前兩個英文字母，得到純數字的發票號碼
                invoice_month = int(invoice_num_and_month.group()[10:15])#取得發票月份
                print(invoice_num,invoice_month)
                if(invoice_month % 2 == 0):#因為兩個月開一次獎，所以偶數月和奇數月的中獎號碼是一樣的
                    invoice_month -= 1
                html_source_code = get("https://www.etax.nat.gov.tw/etw-main/web/ETW183W2_"+ str(invoice_month) +"/")#根據發票月份抓取中獎號碼的網頁原始碼
                html_numbers = BeautifulSoup(html_source_code.text,"html.parser").select(".number")#分析網頁原始碼獲得中獎號碼
                if(not html_numbers):
                    print("尚未開獎")
                    continue
                txt = ""#存放中獎號碼
                for number in html_numbers:#去除不需要的部分，取出中獎號碼
                   txt += number.text
                txt = txt.replace("ã\x80\x81"," ")#去除頓號換成空格
                txt = txt.replace("b","").replace("'","").replace("   ","\n").replace("  ","\n").replace(" ","\n")#去除轉換產生的b和'，並且把空格換成\n
                with open(str(invoice_month) + ".txt", "w") as f:#將中獎號碼寫入檔案
                    f.write(txt)
                                        
                with open(str(invoice_month) + ".txt", "r") as f:#讀取存放中獎號碼的檔案
                    txt_data = f.read()#將檔案資料放到記憶體中
                    start = 0#中獎號碼的開頭
                    end = 0#中獎號碼的結尾
                    winning_num = []#中獎號碼
                    while(1 == 1):
                        start = end
                        end = txt_data.find('\n',start + 1)#因為每一筆中獎號碼都是用\n分開的，所以要找\n和\n中間的內容
                        if(end == -1):#如果找不到\n會出現-1
                            break
                        winning_num.append(txt_data[start:end].replace('\n',''))#將中獎號碼儲存
                    for num in winning_num:#比對中獎號碼
                        if(len(num) > 3):#只取後三碼
                            num = num[len(num)-3:len(num)]
                        if(invoice_num[5:8] == num):#比對後三碼
                            print(invoice_num,"有中獎的機會")
