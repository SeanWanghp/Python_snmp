import json, ast
import os, threading
from flask import Flask, jsonify, request, render_template, send_from_directory, make_response
from dao import db
from setting import TESTBEDS_INFO, systemFile, monitorFile, rootIP, PICTURE_UPLOAD_PATH, monitormore
from utils import retrieve_dir, cleanOldIP, CLI
from ssh import SSH
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["JSON_AS_ASCII"] = False  # jsonify返回的中文正常显示


@app.route('/')
def index():
    # 检查token
    return render_template("main.html")


@app.route('/show_data')
def show():
    if request.method == "GET":
        owners = request.args.get('owners')
        if 'allOwners' in owners or len(owners) == 0:
            sql = f'select * from {TESTBEDS_INFO}'
        else:
            owners = owners.split(',')
            sql = f'select * from {TESTBEDS_INFO} where owner in (' + str(owners)[1:-1] + ')'
        data = db.select(sql)
        return jsonify(data)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/cascade_data')
def cascade_data():
    sql = f'select distinct owner from {TESTBEDS_INFO} where Type != \'VM\''
    owners = db.select(sql)

    sql = f'select distinct owner from {TESTBEDS_INFO} where Type = \'VM\''
    vm_owners = db.select(sql)

    sql = f'select distinct `System` from {TESTBEDS_INFO} where Type != \'VM\''
    systems = db.select(sql)

    sql = f'select distinct `System` from {TESTBEDS_INFO} where Type = \'VM\''
    vm_systems = db.select(sql)

    sql = f'select Owner,`IP`,`System`,Type from {TESTBEDS_INFO} where Type != \'VM\''
    data = db.select(sql)

    sql = f'select Owner,`IP`,`System`,Type from {TESTBEDS_INFO} where Type = \'VM\''
    vm_data = db.select(sql)

    casByOwner = []
    for it in owners:
        tmp = {'value': it['owner'], 'label': it['owner'], 'children': []}
        for item in data:
            if item['Owner'] == it['owner']:
                tmp['children'].append({'value': item['IP'], 'label': item['IP']})
        casByOwner.append(tmp)

    casBySystem = []
    for it in systems:
        tmp = {'value': it['System'], 'label': it['System'], 'children': []}
        for item in data:
            if item['System'] == it['System']:
                tmp['children'].append({'value': item['IP'], 'label': item['IP']})
        casBySystem.append(tmp)
    # vm data
    vm_casByOwner = []
    for it in vm_owners:
        tmp = {'value': it['owner'], 'label': it['owner'], 'children': []}
        for item in vm_data:
            if item['Owner'] == it['owner']:
                tmp['children'].append({'value': item['IP'], 'label': item['IP']})
        vm_casByOwner.append(tmp)
    vm_casBySystem = []
    for it in vm_systems:
        tmp = {'value': it['System'], 'label': it['System'], 'children': []}
        for item in vm_data:
            if item['System'] == it['System']:
                tmp['children'].append({'value': item['IP'], 'label': item['IP']})
        vm_casBySystem.append(tmp)

    result = [

        [
            {
                'value': 'byOwner',
                'label': 'byOwner',
                'children': casByOwner
            },
            {
                'value': 'bySystem',
                'label': 'bySystem',
                'children': casBySystem
            }
        ],

        [
            {
                'value': 'byOwner',
                'label': 'byOwner',
                'children': vm_casByOwner
            },
            {
                'value': 'bySystem',
                'label': 'bySystem',
                'children': vm_casBySystem
            }
        ]

    ]

    return jsonify(result)


@app.route('/check_owners')
def check_owners():
    if request.method == "GET":
        sql = f'select distinct owner from {TESTBEDS_INFO}'
        data = db.select(sql)
        return jsonify(data)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/check_systems')
def check_systems():
    if request.method == "GET":
        sql = f'select distinct `System` from {TESTBEDS_INFO} where `System` !=\'\''
        data = db.select(sql)
        return jsonify(data)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/check_disconnected')
