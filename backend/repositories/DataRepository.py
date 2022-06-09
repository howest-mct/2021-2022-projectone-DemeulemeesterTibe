from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens
    
    @staticmethod
    def insert_historiek(datum,waarde,commentaar,device,actie):
        sql = "insert into historiek (datum,waarde,commentaar,deviceID,actieID) VALUES (%s,%s,%s,%s,%s)"
        params = [datum,waarde,commentaar,device,actie]
        return Database.execute_sql(sql,params)
    
    @staticmethod
    def read_historiek_by_id(id):
        sql = "SELECT concat(datum) as datum,waarde,commentaar,h.deviceID,actieID,meeteenheid from historiek h join device d on h.deviceID = d.deviceID WHERE historiekid = %s"
        params = [id]
        return Database.get_one_row(sql, params)
    
    @staticmethod
    def read_alarmen():
        sql = "SELECT *,dayname(tijd) as dag,concat(time(tijd)) as tijdstip FROM alarm"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_alarmen_nog_komen():
        sql = "SELECT *,concat(time(tijd)) as tijdstip FROM smartwekker.alarm WHERE timestampdiff(second,now(),tijd) >0 and actief = 1 ORDER BY timestampdiff(second,now(),tijd);"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_alarm_by_id(id):
        sql = "SELECT *,dayname(tijd) as dag,concat(time(tijd)) as tijdstip,concat(tijd) as datetime FROM alarm WHERE alarmid = %s"
        payload = [id]
        return Database.get_one_row(sql,payload)
    
    @staticmethod
    def update_alarmActief0_by_id(id):
        sql = "UPDATE alarm set actief = 0 WHERE alarmid = %s"
        payload = [id]
        return Database.execute_sql(sql,payload)

    @staticmethod
    def update_alarm_by_id(id,naam,tijdstip,actief,herhaal):
        sql = "UPDATE alarm SET naam = %s, tijd = %s,actief = %s,herhaal = %s WHERE alarmid = %s"
        payload = [naam,tijdstip,actief,herhaal,id]
        return Database.execute_sql(sql,payload)
    
    @staticmethod
    def delete_alarm_by_id(id):
        sql = "DELETE FROM alarm WHERE alarmid = %s"
        payload = [id]
        return Database.execute_sql(sql,payload)

    @staticmethod
    def insert_alarm(naam,tijd,actief,herhaal):
        sql = "insert into alarm (naam,tijd,actief,herhaal) VALUES (%s,%s,%s,%s)"
        params = [naam,tijd,actief,herhaal]
        return Database.execute_sql(sql,params)
    
    @staticmethod
    def read_slaap():
        # sql = "SELECT *, TIMESTAMPDIFF(hour,starttijd,eindtijd) as hour, MOD(TIMESTAMPDIFF(minute,starttijd,eindtijd),60) as minutes,year(eindtijd)) as datum  FROM smartwekker.slaap;"
        sql = "SELECT *,timestampdiff(minute,starttijd,eindtijd) as sleptmin,concat(day(eindtijd),' ',monthname(eindtijd),' ',year(eindtijd)) as datum,concat(LPad(TIMESTAMPDIFF(hour,starttijd,eindtijd), 2, 0), '.', LPad(MOD(TIMESTAMPDIFF(minute,starttijd,eindtijd),60), 2, 0))as 'hoursMin' FROM smartwekker.slaap ORDER BY STARTTIJD;"
        return Database.get_rows(sql)

    @staticmethod
    def insert_slaap(start,eind):
        sql = "insert into slaap (starttijd,eindtijd) VALUES (%s,%s)"
        params = [start,eind]
        return Database.execute_sql(sql,params)
