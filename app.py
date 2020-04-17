from get_data import *
from flask import Flask, redirect, url_for, request, render_template

import brawlstats

app = Flask(__name__)
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImU4OGMwNzMxLWYyNmEtNGVmOC1iNWVkLTE3ZDA5OGJjMzU1MCIsImlhdCI6MTU4NDk2OTQ0OSwic3ViIjoiZGV2ZWxvcGVyLzhlZTEwM2Y3LWY2OTUtM2U1MC05MGI1LTk2OGIxOTY5NWZiOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTAzLjg1LjkuMjU1Il0sInR5cGUiOiJjbGllbnQifV19.KC2p075pfN3tJthbbXf7cBxdi-7-Ipap9gwY0rWVV5_HlszR0BwkqdPSuSqeQvngdkkvq-y5LAkCPu3yIoQN1g'
import psycopg2
global conn

try:
    conn = psycopg2.connect("dbname='dbms' user='postgres' host='localhost' password='1288'")
except:
    print("ERROR :(")


client = brawlstats.OfficialAPI(token)
# battles = client.get_battle_logs('2LJYR2UU')




# def gt(timee):
    # return datetime.strptime(timee[:4]+"-"+timee[4:6]+"-"+timee[6:8]+" "+timee[9:11]+":"+timee[11:13]+":"+timee[13:15],"%Y-%m-%d %H:%M:%S")

# def insert_bat_det(blog,tag):
#     query = "SELECT battle_time FROM battle_det WHERE tag = '#"+tag+"' ORDER BY battle_time desc FETCH FIRST ROW ONLY"
#     cur = conn.cursor()
#     cur.execute(query)
#     x = cur.fetchall()
#     cnt = 0
#     #print(x)
#     if(len(x)>0):
#         last_bt = datetime.strptime(str(x[0][0]),"%Y-%m-%d %H:%M:%S")
#         for i in range(25):
#             if(gt(blog[i].battle_time)<=last_bt):
#                 break
#             cnt = cnt+1
#     else:
#         cnt = 25
#     return cnt



