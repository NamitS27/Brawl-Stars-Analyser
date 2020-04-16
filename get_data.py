import brawlstats
import sys
from pprint import pprint
import psycopg2
from datetime import datetime

global conn 

# try:
conn = psycopg2.connect("dbname='dbms' user='postgres' host='localhost' password='postgres'")
# except:
    # print("ERROR :(")

cur = conn.cursor()

stdoutOrigin=sys.stdout 
sys.stdout = open("log.txt", "w",encoding="utf-8")

def parse(dic):
    for k, v in dic.items():
        if isinstance(v, dict):
            for p in parse(v):
                yield [k] + p
        else:
            yield [k, v]

def get_victory_defeat__list(vic_dict):
    v_list = []
    for j in range(3):
        tp_list = []
        for i in range(2):
            tp_list.append(vic_dict[j][i][1])
        for i in range(2,len(vic_dict[j])):
            tp_list.append(vic_dict[j][i][2])
        v_list.append(tp_list)
    return v_list

def form_vic_def_list(battle_l):
    battle_log = battle_l.battle.teams[0]
    final_battle_own = []
    final_battle_opp = []
    for i in range(len(battle_log)):
        temp_list = list(parse(battle_l.battle.teams[0][i]))
        temp_list_2 = list(parse(battle_l.battle.teams[1][i]))
        final_battle_own.append(temp_list)
        final_battle_opp.append(temp_list_2)
    return final_battle_own,final_battle_opp

def battle_log(battle_l,tag):
     details = list(parse(battle_l))
     log_b = []
     log_b.append(details[0][1]) # TIME
     log_b.append(details[1][2]) # ID
     log_b.append(details[2][2]) # EVENT MODE
     log_b.append(details[3][2]) # EVENT MAP
     log_b.append(details[4][2]) # BATTLE MODE
     if details[4][2]=='soloShowdown' or details[4][2]=='duoShowdown':
        print("----------------------------------------------------------------------------------------")
        print("DATE : "+time_extract(log_b[0]))
        print("----------------------------------------------------------------------------------------")
        print("Event ID : "+str(log_b[1])+"     | Event Mode : "+log_b[2]+"     | Event Map : "+log_b[3])
        print("Battle Mode : "+log_b[4])
        print("----------------------------------------------------------------------------------------")
        temp_det = []
        temp_det.append(details[5][2]) # Type
        temp_det.append(details[6][2]) # Rank
        j = 0
        if details[7][1]=='trophy_change':
            temp_det.append(details[7][2]) # Trophy Change
        else:
            temp_det.append(0)
            j = 1
        print("Type : "+temp_det[0]+"     | Rank : "+str(temp_det[1])+"    | Trophy Change : "+str(temp_det[2]))
        query = "INSERT INTO battle_det VALUES('{}','{}',{},'{}','{}','{}',{},'{}')".format(tag,time_extract(log_b[0]),log_b[1],log_b[2],log_b[3],temp_det[0],temp_det[2],log_b[4])
        cur.execute(query)
        conn.commit()
        if details[4][2]=='soloShowdown':
            show_down_parse(j,tag,time_extract(log_b[0]),details)
        else:
            dshow_down_parse(j,tag,time_extract(log_b[0]),details)
     elif details[4][2]=='bigGame' or details[4][2]=='roboRumble' or details[4][2]=='bossFight' or details[4][2]=='takedown' or details[4][2]=='loneStar':
        # log_b.append(details[5][2]) #Battle Duration
        # print("----------------------------------------------------------------------------------------")
        # print("DATE : "+time_extract(log_b[0]))
        # print("----------------------------------------------------------------------------------------")
        # print("Event ID : "+str(log_b[1])+"     | Event Mode : "+log_b[2]+"     | Event Map : "+log_b[3])
        # print("Battle Mode : "+log_b[4]+"   | Battle Duration : "+str(convert(log_b[5])))
        # print("----------------------------------------------------------------------------------------")
        # bs = []
        # for x in range(len(details[6][2])): 
        #    temp = []
        #    temp.append(details[6][2][x].tag)
        #    temp.append(details[6][2][x].name)
        #    temp.append(str(details[6][2][x].brawler.id))
        #    temp.append(details[6][2][x].brawler.name)
        #    temp.append(str(details[6][2][x].brawler.power))
        #    temp.append(str(details[6][2][x].brawler.trophies))
        #    bs.append(temp)
        # bbtag = details[7][2]
        # bbn = details[8][2]
        # bbbi = str(details[9][3])
        # bbbn = details[10][3]
        # bbbp = str(details[11][3])
        # bbbt = str(details[12][2])
        print('NO')
     else:
        log_b.append(details[5][2]) # BATTLE TYPE
        log_b.append(details[6][2]) # BATTLE RESULT
        log_b.append(details[7][2]) # BATTLE DURATION
        i = 0
        if details[8][1]=='trophy_change':
            log_b.append(details[8][2]) # TROPHY CHANGE
        else:
            i=1
            log_b.append(0)
        log_b.append(details[9-i][3]) # STAR PLAYER TAG
        l1,l2 = form_vic_def_list(battle_l)
        new_l1 = get_victory_defeat__list(l1)
        new_l2 = get_victory_defeat__list(l2)
        print_log(tag,log_b,new_l1,new_l2)

