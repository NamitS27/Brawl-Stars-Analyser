from get_data import *
from flask import Flask, redirect, url_for, request, render_template
import psycopg2

app = Flask(__name__)

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImRjYzhlY2VhLWFlNzUtNDNlNy1iZGE3LTc5YmM5M2U5NWY1YSIsImlhdCI6MTU4NzE4OTMzNCwic3ViIjoiZGV2ZWxvcGVyL2IwZDZiNDk4LTFlYWMtMTM1Ni1hMTllLTYwZTlmMzQ0YmY3NCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTU3LjMyLjcyLjE2OCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.zY4fi0CRvAn_8sE7_R4Uy-VPglBjtVhLtE0IrNQ57tlul1N0yxBEBaAjaTYDToBzKRvvSiIW8P5NKhD5tWlysg'

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
        if pwd==repwd:
            qu = "INSERT INTO USERDATA values('"+email+"','"+user+"','"+pwd+"');"
            flag=0
            try:
                cur.execute(qu)
                conn.commit()
                return render_template('animatelogin.html',flag=flag)    
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
    return render_template('clash.html',dd=l)


@app.route('/club',methods=['POST','GET'])
def club_det():
    quer1 = "SELECT club_t"
    # plyer = client.get_player(user)
    # l,ll,tag, name, name_colour, role, trophies = club_detai(plyer)
    # number_of_players = len(ll)
    # return render_template('club_details.html', det=l, dd=ll, player_number=number_of_players, tag=tag, name=name, name_colour=name_colour, role=role, trophies=trophies)


@app.route('/')
def send():
    return render_template('animatelogin.html',flag=0)

if __name__=='__main__':
    app.run(debug=True)    
