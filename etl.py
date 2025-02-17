# etl.py

from utils.config_loader import ConfigLoader
from data_processor.data_transformer import DataTransformer
from data_processor.sqlite_database import Database
from data_processor.dataframe import Dataframe

# Erzeuge den ConfigLoader um die YAML Konfigurationen zu laden
yaml_path = "config/database_configuration.yaml"
config_loader = ConfigLoader(yaml_path)


# CSV-Datei laden
csv_filename = config_loader.get_csv_config()
df = Dataframe(csv_filename)
df.load_data()


# Daten transformieren
transformer = DataTransformer(df)
transformed_data = transformer.transform()


# SQLite-Datenbank-Dateipfad laden
db_filename = config_loader.get_database_config()["location"]

with Database(db_filename) as db:

    # Inspection Data Tabelle erstellen
    create_table_query = config_loader.get_queries()["create_table"]
    db.create_table(create_table_query)

    # Daten in die Tabelle einfügen
    insert_data_query = config_loader.get_queries()["insert_data"]
    db.insert_data(transformed_data, insert_data_query)

print("ETL-Prozess abgeschlossen. Daten wurden erfolgreich in die Datenbank geladen.")