def check_disconnected():
    if request.method == "GET":
        sql = f'select * from {TESTBEDS_INFO} where Connected = 0'
        data = db.select(sql)
        return jsonify(data)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/check_error')
def check_error():
    if request.method == "GET":
        sql = f'select * from {TESTBEDS_INFO} where Connected = 3'
        data = db.select(sql)
        return jsonify(data)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/add_equip', methods=["POST"])
def addEquip():
    if request.method == "POST":
        data = request.form.to_dict()
        owner = data['owner']
        system = data['system']
        ip = data['ip']
        type = data['type']
        rack = data['rack']
        connected = data['connected']
        sql = f'insert into {TESTBEDS_INFO} (Owner,`System`,IP,`Type` ,Rack, Connected) values {owner, system, ip, type, rack, connected};'
        db.execute_db(sql)
        return jsonify("添加成功")
    else:
        assert False, 'Request Method don\'t match'


@app.route('/edit_equip', methods=["POST"])
def editEquip():
    if request.method == "POST":
        data = request.form.to_dict()
        owner = data['owner']
        system = data['system']
        ip = data['ip']
        type = data['type']
        rack = data['rack']
        id = data['id']
        connected = data['connected']
        old_ip = sql = f'select IP from {TESTBEDS_INFO} where id = \'{id}\''
        db.execute_db(sql)
        cleanOldIP(old_ip, db)
        sql = f'update {TESTBEDS_INFO} set owner=\'{owner}\', `System`=\'{system}\', ip=\'{ip}\', `Type`=\'{type}\', rack=\'{rack}\', Connected=\'{connected}\' where id = \'{id}\';'
        db.execute_db(sql)
        return jsonify("编辑成功")
    else:
        assert False, 'Request Method don\'t match'


@app.route('/delete_equip')
def deleteEquip():
    if request.method == "GET":
        id = request.args.get('id')
        sql = f'delete from {TESTBEDS_INFO} where id = \'{id}\';'
        db.execute_db(sql)
        return jsonify("删除成功")
    else:
        assert False, 'Request Method don\'t match'


