import json

class GraphStorage:

    def __init__(self, path_to_storage_file):
        self.path_to_storage_file = path_to_storage_file
        self.data = self._load_data()



    def _load_data(self):
            try:
                with open(self.path_to_storage_file, mode='r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                  data = {}
            except json.decoder.JSONDecodeError:
                  data = {}
            return data
    
    def _save_data(self):
            try:
                with open(self.path_to_storage_file, mode='w', encoding='utf-8') as f:
                    json.dump(self.data, f, indent=4, ensure_ascii=False)
                return True
            except Exception:
                  return False

    def put(self, key, value):
            self.data[key] = value
            self._save_data()

    def get(self, key):
          return self.data.get(key)
    

if __name__ == "__main__":
    gs = GraphStorage('db.json')
    #   gs.put( 'img1', [('кот', 'рама', 'мыть'), ('мама', 'кот', 'гладить')] )
    #   gs.put( 'img2', [('мальчик1', 'мяч', 'бьет'), ('мяч', 'ворота', 'летит')] )
    print(gs.get('img3 ааа.jpg'))
    # gs.put( 'img3 ааа.jpg', [('мальчик2', 'мальчик1', 'бьет')] )