def time_extract(timee):
    return timee[4:6]+"-"+timee[6:8]+"-"+timee[:4] + " "+timee[9:11]+":"+timee[11:13]+":"+timee[13:15]

def gt(timee):
    return datetime.strptime(timee[:4]+"-"+timee[4:6]+"-"+timee[6:8]+" "+timee[9:11]+":"+timee[11:13]+":"+timee[13:15],"%Y-%m-%d %H:%M:%S")


def dshow_down_parse(j,tag,time,det):
    for i in range(len(det[8-j][2])):
        print("----------------------------------------------------------------------------------------")
        print("TEAM "+str(i+1))
        for k in range(2):
            print("----------------------------------------------------------------------------------------")
            print("Tag : "+det[8-j][2][i][k].tag)
            print("Name : "+det[8-j][2][i][k].name)
            print("Brawler ID : "+str(det[8-j][2][i][k].brawler.id))
            print("Brawler Name : "+det[8-j][2][i][k].brawler.name)
            print("Brawler Name : "+str(det[8-j][2][i][k].brawler.power))
            print("Brawler Trophies : "+str(det[8-j][2][i][k].brawler.trophies))
            print("----------------------------------------------------------------------------------------")
            query = "INSERT INTO battle_duo VALUES('"+str(tag)+"','"+time+"',"+str(i+1)+",'"+det[8-j][2][i][k].tag+"','"+det[8-j][2][i][k].name.replace("'","''")+"',"+str(det[8-j][2][i][k].brawler.id)+",'"+det[8-j][2][i][k].brawler.name+"',"+str(det[8-j][2][i][k].brawler.power)+","+str(det[8-j][2][i][k].brawler.trophies)+")"
            cur.execute(query)
            conn.commit()


def show_down_parse(j,tag,time,det):
    print("Players : "+str(len(det[8-j][2])))
    for i in range(len(det[8-j][2])):
        print("----------------------------------------------------------------------------------------")
        print("Tag : "+det[8-j][2][i].tag)
        print("Name : "+det[8-j][2][i].name)
        print("Brawler ID : "+str(det[8-j][2][i].brawler.id))
        print("Brawler Name : "+det[8-j][2][i].brawler.name)
        print("Brawler Power : "+str(det[8-j][2][i].brawler.power))
        print("Brawler Trophies : "+str(det[8-j][2][i].brawler.trophies))
        print("----------------------------------------------------------------------------------------")
        # query2 = ins+det[8-j][2][i].tag+btd+"'"+temp_det[0]+"',"+str(get_br_trophies(det[8-j][2][i].tag[1:],det[8-j][2][i].brawler.name)-det[8-j][2][i].brawler.trophies)+bm
        query = "INSERT INTO battle_solo VALUES('"+tag+"','"+time+"',"+str(i+1)+",'"+det[8-j][2][i].tag+"','"+det[8-j][2][i].name.replace("'","''")+"',"+str(det[8-j][2][i].brawler.id)+",'"+det[8-j][2][i].brawler.name+"',"+str(det[8-j][2][i].brawler.power)+","+str(det[8-j][2][i].brawler.trophies)+")"
        # cur.execute(query2)
        # conn.commit()
        cur.execute(query)
        conn.commit()



