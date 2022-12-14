# -*- coding: utf-8 -*-

import psycopg2
import pymysql
from app.settings import *

server_conn = pymysql.connect(database=SERVER_DATABASE, user=SERVER_USER, password=SERVER_PASSWORD,
                               host=SERVER_HOST, port=SERVER_PORT)
server_cur = server_conn.cursor()

local_conn = psycopg2.connect(database=LOCAL_DATABASE, user=LOCAL_USER, password=LOCAL_PASSWORD,
                              host=LOCAL_HOST, port=LOCAL_PORT)
local_cur = local_conn.cursor()


def getPersonInfo(pid, father_id, local_zp_id):
    # 自己的信息
    sql = "select surname, name, zi, hao, gender, generetion, `rank`, is_alive, ce_birth, ce_death," \
          "biography, epitaph from home_individual where id = {};".format(pid)
    server_cur.execute(sql)
    result = list(server_cur.fetchone())
    if result[4] == '0':
        result[4] = '男'
    else:
        result[4] = '女'
    if len(result[5]) == 0:
        result[5] =  1
    else:
        result[5]= int(result[5])
    if len(result[6]) == 0:
        result[6] =  1
    else:
        result[6]= int(result[6])
    if result[7] == '1':
        result[7] = "生"
    else:
        result[7] = "卒"
    result.append(str(father_id))
    result.append(local_zp_id)
    return result


def addPerson(person_info, flag=False):
    sql = "insert into person_info(family_name, name, zi, hao, sex, generation, ranknum, isLiving, date_birth, " \
          "date_dead, desc_living, desc_dead, father_id, zp_id) " \
          "values(" + str(person_info)[1:-1] + ");"
    local_cur.execute(sql)
    if flag:
        local_cur.execute("select currval('person_info_id_seq');")
        person_id = local_cur.fetchone()[0]
        return person_id


#  根据gid 得到始祖信息
def getAncestorId(gid):
    sql = "select id from home_individual where gene_id = (select title from home_genealogy where id = {} limit 1) order by id limit 1;".format(gid)
    server_cur.execute(sql)
    pid = server_cur.fetchone()[0]
    return pid


def getLocalZpId(gid):
    # 本地数据库：zp_info（id, zp_name, family_name, tag, area, build_year, contacts, phone, zp_desc）

    sql = "select title, sername, hall_title, location, contact, contact_phone, note " \
          "from home_genealogy where id={}".format(gid)
    server_cur.execute(sql)
    result = list(server_cur.fetchone())
    result[4] = str(result[4])
    local_zp_name = result[0]
    sql = "insert into zp_info(zp_name, family_name, tag, area, contacts, phone, zp_desc) " \
          "values({}) returning id;".format(str(result)[1:-1])
    local_cur.execute(sql)
    local_zp_id = local_cur.fetchone()[0]

    return local_zp_id, local_zp_name


def web2local(gid):
    server_conn.ping(reconnect=True)

    # 根据gid得到家谱信息插入到本地数据库
    local_zp_id, local_zp_name = getLocalZpId(gid)

    # 根据gid得到始祖的id
    ancestor_id = getAncestorId(gid)

    ancestor_info = getPersonInfo(ancestor_id, -1, local_zp_id)
    cur_generation = ancestor_info[5]
    local_id = addPerson(ancestor_info, True)

    server_pids = [ancestor_id]
    local_pids = [local_id]

    count = 0

    while len(server_pids) > 0 and count < 20:
        new_server_pids = []
        new_local_pids = []
        for i in range(len(server_pids)):
            # 妻子信息
            sql = "select id from home_individual where spouse_id = {};".format(server_pids[i])
            server_cur.execute(sql)
            server_spouse_ids = server_cur.fetchall()
            for spouse_id in server_spouse_ids:
                spouse_info = getPersonInfo(spouse_id[0], local_pids[i], local_zp_id)
                spouse_info[5] = str(cur_generation)  # 替换妻子的世代数为丈夫的世代数
                print(spouse_info)
                addPerson(spouse_info)

            # 子女信息
            sql = "select id from home_individual where farther_id = {};".format(server_pids[i])
            server_cur.execute(sql)
            children_ids = server_cur.fetchall()
            for child_id in children_ids:
                child_info = getPersonInfo(child_id[0], local_pids[i], local_zp_id)
                child_info[5] = str(cur_generation+1)
                print(child_info)
                childID = addPerson(child_info, True)
                if child_info[4] == '男':
                    new_local_pids.append(childID)
                    new_server_pids.append(child_id[0])
        cur_generation += 1
        count += 1
        local_pids = new_local_pids
        server_pids = new_server_pids

    server_conn.commit()
    server_conn.close()
    local_conn.commit()
    # local_conn.close()
    return local_zp_id, local_zp_name


if __name__ == '__main__':
    web2local(40, 53)
