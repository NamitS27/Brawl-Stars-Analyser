from get_data import *
from flask import Flask, redirect, url_for, request, render_template, jsonify
import psycopg2
import requests

def check_email(email):
    if requests.get("https://isitarealemail.com/api/email/validate",params = {'email':email}).json()['status']=="valid":
        return True 
    return False

app = Flask(__name__)

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImIwZjQ4MzRmLTBiMzctNGM0MS04MDRiLTIyN2RjZGUzMzhjYSIsImlhdCI6MTU4NzMwNTAwNCwic3ViIjoiZGV2ZWxvcGVyL2IwZDZiNDk4LTFlYWMtMTM1Ni1hMTllLTYwZTlmMzQ0YmY3NCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMjcuNjEuMTMyLjE5NSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.3oikvdNS0QfZEkIS1L7f1VWt4FQRQ01J-Y1AC-HCHqem8iHai_mQfVhbIGEmaytoZqXliH11bcNLC66T1L6JFQ'

global conn

try:
    conn = psycopg2.connect("dbname='dbms' user='postgres' host='localhost' password='postgres'")
except:
    print("ERROR :(")

cur = conn.cursor()

user = None

def fformat(p):
    l = []
    s = str(p[0])
    l.append(['Tag ',s])
    s = str(p[1])
    l.append(['Name ',s])
    s = str(p[2])
    l.append(['Name Color ',s])
    s = str(p[3])
    l.append(['Trophies ',s])
    s = str(p[4])
    l.append(['Highest Trophies ',s])
    s = str(p[5])
    l.append(['Experience Level ',s])
    s = str(p[6])
    l.append(['Experience Points ',s])
    s = str(p[7])
    l.append(['Championship Qualified ',s])
    s =str(p[8])
    l.append(['3 vs 3 Victories ',s])
    s=str(p[9])
    l.append(['Solo Victories ',s])
    s=str(p[10])
    l.append(['Duo Victories ',s])
    s=str(p[11])
    l.append(['Best Robo Rumble Time ',s])
    s=str(p[12])
    l.append(['Best Time as Big Brawler ',s])
    return l



@app.route('/login',methods=['POST','GET'])
def log():
    global user
    if request.method=='POST':
        user = request.form['name']
        pas = request.form['pass']
        pas = pas.strip()
        user = user.strip()
        kk = "SELECT tag FROM USERDATA WHERE emailid = '"+user+"' AND password = '"+pas+"';"
        cur.execute(kk)
        x = cur.fetchall()
        if len(x)>0:
            x = x[0][0]
            user = str(x)
            Utag = user
            run(token,Utag[1:])
            quer = "SELECT * FROM PROFILE WHERE tag = '"+Utag+"';"
            cur.execute(quer)
            x = cur.fetchall()
            li = fformat(list(x[0]))
            flag = check_club()      
            flag2 = check_battle() 
            return render_template('result.html',d = li,flag=flag,fla2=flag2)
        else:
            fla = 1             #1 for invalid login credentials
            print(fla)
            print('HEY')
            return render_template('animatelogin.html',flag=fla)

def check_club():
    quer = "SELECT * FROM CLUB_MEMBERS WHERE player_tag = '{}'".format(user)
    cur = conn.cursor()
    cur.execute(quer)
    xx = cur.fetchall()
    if len(xx)>0:
        return 1
    return 0

def check_battle():
    quer="SELECT * FROM BATTLE_DET WHERE tag = '{}'".format(user)
    cur = conn.cursor()
    cur.execute(quer)
    xx = cur.fetchall()
    if len(xx)==0:
        return 0
    else: 
        return 1    

@app.route('/signup',methods=['POST','GET'])
def signup():
    global user
    if request.method=='POST': 
        user = request.form['regname']
        email = request.form['regmail']
        pwd = request.form['regpass']
        repwd = request.form['reregpass']
        if pwd==repwd and check_email(email):
            qu = "INSERT INTO USERDATA values('"+email+"','"+user+"','"+pwd+"');"
            flag=0
            try:
                cur.execute(qu)
                conn.commit()
            except:
                flag = 2
            return render_template('animatelogin.html',flag=flag)
        else:
            return render_template('animatelogin.html',flag=2)    


