import json
from unittest import TestCase
from flask_jwt_extended import  create_access_token
from app import db, app, sqlpass, test
import mysql.connector

class TestVistaAsociarEquipoRol(TestCase):

    def setUp(self):
        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='candidatos',
            user='root',
            password='root')
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empleados',
            user='root',
            password='root')

        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='candidatos',
            user='root',
            password=sqlpass)
    
        self.client = app.test_client()
        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}
        
        sql = "DELETE FROM empresas.rol_ficha_trabajo WHERE id_ficha_trabajo in(401,101)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.ficha_trabajo WHERE id_empresa=101"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        sql = "DELETE FROM empresas.empresa WHERE id=101"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        sql_crear = "INSERT INTO empresas.empresa (id, tipo_doc, num_doc, nombre, email, telefono) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (101, "Test", "Test", "Test", "Test", "Test")
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql_crear = "INSERT INTO empresas.ficha_trabajo (id, nombre, id_empresa) VALUES (%s, %s, %s)"
        val = (401, "Ficha 4", 101)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
        sql_crear = "INSERT INTO empresas.ficha_trabajo (id, nombre, id_empresa) VALUES (%s, %s, %s)"
        val = (101, "Ficha 4", 101)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql_crear = "INSERT INTO empresas.rol_ficha_trabajo (id_ficha_trabajo, id_rol) VALUES (%s, %s)"
        val = (401,4)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()

        sql_crear = "INSERT INTO empresas.rol_ficha_trabajo (id_ficha_trabajo, id_rol) VALUES (%s, %s)"
        val = (101,4)
        cursor = self.connection.cursor()
        cursor.execute(sql_crear, val)
        self.connection.commit()
  
    def tearDown(self):
        sql = "DELETE FROM empresas.rol_ficha_trabajo WHERE id_ficha_trabajo=1 AND id_rol=2"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def test_add_rol_to_equipo_success(self):
        data = {"id_rol": 2, "id_equipo": 101}
        response = self.client.post("/equipos/rol/asociar",headers=self.headers ,data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["Mensaje"], "Rol asociado con Éxito")

    # def test_add_rol_to_equipo_duplicate(self):
    #     data = {"id_rol": 5, "id_equipo": 401}
    #     response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
    #     self.assertEqual(response.status_code, 409)

    def test_add_rol_to_equipo_missing_data(self):
        data = {"id_rol": 1} 
        response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 400)

    def test_add_rol_to_equipo_rol_not_found(self):
        data = {"id_rol": 300, "id_equipo": 101}
        response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_add_rol_to_equipo_equipo_not_found(self):
        data = {"id_rol": 1, "id_equipo": 300}
        response = self.client.post("/equipos/rol/asociar",headers=self.headers , data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_delete_rol_from_equipo_success(self):
        data = {"id_rol": 2, "id_equipo": 101}
        response = self.client.post("/equipos/rol/asociar",headers=self.headers ,data=json.dumps(data),
                                 content_type='application/json')
        params = {"id_rol": 2, "id_equipo": 101}
        response = self.client.delete("/equipos/rol/asociar", query_string=params,headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["Mensaje"], "Rol desasociado con Éxito")

    def test_delete_rol_from_equipo_not_found(self):
        params = {"id_rol": 300, "id_equipo": 101}
        response = self.client.delete("/equipos/rol/asociar", query_string=params,headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_rol_from_equipo_missing_params(self):
        response = self.client.delete("/equipos/rol/asociar",headers=self.headers)
        self.assertEqual(response.status_code, 400)
