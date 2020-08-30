import cx_Oracle
import datetime as dt
from typing import List, Tuple


class MinWiseDemandInsertionRepo():
    """repository to push min wise demand of entities to db.
    """

    def __init__(self, con_string: str) -> None:
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string

    def insertMinWiseDemand(self, data: List[Tuple]) -> bool:
        """Insert  min wise demand of entities to db
        Args:
            self : object of class 
            data (List[Tuple]): (timestamp, entity_tag, demand_value)
        Returns:
            bool: return true if insertion is successful else false
        """
        
        # making list of tuple of timestamp(unique),entity_tag based on which deletion takes place before insertion of duplicate

        existingEntityRows = [(x[0],x[1]) for x in data]

        try:
            
            connection = cx_Oracle.connect(self.connString)
            isInsertionSuccess = True

        except Exception as err:
            print('error while creating a connection', err)
        else:
            print(connection.version)
            try:
                cur = connection.cursor()
                try:
                    cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                    del_sql = "DELETE FROM raw_minwise_demand WHERE time_stamp = :1 and entity_tag=:2"
                    cur.executemany(del_sql, existingEntityRows)
                    insert_sql = "INSERT INTO raw_minwise_demand(time_stamp,ENTITY_TAG,demand_value) VALUES(:1, :2, :3)"
                    cur.executemany(insert_sql, data)
                except Exception as e:
                    print("error while insertion/deletion->", e)
                    isInsertionSuccess = False
            except Exception as err:
                print('error while creating a cursor', err)
                isInsertionSuccess = False
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
        return isInsertionSuccess