@app.route('/battles',methods=['POST','GET'])
def battles_show():
    Utag = user
    query_check = "SELECT battle_time,event_mode,event_map,trophy_change FROM battle_det WHERE tag = '"+Utag+"' ORDER BY battle_time DESC LIMIT 25;"
    cur = conn.cursor()
    cur.execute(query_check)
    x = cur.fetchall() 
    fin = []
    if len(x)>0:
        for i in range(len(x)):
            tem = []
            quer = "SELECT * FROM battle_team WHERE tag = '{}' AND battle_time = '{}' ORDER BY battle_result;".format(Utag,x[i][0])
            cur = conn.cursor()
            cur.execute(quer)
            xx = cur.fetchall()
            if len(xx)>0:
                bt = 0                           #teambattle
                br = ' '
                st = -1                          #for star player 
                coun=0
                for j in xx:
                    if j[4]=='star':
                      st = coun   
                    if j[0]==j[6]:
                        br = j[2]
                    coun = coun+1
                tem.append(x[i][1])             #eventmode
                tem.append(x[i][2])             #event map
                tem.append(bt)                  #battletype  (team, solo, duo)
                tem.append(st)                  #starplayer index
                tem.append(br)                  #battle_rank        
                for j in xx:
                    tem.append(j[7])            #player_name
                    tem.append(j[9])            #name
                    tem.append(j[10])           #power
                    tem.append(j[11])           #trophies
                tem.append(x[i][3])             #trophy_change    
            else:
                quer = "SELECT * FROM battle_solo WHERE tag = '{}' AND battle_time = '{}' ORDER BY battle_rank;".format(Utag,x[i][0])
                cur = conn.cursor()
                cur.execute(quer)
                xx = cur.fetchall()
                if len(xx)>0:
                     bt = 1                     #soloshowdown
                     br = ' '
                     st = -1
                     for j in xx:   
                        if j[0]==j[3]:
                            br = str(j[2])
                     
                     tem.append(x[i][1])           #eventmode
                     tem.append(x[i][2])           #event map
                     tem.append(bt)                #battletype
                     tem.append(st)                #starplayer index
                     tem.append(br)                #battle_rank        
                     
                     for j in xx:
                        tem.append(j[4])           #player_name
                        tem.append(j[6])           #name
                        tem.append(j[7])           #power
                        tem.append(j[8])           #trophies
                     tem.append(x[i][3])           #trophy_change
                else:
                    quer = "SELECT * FROM battle_duo WHERE tag = '{}' AND battle_time = '{}' ORDER BY team_rank;".format(Utag,x[i][0])
                    cur = conn.cursor()
                    cur.execute(quer)
                    xx = cur.fetchall()
                    if len(xx)>0:
                        bt = 2                  #duoshowdown
                        br = ' '
                        st = -1
                        for j in xx:   
                            if j[0]==j[3]:
                                br = str(j[2])
                        
                        tem.append(x[i][1]) 
                        tem.append(x[i][2])             #event map
                        tem.append(bt)                  #battletype
                        tem.append(st)                  #starplayer index
                        tem.append(br)                  #battle_rank        
                        for j in xx:
                            tem.append(j[4])            #player_name
                            tem.append(j[6])            #name
                            tem.append(j[7])            #power
                            tem.append(j[8])            #trophies
                        tem.append(x[i][3])             #trophy_change    
            fin.append(tem)
        print(fin)    
        return render_template('battle.html',det = fin)


@app.route('/brawler',methods=['POST','GET'])
def testmet():
    query = "SELECT brawler_id,brawler_name,brawler_power,brawler_rank,brawler_trophies,brawler_highest_trophies,brawler_star_power_1_name,brawler_star_power_2_name from brawlers where tag = '{}'".format(user)
    cur.execute(query)
    l = cur.fetchall()
    avd_id,avg_sd = geta_avg_bd(user)
    return render_template('clash.html',dd=l,ind=avd_id,sd=avg_sd)


@app.route('/club',methods=['POST','GET'])
def club_det():
    quer1 = "SELECT club_tag from club_members where player_tag = '{}'".format(user)
    cur.execute(quer1)
    get_ct = cur.fetchall()
    get_ct = list(get_ct[0])
    query2 = "SELECT * from club where club_tag = '{}'".format(str(get_ct[0]))
    cur.execute(query2)
    club_det = cur.fetchall()
    cd = list(club_det[0])
    final_club = "SELECT * FROM club_members WHERE club_tag = '{}'".format(str(get_ct[0]))
    cur.execute(final_club)
    cmd = cur.fetchall()
    # plyer = client.get_player(user)
    # l,ll,tag, name, name_colour, role, trophies = club_detai(plyer)
    # number_of_players = len(ll)
    return render_template('club_details.html', det=cd, dd=cmd)

