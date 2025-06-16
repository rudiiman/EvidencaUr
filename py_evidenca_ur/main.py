import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

DB_NAME = "work_records.db"

class WorkRecordDB:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS work_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                earnings REAL,
                start_time TEXT,
                end_time TEXT
            )
            """
        )
        self.conn.commit()

    def add_record(self, company, earnings, start_time, end_time):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO work_records (company, earnings, start_time, end_time) VALUES (?, ?, ?, ?)",
            (company, earnings, start_time, end_time),
        )
        self.conn.commit()

    def fetch_records(self):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT company, earnings, start_time, end_time FROM work_records ORDER BY id DESC"
        )
        return cur.fetchall()


class AddRecordPopup(Popup):
    def __init__(self, save_callback, **kwargs):
        super().__init__(title="Add Work Record", size_hint=(0.8, 0.8), **kwargs)
        self.save_callback = save_callback
        box = BoxLayout(orientation="vertical")
        self.company_input = TextInput(hint_text="Company")
        self.earnings_input = TextInput(hint_text="Earnings")
        self.start_input = TextInput(hint_text="Start Time (YYYY-MM-DD HH:MM)")
        self.end_input = TextInput(hint_text="End Time (YYYY-MM-DD HH:MM)")
        save_btn = Button(text="Save")
        save_btn.bind(on_release=self.save)
        box.add_widget(self.company_input)
        box.add_widget(self.earnings_input)
        box.add_widget(self.start_input)
        box.add_widget(self.end_input)
        box.add_widget(save_btn)
        self.add_widget(box)

    def save(self, instance):
        company = self.company_input.text.strip()
        earnings = self.earnings_input.text.strip()
        start = self.start_input.text.strip()
        end = self.end_input.text.strip()
        if not company:
            return
        try:
            earnings_val = float(earnings)
        except ValueError:
            earnings_val = 0.0
        self.save_callback(company, earnings_val, start, end)
        self.dismiss()


class WorkRecordApp(App):
    def build(self):
        self.db = WorkRecordDB()
        self.root = BoxLayout(orientation="vertical")
        add_btn = Button(text="Add Work Record", size_hint_y=None, height=50)
        add_btn.bind(on_release=self.open_add_popup)
        self.root.add_widget(add_btn)
        self.records_container = BoxLayout(orientation="vertical", size_hint_y=None)
        self.records_container.bind(minimum_height=self.records_container.setter("height"))
        scroll = ScrollView()
        scroll.add_widget(self.records_container)
        self.root.add_widget(scroll)
        self.refresh_records()
        return self.root

    def refresh_records(self):
        self.records_container.clear_widgets()
        for record in self.db.fetch_records():
            company, earnings, start, end = record
            label = Label(
                text=f"{company} | {earnings} | {start} - {end}",
                size_hint_y=None,
                height=40,
            )
            self.records_container.add_widget(label)

    def open_add_popup(self, instance):
        popup = AddRecordPopup(self.add_record)
        popup.open()

    def add_record(self, company, earnings, start_time, end_time):
        if not start_time:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        if not end_time:
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.db.add_record(company, earnings, start_time, end_time)
        self.refresh_records()


if __name__ == "__main__":
    WorkRecordApp().run()