@app.route('/get_log')
def getLog():
    if request.method == "GET":
        res = ''
        with open(monitorFile, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            # 只显示最后五十行
            data = lines[-50:]
        for i in data:
            res += i
        return jsonify(res)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/get_more')
def getmore():
    if request.method == "GET":
        res = ''
        with open(monitormore, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            # 只显示最后五十行
            data = lines[-50:]
        for i in data:
            res += i
        return jsonify(res)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/getFileTree')
def getFileTree():
    if request.method == "GET":
        res, nodesNum = retrieve_dir(systemFile, nodeID=1)
        nodesNum -= 1
        return jsonify(res)
    else:
        assert False, 'Request Method don\'t match'


@app.route('/downloadSystemFile/<path>', methods=['GET', 'POST', 'OPTIONS'])
def downloads(path):
    path = path.replace('$', '/')
    fullPath = systemFile + path
    fileName = fullPath.split('/')[-1]
    pre = fullPath.split(fileName)[0]
    try:
        if os.path.isdir(path):
            return '<h1>文件夹无法下载</h1>'
        else:
            print('filePath:', pre)
            print('fileName:', fileName)
            return send_from_directory(path=fullPath, directory=pre, filename=fileName, as_attachment=True)
    except:
        return '<h1>该文件不存在或无法下载</h1>'


@app.route('/execute', methods=['POST'])
def execute():
    if request.method == "POST":
        data = request.form.to_dict()
        ips = json.loads(data['ips'])
        c = data['cli']
        p = []
        res = ''
        error_ip = []
        for item in ips:
            t = CLI(ip=item[2], c=c)
            p.append(t)
        for t in p:
            t.start()
        for t in p:
            t.join()
        for t in p:
            tmp = t.get_result()
            if tmp != 'Wrong!!!':
                tmp = ''.join(tmp)
                res += t.ip + ':\n'
                res += tmp
            else:
                error_ip.append(t.ip)

        return jsonify(res, error_ip)


@app.route('/get_topo')
def getTopo():
    refresh = int(request.args.get('refresh'))
    print(refresh)
    # refresh = 1
    # 先从数据库里读数据出来，如果没有再进系统用命令行取
    sql = 'select * from lldp_neighbor'
    lldp_neighbor = db.select(sql)
    error_ip = []
    if len(lldp_neighbor) == 0 or refresh:
        sql = f'select ip,`System` from {TESTBEDS_INFO} where Type != \'VM\' and `System` != \'\''
        tmp = db.select(sql)
        ips = []
        system_names = []
        for i in tmp:
            ips.append(i['ip'])
            system_names.append(i['System'])
        p = []
        nodes = []
        lines = []
        isolated_system = []
        lines.append({'from': rootIP, 'to': 'isolate'})
        for index in range(len(ips)):
            t = CLI(ip=ips[index], c='show lldp neighbor summary', system_name=system_names[index])
            p.append(t)
        for t in p:
            t.start()
        for t in p:
            t.join()
        for t in p:
            tmp = t.get_result()
            if tmp != 'Wrong!!!':
                isolate = True
                flag = 0
                for item in tmp:
                    if flag == 0:
                        if '---------------' in item:
                            flag = 1
                    else:
                        if item == '\n':
                            break
                        toIP = item.split()[-3]
                        if len(toIP) >= 7:
                            # 防止出现连接到该系统以外的ip
                            if toIP in ips:
                                """Maojun modified the line with 'text' """
                                line = {'from': t.ip, 'to': toIP, 'text': 'lldp neighbor', }
                                lines.append(line)
                                nodes.append({
                                    'id': t.ip,
                                    'text': t.ip + '\n' + t.system_name
                                })
                                isolate = False
                if isolate:
                    if t.system_name in isolated_system:
                        line = {'from': t.ip, 'to': t.system_name}
                        lines.append(line)
                        nodes.append({
                            'id': t.ip,
                            'text': t.ip,
                            'color': '#ff8c00'
                        })
                    else:
                        # 创立isolated子节点
                        isolated_system.append(t.system_name)
                        nodes.append({
                            'id': t.system_name,
                            'text': t.system_name,
                            'color': '#ff8c00'
                        })
                        line = {'from': t.system_name, 'to': 'isolate'}
                        lines.append(line)
            else:
                nodes.append({
                    'id': t.ip,
                    'text': t.ip + '\n' + t.system_name,
                    'color': '#ff0000'
                })
                line = {'from': t.ip, 'to': 'isolate'}
                lines.append(line)
                error_ip.append(t.ip)

        # 把所有孤立的点连到该节点上，防止堆叠，并使得该节点透明
        nodes.append({'id': 'isolate',
                      'text': 'isolate',
                      'color': '#ff8c00'})

        # 将root节点更换颜色
        for item in nodes:
            if item['id'] == rootIP:
                item['color'] = '#43a2f1'
                break

        # 格式参照的前端RelationGraph组件的数据格式需求
        res = {
            'rootID': rootIP,
            'nodes': nodes,
            'lines': lines
        }
        sql = 'delete from lldp_neighbor'
        db.execute_db(sql)
        store = str(res).replace('\\n', '###')
        sql = f'insert into lldp_neighbor (`Result`) values (\"{store}\")'
        db.execute_db(sql)
    else:
        text = lldp_neighbor[0]['Result']
        res = ast.literal_eval(text)
        for item in res['nodes']:
            item['text'] = item['text'].replace('###', '\n')
    return jsonify(res, error_ip)


@app.route('/uploadTopoPic', methods=['POST'])
def uploadTopoPic():
    # download the JPG by click page right key then 'save image as'
    fd = request.files["file"]
    # name = secure_filename(fd.filename): 获取文件名
    name = 'Himalaya.png'
    fd.save(os.path.join(PICTURE_UPLOAD_PATH, secure_filename(name)))
    return "success"