# def bat_log(battle_l,tag):
#      li=[]
#      bat_li=[]
#      details = list(parse(battle_l))
#      log_b = []
#      log_b.append(details[0][1]) # TIME
#      log_b.append(details[1][2]) # ID
#      log_b.append(details[2][2]) # EVENT MODE
#      log_b.append(details[3][2]) # EVENT MAP
#      log_b.append(details[4][2]) # BATTLE MODE
#     #  qq = "INSERT INTO battle_det VALUES('{}','{}',{},'{}','{}'".format(tag,time_extract(log_b[0]),log_b[1],log_b[2],log_b[3])
#     #  r = "INSERT INTO battle_det VALUES('"
#     #  q = "','"+time_extract(log_b[0])+"',"+str(log_b[1])+",'"+log_b[2]+"','"+log_b[3]+"',"
#     #  p = ",'"+log_b[4]+"')"
#      if details[4][2]=='soloShowdown' or details[4][2]=='duoShowdown':
#         print("----------------------------------------------------------------------------------------")
#         print("DATE : "+time_extract(log_b[0]))
#         li.append("DATE : "+time_extract(log_b[0]))
#         print("----------------------------------------------------------------------------------------")
#         li.append("Event ID : "+str(log_b[1])+"     | Event Mode : "+log_b[2]+"     | Event Map : "+log_b[3])
#         print("Event ID : "+str(log_b[1])+"     | Event Mode : "+log_b[2]+"     | Event Map : "+log_b[3])
#         print("Battle Mode : "+log_b[4])
#         li.append("Battle Mode : "+log_b[4])
#         print("----------------------------------------------------------------------------------------")
#         temp_det = []
#         temp_det.append(details[5][2]) # Type
#         temp_det.append(details[6][2]) # Rank
#         j = 0
#         if details[7][1]=='trophy_change':
#             temp_det.append(details[7][2]) # Trophy Change
#         else:
#             temp_det.append(0)
#             j = 1
#         li.append("Type : "+temp_det[0]+"     | Rank : "+str(temp_det[1])+"    | Trophy Change : "+str(temp_det[2]))
#         query = "INSERT INTO battle_det VALUES('{}','{}',{},'{}','{}','{}',{},'{}')".format(tag,time_extract(log_b[0]),log_b[1],log_b[2],log_b[3],temp_det[0],temp_det[2],log_b[4])
#         cur.execute(query)
#         conn.commit()
#         if details[4][2]=='soloShowdown':
#             bat_li.append(solo_show_down_parse(j,tag,time_extract(log_b[0]),details))
#         else:
#             bat_li.append(duo_show_down_parse(j,tag,time_extract(log_b[0]),details))
#      elif details[4][2]=='bigGame' or details[4][2]=='roboRumble' or details[4][2]=='bossFight' or details[4][2]=='takedown':
#         # log_b.append(details[5][2]) #Battle Duration
#         # print("----------------------------------------------------------------------------------------")
#         # print("DATE : "+time_extract(log_b[0]))
#         # print("----------------------------------------------------------------------------------------")
#         # print("Event ID : "+str(log_b[1])+"     | Event Mode : "+log_b[2]+"     | Event Map : "+log_b[3])
#         # print("Battle Mode : "+log_b[4]+"   | Battle Duration : "+str(convert(log_b[5])))
#         # print("----------------------------------------------------------------------------------------")
#         # bs = []
#         # for x in range(len(details[6][2])): 
#         #    temp = []
#         #    temp.append(details[6][2][x].tag)
#         #    temp.append(details[6][2][x].name)
#         #    temp.append(str(details[6][2][x].brawler.id))
#         #    temp.append(details[6][2][x].brawler.name)
#         #    temp.append(str(details[6][2][x].brawler.power))
#         #    temp.append(str(details[6][2][x].brawler.trophies))
#         #    bs.append(temp)
#         # bbtag = details[7][2]
#         # bbn = details[8][2]
#         # bbbi = str(details[9][3])
#         # bbbn = details[10][3]
#         # bbbp = str(details[11][3])
#         # bbbt = str(details[12][2])
#         print('NO')
#      else:
#         log_b.append(details[5][2]) # BATTLE TYPE
#         log_b.append(details[6][2]) # BATTLE RESULT
#         log_b.append(details[7][2]) # BATTLE DURATION
#         i = 0
#         if details[8][1]=='trophy_change':
#             log_b.append(details[8][2]) # TROPHY CHANGE
#         else:
#             i=1
#             log_b.append(0)
#         #query = q+"'"+log_b[5]+"',"+log_b[8]+p
#         log_b.append(details[9-i][3]) # STAR PLAYER TAG
#         l1,l2 = form_vic_def_list(battle_l)
#         new_l1 = get_victory_defeat__list(l1)
#         new_l2 = get_victory_defeat__list(l2)
#         li,bat_li=pint_log(tag,log_b,new_l1,new_l2)
#     return li,bat_li    



# def duo_show_down_parse(j,tag,time,det):
#     # cur.execute(qu)
#     lisl=[]
#     # x = cur.fetchall()
#     # row = list(x[0])
#     # hash_val = int(row[0])
#     # qudate = "UPDATE hash_values SET hash_value = '"+str(hash_val+1)+"' WHERE hash_value = '"+row[0]+"'" 
#     # cur.execute(qudate)
#     # conn.commit()
#     for i in range(len(det[8-j][2])):
#         print("----------------------------------------------------------------------------------------")
#         lisl.append("TEAM "+str(i+1))
#         for k in range(2):
#             print("----------------------------------------------------------------------------------------")
#             lisl.append("Tag : "+det[8-j][2][i][k].tag)
#             lisl.append("Name : "+det[8-j][2][i][k].name)
#             lisl.append("Brawler ID : "+str(det[8-j][2][i][k].brawler.id))
#             lisl.append("Brawler Name : "+det[8-j][2][i][k].brawler.name)
#             lisl.append("Brawler Name : "+str(det[8-j][2][i][k].brawler.power))
#             lisl.append("Brawler Trophies : "+str(det[8-j][2][i][k].brawler.trophies))
#             lisl.append("----------------------------------------------------------------------------------------")
#             query = "INSERT INTO battle_duo VALUES('"+str(tag)+"','"+time+"',"+str(i+1)+",'"+det[8-j][2][i][k].tag+"','"+det[8-j][2][i][k].name.replace("'","''")+"',"+str(det[8-j][2][i][k].brawler.id)+",'"+det[8-j][2][i][k].brawler.name+"',"+str(det[8-j][2][i][k].brawler.power)+","+str(det[8-j][2][i][k].brawler.trophies)+")"
#             cur.execute(query)
#             conn.commit()
#     return lisl        


