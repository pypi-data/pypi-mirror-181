import subprocess

class Shapefile():
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        subprocess.run([
            "shp2pgsql",
            self.filepath,
            self.table_name
        ])
