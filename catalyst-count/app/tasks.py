from celery import shared_task
import pandas as pd
import psycopg2
from io import StringIO
import os
from .models import UploadHistory
from decouple import config


def update_user_upload_history(id, status, progress):
    uploadHistory = UploadHistory.objects.get(id=id)
    uploadHistory.status = status
    uploadHistory.progress = progress
    uploadHistory.save()


@shared_task(bind=True)
def add_csv_data_to_db(self, filename, id):
    update_user_upload_history(id, "Reading file from disk", 10)
    file_path = os.path.join("uploads", filename)

    db_config = {
        "dbname": config("POSTGRES_DB"),
        "user": config("POSTGRES_USER"),
        "password": config("POSTGRES_PASSWORD"),
        "host": config("POSTGRES_HOST", default="localhost"),
        "port": config("POSTGRES_PORT", default="5432"),
    }

    expected_columns = {
        "Unnamed: 0": "uuid",
        "name": "name",
        "domain": "domain",
        "year founded": "year_founded",
        "industry": "industry",
        "size range": "size_range",
        "locality": "locality",
        "country": "country",
        "linkedin url": "linkedin_url",
        "current employee estimate": "current_employee_estimate",
        "total employee estimate": "total_employee_estimate",
    }

    chunk_size = 10000
    check_columns = 0
    missing_columns = []

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Open the CSV in chunks and process each chunk
        update_user_upload_history(id, "Processing chunk", 30)

        for chunk in pd.read_csv(file_path, chunksize=chunk_size):

            if check_columns == 0:
                # Check if all expected columns are present in the chunk
                missing_columns = [
                    col for col in expected_columns.keys() if col not in chunk.columns
                ]

                if len(missing_columns) > 0:
                    return

            check_columns = 1

            # Clean the data (rename columns, drop missing values, extract locality, etc.)
            chunk.rename(
                columns=expected_columns,
                inplace=True,
            )

            # Drop rows with missing 'name'
            chunk = chunk.dropna(subset=["name"])

            # Extract locality into city, state, country
            chunk[["city", "state", "country"]] = chunk["locality"].str.split(
                ",", expand=True
            )
            chunk["city"] = chunk["city"].str.strip()
            chunk["state"] = chunk["state"].str.strip()
            chunk["country"] = chunk["country"].str.strip()

            # Convert numeric fields to integers
            int_fields = [
                "year_founded",
                "current_employee_estimate",
                "total_employee_estimate",
            ]
            for field in int_fields:
                chunk[field] = pd.to_numeric(chunk[field], errors="coerce").astype(
                    "Int64"
                )

            # Ensure the columns are in the correct order and format
            # chunk = chunk[expected_columns.keys()]

            # Prepare CSV buffer
            csv_buffer = StringIO()
            chunk.to_csv(csv_buffer, index=False, header=False)
            csv_buffer.seek(0)

            # Copy the chunk into the database
            cursor.copy_expert(
                """
                COPY app_company (
                    uuid,
                    name,
                    domain,
                    year_founded,
                    industry,
                    size_range,
                    locality,
                    country,
                    linkedin_url,
                    current_employee_estimate,
                    total_employee_estimate,
                    city,
                    state
                )
                FROM STDIN
                WITH (FORMAT CSV, DELIMITER ',');
                """,
                csv_buffer,
            )

            update_user_upload_history(
                id, f"Processed chunk {chunk.index[0]} to {chunk.index[-1]}", 50
            )

        # Commit the transaction after all chunks are processed
        conn.commit()
        update_user_upload_history(id, "All data processed", 80)

        update_user_upload_history(id, "File uploaded", 100)
    except Exception as e:
        update_user_upload_history(id, str(e), 100)
        print(f"Error occurred: {e}")
    finally:
        # Close the database connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

        # Delete the file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

        if len(missing_columns) > 0:
            update_user_upload_history(
                id, f"Missing columns: {', '.join(missing_columns)}", 100
            )
