# path = directory + file_name
import requests,os
def crawler_index(start,end,board):
    directory = "./log/"+board+"/index/"
    file_name = []
    for i in range(start,end):
        website = "/bbs/"+board+"/index" +str(i) +".html"
        payload = {"from": website , "yes": "yes"}
        res = requests.post("https://www.ptt.cc/ask/over18", data=payload)
        res.encoding = 'utf8' 
        temp = "index"+ str(i) #I dont like it. 
        f  = file_handle(directory,temp,"w")
        file_name.append(temp)
        f.write(res.text)
        f.closed
    
    return directory,file_name

def crawler_content(content_link,board): #path should rename content_link
    common_content_link = "/bbs/"+ board +"/"
    payload = {"from": content_link , "yes": "yes"}
    res = requests.post("https://www.ptt.cc/ask/over18", data=payload)
    res.encoding = 'utf8' 
    f  = file_handle("./log/" + board +"/content/", content_link.strip(common_content_link),"w")
    f.write(res.text)
    f.closed

def file_handle(directory,file_name,do): #when path not exist,can dir path
    try:
        f = open(directory+file_name,do)
    except:
        os.makedirs(directory)
        f = open(directory+file_name,do)
    return f

def analysis_index(directory,file_name): #analysis index file to get content link
    path = directory + file_name
    content_link = []
    identify_start = '<a href="'
    identify_end   = '">'
    link_end = 0
    f = open(path,"r")
    index_file = f.read()  
    exception = False
    while exception != True:
        try:
            link_start  = index_file.index(identify_start,link_end) 
            link_start = link_start + len(identify_start)
            link_end = index_file.index(identify_end,link_start)
            temp = index_file[link_start:link_end]
            content_link.append(temp)
        except:
            exception = True
    return content_link 

def start_crawler(start,end,board):
    directory,file_name = crawler_index(start,end,board)
    for now_file_name in file_name:
        content_link = analysis_index(directory,now_file_name)
        for now_content_link in content_link:
            crawler_content(now_content_link,board)
    
    print("crawler finish!!")

board = "Gossiping"
start_crawler(1,3,board)