# def solo_show_down_parse(j,tag,time,det):
#     lisl=[]
#     lisl.append("Players : "+str(len(det[8-j][2])))
#     # qu = "SELECT hash_value FROM hash_values"
#     # cur.execute(qu)
#     # x = cur.fetchall()
#     # row = list(x[0])
#     # hash_val = int(row[0])
#     # qudate = "UPDATE hash_values SET hash_value = '"+str(hash_val+1)+"' WHERE hash_value = '"+row[0]+"'" 
#     # cur.execute(qudate)
#     # conn.commit()
#     for i in range(len(det[8-j][2])):
#         print("----------------------------------------------------------------------------------------")
#         lisl.append("Tag : "+det[8-j][2][i].tag)
#         lisl.append("Name : "+det[8-j][2][i].name)
#         lisl.append("Brawler ID : "+str(det[8-j][2][i].brawler.id))
#         lisl.append("Brawler Name : "+det[8-j][2][i].brawler.name)
#         lisl.append"Brawler Power : "+str(det[8-j][2][i].brawler.power))
#         lisl.append("Brawler Trophies : "+str(det[8-j][2][i].brawler.trophies))
#         lisl.append("----------------------------------------------------------------------------------------")
#         # query2 = ins+det[8-j][2][i].tag+btd+"'"+temp_det[0]+"',"+str(get_br_trophies(det[8-j][2][i].tag[1:],det[8-j][2][i].brawler.name)-det[8-j][2][i].brawler.trophies)+bm
#         query = "INSERT INTO battle_solo VALUES('"+tag+"','"+time+"',"+str(i+1)+",'"+det[8-j][2][i].tag+"','"+det[8-j][2][i].name.replace("'","''")+"',"+str(det[8-j][2][i].brawler.id)+",'"+det[8-j][2][i].brawler.name+"',"+str(det[8-j][2][i].brawler.power)+","+str(det[8-j][2][i].brawler.trophies)+")"
#         # cur.execute(query2)
#         # conn.commit()
#         cur.execute(query)
#         conn.commit()
#     return lisl    


# def pint_teams(tag,duration,time,result,team,bteam,stag):
#     # if(check_tag):
#     lis=[]
#     print("----------------------------------------------------------------------------------------")
#     lis.append("TEAM {}: ".format(team))
#     print("----------------------------------------------------------------------------------------")
#     for i in range(3):
#         flag = True
#         if(bteam[i][0]==stag):
#             lis.append("STAR PLAYER")
#         else:
#             flag = False
#             lis.append("PLAYER")
#         # print("TAG : "+bteam[i][0])
#         # print("Name : "+bteam[i][1])
#         # print("Brawler ID : "+str(bteam[i][2]))
#         # print("Brawler Name : "+bteam[i][3])
#         # print("Brawler Power : "+str(bteam[i][4]))
#         # print("Brawler Trophies : "+str(bteam[i][5]))
#         #limit_content(len(bteam[i]),bteam[i],flag,vic_flag)
#         teem = bteam[i].copy()
#         max_range = len(bteam[i])
#         det = ['TAG','Name','Brawler ID','Brawler Name','Brawler Power','Brawler Trophies']
#         # s = ""
#         for i in range(max_range):
#             lis.append(det[i]+' : '+str(teem[i]))
#         if(max_range!=6):
#             for i in range(6 - max_range):
#                 teem.append('null')
#         s = None
#         if not flag:
#             s = "INSERT INTO battle_team VALUES('{}','{}','{}','{}','normal',{},'{}','{}',{},'{}',{},{})".format(tag,time,result,duration,team,teem[0],teem[1].replace("'","''"),teem[2],teem[3],teem[4],teem[5])
#         else:
#             s = "INSERT INTO battle_team VALUES('{}','{}','{}','{}','star',{},'{}','{}',{},'{}',{},{})".format(tag,time,result,duration,team,teem[0],teem[1].replace("'","''"),teem[2],teem[3],teem[4],teem[5])
#         cur.execute(s)
#         conn.commit()
#         lis.append(" ")
#         lis.append(" ")
#     return lis

