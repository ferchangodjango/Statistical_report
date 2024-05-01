


class QueryDashboard():
    @classmethod
    def sample_upriver(self):
        QUERY="""SELECT SAMPLE_RIVER_UP
            FROM tbl_samplemeasure"""
        return QUERY

    @classmethod
    def sample_downriver(self):
        QUERY="""SELECT SAMPLE_RIVER_DOWN
            FROM tbl_samplemeasure"""
        return QUERY
    @classmethod
    def experiment_dependient_variable(self):
        QUERY="""SELECT AMONIAC_SAMPLE
        FROM tbl_experimentsample"""
        return QUERY
    @classmethod
    def experiment_independient_variable(self):
        QUERY="""SELECT FORCE_SAMPLE
        FROM tbl_experimentsample"""
        return QUERY
    
    @classmethod
    def regresion_data(self):
        QUERY="""SELECT FORCE_SAMPLE,AMONIAC_SAMPLE
        FROM tbl_experimentsample"""
        return QUERY

    @classmethod
    def boxplot_sampleriver(self):
        QUERY="""SELECT SAMPLE_RIVER_UP,SAMPLE_RIVER_DOWN
        FROM tbl_samplemeasure"""
        return QUERY
    
    @classmethod
    def insertquery(self,data):
        QUERY="""INSERT INTO tbl_experimentsample(ID_ENGINIEER,AMONIAC_SAMPLE,FORCE_SAMPLE)
            VALUES ('{0}','{1}','{2}')""".format(data['ID'],data['QUANTITY_AMONIAC'],data['FORCE_APPLY'])
        return QUERY
    
    @classmethod
    def querypareto(self):
        QUERY="""SELECT ID_ENGINIEER,COUNT(ID_ENGINIEER) AS QUANTITY
            FROM tbl_experimentsample
            GROUP BY ID_ENGINIEER
            ORDER BY QUANTITY DESC
            """
        return QUERY
