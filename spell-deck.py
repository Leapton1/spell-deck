from flask import Flask, render_template, jsonify, request, url_for, redirect
import json
from random import randint
import os

app=Flask("dom")



sessions=[]

gamedata=[["145",[],[[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]\
    ,[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]]],\
    ["321",[],[[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]\
    ,[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]]]]

actions=[]
cards=[[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]\
    ,[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]]

def remove_card(cardcode,player,game):
    global gamedata
    if cardcode!="DUD":
        for i in range(0, len(gamedata[game][2][player])):
            if cardcode==gamedata[game][2][player][i][0]:
                index=i
        gamedata[game][2][player].pop(index)

def csh_check(player,game):
    global gamedata
    for i in range(0, len(gamedata[game][2][player])):
        for i2 in range(0, len(gamedata[game][2][player][i][1])):
            if gamedata[game][2][player][i][1][i2]=="arcane" or gamedata[game][2][player][i][1][i2]=="all":
                return True
    return False

def find_game(ID):
    global gamedata
    for i in range(0, len(gamedata)):
        if gamedata[i][0]==ID:
            return int(i)
    return int(0)


@app.route("/")
def start():
    return render_template('spell-setup.html')

@app.route('/makegame', methods = ['POST'])
def makegame():
    global sessions
    pat=request.get_json()
    gamedata.append([pat[0],[],[[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]\
    ,[["FRB",["fire"]],["MGB",["arcane"]],["WRD",["arcane"]],["CSH",["arcane"]],["ACM",["arcane"]],["ABE",["all"]],["TNF",["fire"]],["PFL",["fire"]],["INF",["fire"]],["CTS",["arcane"]]]]])
    return jsonify(pat)

@app.route('/sessionget', methods = ['POST'])
def sessionerget():
    global sessions
    random_num=randint(0,100000)
    pat=request.get_json()
    sessions.append([len(sessions),pat[0],random_num,pat[1],find_game(pat[1])])
    return jsonify(random_num)

@app.route('/sessionsend', methods = ['POST'])
def sessionersend():
    global sessions
    info=0
    print(sessions)
    print(len(sessions))
    pat=request.get_json()
    print(pat)
    for i in range(0,len(sessions)):
        if sessions[i][2]==pat:
            info=sessions[i]
    return jsonify(info)

@app.route("/main")
def mainroute():
    e = request.args.get('e')
    return render_template('spell-deck.html',e=e)

@app.route('/postman', methods = ['POST'])
def postman():
    global gamedata
    pat=request.get_json()
    print(pat)
    #print(pat)
    print([[],len(gamedata[pat[1]][1])])
    info=[[],len(gamedata[pat[1]][1])]
    for i in range(pat[0],len(gamedata[pat[1]][1]) ): 
        info[0].append(gamedata[pat[1]][1][i])
    #print(actions)
    #print(info)
    return jsonify(info)

@app.route('/action', methods = ['POST'])
def actioner():
    global gamedata
    #pat=cardcode,player_num,getstats(cardcode),game_id,appended bit for extra data that is going to be a pain whenever I add something new to this
    pat=request.get_json()
    pat.append([])
    remove_card(pat[0],pat[1],pat[3])
    if pat[0]=="CSH":
        pat[4].append(csh_check(pat[1],pat[3]))
    gamedata[pat[3]][1].append(pat)
    return jsonify('hi there')

port=os.getenv('PORT') or 80

app.run(host='0.0.0.0', port=port)