flag = None
tem = None
gen = None
flag2 = None
pla = None
pla2 = None
page_flag = None
page_flag2 = None
page_lis = None
page_gen = None
page_tem = None
page_genn = None
page_tem2 = None
page_tem3 = None
lis = None

@app.route('/analys',methods=['POST','GET'])
def page_analysis():
    x= ""
    y= -1
    global flag
    global flag2
    if request.method=='POST':
        x = request.form['team_data'] #value selected from Battle Mode dropdown list
        y = request.form['sd_data'] #Value selected from showdown typw dropdown list
        y = int(y)
    flag = get_team_map_analysis(tem,x) #Table1
    if y<3:
        flag2 = showdowni_map_analysis(user,y)    #Table2 for individual showdown
    else:
        flag2 = showdowna_map_analysis(user)        
    return jsonify(flag=flag,flag2=flag2)



@app.route('/anal',methods=['POST','GET'])
def new_analysis():
    x= ""
    y= ""
    z = -1
    w = ""
    print("hello world")
    global pla
    global pla2
    if request.method=='POST':
        x = request.form['team_data'] #value selected from Battle Mode dropdown list
        y = request.form['team_dataa'] #Value selected from brawler for battle mode dropdown list
        z = request.form['sd_data'] #value selected from showdown type dropdown list
        w = request.form['sd_dataa'] #Value selected from brawler showdown type dropdown list
        z = int(z)
        pla = get_brawler_map_team_analysis(page_tem,x,y) #Table1
        if z<3:
            pla2 = get_brawler_map_ind_showdown_analysis(page_tem3[z],w)    #Table2 for individual showdown
        else:
            pla2 = get_brawler_map_showdown_analysis(page_tem2,w)
    print(pla)
    print(pla2)                 
    # else:
    # # x = request.form.get('team_data')
    # x='oookoko'
    # # y = request.form.get('sd_data')
    # y = 'lmlmlkkkl'
    # lis = [['apple','banana','mokey'],['popey','dds','sadsad'],['dads','sdsad','asdsad','sdasad'],['sadsad','sada','sadsad','sadsa'],['asdsa','ssdad','sadsad']]
    # global flag
    # flag = [x,y]
    # flag.append(x)
    # flag.append(y)
    return jsonify(pla=pla,pla2=pla2)    


@app.route('/<string:table>')
def send(table):
    global flag
    global flag2
    print(flag)
    global lis
    global gen
    global tem
    global user
    temp = " "
    if table == 'no':
        # run(token,user)
        flag = None
        flag2 = None
        gen = overall_analysis(user)
        lis,tem = team_map_analysis(user)

    return render_template('analysis.html',flag=flag,lis=lis,flag2=flag2,gen=gen,temp=tem)


@app.route('/new_analysis/<string:table>')
def doit(table):
    global page_flag
    global page_flag2
    # print(flag)
    global page_lis
    global page_gen
    global page_tem
    global page_genn
    global page_tem2
    global page_tem3
    global user
    page_genn = []
    page_tem3 = []
    temp = " "
    # user = "#22G90CY9P"
    global pla
    global pla2
    # lis = ['gemgrab','brawlBall','Bounty','heist']
    # lis = [['apple','banana','mokey'],['popey','dds','sadsad'],['dads','sdsad','asdsad','sdasad'],['sadsad','sada','sadsad','sadsa'],['asdsa','ssdad','sadsad']]
    if table == 'no':
        # run(token,user)
        pla = None
        pla2 = None
        # temp = "helloworld"
        page_lis = brawler_analysis(user)
        page_gen,page_flag,page_tem = brawler_map_team_analysis(user)
        page_flag2,page_tem2 = brawler_map_showdown_analysis(user)
        te,tes = brawler_map_ind_showdown_analysis(user,1)
        te2,tes2 = brawler_map_ind_showdown_analysis(user,2)
        page_genn.append(te)
        page_genn.append(te2)
        page_tem3.append(tes)
        page_tem3.append(tes2)
    return render_template('new_analysis.html',flag=page_flag,lis=page_lis,flag2=page_flag2,gen=page_gen,temp=page_tem,tem2=page_tem2,genn=page_genn,tem3=page_tem3,pla=pla,pla2=pla2)



@app.route('/')
def start():
    return render_template('animatelogin.html',flag=0)


if __name__=='__main__':
    app.run(debug=True)        
