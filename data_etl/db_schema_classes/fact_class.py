class Fact:

    def __init__(self, feature_id, feature_value):
        self.feature_id = feature_id
        self.feature_value = feature_value

    def get_fact_insert_query(self):
        return "INSERT INTO fact(para_id, feature_id, feature_value) VALUES(currval('paragraph_para_id_seq'), " \
               + self.feature_id + ", " + self.feature_value + ");"