'''
This is the python program to create audit log trailts for mysql
This program will create the triggers and tables for the audit trait
'''
class Config:
    '''
    This class is to add the mysql table properties
    '''
    def conf_table_name(self):
        '''
        This function is to configure the table name
        '''
        #add table name here ..
        table_name = "table name"
        return table_name

    def conf_colomns(self):
        '''
        This function is to configure the field names
        '''
        #add table fields here ..
        colomns = [
            "field 1",
            "field 2",
            "field 3",
            "field 4",
            "field 5",
            "field 6",
            "field 7"
            ]
        return colomns
    def conf_primary_key(self):
        '''
        This function is to configure the primary key
        '''
        #add table primary key here ..
        primary_key = "id"
        return primary_key

LINE = "-------------------------------------------------------------------"
class Save:
    '''
    This class contain the file save functions
    '''
    def result(self,content,file_name):
        '''
        This function is to save the sql files created
        '''
        file_object = open(file_name, 'a')
        file_object.write(content)
        file_object.close()
class Doc:
    '''
    This class is to dispaly the instruction to user
    '''
    def how_to_use(self):
        '''
        How to use
        '''
        print('''
        ###############  HOW TO USE CREATED FILES #################################################
        ''')
        print('''
        STEP1 : Run the create_query.sql file in your mysql DB (to create Audit table)
        ''')
        print('''
        STEP2 : Run the insert_query.sql file in your mysql DB (to create Insert data trigger)
        ''')
        print('''
        STEP3 : Run the update_query.sql file in your mysql DB (to create update data trigger)
        ''')
        print('''
        STEP4 : Run the delete_query.sql file in your mysql DB (to create delete data trigger)
        ''')
        print('''
        ############################################################################################
        ''')