def print_log(tag,detls,vic,deft):
    print("----------------------------------------------------------------------------------------")
    print("DATE : "+time_extract(detls[0]))
    print("----------------------------------------------------------------------------------------")
    print("Event ID : "+str(detls[1])+"     | Event Mode : "+detls[2]+"     | Event Map : "+detls[3])
    print("Battle Mode : "+detls[4]+"    | Battle Type : "+detls[5])
    print("----------------------------------------------------------------------------------------")
    print(detls[6].upper()+"        | Battle Duration : "+str(convert(detls[7]))+"      | Trophy Change : "+str(detls[8]))
    print("----------------------------------------------------------------------------------------")
    star_ply_tg = detls[9]
    query = "INSERT INTO battle_det VALUES('{}','{}',{},'{}','{}','{}',{},'{}')".format(tag,time_extract(detls[0]),detls[1],detls[2],detls[3],detls[5],detls[8],detls[4])
    cur.execute(query)
    conn.commit()
    vic_flag = True
    for i in range(3):
        if(vic[i][0]==star_ply_tg):
            vic_flag = False
            break
    if detls[6].upper()!='DRAW':
        if not vic_flag:
            print_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'VICTORY',1,vic,star_ply_tg)
            print_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DEFEAT',2,deft,star_ply_tg)
        else:
            print_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DEFEAT',1,vic,star_ply_tg)
            print_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'VICTORY',2,deft,star_ply_tg)
    else:
        print_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DRAW',1,vic,star_ply_tg)
        print_teams(tag,str(convert(detls[7])),time_extract(detls[0]),'DRAW',2,deft,star_ply_tg)


def print_teams(tag,duration,time,result,team,bteam,stag):
    print("----------------------------------------------------------------------------------------")
    print("TEAM {}: ".format(team))
    print("----------------------------------------------------------------------------------------")
    for i in range(3):
        flag = True
        if(bteam[i][0]==stag):
            print("STAR PLAYER")
        else:
            flag = False
            print("PLAYER")
        teem = bteam[i].copy()
        max_range = len(bteam[i])
        det = ['TAG','Name','Brawler ID','Brawler Name','Brawler Power','Brawler Trophies']
        for i in range(max_range):
            print(det[i]+' : '+str(teem[i]))
        if(max_range!=6):
            for i in range(6 - max_range):
                teem.append('null')
        s = None
        if not flag:
            s = "INSERT INTO battle_team VALUES('{}','{}','{}','{}','normal',{},'{}','{}',{},'{}',{},{})".format(tag,time,result,duration,team,teem[0],teem[1].replace("'","''"),teem[2],teem[3],teem[4],teem[5])
        else:
            s = "INSERT INTO battle_team VALUES('{}','{}','{}','{}','star',{},'{}','{}',{},'{}',{},{})".format(tag,time,result,duration,team,teem[0],teem[1].replace("'","''"),teem[2],teem[3],teem[4],teem[5])
        cur.execute(s)
        conn.commit()
        print(" ")
        print(" ")

