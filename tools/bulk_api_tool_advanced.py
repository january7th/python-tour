
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json, csv, threading
import requests
from concurrent.futures import ThreadPoolExecutor
from openpyxl import Workbook, load_workbook
from odf.opendocument import load as load_ods
from odf.table import Table, TableRow, TableCell
from odf.text import P

class BulkApiTool:
    def __init__(self, root):
        self.root = root
        root.title("Bulk API Tester")

        ttk.Label(root, text="URL").grid(row=0, column=0, sticky="w")
        self.url = tk.StringVar()
        ttk.Entry(root, textvariable=self.url, width=100).grid(row=0, column=1, sticky="ew")

        ttk.Label(root, text="Method").grid(row=1, column=0, sticky="w")
        self.method = tk.StringVar(value="POST")
        ttk.Combobox(root, textvariable=self.method,
                     values=["GET","POST","PUT","PATCH","DELETE"],
                     width=12).grid(row=1, column=1, sticky="w")

        ttk.Label(root, text="Bearer Token").grid(row=2, column=0, sticky="w")
        self.token = tk.StringVar()
        ttk.Entry(root, textvariable=self.token, width=100).grid(row=2, column=1, sticky="ew")

        ttk.Label(root, text="Payload(s)").grid(row=3, column=0, sticky="nw")
        self.payload = tk.Text(root, width=100, height=15)
        self.payload.grid(row=3, column=1)

        btn = ttk.Frame(root)
        btn.grid(row=4, column=1, sticky="w")

        ttk.Button(btn, text="Load JSON", command=self.load_json).pack(side="left")
        ttk.Button(btn, text="Load CSV", command=self.load_csv).pack(side="left")
        ttk.Button(btn, text="Load Excel/ODS", command=self.load_sheet).pack(side="left")
        ttk.Button(btn, text="Run", command=self.run).pack(side="left")
        ttk.Button(btn, text="Export Excel", command=self.export_excel).pack(side="left")

        ttk.Label(root, text="Result").grid(row=5, column=0, sticky="nw")
        self.result = tk.Text(root, width=100, height=15)
        self.result.grid(row=5, column=1)

        self.rows = []

    def load_json(self):
        p = filedialog.askopenfilename()
        if p:
            self.payload.delete("1.0", tk.END)
            self.payload.insert(tk.END, Path(p).read_text(encoding="utf-8"))

    def load_csv(self):
        p = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if not p:
            return
        data = []
        with open(p, newline='', encoding="utf-8") as f:
            for r in csv.DictReader(f):
                data.append(r)
        self.payload.delete("1.0", tk.END)
        self.payload.insert(tk.END, json.dumps(data, ensure_ascii=False, indent=2))

    def load_sheet(self):
        p = filedialog.askopenfilename(filetypes=[("Excel/ODS","*.xlsx *.ods")])
        if not p:
            return
        if p.endswith(".xlsx"):
            wb = load_workbook(p)
            ws = wb.active
            rows = list(ws.iter_rows(values_only=True))
            headers = [str(h) for h in rows[0]]
            data = []
            for row in rows[1:]:
                data.append({headers[i]: row[i] for i in range(len(headers))})
        else:
            doc = load_ods(p)
            tables = doc.getElementsByType(Table)
            table = tables[0]
            data_rows = []
            for row in table.getElementsByType(TableRow):
                vals = []
                for cell in row.getElementsByType(TableCell):
                    text = ''.join(t.data for p in cell.getElementsByType(P) for t in p.childNodes if hasattr(t, 'data'))
                    vals.append(text)
                if vals:
                    data_rows.append(vals)
            headers = data_rows[0]
            data = []
            for row in data_rows[1:]:
                data.append({headers[i]: row[i] if i < len(row) else "" for i in range(len(headers))})
        self.sheet_rows = data
        self.payload.delete("1.0", tk.END)
        self.payload.insert(tk.END, json.dumps(data[:5], ensure_ascii=False, indent=2))

    def request_one(self, idx, payload):
        headers = {"Content-Type":"application/json"}
        if self.token.get().strip():
            headers["Authorization"] = f"Bearer {self.token.get().strip()}"

        try:
            resp = requests.request(
                self.method.get(),
                self.url.get(),
                json=payload,
                headers=headers,
                timeout=60
            )
            return [idx, resp.status_code, resp.text[:5000]]
        except Exception as e:
            return [idx, "ERROR", str(e)]

    def run(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        self.result.delete("1.0", tk.END)
        self.rows.clear()

        try:
            data = json.loads(self.payload.get("1.0", tk.END))
        except Exception as e:
            messagebox.showerror("JSON Error", str(e))
            return

        if isinstance(data, dict):
            data = [data]

        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [ex.submit(self.request_one, i + 1, p) for i, p in enumerate(data)]

            for f in futures:
                row = f.result()
                self.rows.append(row)
                self.result.insert(
                    tk.END,
                    f"#{row[0]} | {row[1]}\n{row[2]}\n{'-'*80}\n"
                )

    def export_excel(self):
        if not self.rows:
            messagebox.showinfo("Info", "No results")
            return

        wb = Workbook()
        ws = wb.active
        ws.append(["RequestNo", "Status", "Response"])
        for r in self.rows:
            ws.append(r)

        p = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if p:
            wb.save(p)
            messagebox.showinfo("Done", "Exported")

root = tk.Tk()
BulkApiTool(root)
root.mainloop()
