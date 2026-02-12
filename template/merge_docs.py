from pathlib import Path

from docxtpl import DocxTemplate
import pandas as pd
import zipfile

doc = DocxTemplate("temp/template.docx")
df = pd.read_csv("temp/data.csv", dtype=str)

output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for index, row in df.iterrows():
    context = {
        "customer_name": row["CUSTOMER_NAME"],
        "id_card_number": row["ID_CARD_NUMBER"] ,
        "issue_date": row["ISSUE_DATE"] ,
        "issue_place": row["ISSUE_PLACE"] ,
        "date_of_birth": row["DATE_OF_BIRTH"]
    }
    doc.render(context)

    output_filename = f"output/{row["CUSTOMER_NAME"].replace(' ', '_')}_{row["MOBILE_PHONE"]}.docx"
    doc.save(output_filename)
    print(f"Đã tạo: {output_filename}")

zip_path = Path("output.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for file in output_dir.iterdir():
        zipf.write(file, arcname=file.name)

print(f"Đã tạo file ZIP: {zip_path}")