# def pint_log(tag,detls,vic,deft):
#     li=[]
#     lisl=[]
#     print("----------------------------------------------------------------------------------------")
#     li.append("DATE : "+time_extract(detls[0]))
#     print("----------------------------------------------------------------------------------------")
#     li.append("Event ID : "+str(detls[1])+"     | Event Mode : "+detls[2]+"     | Event Map : "+detls[3])
#     li.append("Battle Mode : "+detls[4]+"    | Battle Type : "+detls[5])
#     print("----------------------------------------------------------------------------------------")
#     li.append(detls[6].upper()+"        | Battle Duration : "+str(convert(detls[7]))+"      | Trophy Change : "+str(detls[8]))
#     li.append("----------------------------------------------------------------------------------------")
#     star_ply_tg = detls[9]
#     # qu = "SELECT hash_value FROM hash_values"
#     # cur.execute(qu)
#     # x = cur.fetchall()
#     # row = list(x[0])
#     # hash_val = int(row[0])
#     # qudate = "UPDATE hash_values SET hash_value = '"+str(hash_val+1)+"' WHERE hash_value = '"+row[0]+"'" 
#     # cur.execute(qudate)
#     # conn.commit()
#     query = "INSERT INTO battle_det VALUES('{}','{}',{},'{}','{}','{}',{},'{}')".format(tag,time_extract(detls[0]),detls[1],detls[2],detls[3],detls[5],detls[8],detls[4])
#     cur.execute(query)
#     conn.commit()
#     vic_flag = True
#     for i in range(3):
#         if(vic[i][0]==star_ply_tg):
#             vic_flag = False
#             break
#     if detls[6].upper()!='DRAW':
#         if not vic_flag:
#             lisl.append(pint_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'VICTORY',1,vic,star_ply_tg))
#             lisl.append(pint_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DEFEAT',2,deft,star_ply_tg))
#         else:
#             lisl.append(pint_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DEFEAT',1,vic,star_ply_tg))
#             lisl.append(pint_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'VICTORY',2,deft,star_ply_tg))
#     else:
#         lisl.append(pint_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DRAW',1,vic,star_ply_tg))
#         lisl.append(pint_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DRAW',2,deft,star_ply_tg))
#     return li,lisl    


def club_detai(play):
    l = []
    club = play.get_club()
    print(club)
    l.append("CLUB TAG : "+club.tag)
    l.append("CLUB NAME : "+club.name)
    l.append("CLUB TROPHIES : "+str(club.trophies))
    l.append("CLUB TYPE : "+club.type)
    l.append("CLUB RTRP : "+str(club.required_trophies))
    l.append("CLUB DESC : "+club.description)
    mem = club.get_members()
    ll =[]
    tag=[]
    name=[]
    name_colour=[]
    role=[]
    trophies=[]
    for pla in mem:
        ll.append(get_club_plyer_det(pla))
        tag.append(get_tag(pla))
        name.append(get_name((pla)))
        name_colour.append(get_name_colour(pla))
        role.append(get_role(pla))
        trophies.append(get_trophies(pla))
    return l, ll, tag, name, name_colour, role, trophies


def get_club_plyer_det(player_det):
    tag = []
    name =[]
    name_colour = []
    role = []
    trophies = []
    l = []
    l.append("---------------------------------------------------------------------")
    l.append("Tag : "+player_det.tag)
    tag.append(player_det.tag)
    l.append("Name : "+player_det.name)
    name.append(player_det.name)
    l.append("Name Color : "+player_det.name_color)
    name_colour.append(player_det.name_color)
    l.append("Role : "+player_det.role)
    role.append(player_det.role)
    l.append("Trophies : "+str(player_det.trophies))
    trophies.append(player_det.trophies)
    l.append("---------------------------------------------------------------------")
    return l


def get_tag(player_det):
    tag = []
    tag.append(player_det.tag)
    return tag


def get_name(player_det):
    name = []
    name.append(player_det.name)
    return name


def get_name_colour(player_det):
    name_colour = []
    name_colour.append(player_det.name_color)
    return name_colour


def get_role(player_det):
    role = []
    role.append(player_det.role)
    return role


def get_trophies(player_det):
    trophies = []
    trophies.append(player_det.trophies)
    return trophies