class DB:
    '''
    This class contain the functions to create the triggers and table
    for the audit trait
    '''
    def __init__(self) -> None:
        self.file_obj = Save()
    def create_audit_table(self):
        '''
        This is to create audit table
        '''
        print("[+] Creating Audit table")
        conf_obj = Config()
        table_name = conf_obj.conf_table_name()
        query= '''
        create table Audit_trail_'''+table_name+'''(id int NOT NULL AUTO_INCREMENT,
        '''+table_name+'''_id int NOT NULL,
        column_name varchar(255),
        old_value varchar(255),
        new_value varchar(255),
        done_by varchar(255) NOT NULL,
        done_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        operation varchar(255) NOT NULL,
        PRIMARY KEY (id));
        '''
        self.file_obj.result(query,'create_query.sql')
        print("[+] Audit table created")
        print("[*]Table Name : Audit_trail_"+table_name)
        print("[*]File Name : create_query.sql")
        print(LINE)
    def insert_trigger(self):
        '''
        This is to create db insert trigger
        '''
        print("[+] Creating insert trigger")
        conf_obj = Config()
        table_name = conf_obj.conf_table_name()
        primary_key = conf_obj.conf_primary_key()
        query_head = '''
        DELIMITER $$
        CREATE TRIGGER '''+table_name+'''_create
        AFTER INSERT
        ON '''+table_name+''' FOR EACH ROW
        BEGIN'''
        query = ""
        colomns_list = conf_obj.conf_colomns()
        for colomn in colomns_list:
            query = query + '''insert into Audit_trail_'''+str(table_name)+'''
            (
                '''+table_name+'_'+str(primary_key)+''',
                column_name,
                new_value,
                done_by,
                operation
            ) 
            values
            (
                NEW.'''+str(primary_key)+''',
                ''''+str(colomn)+'''',
                NEW.'''+str(colomn)+''',
                (SELECT CURRENT_USER()),
                'INSERT'
            );
            '''
        query_foot = """END$$
        DELIMITER ;"""
        trait_query = query_head+" "+query+" "+query_foot
        self.file_obj.result(trait_query,'insert_query.sql')
        print("[+] Insert Trigger query created")
        print("[*] Trigger Name : "+table_name+"_create")
        print("[*] File Name :insert_query.sql ")
        print(LINE)
    def delete_trigger(self):
        '''
        This is to create db delete trigger
        '''
        print("[+] Creating delete trigger")
        conf_obj = Config()
        table_name = conf_obj.conf_table_name()
        primary_key = conf_obj.conf_primary_key()
        query_head = '''
        DELIMITER $$
        CREATE TRIGGER '''+table_name+'''_delete
        AFTER DELETE
        ON '''+table_name+''' FOR EACH ROW
        BEGIN'''
        query = ""
        colomns_list = conf_obj.conf_colomns()
        for colomn in colomns_list:
            query = query + '''
            insert into Audit_trail_'''+str(table_name)+'''
            (
                '''+table_name+'_'+str(primary_key)+''',
                column_name,
                old_value,
                done_by,
                operation
            )
            values
            (
                OLD.'''+str(primary_key)+''',
                ''''+str(colomn)+'''',
                OLD.'''+str(colomn)+''',
                (SELECT CURRENT_USER()),
                'DELETED'
            );
            '''
        query_foot = """END$$
        DELIMITER ;"""
        trait_query = query_head+" "+query+" "+query_foot
        self.file_obj.result(trait_query,'delete_query.sql')
        print("[+] Delete Trigger query created")
        print("[*] Trigger Name : "+table_name+"_delete")
        print("[*] File Name :delete_query.sql ")
        print(LINE)
    def update_trigger(self):
        '''
        This is to create db update trigger
        '''
        print("[+] Creating update trigger")
        conf_obj = Config()
        table_name = conf_obj.conf_table_name()
        primary_key = conf_obj.conf_primary_key()
        query_head = '''DELIMITER $$
        CREATE TRIGGER '''+table_name+'''_update
        AFTER UPDATE
        ON '''+table_name+''' FOR EACH ROW
        BEGIN'''
        query = ""
        colomns_list = conf_obj.conf_colomns()
        for colomn in colomns_list:
            query = query + '''IF OLD.'''+str(colomn)+''' <> new.'''+str(colomn)+''' THEN
            insert into Audit_trail_'''+str(table_name)+'''
            ('''+table_name+'_'+str(primary_key)+''',
                column_name,
                old_value,
                new_value,
                done_by,
                operation
            ) 
            values
            (
                NEW.'''+str(primary_key)+''',
                "'''+str(colomn)+'''",
                OLD.'''+str(colomn)+''',
                NEW.'''+str(colomn)+''',
                (SELECT CURRENT_USER()),
                'UPDATE'
            );
            END IF;'''
        query_foot = '''END$$
        DELIMITER ;'''

        trait_query = query_head+" "+query+" "+query_foot
        self.file_obj.result(trait_query,'update_query.sql')
        print("[+] Update Trigger query created")
        print("[*] Trigger Name : "+table_name+"_update")
        print("[*] File Name :update_query.sql ")
        print(LINE)
def main():
    '''
    This is the main function that the execution start
    '''
    print("\n")
    print('''
    ░█████╗░██╗░░░██╗██████╗░██╗████████╗  ████████╗██████╗░░█████╗░██╗████████╗
    ██╔══██╗██║░░░██║██╔══██╗██║╚══██╔══╝  ╚══██╔══╝██╔══██╗██╔══██╗██║╚══██╔══╝
    ███████║██║░░░██║██║░░██║██║░░░██║░░░  ░░░██║░░░██████╔╝███████║██║░░░██║░░░
    ██╔══██║██║░░░██║██║░░██║██║░░░██║░░░  ░░░██║░░░██╔══██╗██╔══██║██║░░░██║░░░
    ██║░░██║╚██████╔╝██████╔╝██║░░░██║░░░  ░░░██║░░░██║░░██║██║░░██║██║░░░██║░░░
    ╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═╝░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░
    ''')
    print('''
    DBMS : MYSQL
    ''')
    print("\n")
    db_obj = DB()
    print("[+] Audit log maker started")
    print(LINE)
    try:
        db_obj.create_audit_table()
        db_obj.insert_trigger()
        db_obj.update_trigger()
        db_obj.delete_trigger()
        print("[+] Process Completed")
        doc_obj = Doc()
        doc_obj.how_to_use()
    except:
        print("[-] Something went wrong please check all things configured")
main()
    
