import json
import random
from jsonschema import validate, ValidationError

JSON_DATA_FILE = 'albums.json'
JSON_SCHEMA_FILE = 'schema.json'


def load_json_data(file_path):
    """Загрузка JSON данных из файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return None
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный формат JSON в файле '{file_path}'.")
        return None


def validate_json_with_schema(data, schema_path):
    """Валидация JSON данных с использованием JSON Schema."""
    schema = load_json_data(schema_path)
    if not schema or not data:
        return False
    try:
        validate(instance=data, schema=schema)
        print(f"JSON данные валидны по схеме '{schema_path}'.")
        return True
    except ValidationError as e:
        print(f"JSON данные НЕ валидны по схеме '{schema_path}':")
        print(f"  Ошибка: {e.message}")
        print(f"  Путь: {list(e.path)}")
        return False
    except Exception as e:
        print(f"Произошла ошибка при валидации JSON: {e}")
        return False


def query_albums_by_genre(data, genre):
    """Получить все альбомы указанного жанра."""
    print(f"\n--- Альбомы жанра '{genre}' ---")
    results = [album for album in data if genre in album.get('genres', [])]
    if not results:
        print("Альбомы не найдены.")
    for album in results:
        print(
            f"- {album['title']} (Исполнители: {', '.join(album['artists'])})")
    return results


def query_genres_by_artist(data, artist_name):
    """Получить все жанры, в которых работал указанный исполнитель."""
    print(f"\n--- Жанры исполнителя '{artist_name}' ---")
    genres = set()
    for album in data:
        if artist_name in album.get('artists', []):
            for genre in album.get('genres', []):
                genres.add(genre)
    if not genres:
        print("Жанры не найдены или исполнитель не найден.")
    else:
        print(f"Жанры: {', '.join(sorted(list(genres)))}")
    return list(genres)


def query_albums_with_long_tracks(data, min_duration_seconds=300):
    """Получить все альбомы, в которых есть композиции длиннее X секунд."""
    print(
        f"\n--- Альбомы с композициями > {min_duration_seconds // 60} минут ---")
    results = []
    for album in data:
        for comp in album.get('compositions', []):
            if comp.get('duration_seconds', 0) > min_duration_seconds:
                results.append(album)
                break  # Достаточно одной такой композиции в альбоме
    if not results:
        print("Альбомы не найдены.")
    for album in results:
        print(f"- {album['title']}")
    return results


def generate_json_random_playlist(data, num_tracks=5):
    """Сформировать список воспроизведения из заданного количества композиций случайным образом."""
    print(f"\n--- Случайный плейлист из {num_tracks} композиций (JSON) ---")
    all_compositions_info = []
    for album in data:
        album_title = album.get('title', 'N/A')
        artist_names = album.get('artists', ['N/A'])
        for comp in album.get('compositions', []):
            all_compositions_info.append({
                "name": comp.get('name', 'N/A'),
                "duration_seconds": comp.get('duration_seconds', 0),
                "album": album_title,
                "artists": ", ".join(artist_names)
            })

    if not all_compositions_info:
        print("Композиции не найдены.")
        return

    num_to_select = min(num_tracks, len(all_compositions_info))
    selected_tracks = random.sample(all_compositions_info, num_to_select)

    for i, track in enumerate(selected_tracks, 1):
        minutes = track['duration_seconds'] // 60
        seconds = track['duration_seconds'] % 60
        print(
            f"{i}. {track['name']} ({minutes:02d}:{seconds:02d}) - {track['artists']} (Альбом: {track['album']})")


def custom_json_query(data):
    """
    Собственный запрос: "Получить альбомы, где количество композиций равно 3 И название альбома содержит 'The'"
    """
    print(f"\n--- Собственный JSON запрос: альбомы с 3 композициями и 'The' в названии ---")
    results = [
        album for album in data
        if len(album.get('compositions', [])) == 3 and "The" in album.get('title', "")
    ]
    if not results:
        print("Альбомы не найдены.")
    for album in results:
        print(f"- {album['title']}")
    return results


if __name__ == "__main__":
    music_data = load_json_data(JSON_DATA_FILE)
    if music_data:
        print("=== Валидация JSON ===")
        validate_json_with_schema(music_data, JSON_SCHEMA_FILE)

        print("\n=== \"Запросы\" к JSON данным ===")
        # a)
        query_albums_by_genre(music_data, "Progressive Rock")
        # b)
        query_genres_by_artist(music_data, "Queen")
        # c)
        query_albums_with_long_tracks(music_data, 300)  # 300 секунд = 5 минут
        # d)
        generate_json_random_playlist(music_data, num_tracks=3)
        # e)
        custom_json_query(music_data)
