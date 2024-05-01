from Models.entities.User import User

class ModelUser():
    @classmethod
    def logged_user(self,db,user):
        try:
            cursor=db.connection.cursor()
            QUERY="""SELECT IDADMIN,USERNAME,USERPASSWORD
                FROM tbl_administrator
                WHERE USERNAME='{}'""".format(user.USERNAME)
            cursor.execute(QUERY)
            answer=cursor.fetchone()
            if answer != None:
                user_logged=User(answer[0],answer[1],User.CheckPassword(answer[2],user.PASSWORD))
                return user_logged
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_id(self,db,ID):
        try:
            cursor=db.connection.cursor()
            QUERY="""SELECT IDADMIN,USERNAME
                FROM tbl_administrator
                WHERE IDADMIN={}""".format(ID)
            cursor.execute(QUERY)
            answer=cursor.fetchone()
            if answer != None:
                user_id=User(answer[0],answer[1],None)
                return user_id
            
            else:
                return None
        
        except Exception as ex:
            raise Exception(ex)