def insert_battle_det(blog,tag):
    query = "SELECT battle_time FROM battle_det WHERE tag = '#"+tag+"' ORDER BY battle_time desc FETCH FIRST ROW ONLY"
    cur = conn.cursor()
    cur.execute(query)
    x = cur.fetchall()
    cnt = 0
    if(len(x)>0):
        last_bt = datetime.strptime(str(x[0][0]),"%Y-%m-%d %H:%M:%S")
        for i in range(25):
            if(gt(blog[i].battle_time)<=last_bt):
                break
            cnt = cnt+1
    else:
        cnt = 25
    return cnt
       

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def parse_profile(prof_list):
    print("---------------------------------------------------------------------")
    print("PLAYER PROFILE ")
    print("---------------------------------------------------------------------")
    print("Tag : "+prof_list.tag)
    print("Name : "+prof_list.name)
    print("Name Color : "+str(prof_list.name_color))
    print("Trophies : "+str(prof_list.trophies))
    print("Highest Trophies : "+str(prof_list.highest_trophies))
    print("Experience Level : "+str(prof_list.exp_level))
    print("Expereince Points : "+str(prof_list.exp_points))
    print("CC Q : "+str(prof_list.is_qualified_from_championship_challenge))
    print("3vs3 Victories : "+str(prof_list.x3vs3_victories))
    print("Solo Victories : "+str(prof_list.solo_victories))
    print("Duo Victories : "+str(prof_list.duo_victories))
    print("Best Robo Rumble Time : "+str(convert(prof_list.best_robo_rumble_time)))
    print("Best Time as Big Brawler : "+str(convert(prof_list.best_time_as_big_brawler)))
    query_check = "SELECT * FROM PROFILE WHERE tag = '"+prof_list.tag+"';"
    cur.execute(query_check)
    x = cur.fetchall()
    query = ""
    if(len(x)>0):
        query = "UPDATE PROFILE SET tag = '"+prof_list.tag+"',name = '"+prof_list.name.replace("'","''")+"',name_color = '"+str(prof_list.name_color)+"',trophies = "+str(prof_list.trophies)+",highest_trophies = "+str(prof_list.highest_trophies)+",exp_level = "+str(prof_list.exp_level)+",exp_points = "+str(prof_list.exp_points)+",champ_q = '"+str(prof_list.is_qualified_from_championship_challenge)+"',tvt_vict = "+str(prof_list.x3vs3_victories)+",solo_vict = "+str(prof_list.solo_victories)+",duo_vict = "+str(prof_list.duo_victories)+",rrt = '"+str(convert(prof_list.best_robo_rumble_time))+"',bbt = '"+str(convert(prof_list.best_time_as_big_brawler))+"' WHERE tag = '"+prof_list.tag+"'" 
    else:
        query = "INSERT INTO PROFILE VALUES('"+prof_list.tag+"','"+prof_list.name.replace("'","''")+"','"+str(prof_list.name_color)+"',"+str(prof_list.trophies)+","+str(prof_list.highest_trophies)+","+str(prof_list.exp_level)+","+str(prof_list.exp_points)+",'"+str(prof_list.is_qualified_from_championship_challenge)+"',"+str(prof_list.x3vs3_victories)+","+str(prof_list.solo_victories)+","+str(prof_list.duo_victories)+",'"+str(convert(prof_list.best_robo_rumble_time))+"','"+str(convert(prof_list.best_time_as_big_brawler))+"');"
    cur.execute(query)
    conn.commit()
    # cur.execute(query_check)
    # x = cur.fetchall() # Reutrns the player details , Data type : Tuple
    parse_ind_brawlers(prof_list.brawlers,prof_list.tag) # Function to get list of bralwers
    # return query

def parse_ind_brawlers(lets_brawl,tag):
    flag = True
    query_check = "SELECT * FROM BRAWLERS WHERE tag = '"+tag+"';"
    cur.execute(query_check)
    x = cur.fetchall()
    if(len(x)>0) :
        flag = False
    print("---------------------------------------------------------------------")
    print("BRAWLER LIST : "+str(len(lets_brawl))+" BRAWLERS")
    print("---------------------------------------------------------------------")
    for i in lets_brawl:
        get_brawler_details(list(parse(i)),tag,flag)
    cur.execute(query_check)
    x = cur.fetchall()
    for i in x:
        print(i)


def get_brawler_details(brawl_list,tag,flag):
    list_tp = []
    # print(brawl_list)
    for i in brawl_list:
        list_tp.append(i[1])
    print("---------------------------------------------------------------------")
    print("ID : "+str(list_tp[0]))
    print("Brawler Name : "+list_tp[1])
    print("Power : "+str(list_tp[2]))
    print("Rank : "+str(list_tp[3]))
    print("Trophies : "+str(list_tp[4]))
    print("Highest Trophies : "+str(list_tp[5]))
    x = list(list_tp[6])
    star_list = []
    temp_str = ""
    temp_ste = "" 
    cntr = 0
    for y in x:
        cntr = cntr + 1
        star_list.append(y.id)
        temp_str += ","+str(y.id)+","
        temp_ste += ",brawler_star_power_{}_id = ".format(cntr)+str(y.id)
        star_list.append(y.name)
        temp_str += "'"+y.name+"'"
        temp_ste += ",brawler_star_power_{}_name = '".format(cntr)+y.name+"'"
    print("STAR POWER : "+str(star_list))
    print("---------------------------------------------------------------------")
    print(temp_ste)
    query = ""
    if not flag:
        query = "UPDATE BRAWLERS SET brawler_power = "+str(list_tp[2])+", brawler_rank = "+str(list_tp[3])+", brawler_trophies = "+str(list_tp[4])+", brawler_highest_trophies = "+str(list_tp[5])+temp_ste+"WHERE tag = '"+tag+"' and brawler_id = "+str(list_tp[0])
    else:
        query = "INSERT INTO BRAWLERS VALUES('"+tag+"',"+str(list_tp[0])+",'"+list_tp[1]+"',"+str(list_tp[2])+","+str(list_tp[3])+","+str(list_tp[4])+","+str(list_tp[5])+temp_str+")"
    cur.execute(query)
    conn.commit()
    

