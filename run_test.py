import subprocess
import time
import json
import csv
from pathlib import Path
import os

def run_locust_test(
    host: str = "http://localhost:8000",
    users: int = 10,
    spawn_rate: int = 10,
    duration: str = "1m",
    locustfile: str = "tester.py",
    stats_output_dir: str = "load_test_results"
):
    """Запускает Locust-тест и сохраняет статистику."""
    # Создаем папку для результатов
    output_dir = Path(stats_output_dir)
    output_dir.mkdir(exist_ok=True)

    # Генерируем имя файла с timestamp
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    stats_csv = output_dir / f"locust_stats_{timestamp}.csv"
    stats_json = output_dir / f"locust_stats_{timestamp}.json"

    # Команда для запуска Locust
    cmd = [
        "locust",
        "-f", locustfile,
        "--host", host,
        "--headless",
        "-u", str(users),
        "-r", str(spawn_rate),
        "-t", duration,
        "--csv", str(output_dir / "locust_stats"),  # Locust сам добавит timestamp
        "--json"  # Для вывода в JSON (если нужно)
    ]

    print(f"🚀 Запускаю тест: {cmd}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"❌ Ошибка при запуске Locust:\n{stderr.decode()}")
        return

    print("\n✅ Тест завершен. Собираю статистику...")

    # Чтение CSV-файла, который сгенерировал Locust
    stats_file = output_dir / "locust_stats_stats.csv"
    try:
        if stats_file.exists():
            with open(stats_file, "r") as f:
                csv_data = list(csv.DictReader(f))
            with open(stats_json, "w") as f:
                json.dump(csv_data, f, indent=2)
            print(f"📊 Результаты сохранены в:\n- {stats_csv}\n- {stats_json}")
        else:
            print("⚠️ Файл статистики не найден. Проверьте, что Locust завершился без ошибок.")
            return
    except Exception as e:
        print(f"⚠️ Ошибка при обработке файла статистики: {e}")
        return

    # Вывод сводки
    if csv_data:
        last_row = csv_data[-1]  # Берем последнюю запись (итоги)
        print("\n📌 Итоговая статистика:")
        print(f"Запросов: {last_row['Request Count']}")
        print(f"Ошибок: {last_row['Failure Count']} ({last_row['Failures/s']} ошибок/сек)")
        print(f"Средняя задержка: {last_row['Average Response Time']} мс")
        print(f"RPS: {last_row['Requests/s']}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Запуск нагрузочного теста с Locust.")
    parser.add_argument("--host", default="http://localhost:8000", help="URL тестируемого сервера")
    parser.add_argument("--users", type=int, default=10, help="Количество виртуальных пользователей")
    parser.add_argument("--spawn-rate", type=int, default=10, help="Скорость роста пользователей (в секунду)")
    parser.add_argument("--duration", default="1m", help="Длительность теста (например, 1m, 5m)")
    parser.add_argument("--locustfile", default="tester.py", help="Файл сценария Locust")
    parser.add_argument("--output-dir", default="load_test_results", help="Папка для сохранения результатов")

    args = parser.parse_args()

    run_locust_test(
        host=args.host,
        users=args.users,
        spawn_rate=args.spawn_rate,
        duration=args.duration,
        locustfile=args.locustfile,
        stats_output_dir=args.output_dir
    )
