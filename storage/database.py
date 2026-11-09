
import json
from ingestion import raw
from process import extract_transforme


def toJson():
    rows = raw.toRows("data")
    data = []

    for row in rows:
        result = extract_transforme.extract(row)

        if result:
            data.append(result)

    with open("storage/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Conversion de auth.log vers JSON terminée !")
    print("Nombre de lignes traitées :", len(data))


if __name__ == "__main__":
    toJson()
