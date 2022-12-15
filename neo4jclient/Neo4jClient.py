from neo4j import GraphDatabase,unit_of_work
import pandas as pd


class Neo4jClient():
    """
    Neo4J DB Interface class
    """

    def __init__(self, *args, **kwargs):
        url = kwargs.get('url', 'bolt://54.68.133.241:7687/')
        username = kwargs.get('username', 'neo4j')
        password = kwargs.get('password', 'centraldev1100')
        database = kwargs.get('database', 'neo4j')
        self.client = GraphDatabase.driver(url, auth=(username, password), database=database)

    @unit_of_work(timeout=1200)
    def __run(self, tx, query, **kwargs):
        if kwargs.get('data_frame'):
            return pd.DataFrame([dict(record) for record in tx.run(query)])
        result = [row for row in tx.run(query)]
        return result

    def execute(self, query, **kwargs):
        with self.client.session() as session:
            tx = session.begin_transaction()
            result = self.__run(tx, query, **kwargs)
            tx.close()
            return result

    def read(self, query, **kwargs):
        with self.client.session() as session:
            return session.execute_read(self.__run, query, **kwargs)

    def write(self, **kwargs):
        tx_func = kwargs.get('tx_func',None)
        parameters = kwargs.get('parameters',None)
        with self.client.session() as session:
            return session.write_transaction(tx_func,parameters)



