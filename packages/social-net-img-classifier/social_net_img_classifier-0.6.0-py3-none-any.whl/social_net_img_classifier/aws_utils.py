import boto3
import os
import traceback
from social_net_img_classifier.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME


class AwsS3:
    """
    :Date: 2022-08-10
    :Version: 0.2
    :Author: Joan Felipe Mendoza - Whale & Jaguar Consultants S.A.S.
    :Description: FUNCIONES AUXILIARES PARA OPERACIONES SOBRE S3
    """
    def __init__(self, bucket=BUCKET_NAME):
        """
        :Description: inicializar clase
        :param bucket: nombre del bucket en S3 (:type: string)
        """
        self.client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.bucket = bucket

    def upload_file(self, local_file, s3_filename):
        """
        :Description: cargar un archivo al bucket en S3
        :param local_file: ubicación del archivo local (:type: string)
        :param s3_filename: ubicación y nombre del archivo a crear en S3 (:type: string)
        :return: éxito o fracaso de la operación (:type: boolean)
        """
        try:
            if isinstance(local_file, str):
                self.client.upload_file(local_file, self.bucket, s3_filename)
            else:
                self.client.upload_fileobj(local_file, self.bucket, s3_filename)
            return True
        except Exception:
            print(f"Problemas con local_file: {local_file}, s3_filename: {s3_filename}")
            traceback.print_exc()
            return False

    def delete_file(self, s3_filename):
        """
        :Description: borrar un archivo del bucket en S3
        :param s3_filename: ubicación y nombre del archivo a borrar en S3 (:type: string)
        :return: éxito o fracaso de la operación (:type: boolean)
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=s3_filename)
            return True
        except Exception:
            print(f"Problemas con s3_filename: {s3_filename}")
            traceback.print_exc()
            return False

    def read_file(self, s3_filename):
        """
        :Description: leer un archivo desde un bucket en S3
        :param s3_filename: ubicación y nombre del archivo a leer (:type: string)
        :return: éxito o fracaso de la operación (:type: boolean)
        """
        data = self.client.get_object(Bucket=BUCKET_NAME, Key=s3_filename)
        return data['Body'].read()

    def copy_delete_file(self, s3_original_path, s3_dest_path):
        """
        :Description: mover un archivo un archivo dentro de un bucket en S3
        :param s3_original_path: ubicación original (:type: string)
        :param s3_dest_path: ubicación de destino (:type: string)
        :return: éxito o fracaso de la operación (:type: boolean)
        """
        try:
            copy_source = {'Bucket': self.bucket, 'Key': s3_original_path}
            self.client.copy_object(Bucket=self.bucket, CopySource=copy_source, Key=s3_dest_path)
            self.client.delete_object(Bucket=self.bucket, Key=s3_original_path)
            return True
        except Exception:
            print(f"Problemas con s3_original_path: {s3_original_path}, s3_dest_path: {s3_dest_path}")
            traceback.print_exc()
            return False

    def empty_bucket(self):
        """
        :Description: vaciar un bucket en S3
        :return: éxito o fracaso de la operación (:type: boolean)
        """
        try:
            client = boto3.resource(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
            client.Bucket(self.bucket).objects.all().delete()
            return True
        except Exception:
            print(f"Problemas vaciando bucket {BUCKET_NAME}")
            traceback.print_exc()
            return False

    def download_folder(self, s3_folder, local_dir=None):
        client = boto3.resource(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
        bucket = client.Bucket(self.bucket)
        for obj in bucket.objects.filter(Prefix=s3_folder):
            target = obj.key if local_dir is None \
                else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)

    def files_in_folder(self, folder=None, search_term=None):
        """
        :Description: listar archivos dentro de una ubicación específica en el bucket en S3
        :param folder: ubicación o carpeta en S3 (:type: string)
        :param search_term: término de búsqueda (:type: string)
        :return: éxito o fracaso de la operación (:type: boolean)
        """
        try:
            if folder is None:
                result = self.client.list_objects(Bucket=self.bucket, Delimiter="/")
            else:
                result = self.client.list_objects(Bucket=self.bucket, Prefix=f"{folder}/", Delimiter="/")
            if search_term is None:
                return [key["Key"] for key in result["Contents"] if key["Key"] != f"{folder}/"]
            else:
                return [key["Key"] for key in result["Contents"] if search_term in key["Key"]]
        except Exception:
            print(f"Problemas con folder: {folder}, search_term: {search_term}")
            traceback.print_exc()
            return []