def get_prof(prof_list):
    l = []
    # ll = []
    # s = "---------------------------------------------------------------------"
    # # l.append(s)
    # s = "PLAYER PROFILE "
    # # l.append(s)
    # s = "---------------------------------------------------------------------"
    # # l.append(s)
    s = prof_list.tag
    l.append(['Tag ',s])
    s = prof_list.name
    l.append(["Name ",s])
    s = str(prof_list.name_color)
    l.append(['Name Color ',s])
    s = str(prof_list.trophies)
    l.append(['Trophies',s])
    s = str(prof_list.highest_trophies)
    l.append(['Highest Trophies',s])
    s = str(prof_list.exp_level)
    l.append(['Experience Level',s])
    s = str(prof_list.exp_points)
    l.append(['Expereince Points',s])
    s = str(prof_list.is_qualified_from_championship_challenge)
    l.append(['CC Q',s])
    s =str(prof_list.x3vs3_victories)
    l.append(['3vs3 Victories',s])
    s=str(prof_list.solo_victories)
    l.append(['Solo Victories',s])
    s=str(prof_list.duo_victories)
    l.append(['Duo Victories',s])
    s=str(convert(prof_list.best_robo_rumble_time))
    l.append(['Best Robo Rumble Time',s])
    s=str(convert(prof_list.best_time_as_big_brawler))
    l.append(['Best Time as Big Brawler',s])
    return l


def get_profile(prof_list):
    query_check = "SELECT * FROM PROFILE WHERE tag = '"+prof_list.tag+"';"
    cur = conn.cursor()
    cur.execute(query_check)
    x = cur.fetchall()
    query = ""
    if(len(x)>0):
        query = "UPDATE PROFILE SET tag = '"+prof_list.tag+"',name = '"+prof_list.name+"',name_color = '"+str(prof_list.name_color)+"',trophies = "+str(prof_list.trophies)+",highest_trophies = "+str(prof_list.highest_trophies)+",exp_level = "+str(prof_list.exp_level)+",exp_points = "+str(prof_list.exp_points)+",champ_q = '"+str(prof_list.is_qualified_from_championship_challenge)+"',tvt_vict = "+str(prof_list.x3vs3_victories)+",solo_vict = "+str(prof_list.solo_victories)+",duo_vict = "+str(prof_list.duo_victories)+",rrt = '"+str(convert(prof_list.best_robo_rumble_time))+"',bbt = '"+str(convert(prof_list.best_time_as_big_brawler))+"' WHERE tag = '"+prof_list.tag+"'" 
    else:
        query = "INSERT INTO PROFILE VALUES('"+prof_list.tag+"','"+prof_list.name+"','"+str(prof_list.name_color)+"',"+str(prof_list.trophies)+","+str(prof_list.highest_trophies)+","+str(prof_list.exp_level)+","+str(prof_list.exp_points)+",'"+str(prof_list.is_qualified_from_championship_challenge)+"',"+str(prof_list.x3vs3_victories)+","+str(prof_list.solo_victories)+","+str(prof_list.duo_victories)+",'"+str(convert(prof_list.best_robo_rumble_time))+"','"+str(convert(prof_list.best_time_as_big_brawler))+"');"
    cur.execute(query)
    conn.commit()
    cur.execute(query_check)
    x = cur.fetchall()
    p = list(x[0])
    # print(p)
    for i in p:
        print(type(i))
    l = []
    # s = "---------------------------------------------------------------------"
    # l.append(s)
    # s = "PLAYER PROFILE "
    # l.append(s)
    # s = "---------------------------------------------------------------------"
    # l.append(s)
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
    l.append(['CC Q ',s])
    s =str(p[8])
    l.append(['3vs3 Victories ',s])
    s=str(p[9])
    l.append(['Solo Victories ',s])
    s=str(p[10])
    l.append(['Duo Victories ',s])
    s=str(p[11])
    l.append(['Best Robo Rumble Time ',s])
    s=str(p[12])
    l.append(['Best Time as Big Brawler ',s])
    return l


def ind_brawlers(lets_brawl,tag):
    l = []
    l1 = []
    l1.append("---------------------------------------------------------------------")
    l1.append("BRAWLER LIST : "+str(len(lets_brawl))+" BRAWLERS")
    l1.append("---------------------------------------------------------------------")
    for i in lets_brawl:
        l.append(brawler_details(list(parse(i)),tag))
    return l1,l    