def get_club_ply_det(player_det,club_tag):
    query_flag = False
    query = "select * from club_members where player_tag = '"+player_det.tag+"'"
    cur.execute(query)
    x = cur.fetchall()
    if len(x) > 0: 
        query_flag = True
    print("---------------------------------------------------------------------")
    print("Tag : "+player_det.tag)
    print("Name : "+player_det.name)
    print("Name Color : "+player_det.name_color)
    print("Role : "+player_det.role)
    print("Trophies : "+str(player_det.trophies))
    print("---------------------------------------------------------------------")
    query = ""
    if query_flag:
        query = "UPDATE CLUB_MEMBERS SET club_tag = '"+club_tag+"',player_name = '"+player_det.name.replace("'","''")+"',player_nc = '"+player_det.name_color+"',player_role = '"+player_det.role+"',player_trophies = "+str(player_det.trophies)+" WHERE player_tag = '"+player_det.tag+"'"
    else:
        query = "INSERT INTO CLUB_MEMBERS VALUES('"+club_tag+"','"+player_det.tag+"','"+player_det.name.replace("'","''")+"','"+player_det.name_color+"','"+player_det.role+"',"+str(player_det.trophies)+")"
    cur.execute(query)
    conn.commit()
    # return query

def club_details(play):
    club = play.get_club()
    flagi = True
    try:
        test = club.tag
    except:
        flagi = False
        print("Not in club")
    if flagi:
        print("CLUB TAG : "+club.tag)
        print("CLUB NAME : "+club.name)
        print("CLUB TROPHIES : "+str(club.trophies))
        print("CLUB TYPE : "+club.type)
        print("CLUB RTRP : "+str(club.required_trophies))
        print("CLUB DESC : "+club.description)
        query_check = "SELECT * FROM CLUB WHERE club_tag = '"+club.tag+"';"
        cur.execute(query_check)
        x = cur.fetchall()
        flag = False
        if(len(x)>0):
            flag= True
            query = "UPDATE CLUB SET club_name = '"+club.name.replace("'","''")+"',club_trophies = "+str(club.trophies)+",club_required_t = "+str(club.required_trophies)+",club_type = '"+club.type+"',club_description = '"+club.description.replace("'","''")+"' WHERE club_tag = '"+club.tag+"'"
        else:
            query = "INSERT INTO CLUB VALUES('"+club.tag+"','"+club.name.replace("'","''")+"',"+str(club.trophies)+","+str(club.required_trophies)+",'"+club.type+"','"+club.description.replace("'","''")+"');"
        cur.execute(query)
        conn.commit()
        club_mem = club.get_members()
        for i in club_mem:
            get_club_ply_det(i,club.tag)
        cur.execute(query_check)
        x = cur.fetchall()
        print(x)
        cur.execute("SELECT * FROM CLUB_MEMBERS WHERE club_tag = '"+club.tag+"'")
        y = cur.fetchall()
        print(y)
    # return query

