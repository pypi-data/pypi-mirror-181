

class DatoCommonInterface(object):
    def wait(self):
        pass

    def list_tables(self):
        pass


class DatoGenInterface(DatoCommonInterface):
    def get_generated_data(self):
        pass

    def get_generated_data_csv(self, table_name: str = None):
        pass