def brawler_details(brawl_list,tag):
    list_tp = []
    ll = []
    # print(brawl_list)
    # flag = True
    # query_check = "SELECT * FROM PROFILE WHERE tag = '"+prof_list.tag+"';"
    # cur = conn.cursor()
    # cur.execute(query_check)
    # x = cur.fetchall()
    # if(len(x)>0) :
    #     flag = False
    for i in brawl_list:
        list_tp.append(i[1])
    # ll.append("---------------------------------------------------------------------")
    ll.append(str(list_tp[0])) #ID
    ll.append(list_tp[1]) #BrawlerName
    ll.append(str(list_tp[2])) #Power
    ll.append(str(list_tp[3])) #Rank
    ll.append(str(list_tp[4])) #Trophies
    ll.append(str(list_tp[5])) #Highest Trophies
    x = list(list_tp[6])
    star_list = []
    temp_str = ""
    temp_ste = "" 
    cntr = 0
    for y in x:
        cntr = cntr + 1
        star_list.append(y.id)
        temp_str += ","+str(y.id)+","
        temp_ste += ",star_power_{}_id = ".format(cntr)+str(y.id)+","
        star_list.append(y.name)
        temp_str += "'"+y.name+"'"
        temp_ste += ",star_power_{}_name = '".format(cntr)+"'"
    ll.append(star_list) #starpower
    # ll.append("---------------------------------------------------------------------")
    return ll

user = None

# plyer = brawlstats.officialapi.models.Player() 

@app.route('/login',methods=['POST','GET'])
def log():
    global user
    # print('helloworld')
    if request.method=='POST':
        user = request.form['name']
        pas = request.form['pass']
        pas = pas.strip()
        user = user.strip()
        # Utag = "#{}".format(user)
        # qu = "SELECT tag from USERDATA where emailid = '"+user+"' and password = '"+pas+"';"
        kk = "SELECT tag FROM USERDATA WHERE emailid = '"+user+"' AND password = '"+pas+"';"
        cur = conn.cursor()
        cur.execute(kk)
        x = cur.fetchall()
        print(x,' is the value of x')
        fla = x
        print(fla)
        print('HEY')
        return render_template('file.html', flag=fla)
        # if len(x)>0:
        #     x = x[0][0]
        #     user = str(x)
        #     print(user)
        #     plyer = client.get_player(user)
        #     print(type(plyer))
        #     print(user)
        #     li = get_profile(plyer)
        #     zzz = plyer.get_club()
        #     flag=0
        #     if zzz is not None:
        #         flag=1
        #     return render_template('result.html',d = li,flag=flag)
        # else:
        #     fla = x
        #     print(fla)
        #     print('HEY')
        #     return render_template('login.html',flag=fla)

@app.route('/signup',methods=['POST','GET'])
def signup():
    global user
    if request.method=='POST':
        user = request.form['regname']
        email = request.form['regmail']
        pwd = request.form['regpass']
        repwd = request.form['reregpass']
        Utag = "#{}".format(user)
        if pwd==repwd:
            qu = "INSERT INTO USERDATA values('"+email+"','"+Utag+"','"+pwd+"');"
            cur = conn.cursor()
            cur.execute(qu)
            conn.commit()
            plyer = client.get_player(user)
            print(type(plyer))
            print(user)
            li = get_profile(plyer)
            zzz = plyer.get_club()
            flag=0
            if zzz is not None:
                flag=1
            return render_template('result.html',d = li,flag = flag)
        else:
            return render_template('login.html',flag=2)    


@app.route('/home', methods=['POST','GET'])
def home():
    global user
    # global plyer
    if request.method=='POST':
        user = request.form['ptag']
        plyer = client.get_player(user)
        print(type(plyer))
        print(user)
        li = get_profile(plyer)
        zzz = plyer.get_club()
        flag=0
        if zzz is not None:
            flag=1
        # with open('player_info.csv','w') as write_obj:
        #     csv_writer = writer(write_obj)
        #     csv_writer.writerows(li)
        # data = pd.read_csv('player_info.csv')
        # data.index.name = None
        return render_template('result.html',d = li,flag=flag)
    # return render_template('test.html',tables=[data.to_html(classes='data')],titles=['Table Title'])
    print(request.args)
    # global user
    user = request.args.get('ptag')
    plyer = client.get_player(user)
    print(type(user))
    li = get_profile(plyer)
    # with open('player_info.csv','w') as write_obj:
    #     csv_writer = writer(write_obj)
    #     csv_writer.writerows(li)
    # data = pd.read_csv('player_info.csv')
    # data.index.name = None
    return render_template('result.html',d = li)             



