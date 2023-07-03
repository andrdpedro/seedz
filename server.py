import data_base
import json
import uvicorn

from fastapi import FastAPI, Response, status

app = FastAPI()
data_base.create_db()

if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, log_level="info", workers=6)
else:
    @app.post("/weather/add_data", status_code=200)
    async def add_weather_data(
        id: int,
        date: str,
        precipitation: int,
        high_temperature: int,
        relative_humidity: int,
        evaporation: int
    ):
        """
        Rota responsável por adicionar novos dados ao banco de dados.\n
        id: id da cidade;\n
        date: data dos dados adicionados(aaaa-mm-dd);\n
        precipitation: precipitação;\n
        high_temperature: temperatura máxima;\n
        relative_humidity: humidade relativa;\n
        evaporation: evaporação.\n
        """
        data = data_base.add_weather_data(id, date, precipitation, high_temperature, relative_humidity, evaporation)
        return json.loads(data)


    @app.get("/weather/ids", status_code=200)
    async def get_ids(
        response: Response,
    ):
        """
        Rota responsável por retornar todos os ids e nomes de cidades cadastrados no banco de dados!
        """
        cities_name = data_base.get_cities_ids_names()
        return json.loads(cities_name)
    

    @app.get("/weather/get_data", status_code=200)
    async def find_weather_data(
        response: Response,
        id: int,
        year: str=0,
        month: str=0,
        day: str=0
    ):
        """
        Rota responsável por retornar os dados existentes no banco de dados a partir do id, ano, mês e dia.\n
        id: id da cidade;\n
        year: data dos dados adicionados;\n
        month: precipitação;\n
        day: temperatura máxima;\n
        """
        data = data_base.get_weather_data(id, year, month, day)
        return json.loads(data)
    

    @app.delete("/weather/delete_data", status_code=200)
    async def delete_weather_data(
        response: Response,
        id: int,
        year: str=0,
        month: str=0,
        day: str=0
    ):
        """
        Rota responsável por deletar dados do banco de dados!\n
        id: id da cidade;\n
        year: data dos dados adicionados;\n
        month: precipitação;\n
        day: temperatura máxima;\n
        """
        message, data,  code = data_base.delete_weather_data(id, year, month, day)
        response.status_code = code
        return {
            "Message: ": message,
            "Status Code: ":response.status_code,
            "Data": json.loads(data)
        }
    

    @app.put("/weather/update_data", status_code=200)
    async def update_weather_data(
        response: Response,
        id: int,
        date: str,
        precipitation: int,
        high_temperature: int,
        relative_humidity: int,
        evaporation: int
    ):
        """
        Rota responsável por atualizar valores do banco de dados!\n
        id: id da cidade;\n
        date: data dos dados adicionados(aaaa-mm-dd);\n
        precipitation: precipitação;\n
        high_temperature: temperatura máxima;\n
        relative_humidity: humidade relativa;\n
        evaporation: evaporação.\n
        """
        message, data,  code = data_base.update_weather_data(id, date, precipitation, high_temperature, relative_humidity, evaporation)
        
        response.status_code = code
        return {
            "Message: ": message,
            "Status Code: ":response.status_code,
            "Data": json.loads(data)
        }
    