def analysis(tag):
    cur.execute("SELECT * from WIN_TEAM('{}')".format(tag))
    x = cur.fetchall()
    wins = 0 if x[0][0] is None else x[0][0]
    games_palyed = 1 if x[0][1] is None else x[0][1]
    cur.execute("SELECT * FROM WIN_SHOW('{}')".format(tag))
    x = cur.fetchall()
    sr1 = 0 if x[0][0] is None else x[0][0]
    sr2 = 0 if x[0][1] is None else x[0][1]
    sgp = 1 if x[0][2] is None else x[0][2]
    cur.execute("select * from WIN_SHOWR('{}',{})".format(tag,1))
    x = cur.fetchall()
    var1 = 0 if x[0][0] is None else x[0][0]
    var2 = 0 if x[0][1] is None else x[0][1]
    var3 = 1 if x[0][2] is None else x[0][2]
    
    cur.execute("select * from WIN_SHOWR('{}',{})".format(tag,2))
    x = cur.fetchall()
    print(x)
    var1s = 0 if x[0][0] is None else x[0][0]
    var2s = 0 if x[0][1] is None else x[0][1]
    var3s = 1 if x[0][2] is None else x[0][2]
   
    print("OVERALL WIN RATE : {}".format(((wins+sr1+sr2)*100)/(games_palyed+sgp)))
    print("TEAM WIN RATE : {}".format((wins*100)/games_palyed))
    print("SHOWDOWN WIN RATE : Rank 1 : {}  | Rank 2 : {}".format((sr1*100)/sgp,(sr2*100)/sgp))
    print("SOLO SHOWDOWN WIN RATE : Rank 1 : {}  | Rank 2 : {}".format((var1*100)/var3,(var2*100)/var3))
    print("DUO SHOWDOWN WIN RATE : Rank 1 : {}  | Rank 2 : {}".format((var1s*100)/var3s,(var2s*100)/var3s))

def ind_event_page(tag):
    print("TEAM MAPS")
    cur.execute("SELECT * FROM IND_MAP('{}')".format(tag))
    team_event = cur.fetchall()
    modes = []
    for i in team_event:
        modes.append(i[0])
    modes = set(modes)
    print(modes)
    print("\n\nShowdown Map")
    cur.execute("SELECT * FROM IND_MAP_SHOW('{}')".format(tag))
    show = cur.fetchall()
    smaps = []
    for i in show:
        smaps.append(i[0])
    smaps = set(smaps)
    print(smaps)

    print("\n\nShowdown Map Ind")
    cur.execute("SELECT * FROM IND_MAP_SHOWE('{}',{});".format(tag,1))
    show_r = cur.fetchall()
    smaps1 = []
    for i in show_r:
        smaps1.append(i[0])
    smaps1 = set(smaps1)
    print(smaps1)

    print("\n\nShowdown Map Ind 2")
    cur.execute("SELECT * FROM IND_MAP_SHOWE('{}',{});".format(tag,2))
    show_r = cur.fetchall()
    smaps2 = []
    for i in show_r:
        smaps2.append(i[0])
    smaps2 = set(smaps2)
    print(smaps2)

def exist(s,el):
    for i in s:
        if i[0]==el and i[1]:
            return True
    return False
    
def ind_brawler(tag):
    print("-------------------------------------------------------------------")
    cur.execute("SELECT * FROM brawler_performance('{}')".format(tag))
    brawler_performance = cur.fetchall()
    bp = []
    for i in brawler_performance:
        bp.append(i[0])
    bp = set(bp)
    print(bp)
    
    print("\n\n")
    cur.execute("SELECT * FROM team_brawler_performance('{}')".format(tag))
    team_performance = cur.fetchall()
    tp = []
    for i in team_performance:
        tp.append((i[0],i[2]))
    tp = set(tp)
    m = []
    mb = []
    check = []
    for i in tp:
        if not exist(check,i[0]):
            m.append(i[0])
            check.append((i[0],True))
            temp = []
            for j in tp:
                if i[0]==j[0]:
                    temp.append(j[1])
            temp = set(temp)
            mb.append(temp)
    m = set(m)
    print(m)
    print(mb)


    print("\n\n")
    cur.execute("SELECT * FROM showdown_brawler_performance('{}')".format(tag))
    showdown_performance = cur.fetchall()
    sp = []
    for i in showdown_performance:
        sp.append(i[1])
    sp = set(sp)
    print(sp)
    print("\n\n")
    cur.execute("SELECT * FROM showdown_ind_brawler_performance('{}',{})".format(tag,1))
    showdown_performance_ind = cur.fetchall()
    sp1 = []
    for i in showdown_performance_ind:
        sp1.append(i[1])
    sp1 = set(sp1)
    print(sp1)


    print("\n\n")
    cur.execute("SELECT * FROM showdown_ind_brawler_performance('{}',{})".format(tag,2))
    showdown_performance_ind = cur.fetchall()
    sp2 = []
    for i in showdown_performance_ind:
        sp2.append(i[1])
    sp2 = set(sp2)
    print(sp2)
    


