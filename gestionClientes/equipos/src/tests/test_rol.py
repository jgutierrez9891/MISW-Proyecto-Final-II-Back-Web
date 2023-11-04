import json
from unittest import TestCase
import mysql.connector
from faker import Faker
from flask_jwt_extended import create_access_token
from app import app, sqlpass, test


class TestRol(TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.data_factory = Faker()

        if test:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@0.0.0.0:3306/empresas'
            self.connection = mysql.connector.connect(host='0.0.0.0',
            database='empresas',
            user='root',
            password='root')
        else:
            self.connection = mysql.connector.connect(host='34.27.118.190',
            database='empresas',
            user='root',
            password=sqlpass)
        
        sql = "DELETE FROM empresas.rol_ficha_trabajo WHERE id_ficha_trabajo=1"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        sql = "insert into empresas.rol_ficha_trabajo (id_ficha_trabajo, id_rol) values (1,1);"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

        self.token_de_acceso = create_access_token(identity=123)
        self.headers ={'Content-Type': 'application/json',
                       "Authorization" : "Bearer "+str(self.token_de_acceso)}
    
    def test_1_detallar_rol_OK(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1],
            "lista_habilidades_tecnicas":[2]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 200)

    def test_2_detallar_rol_400(self):
        post_request = self.client.put("/equipos/rol",
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 400)
        
    def test_3_detallar_rol_404_rol_no_encontrado(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":-1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1],
            "lista_habilidades_tecnicas":[2]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 404)
        
    def test_4_detallar_rol_404_habilidad_blanda_no_encontrada(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1058],
            "lista_habilidades_tecnicas":[2]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 404)
        
    def test_5_detallar_rol_404_habilidad_tecnica_no_encontrada(self):
        post_request = self.client.put("/equipos/rol", 
        json={
            "id_rol":1,
            "titulo_rol":"rol prueba",
            "descripcion_rol":"descripcion prueba 1",
            "lista_habilidades_blandas":[1],
            "lista_habilidades_tecnicas":[1058]
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 404)
    
    def test_6_consultar_rol_equipo(self):
        get_request = self.client.get("/equipos/rol?equipo_id=1",headers=self.headers)
        self.assertEqual(get_request.status_code, 200)

    def test_7_asociar_rol_equipo(self):
        post_request = self.client.post("/equipos/rol/asociar", 
        json={
                "id_rol":1,
                "id_equipo": 1
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 200)

    def test_8_desasociar_rol_equipo(self):
        post_request = self.client.delete("/equipos/rol/asociar", 
        json={
                "id_rol":1,
                "id_equipo": 1
        },headers=self.headers)
        self.assertEqual(post_request.status_code, 200)
        
                
    def tearDown(self) -> None:
        return super().tearDown()