@app.route('/battles',methods=['POST','GET'])
def battles_show():
    # if request.method=='GET':
    # global user
    plyer = client.get_player(user)
    battles = client.get_battle_logs(user)
    Utag = "#{}".format(user)
    count = insert_battle_det(battles,user)
    print(count)
    for i in range(count):
        print("BATTLE NUMBER : "+str(i+1))
        battle_log(battles[i],Utag)
    query_check = "SELECT battle_time,event_mode,event_map FROM battle_det WHERE tag = '"+Utag+"' ORDER BY battle_time DESC LIMIT 25;"
    cur = conn.cursor()
    cur.execute(query_check)
    x = cur.fetchall()
    print('yaha tak sab sahi hai ')    
        # x = parse_ind_brawlers(plyer.brawlers,plyer.tag)
        # print('ok',user,'User')
    fin = []
    if len(x)>0:
        for i in range(0,len(x)):
            # qq = "SELECT TO_CHAR( TIMESTAMP '','HH24:MI:SS');"
            tem = []
            quer = "SELECT * FROM battle_team WHERE tag = '{}' AND battle_time = '{}' ORDER BY battle_result;".format(Utag,x[i][0])
            cur = conn.cursor()
            cur.execute(quer)
            xx = cur.fetchall()
            if len(xx)>0:
                bt = 0 #teambattle
                br = ' '
                st = -1
                coun=0
                for j in xx:
                    if j[4]=='star':
                      st = coun   
                    if j[0]==j[6]:
                        br = j[2]
                    coun = coun+1
                tem.append(x[i][1]) #eventmode
                tem.append(x[i][2]) #event map
                tem.append(bt)   #battletype
                tem.append(st)   #starplayer index
                tem.append(br)   #battle_rank        
                for j in xx:
                    tem.append(j[7])#player_name
                    tem.append(j[9])#name
                    tem.append(j[10])#power
                    tem.append(j[11])#trophies
            
            else:
                quer = "SELECT * FROM battle_solo WHERE tag = '{}' AND battle_time = '{}' ORDER BY battle_rank;".format(Utag,x[i][0])
                cur = conn.cursor()
                cur.execute(quer)
                xx = cur.fetchall()
                if len(xx)>0:
                     bt = 1 #soloshowdown
                     br = ' '
                     st = -1
                     for j in xx:   
                        if j[0]==j[3]:
                            br = str(j[2])
                     
                     tem.append(x[i][1]) #eventmode
                     tem.append(x[i][2])#event map
                     tem.append(bt)#battletype
                     tem.append(st) #starplayer index
                     tem.append(br) #battle_rank        
                     
                     for j in xx:
                        tem.append(j[4])#player_name
                        tem.append(j[6])#name
                        tem.append(j[7])#power
                        tem.append(j[8])#trophies
                
                else:
                    quer = "SELECT * FROM battle_duo WHERE tag = '{}' AND battle_time = '{}' ORDER BY team_rank;".format(Utag,x[i][0])
                    cur = conn.cursor()
                    cur.execute(quer)
                    xx = cur.fetchall()
                    if len(xx)>0:
                        bt = 2 #duoshowdown
                        br = ' '
                        st = -1
                        for j in xx:   
                            if j[0]==j[3]:
                                br = str(j[2])
                        
                        tem.append(x[i][1]) 
                        tem.append(x[i][2])#event map
                        tem.append(bt)#battletype
                        tem.append(st) #starplayer index
                        tem.append(br) #battle_rank        
                        for j in xx:
                            tem.append(j[4])#player_name
                            tem.append(j[6])#name
                            tem.append(j[7])#power
                            tem.append(j[8])#trophies
            
            fin.append(tem)
        print(fin)    
        return render_template('battles.html',det = fin)


@app.route('/brawler',methods=['POST','GET'])
def testmet():
    # if request.method=='GET':
    # global user
    plyer = client.get_player(user)
    l1,l = ind_brawlers(plyer.brawlers,user)
        # x = parse_ind_brawlers(plyer.brawlers,plyer.tag)
        # print('ok',user,'User')
    return render_template('clash.html',det = l1, dd=l)


@app.route('/club',methods=['POST','GET'])
def club_det():
    # if request.method=='GET':
    # global user
    print(user)
    plyer = client.get_player(user)
    l,ll,tag, name, name_colour, role, trophies = club_detai(plyer)
    number_of_players = len(ll)
    return render_template('club_details.html', det=l, dd=ll, player_number=number_of_players, tag=tag, name=name, name_colour=name_colour, role=role, trophies=trophies)


@app.route('/')
def send():
    return render_template('animatelogin.html',flag=0)

if __name__=='__main__':
    app.run(debug=True)    