token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImFlNTMzMjlhLWFjNjItNDQ0YS05NzlhLTI2YzFlZjVkMjM0ZSIsImlhdCI6MTU4Njk0NDgyMiwic3ViIjoiZGV2ZWxvcGVyL2IwZDZiNDk4LTFlYWMtMTM1Ni1hMTllLTYwZTlmMzQ0YmY3NCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTU3LjMyLjIzOC4yMzMiXSwidHlwZSI6ImNsaWVudCJ9XX0.6KfTuA3vb8giIcjqRz1U9ar6jAqpRqvpG2iGH60Fhthn1JO_12VEJG8hrdpxcUfszp3Y0ud7ihz0NOLbAOw9nw'

# tagg = sys.argv[1]
# print(type(tagg))



#     print('')
#     print('')

# insert_battle_det('#P0VYR22V')
# battles = client.get_battle_logs(tag)
# for i in range(25):
    # print("BATTLE NUMBER : "+str(i+1))
    # battles[i].battle_time = '0200406T111944'
    # pprint(battles[i])
# 
# print('\n\n\n')

# Tag = 'Q80JYUJU'
# try:
# client = brawlstats.OfficialAPI(token)
# tag = '2LJYR2UU'
# player = client.get_player(tag)
# parse_profile(player)
# club_details(player)
# battles = client.get_battle_logs(tag)
# Tag = "#{}".format(tag)
# count = insert_battle_det(battles,tag)
# print(count)
# for i in range(count):
#     print("BATTLE NUMBER : "+str(i+1))
#     # print(battles[i])
#     battle_log(battles[i],Tag)
# analysis(Tag)
# ind_event_page(Tag)
# ind_brawler(Tag)
# except:
#     print("Doffa khotu kem nakhe che")

# get_br_trophies(Tag,'NAMIT')

# club_details(player)
# # cur.execute(parse_profile(player))
# conn.commit()
# print(player.raw_data)
# cont = client.get_constants()
# print(cont[0])

# print('\n\n\n')

# try:
#     print(club.tag))
# except:
#     print("NO")
# print("CLUB TAG : "+club.tag)
# print("CLUB NAME : "+club.name)
# print("CLUB TROPHIES : "+str(club.trophies))
# print("CLUB TYPE : "+club.type)
# print("CLUB RTRP : "+str(club.required_trophies))
# print("CLUB DESC : "+club.description)
# # # print(club.badge)
# best_players = club.get_members() # members sorted by trophies
# for player in best_players:
#     get_club_ply_det(player)



# {'battle_time': '20200404T132900.000Z', 'event': {'id': 15000039, 'mode': 'roboRumble', 'map': 'Keep Safe'}, 'battle': {'mode': 'roboRumble', 'duration': 357, 'players': [{'tag': '#2LJYR2UU', 'name': '〘 彡★ ZΞUS ★彡 〙', 'brawler': {'id': 16000007, 'name': 'JESSIE', 'power': 9, 'trophies': 571}}, {'tag': '#2JPY8PUC', 'name': 'Super3abdo', 'brawler': {'id': 16000001, 'name': 'COLT', 'power': 10, 'trophies': 567}}, {'tag': '#GJUJJ09L', 'name': 'ThuNder', 'brawler': {'id': 16000016, 'name': 'PAM', 'power': 10, 'trophies': 543}}]}}


# 1. SORT BRAWLERS ON BASIS OF POWER,TROPHIES
# 2. OVERALL WINING PERCENTAGE OF THE IND PLAYER REGARDLESS OF MAP,EVENT,BATTLE TYPE
# 3. WINNING PERCENTAGE CONSIDERING TEAM,DUO AND SOLO WISE
# 4. WINNING PERCENTAGE CONDIDERING MAPS FOR SPECIFIC EVENT FOR TEAM,DUO AND SOLO
# 5. BRAWLER PERFORMANCE FOR PARTICULAR EVENT I.E. TEAM,SOLO,DUO
# 6. PLAYER'S BRAWLER PERFORMANCE ON BASIS OF HIS BATTLE FOR TEAM,DUO,SOLO
# 7. BRAWLERS PERFORMANCE ON BASIS OF PARTIUCULAR MAP OF IND. EVENT
# 8. PLAYER'S BRAWLER PERFORMANCE ON BASIS OF PARTICULAR MAP OF IND. EVENT
# 9. Brawlers Performance regardless of team,solo,duo