from flet import *
import flet as ft
import mysql.connector

# Connection to DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flet_crud_db"
)
cursor = mydb.cursor()

def main(page: Page):
    nametxt = TextField(label="name")
    agetxt = TextField(label="age")

    # CREATE EDIT FIELDS
    edit_nametxt = TextField(label="name")
    edit_agetxt = TextField(label="age")
    edit_id = Text()

    mydt = DataTable(
        columns=[
            DataColumn(Text("id")),
            DataColumn(Text("name")),
            DataColumn(Text("age")),
            DataColumn(Text("actions")),
        ],
        rows=[]
    )

    # DELETE FUNCTION
    def deletebtn(e):
        try:
            sql = "DELETE FROM tbl_people WHERE id = %s"
            val = (e.control.data['id'],)
            cursor.execute(sql, val)
            mydb.commit()
            mydt.rows.clear()
            load_data()

            # SHOW SNACK BAR
            page.snack_bar = SnackBar(
                Text("Data Successfully Deleted", size=30),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

        except Exception as e:
            print(e)

        # CLEAR ENTRY FIELDS
        nametxt.value = ""
        agetxt.value = ""
        page.update()

    # UPDATE THE DATA
    def updateData(e):
        try:
            sql = "UPDATE tbl_people SET name= %s, age= %s WHERE id = %s"
            val = (edit_nametxt.value, edit_agetxt.value, edit_id.value)
            cursor.execute(sql, val)
            mydb.commit()

            dialog.open = False
            page.update()

            # CLEAR EDIT TEXTFIELDS
            edit_nametxt.value = ""
            edit_agetxt.value = ""
            edit_id.value = ""

            mydt.rows.clear()
            load_data()

            # SHOW SNACK BAR
            page.snack_bar = SnackBar(
                Text("Data Successfully Updated", size=30),
                bgcolor="yellow")
            page.snack_bar.open = True
            page.update()

        except Exception as e:
            print(e)

    # EDIT FUNCTION
    def editbtn(e):
        edit_nametxt.value = e.control.data['name']
        edit_agetxt.value = e.control.data['age']
        edit_id.value = e.control.data['id']

        page.dialog = dialog  # Set dialog directly on the page
        dialog.open = True
        page.update()

    # CREATE DIALOG SHOW WHEN YOU CLICK EDIT BUTTON
    dialog = AlertDialog(
        title=Text("Edit data"),
        content=Column([
            edit_nametxt,
            edit_agetxt
        ]),
        actions=[
            TextButton("Save", on_click=updateData)
        ]
    )

    def load_data():
        # GET ALL DATA FROM DATABASE AND PUSH TO DATATABLE
        cursor.execute("SELECT * FROM tbl_people")
        result = cursor.fetchall()

        # PUSH DATA TO DICT
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns, row)) for row in result]

        # LOOP AND PUSH
        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(row['id']))),
                        DataCell(Text(row['name'])),
                        DataCell(Text(str(row['age']))),
                        DataCell(
                            Row([
                                IconButton(
                                    icon=icons.DELETE,
                                    icon_color="red",
                                    data=row,
                                    on_click=deletebtn
                                ),
                                IconButton(
                                    icon=icons.EDIT,
                                    icon_color="blue",
                                    data=row,
                                    on_click=editbtn
                                ),
                            ])
                        )
                    ]
                )
            )
        page.update()

    # CALL FUNCTION WHEN THE APP OPENS FOR THE FIRST TIME
    load_data()

    def addtodb(e):
        try:
            sql = "INSERT INTO tbl_people(name, age) VALUES(%s,%s)"
            val = (nametxt.value, agetxt.value)
            cursor.execute(sql, val)
            mydb.commit()

            # CLEAR ROWS IN TABLE AND PUSH FROM DATABASE AGAIN
            mydt.rows.clear()
            load_data()

            # SHOW SNACK BAR
            page.snack_bar = SnackBar(
                Text("Data Successfully added", size=30),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(e)

        # CLEAR ENTRY FIELDS
        nametxt.value = ""
        agetxt.value = ""
        page.update()

    page.add(
        Column([
            nametxt,
            agetxt,
            ElevatedButton("Add to DB", on_click=addtodb),
            mydt
        ])
    )

ft.app(target=main)
