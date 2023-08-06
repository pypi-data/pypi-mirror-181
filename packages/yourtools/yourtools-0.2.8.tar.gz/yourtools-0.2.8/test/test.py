# from yourtools.WeChat import WeChat
from yourtools import WeChat
from yourtools import MySQL
from yourtools import Hive


def test_wechat():
    # 仲达（测试）
    zd_test = WeChat("ww06fa03084e27ff22", "uwYEfV7eyDL1y3IzkD_RvksxiA5UBvmJzWNP4ze8vjU", 1000116)
    data = {
        "touser": "1331811502877461564",
        "toparty": "",
        "totag": "",
        "msgtype": "text",
        "agentid": 1000116,
        "text": {
            "content": "你的快递已到，请携带工卡前往邮件中心领取。\n出发前可查看<a href=\"http://work.weixin.qq.com\">邮件中心视频实况</a>，聪明避开排队。"
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    send_statu = zd_test.send_msg(data)
    print(send_statu)


def test_mysql():
    dbconfg = {
        'host': '172.28.28.99',
        'port': 3308,
        'username': 'root',
        'password': 'Data@2022!',
        'db': 'test',
        'charset': 'utf8'
    }
    mysql = MySQL(dbconfg)
    # result = mysql.execute("insert into users_cdc(name,birthday,ts) values('灭霸2','2022-11-01 16:00:00','2022-11-01 16:00:00') ")
    result = mysql.query("select * from users_cdc")
    print(result)


def test_hive():
    hive_connection = {
        'host': 'emr-header-2',
        'port': 10000,
        'db': 'ods',
        'username': '',
        'auth': 'NOSASL'
    }
    hive = Hive(hive_connection)
    hive_sql = """
    select count(*) from dim.dim_clinic
    """
    rows = hive.query(hive_sql)
    print(rows)


def main():
    test_mysql()


if __name__ == '__main__':
    main()
