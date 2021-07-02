from os.path import dirname, exists, join


class DataLoader:
    @staticmethod
    def load_from_file(filename):
        if not exists(filename):
            filename = join(dirname(__file__), filename)

        try:
            with open(filename, 'r') as f:
                data = [line.strip('\r\n ') for line in f]
        except OSError as e:
            raise ValueError(f'Can\'t open/read file: {filename}.')

        return data
