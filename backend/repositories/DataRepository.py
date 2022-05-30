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
    def insert_alarm(naam,tijd):
        sql = "insert into alarm (naam,tijd) VALUES (%s,%s)"
        params = [naam,tijd]
        print("test",params)
        return Database.execute_sql(sql,params)
    
    # @staticmethod
    # def read_status_lampen():
    #     sql = "SELECT * from lampen"
    #     return Database.get_rows(sql)


    # @staticmethod
    # def update_status_lamp(id, status):
    #     sql = "UPDATE lampen SET status = %s WHERE id = %s"
    #     params = [status, id]
    #     return Database.execute_sql(sql, params)

    # @staticmethod
    # def update_status_alle_lampen(status):
    #     sql = "UPDATE lampen SET status = %s"
    #     params = [status]
    #     return Database.execute_sql(sql, params)
